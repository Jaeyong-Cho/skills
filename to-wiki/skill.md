---
name: to-wiki
description: Harvest tacit knowledge from the current session into source-of-truth/wiki/ — create, update, or remove entries. Use when the user says "save to wiki", "add to wiki", "remember this", "capture this", "update wiki", "remove from wiki", "delete wiki entry", or when a non-obvious insight worth preserving surfaces.
---

# To Wiki

Manage `source-of-truth/wiki/` entries.

**What to harvest** — tacit knowledge the codebase or docs can't show: constraints, domain facts, key decisions, patterns. Skip anything derivable from code, git history, or CLAUDE.md.

**One file per topic, each short.** Each distinct concept gets its own file. Do not mix unrelated knowledge into one file.

## Create / Update

For each piece of knowledge:
1. List `source-of-truth/wiki/` — if a file for this topic exists, update it rather than creating a duplicate.
2. If new: run `date +%Y%m%d-%H%M%S`, derive a kebab-case slug, write `source-of-truth/wiki/{timestamp}-{slug}.md`.

Format:
```markdown
# {Topic}

{The knowledge — one focused concept.}
```

`mkdir -p source-of-truth/wiki` if needed.

## Remove

Delete the file when the user asks to remove an entry.

Completion criterion: every non-obvious insight is written or updated in its own focused file; stale entries removed on request; no file mixes unrelated concepts.
