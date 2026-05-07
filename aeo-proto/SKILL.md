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

Core rules — apply regardless of type:

- Mark the prototype clearly as temporary (comment at the top of every file)
- Place it near its context (e.g. `src/__proto__/` or alongside the relevant module)
- Single command to launch everything
- No persistence unless you're specifically testing persistence
- No tests, no abstractions, no polish
- Always surface the resulting state after each change so the user sees what happened

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

After writing the ADR, ask the user to confirm before any further implementation.
