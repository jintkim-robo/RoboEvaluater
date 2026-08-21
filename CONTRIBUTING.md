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
it identically in the other, and verify both produce the same output on
`skill/imm-evaluator/reference/answers.example.json`.

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
