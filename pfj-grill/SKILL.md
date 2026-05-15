---
name: pfj-grill
description: |
  Grill the user about any concern, plan, or decision using today.md as context — then record the outcome in the journal.
  Use whenever the user wants to think something through, resolve a concern, make a decision, plan next steps, or get unstuck. The grilling surfaces the user's own reasoning and ends with a recorded conclusion.
  Triggers: "pfj-grill", "grill me about", "I want to think through", "help me decide", "I'm concerned about", "what should I do about", "I'm stuck on", "let's figure out", or any request to reason through a problem and record the result in the journal.
---

# pfj-grill

Think something through with the user. Grill until conclusion. Record in today.md.

## Step 1: Load context

Read `today.md` in full — the `## Goals` section shows today's plan, the journal shows what has happened.

Pull in other files (wiki, goals, weekly/monthly goal files) only as the conversation requires. Do not preload everything.

## Step 2: Grill

Ask questions one at a time. No maximum. For each question, provide your recommended answer so the user can react rather than invent from scratch.

Walk every branch until the concern is resolved, a plan is formed, or a decision is made. Keep going until there is nothing left to resolve.

If the user says "wrap up", skip remaining branches and move to Step 3.

## Step 3: Detect conclusion

When a natural conclusion appears — decision reached, plan formed, concern resolved — propose:

> "Think we've reached a conclusion. Record this in today.md?"

Wait for confirmation before writing anything.

## Step 4: Append to today.md

Append at the bottom of `today.md`:

```markdown
## HH:MM:SS (grill)

**Topic**: one-line description of what was discussed

Brief reasoning chain — key points that led to the outcome. Enough context for future-you to understand why, not a full transcript.

**Outcome**: decisions made / plan formed / concerns resolved / open questions remaining

**Steps**: (omit if no concrete steps surfaced)
1. Step one
2. Step two
   ```bash
   exact command here
   ```
```

Use 24h time. Keep it tight — this is a journal entry, not a report.

**Detail rule**: if the discussion produced specific commands, code snippets, config values, or ordered steps — write them verbatim under **Steps**. Do not summarize or paraphrase concrete technical details. A future reader must be able to execute without re-researching.

## Step 5: Update Goals (if tasks identified)

If the discussion produced concrete tasks, add them to the `## Goals` section at the top of `today.md`:

- Infer topic section and priority from context
- Ask the user if unclear
- Format: `- [ ] Task *(Priority)* *(ai: how AI helps)* — rationale *(→ Weekly: deliverable)*`
- Place in correct topic section at correct priority position

**Skills**: When filling `*(ai: ...)*`, consider which skill best fits the task. Check available skills:

```bash
ls ~/.claude/skills/
```

Reference the skill by name in the ai field — e.g. `*(ai: /pf-proto - protoryping and poc)*`, `*(ai: /pf-impl — implement ADR step by step)*`, `*(ai: /pf — write ADR for this design)*`, `*(ai: /pfj-grill — think through this concern)*`. If no skill fits, describe how AI helps instead.
