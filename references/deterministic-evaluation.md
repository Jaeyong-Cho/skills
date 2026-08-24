# Deterministic Evaluation Method

**Deterministic** means the pass/fail check gives the same verdict rerun after rerun — no eyeballing, no LLM-as-judge, no "looks right." A checklist point only counts as answered once it names one of the two:

## Integration test

Exercises the change at a component boundary — real adjacent module/DB/queue, not the full user-facing path. Pick when the change lives inside one service/module and the risk is in how components wire together, not in the end-to-end flow.

## E2E test

Exercises the full user-facing flow through the real system, structured per `test-loop.md` (`run` writes outputs, `verify` checks them against expected). Pick when the change is only provable by walking the same path a real user/caller takes, or the risk spans service boundaries.

## Naming it

For each acceptance criterion: name the test type (integration/e2e), the file/path (existing or to be written), and the exact observable pass/fail signal (a returned value, a DB row, an HTTP status — not "the output looks correct"). This is what `@skills/to-plan`'s Verification Method column and `@skills/do-plan`'s acceptance-criteria check both consume.
