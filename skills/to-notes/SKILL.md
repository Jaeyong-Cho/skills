---
name: to-notes
description: Maintain a Zettelkasten-style permanent-note wiki under ~/wiki/notes — atomic, own-words notes densely linked to each other, separate from the raw journal/research archive. Create/Read/Update/Delete. Invoke as /to-notes.
disable-model-invocation: true
---

# To-Notes

A link-organized store of permanent notes rooted at `~/wiki/notes/` — the "well-structured wiki," as opposed to `~/wiki/journal/`'s raw daily archive. Every note is written and linked by hand, one idea at a time. Starts flat; a directory only grows category sub-directories once it's outgrown flat browsing (Split, below) — links, not folders, are still what connects notes to each other.

**Threshold:** a directory splits once it holds more than 30 note files directly inside it. (ponytail: fixed number, no real usage data yet — raise/lower it if 30 turns out to be the wrong skimmability line.)

## Create

1. **Follow document style.** Read `../references/document-style/frontmatter.md` first — every note carries OKF frontmatter (`type: Permanent Note`).
2. **One note, one idea.** If what you're capturing covers more than one idea, split it into separate notes rather than one long note. Title it so it stands alone out of context — not "notes from Tuesday" but the idea itself, e.g. `event-sourcing-decouples-write-from-read.md`.
3. **Write it in your own words** — never a verbatim copy from a source or journal entry. Summarizing forces understanding; the note is what you concluded, not what you read.
4. **Find and link related notes before saving** — grep note frontmatter/titles under `~/wiki/notes/` (recursively, if already split) for overlapping tags or topics, or walk the `index.md` chain from `~/wiki/notes/index.md` down. Add a `## Links` section linking every related note (relative path, e.g. `[title](./other-slug.md)` or `[title](../other-category/other-slug.md)`), and add a reciprocal link back from each of those notes' own `## Links` section. A new note with zero links is a smell — the one exception is the very first note in the box.
5. **File it** — if its category (or the root) hasn't been split yet, write to `{dir}/{slug}.md`. If already split, place it in the most specific existing category it genuinely fits; don't invent a new category for one note.
6. **Update that directory's `index.md`** — add the new note as one line (link + one-line description), same catalog convention as every other `index.md` in this repo.
7. **Check the split threshold** on the directory just written into — if it now holds more than 30 note files directly, run **Split** below before finishing.

## Read

"What do I know about X": start at `~/wiki/notes/index.md`, walk into the narrowest matching category, follow links from there; grep frontmatter tags recursively for a keyword miss.

## Update

- **Correction** — edit a note in place for a fix to the same idea. New content that's actually a *different* idea gets its own new note (Create), linked in, not folded into an existing one.
- **Split** — when a directory exceeds the 30-file threshold: group its flat notes into MECE broad categories exactly like `@skills/categorize` (mutually exclusive, collectively exhaustive, catch-all capped at one). `mkdir` one sub-directory per category, move each note in (`git mv` if the wiki is a git repo, plain `mv` otherwise), write that category's own `index.md`, and replace the parent directory's flat note listing with one line per category linking to its `index.md` — broadest split at the top, narrower categories nested deeper. After moving, fix every relative link inside moved notes and in any note that linked to them (the relative path changed), and fix the parent's `index.md` entries. Recurse the same rule into any resulting category that itself now exceeds 30 files — split again, one level narrower (broad → detailed) — until every directory is under the threshold.
- **Fix** — rename a misnamed note (file + title), or re-point links after any of the above.

## Delete

Rare: only a genuine duplicate or wrong note. Merge its unique content into the surviving note first, then re-point every note that linked to the deleted one, and remove its line from the parent `index.md`.

Tell the user the note's path, which existing notes it linked to, and whether a split happened, when done.
