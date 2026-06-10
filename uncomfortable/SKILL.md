---
name: uncomfortable
description: Surface and resolve uncomfortable things. Reads ~/.strong/uncomfortable.md, interviews the user to pick the most uncomfortable item, runs 5 Whys to find the root cause, then sets a concrete goal and appends it back to the file. Use when user says "uncomfortable", "face uncomfortable", "what's bothering me", or "work through my uncomfortable list".
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

### 2. Pick the most uncomfortable

Ask (plain text, open-ended): "Which of these feels most uncomfortable to you right now?"
Let the user point to a number or describe it. Confirm which item was chosen.

### 3. Five Whys interview

Ask up to 5 rounds:

> "Why does [item / previous answer] make you uncomfortable?"

After each answer, judge: is this a root cause (a belief, fear, or pattern with no deeper why), or is there another layer?
- If deeper layer exists → ask again
- If root reached (or 5 rounds done) → move on

Summarize the root cause in one sentence before continuing.

### 4. Set a goal

Based on the root cause, propose one concrete, time-bound goal:
- Specific action (not "be better at X")
- Achievable in 2–4 weeks
- Directly targets the root cause

Ask the user: "Does this goal feel right?" — let them adjust wording before saving.

### 5. Extract notes

Without asking the user, synthesize key things to remember from the conversation — constraints mentioned, prior attempts, patterns, context that would matter when working on this goal. Write 1–3 bullet points max. Omit if nothing meaningful surfaced.

### 6. Save

Promote the chosen item from `## Inbox` to its own H2 section in `~/.strong/uncomfortable.md`:

1. Remove the bullet from `## Inbox`
2. Add a new H2 section above `## Inbox`:

```
## [original item text]
- Root cause: [one sentence]
- Goal: [concrete goal]
- Notes: [synthesized from conversation — omit if empty]
```

If the item was already an H2 section (re-analysis), replace its sub-bullets in place.

## Rules

- Never skip the 5 Whys — if the user gives shallow answers, gently push once more
- Goal must be specific and time-bound — reject vague goals like "work on this"
- One uncomfortable item per session
