---
name: persona-drilldown-lab
description: "Use when orchestrating the full persona-drilldown workflow from news signal to persona drilldown and optional idea concepting."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [personas, news, ideation, orchestrator]
    related_skills: [pdl-signal-framing, pdl-persona-casting, pdl-persona-drilldown, pdl-decision-gate, pdl-idea-concepting]
---

# Persona Drilldown Lab

## Overview

This is the orchestrator skill for the Persona Drilldown Lab skillset. It treats the workflow as a graph of work units, not as a pile of tiny steps. Use it to route a news event, trend, or social signal through the right subskills.

## Workflow Graph

```text
[news / event / trend]
        ↓
pdl-signal-framing
        ↓
pdl-persona-casting
        ↓
pdl-persona-drilldown
        ↓
pdl-decision-gate
        ├── finish report
        ├── recast personas → pdl-persona-casting
        ├── drill deeper → pdl-persona-drilldown
        └── generate idea concepts → pdl-idea-concepting
```

## When to Use

- The user wants to monitor a news issue and understand which humans would care.
- The user wants weird/random personas repaired into plausible human lenses.
- The user wants to optionally turn synthesized reactions into idea concepts.

Do not use this for pure marketing copy. This lab stops at concept design unless the user asks for marketing explicitly.

## Operating Rules

1. Frame the event before sampling personas.
2. Use random personas as creative lenses, not demographic truth.
3. Preserve weird combinations and make them plausible instead of sanitizing them away.
4. Ask before idea concepting.
5. Concepting focuses on problem, context, user experience, MVP, assumptions, and validation.

## Shared Files

This repository keeps shared constants and scripts outside individual skill folders:

```text
shared/references/persona_constants.json
shared/scripts/persona_sampler.py
```

When installed into Hermes, copy or symlink these into the relevant skill folder if direct `skill_view(..., file_path=...)` access is desired.

## Verification Checklist

- [ ] Event was framed as a signal.
- [ ] Personas were sampled or intentionally specified.
- [ ] Drilldown includes fear, desire, behavior, and opportunity signal.
- [ ] User was asked before idea concepting.
- [ ] Any idea concepts are concept-first, not marketing-first.
