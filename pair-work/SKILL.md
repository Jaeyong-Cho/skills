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

**Each exec must be one logical unit** — one behavior, one function, one config block. Prefer small changes that are easy to read and understand at a glance. If a change is getting large, split it voluntarily — smaller is easier to review, easier to roll back, easier to learn from.

**After each exec**, show the result and confirm understanding:

1. Show what changed (inline diff or code block)
2. Explain in one sentence what was done and why
3. Ask via `AskUserQuestion`: "Does this look right?" — options: "Yes, continue" (Recommended), "Redirect", "Blame (roll back)"

Do not proceed to the next step until confirmed — unless user said "keep going".

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
