#!/usr/bin/env python3
"""
Lint an experiment write-up markdown report for writing-quality rules.

Same prose rules as to-paper's lint_paper.py (title word count, a
paragraph-count range that varies by section — see SECTION_PARAGRAPH_RANGES
there, e.g. introduction 3-5, background 4-8, methodology 2-4, results 2-4,
discussion 3-6, conclusion 1-3 — sentences per paragraph, words per
sentence) — reused
from that script rather than duplicated — applied to a plain markdown
report instead of a manifest.json. No diagram requirement: an experiment
report doesn't need a figure to be complete.

Expected shape:

    # {Title}

    ## Abstract
    {one paragraph}

    ## Introduction
    {paragraphs}

    ## Background
    {paragraphs}

    ## Methodology
    {paragraphs}

    ## Results
    {paragraphs}

    ## Discussion
    {paragraphs}

    ## Conclusion
    {paragraphs}

`##` headings may optionally carry a leading number ("## 1. Introduction"),
matched case-insensitively; each of the seven sections is required exactly
once and flat (no subsections).

Usage:
  python lint_report.py <report.md>

Exit code 0 if every check passes, 1 otherwise (one line per violation).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "to-paper" / "scripts"))
from lint_paper import (  # noqa: E402
    MAX_TITLE_WORDS,
    SECTION_PARAGRAPH_RANGES,
    check_prose_block,
    paragraphs,
    words,
)

SECTION_ORDER = ["introduction", "background", "methodology", "results", "discussion", "conclusion"]
HEADING_RE = re.compile(r"^##\s+(?:\d+\.\s+)?(.+?)\s*$")


def parse_report(text):
    """Returns (title, {section_name_lower: body_text})."""
    lines = text.splitlines()
    title = None
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            break

    sections = {}
    current_key = None
    current_lines = []
    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            if current_key is not None:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = m.group(1).strip().lower()
            current_lines = []
        elif current_key is not None:
            current_lines.append(line)
    if current_key is not None:
        sections[current_key] = "\n".join(current_lines).strip()
    return title, sections


def lint(text):
    errors = []
    title, sections = parse_report(text)

    if title is None:
        errors.append("missing '# Title' heading")
    else:
        title_words = words(title)
        if len(title_words) >= MAX_TITLE_WORDS:
            errors.append(f"title: {len(title_words)} words, must be fewer than {MAX_TITLE_WORDS}")

    required = ["abstract", *SECTION_ORDER]
    missing = [k for k in required if k not in sections]
    if missing:
        errors.append(f"report missing required section(s): {', '.join('## ' + m.title() for m in missing)}")
        return errors

    check_prose_block("abstract", paragraphs(sections["abstract"]), errors, one_paragraph=True)
    for key in SECTION_ORDER:
        check_prose_block(key, paragraphs(sections[key]), errors, paragraph_range=SECTION_PARAGRAPH_RANGES[key])
    return errors


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    errors = lint(path.read_text(encoding="utf-8"))
    for e in errors:
        print(e)
    if errors:
        print(f"FAIL — {len(errors)} violation(s)")
        sys.exit(1)
    print("OK")
    sys.exit(0)


def self_test():
    three_sentences = " ".join(f"This is sentence number {i}." for i in range(3))

    def block(n_paragraphs):
        return "\n\n".join(three_sentences for _ in range(n_paragraphs))

    good_report = (
        "# A Short Report Title\n\n"
        f"## Abstract\n{three_sentences}\n\n"
        f"## 1. Introduction\n{block(3)}\n\n"
        f"## 2. Background\n{block(4)}\n\n"
        f"## 3. Methodology\n{block(3)}\n\n"
        f"## 4. Results\n{block(3)}\n\n"
        f"## 5. Discussion\n{block(3)}\n\n"
        f"## 6. Conclusion\n{block(2)}\n"
    )
    errors = lint(good_report)
    assert not errors, f"good report should lint clean, got: {errors}"

    title, sections = parse_report(good_report)
    assert title == "A Short Report Title"
    assert set(sections) == {
        "abstract", "introduction", "background", "methodology", "results", "discussion", "conclusion",
    }
    assert sections["introduction"] == block(3)

    no_title = good_report.split("\n\n", 1)[1]
    errors = lint(no_title)
    assert any("missing '# Title'" in e for e in errors), "\n".join(errors)

    missing_section = good_report.replace(f"## 6. Conclusion\n{block(2)}\n", "")
    errors = lint(missing_section)
    assert any("conclusion" in e.lower() and "missing" in e.lower() for e in errors), "\n".join(errors)

    bad_report = good_report.replace(
        f"## Abstract\n{three_sentences}", f"## Abstract\n{block(2)}"
    ).replace(
        f"## 1. Introduction\n{block(3)}", f"## 1. Introduction\n{block(1)}"
    )
    errors = lint(bad_report)
    joined = "\n".join(errors)
    assert any("abstract" in e and "one paragraph" in e for e in errors), joined
    assert any("introduction" in e for e in errors), joined

    print("self-test passed")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        self_test()
    else:
        main()
