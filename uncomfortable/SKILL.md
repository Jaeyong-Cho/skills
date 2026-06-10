---
name: uncomfortable
description: Surface and resolve uncomfortable things. Reads ~/.strong/uncomfortable.md, interviews the user to pick the most uncomfortable item, runs 5 Whys to find the root cause, then sets a concrete goal and appends it back to the file. Use when user says "uncomfortable", "face uncomfortable", "what's bothering me", or "work through my uncomfortable list".
---

# Uncomfortable

Surface what's uncomfortable, find why, set a goal to face it.

## Data file

`~/.strong/uncomfortable.md` — simple bullet list, one item per line.

If the file doesn't exist, create `~/.strong/` and an empty `~/.strong/uncomfortable.md`.

## Process

### 1. Show the list

Read `~/.strong/uncomfortable.md` and display all items numbered.
If the list is empty, tell the user and stop — ask them to add items first.

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

### 5. Capture notes

Ask (plain text): "What are the important things to remember when working on this goal?"

Let the user list anything — context, constraints, prior attempts, key insights from the interview. Accept free-form text. If they have nothing to add, skip.

### 6. Save

Append root cause, goal, and notes directly under the chosen item in `~/.strong/uncomfortable.md`:

```
- [original item text]
  - Root cause: [one sentence]
  - Goal: [concrete goal]
  - Notes: [key things to remember — from step 5, or omit if none]
```

If the item already has a root cause/goal block, replace it.

## Rules

- Never skip the 5 Whys — if the user gives shallow answers, gently push once more
- Goal must be specific and time-bound — reject vague goals like "work on this"
- One uncomfortable item per session
