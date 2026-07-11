---
name: to-wiki
description: Harvest tacit knowledge from the current session into .context/wiki/ — create, update, or remove entries. Use when the user says "save to wiki", "add to wiki", "remember this", "capture this", "update wiki", "remove from wiki", "delete wiki entry", or when a non-obvious insight worth preserving surfaces.
---

# To Wiki

Manage `.context/wiki/` entries.

**What to harvest** — tacit knowledge the codebase or docs can't show: constraints, domain facts, key decisions, patterns. Skip anything derivable from code, git history, or CLAUDE.md.

**Structure:** files live under category subdirectories — `.context/wiki/{category}/{slug}.md`. One file per topic, each short. Do not mix unrelated knowledge into one file.

## Create / Update

For each piece of knowledge:
1. Assign it a category (e.g. `architecture`, `decisions`, `constraints`, `patterns`, `ops`).
2. List `.context/wiki/{category}/` — if a file for this topic exists, update it rather than creating a duplicate.
3. If new: derive a kebab-case slug, write `.context/wiki/{category}/{slug}.md`.

```bash
mkdir -p .context/wiki/{category}
```

Format:
```markdown
# {Topic}

{The knowledge — one focused concept.}
```

## Remove / Update stale

After writing or updating entries, scan existing files in the relevant category for entries that are now stale, contradicted, or superseded. Update them to reflect the new truth, or delete them if the knowledge no longer applies.

## Compaction

Run a compaction pass when either condition is met:

```bash
ls .context/wiki/ | wc -l                        # total category count
ls .context/wiki/{category}/ | wc -l             # per-category file count
```

- **Total categories exceed 20:** reassign files across categories — merge categories that overlap, split ones that are too broad.
- **Any single category exceeds 20 files:** compact that category:
  1. Read all files in the category.
  2. Write or overwrite `.context/wiki/{category}/TOC.md` — a table of contents listing every file with a one-line summary.
  3. For each file: freshen the content — tighten wording, correct anything outdated, remove anything no longer true.
  4. Delete files whose knowledge is entirely obsolete or incorrect with no salvageable content.

Completion criterion: every non-obvious insight is written or updated in its own focused file under the right category; stale or superseded entries updated or removed proactively; no file mixes unrelated concepts; any category over 20 files has a current TOC.
