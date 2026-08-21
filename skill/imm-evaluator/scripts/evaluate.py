#!/usr/bin/env python3
"""Score a project's answers against the IMP five-dimension questionnaire
and render a Markdown impact report.

Usage:
    python evaluate.py answers.json [--out report.md]

See reference/imp-five-dimensions.md for the scoring model, and
reference/answers.example.json for the expected input shape.
"""
import argparse
import json
import sys
from pathlib import Path

RISK_KEYS = [
    "evidence_risk",
    "external_risk",
    "stakeholder_participation_risk",
    "drop_off_risk",
    "efficiency_risk",
    "unexpected_impact_risk",
]

COUNTERFACTUAL_SCORES = {"none": 5, "some": 4, "much": 2, "most": 1}

# An evidence_risk at or above this level blocks a "C: Contribute to Solutions"
# classification. See the evidence gate note in score().
EVIDENCE_GATE_RISK = 4


SCORE_KEYS = ["outcome_importance", "stakeholder_underserved", "depth"] + RISK_KEYS


def _require_number(answers, key, minimum, maximum=None):
    value = answers[key]
    # bool is an int subclass, and True would silently score as 1.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a number, got {value!r}")
    if value < minimum or (maximum is not None and value > maximum):
        bound = f"{minimum}-{maximum}" if maximum is not None else f">= {minimum}"
        raise ValueError(f"{key} must be {bound}, got {value!r}")


def _validate(answers):
    """Reject inputs the scoring model cannot meaningfully score.

    Without this, an out-of-range or wrongly-typed risk score silently skews
    the result -- and in the worst case slips past the evidence gate -- rather
    than failing where the caller can see it.
    """
    missing = [k for k in SCORE_KEYS + ["scale", "duration_years"] if k not in answers]
    if missing:
        raise ValueError(f"missing required answers: {missing}")

    for key in SCORE_KEYS:
        _require_number(answers, key, 1, 5)
    _require_number(answers, "scale", 0)
    _require_number(answers, "duration_years", 0)

    valence = answers.get("outcome_valence", "positive")
    if valence not in ("positive", "negative"):
        raise ValueError(
            f"outcome_valence must be 'positive' or 'negative', got {valence!r}"
        )

    counterfactual = answers["counterfactual"]
    if counterfactual not in COUNTERFACTUAL_SCORES:
        raise ValueError(
            f"counterfactual must be one of {list(COUNTERFACTUAL_SCORES)}, "
            f"got {counterfactual!r}"
        )


def _band_scale(scale):
    if scale < 100:
        return 1
    if scale <= 1000:
        return 3
    return 5


def _band_duration(years):
    if years < 1:
        return 1
    if years <= 3:
        return 3
    return 5


def score(answers):
    _validate(answers)

    what_score = answers["outcome_importance"]
    who_score = answers["stakeholder_underserved"]

    how_much_score = (
        _band_scale(answers["scale"])
        + answers["depth"]
        + _band_duration(answers["duration_years"])
    ) / 3

    contribution_score = COUNTERFACTUAL_SCORES[answers["counterfactual"]]
    risk_score = sum(answers[k] for k in RISK_KEYS) / len(RISK_KEYS)

    impact_score = (
        what_score + who_score + how_much_score + contribution_score
    ) / 4 - max(0, risk_score - 3) * 0.5
    impact_score = max(1.0, min(5.0, impact_score))

    # Evidence gate: a "Contribute to Solutions" claim asserts the outcome is
    # really happening, so weak outcome evidence caps the result at B no matter
    # how strong the other dimensions look. Awards, funding and partnerships
    # attest to an organization's standing, not to its outcomes -- score
    # evidence_risk on the latter.
    valence = answers.get("outcome_valence", "positive")
    reaches_c = (
        valence != "negative" and impact_score >= 4 and contribution_score >= 4
    )
    evidence_gated = reaches_c and answers["evidence_risk"] >= EVIDENCE_GATE_RISK

    if valence == "negative":
        classification = "A: Act to Avoid Harm"
    elif reaches_c and not evidence_gated:
        classification = "C: Contribute to Solutions"
    elif impact_score >= 2.5:
        classification = "B: Benefit Stakeholders"
    else:
        classification = "Insufficient impact evidence"

    return {
        "what_score": round(what_score, 2),
        "who_score": round(who_score, 2),
        "how_much_score": round(how_much_score, 2),
        "contribution_score": round(contribution_score, 2),
        "risk_score": round(risk_score, 2),
        "impact_score": round(impact_score, 2),
        "classification": classification,
        "evidence_gated": evidence_gated,
    }


def render_report(answers, result):
    lines = [
        f"# IMM Impact Report — {answers.get('project_name', 'Untitled project')}",
        "",
        f"**Classification:** {result['classification']}",
        f"**Overall impact score:** {result['impact_score']} / 5",
        "",
    ]
    if result["evidence_gated"]:
        lines += [
            "> **Held at B by the evidence gate.** The dimension scores otherwise "
            "reach *C: Contribute to Solutions*, but the evidence that this "
            "outcome actually occurs is too weak to support that claim "
            "(`evidence_risk` "
            f"{answers['evidence_risk']}/5, gate fires at {EVIDENCE_GATE_RISK}). "
            "Strengthen outcome measurement — tracked outcome data, a comparison "
            "group, or independent verification — before claiming C. Awards, "
            "funding and partnerships attest to standing, not to outcomes.",
            "",
        ]
    lines += [
        "## Dimension scores",
        "",
        "| Dimension | Score (1–5) |",
        "|---|---|",
        f"| What | {result['what_score']} |",
        f"| Who | {result['who_score']} |",
        f"| How much | {result['how_much_score']} |",
        f"| Contribution | {result['contribution_score']} |",
        f"| Risk (higher = riskier) | {result['risk_score']} |",
        "",
        "## Notes",
        "",
        answers.get("notes", "_No additional notes provided._"),
        "",
        "---",
        "_Generated by RoboEvaluater — a simplified, open operationalization of the "
        "IMP five dimensions. See reference/imp-five-dimensions.md for methodology._",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("answers", type=Path, help="Path to a JSON answers file")
    parser.add_argument("--out", type=Path, help="Write report to this path instead of stdout")
    args = parser.parse_args()

    answers = json.loads(args.answers.read_text(encoding="utf-8"))
    result = score(answers)
    report = render_report(answers, result)

    if args.out:
        args.out.write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    sys.exit(main())
