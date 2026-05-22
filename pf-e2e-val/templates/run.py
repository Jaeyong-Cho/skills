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
