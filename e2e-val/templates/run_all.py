#!/usr/bin/env python3
"""Run all E2E validation cases for <slug>."""

import subprocess, json, glob, os, sys
from datetime import datetime

# Embedded at scaffold time by e2e-val skill — do not edit manually.
KANAGAWA_CSS = """
<KANAGAWA_CSS_PLACEHOLDER>
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
