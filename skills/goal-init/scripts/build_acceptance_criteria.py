#!/usr/bin/env python3
"""
Rebuild the "## Acceptance Criteria" section of goal.md from every
"**Answer:** Supported|Refuted -- <takeaway>" line under a "## Question N"
heading. Inconclusive/unanswered questions are skipped -- no settled claim to
turn into a criterion yet. Idempotent: re-running replaces the section in
place and preserves any box a human/e2p already checked (matched by text).

Usage:
  python build_acceptance_criteria.py [goal.md]

Called by /goal-init (after recording questions) and by /experiment's Publish
stage (after it writes a question's Answer line) -- same script either way,
don't reimplement it.
"""
import sys, re

ANSWER_RE = re.compile(
    r"^\*\*Answer:\*\*\s*(Supported|Refuted)\s*(?:--|—|-)\s*(.+)$", re.MULTILINE
)
SECTION_RE = re.compile(r"\n?## Acceptance Criteria\n.*?(?=\n## |\Z)", re.DOTALL)
EXISTING_ITEM_RE = re.compile(r"^- \[( |x)\] (.+)$", re.MULTILINE)


def build_section(text):
    criteria = [
        f"{verdict} -- {takeaway.strip()}"
        for verdict, takeaway in ANSWER_RE.findall(text)
    ]

    checked = {
        item.strip() for mark, item in EXISTING_ITEM_RE.findall(text) if mark == "x"
    }

    if not criteria:
        return None

    lines = [f"- [{'x' if c in checked else ' '}] {c}" for c in criteria]
    return "\n## Acceptance Criteria\n" + "\n".join(lines) + "\n"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "goal.md"
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"{path} not found -- nothing to do")
        return

    section = build_section(text)
    body = SECTION_RE.sub("", text).rstrip("\n")

    if section is None:
        out = body + "\n"
        n = 0
    else:
        out = body + "\n" + section
        n = section.count("\n- [")

    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {path} ({n} acceptance criteria)")


if __name__ == "__main__":
    main()
