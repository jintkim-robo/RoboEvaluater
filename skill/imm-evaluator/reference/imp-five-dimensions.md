# IMP Five Dimensions of Impact — Reference

RoboEvaluater's questionnaire and scoring are a simplified, open operationalization
of the Impact Management Project (IMP)'s five dimensions of impact. This is not an
official IMP certification tool — it is our own interpretation, built to give NPOs
and social ventures a fast, structured first pass at IMM (Impact Measurement and
Management).

## The five dimensions

1. **What** — What outcome occurs, how important it is to stakeholders, and
   whether it is positive or negative.
2. **Who** — Which stakeholders experience the outcome, and how underserved
   or vulnerable they are relative to the outcome.
3. **How much** — The scale (how many stakeholders), depth (degree of change
   per stakeholder), and duration (how long the effect lasts).
4. **Contribution** — Whether the outcome is better or worse than what would
   have happened anyway (the counterfactual).
5. **Risk** — The risk that impact does not occur as expected. IMP names six
   risk types; we score all six:
   - Evidence risk — the evidence behind the expected outcome is weak.
   - External risk — external factors could reduce or reverse the outcome.
   - Stakeholder participation risk — the outcome wasn't designed with
     stakeholder input, so it may miss what stakeholders actually need.
   - Drop-off risk — the effect may fade after the intervention ends.
   - Efficiency risk — the outcome could have been achieved more efficiently.
   - Unexpected impact risk — there is a chance of significant unintended
     positive or negative side effects.

## Scoring model (RoboEvaluater's operationalization)

Each dimension is scored 1–5 from the questionnaire answers:

| Dimension    | Input                                              | Score rule |
|---|---|---|
| What         | `outcome_importance` (1–5), `outcome_valence`      | direct 1–5; valence flags harm |
| Who          | `stakeholder_underserved` (1–5)                    | direct 1–5 |
| How much     | `scale`, `depth` (1–5), `duration_years`           | mean of scale/depth/duration bands |
| Contribution | `counterfactual` (none/some/much/most)             | none=5, some=4, much=2, most=1 |
| Risk         | 6 risk sub-scores (1–5 each, 5 = highest risk)     | mean of the six |

`scale` bands: <100 stakeholders → 1, 100–1000 → 3, >1000 → 5.
`duration_years` bands: <1 → 1, 1–3 → 3, >3 → 5.

## Classification

```
impact_score = mean(what, who, how_much, contribution) - max(0, risk_score - 3) * 0.5
```

- If `outcome_valence == "negative"` → **A: Act to Avoid Harm** (the priority
  is mitigating harm, not claiming impact).
- Else if `impact_score >= 4` and `contribution_score >= 4` **and
  `evidence_risk < 4`** → **C: Contribute to Solutions**.
- Else if `impact_score >= 2.5` → **B: Benefit Stakeholders**.
- Else → **Insufficient impact evidence** — the inputs don't yet support an
  impact claim; strengthen evidence or reconsider the theory of change.

### The evidence gate

The `evidence_risk < 4` condition on C is deliberate, and it is the one rule
here that can override otherwise-excellent scores.

Claiming *Contribute to Solutions* asserts that the outcome is really
happening. Without evidence for that, the claim is a statement of intent
dressed as a result. The mean of the four positive dimensions cannot catch
this on its own: an organization serving a highly underserved group (Who = 5)
with a self-evidently important outcome (What = 5) starts halfway to a C
before anyone has measured anything. Left ungated, the model hands its top
classification to the exact failure mode IMM exists to prevent — sincere
mission, unmeasured results.

So when `evidence_risk` is 4 or 5, the result is capped at **B: Benefit
Stakeholders** and the report says so explicitly, naming what would lift the
cap. The scoring result carries an `evidence_gated` flag for this.

Two clarifications that come up constantly when scoring `evidence_risk`:

- **Awards, grants, investment and partnerships are not outcome evidence.**
  They attest to an organization's standing and to funders' confidence. They
  say nothing about whether the intended outcome occurred for stakeholders.
  Score `evidence_risk` on outcome data — tracked results, comparison groups,
  independent verification — not on reputation.
- **Outputs are not outcomes.** People trained is an output. People who got
  and kept work, and what happened to their income, is the outcome. Score the
  latter, and use the outcome count for `scale` too.

The gate only ever caps C down to B. It never promotes a weak project, and it
never overrides an `A: Act to Avoid Harm` classification.

This mirrors IMP's A/B/C classes at a conceptual level but is a deliberately
simplified, transparent scoring rule — not the official IMP methodology.
Organizations doing formal reporting (e.g. to funders using IRIS+ or the IMP
itself) should treat this as a starting diagnostic, not a substitute.
