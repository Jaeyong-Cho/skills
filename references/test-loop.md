# Test-Loop

A test-loop is a tight, repeatable harness that mirrors the real system as closely as possible. Run it after every change — implementation or bug fix — to see what the system actually does.

The target is **full situational coverage with the real system** — happy path, edge cases, error conditions, and boundary inputs. If a situation can happen in production, the test-loop should be able to exercise it.

## What makes a good test-loop

- **Clean state** — reset and initialize to a known baseline before each run. Delete output dirs, clear caches, reset the database, remove side effects from the previous run, then initialize to the required initial state (seed data, default config, starting conditions). A dirty or uninitialized state hides real behavior.
- **Environment setup** — configure what the system needs before it runs: env vars, seed data, config files, dependency state. Make setup scripted and reproducible.
- **Specific test behaviors** — define the exact scenarios the loop exercises: which inputs, which user actions, which edge cases. Name them. Don't run the whole system blindly.
- **Real-system parity** — same input format, same dependencies, same environment assumptions as production. No stubs unless the dependency is unavailable.
- **Real result output** — the actual system output: stdout, files, API response, database state. Not just pass/fail.
- **Debug output** — intermediate state at each stage, written to a directory. Use `--debug` / `--debug-dir` flags so debug output is opt-in and inspectable after the run.
- **Logs** — runtime log output written to the debug-dir alongside debug artifacts. Logs reveal control flow, errors, and timing that neither the real result nor debug artifacts show.

## Outputs

| Output | What it is | How to use it |
|--------|-----------|---------------|
| Real result | What the system produced | Compare against expected output; flag anything unexpected |
| Debug output | Intermediate state per stage | Trace where the system diverged from expected behavior |
| Logs | Runtime log output | Reveal control flow, errors, and timing; confirm expected log sequences |

## Test layers

Manage UT, IT, and E2E separately — each has different scope, speed, and setup needs. Run them in order.

| Layer | Scope | Setup | When it fails |
|-------|-------|-------|---------------|
| **UT** (unit) | Single function or module in isolation | Minimal — no env, no I/O | Logic error inside the unit |
| **IT** (integration) | Component interactions, real dependencies | Partial env — real DB, real services where possible | Contract or wiring error between components |
| **E2E** (end-to-end) | Full system, real inputs to real outputs | Full env — same as production | System-level behavior broken |

Design the test-loop with each layer in mind. A scenario may have coverage at one or more layers — name which layer covers it.

## Recommended pattern

```bash
# 1. Clean state
rm -rf ./debug-out ./output

# 2. Environment setup
export ENV_VAR=value
# seed data, config, etc.

# 3. Run specific behavior
<entrypoint> --debug --debug-dir ./debug-out <inputs>
```

- Real result goes to stdout or the expected output location
- Debug artifacts land in `./debug-out/` — one file per stage or decision point
- Logs also write to `./debug-out/` — co-located with debug artifacts for easy inspection
- Run → inspect real result → inspect debug output → inspect logs → change → repeat

## Where this fits in the workflow

**Planning (`/planning`)** — reuse before creating. Check if an existing test-loop already covers the needed behaviors; extend it rather than creating a new one. Too many test-loops become unmanageable. Only create a new loop when the existing one structurally cannot cover the scenarios. Design the test-loop explicitly:
- What is the clean state? What must be reset before each run?
- What environment setup is needed? (env vars, seed data, dependencies)
- What specific behaviors does the loop exercise? Name each scenario.
- What are the expected outputs for each behavior?

**Evaluate (`/evaluate`)** — use test-loop output to find unexpected results and their root causes:
- Run each named behavior from the test-loop design
- For each output: is it what you expected? Flag anything unexpected
- For every unexpected result: trace the root cause through debug output and logs
- A passing evaluation criterion should be expressible in terms of test-loop output
