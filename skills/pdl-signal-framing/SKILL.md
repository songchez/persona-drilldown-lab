---
name: pdl-signal-framing
description: "Use when converting a news event, trend, or social issue into a compact persona-analysis signal."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [personas, news, signal-framing]
    related_skills: [pdl-persona-casting, persona-drilldown-lab]
---

# PDL Signal Framing

## Overview

Turn a raw news title, article, trend, or social event into a compact signal that can be thrown into persona analysis.

## When to Use

- Before persona sampling.
- When the event is too broad, technical, or abstract.
- When the user gives a messy bundle of headlines and needs one analyzable signal.

## Input

- News title, URL, headline bundle, or trend description.
- Optional context: country, industry, audience, why the user cares.

## Output

Produce:

1. **One-line signal** — the event in plain language.
2. **Core change** — what is shifting now.
3. **Affected groups** — who may care.
4. **Emotional triggers** — fear, desire, anger, curiosity, status anxiety, money pressure.
5. **Open questions** — what should personas react to.

## Template

```text
오늘의 시그널:

핵심 변화:

영향 받을 사람들:

감정 트리거:

페르소나에게 던질 질문:
```

## Common Pitfalls

1. Do not summarize only facts; extract why humans may care.
2. Do not overclaim beyond the source.
3. Do not make it too broad; a good signal can be reacted to in one sentence.

## Verification Checklist

- [ ] Signal is short enough to pass into persona sampling.
- [ ] Emotional triggers are explicit.
- [ ] Affected groups are concrete.
