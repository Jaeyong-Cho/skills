# Debugger CuRS / SRS / AT Item Templates

Used by **sophist-curs** (Step 3b) and **sophist-init** (Step 10d-debugger) when no `#debug` CuRS exists yet.

Substitute `{NNN}` with the next available item numbers in sequence.

---

## CuRS-{NNN}: Runtime Observability via CLI Debug Options

```markdown
# CuRS-{NNN}: Runtime Observability via CLI Debug Options

## State
`draft`

## Tags
`#debug`

## Why
Operators need to diagnose runtime behavior in production and test environments without rebuilding the software. CLI-controlled debug output lets them increase verbosity and capture structured data on demand.

## Traces
- → [SRS-{NNN}](../srs/SRS-{NNN}.md): formalizes debug level control and its semantics
- → [SRS-{NNN+1}](../srs/SRS-{NNN+1}.md): formalizes debug output directory, log format, and data file rules

## Input
> "Operators shall be able to set debug verbosity and output destination via CLI options without rebuilding the software."

## Context
Cross-cutting concern — applies to all components. Must be specified before sophist-impl can instrument log calls and debug data files consistently across the codebase.
```

---

## SRS-{NNN}: Debug Level Control

```markdown
# SRS-{NNN}: Debug Level Control via --debug-level

## State
`draft`

## Tags
`#debug`

## Why
Operators need granular control over how much diagnostic output the system emits, without changing code or restarting with different builds.

## Traces
- ← [CuRS-{NNN}](../curs/CuRS-{NNN}.md): directly formalizes the operator's need to set verbosity at runtime
- → [AT-{NNN}](../at/AT-{NNN}.md): acceptance test verifies --debug-level values and their effect on output

## Description

The system shall accept a `--debug-level` CLI option with the following values:

- `OFF` (default) — suppresses all log output; data file writes still occur if `--debug-output-dir` is set
- `INFO` — SAD-level logging: component boundary crossings, entry/exit of major operations
- `DEBUG` — SDD-level logging: internal algorithm steps, variable values at key decision points
- `VERBOSE` — fine-grained traces: loop iterations, intermediate computations, low-level state

Levels are cumulative: `DEBUG` includes all `INFO` output; `VERBOSE` includes all `DEBUG` and `INFO` output.

### Review needed
- Confirm the four levels (OFF/INFO/DEBUG/VERBOSE) are sufficient or whether additional levels are needed
```

---

## SRS-{NNN+1}: Debug Output Directory, Log Format, and Data File Rules

```markdown
# SRS-{NNN+1}: Debug Output Directory, Log Format, and Data File Rules

## State
`draft`

## Tags
`#debug`

## Why
Consistent output location, log format, and data file behavior are required so that debugging tools, scripts, and human analysts can reliably locate and parse debug artifacts.

## Traces
- ← [CuRS-{NNN}](../curs/CuRS-{NNN}.md): directly formalizes the operator's need to direct output to a known location
- → [AT-{NNN}](../at/AT-{NNN}.md): acceptance test verifies data files appear in the specified directory

## Description

**Output directory**: The system shall accept `--debug-output-dir <path>`. When set, all log output is written to a timestamped log file inside that directory (e.g. `YYYYMMDD-HHMMSS.log`). When omitted, logs are written to stdout only and data file writes are no-ops.

**Data file trigger**: Specifying `--debug-output-dir` alone (without `--debug-level`) shall be sufficient to trigger all structured data file writes. Data files are written regardless of `--debug-level`.

**Log format**: Each log line shall follow the format:
```
<timestamp> <LEVEL> <filename>:<line_number> <message>
```
Source location (`filename:line_number`) is mandatory and shall be configured at the handler, not at call sites.

**Data file writes**: The system shall provide a `write(filename, data, purpose)` operation that:
- Writes `data` to `--debug-output-dir/<filename>`
- Infers format from extension: `.json` → pretty-printed JSON; other extensions → string
- On filename collision, appends a sequence index before the extension (`-1`, `-2`, …) rather than overwriting
- Logs the resulting file path, purpose, and write event to the main log immediately after each write
- Is a no-op when `--debug-output-dir` is not set
- Never raises an exception — debug output must never crash the program

**Data model**: Each component's debug data files shall be documented in the SAD `## Debug strategy` section as a table (`| File | Format | When written | Contents |`), so that the full set of expected debug artifacts is known before implementation.

### Review needed
- Confirm the log timestamp format (ISO 8601 recommended: `2024-01-15T14:30:22`)
- Confirm whether subprocess log capture is needed for this project (only relevant if the project spawns subprocesses)
```

---

## AT-{NNN}: Debug CLI Options — Runtime Verification

_(sophist-curs creates this; sophist-init skips it — AT items are added after requirements are reviewed.)_

```markdown
# AT-{NNN}: Debug CLI Options — Runtime Verification

## State
`draft`

## Tags
`#debug`

## Why
Verifies that the debug contract is fulfilled end-to-end: operators can control verbosity and output location from the CLI without rebuilding.

## Traces
- ← [SRS-{NNN}](../srs/SRS-{NNN}.md): verifies --debug-level values produce correct log output
- ← [SRS-{NNN+1}](../srs/SRS-{NNN+1}.md): verifies --debug-output-dir creates files with correct format

## Preconditions
Application is built and runnable. A temporary output directory exists.

## Steps
1. Run with `--debug-level=INFO` — verify INFO-level log lines appear and DEBUG/VERBOSE do not
2. Run with `--debug-level=DEBUG` — verify both INFO and DEBUG lines appear
3. Run with `--debug-output-dir=<tmp>` only (no `--debug-level`) — verify log file and data files are created in `<tmp>`
4. Inspect the log file — verify each line matches `<timestamp> <LEVEL> <filename>:<line_number> <message>`
5. Inspect a data file — verify format matches the extension (JSON for `.json`)
6. Run a second time with same `--debug-output-dir` — verify colliding filenames get sequence index appended, not overwritten
7. Run with neither flag — verify no files are created and no crash occurs

## Expected result
All seven steps produce their stated outcome without errors or crashes.

## Failure criterion
Any step produces unexpected output, missing files, wrong format, or a program crash.
```
