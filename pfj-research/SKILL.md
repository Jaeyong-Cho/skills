---
name: pfj-research
description: |
  Capture and sharpen research from an experiment, observation, or phenomenon — grills the user to extract what they observed and challenge their assumptions, then writes a markdown research note to the global journal.
  Use when the user ran an experiment, observed unexpected output, noticed a phenomenon, or has raw insights and thinking they want to crystallize. Triggers: "pfj-research", "I tried something", "I observed this", "research note", "capture this finding", "I have an insight", "I want to document this experiment".
---

Read `../pf/references/caveman.md` and apply caveman style throughout.
Check journal: `[ -n "$PFJ_PATH" ] && cat "$PFJ_PATH/today.md" 2>/dev/null`

# Research Notes

Grill to extract what user observed and challenge their reasoning. Write markdown research note.

## Step 1: Capture observation

Read user's description. Extract:
- **Experiment / context** — what was tried, what setup, what action
- **Observation** — what actually happened (output, behavior, phenomenon)
- **Initial thinking** — what user thinks it means, their hypothesis or concern

If any part is missing, ask once in plain text.

## Step 2: Grill — extract

Draw out full understanding before challenging. One question at a time, plain text or `AskUserQuestion`:
- What exactly did you observe? What were the inputs?
- What did you expect instead? Why?
- Have you seen this before, or is it new?
- What have you already ruled out?
- Which part are you most uncertain about?

User can say **"wrap up"** to skip to challenge phase.

## Step 3: Grill — challenge

Stress-test what emerged in Step 2. One question at a time:
- What assumptions are baked into that explanation?
- What else could cause this observation?
- What would falsify your interpretation?
- What's the simplest explanation you haven't considered?
- What would you need to see to be confident?

User can say **"wrap up"** to move to conclusions.

## Step 4: Write markdown note

Derive slug from experiment topic (lowercase, hyphens, max 40 chars).

Save: `$PFJ_PATH/research/YYYY/MM-DD-<slug>.md`

```bash
mkdir -p $PFJ_PATH/research/YYYY
```

Format:

```markdown
# <title>

Date: YYYY-MM-DD
Confidence: high / medium / low
Tags: #tag1 #tag2

## Observation

<what happened — inputs, context, action>

## Interpretation

<what it likely means>

## Key Findings

- <finding — with reasoning>

## Open Questions

- <what remains unresolved>

## Next Experiments

- <what to try next>
```

Print path:
```
Note: $PFJ_PATH/research/YYYY/MM-DD-<slug>.md
```

To generate HTML report from this note, run `/pfj-research-view`.
