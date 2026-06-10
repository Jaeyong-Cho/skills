---
name: uncomfortable
description: Surface and resolve uncomfortable things. Reads ~/.strong/uncomfortable.md, reviews all items holistically, runs 5 Whys for each Inbox item, sets a goal for each considering relationships and existing goals, then saves. Use when user says "uncomfortable", "face uncomfortable", "what's bothering me", or "work through my uncomfortable list".
---

# Uncomfortable

Surface what's uncomfortable, find why, set a goal to face it.

## Data file

`~/.strong/uncomfortable.md` — structured markdown:

```
# Uncomfortable List

## <analyzed item title>
- Root cause: ...
- Goal: ...
- Notes: ... (optional)
- Status: done ✓ (optional)

## Inbox
- unanalyzed item 1
- unanalyzed item 2
```

H2 sections = analyzed items with root cause + goal. `## Inbox` = raw items not yet worked through.

If the file doesn't exist, create `~/.strong/` with an empty file containing just `# Uncomfortable List\n\n## Inbox\n`.

## Process

### 1. Show the list

Read `~/.strong/uncomfortable.md`. Display two groups numbered:

```
Inbox (not yet analyzed):
1. ...
2. ...

Already analyzed:
3. ...
4. ...
```

If both groups are empty, tell the user and stop — ask them to add items to Inbox first.

### 2. Holistic review

Before working any item, read all items together — both Inbox and existing H2 sections. Silently note:
- Items that share a root cause or could be resolved by the same goal
- Existing goals that might conflict with each other or worsen other items
- Patterns across items

Summarize what you noticed in 2–3 lines before proceeding.

### 3. Work each Inbox item

For every item in `## Inbox`, in order:

**a. Five Whys** — ask up to 5 rounds:
> "Why does [item / previous answer] make you uncomfortable?"

After each answer, judge: root cause reached, or deeper layer exists? Stop when root is clear. Summarize in one sentence.

**b. Set a goal** — propose one concrete, time-bound goal:
- Specific action (not "be better at X")
- Achievable in 2–4 weeks
- Directly targets the root cause
- **Explicitly check**: does this goal conflict with or relate to other items or existing goals? Mention it if so.

Ask the user: "Does this goal feel right?" — let them adjust wording.

**c. Extract notes** — without asking, synthesize key things from the conversation (constraints, patterns, prior context). 1–3 bullets max. Omit if nothing meaningful.

**d. Save** — promote the item from `## Inbox` to its own H2 section:
1. Remove its bullet from `## Inbox`
2. Add new H2 above `## Inbox`:
```
## [original item text]
- Root cause: [one sentence]
- Goal: [concrete goal]
- Notes: [synthesized — omit if empty]
```

### 4. Review existing goals

After all Inbox items are processed, show the existing H2 goals. Ask:
> "Do any of these goals need updating given what we just worked through?"

If yes — re-run goal-setting for that item and replace its sub-bullets in place.

## Rules

- Never skip the 5 Whys — if answers are shallow, push once more
- Goal must be specific and time-bound — reject vague goals like "work on this"
- When setting a goal, always consider the full list — goals must not inadvertently worsen other items
