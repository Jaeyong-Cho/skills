---
name: pfj-review
description: |
  End-of-day review for the POFE knowledge base. Reads today.md, extracts wiki and experience entries worth keeping, and recommends what to work on next. The human writes their own todo list.
  Triggers: "end of day", "daily review", "review today", "pfj review", "wrap up today", "end of work", or any request to summarize today's journal.
---

# pfj-review: End-of-Day Review

Read today's journal, extract knowledge worth keeping, and surface recommendations — the human decides what to do with them.

---

## Source of Truth

Human-written journal text is always correct. Labeled sections (`## HH:MM:SS (skill-name)`) are AI-generated summaries — accurate but not ground truth.

- **Human-written**: `## HH:MM:SS` with no label, or freeform text below `<!-- Write freely below -->` — treat as ground truth.
- **AI-written**: `## HH:MM:SS (label)` — trust for facts and outcomes, not for personal voice or reflection.

---

## Step 1: Load today's files

1. Find `today.md`. If missing, stop and tell the user.
2. Read the full journal.
3. Load N most recent archived journals from `Journal/` for context (default N=3).

---

## Step 2: Load related wiki entries

Infer key topics from today's journal. Scan the first 3 lines of each file in `wiki/` to find the tag line. Fully read only the files whose tags overlap with today's topics.

---

## Step 3: Extract and save wiki entries

Identify technical knowledge worth preserving — good candidates:

- A technique, pattern, or approach that solved a non-obvious problem
- A tool, library, or API insight that took real effort to figure out
- A design decision and the reasoning behind it
- A research finding, mental model, or concept that clarified something
- A recurring workflow or setup step worth referencing again

Skip obvious or ephemeral things. Update existing entries rather than creating duplicates.

**Wiki entry format** (`wiki/<slug>.md`):
```markdown
# Title

#tag1 #tag2 #tag3

Clear explanation for your future self.

## Details

Code snippets, diagrams, examples.

---
*First noted: YYYY-MM-DD*
```

If a loaded wiki entry conflicts with the journal, correct the wiki entry and note `*Updated: YYYY-MM-DD — reason*`.

---

## Step 4: Extract and save experience entries

Scan for personal and professional experience worth keeping — how you work, not what you know:

- A work habit or approach that made a noticeable difference
- A decision pattern — what led to a good or bad call
- A mistake with the root cause understood
- A mental shift — a belief or assumption that changed

**Experience entry format** (`reflections/<slug>.md`):
```markdown
# Title

#tag1 #tag2 #tag3

What happened and what you learned from it.

## Context

The situation that revealed this.

## What to apply

One or two sentences on how to act on this going forward.

---
*First noted: YYYY-MM-DD*
```

Before creating a new entry, scan `reflections/` for an existing match — append a dated sub-section rather than duplicating.

---

## Step 5: Update SUMMARY.md

Add new wiki entries under Wiki (alphabetically) and new reflection entries under Reflections (alphabetically). Create the Reflections section if it doesn't exist yet.

---

## Step 6: Recommend next tasks

Based on what was done today, what's incomplete, and what open questions remain — output a short recommended plan. Do not write it anywhere. The human will write their own todo list.

Format:
```
## Recommended next
- <task> — <why: what it unblocks or advances>
- <task> — <why>
```

Keep it short. Surface the highest-value next steps only.

---

## Step 7: Show the commit message

Do **not** commit — just show:

```
pfj: YYYY-MM-DD — <one-line summary of today's main work>

- wiki/slug.md (new/updated)
- reflections/slug.md (new/updated)
```
