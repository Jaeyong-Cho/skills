---
name: directing
description: Direction-setting skill. Grills to find the real goal, explores the decision space, commits to a direction, and writes the direction. Use when invoked as /directing.
disable-model-invocation: true
---

# Directing

Read all files in `.sot/wiki/` and `.sot/attack/` for context. If invoked with a finding from /attack, treat it as the starting problem.

Use this for new goals or to redirect an existing one. If an existing direction file covers the same topic, read it and update it rather than creating a new file.

Run a `/grilling` skill to reach a committed direction:

1. **Goal** — what does success actually look like? Push past the surface request to the real outcome the user needs.
2. **Failure modes** — what does bad look like? What is the ambiguous middle zone where partial success might be acceptable vs not? Name specific failure conditions, not just "it doesn't work."
3. **Decision space** — what are the options? For each: what does it unlock, what does it cost, what does it leave unresolved?
4. **Constraints** — what is fixed vs. assumed? Challenge assumed constraints.
5. **Direction** — one choice the user commits to. Not "we might" — "we will."

Grill until the direction is unambiguous. Completion criterion: the user has stated a committed direction in their own words.

Get the timestamp: run `date +%Y%m%d-%H%M%S`. Derive a kebab-case slug from the topic.

Write `.sot/direction/{timestamp}-{slug}.md`:

```markdown
# {Topic}

## Goal
{What success looks like}

## Failure Criteria
{What bad looks like — specific failure conditions}

## Ambiguous Zone
{What partial success looks like — which tradeoffs are acceptable vs not}

## Direction
{The committed choice and why}

## Constraints
{What is fixed}

## Out of Scope
{What was explicitly ruled out}
```

`mkdir -p .sot/direction` if needed. Tell the user the file path. Next step: `/planning`.

Any useful truth discovered during this session — a constraint, a domain fact, a key decision — can also be written to `.sot/wiki/` at any time.

**DO NOT START IMPLEMENT**
