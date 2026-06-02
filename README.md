# persona-drilldown-lab

A Hermes skillset for turning news events, trends, or social signals into persona-based drilldowns and optional idea concepts.

This repo is intentionally organized as a **work-unit graph**, not one giant skill and not tiny arbitrary fragments.

## Skillset graph

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

## Skills

```text
skills/
├── persona-drilldown-lab/   # orchestrator / graph router
├── pdl-signal-framing/      # raw news → analyzable signal
├── pdl-persona-casting/     # JSON constants + random persona sampling
├── pdl-persona-drilldown/   # persona psychology / behavior / opportunity signal
├── pdl-decision-gate/       # finish / recast / deeper drill / concepting branch
└── pdl-idea-concepting/     # concept design, not marketing copy
```

## Shared lightweight data and script

```text
shared/
├── references/
│   └── persona_constants.json
└── scripts/
    ├── persona_sampler.py
    └── test_persona_sampler.py
```

## Quick test

```bash
python3 -m pytest shared/scripts/test_persona_sampler.py -q
```

## Sample run

```bash
python3 shared/scripts/persona_sampler.py   --constants shared/references/persona_constants.json   --news "AI 데이터센터 전력 수요 급증"   --count 4   --seed 7   --with-patterns
```

## Local Hermes install

Copy the skills into your Hermes skills directory:

```bash
mkdir -p ~/.hermes/skills/creative
cp -R skills/* ~/.hermes/skills/creative/
```

Then start a new Hermes session so the skill loader can pick them up.

If you want the sampler available from inside an installed skill, also copy `shared/` alongside your repo or manually copy the shared files into the relevant skill folder.
