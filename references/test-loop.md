# Test-Loop

A test-loop is a tight, repeatable harness that mirrors the real system as closely as possible. Run it after every change — implementation or bug fix — to see what the system actually does.

## What makes a good test-loop

- **Real-system parity** — same input format, same dependencies, same environment assumptions as production. No stubs unless the dependency is unavailable.
- **Real result output** — the actual system output: stdout, files, API response, database state. Not just pass/fail.
- **Debug output** — intermediate state at each stage, written to a directory. Use `--debug` / `--debug-dir` flags so debug output is opt-in and inspectable after the run.
- **Logs** — runtime log output from the system. Logs are in scope: they reveal control flow, errors, and timing that neither the real result nor debug artifacts show.

## Outputs

| Output | What it is | How to use it |
|--------|-----------|---------------|
| Real result | What the system produced | Compare against expected output to judge correctness |
| Debug output | Intermediate state per stage | Trace where the system diverged from expected behavior |
| Logs | Runtime log output | Reveal control flow, errors, and timing; confirm expected log sequences |

## Recommended pattern

```bash
<entrypoint> --debug --debug-dir ./debug-out <inputs>
```

- Real result goes to stdout or the expected output location
- Debug artifacts land in `./debug-out/` — one file per stage or decision point
- Logs go to stderr or a log file — capture them alongside the run
- Run → inspect real result → inspect debug output → inspect logs → change → repeat

## Where this fits in the workflow

**Planning (`/planning`)** — include the test-loop in the action sequence:
1. Set up the test-loop before implementing
2. Verify the loop runs and produces all three output types
3. Implement the feature or fix
4. Run the loop to evaluate

**Evaluate (`/evaluate`)** — use test-loop output as the primary evaluation signal:
- Real result output is the ground truth for correctness
- Debug output is the trace for diagnosing failures
- Logs confirm expected sequences (e.g. "log A → log B means the path was taken")
- A passing evaluation criterion should be expressible in terms of test-loop output
