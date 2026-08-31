# Story Checklist

Every point a `@skills/grill-me` interview must cover to build a complete agile Story. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms.

- Persona (who hits this — a real user role, not "the system")
- User value (the "so that" — what they get, what breaks or stays missing without it)
- Trigger (the event or context this scenario starts from)
- Happy path scenario (Given/When/Then — the one flow that must work)
- Alternate scenarios (other valid Given/When/Then paths to the same value)
- Edge cases (boundary: empty, max, first-of-its-kind, exactly-at-the-limit)
- Negative scenarios (invalid input, denied permission, failure — Given/When/Then too)
- Dependencies / preconditions (data, state, other stories that must land first)
- Function abstraction shape (L1/L2/L3) — does the changed public function read as L1 intent with no L2/L3 leaking in; which L2 domain functions and L3 mechanism functions does it need, and do they already exist or need creating? (`abstraction-levels.md`)
- Git branch to work this story (fit/*, feature/*, refactor/*, ...)
- New simple and representative testcase with **built program integration test** not just unit test. (one concrete example per scenario bullet above — real names/numbers, not "a user" / "some data") — name its fixture (real seed data, mock/stub setup, or existing state it needs) so the test isn't blocked writing it
- **INVEST** check (Independent, Negotiable, Valuable, Estimable, Small, Testable) — a Story failing any letter goes back into the round, not into the spec
- What I want — the observable outcome of the happy path scenario above, not a restatement of it
- How to evaluate it — deterministic check for the line above: integration test or e2e test, per `deterministic-evaluation.md`
- Dogfood test
