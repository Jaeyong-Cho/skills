---
name: pfj-grill
description: |
  Grill the user about any concern, plan, or decision using today.md as context — ends with a rich standalone HTML report and a journal entry.
  No limit on questions. Use whenever the user wants to think something through, resolve a concern, make a decision, plan next steps, or get unstuck.
  Triggers: "pfj-grill", "grill me about", "I want to think through", "help me decide", "I'm concerned about", "what should I do about", "I'm stuck on", "let's figure out", "pfj-discuss", "discuss", "deep dive on", or any request to reason through a problem and record the result.
---

# pfj-grill

Grill user without limit using today.md as context. Generate rich standalone HTML report and append journal entry at end.

## Step 1: Load context

```bash
cat $PFJ_PATH/today.md
```

Extract discussion topic from user's args. If unclear, ask once. Pull wiki/goals only as conversation requires.

## Step 2: Grill — no limit

One question at a time with recommended answer. Use `AskUserQuestion` for discrete options (recommended first), plain text for open-ended, explore files instead of asking when possible.

Walk every branch of decision tree. Surface assumptions, risks, alternatives. Resolve dependencies before moving on.

Track: questions + answers, branches explored/skipped, conclusions, action items, tensions.

No maximum. Keep until every branch resolved. User can say **"wrap up"** to skip remaining branches.

## Step 3: Confirm report

When discussion ends, ask via `AskUserQuestion`: "Ready to generate the HTML report?"

## Step 4: Generate HTML report

See [REPORT.md](REPORT.md) for structure and styling spec.

Derive topic slug: lowercase, hyphens, max 40 chars. Save path: `$PFJ_PATH/discuss/YYYY/MM-DD-<topic-slug>.html`

`mkdir -p $PFJ_PATH/discuss/YYYY`

Write file, print path:
```
Report saved: /path/to/discuss/YYYY/MM-DD-topic-slug.html
```

## Step 5: Append to today.md

See [REFERENCE.md](REFERENCE.md#journal-entry-format) for format. Use 24h time. Keep tight — journal entry, not report. Write concrete commands/code/config verbatim under **Steps**; never paraphrase technical details.

## Step 6: Update Goals (if tasks identified)

If discussion produced concrete tasks, add to `## Goals` in today.md. See [REFERENCE.md](REFERENCE.md#goals-format) for format. Infer topic section and priority from context; ask if unclear.

Check available skills: `ls ~/.claude/skills/` — reference by name in `*(ai: ...)*` field.

If insights, observations, or unexpected findings surfaced during this session → suggest running `/pf-research` to record them.
