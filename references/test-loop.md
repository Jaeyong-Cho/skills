# Test-Loop

A test-loop is an E2E harness that runs the real system against real inputs and verifies the outputs. It lives under `tests/e2e/{topic}/`.

The target is **full situational coverage with the real system** — happy path, edge cases, error conditions, and boundary inputs. If a situation can happen in production, the test-loop should be able to exercise it.

## Structure

```
tests/e2e/{topic}/
├── run.py      # or run.sh — execute the system, write outputs
├── verify.py   # or verify.sh — read outputs, check results
└── data/       # input data, fixtures, seed files
```

## Run

`run.py / run.sh` — execute the system and write all outputs to a result directory:
- System outputs (files, API responses, DB state)
- Metadata the verifier needs: version, input data, timestamps, config, environment info
- Debug output and logs (use `--debug-dir`)

```bash
python tests/e2e/{topic}/run.py --output-dir ./e2e-out --debug-dir ./e2e-out/debug
# writes: ./e2e-out/result.json, ./e2e-out/meta.json, ./e2e-out/debug/...
```

## Verify

`verify.py / verify.sh` — read the result directory and check outputs:
- Reads metadata (version, inputs) written by run to know what to verify
- Compares actual outputs against expected per scenario
- Reports: good / unexpected / ambiguous — with root cause from debug output and logs

```bash
python tests/e2e/{topic}/verify.py --output-dir ./e2e-out
```

Run once, verify many times. Compare output dirs across versions to spot regressions.

## Clean state

Reset and initialize before each run — delete output dirs, clear caches, reset DB, then initialize to the required starting state (seed data, default config). A dirty or uninitialized state hides real behavior.

## Where this fits in the workflow

**Planning (`/planning`)** — reuse before creating. Check if an existing test-loop under `tests/e2e/` already covers the needed behaviors; extend it rather than creating a new topic. Only create a new `tests/e2e/{topic}/` when structurally needed.

Design explicitly:
- What is the clean state?
- What does `run` write to the output dir? (results, metadata: version, input data, config)
- What does `verify` check per scenario?

**Evaluate (`/evaluate`)** — run the test-loop and use its output as the primary evaluation signal:
- Run `run.py`, then `verify.py`
- For every unexpected result: trace root cause through debug output and logs
