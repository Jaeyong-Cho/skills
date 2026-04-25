# Debugger Specification (Shared)

Used by sophist-impl, sophist-lazy, and any skill that instruments or documents debug output.

---

## Default Debugger model

When no Debugger SAD/SDD items exist in the SOPHIST book, apply this spec. After implementing, suggest the human capture it as SOPHIST items via sophist-curs.

| Requirement | Detail |
|-------------|--------|
| **Output destination** | `--debug-output-dir <path>` — all debug output (log file + data files) written to this directory. Omit to send logs to stdout only; omitting also makes data writes and subprocess log captures no-ops. **Specifying `--debug-output-dir` alone (without `--debug-level`) is sufficient to trigger all data file output automatically.** |
| **Enable/disable** | `--debug-level=OFF` (default) suppresses all log output but data file writes still occur when `--debug-output-dir` is set |
| **Levels** | `INFO` → `DEBUG` → `VERBOSE` in ascending detail. Higher levels are cumulative. |
| **Level semantics** | `INFO` — SAD-level (component boundary crossings); `DEBUG` — SDD-level (internal algorithm steps); `VERBOSE` — fine-grained traces |
| **Log format** | `<timestamp> <level> <filename>:<line_number> <message>` — source location is mandatory, configured at the handler not at call sites |
| **Interface** | `info(msg)`, `debug(msg)`, `verbose(msg)`, `warning(msg)`, `error(msg)` for log lines; `write(filename, data, purpose)` for structured data files; `subprocess_log_path(name)` for subprocess log routing |

**`write(filename, data, purpose)`** writes `data` to `--debug-output-dir/<filename>`. If a file with that name already exists, appends a sequence index (`-1`, `-2`, …) before the extension to avoid conflicts. After writing, logs the file path, purpose, and write event to the main log. Infers format from extension (`.json` → JSON, anything else → string). No-op when `--debug-output-dir` is not set. Never raises.

**`subprocess_log_path(name)`** returns a unique file path inside `--debug-output-dir` for a subprocess to write its stdout/stderr to (e.g. `<dir>/<name>-<timestamp>.log`). Returns `None` when `--debug-output-dir` is not set. The caller records the returned path and the start time in the main log before launching the subprocess, and logs completion after it exits.

**Data model**: every file written via `write()` should correspond to a row in the item's `## Debug data` table, which defines `filename`, `format`, `when written`, `purpose`, and `contents`. This table is the data model — it ensures all debugging-relevant state is captured in a predictable schema that analysis tools and humans can rely on.

---

## Reference implementation (Python)

This illustrates the required behaviors. Adapt the language, style, file name, and class structure to the project — it is **one example, not a prescription**.

```python
# Example: debugger.py (Python) — adapt name, structure, and idioms to your project's language
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
        if self._threshold >= 1: self._log.warning(msg)

    def error(self, msg: str) -> None:
        if self._threshold >= 1: self._log.error(msg)

    def write(self, filename: str, data, purpose: str = "") -> None:
        """Write structured debug data to --debug-output-dir.
        No-op if dir is unset. Triggered by --debug-output-dir alone,
        regardless of --debug-level. Appends -N index on filename collision.
        Logs file path, purpose, and write event to main log."""
        if not self._dir:
            return
        try:
            os.makedirs(self._dir, exist_ok=True)
            # Resolve collision: append -1, -2, ... before extension
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
            # Log metadata to main log
            self._log.info(f"[debug-write] path={candidate} purpose={purpose or 'unspecified'}")
        except Exception:
            pass  # debug output must never crash the program

    def subprocess_log_path(self, name: str) -> str | None:
        """Return a unique log file path for a subprocess to write stdout/stderr to.
        Returns None when --debug-output-dir is not set (caller skips capture).
        Caller must log the returned path and start time before launching the subprocess,
        and log completion (exit code, duration) after it exits."""
        if not self._dir:
            return None
        os.makedirs(self._dir, exist_ok=True)
        return os.path.join(self._dir, f"{name}-{datetime.now():%Y%m%d-%H%M%S}.log")
```

Construct the Debugger once at application entry from the CLI options, then pass it to every component that needs it. Components call `debugger.info(...)`, `debugger.write(...)` — they never access `--debug-output-dir` directly.
