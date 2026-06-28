---
name: directing
description: Direction-setting skill. Grills to find the real goal, explores the decision space, commits to a direction, and writes the wiki. Use when invoked as /directing.
disable-model-invocation: true
---

# Directing

Read all files in `source-of-truth/wiki/` and `source-of-truth/attack/` for context. If invoked with a finding from /attack, treat it as the starting problem.

Run a `/grilling` skill to reach a committed direction:

1. **Goal** — what does success actually look like? Push past the surface request to the real outcome the user needs.
2. **Decision space** — what are the options? For each: what does it unlock, what does it cost, what does it leave unresolved?
3. **Constraints** — what is fixed vs. assumed? Challenge assumed constraints.
4. **Direction** — one choice the user commits to. Not "we might" — "we will."

Grill until the direction is unambiguous. Completion criterion: the user has stated a committed direction in their own words.

Then write `source-of-truth/wiki/{topic}.md`:

```markdown
# {Topic}

## Goal
{What success looks like}

## Direction
{The committed choice and why}

## Constraints
{What is fixed}

## Out of Scope
{What was explicitly ruled out}
```

`mkdir -p source-of-truth/wiki` if needed. Tell the user the file path. Next step: `/planning`.
