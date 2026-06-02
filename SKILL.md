---
name: persona-drilldown-lab
description: Use when turning a news event, trend, or social signal into persona-based reactions and optional idea concepts using a lightweight persona constant store.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [personas, ideation, news, trends, creative-research]
    related_skills: []
---

# Persona Drilldown Lab

## Overview

Persona Drilldown Lab converts a news event or trend into human-centered insight. It frames the event, samples several normal/outlier personas from a lightweight JSON constant store, drills into how each persona may react, and then asks the user whether to continue into idea concepting.

This skill is deliberately lightweight: constants live in `references/persona_constants.json`, and `scripts/persona_sampler.py` only prints sampled persona cards as text. The skill does not store large live databases inside `SKILL.md`.

## When to Use

Use when the user wants to:

- Monitor recent news/trends and understand who would care and why
- Generate odd but useful persona lenses for an event
- Explore psychological reactions, fears, desires, and possible behaviors
- Optionally turn synthesized reactions into product/content/service idea concepts

Do not use for pure marketing copywriting. The final idea step is concepting, not viral packaging.

## Workflow Graph

```text
[news / event / trend]
        ↓
signal framing
        ↓
persona sampling from JSON constants
        ↓
persona drilldown
        ↓
summary of cross-persona signals
        ↓
ask user: "아이디어 컨셉까지 생성할까요?"
        ├── no  → finish with persona insight report
        └── yes → idea concepting
```

## Work Units

### 1. Signal Framing

Convert the event into a compact signal:

- One-line event
- Core change
- Who may be affected
- Emotional triggers
- Open questions

### 2. Persona Sampling

Use `scripts/persona_sampler.py` with `references/persona_constants.json` to sample persona cards. Keep this deterministic when needed by passing `--seed`.

Example:

```bash
python3 ~/.hermes/skills/creative/persona-drilldown-lab/scripts/persona_sampler.py \
  --news "AI 데이터센터 전력 수요 급증" \
  --count 4 \
  --seed 7
```

### 3. Persona Drilldown

For each sampled persona, analyze:

- Surface reaction
- Hidden fear
- Hidden desire
- Why this event matters to them
- Likely behavior
- Search keywords
- Opportunity signal

### 4. Decision Gate

After persona drilldown, ask the user:

> 이 종합 데이터를 바탕으로 아이디어 컨셉까지 생성할까요?

Options:

- 여기서 종료
- 특정 페르소나 더 파기
- 페르소나 다시 뽑기
- 아이디어 컨셉 생성

### 5. Idea Concepting

Only if the user wants it, turn the synthesized data into idea concepts. Focus on concept, not marketing.

For each idea concept, output:

- Concept title
- Source signal
- Target persona
- Problem
- Why now
- Core user experience
- Minimum feature set
- What to validate next
- Risks or weak assumptions

## Data Design

The current version uses a constant JSON file, not a live database:

```text
references/persona_constants.json
```

The Python script reads this file and combines persona dimensions randomly. This is enough for quick experimentation and avoids overbuilding.

If the workflow becomes recurring, add a separate data store under:

```text
~/.hermes/data/persona-drilldown-lab/
```

Do not dump growing data into `SKILL.md`.

## Output Style

Prefer Korean. Be direct and structured:

1. 오늘의 시그널
2. 뽑힌 페르소나
3. 페르소나별 반응
4. 공통 패턴
5. 아이디어 컨셉 생성 여부 질문

## Common Pitfalls

1. **Over-splitting skills.** Keep this as a work-unit graph, not one skill per tiny step.
2. **Turning concepting into marketing.** Do not generate slogans unless explicitly asked.
3. **Overbuilding storage.** Start with JSON constants and a tiny sampler script.
4. **Ignoring weird personas.** Strange combinations are useful; repair them into plausible humans instead of sanitizing them away.

## Verification Checklist

- [ ] Event is framed as a clear signal
- [ ] Persona cards were sampled from JSON constants or explicitly created
- [ ] Each persona drilldown includes fear, desire, behavior, and opportunity signal
- [ ] User is asked before idea concepting
- [ ] Idea concepts, if generated, focus on problem/experience/MVP/validation rather than marketing copy
