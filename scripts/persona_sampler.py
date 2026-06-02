#!/usr/bin/env python3
"""Lightweight persona sampler for persona-drilldown-lab.

Reads constant persona dimensions from JSON and prints random persona cards as text.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any


def default_constants_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "persona_constants.json"


def load_constants(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    required = [
        "age_groups",
        "regions",
        "jobs",
        "money_states",
        "digital_literacy",
        "core_fears",
        "hidden_desires",
        "attention_biases",
        "reaction_styles",
        "weird_modifiers",
        "idea_patterns",
    ]
    missing = [key for key in required if key not in data or not data[key]]
    if missing:
        raise SystemExit(f"constants file is missing required non-empty keys: {', '.join(missing)}")
    return data


def pick_many(rng: random.Random, items: list[str], min_count: int = 2, max_count: int = 4) -> list[str]:
    n = min(len(items), rng.randint(min_count, max_count))
    return rng.sample(items, n)


def build_persona(index: int, rng: random.Random, data: dict[str, Any], outlier_rate: float) -> dict[str, Any]:
    is_outlier = rng.random() < outlier_rate
    attention_biases = pick_many(rng, data["attention_biases"])
    persona = {
        "index": index,
        "age_group": rng.choice(data["age_groups"]),
        "region": rng.choice(data["regions"]),
        "job": rng.choice(data["jobs"]),
        "money_state": rng.choice(data["money_states"]),
        "digital_literacy": rng.choice(data["digital_literacy"]),
        "core_fear": rng.choice(data["core_fears"]),
        "hidden_desire": rng.choice(data["hidden_desires"]),
        "attention_biases": attention_biases,
        "reaction_style": rng.choice(data["reaction_styles"]),
        "weird_modifier": rng.choice(data["weird_modifiers"]) if is_outlier else None,
        "is_outlier": is_outlier,
    }
    return persona


def persona_title(persona: dict[str, Any]) -> str:
    base = f"{persona['age_group']} · {persona['region']} · {persona['job']}"
    if persona["weird_modifier"]:
        return f"{base} · {persona['weird_modifier']}"
    return base


def render_persona(persona: dict[str, Any], news: str) -> str:
    outlier_label = "이상치" if persona["is_outlier"] else "일반"
    keywords = ", ".join(persona["attention_biases"])
    return "\n".join(
        [
            f"페르소나 {persona['index']} [{outlier_label}] {persona_title(persona)}",
            f"- 돈/상황: {persona['money_state']}",
            f"- 디지털 감각: {persona['digital_literacy']}",
            f"- 핵심 두려움: {persona['core_fear']}",
            f"- 숨은 욕망: {persona['hidden_desire']}",
            f"- 관심 편향: {keywords}",
            f"- 반응 스타일: {persona['reaction_style']}",
            f"- 이 뉴스와 연결점: '{news}'를 {keywords} 관점에서 해석할 가능성이 큼",
        ]
    )


def render_idea_patterns(data: dict[str, Any], rng: random.Random, count: int = 2) -> str:
    patterns = rng.sample(data["idea_patterns"], min(count, len(data["idea_patterns"])))
    lines = ["아이디어 컨셉 후보 패턴:"]
    for pattern in patterns:
        lines.append(f"- {pattern['name']}: {pattern['description']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample persona cards from persona-drilldown-lab constants.")
    parser.add_argument("--news", required=True, help="News/event/signal text to attach to sampled personas.")
    parser.add_argument("--count", type=int, default=4, help="Number of personas to print.")
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed for deterministic output.")
    parser.add_argument("--outlier-rate", type=float, default=0.35, help="Probability that a persona receives a weird modifier.")
    parser.add_argument("--constants", type=Path, default=default_constants_path(), help="Path to persona constants JSON.")
    parser.add_argument("--with-patterns", action="store_true", help="Also print sampled idea concept patterns.")
    args = parser.parse_args()

    if args.count < 1:
        raise SystemExit("--count must be at least 1")
    if not 0 <= args.outlier_rate <= 1:
        raise SystemExit("--outlier-rate must be between 0 and 1")

    rng = random.Random(args.seed)
    data = load_constants(args.constants)

    print(f"뉴스/시그널: {args.news}")
    print(f"샘플 수: {args.count}")
    print("-" * 48)
    for i in range(1, args.count + 1):
        persona = build_persona(i, rng, data, args.outlier_rate)
        print(render_persona(persona, args.news))
        if i != args.count:
            print()
    if args.with_patterns:
        print("\n" + "-" * 48)
        print(render_idea_patterns(data, rng))


if __name__ == "__main__":
    main()
