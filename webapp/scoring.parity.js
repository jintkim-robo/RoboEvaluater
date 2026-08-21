// Emits the JS scorer's verdict for every case in the shared parity fixture,
// as JSON on stdout. test_parity.py runs this and compares against the Python
// scorer, which is what keeps the two implementations from drifting apart.
//
// Usage: node webapp/scoring.parity.js <path-to-parity_cases.json>

const fs = require("fs");
const path = require("path");

eval(fs.readFileSync(path.join(__dirname, "scoring.js"), "utf8"));

const fixture = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));

const valid = fixture.cases.map((c) => ({
  name: c.name,
  result: scoreAnswers(c.answers),
}));

const invalid = fixture.invalid_cases.map((c) => {
  try {
    scoreAnswers(c.answers);
    return { name: c.name, rejected: false };
  } catch (e) {
    return { name: c.name, rejected: true };
  }
});

process.stdout.write(JSON.stringify({ valid, invalid }, null, 2));
