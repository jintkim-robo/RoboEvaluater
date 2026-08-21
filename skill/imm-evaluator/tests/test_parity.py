"""Pin the Python and JS scorers to identical behaviour.

The same scoring model is implemented twice -- once in Python for the CLI and
skill, once in JS for the static web app, which cannot run Python. Nothing but
this test stops the two from drifting apart, and the web app is the copy most
users actually touch. See CONTRIBUTING.md.

Skipped when node is unavailable; CI installs it.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import evaluate  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).parent / "parity_cases.json"
JS_RUNNER = REPO_ROOT / "webapp" / "scoring.parity.js"

# Locally, no node means no parity check. In CI a silent skip would let the two
# scorers drift while the build stayed green, so there it is a hard failure.
requires_node = pytest.mark.skipif(
    shutil.which("node") is None and not os.environ.get("CI"),
    reason="node is not installed (set CI=1 to make this a failure instead)",
)


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def js_output():
    completed = subprocess.run(
        ["node", str(JS_RUNNER), str(FIXTURE)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


@requires_node
def test_every_valid_case_scores_identically(js_output):
    fixture = load_fixture()
    assert len(js_output["valid"]) == len(fixture["cases"])

    mismatches = []
    for case, js_case in zip(fixture["cases"], js_output["valid"]):
        assert case["name"] == js_case["name"]
        python_result = evaluate.score(case["answers"])
        if python_result != js_case["result"]:
            mismatches.append((case["name"], python_result, js_case["result"]))

    assert not mismatches, "Python and JS scorers disagree:\n" + "\n".join(
        f"  {name}\n    python: {py}\n    js:     {js}" for name, py, js in mismatches
    )


@requires_node
def test_both_implementations_reject_the_same_invalid_input(js_output):
    fixture = load_fixture()
    assert len(js_output["invalid"]) == len(fixture["invalid_cases"])

    for case, js_case in zip(fixture["invalid_cases"], js_output["invalid"]):
        assert case["name"] == js_case["name"]
        with pytest.raises(ValueError):
            evaluate.score(case["answers"])
        assert js_case["rejected"], f"JS accepted invalid input: {case['name']}"


def test_python_rejects_every_invalid_case_even_without_node():
    """The validation half of the contract, independent of the JS runner."""
    for case in load_fixture()["invalid_cases"]:
        with pytest.raises(ValueError):
            evaluate.score(case["answers"])


def test_fixture_covers_both_gated_and_ungated_results():
    """A parity fixture that never fires the gate would pin nothing about it."""
    results = [evaluate.score(c["answers"]) for c in load_fixture()["cases"]]
    assert any(r["evidence_gated"] for r in results)
    assert any(not r["evidence_gated"] for r in results)
