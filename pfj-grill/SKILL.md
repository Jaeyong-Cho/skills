---
name: pfj-grill
description: |
  Grill the user about any concern, plan, or decision using today.md as context — ends with a rich standalone HTML report and a journal entry.
  No limit on questions. Use whenever the user wants to think something through, resolve a concern, make a decision, plan next steps, or get unstuck.
  Triggers: "pfj-grill", "grill me about", "I want to think through", "help me decide", "I'm concerned about", "what should I do about", "I'm stuck on", "let's figure out", "pfj-discuss", "discuss", "deep dive on", or any request to reason through a problem and record the result.
---

# pfj-grill

Grill the user without limit using today.md as context. Generate a rich standalone HTML report and append a journal entry at the end.

## Step 1: Load context

```bash
cat $PFJ_PATH/today.md
```

Extract the discussion topic from the user's args. If unclear, ask once before proceeding.

Pull additional files (wiki, goals) only as the conversation requires.

## Step 2: Grill — no limit

Ask questions one at a time. For each question, provide your recommended answer so the user can react rather than invent from scratch.

- When a question has clear discrete options → use `AskUserQuestion`, recommended option first marked "(Recommended)"
- When a question is open-ended with no clear options → ask in plain text
- When a question can be answered by exploring the codebase or files → explore instead of asking

Walk every branch of the decision tree. Surface assumptions, risks, and alternatives. Resolve dependencies between decisions before moving on.

Track internally as you go:
- Every question and the user's answer
- Branches explored vs. explicitly skipped
- Conclusions reached at each branch
- Action items that surface
- Key tensions or trade-offs named

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some topics need three questions, some need fifty. The user can stop at any time or say **"wrap up"** to skip remaining branches and move on.

## Step 3: Confirm report

When the discussion reaches a natural end, ask via `AskUserQuestion`:
> "Ready to generate the HTML report?"

Wait for confirmation.

## Step 4: Generate the HTML report

See [REPORT.md](REPORT.md) for structure and styling spec.

Derive the topic slug: lowercase, hyphens, max 40 chars (e.g. `api-auth-strategy`).
Compute the save path:
```
$PFJ_PATH/discuss/YYYY/MM-DD-<topic-slug>.html
```

Create parent directories if needed:
```bash
mkdir -p $PFJ_PATH/discuss/YYYY
```

Write the file, then print the path so the user can open it:
```
Report saved: /path/to/discuss/YYYY/MM-DD-topic-slug.html
```

## Step 5: Continue into a skill (if outcome warrants it)

If the discussion concluded with a clear next action, offer to run the matching skill immediately via `AskUserQuestion`:

| Outcome | Skill to offer |
|---------|---------------|
| Need to write an ADR | `/pf` |
| Need to prototype before deciding | `/pf-proto` |
| ADR exists, ready to implement | `/pf-impl` |

Ask: *"Continue into [skill name] now?"* — if yes, invoke the skill via the `Skill` tool and pass the discussion conclusions as context.

Skip this step if no skill clearly maps to the outcome.

## Step 6: Append to today.md

```markdown
## HH:MM:SS (grill)

**Topic**: one-line description of what was discussed

**Outcome**: key decisions / conclusions reached

**Steps**: (omit if no concrete steps surfaced)
1. Step one
2. Step two
   ```bash
   exact command here
   ```

**Report**: $PFJ_PATH/discuss/YYYY/MM-DD-topic-slug.html
```

Use 24h time. Keep it tight — this is a journal entry, not a report.

**Detail rule**: if the discussion produced specific commands, code snippets, config values, or ordered steps — write them verbatim under **Steps**. Do not summarize or paraphrase concrete technical details.

## Step 7: Update Goals (if tasks identified)

If the discussion produced concrete tasks, add them to the `## Goals` section at the top of `today.md`:

- Infer topic section and priority from context
- Ask the user if unclear
- Format: `- [ ] Task *(Priority)* *(ai: how AI helps)* — rationale *(→ Weekly: deliverable)*`
- Place in correct topic section at correct priority position

**Skills**: When filling `*(ai: ...)*`, check available skills:

```bash
ls ~/.claude/skills/
```

Reference the skill by name in the ai field — e.g. `*(ai: /pf-proto — prototyping and poc)*`, `*(ai: /pf-impl — implement ADR step by step)*`, `*(ai: /pf — write ADR for this design)*`. If no skill fits, describe how AI helps instead.
