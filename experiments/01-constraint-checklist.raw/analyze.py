#!/usr/bin/env python3
"""Compare present-only prose gathering with an explicit category checklist."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
ALL = [
    "scope_paths", "structure", "coding_style", "build_test", "interfaces_contracts",
    "dependencies", "branch_versioning", "release_publishing",
    "ownership_approval", "changeability_rollback", "generated_artifacts",
    "security", "deployment", "configuration", "data", "compatibility",
    "performance", "observability", "documentation", "licensing", "process",
]
PATTERNS = {
    "scope_paths": r"`[^`]*(?:/|\\)|file naming|file names|production files",
    "structure": r"markdown structure|document structure|existing document structure",
    "coding_style": r"coding style|formatting|naming conventions",
    "build_test": r"unittest|test suite|verification command",
    "interfaces_contracts": r"public api contract|interface contract",
    "dependencies": r"libraries? or dependencies|current dependencies|dependencies",
    "branch_versioning": r"branch|versioning",
    "release_publishing": r"publish|release",
    "ownership_approval": r"maintainer|final approval|owner approves|owner",
    "changeability_rollback": r"rollback|reversible|safe(?:ly)? change|changeability|unchanged",
    "generated_artifacts": r"generated output|generated",
    "security": r"credentials|secrets|authentication",
    "deployment": r"deployment",
    "configuration": r"configuration|environment variables",
    "data": r"sample data|local data|data",
    "compatibility": r"support python|compatible with|compatib",
    "performance": r"within 2 seconds|latency|performance",
    "observability": r"stdout|test output|logs?",
    "documentation": r"documentation|document the result",
    "licensing": r"licens",
    "process": r"requirements|boundaries|documentation-only|verification command|production files may be changed",
}

def cases(text):
    found = re.findall(r"^## Case ([A-Z]):.*?$", text, re.MULTILINE)
    out = {}
    for i, name in enumerate(found):
        start = re.search(rf"^## Case {name}:.*?$", text, re.MULTILINE).end()
        end = (re.search(rf"^## Case {found[i+1]}:.*?$", text, re.MULTILINE).start()
               if i + 1 < len(found) else len(text))
        out[name] = text[start:end].strip()
    return out

def present(text):
    return sorted(name for name in ALL if re.search(PATTERNS[name], text, re.IGNORECASE))

def main():
    text = (ROOT / "input.md").read_text()
    gold = json.loads((ROOT / "gold.json").read_text())["expected_present"]
    results = []
    totals = {"tp": 0, "fp": 0, "fn": 0}
    for name, body in cases(text).items():
        actual = set(present(body))
        expected = set(gold[name])
        checklist_missing = set(ALL) - actual
        gold_missing = set(ALL) - expected
        tp = len(checklist_missing & gold_missing)
        fp = len(checklist_missing - gold_missing)
        fn = len(gold_missing - checklist_missing)
        totals["tp"] += tp
        totals["fp"] += fp
        totals["fn"] += fn
        results.append({
            "case": name,
            "prose_only_present": sorted(actual),
            "prose_only_missing_report": [],
            "checklist_missing": sorted(checklist_missing),
            "gold_missing": sorted(gold_missing),
            "missing_counts": {"checklist": len(checklist_missing), "gold": len(gold_missing)},
            "checklist_error_counts": {"tp": tp, "fp": fp, "fn": fn},
        })
    precision = totals["tp"] / (totals["tp"] + totals["fp"]) if totals["tp"] + totals["fp"] else None
    recall = totals["tp"] / (totals["tp"] + totals["fn"]) if totals["tp"] + totals["fn"] else None
    baseline_recall = 0 if sum(len(r["gold_missing"]) for r in results) else 1
    print(json.dumps({
        "method": "same cue extractor; prose-only reports present categories, checklist reports all absent categories",
        "categories": ALL,
        "cases": results,
        "aggregate": {
            "gold_missing_total": sum(len(r["gold_missing"]) for r in results),
            "checklist_missing_detection": totals,
            "checklist_missing_precision": precision,
            "checklist_missing_recall": recall,
            "prose_only_missing_recall": baseline_recall,
        },
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
