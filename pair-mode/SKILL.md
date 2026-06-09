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

**Each exec must be one logical unit** — one behavior, one function, one config block. Prefer small changes that are easy to read and understand at a glance. If a change is getting large, split it voluntarily.

**After each exec**, show the result and confirm understanding:

1. Show what changed (inline diff or code block)
2. Explain in one sentence what was done and why
3. **Call `AskUserQuestion` tool** — do not ask in plain text:
   - "Yes, continue" (Recommended)
   - "Redirect"
   - "Blame (roll back)"

Do not proceed to the next step until confirmed — unless user said "keep going".

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
- One question at a time — no maximum. Keep asking until clear. User can say "wrap up" to move forward.
- Never skip a step without declaring why
- If the wrapped skill grills the user, follow its grill process — prefix each question with `> [ask]`
