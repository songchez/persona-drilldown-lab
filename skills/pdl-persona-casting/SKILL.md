---
name: pdl-persona-casting
description: "Use when sampling or constructing normal and outlier personas for persona-drilldown analysis."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [personas, sampling, creative-research]
    related_skills: [pdl-signal-framing, pdl-persona-drilldown]
---

# PDL Persona Casting

## Overview

Create a small cast of personas that can look at the same signal from different human angles. Use the lightweight JSON constant store and sampler script when available.

## When to Use

- After signal framing.
- When the analysis needs diverse human lenses.
- When the user asks for random, weird, or broken persona combinations.

## Shared Sampler

From the repository root:

```bash
python3 shared/scripts/persona_sampler.py   --constants shared/references/persona_constants.json   --news "AI 데이터센터 전력 수요 급증"   --count 4   --seed 7   --with-patterns
```

## Casting Rules

- Mix normal and outlier personas.
- Keep outliers plausible by adding context instead of deleting weirdness.
- Prefer 3-5 personas for one run.
- If the user picks one persona, drill into that one deeply rather than sampling again.

## Output

For each persona:

- Title
- Situation/money state
- Digital literacy
- Core fear
- Hidden desire
- Attention biases
- Reaction style
- Why this signal may matter

## Common Pitfalls

1. Sanitizing weird personas too aggressively.
2. Treating personas as market research facts.
3. Sampling too many personas and losing depth.

## Verification Checklist

- [ ] 3-5 personas unless user asks otherwise.
- [ ] At least one outlier or surprising lens when creative exploration is desired.
- [ ] Each persona has a clear connection to the signal.
