#!/usr/bin/env python3
"""
CLI to mutate a KB doc's frontmatter under ~/wiki/kb — the hit-tracking /
lifecycle fields, never the content body.

Usage:
  python3 kb.py search <word> [<word> ...]  # rank kb/ docs by OKF-field match
  python3 kb.py hit <doc.md>         # hit_count += 1, last_hit_at = today
  python3 kb.py deprecate <doc.md>   # move to ~/wiki/kb-deprecated, same
                                      # relative path (git mv if in a repo);
                                      # also appends a log.md entry
  python3 kb.py log <create|update> <doc.md>  # append a log.md entry
                                      # (deprecate logs itself, no separate
                                      # call needed)

`search` is what `@skills/grill-me` shells out to before asking a question —
it matches every OKF descriptive field (`type`, `title`, `description`,
`tags`), not tags alone, plus the doc's directory path (domain/category),
and prints `score\tpath` for every doc that scores > 0, highest first.

Schema (extended OKF — see lint_kb.py's docstring for the full spec):
  type, title, description, tags, timestamp, created_at, owner,
  last_hit_at, hit_count  (resource optional)

Only `@skills/to-kb` (after confirming a KB answer actually held up in a
finished session) and a human by hand should run `hit` — `@skills/grill-me`
only *reads* the KB live, it never writes to it.
"""
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

KB_ROOT = Path.home() / "wiki" / "kb"
DEPRECATED_ROOT = Path.home() / "wiki" / "kb-deprecated"
FRONTMATTER_RE_START = "---\n"
LOG_ACTIONS = ("create", "update", "deprecate")


