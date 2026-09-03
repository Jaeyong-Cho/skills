#!/usr/bin/env python3
"""
Lint ~/wiki/kb against the cache-inspired Google-OKF structural rules, and
report SLRU pruning candidates when capacity is breached.

Frontmatter schema (extended OKF — the six standard fields plus four
cache-lifecycle fields; `resource` optional, everything else required):

  type, title, description, tags, timestamp, created_at, owner,
  last_hit_at, hit_count

`timestamp` = last meaningfully edited (existing OKF meaning). `created_at`
is kept separate from it on purpose: the 30-day grace period below is
measured from creation, not last edit — collapsing the two would silently
break the grace rule for any doc edited after it was created.

Static rules (Warning / Error):
  file length         50-300 lines   > 300 / > 600
  directory depth      <= 3 levels   depth 4 / depth >= 5
  files per directory   5-15 files   > 15 / > 25
  total repo files    100-300 files  > 300 / > 500
  every directory carries an index.md (no frontmatter on it, not counted
  as a content file)

Cache eviction (SLRU): eviction logic only *reports* here — pruning is
`@skills/to-kb`'s job via `kb.py deprecate`, this script never moves files.
Runs only when total files > MAX_FILES_TOTAL or a directory's file count >
MAX_FILES_PER_DIRECTORY. Protected Segment (`created_at` within
NEW_DOC_GRACE_DAYS) is exempt; the rest is ranked by `last_hit_at`
ascending and the bottom PRUNING_PERCENTILE are flagged as candidates.

Usage:
  python3 lint_kb.py [kb_root]     # defaults to ~/wiki/kb
Exit code 1 if any ERROR-level violation is found, 0 otherwise (warnings
and pruning candidates are informational, not failures).
"""
import math
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

# Capacity limits (eviction trigger — matches the Warning thresholds above)
MAX_FILES_PER_DIRECTORY = 15
MAX_FILES_TOTAL = 300

# Cache policy parameters
PRUNING_PERCENTILE = 0.20
NEW_DOC_GRACE_DAYS = 30

MIN_LINES, WARN_LINES, ERROR_LINES = 50, 300, 600
WARN_DEPTH, ERROR_DEPTH = 4, 5
WARN_FILES_PER_DIR, ERROR_FILES_PER_DIR = 15, 25
WARN_FILES_TOTAL, ERROR_FILES_TOTAL = 300, 500

REQUIRED_FIELDS = [
    "type", "title", "description", "tags", "timestamp",
    "created_at", "owner", "last_hit_at", "hit_count",
]
RESERVED_NAMES = {"index.md", "log.md"}


