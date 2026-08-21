# Contributing to RoboEvaluater

Thanks for your interest in improving RoboEvaluater — an open-source IMM
(Impact Measurement and Management) evaluator built on the Impact Management
Project's five dimensions.

## Ways to contribute

- **Bug reports / UX issues** — especially in the web app, since it's aimed
  at non-technical NPO users. Open an issue with steps to reproduce.
- **Scoring model feedback** — if you have IMM/IMP expertise and think the
  simplified scoring rules in
  [`skill/imm-evaluator/reference/imp-five-dimensions.md`](skill/imm-evaluator/reference/imp-five-dimensions.md)
  should change, open an issue describing the concern before sending a PR —
  scoring changes affect both the Python and JS implementations and should
  be discussed first.
- **Translations** — the web app is currently Japanese-only; PRs adding a
  language toggle are welcome.
- **Code** — see below.

## Development setup

```
git clone https://github.com/jintkim-robo/RoboEvaluater.git
cd RoboEvaluater
pip install pytest
pytest skill/imm-evaluator/tests/
```

For the web app, no build step is required:

```
cd webapp
python3 -m http.server 8000
```

## Keeping the Python and JS scorers in sync

`skill/imm-evaluator/scripts/evaluate.py` and `webapp/scoring.js` implement
the *same* scoring model independently (no shared runtime between Python and
a static web page). If you change the scoring logic in one, you must change
it identically in the other.

`skill/imm-evaluator/tests/test_parity.py` enforces this: it runs both
implementations over every case in `tests/parity_cases.json` and fails on any
difference in the returned scores, classification or `evidence_gated` flag. It
also checks that both reject the same invalid input. Running the suite needs
`node` on your PATH; without it the parity tests skip locally, but in CI they
are a hard failure.

**When you change the scoring model, add a case to `parity_cases.json` that
covers the new behaviour.** A parity suite that doesn't exercise your change
pins nothing about it.

## Private evaluation data

`answers.*.json` is gitignored apart from `answers.example.json`. Real
evaluation inputs describe a named organization's outcomes, evidence gaps and
internal assessments — keep them local and out of pull requests. If you want a
worked example in the repo, write a synthetic one.

## Pull requests

- Keep PRs focused on one change.
- Add or update tests in `skill/imm-evaluator/tests/` for any scoring logic
  change.
- CI (GitHub Actions) runs `pytest` on every PR — make sure it's green.
- Describe what you tested manually for web app changes, since there's no
  automated browser test suite yet.

## Code of conduct

Be respectful and constructive. This project serves NPOs and social-impact
practitioners; keep discussion focused on making the tool more useful and
accurate for them.
