---
name: e2e-val
description: |
  Scaffold, run, and report E2E validation for a feature — generates test cases from grill/impl conclusions, runs each standalone, writes a lightweight HTML stats report (run_all.py) and a rich analysis HTML report (skill).
  Use whenever the user wants to E2E test, validate, or smoke-test implemented code with real sample data. Triggers: "e2e-val", "e2e test", "end-to-end test", "validate this feature", "add E2E", "sample test", "run validation", or any request to test implemented code with real inputs and check outputs.
---

Read `../pf/references/caveman.md` and apply caveman style throughout.

Check journal context:

```bash
[ -n "$PFJ_PATH" ] && cat "$PFJ_PATH/today.md" 2>/dev/null
```

For layer definitions, read `../pf/references/layers.md`.

---

# VAO Validation

## Directory structure

```
validate/<slug>/
  cases/
    01-<name>/
      run.py        ← standalone: python run.py
      input.json
      expected.json
      result.json   ← written by run.py after execution
  run_all.py        ← runs all cases, writes report.html
  report.html       ← lightweight: stats + pass/fail table only
```

---

## Step 1: Resolve slug + source

If user provides feature name or slug, use it. Otherwise ask.

Check if scaffold already exists:

```bash
ls validate/<slug>/ 2>/dev/null
```

If exists → skip to Step 4 (run).

Read grill/impl conclusions from context. If not in context, ask user to describe the feature's happy path, edge cases, and error cases.

---

## Step 2: Derive cases

From conclusions, derive all cases grouped by type:

```
Happy path:
  01-<name>   — normal input, expect success
  ...

Edge cases:
  02-<name>   — boundary or unusual input
  ...

Error cases:
  03-<name>   — invalid input, missing data, failure scenario
  ...
```

Show list. Ask via `AskUserQuestion`: "Add or remove any cases?" — adjust before scaffolding.

---

## Step 3: Scaffold

Create directory structure:

```bash
mkdir -p validate/<slug>/cases
```

For each case, create `validate/<slug>/cases/<N>-<name>/`:

**`input.json`** — sample input data derived from case description.

**`expected.json`** — expected output or response derived from feature design.

**`run.py`** — standalone script:

```python
#!/usr/bin/env python3
"""Case: <name> — <one-line description>"""

import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

# --- setup ---
with open(os.path.join(os.path.dirname(__file__), 'input.json')) as f:
    input_data = json.load(f)
with open(os.path.join(os.path.dirname(__file__), 'expected.json')) as f:
    expected = json.load(f)

logs = []

def log(msg):
    logs.append(msg)
    print(msg)

# --- run ---
try:
    # TODO: call the actual feature code here
    actual = None  # replace with real call

    # --- assertions ---
    passed = actual == expected
    # add rule-based assertions as needed

    status = "PASS" if passed else "FAIL"
    log(f"[{status}] actual={actual!r} expected={expected!r}")

except Exception as e:
    passed = False
    status = "ERROR"
    log(f"[ERROR] {e}")
    actual = None

# --- write result ---
result = {
    "case": "<N>-<name>",
    "status": status,
    "passed": passed,
    "actual": actual,
    "expected": expected,
    "logs": logs,
}
with open(os.path.join(os.path.dirname(__file__), 'result.json'), 'w') as f:
    json.dump(result, f, indent=2)

print(f"\n{'✅ PASS' if passed else '❌ FAIL'}: <name>")
sys.exit(0 if passed else 1)
```

**`validate/<slug>/run_all.py`** — runs all cases, collects results, writes `report.html`:

When generating this file, read `~/.claude/skills/pfj-grill/kanagawa.css` and embed its full contents as the `KANAGAWA_CSS` string literal below. Do not reference the file path at runtime — embed verbatim.

```python
#!/usr/bin/env python3
"""Run all E2E validation cases for <slug>."""

import subprocess, json, glob, os, sys
from datetime import datetime

KANAGAWA_CSS = """
<embed full contents of ~/.claude/skills/pfj-grill/kanagawa.css here verbatim>
"""

base = os.path.dirname(__file__)
case_dirs = sorted(glob.glob(os.path.join(base, 'cases', '*')))

results = []
for case_dir in case_dirs:
    run_py = os.path.join(case_dir, 'run.py')
    if not os.path.exists(run_py):
        continue
    print(f"\n→ {os.path.basename(case_dir)}")
    subprocess.run([sys.executable, run_py], capture_output=False)
    result_path = os.path.join(case_dir, 'result.json')
    if os.path.exists(result_path):
        with open(result_path) as f:
            results.append(json.load(f))

# --- summary ---
total = len(results)
passed = sum(1 for r in results if r.get('passed'))
failed = total - passed
print(f"\n{'='*40}")
print(f"Results: {passed}/{total} passed")

# --- HTML report (kanagawa theme, stats only) ---
rows = ''.join(
    f"<tr><td>{r['case']}</td>"
    f"<td>{'✅ PASS' if r['passed'] else '❌ FAIL'}</td>"
    f"<td><code>{r.get('logs', [''])[-1] if r.get('logs') else ''}</code></td></tr>"
    for r in results
)
pct = int(passed / total * 100) if total else 0
html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>e2e-val: <slug></title>
<style>{KANAGAWA_CSS}
.bar-wrap{{background:var(--bg-dim,#1f1f28);border-radius:4px;height:1rem;margin:.5rem 0}}
.bar{{background:var(--green,#76946a);height:100%;border-radius:4px;width:{pct}%}}
</style></head><body>
<h1>e2e-val: <slug></h1>
<p>{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<div class="bar-wrap"><div class="bar"></div></div>
<p>{passed}/{total} passed ({pct}%)</p>
<table>
<tr><th>Case</th><th>Result</th><th>Last log</th></tr>
{rows}
</table>
<hr><footer>run_all.py · {datetime.now().strftime('%Y-%m-%d')}</footer>
</body></html>"""

report_path = os.path.join(base, 'report.html')
with open(report_path, 'w') as f:
    f.write(html)
print(f"\nReport: {report_path}")
sys.exit(0 if failed == 0 else 1)
```

---

## Step 4: Run

```bash
cd <project-root>
python validate/<slug>/run_all.py
```

Print stdout as it runs. Show final pass/fail count.

---

## Step 5: Rich HTML report

Follow `../pfj-grill/REPORT.md` for structure, styling, interactivity, and generation rules.

Read all `validate/<slug>/cases/*/result.json` files.

Save: `.pf/reports/validate/YYYY/MM-DD-<slug>.html`

```bash
mkdir -p .pf/reports/validate/YYYY
```

Header: `validate: <slug>` · date · one-line outcome.
Footer: `Generated by pf-validate · date · slug`

**Always include:**
- **Pass rate** — progress bar: passed / total, broken down by type (happy/edge/error)
- **Results table** — case name, type, status (✅/❌/⚠️), last log line
- **Failure analysis** — for each failed case: actual vs expected diff, log trace, likely cause

**Include when content warrants:**
- **Pattern analysis** — which layer (value/aspect/object) has most failures → where the bug lives
- **Log patterns** — recurring log messages across cases; signal vs noise
- **Coverage map** — which scenarios covered vs missing; gaps to add next

Print path:
```
Report: .pf/reports/validate/YYYY/MM-DD-<slug>.html
```
