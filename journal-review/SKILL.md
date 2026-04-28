---
name: journal-review
description: |
  End-of-day review for a markdown knowledge base. Reads today.md, writes a report section (achievements + next-work plan), renames it to Journal/YYYY/MM-DD.md, creates a fresh today.md pre-filled with tomorrow's plan, extracts valuable knowledge to wiki/, updates SUMMARY.md, and suggests a git commit message. Use at the end of each work day for software development or research work.
  Triggers: "end of day", "daily review", "review today", "journal review", "wrap up today", "end of work", or any request to summarize today's journal and plan tomorrow.
---

# journal-review: End-of-Day Review

**Goal**: Turn `today.md` into a structured report, archive it as a dated journal entry, save reusable knowledge to the wiki, seed tomorrow's `today.md` with the next-work plan, and hand the user a ready-to-use commit message.

---

## Step 1: Find today's journal

Look for `today.md` in the repo root. If it doesn't exist, tell the user and stop — there is nothing to review.

Determine today's date for the archive path: `Journal/YYYY/MM-DD.md`.

---

## Step 2: Gather context

1. Read `today.md` in full.
2. Find and read the **N most recent** archived journal files (default N=5). Scan `Journal/` recursively, sort by filename (YYYY/MM-DD lexicographic order), take the N most recent. If the user specifies a different N (e.g., "look back 7 days"), use that instead.
3. Infer the key tags for today's work from the journal content (e.g., a day debugging Rust async → `#rust`, `#async`, `#debugging`). Then scan wiki files for those tags — read only the first few lines of each wiki file (title + tag line) to check for matches, and fully read only the files whose tags overlap. This keeps context lean while still surfacing relevant entries.

---

## Step 3: Write the Daily Report section

Append the following section **at the end of `today.md`**. Do not rewrite or modify anything above it.

```markdown
---

## Daily Report

### Achievements

<!-- What was actually completed or meaningfully progressed today? -->
<!-- Be concrete: "implemented X", "debugged Y", "read paper Z and understood W" -->

- ...

### Related Knowledge

<!-- Wiki entries whose tags overlap with today's topics — useful references for the work done or planned -->
<!-- Format: [title](../wiki/slug.md) — why it's relevant -->

- ...  *(none if no matches)*

### Knowledge Saved

<!-- Wiki entries created or updated in this session -->
<!-- Format: [title](../wiki/slug.md) — one-line summary -->

- ...  *(none if nothing was saved)*

### Next Work Plan

<!-- Detailed, actionable, prioritized. Infer from: unfinished items today, open questions mentioned, logical next steps in the project. -->
<!-- For research: include readings, experiments, or analysis tasks. -->
<!-- For software dev: include specific features, bugs, or refactors. -->

1. ...
2. ...
```

Fill each section with real content — don't leave placeholders. The plan should be specific enough that the user can start tomorrow without re-reading everything.

**For Related Knowledge**: infer the key topics/tags from today's journal (e.g., a day about Rust async maps to `#rust`, `#async`), then find wiki entries that carry any of those tags. Include only entries that are genuinely relevant — not every tag match, but the ones a reader would actually want to revisit given today's work.

If `today.md` already has a `## Daily Report` section (skill ran twice), overwrite only that section rather than appending a second one.

---

## Step 4: Extract and save wiki entries

Read the full journal (today + context days) and identify knowledge worth preserving for future use. Good candidates:

- A technique, pattern, or approach that solved a non-obvious problem
- A tool, library, or API insight that took real effort to figure out
- A design decision and the reasoning behind it
- A research finding, mental model, or concept that clarified something
- A recurring workflow or setup step worth referencing again
- An insight — an observation, hypothesis, or "aha" moment about a system, domain, or approach, even if not yet proven. Insights are valuable even when tentative; record them with their context and reasoning so they can be revisited later.

**Skip** things that are obvious, ephemeral, or already covered — check filenames and the tag-matched files you already read before creating a new entry.

For each piece of knowledge worth saving:

1. Choose a short slug: lowercase, hyphens, e.g., `rust-lifetime-covariance`, `attention-mechanism-intuition`
2. Create `wiki/<slug>.md`:

```markdown
# <Title>

#tag1 #tag2 #tag3

<Clear explanation of the concept, decision, or technique. Write for your future self — enough context to be useful without needing to re-read the original journal.>

## Details

<Supporting content: code snippets, diagrams, examples, links.>
<Use mermaid blocks for flows or architecture when it aids understanding.>

---
*First noted: YYYY-MM-DD*
```

Tag guidelines:
- Use specific, reusable tags: `#rust`, `#debugging`, `#ml`, `#architecture`, `#research`, `#devops`, `#insight`
- Use `#insight` for observations, hypotheses, and "aha" moments that may evolve over time
- 2–5 tags per entry is typical
- Prefer existing tags over inventing new ones (scan existing wiki files for established tags)

If a wiki entry for this topic already exists, **update it** rather than creating a duplicate — add new learnings under a new sub-section and update the date footer.

---

## Step 5: Archive today.md and seed tomorrow

1. Create the year directory if needed: `Journal/YYYY/`
2. Move (rename) `today.md` → `Journal/YYYY/MM-DD.md`
3. Create a fresh `today.md` in the repo root with only the next-work plan pre-filled:

```markdown
<!-- today: YYYY-MM-DD -->
<!-- Write freely below. No format required. -->

## Plan

<copy the Next Work Plan items from the archived report here>
```

The plan at the top of `today.md` gives a clear starting point for the next work session. The user can edit or ignore it — it's a prompt, not a constraint.

---

## Step 6: Update SUMMARY.md

Update `SUMMARY.md` so mdbook can render the new archived entry and any new wiki entries.

- Add the archived journal under the Journal section:
  ```markdown
  - [YYYY-MM-DD](Journal/YYYY/MM-DD.md)
  ```
- Add each new wiki entry under the Wiki section:
  ```markdown
  - [Title](wiki/slug.md)
  ```

Keep both sections sorted — journals by date descending, wiki alphabetically by title.

---

## Step 7: Show the commit message

Print a suggested git commit message. Do **not** run `git commit` — just show the message for the user to copy.

Format:
```
journal: YYYY-MM-DD — <one-line summary of today's main work>

- <wiki entry created/updated, if any>
- <wiki entry created/updated, if any>
```

Example:
```
journal: 2026-01-15 — implemented JWT auth and debugged token expiry edge case

- wiki/jwt-expiry-handling.md (new)
- wiki/rust-error-propagation.md (updated)
```

---

## Notes

- Never modify the original diary text — only append the report section.
- For research days with no code: the plan should reference papers, experiments, or analysis tasks.
- Mermaid diagrams in wiki entries are rendered by mdbook-mermaid. Use them when a visual adds real clarity (flows, state machines, architecture). Don't use them just to have a diagram.
- After a vacation (gap in journal dates), the skill still works — it just finds the last N archived entries as context regardless of how far back they are.
