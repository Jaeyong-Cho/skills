---
name: pair-mode
description: Wrap any skill with transparent, human-in-the-loop execution — reads the target skill's process and runs it with intent declarations, small atomic changes, and post-edit confirmation via AskUserQuestion at every step. Use when user says "pair-mode", "pair-mode with", or invokes as "/pair-mode /<skill> <goal>".
---

# Pair-Mode

Wrap any skill with the pair-work protocol. No silent moves.

## Invocation

```
/pair-mode /<skill> <goal>
/pair-mode /pf-impl build an auth module
/pair-mode /pf-proto prove this state model
```

## Setup

Read the target skill's SKILL.md. Run its process exactly — but apply the protocol below at every step.

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

**Before starting a step's changes**, list ALL planned file changes (`> [plan] change 1, change 2, ...`). Group identical/parallel changes. Call `AskUserQuestion` to confirm the list before touching anything.

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
- If the wrapped skill grills the user, follow its grill process — prefix each question with `> [ask]`
