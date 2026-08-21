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
  const whatScore = answers.outcome_importance;
  const whoScore = answers.stakeholder_underserved;

  const howMuchScore =
    (bandScale(answers.scale) + answers.depth + bandDuration(answers.duration_years)) / 3;

  const contributionScore = COUNTERFACTUAL_SCORES[answers.counterfactual];
  if (contributionScore === undefined) {
    throw new Error(`counterfactual must be one of ${Object.keys(COUNTERFACTUAL_SCORES)}`);
  }

  for (const key of RISK_KEYS) {
    if (!(key in answers)) throw new Error(`missing risk score: ${key}`);
  }
  const riskScore = RISK_KEYS.reduce((sum, k) => sum + answers[k], 0) / RISK_KEYS.length;

  let impactScore =
    (whatScore + whoScore + howMuchScore + contributionScore) / 4 -
    Math.max(0, riskScore - 3) * 0.5;
  impactScore = Math.max(1, Math.min(5, impactScore));

  const valence = answers.outcome_valence || "positive";
  let classification;
  if (valence === "negative") {
    classification = "A: Act to Avoid Harm";
  } else if (impactScore >= 4 && contributionScore >= 4) {
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
  };
}
