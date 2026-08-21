---
name: imm-evaluator
description: Runs an IMM (Impact Measurement and Management) evaluation of a project or organization using the Impact Management Project's five dimensions (What, Who, How Much, Contribution, Risk). Use when the user asks to evaluate social/impact-investing impact, run an "IMMをやる" / "インパクト評価" request, score a project against IMP's five dimensions, or produce an impact report for a nonprofit or impact investment.
---

# IMM Evaluator

Interviews the user about a project across the IMP five dimensions, scores the
answers, and generates a Markdown impact report. See
`reference/imp-five-dimensions.md` for the full framework and scoring model —
read it before running an evaluation.

## When to use

- The user wants an impact evaluation, IMM assessment, or IMP five-dimension
  scoring for a specific project, program, or investment.
- The user wants to compare a positive-impact claim to its risk of not
  materializing (contribution risk, drop-off risk, etc.).

## How to run an evaluation

1. Read `reference/imp-five-dimensions.md` for the questions and scoring
   rules behind each dimension.
2. Interview the user one dimension at a time (What → Who → How much →
   Contribution → Risk). Don't dump all the questions at once — this is
   meant to feel like a structured conversation, not a form. Confirm numeric
   estimates (scale, depth, duration) rather than accepting vague answers.
3. Assemble the answers into a JSON object matching the shape in
   `reference/answers.example.json`.
4. Run the scorer:
   ```
   python3 scripts/evaluate.py <answers.json> --out report.md
   ```
5. Walk the user through the resulting classification and dimension scores.
   Flag any dimension scored low, and suggest one concrete next step per weak
   dimension (e.g. high `drop_off_risk` → discuss a sustainability plan).

## Scoring evidence_risk honestly

`evidence_risk` decides whether a C classification is available at all (see the
evidence gate in `reference/imp-five-dimensions.md`), and it is the score users
most reliably get wrong in their own favour. Two traps to name out loud when
interviewing:

- **Reputation is not outcome evidence.** Awards, grants, investment,
  government or UN partnerships tell you funders trust the organization. They
  do not tell you the outcome reached stakeholders. Score this dimension on
  tracked outcome data, comparison groups, and independent verification.
- **Outputs are not outcomes.** "We trained 50 people" is an output. "40 of
  them were working six months later, earning on average X% more" is an
  outcome. Push for the second; if only the first exists, `evidence_risk` is
  4 or higher and you should say so plainly.

When the gate fires, don't soften it. Report the B, and tell the user exactly
what measurement would lift it to C — that is the most useful output this
skill produces.

## Notes

- If the user is non-technical and would rather use a form than be
  interviewed, point them to the sibling web app in `/webapp` in this
  repository (a no-install, client-side questionnaire that renders the same
  report in the browser).
- This tool is a simplified, transparent operationalization of the IMP
  framework, not an official IMP certification — say so if the user is
  planning to use the output in funder-facing reporting.
