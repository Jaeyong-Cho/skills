---
name: pair-work
description: Transparent pair-work wrapper — runs any skill's process while declaring intent before every move, asking approval before file writes or commands, and handling redirect/blame/why at any point. Use when user says "pair-work", "explain as you go", "step by step with me", or invokes as "/pair-work /<skill> <goal>".
---

# Pair-Work

Wrap any skill with transparent, human-in-the-loop execution. No silent moves.

## Invocation

```
/pair-work /<skill> <goal>
/pair-work /pf-impl build an auth module
/pair-work /pf-proto prove this state model
```

If invoked without a skill name, run **standalone mode** — see below.

## Standalone mode (no skill named)

1. **Get the goal** — user states what they want to achieve. If vague, ask one clarifying question first.
2. **Break it down** — decompose top-down into ordered steps. Show the list.
   ```
   Steps:
   1. <first logical unit>
   2. <next>
   ...
   ```
   Ask: "Does this order look right?" Adjust if needed.
3. **Work each step** — apply the protocol for every step: declare intent, ask approval before exec, show what changed after, check in before next.
4. **Done** — when all steps are complete, summarize what was achieved in 2–3 lines.

## Skill-wrap mode (skill name given)

Read the target skill's SKILL.md. Run its process exactly — but apply this protocol at every step.

## Protocol

**Before every action**, output one line:

```
> [ask]  what I'm asking — why
> [exec] what I'm about to do — why
> [plan] how I'm restructuring — why
> [check] what I'm verifying — why
```

**Each exec is one logical unit** — one behavior, one function, one config block. Max ~30 lines changed per edit. If a change would exceed this or touch multiple logical units, split it into separate steps first and show the split plan before proceeding.

**Before any file write or command**, ask approval:

> [exec] About to write `src/auth.ts` — implementing the login behavior from step 2

Use `AskUserQuestion`: options are "Proceed" (Recommended) and "Redirect".

**After each exec**, show a one-line summary of what changed (file, what was added/removed), then check in before continuing — unless user said "keep going".

## Human controls

| Say this | Effect |
|----------|--------|
| `redirect` | Stop. Restate what you want instead. I'll re-plan from here. |
| `blame` | Last action was wrong. I'll show the diff of what changed, then ask: roll back or fix forward? |
| `why` | I'll explain the current intent in full before continuing. |
| `keep going` | Disable per-step check-ins for the rest of the session. |
| `pause` | Re-enable check-ins after "keep going". |

## Rules

- No silent moves — intent declared before every action
- One question at a time — there is no maximum number of questions. Keep asking until the step or intent is fully clear. User can say "wrap up" to move forward at any point.
- Never skip a step without declaring why
- If the wrapped skill grills the user, follow its grill process — just prefix each question with `> [ask]`
