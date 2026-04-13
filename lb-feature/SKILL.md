---
name: lb-feature
description: |
  Use this skill when the user wants to add a new feature, capability, or topic to the literate book. Triggers: "add a new feature", "new feature request", "I want to add X to the program", "document this feature", "add a chapter about X", "extend the book with X". This is Workflow 1 of the literate programming development cycle. Use this skill before any code is written — the book is updated first, code follows after human review.
---

# lb-feature: Add a New Feature to the Book

**Goal**: Write the design of a new feature into the book. No code is written yet — the book is updated, flagged for review, and code tasks are queued as `IMPLEMENT` flags.

Read these references before writing:
- `references/writing.md` — topic-centric structure, narrative style, diagrams
- `references/flags.md` — DRAFT / IMPLEMENT / FIX semantics
- `references/source-refs.md` — source code reference format

---

## Steps

### 1. Read the existing book

```bash
cat book/src/SUMMARY.md
```

Read the chapters most relevant to the new feature. Understand the current design before adding to it.

### 2. Find the placement

Ask: does this feature belong in an existing chapter, or does it need a new one?

- **Existing chapter**: the feature is an extension of a concept already covered
- **New chapter**: the feature introduces a distinct concern the book doesn't cover yet
- **New sub-chapter**: the feature is deep enough to need its own page within an existing chapter

Name chapters after the **concept**, never after document type.  
`authentication/token-refresh.md` ✅  `requirements/token-refresh.md` ❌

If a new chapter is needed, explain the placement decision to the user before writing.

### 3. Write the book update

Write as a narrative — context → problem → solution → design → tradeoffs. See `references/writing.md`.

Every new or significantly changed section gets a `DRAFT` flag immediately after the section heading or at the end of the section:

```markdown
## Token Refresh

<!-- DRAFT: wrote initial design for token refresh — review expiry window and whether refresh tokens are needed -->

When a JWT is close to expiry...
```

Include:
- At least one Mermaid diagram per new chapter or major section
- Source code references for existing symbols (verify with grep first)
- `[not yet implemented]` for symbols that don't exist yet

### 4. Place IMPLEMENT flags for all code tasks

For every concrete implementation task that follows from the design, place an `IMPLEMENT` flag. Be precise — file path, function/class name, behavior.

```markdown
<!-- IMPLEMENT: src/services/AuthService.ts :: AuthService.refreshToken(token: string): Promise<string> — check token is within 1h of expiry; if valid, issue new JWT with reset expiry; if expired or invalid, throw UnauthorizedError -->
```

One flag per distinct unit of work. Do not bundle multiple functions into one flag.

### 5. Update SUMMARY.md

If new files were created, add them to `book/src/SUMMARY.md` in logical reading order.

### 6. Build check

```bash
cd book && mdbook build 2>&1 | tail -20
```

Fix all errors before reporting.

### 7. Report

Summarize:
- Which chapters were added or changed
- The key design decision made (and any open questions)
- How many `DRAFT` flags placed (awaiting review)
- How many `IMPLEMENT` flags placed (code tasks queued)
- What the user should review

---

## Output State

Book updated. All new/changed content marked `DRAFT`. All pending code tasks marked `IMPLEMENT`. **No source code written.**

The user reviews `DRAFT` sections and either:
- Approves → changes `DRAFT` to `IMPLEMENT` (or removes it)
- Requests changes → edits inline → AI revises with **lb-flags**
