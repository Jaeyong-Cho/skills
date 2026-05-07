---
name: aeo-proto
description: |
  Build a throwaway prototype to validate a design question, then capture the findings in an ADR.
  Use when the user wants to prototype before committing to an architecture — either for an existing ADR or a new idea.
  Triggers: "aeo-proto", "prototype this", "let's prototype", "explore this idea", "validate this design", "I want to try something before deciding".
---

# AEO Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

ADRs are stored at `.aeo/src/adr/<ID>-<slug>.md` (e.g. `adr-001` → `.aeo/src/adr/0001-*.md`).

---

## Step 1: Identify the question

Ask the user: **what specific question does this prototype need to answer?**

If an existing ADR is referenced, read it first — the question is usually an unresolved decision in the Decision or Alternatives Considered section.

If no ADR exists yet, the question comes from the user's request.

The question determines the prototype type:
- **Logic question** (state transitions, business rules, data shape) → read `references/proto-logic.md`
- **UI question** (layout, interaction, design direction) → read `references/proto-ui.md`

---

## Step 2: Build the prototype

Rules that apply to both branches:

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype close to where it will actually be used (next to the module or page it's prototyping for) — but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey the project's existing routing conventions; don't invent a new top-level structure.
2. **One command to run.** Whatever the project's existing task runner supports — `pnpm <name>`, `python <path>`, `bun <path>`, etc. The user must be able to start it without thinking.
3. **No persistence by default.** State lives in memory. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype runnable, no abstractions.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Delete or absorb when done.** When the prototype has answered its question, either delete it or fold the validated decision into the real code — don't leave it rotting in the repo.

---

## Step 3: Capture findings

Once the prototype answers its question, document what was learned:

- What the question was
- What the prototype revealed
- What was validated or invalidated
- Any decisions made (interfaces, data shapes, workflows)
- What is out of scope or deferred

---

## Step 4: Update or create the ADR

For ADR format and template, read `../aeo/references/adr.md`.

**If an existing ADR was referenced:**
- Add the prototype findings to the Decision section
- Update Alternatives Considered if any options were ruled out
- Update the Step-by-Step Plan if the prototype revealed a better approach
- Delete the prototype code

**If no ADR exists:**
- Create a new ADR using the template in `../aeo/references/adr.md`
- Use the prototype findings to fill in Context, Decision, and Step-by-Step Plan
- The prototype answers the grill-me questions — skip Step 1 of the ADR process
- Delete the prototype code

After writing the ADR, ask the user to confirm. Once confirmed, use the `aeo-impl` skill to implement with TDD.
