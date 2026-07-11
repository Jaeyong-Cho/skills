---
name: to-wiki
description: Harvest tacit knowledge from the current session into .context/wiki/ — create, update, or remove entries. Use when the user says "save to wiki", "add to wiki", "remember this", "capture this", "update wiki", "remove from wiki", "delete wiki entry", or when a non-obvious insight worth preserving surfaces.
---

# To Wiki

Manage `.context/wiki/` entries.

**What to harvest** — tacit knowledge the codebase or docs can't show: constraints, domain facts, key decisions, patterns. Skip anything derivable from code, git history, or CLAUDE.md.

**Never write personal or private information** — no names, credentials, personal data, private conversations, or anything that identifies an individual. Wiki entries must be purely technical or domain knowledge.

**One file per topic, each short.** Do not mix unrelated knowledge into one file.

## Create / Update

For each piece of knowledge:
1. List `.context/wiki/` (and category subdirectories if they exist) — if a file for this topic exists anywhere, update it rather than creating a duplicate.
2. Place the file in the right category directory. If no category fits, place it at the root for now.
3. If new: derive a kebab-case slug, write `.context/wiki/{category}/{slug}.md` (or `.context/wiki/{slug}.md` if uncategorized).

```bash
mkdir -p .context/wiki/{category}
```

Format:
```markdown
# {Topic}

{The knowledge — one focused concept.}
```

## Remove / Update stale

After writing or updating entries, scan existing files relevant to the current session's topic. Update entries that are now outdated, or delete them if the knowledge no longer applies.

## Compaction

Check after every write:

```bash
ls .context/wiki/ | wc -l
ls .context/wiki/{category}/ | wc -l   # for each existing category
```

**When any directory (root or category) exceeds 20 entries, compact it:**

1. Read all files in that directory.
2. **Categorize** — group files by theme. Move each into its category subdirectory. Create the subdirectory if needed.
3. **Combine common** — merge files that cover the same concept. Keep the best phrasing; discard the rest.
4. **Remove stale** — delete files whose knowledge is incorrect, obsolete, or already captured in a merged file.
5. **TOC** — write or overwrite a `TOC.md` in that directory listing every remaining file with a one-line summary.

**The same rule applies recursively to each category directory.** If a category grows past 20 files after compaction, apply the same five steps within it — sub-categorize, combine, remove, TOC.

Completion criterion: every non-obvious insight lives in its own focused file in the right category; stale entries removed; duplicates merged; any directory over 20 entries has a current TOC.
