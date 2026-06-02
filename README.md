# persona-drilldown-lab

Hermes skill for turning news events, trends, or social signals into persona-based drilldowns and optional idea concepts.

## Contents

```text
persona-drilldown-lab/
├── SKILL.md
├── references/
│   └── persona_constants.json
└── scripts/
    ├── persona_sampler.py
    └── test_persona_sampler.py
```

## Quick test

```bash
python3 -m pytest scripts/test_persona_sampler.py -q
```

## Sample run

```bash
python3 scripts/persona_sampler.py \
  --news "AI 데이터센터 전력 수요 급증" \
  --count 4 \
  --seed 7 \
  --with-patterns
```

## Install locally in Hermes

Copy this directory into your Hermes skills folder, for example:

```bash
mkdir -p ~/.hermes/skills/creative
cp -R persona-drilldown-lab ~/.hermes/skills/creative/
```

Then start a new Hermes session so the skill loader can pick it up.
