---
name: to-notes
description: Maintain a Zettelkasten-style note wiki under ~/wiki/notes — fleeting notes (raw capture, replaces to-context) and literature notes (source notes) get triaged into permanent notes (atomic, own-words, densely linked ideas). Create/Read/Update/Delete. Invoke as /to-notes.
disable-model-invocation: true
---

# To-Notes

A link-organized store of notes rooted at `~/wiki/notes/` — the "well-structured wiki," as opposed to `~/wiki/journal/`'s raw daily archive. Three note types, one flow: capture fast (fleeting/literature), then mine what's durable out of them into permanent notes — atomic, own-words, densely linked ideas, one at a time. This is now where session facts/state go too (`fleeting`, below) — `to-context` is retired. The steps below are self-sufficient day to day; open [`references/zettelkasten.md`](references/zettelkasten.md) only when a judgment call isn't covered by them (e.g. an edge case in what counts as one idea, or why a rule exists).

## Note types

- **Fleeting** (`~/wiki/notes/fleeting/{slug}.md`) — a raw thought, fact, or session detail, captured fast before it's lost. No polish, no mandatory links, no own-words rewrite — write it however it comes out, including "what was asked / what changed / what's next" for a session you want to resume later. Transient by design: triaged (Update → Triage) within a day or two, not left to pile up.
- **Literature** (`~/wiki/notes/literature/{slug}.md`) — notes on a specific source (doc, PR, article, conversation) as you go through it, in your own words, one note per source with `resource` set to that source's canonical URI. Kept indefinitely as your reading record, unlike fleeting notes.
- **Permanent** (`~/wiki/notes/permanent/{slug}.md`) — the actual slip-box: atomic, own-words, densely linked ideas. This is what you *get from* fleeting/literature notes (Promote, below), not usually what you write first.

**Threshold:** evaluated per directory, not per type or per tree — a directory splits once it holds more than 30 note files directly inside it, counting only that directory's own files (not sub-directories' files, not siblings, not a sum across `fleeting/`/`literature/`/`permanent/`). Each of those three, and every category nested under them, is checked independently against the same 30. (ponytail: fixed number, no real usage data yet.)

## Create

**Fleeting or literature** — lightweight, no atomicity or linking required:
1. Fleeting: write the thought/fact into `~/wiki/notes/fleeting/{slug}.md`, OKF frontmatter (`type: Fleeting Note`), content as-is.
2. Literature: one note per source at `~/wiki/notes/literature/{slug}.md`, frontmatter `type: Literature Note` with `resource: {source URI}`, paraphrased in your own words; append to the same note on repeat visits to that source rather than creating a new one.
3. Add a line to that type's `index.md`.

**Permanent** — same discipline as before:
1. Follow document style. Read `../references/document-style/frontmatter.md` first — `type: Permanent Note`.
2. One note, one idea — split into separate notes rather than one long note. Title it so it stands alone out of context.
3. Write it in your own words — never a verbatim copy. A note holds an idea/opinion/conclusion; a fact or session state is a fleeting note, not this.
4. Find and link related permanent notes before saving — grep frontmatter/titles under `~/wiki/notes/permanent/` (recursively, if split), or walk its `index.md` chain. Add a `## Links` section (relative paths), and a reciprocal link back from each linked note. A new note with zero links is a smell — except the very first note in the box.
5. File it under `~/wiki/notes/permanent/{dir}/{slug}.md` (most specific existing category if already split, else the root).
6. Update that directory's `index.md`.
7. Check the split threshold on the directory just written into — run **Split** below if it now exceeds 30.

## Promote — turn fleeting/literature into new ideas

The point of keeping fleeting/literature notes at all: on request (e.g. "process my notes," or as part of Triage) —
1. Read every unprocessed fleeting note, and any literature notes touched recently.
2. Look for patterns, connections, or contradictions — across those notes, and against existing permanent notes. Two unrelated notes juxtaposed can suggest a third idea neither stated outright; that's the payoff of this step, not just filing.
3. For each idea that's genuinely durable, write or update a permanent note for it (Create → Permanent rules apply in full).
4. Delete the fleeting note(s) it came from — its content now lives in the permanent note, nothing is lost. Leave literature notes in place even after a permanent note is drawn from them; they stay as source-anchored reference. A fleeting note that yields nothing durable still gets deleted once reviewed — that's Triage, not a failure.

## Read

"What do I know about X": start at `~/wiki/notes/permanent/index.md`, walk into the narrowest matching category, follow links from there; grep frontmatter tags recursively for a keyword miss. Check `literature/` if the answer should be source-anchored; check `fleeting/` only for something very recent that hasn't been promoted yet.

## Update

- **Correction** — edit a permanent note in place for a fix to the same idea. New content that's actually a *different* idea gets its own new note (Create), linked in.
- **Triage** — review fleeting notes older than a day or two: run Promote on whatever's still useful, delete the rest. Fleeting notes are not meant to accumulate.
- **Split** — when a directory exceeds the 30-file threshold: group its flat notes into MECE broad categories exactly like `@skills/categorize` (mutually exclusive, collectively exhaustive, catch-all capped at one). `mkdir` one sub-directory per category, move each note in (`git mv` if the wiki is a git repo, plain `mv` otherwise), write that category's own `index.md`, and replace the parent directory's flat listing with one line per category linking to its `index.md` — broadest split at the top, narrower categories nested deeper. Fix every relative link inside moved notes and in any note that linked to them, and fix the parent's `index.md` entries. Recurse into any resulting category that itself now exceeds 30 files, one level narrower each time, until every directory is under the threshold.
- **Fix** — rename a misnamed note (file + title), or re-point links after any of the above.

## Delete

- Fleeting: delete freely, no ceremony — that's the normal end state for most of them (via Triage).
- Literature/Permanent: rare — only a genuine duplicate or wrong note. Merge unique content into the surviving note first, re-point every note that linked to the deleted one, and remove its line from the parent `index.md`.

Tell the user the note's type and path, and — for a permanent note — what it linked to or whether a split happened, when done.
