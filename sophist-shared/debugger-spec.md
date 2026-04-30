# Debugger Specification (Shared)

Used by sophist-impl, sophist-lazy, and any skill that instruments or documents debug output.

---

## Contract (language-agnostic)

These behaviors must be preserved regardless of language or implementation style. Everything else is free to adapt.

| Requirement | Detail |
|-------------|--------|
| **Output destination** | `--debug-output-dir <path>` — all debug output (log file + data files) written to this directory. Omit to send logs to stdout only; omitting also makes data writes and subprocess log captures no-ops. **Specifying `--debug-output-dir` alone (without `--debug-level`) is sufficient to trigger all data file output automatically.** |
| **Enable/disable** | `--debug-level=OFF` (default) suppresses `INFO`/`DEBUG`/`VERBOSE` log output, but data file writes still occur when `--debug-output-dir` is set. `WARNING` and `ERROR` are never suppressed — they emit at all levels including `OFF`. |
| **Levels** | `INFO` → `DEBUG` → `VERBOSE` in ascending detail. Higher levels are cumulative. `WARNING` and `ERROR` sit outside this hierarchy — they are always on. |
| **Level semantics** | `INFO` — SAD-level (component boundary crossings); `DEBUG` — SDD-level (internal algorithm steps); `VERBOSE` — fine-grained traces; `WARNING` — recoverable anomaly (always emitted); `ERROR` — operation failed (always emitted) |
| **Log format** | `<timestamp> <level> <filename>:<line_number> <message>` — source location is mandatory, configured at the handler not at call sites |
| **Log methods** | `info(msg)`, `debug(msg)`, `verbose(msg)` — gated by `--debug-level`; `warning(msg)`, `error(msg)` — bypass the threshold entirely, always emitted |
| **Data write** | `write(filename, data, purpose)` — writes to `--debug-output-dir/<filename>`, infers format from extension (`.json` → JSON, else string), appends sequence index on collision, logs the write event to the main log, never raises |
| **Subprocess routing** | optional — only implement if the project spawns subprocesses; returns a unique log path inside `--debug-output-dir`, or null/None when unset |

**Data model**: every file written via `write()` corresponds to a row in the item's `## Debug data` table (`filename`, `format`, `when written`, `purpose`, `contents`). This is what makes debug output predictable and analysable.

**Single owner**: construct the Debugger once at application entry and pass it to every component. Components never access `--debug-output-dir` or the filesystem directly.

---

## Adapting to your project

Before implementing, read the project to understand its conventions:

- **Language and idioms** — use the project's natural logging library, file I/O patterns, and module/class structure. A Go project uses a struct with methods; a TypeScript project might use a class or a module-level singleton; a shell script uses functions and environment variables. Don't impose an alien style.
- **CLI flag parsing** — use whatever the project already uses (argparse, cobra, yargs, flags, env vars). The flag names `--debug-level` and `--debug-output-dir` are the external contract; the parsing mechanism is not.
- **Subprocess pattern** — only implement `subprocess_log_path` if the project actually spawns subprocesses. Many projects don't need it.
- **Error handling** — match the project's style for silent failures in non-critical paths. The key invariant is: debug output must never crash the program.
- **File/module name** — name it whatever fits the project (`debugger.py`, `debug.go`, `logger.ts`, `debug.sh`, etc.).

The contract is the interface (levels, write(), log format, CLI flags). The implementation is yours to shape.

---

## Reference implementation (Python)

Illustrates the required behaviors in Python. Use this as a mental model, not a template to copy.

```python
import json, logging, os
from datetime import datetime

class Debugger:
    _LEVELS = {"OFF": 0, "INFO": 1, "DEBUG": 2, "VERBOSE": 3}

    def __init__(self, debug_level: str = "OFF", debug_output_dir: str | None = None):
        self._threshold = self._LEVELS.get(debug_level.upper(), 0)
        self._dir = debug_output_dir
        self._log = self._make_logger(debug_output_dir)

    def _make_logger(self, output_dir: str | None) -> logging.Logger:
        log = logging.getLogger("app.debugger")
        log.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s")
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            h = logging.FileHandler(os.path.join(output_dir, f"{datetime.now():%Y%m%d-%H%M%S}.log"))
        else:
            h = logging.StreamHandler()
        h.setFormatter(fmt)
        log.addHandler(h)
        return log

    def info(self, msg: str) -> None:
        if self._threshold >= 1: self._log.info(msg)

    def debug(self, msg: str) -> None:
        if self._threshold >= 2: self._log.debug(msg)

    def verbose(self, msg: str) -> None:
        if self._threshold >= 3: self._log.debug(f"[VERBOSE] {msg}")

    def warning(self, msg: str) -> None:
        self._log.warning(msg)  # always emitted — not gated by threshold

    def error(self, msg: str) -> None:
        self._log.error(msg)  # always emitted — not gated by threshold

    def write(self, filename: str, data, purpose: str = "") -> None:
        if not self._dir:
            return
        try:
            os.makedirs(self._dir, exist_ok=True)
            base, ext = os.path.splitext(filename)
            candidate = os.path.join(self._dir, filename)
            idx = 1
            while os.path.exists(candidate):
                candidate = os.path.join(self._dir, f"{base}-{idx}{ext}")
                idx += 1
            with open(candidate, "w") as f:
                if filename.endswith(".json"):
                    json.dump(data, f, indent=2)
                else:
                    f.write(str(data))
            self._log.info(f"[debug-write] path={candidate} purpose={purpose or 'unspecified'}")
        except Exception:
            pass

    def subprocess_log_path(self, name: str) -> str | None:
        if not self._dir:
            return None
        os.makedirs(self._dir, exist_ok=True)
        return os.path.join(self._dir, f"{name}-{datetime.now():%Y%m%d-%H%M%S}.log")
```
