#!/usr/bin/env python3
"""Build expanded persona constants from Hugging Face persona rows.

Default source: nvidia/Nemotron-Personas-Korea via Hugging Face datasets-server.
This script deliberately writes a compact JSON constant file, not the full raw dataset.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import urllib.parse
import urllib.request
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any, Iterable

DATASET = "nvidia/Nemotron-Personas-Korea"
DATASET_SERVER_ROWS = "https://datasets-server.huggingface.co/rows"
DATASET_SERVER_FIRST_ROWS = "https://datasets-server.huggingface.co/first-rows"

DEFAULT_CORE_FEARS = [
    "AI와 자동화 때문에 내 일이 사라지는 것",
    "물가와 생활비가 계속 올라 감당하지 못하는 것",
    "젊은 세대나 디지털 도구에 뒤처지는 것",
    "노후자금이 부족해지는 것",
    "가족에게 경제적 부담이 되는 것",
    "지역경제가 쇠퇴하고 기회가 줄어드는 것",
    "건강이 나빠져 현재 일을 계속하지 못하는 것",
    "투자나 대출에서 잘못된 선택을 하는 것",
    "사기성 정보나 과장 광고에 속는 것",
    "내 경험이 더 이상 쓸모없어지는 것",
    "자녀 교육이나 주거 비용을 감당하지 못하는 것",
    "소상공인 매출이 줄고 고정비만 늘어나는 것",
]

DEFAULT_HIDDEN_DESIRES = [
    "복잡한 뉴스를 내 상황에 맞게 쉽게 번역받고 싶음",
    "작게라도 추가 수입이나 부업 기회를 만들고 싶음",
    "내 경험이 아직 가치 있다는 것을 증명하고 싶음",
    "불안을 체크리스트와 행동 계획으로 바꾸고 싶음",
    "가족이나 주변 사람에게 쓸모 있는 정보를 전달하고 싶음",
    "남들보다 먼저 기회를 알아차리고 싶음",
    "시간과 체력을 아끼면서 더 효율적으로 일하고 싶음",
    "디지털 도구를 배우되 너무 어렵지 않게 시작하고 싶음",
    "지역이나 업종 변화에서 나만의 틈새를 찾고 싶음",
    "돈 문제를 숫자와 시나리오로 명확하게 보고 싶음",
]

DEFAULT_REACTION_STYLES = [
    "처음엔 의심하지만 실제 사례를 보면 빠르게 관심을 보임",
    "숫자, 계산기, 비교표가 있어야 신뢰함",
    "주변 사람 반응을 확인한 뒤 따라 움직임",
    "위험을 먼저 보고 천천히 검토함",
    "기회라고 느끼면 바로 검색하고 저장함",
    "짧은 영상이나 카드뉴스로 이해해야 반응함",
    "가족 단톡방이나 지역 커뮤니티에 공유하며 판단함",
    "전문가 권위보다 생활 사례에 더 설득됨",
    "무료 도구를 먼저 써보고 복잡하면 포기함",
    "자신의 업종/지역에 맞는 예시가 있어야 움직임",
]

DEFAULT_VALUE_ORIENTATIONS = [
    "안정과 예측 가능성을 중시함",
    "가족 책임과 체면을 강하게 느낌",
    "새로운 기술에는 호기심이 있지만 손실을 싫어함",
    "지역 커뮤니티의 평판과 소속감을 중요하게 여김",
    "돈보다 시간과 건강의 균형을 중시함",
    "자기계발과 배움으로 불안을 줄이려 함",
    "전문가 설명보다 주변의 검증된 사례를 신뢰함",
    "작은 실험을 통해 가능성을 확인하고 싶어함",
]

DEFAULT_MONEY_TRIGGERS = [
    "전기요금", "가스비", "대출이자", "월세", "전세", "원가율", "배달 앱 수수료", "광고비",
    "식비", "교육비", "병원비", "노후자금", "부업 수입", "주식 손실", "부동산 경기", "세금",
]

DEFAULT_TECH_TRIGGERS = [
    "AI", "챗GPT", "자동화", "데이터센터", "반도체", "로봇", "전력망", "클라우드",
    "AI 마케팅", "AI 세무", "AI 교육", "콘텐츠 제작", "리뷰 자동화", "업무 자동화",
]

DEFAULT_SOCIAL_TRIGGERS = [
    "지역 소외", "일자리 변화", "고령화", "자녀 세대 격차", "소상공인 위기", "맘카페 여론",
    "가족 단톡방", "동네 커뮤니티", "교육 경쟁", "노후 불안", "건강 불안", "이민/해외 기회",
]

DEFAULT_IDEA_PATTERNS = [
    {"name": "진단기", "description": "개인 입력을 받아 나에게 어떤 영향이 오는지 쉬운 리포트로 번역한다."},
    {"name": "계산기", "description": "복잡한 정책/경제/기술 변화를 돈·시간·위험 수치로 바꾼다."},
    {"name": "시나리오 카드", "description": "미래 가능성을 여러 갈래 카드로 보여준다."},
    {"name": "행동 체크리스트", "description": "불안을 바로 실행 가능한 다음 행동으로 바꾼다."},
    {"name": "비교 지도", "description": "지역/직업/연령별 영향을 비교해서 보여준다."},
    {"name": "업종별 번역기", "description": "같은 뉴스를 업종별 영향과 실행 과제로 번역한다."},
    {"name": "생활비 영향 리포트", "description": "거시 뉴스를 생활비 항목별 영향으로 풀어준다."},
    {"name": "부업 실험 과제", "description": "뉴스 시그널을 30분짜리 부업/콘텐츠 실험으로 바꾼다."},
    {"name": "커뮤니티 질문 생성기", "description": "사람들이 실제로 물어볼 질문과 댓글 포인트를 만든다."},
    {"name": "리스크 알림", "description": "과장 광고나 투자 오해로 이어질 수 있는 위험을 경고한다."},
]


def unique_add(bucket: OrderedDict[str, None], value: str | None, max_len: int = 80) -> None:
    if not value:
        return
    value = normalize_text(value)
    if not value or len(value) > max_len:
        return
    bucket[value] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    text = re.sub(r"\s+", " ", text)
    return text.strip(" |,;/")


def remove_korean_name_prefix(text: str) -> str:
    """Remove synthetic row names so constants stay archetypal."""
    return re.sub(r"^[가-힣]{2,4}\s*씨는\s*", "", text)


def split_list_field(value: Any) -> list[str]:
    if isinstance(value, list):
        return [p for p in (normalize_text(x) for x in value) if p]
    text = normalize_text(value)
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list):
                return [p for p in (normalize_text(x) for x in parsed) if p]
        except (SyntaxError, ValueError):
            pass
    parts = re.split(r"\s*[|,;/、]\s*", text)
    return [p for p in (normalize_text(x) for x in parts) if p]


def age_group(age: Any) -> str | None:
    try:
        n = int(age)
    except (TypeError, ValueError):
        return None
    if n < 20:
        return "10대"
    if n >= 80:
        return "80대 이상"
    return f"{n // 10 * 10}대"


def region_archetype(row: dict[str, Any]) -> str | None:
    province = normalize_text(row.get("province"))
    district = normalize_text(row.get("district"))
    if not province and not district:
        return None
    if "서울" in province and district in {"강남구", "서초구", "송파구"}:
        return "서울 강남권"
    if any(x in province for x in ["서울", "경기", "인천"]):
        return "수도권 생활권"
    if any(x in province for x in ["부산", "대구", "광주", "대전", "울산"]):
        return "광역시 생활권"
    if any(x in district for x in ["군", "읍", "면"]):
        return "농어촌 생활권"
    return "지방 도시 생활권"


def fetch_rows(dataset: str, config: str, split: str, offsets: Iterable[int], length: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset in offsets:
        params = urllib.parse.urlencode({"dataset": dataset, "config": config, "split": split, "offset": offset, "length": length})
        url = f"{DATASET_SERVER_ROWS}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "persona-drilldown-lab/1.0"})
        payload = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=45) as resp:
                    payload = json.load(resp)
                break
            except Exception as exc:  # noqa: BLE001 - CLI should tolerate transient HF errors.
                if attempt == 2:
                    print(f"warning: skipping offset {offset} after fetch error: {exc}", file=sys.stderr)
                else:
                    time.sleep(1 + attempt)
        if payload is None:
            continue
        for item in payload.get("rows", []):
            row = item.get("row", item)
            if isinstance(row, dict):
                rows.append(row)
    return rows


def fetch_first_rows(dataset: str, config: str, split: str) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"dataset": dataset, "config": config, "split": split})
    url = f"{DATASET_SERVER_FIRST_ROWS}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "persona-drilldown-lab/1.0"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        payload = json.load(resp)
    rows = []
    for item in payload.get("rows", []):
        row = item.get("row", item)
        if isinstance(row, dict):
            rows.append(row)
    return rows


def load_fixture(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for item in payload.get("rows", payload if isinstance(payload, list) else []):
        row = item.get("row", item) if isinstance(item, dict) else None
        if isinstance(row, dict):
            rows.append(row)
    return rows


def build_constants(rows: list[dict[str, Any]], max_items: int) -> dict[str, Any]:
    buckets = {name: OrderedDict() for name in [
        "age_groups", "sex", "marital_status", "family_type", "housing_type", "education_level",
        "provinces", "districts", "region_archetypes", "occupations", "work_contexts", "skills",
        "career_goals", "hobbies", "food_patterns", "travel_patterns", "family_situations",
        "persona_seeds", "cultural_backgrounds",
    ]}
    for row in rows:
        unique_add(buckets["age_groups"], age_group(row.get("age")))
        for src, dest in [
            ("sex", "sex"), ("marital_status", "marital_status"), ("family_type", "family_type"),
            ("housing_type", "housing_type"), ("education_level", "education_level"), ("province", "provinces"),
            ("district", "districts"), ("occupation", "occupations"), ("career_goals_and_ambitions", "career_goals"),
            ("cultural_background", "cultural_backgrounds"),
        ]:
            unique_add(buckets[dest], row.get(src), max_len=160 if dest in {"career_goals", "cultural_backgrounds"} else 80)
        unique_add(buckets["region_archetypes"], region_archetype(row))
        unique_add(buckets["work_contexts"], summarize_sentence(row.get("professional_persona")), max_len=160)
        unique_add(buckets["food_patterns"], summarize_sentence(row.get("culinary_persona")), max_len=160)
        unique_add(buckets["travel_patterns"], summarize_sentence(row.get("travel_persona")), max_len=160)
        unique_add(buckets["family_situations"], summarize_sentence(row.get("family_persona")), max_len=160)
        unique_add(buckets["persona_seeds"], summarize_sentence(row.get("persona")), max_len=180)
        for item in split_list_field(row.get("skills_and_expertise_list") or row.get("skills_and_expertise")):
            unique_add(buckets["skills"], item)
        for item in split_list_field(row.get("hobbies_and_interests_list") or row.get("hobbies_and_interests")):
            unique_add(buckets["hobbies"], item)

    def take(name: str) -> list[str]:
        return list(buckets[name].keys())[:max_items]

    attention = unique(DEFAULT_MONEY_TRIGGERS + DEFAULT_TECH_TRIGGERS + DEFAULT_SOCIAL_TRIGGERS + take("hobbies") + take("skills"))[:max_items]
    weird_modifiers = unique([
        "가족 단톡방의 정보 전달자", "동네 커뮤니티 헤비 유저", "새벽 경제 유튜브 시청자", "중고거래 고수",
        "AI 도구를 몰래 연습 중", "한때 투자 손실을 크게 겪음", "지역 축제 기획 경험 있음", "문화센터 수강생",
        "배달 앱 리뷰에 집착함", "가게 원가표를 직접 엑셀로 관리함", "자녀에게 AI를 배우는 중", "퇴직 후 강의를 꿈꿈",
    ] + take("hobbies") + take("career_goals"))[:max_items]

    return {
        "schema_version": 2,
        "sources": [{"dataset": DATASET, "license": "cc-by-4.0", "note": "Compact derived constants; raw rows are not vendored."}],
        "demographics": {
            "age_groups": take("age_groups") or ["20대", "30대", "40대", "50대", "60대", "70대"],
            "sex": take("sex"),
            "marital_status": take("marital_status"),
            "family_type": take("family_type"),
            "housing_type": take("housing_type"),
            "education_level": take("education_level"),
        },
        "geography": {"provinces": take("provinces"), "districts": take("districts"), "region_archetypes": take("region_archetypes")},
        "work": {"occupations": take("occupations"), "work_contexts": take("work_contexts"), "skills": take("skills"), "career_goals": take("career_goals")},
        "life": {"hobbies": take("hobbies"), "food_patterns": take("food_patterns"), "travel_patterns": take("travel_patterns"), "family_situations": take("family_situations")},
        "psychology": {
            "core_fears": DEFAULT_CORE_FEARS[:max_items],
            "hidden_desires": DEFAULT_HIDDEN_DESIRES[:max_items],
            "reaction_styles": DEFAULT_REACTION_STYLES[:max_items],
            "value_orientations": DEFAULT_VALUE_ORIENTATIONS[:max_items],
        },
        "attention": {"attention_biases": attention, "money_triggers": DEFAULT_MONEY_TRIGGERS[:max_items], "technology_triggers": DEFAULT_TECH_TRIGGERS[:max_items], "social_triggers": DEFAULT_SOCIAL_TRIGGERS[:max_items]},
        "outlier": {"weird_modifiers": weird_modifiers, "contradictions": ["전통적이지만 AI에 호기심이 많음", "디지털을 두려워하지만 새 앱은 빨리 설치함", "안정을 원하지만 부업 실험을 계속함", "지역을 떠나고 싶지만 동네 평판에 민감함"]},
        "persona_seeds": take("persona_seeds"),
        "cultural_backgrounds": take("cultural_backgrounds"),
        "idea_patterns": DEFAULT_IDEA_PATTERNS,
    }


def summarize_sentence(value: Any) -> str:
    text = normalize_text(value)
    if not text:
        return ""
    # Keep this dependency-free and regex-simple: Korean persona blurbs usually
    # end the first useful sentence with one of these endings.
    cut_points = []
    for marker in ["입니다.", "합니다.", "습니다.", ".", "!", "?", "。"]:
        idx = text.find(marker)
        if idx >= 0:
            cut_points.append(idx + len(marker))
    if cut_points:
        return remove_korean_name_prefix(normalize_text(text[: min(cut_points)]))
    return remove_korean_name_prefix(text[:160])


def unique(items: Iterable[str]) -> list[str]:
    seen = OrderedDict()
    for item in items:
        item = normalize_text(item)
        if item:
            seen[item] = None
    return list(seen.keys())


def main() -> None:
    parser = argparse.ArgumentParser(description="Build expanded persona constants from Hugging Face rows or a fixture.")
    parser.add_argument("--dataset", default=DATASET)
    parser.add_argument("--config", default="default")
    parser.add_argument("--split", default="train")
    parser.add_argument("--offsets", default="0,1000,10000,50000,100000", help="Comma-separated dataset offsets to sample.")
    parser.add_argument("--length", type=int, default=25, help="Rows per offset from datasets-server.")
    parser.add_argument("--fixture", type=Path, help="Local datasets-server-style JSON fixture for tests/offline builds.")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "references" / "persona_constants.expanded.json")
    parser.add_argument("--max-items-per-list", type=int, default=300)
    args = parser.parse_args()

    if args.fixture:
        rows = load_fixture(args.fixture)
    else:
        offsets = [int(x.strip()) for x in args.offsets.split(",") if x.strip()]
        rows = fetch_rows(args.dataset, args.config, args.split, offsets, args.length)
        if not rows:
            print("warning: rows endpoint returned no rows; falling back to first-rows endpoint", file=sys.stderr)
            rows = fetch_first_rows(args.dataset, args.config, args.split)
    if not rows:
        raise SystemExit("no rows loaded")

    constants = build_constants(rows, args.max_items_per_list)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(constants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output} from {len(rows)} rows")


if __name__ == "__main__":
    main()
