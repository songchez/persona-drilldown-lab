import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("persona_sampler.py")
CONSTANTS = Path(__file__).parents[1] / "references" / "persona_constants.json"


def run_sampler(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--constants", str(CONSTANTS), *args],
        text=True,
        capture_output=True,
        check=True,
    ).stdout


def test_outputs_requested_number_of_personas():
    output = run_sampler("--news", "AI 데이터센터 전력 수요 급증", "--count", "3", "--seed", "1")
    assert output.count("페르소나 ") == 3
    assert "뉴스/시그널: AI 데이터센터 전력 수요 급증" in output


def test_seed_makes_output_deterministic():
    first = run_sampler("--news", "반도체 투자 확대", "--count", "2", "--seed", "42")
    second = run_sampler("--news", "반도체 투자 확대", "--count", "2", "--seed", "42")
    assert first == second


def test_constants_file_is_valid_json():
    data = json.loads(CONSTANTS.read_text(encoding="utf-8"))
    assert "jobs" in data
    assert "idea_patterns" in data
