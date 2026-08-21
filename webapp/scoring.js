// Mirrors skill/imm-evaluator/scripts/evaluate.py — keep the two in sync.
// See skill/imm-evaluator/reference/imp-five-dimensions.md for the model.

const RISK_KEYS = [
  "evidence_risk",
  "external_risk",
  "stakeholder_participation_risk",
  "drop_off_risk",
  "efficiency_risk",
  "unexpected_impact_risk",
];

const COUNTERFACTUAL_SCORES = { none: 5, some: 4, much: 2, most: 1 };

// An evidence_risk at or above this level blocks a "C: Contribute to Solutions"
// classification. See the evidence gate note in scoreAnswers().
const EVIDENCE_GATE_RISK = 4;

const SCORE_KEYS = [
  "outcome_importance",
  "stakeholder_underserved",
  "depth",
  ...RISK_KEYS,
];

function requireNumber(answers, key, minimum, maximum) {
  const value = answers[key];
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new Error(`${key} must be a number, got ${JSON.stringify(value)}`);
  }
  if (value < minimum || (maximum !== undefined && value > maximum)) {
    const bound = maximum !== undefined ? `${minimum}-${maximum}` : `>= ${minimum}`;
    throw new Error(`${key} must be ${bound}, got ${value}`);
  }
}

// Reject inputs the scoring model cannot meaningfully score. Without this, an
// out-of-range or wrongly-typed risk score silently skews the result -- and in
// the worst case slips past the evidence gate -- rather than failing where the
// caller can see it. Mirrors _validate() in the Python scorer.
function validate(answers) {
  const missing = [...SCORE_KEYS, "scale", "duration_years"].filter(
    (k) => !(k in answers),
  );
  if (missing.length) {
    throw new Error(`missing required answers: ${missing.join(", ")}`);
  }

  SCORE_KEYS.forEach((key) => requireNumber(answers, key, 1, 5));
  requireNumber(answers, "scale", 0);
  requireNumber(answers, "duration_years", 0);

  const valence = answers.outcome_valence || "positive";
  if (valence !== "positive" && valence !== "negative") {
    throw new Error(
      `outcome_valence must be 'positive' or 'negative', got ${JSON.stringify(valence)}`,
    );
  }

  if (!(answers.counterfactual in COUNTERFACTUAL_SCORES)) {
    throw new Error(
      `counterfactual must be one of ${Object.keys(COUNTERFACTUAL_SCORES)}, ` +
        `got ${JSON.stringify(answers.counterfactual)}`,
    );
  }
}

function bandScale(scale) {
  if (scale < 100) return 1;
  if (scale <= 1000) return 3;
  return 5;
}

function bandDuration(years) {
  if (years < 1) return 1;
  if (years <= 3) return 3;
  return 5;
}

function scoreAnswers(answers) {
  validate(answers);

  const whatScore = answers.outcome_importance;
  const whoScore = answers.stakeholder_underserved;

  const howMuchScore =
    (bandScale(answers.scale) + answers.depth + bandDuration(answers.duration_years)) / 3;

  const contributionScore = COUNTERFACTUAL_SCORES[answers.counterfactual];
  const riskScore =
    RISK_KEYS.reduce((sum, k) => sum + answers[k], 0) / RISK_KEYS.length;

  let impactScore =
    (whatScore + whoScore + howMuchScore + contributionScore) / 4 -
    Math.max(0, riskScore - 3) * 0.5;
  impactScore = Math.max(1, Math.min(5, impactScore));

  // Evidence gate: a "Contribute to Solutions" claim asserts the outcome is
  // really happening, so weak outcome evidence caps the result at B no matter
  // how strong the other dimensions look. Awards, funding and partnerships
  // attest to an organization's standing, not to its outcomes -- score
  // evidence_risk on the latter.
  const valence = answers.outcome_valence || "positive";
  const reachesC =
    valence !== "negative" && impactScore >= 4 && contributionScore >= 4;
  const evidenceGated = reachesC && answers.evidence_risk >= EVIDENCE_GATE_RISK;

  let classification;
  if (valence === "negative") {
    classification = "A: Act to Avoid Harm";
  } else if (reachesC && !evidenceGated) {
    classification = "C: Contribute to Solutions";
  } else if (impactScore >= 2.5) {
    classification = "B: Benefit Stakeholders";
  } else {
    classification = "Insufficient impact evidence";
  }

  const round2 = (n) => Math.round(n * 100) / 100;

  return {
    what_score: round2(whatScore),
    who_score: round2(whoScore),
    how_much_score: round2(howMuchScore),
    contribution_score: round2(contributionScore),
    risk_score: round2(riskScore),
    impact_score: round2(impactScore),
    classification,
    evidence_gated: evidenceGated,
  };
}
