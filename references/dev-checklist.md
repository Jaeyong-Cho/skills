# Dev Checklist

Every point a `@skills/grill-me` interview must cover for a feature or a fix. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical.

- Human Acceptance Criteria (HAC) - (**MUST CHECK** which result make human agree and satisfy when this topic is done: detailed step-by-step e.g. run test script, see the db result, found the expected column...)
- Intent and purpose
- Scope-in / scope-out
- Root cause (for fix)
- Fundamental Solution (**MUST NOT** Ad-Hoc or Workaround)
- Architecture — components and interfaces
- Impact scope
- Observability and Monitoring
- Testability
- Branch to work this topic(git)
- New simple and representative testcase with **built program integration test**, not just unit test — name its fixture (real seed data, mock/stub setup, or existing state it needs) so the test isn't blocked writing it
- What I want — the observable outcome (a value, a state, a visible change), not a restatement of the intent above
- How to evaluate it — deterministic check for the line above: integration test or e2e test, per `deterministic-evaluation.md`
- Release and ship plan
- Dogfood test
