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

If the count exceeds 20, compact before adding new entries:
1. Read all files. Group by theme.
2. Merge files that cover the same concept into one — keep the best phrasing, discard the rest.
3. Delete files whose knowledge is no longer correct, no longer relevant, or already captured in a merged file.
4. Do not invent or expand content during compaction — only consolidate what exists.

Completion criterion: every non-obvious insight is written or updated in its own focused file; stale or superseded entries updated or removed proactively; no file mixes unrelated concepts; file count kept manageable.