def load(path):
    """Returns (meta dict, body str)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith(FRONTMATTER_RE_START):
        sys.exit(f"{path}: no YAML frontmatter (must start with '---')")
    end = text.find("\n---", len(FRONTMATTER_RE_START))
    if end == -1:
        sys.exit(f"{path}: unterminated frontmatter block")
    meta = yaml.safe_load(text[len(FRONTMATTER_RE_START):end]) or {}
    body = text[end + len("\n---"):].lstrip("\n")
    return meta, body


def dump(path, meta, body):
    front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{front}\n---\n\n{body}", encoding="utf-8")


def _searchable_text(meta, path):
    """OKF descriptive fields (type/title/description/tags) plus the
    domain/category path components — not tags alone."""
    tags = meta.get("tags") or []
    fields = [
        str(meta.get("type", "")),
        str(meta.get("title", "")),
        str(meta.get("description", "")),
        " ".join(str(t) for t in tags),
        " ".join(p for p in path.parent.parts),
    ]
    return " ".join(fields).lower()


def cmd_search(words):
    words = [w.lower() for w in words]
    scored = []
    for path in sorted(KB_ROOT.rglob("*.md")):
        if path.name in ("index.md", "log.md"):
            continue
        try:
            meta, _ = load(path)
        except SystemExit:
            continue
        text = _searchable_text(meta, path.relative_to(KB_ROOT))
        score = sum(text.count(w) for w in words)
        if score:
            scored.append((score, path))
    scored.sort(key=lambda sp: sp[0], reverse=True)
    for score, path in scored:
        print(f"{score}\t{path}")


LOG_LABELS = {"create": "Creation", "update": "Update", "deprecate": "Deprecation"}
LOG_HEADER = "# KB Update Log\n"


def cmd_log(action, path):
    """Append one entry to ~/wiki/kb/log.md, per references/okf/SPEC.md §9
    (repo root): a flat, date-grouped list, newest date heading first, entries newest-last
    within a day (append order)."""
    if action not in LOG_ACTIONS:
        sys.exit(f"log action must be one of {LOG_ACTIONS}, got {action!r}")
    try:
        rel = path.resolve().relative_to(KB_ROOT.resolve())
    except ValueError:
        rel = path
    title = rel.stem
    try:
        meta, _ = load(path)
        title = meta.get("title", title)
    except SystemExit:
        pass  # doc already moved/gone (e.g. deprecate after the git mv) — use filename

    entry = f"* **{LOG_LABELS[action]}**: [{title}](/{rel})\n"
    today_heading = f"## {date.today().isoformat()}\n"

    log_path = KB_ROOT / "log.md"
    lines = log_path.read_text(encoding="utf-8").splitlines(keepends=True) \
        if log_path.exists() else [LOG_HEADER, "\n"]

    first_heading = next((i for i, l in enumerate(lines) if l.startswith("## ")), len(lines))
    if first_heading < len(lines) and lines[first_heading] == today_heading:
        # today's section already exists — append the entry at its end,
        # right before the next date heading (or EOF)
        insert_at = first_heading + 1
        while insert_at < len(lines) and not lines[insert_at].startswith("## "):
            insert_at += 1
        lines.insert(insert_at, entry)
    else:
        lines[first_heading:first_heading] = [today_heading, entry, "\n"]

    log_path.write_text("".join(lines), encoding="utf-8")


def cmd_hit(path):
    meta, body = load(path)
    meta["hit_count"] = int(meta.get("hit_count", 0)) + 1
    meta["last_hit_at"] = date.today().isoformat()
    dump(path, meta, body)
    print(f"hit_count={meta['hit_count']} last_hit_at={meta['last_hit_at']}")


def cmd_deprecate(path):
    path = path.resolve()
    try:
        rel = path.relative_to(KB_ROOT.resolve())
    except ValueError:
        sys.exit(f"{path}: not under {KB_ROOT}, refusing to deprecate")
    target = DEPRECATED_ROOT / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd_log("deprecate", path)  # read title before the file moves away
    in_git = subprocess.run(
        ["git", "-C", str(path.parent), "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True,
    ).returncode == 0
    if in_git:
        subprocess.run(["git", "mv", str(path), str(target)], check=True)
    else:
        shutil.move(str(path), str(target))
    print(f"deprecated -> {target}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    action = sys.argv[1]
    if action == "search":
        if len(sys.argv) < 3:
            sys.exit(__doc__)
        cmd_search(sys.argv[2:])
        return
    if action == "log":
        if len(sys.argv) < 4:
            sys.exit(__doc__)
        cmd_log(sys.argv[2], Path(sys.argv[3]))
        return
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    arg = Path(sys.argv[2])
    if action == "hit":
        cmd_hit(arg)
    elif action == "deprecate":
        cmd_deprecate(arg)
    else:
        sys.exit(__doc__)


def self_test():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        doc = tmp / "doc.md"
        doc.write_text(
            "---\n"
            "type: Note\n"
            "title: Test\n"
            "description: A test doc\n"
            "tags: [test]\n"
            "timestamp: 2026-01-01T00:00:00+00:00\n"
            "created_at: 2026-01-01\n"
            "owner: '@dev'\n"
            "last_hit_at: 2026-01-01\n"
            "hit_count: 0\n"
            "---\n\nBody text.\n",
            encoding="utf-8",
        )

        global KB_ROOT, DEPRECATED_ROOT
        old_kb_for_search = KB_ROOT
        KB_ROOT = tmp
        try:
            import io
            import contextlib

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                cmd_search(["test"])
            assert "doc.md" in buf.getvalue(), buf.getvalue()

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                cmd_search(["nonexistentword"])
            assert buf.getvalue() == "", buf.getvalue()
        finally:
            KB_ROOT = old_kb_for_search

        cmd_hit(doc)
        meta, body = load(doc)
        assert meta["hit_count"] == 1, meta
        assert meta["last_hit_at"] == date.today().isoformat(), meta
        assert body.strip() == "Body text."

        cmd_hit(doc)
        meta, _ = load(doc)
        assert meta["hit_count"] == 2, meta

        old_kb, old_dep = KB_ROOT, DEPRECATED_ROOT
        KB_ROOT, DEPRECATED_ROOT = tmp, tmp / "deprecated"
        try:
            cmd_log("create", doc)
            cmd_log("update", doc)  # same day -> appended under the same heading
            log_text = (tmp / "log.md").read_text(encoding="utf-8")
            assert log_text.count(f"## {date.today().isoformat()}") == 1, log_text
            assert "**Creation**: [Test](/doc.md)" in log_text, log_text
            assert "**Update**: [Test](/doc.md)" in log_text, log_text
            assert log_text.index("**Creation**") < log_text.index("**Update**")

            cmd_deprecate(doc)
            assert (tmp / "deprecated" / "doc.md").exists()
            assert not doc.exists()
            log_text = (tmp / "log.md").read_text(encoding="utf-8")
            assert "**Deprecation**: [Test](/doc.md)" in log_text, log_text
        finally:
            KB_ROOT, DEPRECATED_ROOT = old_kb, old_dep

    print("self-test passed")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        self_test()
    else:
        main()
