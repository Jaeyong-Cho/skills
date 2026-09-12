#!/usr/bin/env python3
"""Validate the structure and minimum content of a .bible directory."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

SECTION_RE = re.compile(r"^##\s+(WHY|WHAT|SCOPE|AUDIT|VERIFICATION|EVIDENCE)\s*$", re.I)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$")
LAW_ID_RE = re.compile(r"^#\s+(LAW-[A-Z0-9][A-Z0-9-]*)\b", re.I)
LINK_RE = re.compile(r"!?(?:\[[^]]*\])\(([^)]+)\)")


def error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path}: {message}")


def check_index_links(path: Path, errors: list[str]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        error(errors, path, f"cannot read index.md: {exc}")
        return

    for target in LINK_RE.findall(text):
        target = target.strip().split()[0]
        if target.startswith(("#", "/", "http:", "https:", "mailto:")):
            continue
        destination = (path.parent / target.split("#", 1)[0]).resolve()
        if not destination.exists():
            error(errors, path, f"broken relative link: {target}")


def check_law(path: Path, law_ids: dict[str, Path], errors: list[str]) -> None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        error(errors, path, f"cannot read Law: {exc}")
        return

    titles = [match.group(1) for line in lines if (match := TITLE_RE.match(line))]
    if len(titles) != 1:
        error(errors, path, f"Law needs exactly one top-level title, found {len(titles)}")
    elif not titles[0].strip():
        error(errors, path, "Law title is empty")

    section_positions: list[tuple[str, int]] = []
    for index, line in enumerate(lines):
        if match := SECTION_RE.match(line):
            section_positions.append((match.group(1).upper(), index))
    sections: dict[str, int] = {}
    for key, _ in section_positions:
        sections[key] = sections.get(key, 0) + 1
    for required in ("WHY", "WHAT"):
        if sections.get(required, 0) != 1:
            error(errors, path, f"Law needs exactly one ## {required} section")
        else:
            start = next(index for key, index in section_positions if key == required)
            end = next((index for _, index in section_positions if index > start), len(lines))
            if not "\\n".join(lines[start + 1 : end]).strip():
                error(errors, path, f"## {required} section must not be empty")

    law_id = next((match.group(1).upper() for line in lines if (match := LAW_ID_RE.match(line))), None)
    if law_id:
        previous = law_ids.get(law_id)
        if previous:
            error(errors, path, f"duplicate Law identifier {law_id}; also used by {previous}")
        else:
            law_ids[law_id] = path


def check_level(path: Path, kind: str, errors: list[str]) -> None:
    """Check category/subcategory/artifact depth below laws/ or tools/."""
    if not path.is_dir():
        error(errors, path, f"{kind}/ must be a directory")
        return

    for category in path.iterdir():
        if category.name == "index.md":
            continue
        if not category.is_dir() or category.is_symlink():
            error(errors, category, f"unexpected entry; {kind}/ needs category directories")
            continue
        for subcategory in category.iterdir():
            if subcategory.name == "index.md":
                continue
            if not subcategory.is_dir() or subcategory.is_symlink():
                error(errors, subcategory, "unexpected entry; category needs subcategory directories")
                continue
            for artifact in subcategory.iterdir():
                if artifact.name == "index.md":
                    continue
                if artifact.is_dir() or artifact.is_symlink():
                    error(errors, artifact, "taxonomy is limited to category/subcategory; nested directories are not allowed")
                    continue
                if kind == "laws":
                    if artifact.suffix.lower() != ".md":
                        error(errors, artifact, "Law files must use the .md extension")
                elif not artifact.stat().st_mode & 0o111:
                    error(errors, artifact, "tools must be executable")


def lint(root: Path, parents: list[Path] | None = None) -> list[str]:
    root = root.expanduser().resolve()
    errors: list[str] = []
    law_ids: dict[str, Path] = {}
    roots = [root, *[parent.expanduser().resolve() for parent in (parents or [])]]

    for bible in roots:
        if bible.name != ".bible":
            error(errors, bible, "Bible root must be named .bible")
        if not bible.is_dir():
            error(errors, bible, "Bible root does not exist or is not a directory")
            continue

        required_dirs = ("laws", "tools")
        allowed = {"index.md", *required_dirs}
        for entry in bible.iterdir():
            if entry.name not in allowed:
                error(errors, entry, "only index.md, laws/, and tools/ are allowed at Bible root")
        for name in required_dirs:
            if not (bible / name).is_dir():
                error(errors, bible / name, f"missing {name}/ directory")

        for directory in [bible, *[p for p in bible.rglob("*") if p.is_dir()]]:
            if not (directory / "index.md").is_file():
                error(errors, directory, "every Bible directory needs index.md")
        for index in bible.rglob("index.md"):
            if index.is_file():
                check_index_links(index, errors)

        check_level(bible / "laws", "laws", errors)
        check_level(bible / "tools", "tools", errors)
        for law in (bible / "laws").glob("*/*/*.md"):
            if law.name != "index.md":
                check_law(law, law_ids, errors)

    if len(roots) != len({str(path) for path in roots}):
        error(errors, root, "Bible parent chain contains a duplicate root")
    return errors


def self_test() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory) / ".bible"
        for path in (
            root / "laws/architecture",
            root / "laws/architecture/dependency",
            root / "tools/static",
            root / "tools/static/dependency",
        ):
            path.mkdir(parents=True)
            (path / "index.md").write_text("# Index\n", encoding="utf-8")
        (root / "index.md").write_text("# Bible\n", encoding="utf-8")
        (root / "laws/index.md").write_text("# Laws\n", encoding="utf-8")
        (root / "tools/index.md").write_text("# Tools\n", encoding="utf-8")
        law = root / "laws/architecture/dependency/example.md"
        law.write_text("# LAW-EXAMPLE-001 — Example\n\n## WHY\nreason\n\n## WHAT\nrule\n", encoding="utf-8")
        tool = root / "tools/static/dependency/check"
        tool.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        tool.chmod(0o755)
        assert lint(root) == []

        (root / "laws/architecture/dependency/bad.md").write_text("# Bad\n\n## WHAT\nrule\n", encoding="utf-8")
        errors = lint(root)
        assert any("bad.md" in item and "WHY" in item for item in errors), errors

        (root / "laws/architecture/dependency/deeper").mkdir()
        errors = lint(root)
        assert any("nested directories" in item for item in errors), errors
    print("self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bible", nargs="?", type=Path, default=Path(".bible"))
    parser.add_argument("--parent", action="append", type=Path, default=[], help="parent .bible root; repeat for the full chain")
    parser.add_argument("--test", action="store_true", help="run the built-in self-test")
    args = parser.parse_args()
    if args.test:
        self_test()
        return 0

    errors = lint(args.bible, args.parent)
    if errors:
        for item in errors:
            print(f"FAIL: {item}", file=sys.stderr)
        print(f"FAIL — {len(errors)} violation(s)", file=sys.stderr)
        return 1
    print(f"OK — {args.bible} is a valid Bible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
