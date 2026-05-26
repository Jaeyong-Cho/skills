# Observability Reference

Software systems are not fully knowable in advance. Observability is the practice of making a system's internal state visible so differences, patterns, and causes can be detected and understood.

---

## What to Observe

### Logs
Structured records of what happened. Write to file, not just stdout.

- Entry/exit of key operations with inputs and outputs
- Branch decisions and the reason taken
- Errors with full context (input values, state at time of failure)
- Performance-relevant events (slow queries, retries, cache misses)

### Environment
Captured once at startup or entry point.

- Runtime version (Python 3.11.2, Node 20.5.0, etc.)
- Environment name (`development`, `staging`, `production`)
- Hostname, OS, architecture
- Active feature flags and their values

### Versions and Dependencies
Captured at startup or in a dedicated script.

- Application version / git commit hash
- Key dependency versions (framework, database client, etc.)
- Lock file hash or checksum for reproducibility

### Inputs and Requests
Captures what entered the system.

- HTTP request: method, path, headers, body (redact secrets)
- Function arguments for key entry points
- Event payloads, queue messages, file contents

### Runtime State
Snapshots of what the system holds in memory or on disk.

- In-memory caches, queues, connection pools
- Database query results and row counts
- File system state (existence, size, modification time)
- Resource usage: CPU, memory, open file descriptors, network connections

---

## CLI Debug Options

Implement these flags in entry points to enable observation without code changes:

| Flag | Purpose | Example |
|------|---------|---------|
| `--debug-path <dir>` | Write all debug output to this directory | `--debug-path ./observe/output` |
| `--debug-level <level>` | Verbosity: `off`, `info`, `debug`, `trace` | `--debug-level debug` |
| `--log-inputs` | Capture and write all inputs to file | |
| `--snapshot-state` | Write runtime state snapshot to file at exit | |
| `--dry-run` | Run without side effects, log what would happen | |

Example entry point pattern:

```python
import argparse, json, os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--debug-path", default=None)
parser.add_argument("--debug-level", default="off", choices=["off", "info", "debug", "trace"])
parser.add_argument("--log-inputs", action="store_true")
parser.add_argument("--snapshot-state", action="store_true")
args = parser.parse_args()

debug_path = Path(args.debug_path) if args.debug_path else None
if debug_path:
    debug_path.mkdir(parents=True, exist_ok=True)

def debug_write(name: str, data: dict):
    if debug_path:
        (debug_path / name).write_text(json.dumps(data, indent=2, default=str))
```

---

## Observation File Conventions

Write structured files (JSON or JSONL) to `observe/output/` during debug runs:

| File | Contents |
|------|---------|
| `env.json` | Environment snapshot (runtime, OS, feature flags) |
| `versions.json` | App version, dependency versions, git hash |
| `input-<id>.json` | Captured input / request payload |
| `state-<id>.json` | Runtime state snapshot |
| `run.jsonl` | Append-only structured log (one JSON object per line) |

---

## Logging to File

Never rely solely on stdout. Write a structured log file so diffs and patterns can be detected later.

```python
import json, time
from pathlib import Path

class StructuredLogger:
    def __init__(self, path: Path | None, level: str = "info"):
        self.path = path
        self.level = level
        self._levels = {"off": 0, "info": 1, "debug": 2, "trace": 3}

    def log(self, level: str, event: str, **kwargs):
        if self._levels.get(level, 0) > self._levels.get(self.level, 1):
            return
        entry = {"t": time.time(), "level": level, "event": event, **kwargs}
        if self.path:
            with open(self.path / "run.jsonl", "a") as f:
                f.write(json.dumps(entry, default=str) + "\n")
```

---

## Observe Script Conventions

Scripts in `observe/` should:

- Accept `--path` to point at an output directory from a debug run
- Print human-readable diffs, summaries, or patterns — not raw JSON
- Be runnable standalone with no project imports
- Exit 0 even if nothing found; print `"no data"` if output dir is missing
