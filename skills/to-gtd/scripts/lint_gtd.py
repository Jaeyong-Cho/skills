#!/usr/bin/env python3
"""
Lint the GTD document tree written by @skills/to-gtd.

Checks, per file:
- Every .md file except index.md/log.md (OKF's reserved names) starts with a
  frontmatter block carrying all six OKF fields.
- Every `- [ ]`/`- [x]` checkbox line is well-formed (space after the bracket).
- waiting-for.md lines end in "waiting on {who}, follow up {YYYY-MM-DD}".
- calendar.md lines start with "{YYYY-MM-DD}: ".
- projects/*.md (not index.md) has an "## Outcome" heading.
- archive/*/*/log.md lines start with an ISO-8601 timestamp.
- every relative markdown link in an index.md resolves to a real file.

Usage:
  python lint_gtd.py <gtd-root-dir>

Exit code 0 if every check passes, 1 otherwise (one line per violation).
"""
import re
import sys
from datetime import datetime
from pathlib import Path

FRONTMATTER_KEYS = ["type", "title", "description", "tags", "timestamp"]
CHECKBOX_RE = re.compile(r"^- \[([ xX])\] (.+)$")
BAD_CHECKBOX_RE = re.compile(r"^-\s*\[[ xXfF]?\]")
WAITING_RE = re.compile(r"— waiting on .+, follow up (\d{4}-\d{2}-\d{2})$")
CALENDAR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}): .+$")
LOG_LINE_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def is_valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def check_frontmatter(path, lines, errors):
    if path.name in ("index.md", "log.md"):
        return
    if not lines or lines[0].rstrip("\n") != "---":
        errors.append(f"{path}:1: missing frontmatter (must start with '---')")
        return
    try:
        end = lines[1:].index("---\n") + 1
    except ValueError:
        errors.append(f"{path}:1: frontmatter block never closes with '---'")
        return
    block = "".join(lines[1:end])
    for key in FRONTMATTER_KEYS:
        if not re.search(rf"^{key}:", block, re.MULTILINE):
            errors.append(f"{path}:1: frontmatter missing '{key}:' field")


def check_checkboxes(path, lines, errors):
    for i, line in enumerate(lines, start=1):
        stripped = line.rstrip("\n")
        if not stripped.startswith("-"):
            continue
        if CHECKBOX_RE.match(stripped):
            continue
        if BAD_CHECKBOX_RE.match(stripped) or re.match(r"^-\[", stripped):
            errors.append(f"{path}:{i}: malformed checkbox line: {stripped!r}")


def check_waiting_for(path, lines, errors):
    for i, line in enumerate(lines, start=1):
        m = CHECKBOX_RE.match(line.rstrip("\n"))
        if not m:
            continue
        wm = WAITING_RE.search(m.group(2))
        if not wm:
            errors.append(f"{path}:{i}: waiting-for line missing 'waiting on ..., follow up YYYY-MM-DD'")
        elif not is_valid_date(wm.group(1)):
            errors.append(f"{path}:{i}: invalid follow-up date {wm.group(1)!r}")


def check_calendar(path, lines, errors):
    for i, line in enumerate(lines, start=1):
        m = CHECKBOX_RE.match(line.rstrip("\n"))
        if not m:
            continue
        cm = CALENDAR_RE.match(m.group(2))
        if not cm:
            errors.append(f"{path}:{i}: calendar line must start with 'YYYY-MM-DD: '")
        elif not is_valid_date(cm.group(1)):
            errors.append(f"{path}:{i}: invalid calendar date {cm.group(1)!r}")


def check_project(path, lines, errors):
    if not any(line.rstrip("\n") == "## Outcome" for line in lines):
        errors.append(f"{path}:1: project file missing '## Outcome' heading")


def check_log(path, lines, errors):
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        m = LOG_LINE_RE.match(line.rstrip("\n"))
        if not m:
            errors.append(f"{path}:{i}: archive log line missing leading ISO timestamp")


def check_links(path, lines, errors):
    for i, line in enumerate(lines, start=1):
        for target in LINK_RE.findall(line):
            if target.startswith(("http://", "https://", "#")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path}:{i}: dangling link -> {target}")


def lint_file(path, root, errors):
    lines = path.read_text().splitlines(keepends=True)
    check_frontmatter(path, lines, errors)
    check_checkboxes(path, lines, errors)
    rel = path.relative_to(root)
    if path.name == "waiting-for.md":
        check_waiting_for(path, lines, errors)
    if path.name == "calendar.md":
        check_calendar(path, lines, errors)
    if rel.parts[0:1] == ("projects",) and path.name != "index.md":
        check_project(path, lines, errors)
    if path.name == "log.md":
        check_log(path, lines, errors)
    if path.name == "index.md":
        check_links(path, lines, errors)


def lint_tree(root):
    errors = []
    for path in sorted(root.rglob("*.md")):
        lint_file(path, root, errors)
    return errors


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"{root}: not a directory")
        sys.exit(1)
    errors = lint_tree(root)
    for e in errors:
        print(e)
    if errors:
        print(f"FAIL — {len(errors)} violation(s)")
        sys.exit(1)
    print("OK")
    sys.exit(0)


def self_test():
    import shutil
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    try:
        good_fm = (
            "---\ntype: GTD Next Actions\ntitle: Next Actions\n"
            "description: d\ntags: [gtd]\ntimestamp: 2026-08-25T00:00:00+09:00\n---\n\n"
        )
        (tmp / "next-actions.md").write_text(good_fm + "## Next\n- [ ] call dentist\n")
        (tmp / "index.md").write_text("# GTD\n- [Next Actions](./next-actions.md)\n- [Missing](./nope.md)\n")
        (tmp / "waiting-for.md").write_text(
            good_fm + "- [ ] invoice — waiting on Sam, follow up 2026-09-01\n"
            "- [ ] broken line with no date\n"
        )
        (tmp / "calendar.md").write_text(good_fm + "- [ ] 2026-09-01: dentist\n- [ ] not-a-date: oops\n")
        (tmp / "projects").mkdir()
        (tmp / "projects" / "index.md").write_text("# Projects\n")
        (tmp / "projects" / "taxes.md").write_text(good_fm + "# Taxes\n\n## Next Actions\n- [ ] email accountant\n")
        (tmp / "archive").mkdir(parents=True)
        (tmp / "archive" / "log.md").write_text("- 2026-08-25T09:00:00 [next-actions] call dentist\n- not a log line\n")

        errors = lint_tree(tmp)
        joined = "\n".join(errors)

        assert any("nope.md" in e for e in errors), "should catch dangling link"
        assert any("waiting-for.md" in e and "waiting on" in e for e in errors), "should catch bad waiting-for line"
        assert any("calendar.md" in e for e in errors), "should catch bad calendar date"
        assert any("taxes.md" in e and "Outcome" in e for e in errors), "should catch missing Outcome heading"
        assert any("archive" in e and "timestamp" in e for e in errors), "should catch bad log line"
        assert not any("next-actions.md" in e for e in errors), f"next-actions.md should be clean, got:\n{joined}"
        print("self-test passed")
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        self_test()
    else:
        main()