def load_frontmatter(path):
    """Returns meta dict, or None (with an error string) if malformed."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "no YAML frontmatter (must start with '---')"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "unterminated frontmatter block"
    try:
        meta = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as e:
        return None, f"invalid YAML frontmatter: {e}"
    return meta, None


def content_files(kb_root):
    return [p for p in sorted(kb_root.rglob("*.md")) if p.name not in RESERVED_NAMES]


def lint(kb_root):
    """Returns (errors, warnings, pruning_candidates) — each a list of str."""
    errors, warnings = [], []
    files = content_files(kb_root)

    # Every directory that holds a content file (or a subdirectory) needs
    # its own index.md, kb_root included.
    dirs = {kb_root} | {p.parent for p in files}
    for d in sorted(dirs):
        if not (d / "index.md").exists():
            errors.append(f"{d}: missing index.md")

    per_dir = {}
    hit_meta = {}
    for f in files:
        rel = f.relative_to(kb_root)
        depth = len(rel.parts)
        if depth >= ERROR_DEPTH:
            errors.append(f"{f}: directory depth {depth}, must be < {ERROR_DEPTH}")
        elif depth >= WARN_DEPTH:
            warnings.append(f"{f}: directory depth {depth}, recommended <= 3")

        n_lines = len(f.read_text(encoding="utf-8").splitlines())
        if n_lines > ERROR_LINES:
            errors.append(f"{f}: {n_lines} lines, must be <= {ERROR_LINES}")
        elif n_lines > WARN_LINES:
            warnings.append(f"{f}: {n_lines} lines, recommended <= {WARN_LINES}")

        meta, err = load_frontmatter(f)
        if err:
            errors.append(f"{f}: {err}")
        else:
            missing = [k for k in REQUIRED_FIELDS if k not in meta]
            if missing:
                errors.append(f"{f}: frontmatter missing field(s): {', '.join(missing)}")
            else:
                hit_meta[f] = meta

        per_dir.setdefault(f.parent, []).append(f)

    for d, fs in sorted(per_dir.items()):
        n = len(fs)
        if n > ERROR_FILES_PER_DIR:
            errors.append(f"{d}: {n} files, must be <= {ERROR_FILES_PER_DIR}")
        elif n > WARN_FILES_PER_DIR:
            warnings.append(f"{d}: {n} files, recommended <= {WARN_FILES_PER_DIR}")

    total = len(files)
    if total > ERROR_FILES_TOTAL:
        errors.append(f"{kb_root}: {total} total files, must be <= {ERROR_FILES_TOTAL}")
    elif total > WARN_FILES_TOTAL:
        warnings.append(f"{kb_root}: {total} total files, recommended <= {WARN_FILES_TOTAL}")

    candidates = []
    breached = total > MAX_FILES_TOTAL or any(len(fs) > MAX_FILES_PER_DIRECTORY for fs in per_dir.values())
    if breached:
        today = date.today()
        probational = []
        for f, meta in hit_meta.items():
            created = _parse_date(meta.get("created_at"))
            if created and (today - created).days < NEW_DOC_GRACE_DAYS:
                continue
            last_hit = _parse_date(meta.get("last_hit_at")) or date.min
            probational.append((last_hit, f))
        probational.sort(key=lambda lh_f: lh_f[0])
        n_evict = math.ceil(len(probational) * PRUNING_PERCENTILE)
        candidates = [f for _, f in probational[:n_evict]]

    return errors, warnings, candidates


def _parse_date(value):
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def main():
    kb_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "wiki" / "kb"
    if not kb_root.is_dir():
        sys.exit(f"{kb_root}: not a directory")

    errors, warnings, candidates = lint(kb_root)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if candidates:
        print(f"\nPruning candidates (bottom {int(PRUNING_PERCENTILE * 100)}% by last_hit_at, capacity breached):")
        for f in candidates:
            print(f"  {f}")

    if errors:
        print(f"\nFAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    print(f"OK — {len(warnings)} warning(s)")
    sys.exit(0)


def self_test():
    import shutil
    import tempfile

    def doc(root, rel, lines=5, created_at="2020-01-01", last_hit_at="2020-01-01",
             missing_field=None):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = {
            "type": "Note", "title": rel, "description": "d", "tags": "[t]",
            "timestamp": "2020-01-01T00:00:00+00:00", "created_at": created_at,
            "owner": "'@dev'", "last_hit_at": last_hit_at, "hit_count": 0,
        }
        if missing_field:
            fields.pop(missing_field)
        front = "\n".join(f"{k}: {v}" for k, v in fields.items())
        body = "\n".join(f"line {i}" for i in range(lines))
        path.write_text(f"---\n{front}\n---\n\n{body}\n", encoding="utf-8")
        return path

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "index.md").write_text("# kb\n", encoding="utf-8")
        (root / "domain").mkdir()
        (root / "domain" / "index.md").write_text("# domain\n", encoding="utf-8")
        doc(root, "domain/good.md")

        errors, warnings, candidates = lint(root)
        assert errors == [], errors
        assert candidates == [], candidates

        # missing index.md in a directory that holds a file
        (root / "domain" / "cat").mkdir()
        doc(root, "domain/cat/no-index.md")
        errors, _, _ = lint(root)
        assert any("missing index.md" in e for e in errors), errors
        (root / "domain" / "cat" / "index.md").write_text("# cat\n", encoding="utf-8")

        # too deep: domain/category/sub/doc.md = depth 4 = warn; add one more = error
        (root / "domain" / "cat" / "sub" / "sub2").mkdir(parents=True)
        for d in ["domain/cat/sub/index.md", "domain/cat/sub/sub2/index.md"]:
            (root / d).write_text("# x\n", encoding="utf-8")
        doc(root, "domain/cat/sub/sub2/deep.md")
        errors, _, _ = lint(root)
        assert any("directory depth" in e for e in errors), errors
        shutil.rmtree(root / "domain" / "cat" / "sub")
        (root / "domain" / "cat" / "index.md").write_text("# cat\n", encoding="utf-8")

        # too long: error
        doc(root, "domain/cat/long.md", lines=700)
        errors, _, _ = lint(root)
        assert any("lines, must be" in e for e in errors), errors
        (root / "domain" / "cat" / "long.md").unlink()

        # missing required field
        doc(root, "domain/cat/bad.md", missing_field="owner")
        errors, _, _ = lint(root)
        assert any("missing field(s): owner" in e for e in errors), errors
        (root / "domain" / "cat" / "bad.md").unlink()

        # eviction: breach MAX_FILES_PER_DIRECTORY, oldest last_hit_at evicted first
        for i in range(MAX_FILES_PER_DIRECTORY + 1):
            doc(root, f"domain/cat/f{i}.md", last_hit_at=f"2020-01-{i + 1:02d}",
                created_at="2019-01-01")
        errors, warnings, candidates = lint(root)
        assert candidates, "expected pruning candidates once capacity is breached"
        assert candidates[0].name == "f0.md", [c.name for c in candidates]

        # grace period exempts a freshly created doc even with old last_hit_at
        doc(root, "domain/cat/f1.md", last_hit_at="2020-01-01", created_at=date.today().isoformat())
        _, _, candidates = lint(root)
        assert all(c.name != "f1.md" for c in candidates), [c.name for c in candidates]

    print("self-test passed")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        self_test()
    else:
        main()
