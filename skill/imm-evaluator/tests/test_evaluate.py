import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import evaluate  # noqa: E402


def base_answers(**overrides):
    answers = {
        "project_name": "Test project",
        "outcome_importance": 4,
        "outcome_valence": "positive",
        "stakeholder_underserved": 4,
        "scale": 500,
        "depth": 4,
        "duration_years": 2,
        "counterfactual": "some",
        "evidence_risk": 2,
        "external_risk": 2,
        "stakeholder_participation_risk": 2,
        "drop_off_risk": 2,
        "efficiency_risk": 2,
        "unexpected_impact_risk": 2,
    }
    answers.update(overrides)
    return answers


def test_example_file_scores_without_error():
    example_path = (
        Path(__file__).resolve().parents[1] / "reference" / "answers.example.json"
    )
    answers = json.loads(example_path.read_text(encoding="utf-8"))
    result = evaluate.score(answers)
    assert 1.0 <= result["impact_score"] <= 5.0
    assert result["classification"] in {
        "A: Act to Avoid Harm",
        "B: Benefit Stakeholders",
        "C: Contribute to Solutions",
        "Insufficient impact evidence",
    }


def test_negative_valence_is_always_act_to_avoid_harm():
    answers = base_answers(outcome_valence="negative", counterfactual="none")
    result = evaluate.score(answers)
    assert result["classification"] == "A: Act to Avoid Harm"


def test_high_scores_and_no_counterfactual_contribute_to_solutions():
    answers = base_answers(
        outcome_importance=5,
        stakeholder_underserved=5,
        scale=2000,
        depth=5,
        duration_years=5,
        counterfactual="none",
        evidence_risk=1,
        external_risk=1,
        stakeholder_participation_risk=1,
        drop_off_risk=1,
        efficiency_risk=1,
        unexpected_impact_risk=1,
    )
    result = evaluate.score(answers)
    assert result["classification"] == "C: Contribute to Solutions"


def test_low_scores_are_insufficient_evidence():
    answers = base_answers(
        outcome_importance=1,
        stakeholder_underserved=1,
        scale=10,
        depth=1,
        duration_years=0.5,
        counterfactual="most",
        evidence_risk=5,
        external_risk=5,
        stakeholder_participation_risk=5,
        drop_off_risk=5,
        efficiency_risk=5,
        unexpected_impact_risk=5,
    )
    result = evaluate.score(answers)
    assert result["classification"] == "Insufficient impact evidence"


def test_missing_risk_key_raises():
    answers = base_answers()
    del answers["evidence_risk"]
    try:
        evaluate.score(answers)
        assert False, "expected ValueError"
    except ValueError as e:
        assert "evidence_risk" in str(e)


def test_invalid_counterfactual_raises():
    answers = base_answers(counterfactual="unknown")
    try:
        evaluate.score(answers)
        assert False, "expected ValueError"
    except ValueError:
        pass


def strong_c_answers(**overrides):
    """Answers that would classify as C were it not for the evidence gate."""
    answers = base_answers(
        outcome_importance=5,
        stakeholder_underserved=5,
        scale=2000,
        depth=5,
        duration_years=5,
        counterfactual="none",
        evidence_risk=1,
        external_risk=1,
        stakeholder_participation_risk=1,
        drop_off_risk=1,
        efficiency_risk=1,
        unexpected_impact_risk=1,
    )
    answers.update(overrides)
    return answers


def test_weak_evidence_caps_a_would_be_c_at_b():
    """The core evidence gate: no C classification without outcome evidence."""
    result = evaluate.score(strong_c_answers(evidence_risk=4))
    assert result["classification"] == "B: Benefit Stakeholders"
    assert result["evidence_gated"] is True


def test_evidence_gate_also_applies_at_maximum_evidence_risk():
    result = evaluate.score(strong_c_answers(evidence_risk=5))
    assert result["classification"] == "B: Benefit Stakeholders"
    assert result["evidence_gated"] is True


def test_evidence_risk_just_below_threshold_still_reaches_c():
    result = evaluate.score(strong_c_answers(evidence_risk=3))
    assert result["classification"] == "C: Contribute to Solutions"
    assert result["evidence_gated"] is False


def test_evidence_gate_does_not_override_harm_classification():
    """Avoiding harm outranks the evidence gate."""
    result = evaluate.score(
        strong_c_answers(evidence_risk=5, outcome_valence="negative")
    )
    assert result["classification"] == "A: Act to Avoid Harm"
    assert result["evidence_gated"] is False


def test_gate_fires_exactly_at_the_threshold_not_below():
    """Pin the boundary, including non-integer inputs."""
    assert evaluate.score(strong_c_answers(evidence_risk=3.999))["evidence_gated"] is False
    assert evaluate.score(strong_c_answers(evidence_risk=4.0))["evidence_gated"] is True


def test_a_gated_result_is_always_classified_b():
    """Invariant: the gate's only effect is capping C at B."""
    for evidence_risk in (4, 4.5, 5):
        result = evaluate.score(strong_c_answers(evidence_risk=evidence_risk))
        assert result["evidence_gated"] is True
        assert result["classification"] == "B: Benefit Stakeholders"


def test_evidence_gate_does_not_promote_a_weak_project():
    """Gating only ever caps C down to B; it never lifts a failing project up."""
    result = evaluate.score(
        base_answers(
            outcome_importance=1,
            stakeholder_underserved=1,
            scale=10,
            depth=1,
            duration_years=0.5,
            counterfactual="most",
            evidence_risk=5,
            external_risk=5,
            stakeholder_participation_risk=5,
            drop_off_risk=5,
            efficiency_risk=5,
            unexpected_impact_risk=5,
        )
    )
    assert result["classification"] == "Insufficient impact evidence"
    assert result["evidence_gated"] is False


def test_ungated_results_report_evidence_gated_false():
    result = evaluate.score(base_answers())
    assert result["evidence_gated"] is False


def test_report_explains_the_evidence_gate_when_it_fires():
    answers = strong_c_answers(evidence_risk=5)
    report = evaluate.render_report(answers, evaluate.score(answers))

    assert "Held at B by the evidence gate" in report
    # States the score that tripped it and the threshold, so the reader can act.
    assert "5/5" in report
    assert f"gate fires at {evaluate.EVIDENCE_GATE_RISK}" in report
    # Names the remedy, not just the verdict.
    assert "independent verification" in report


def test_report_omits_the_gate_notice_when_the_gate_does_not_fire():
    """Without this, deleting the guard would banner every report as gated."""
    answers = strong_c_answers(evidence_risk=1)
    report = evaluate.render_report(answers, evaluate.score(answers))

    assert "C: Contribute to Solutions" in report
    assert "evidence gate" not in report
    assert "Held at B" not in report


def test_scale_and_duration_bands():
    assert evaluate._band_scale(50) == 1
    assert evaluate._band_scale(500) == 3
    assert evaluate._band_scale(5000) == 5
    assert evaluate._band_duration(0.5) == 1
    assert evaluate._band_duration(2) == 3
    assert evaluate._band_duration(4) == 5
