---
name: directing
description: Direction-setting skill. Grills to find the real goal, explores the decision space, commits to a direction, and writes the direction. Use when invoked as /directing.
disable-model-invocation: true
---

# Directing

Read all files in `.context/wiki/` for context.

Check `.claude/agents/` and `.github/agents/` for existing project subagents. If one's description matches this topic, delegate the relevant research or exploration to it rather than doing that work inline yourself.

Use this for new goals or to redirect an existing one. If an existing direction file covers the same topic, read it and update it rather than creating a new file.

Run a `/grilling` skill to reach a committed direction:

1. **Goal** — what does success actually look like? Push past the surface request to the real outcome the user needs.
2. **Failure modes** — what does bad look like? What is the ambiguous middle zone where partial success might be acceptable vs not? Name specific failure conditions, not just "it doesn't work."
3. **Decision space** — what are the options? For each: what does it unlock, what does it cost, what does it leave unresolved?
4. **Constraints** — what is fixed vs. assumed? Challenge assumed constraints.
5. **Direction** — one choice the user commits to. Not "we might" — "we will."

Grill until the direction is unambiguous. Completion criterion: the user has stated a committed direction in their own words.

Get the timestamp: run `date +%Y%m%d-%H%M%S`. Derive a kebab-case slug from the topic.

Write `.context/direction/{timestamp}-{slug}.md`:

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

`mkdir -p .context/direction` if needed. If truths, constraints, or decisions worth persisting were discovered, or any existing wiki entries are now stale, update `.context/wiki/` via `/to-wiki` — skip it otherwise. Tell the user the file path. Next step: `/planning`.

**DO NOT START IMPLEMENT**
