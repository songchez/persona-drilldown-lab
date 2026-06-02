---
name: pdl-decision-gate
description: "Use when deciding what to do after persona drilldown: finish, recast, drill deeper, or generate idea concepts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [personas, decision-gate, workflow]
    related_skills: [pdl-persona-drilldown, pdl-idea-concepting]
---

# PDL Decision Gate

## Overview

This skill handles the branch after persona drilldown. It prevents the workflow from automatically jumping into idea generation without the user's intent.

## When to Use

- After completing persona drilldown.
- When the next path depends on user choice.
- When the user may want idea concepts, deeper analysis, or just a report.

## Required Question

Ask:

> 이 종합 데이터를 바탕으로 아이디어 컨셉까지 생성할까요?

## Options

Offer concise choices:

1. 여기서 종료
2. 특정 페르소나 더 파기
3. 페르소나 다시 뽑기
4. 아이디어 컨셉 생성

If the user already clearly chooses a path, proceed without asking again.

## Common Pitfalls

1. Asking too early before enough material exists.
2. Generating marketing copy instead of concepting.
3. Treating the gate as a yes/no only; recast and deeper drilldown are valid paths.

## Verification Checklist

- [ ] User has enough synthesis to decide.
- [ ] Branch options are clear.
- [ ] Idea concepting only runs after explicit or obvious user intent.
