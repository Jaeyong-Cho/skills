---
name: pair-work
description: Transparent step-by-step execution toward a goal — breaks the goal top-down, works each step with intent declarations, small changes, and post-edit confirmation via AskUserQuestion. Use when user says "pair-work", "work through this with me", "step by step", or "let's do this together".
---

# Pair-Work

Pursue a goal top-down with transparent, human-in-the-loop execution. No silent moves.

## Process

1. **Get the goal** — if vague, ask one clarifying question first.
2. **Break it down** — decompose top-down into ordered steps. Show the list.
   ```
   Steps:
   1. <first logical unit>
   2. <next>
   ...
   ```
   Call `AskUserQuestion`: "Does this order look right?" — options: "Yes, proceed" (Recommended), "Reorder", "Add/remove steps".
3. **Work each step** — for every step:
   - **Pre-flight**: list ALL file changes this step will make (`> [plan] change 1, change 2, ...`). Group identical/parallel changes. Call `AskUserQuestion` to confirm the list before touching anything.
   - For each change (or batch of identical changes):
     - Declare intent (`> [exec] ...`)
     - Execute the change
     - Explain in one sentence what was done and why
     - Call `AskUserQuestion` with a specific question about what was done
   - Do not proceed until confirmed — unless user said "keep going"
4. **Done** — summarize what was achieved in 2–3 lines.

## Protocol

**Before every action**, output one line:

```
> [ask]  what I'm asking — why
> [exec] what I'm about to do — why
> [plan] how I'm restructuring — why
> [check] what I'm verifying — why
```

**Every interaction is a dialogue** — not just exec confirms. For every `[ask]`, `[plan]`, `[check]`, and post-exec confirm:
- When options are clear: call `AskUserQuestion` tool — list options with recommended first marked "(Recommended)". Never ask in plain text when options exist.
- When open-ended (no clear options): ask in plain text.
- **Questions must be specific** — include the current intent in the question text. Options must reflect the actual decision, not generic labels. Bad: "Does this look right?" / "Yes, continue". Good: "I used a regex to validate date format and throw on mismatch — does this error strategy fit?" / "Yes, throw is right" / "Return null instead" / "Roll back".

**Each exec must be one logical unit** — one behavior, one function, one config block. Prefer small changes. If a change is getting large, split it voluntarily. Identical or parallel changes (same edit in multiple files) can be batched into one exec — declare them together and execute simultaneously. If an edit exceeds ~30–40 lines, split into logical chunks — confirm and review each chunk before moving to the next.

**Design decisions require confirmation** — before choosing a file name, directory structure, interface name, class name, public method signature, or any key design decision, ask via `AskUserQuestion`. One question per decision, grill-me style. Always include a recommended option marked "(Recommended)". Never silently pick a name, structure, or interface.

**After each exec**, call `AskUserQuestion` with a specific question about what was done — options reflect actual choices, not "yes/redirect/blame"

## Human controls

| Say this | Effect |
|----------|--------|
| `redirect` | Stop. Restate what you want instead. I'll re-plan from here. |
| `blame` | Last action was wrong. I'll show the diff, then ask: roll back or fix forward? |
| `why` | I'll explain the current intent in full before continuing. |
| `keep going` | Disable per-step check-ins for the rest of the session. |
| `pause` | Re-enable check-ins after "keep going". |

## Rules

- No silent moves — intent declared before every action
- One question at a time, no limit per step. Keep asking until the step is fully understood before moving on. User can say "wrap up" to move forward.
- Never skip a step without declaring why
