---
name: to-wiki
description: Harvest tacit knowledge from the current session into .context/wiki/ — create, update, or remove entries. Use when the user says "save to wiki", "add to wiki", "remember this", "capture this", "update wiki", "remove from wiki", "delete wiki entry", or when a non-obvious insight worth preserving surfaces.
---

# To Wiki

Manage `.context/wiki/` entries.

**What to harvest** — tacit knowledge the codebase or docs can't show: constraints, domain facts, key decisions, patterns. Skip anything derivable from code, git history, or CLAUDE.md.

**One file per topic, each short.** Each distinct concept gets its own file. Do not mix unrelated knowledge into one file.

## Create / Update

For each piece of knowledge:
1. List `.context/wiki/` — if a file for this topic exists, update it rather than creating a duplicate.
2. If new: derive a kebab-case slug, write `.context/wiki/{slug}.md`.

Format:
```markdown
# {Topic}

{The knowledge — one focused concept.}
```

`mkdir -p .context/wiki` if needed.

## Remove / Update stale

After writing or updating entries, scan existing `.context/wiki/` files for entries that are now stale, contradicted, or superseded by the current session's findings. Update them to reflect the new truth, or delete them if the knowledge no longer applies.

## Compaction

```bash
ls .context/wiki/ | wc -l
```

If the count exceeds 20, run a compaction pass before adding new entries:
1. Read all files. Assign each a category.
2. Write or overwrite `.context/wiki/TOC.md` — a categorized table of contents listing every file with a one-line summary.
3. For each file: freshen the content — tighten wording, correct anything outdated, remove anything no longer true.
4. Delete files whose knowledge is entirely obsolete or incorrect with no salvageable content.

Completion criterion: every non-obvious insight is written or updated in its own focused file; stale or superseded entries updated or removed proactively; no file mixes unrelated concepts; TOC exists and is current when file count is high.
