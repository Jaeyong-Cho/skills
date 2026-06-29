---
name: directing
description: Direction-setting skill. Grills to find the real goal, explores the decision space, commits to a direction, and writes the wiki. Use when invoked as /directing.
disable-model-invocation: true
---

# Directing

Read all files in `source-of-truth/wiki/` and `source-of-truth/attack/` for context. If invoked with a finding from /attack, treat it as the starting problem.

Use this for new goals or to redirect an existing one. If an existing wiki file covers the same topic, read it and update it rather than creating a new file.

Run a `/grilling` skill to reach a committed direction:

1. **Goal** — what does success actually look like? Push past the surface request to the real outcome the user needs.
2. **Decision space** — what are the options? For each: what does it unlock, what does it cost, what does it leave unresolved?
3. **Constraints** — what is fixed vs. assumed? Challenge assumed constraints.
4. **Direction** — one choice the user commits to. Not "we might" — "we will."

Grill until the direction is unambiguous. Completion criterion: the user has stated a committed direction in their own words.

Get the timestamp: run `date +%Y%m%d-%H%M%S`. Derive a kebab-case slug from the topic.

Write `source-of-truth/direction/{timestamp}-{slug}.md`:

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

`mkdir -p source-of-truth/direction` if needed. Tell the user the file path. Next step: `/planning`.

Any useful truth discovered during this session — a constraint, a domain fact, a key decision — can also be written to `source-of-truth/wiki/` at any time.

**DO NOT START IMPLEMENT**
