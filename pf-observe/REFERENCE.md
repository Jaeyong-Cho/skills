# Observability Reference

Software systems are not fully knowable in advance. Observability is the practice of making a system's internal state visible so differences, patterns, and causes can be detected and understood.

---

## Part 1: Instrumenting the App

These patterns add debug output *to the app itself* so observation scripts can analyze the results.

### What to Observe

| Category | Examples |
|----------|---------|
| **Source code** | Call site counts, coupling between modules, duplication, dead code, pattern frequency, layer violations |
| **Logs** | Entry/exit of key operations with inputs and outputs; branch decisions; errors with full context; slow queries, retries, cache misses |
| **Environment** | Runtime version, env name (`dev`/`staging`/`prod`), hostname, active feature flags |
| **Versions** | App version, git commit hash, key dependency versions, lock file checksum |
| **Inputs** | HTTP request (method, path, headers, body — redact secrets); function arguments; event payloads |
| **Runtime state** | In-memory caches, DB row counts, file system state, CPU/memory/connections |

### Adding Debug CLI Options

Two flags to add to every app entry point — caller decides where output goes, never hardcoded:

| Flag | Purpose | Values |
|------|---------|--------|
| `--debug-path <dir>` | Directory to write all debug output | any path |
| `--debug-level <level>` | Verbosity | `off` · `info` · `debug` · `trace` |

The pattern (adapt to any language):
1. Parse the two flags
2. If `--debug-path` is set, create the directory
3. Route all debug writes there as structured JSON/JSONL files

```python
# Python example
import argparse, json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--debug-path", default=None)
parser.add_argument("--debug-level", default="off", choices=["off", "info", "debug", "trace"])
args = parser.parse_args()

debug_path = Path(args.debug_path) if args.debug_path else None
if debug_path:
    debug_path.mkdir(parents=True, exist_ok=True)

def debug_write(name: str, data: dict):
    if debug_path:
        (debug_path / name).write_text(json.dumps(data, indent=2, default=str))
```

```go
// Go example
debugPath := flag.String("debug-path", "", "directory to write debug output")
debugLevel := flag.String("debug-level", "off", "off|info|debug|trace")
flag.Parse()
if *debugPath != "" {
    os.MkdirAll(*debugPath, 0755)
}
```

### Writing Structured Logs

Never rely solely on stdout. Write a structured log file (JSONL) so diffs and patterns can be detected later. Each entry needs: timestamp, level, event name, key-value context.

```python
# Python example
import json, time
from pathlib import Path

class StructuredLogger:
    def __init__(self, path: Path | None, level: str = "info"):
        self.path = path
        self._levels = {"off": 0, "info": 1, "debug": 2, "trace": 3}
        self.level = level

    def log(self, level: str, event: str, **kwargs):
        if self._levels.get(level, 0) > self._levels.get(self.level, 1):
            return
        entry = {"t": time.time(), "level": level, "event": event, **kwargs}
        if self.path:
            with open(self.path / "run.jsonl", "a") as f:
                f.write(json.dumps(entry, default=str) + "\n")
```

### Output File Conventions

Write structured files to the `--debug-path` directory during debug runs:

| File | Contents |
|------|---------|
| `env.json` | Environment snapshot (runtime, OS, feature flags) |
| `versions.json` | App version, dependency versions, git hash |
| `input-<id>.json` | Captured input / request payload |
| `state-<id>.json` | Runtime state snapshot |
| `run.jsonl` | Append-only structured log (one JSON object per line) |

---

## Part 2: Writing Observation Scripts

These are standalone scripts in `observe/` that *analyze* the output produced by the instrumented app.

### Script Rules

- **Accept all paths and config as CLI options** — never hardcode file paths, thresholds, or env-specific values
- Print human-readable diffs, summaries, or patterns — not raw JSON
- Runnable standalone with no project imports
- Exit 0 even if nothing found; print `"no data"` if input is missing

### Templates

```python
# Python template
import argparse, json, sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input-dir", required=True, help="debug output directory to analyze")
parser.add_argument("--output-dir", default=None, help="where to write results (optional)")
parser.add_argument("--since", default=None, help="ISO timestamp lower bound")
args = parser.parse_args()

input_dir = Path(args.input_dir)
if not input_dir.exists():
    print("no data")
    sys.exit(0)

# ... analysis logic here ...
```

```bash
# Shell template
#!/usr/bin/env bash
INPUT_DIR="${1:?usage: $0 <input-dir> [output-dir]}"
OUTPUT_DIR="${2:-}"

[ -d "$INPUT_DIR" ] || { echo "no data"; exit 0; }

# ... analysis logic here ...
```

### Visualizing Output

When a visual communicates the observation faster or more clearly than text — use it. No constraint on method or format: ASCII, table, SVG, chart, Mermaid diagram, any library. Pick whatever fits the data and the question being asked.

Save output files to `observe/` and print the path so the user can open them.

Useful libraries: `matplotlib` (SVG/PNG charts), `rich` (terminal tables, progress). Install as needed.
