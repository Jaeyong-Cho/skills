---
name: journal-review
description: |
  End-of-day review for a markdown knowledge base. Reads today's journal, writes a report section (achievements + next-work plan), extracts valuable knowledge to wiki/, updates SUMMARY.md, and suggests a git commit message. Use at the end of each work day for software development or research work.
  Triggers: "end of day", "daily review", "review today", "journal review", "wrap up today", "end of work", "도 review", or any request to summarize today's journal and plan tomorrow.
---

# journal-review: End-of-Day Review

**Goal**: Turn today's freeform diary into a structured report, save reusable knowledge to the wiki, and hand the user a ready-to-use commit message.

---

## Step 1: Find today's journal

Determine today's date and locate `Journal/YYYY/MM-DD.md`. If the file doesn't exist, tell the user and stop — there is nothing to review.

---

## Step 2: Gather context

1. Read today's journal entry in full.
2. Find and read the **N most recent** previous journal files (default N=5). Scan `Journal/` recursively, sort by filename (YYYY/MM-DD lexicographic order), take the N entries before today. If the user specifies a different N in their message (e.g., "look back 7 days"), use that instead.
3. Read all existing wiki files in `wiki/` — just their filenames and first few lines — to avoid creating duplicate entries.

---

## Step 3: Write the Daily Report section

Append the following section **at the end of today's journal file**. Do not rewrite or modify anything above it.

```markdown
---

## Daily Report

### Achievements

<!-- What was actually completed or meaningfully progressed today? -->
<!-- Be concrete: "implemented X", "debugged Y", "read paper Z and understood W" -->

- ...

### Knowledge Saved

<!-- List any wiki entries created or updated in this session -->
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

---

## Step 4: Extract and save wiki entries

Read the full journal (today + context days) and identify knowledge worth preserving for future use. Good candidates:

- A technique, pattern, or approach that solved a non-obvious problem
- A tool, library, or API insight that took real effort to figure out
- A design decision and the reasoning behind it
- A research finding, mental model, or concept that clarified something
- A recurring workflow or setup step worth referencing again

**Skip** things that are obvious, ephemeral, or already well-documented in the wiki.

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
- Use specific, reusable tags: `#rust`, `#debugging`, `#ml`, `#architecture`, `#research`, `#devops`
- 2–5 tags per entry is typical
- Prefer existing tags over inventing new ones (scan existing wiki files for established tags)

If a wiki entry for this topic already exists, **update it** rather than creating a duplicate — add new learnings under a new sub-section and update the date footer.

---

## Step 5: Update SUMMARY.md

After creating or updating wiki entries, update `SUMMARY.md` so mdbook can render them.

- Add today's journal under the Journal section if not already listed:
  ```markdown
  - [YYYY-MM-DD](Journal/YYYY/MM-DD.md)
  ```
- Add each new wiki entry under the Wiki section:
  ```markdown
  - [Title](wiki/slug.md)
  ```

Keep both sections sorted — journals by date descending, wiki alphabetically by title.

---

## Step 6: Show the commit message

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

- The report section is the only thing appended to the journal — never modify the original diary text.
- If today's journal already has a `## Daily Report` section (ran twice by mistake), overwrite only that section rather than appending a second one.
- For research days with no code: the plan should reference papers, experiments, or analysis tasks — not code tasks.
- Mermaid diagrams in wiki entries are rendered by mdbook-mermaid. Use them when a visual adds real clarity (flows, state machines, architecture). Don't use them just to have a diagram.
