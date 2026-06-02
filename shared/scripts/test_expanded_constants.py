import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "shared" / "scripts" / "build_constants_from_hf.py"
SAMPLER = ROOT / "shared" / "scripts" / "persona_sampler.py"
FIXTURE = ROOT / "shared" / "tests" / "fixtures" / "nemotron_rows.json"


def test_builder_creates_v2_constants_from_fixture(tmp_path):
    output = tmp_path / "persona_constants.expanded.json"
    subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            "--fixture",
            str(FIXTURE),
            "--output",
            str(output),
            "--max-items-per-list",
            "20",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["schema_version"] == 2
    assert data["sources"][0]["dataset"] == "nvidia/Nemotron-Personas-Korea"
    assert "전기태" not in json.dumps(data, ensure_ascii=False)  # no raw huge persona blob copied
    assert "광주광역시" in data["geography"]["provinces"]
    assert "하역원" in data["work"]["occupations"]
    assert "전·월세 아파트" in data["demographics"]["housing_type"]
    assert len(data["psychology"]["core_fears"]) >= 5
    assert len(data["attention"]["attention_biases"]) >= 8


def test_sampler_accepts_v2_constants(tmp_path):
    output = tmp_path / "persona_constants.expanded.json"
    subprocess.run(
        [sys.executable, str(BUILDER), "--fixture", str(FIXTURE), "--output", str(output)],
        check=True,
        text=True,
        capture_output=True,
    )

    run = subprocess.run(
        [
            sys.executable,
            str(SAMPLER),
            "--constants",
            str(output),
            "--news",
            "AI 데이터센터 전력 수요 급증",
            "--count",
            "2",
            "--seed",
            "3",
            "--with-patterns",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert run.stdout.count("페르소나 ") == 2
    assert "뉴스/시그널: AI 데이터센터 전력 수요 급증" in run.stdout
    assert "아이디어 컨셉 후보 패턴" in run.stdout
