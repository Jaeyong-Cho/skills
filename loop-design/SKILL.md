---
name: loop-design
description: Loop-design skill. Grills to resolve a recurring loop's goal, per-iteration body, test strategy, and required actions, then writes a spec. Use when invoked as /loop-design.
disable-model-invocation: true
---

# Loop Design

Read `.context/wiki/` for context. If an existing `.context/loop/` file covers the same topic, read it and revise it rather than creating a new one.

Use this before setting up a recurring `/loop` or a `/schedule` cron routine — it resolves what the loop should do, not how often it fires.

Run a `/grilling` skill to resolve every branch:

1. **Goal** — what should this loop achieve or watch for? What does success look like across many iterations, not just one?
2. **Loop body** — what exact action happens each iteration? One concern, describable without "and". If it takes several ordered sub-steps, number them.
3. **Test strategy** — how do you know one iteration worked? How do you verify across iterations without re-running everything? Apply `test-loop.md`: run once, verify many.
4. **Progress record** — what does each iteration write down to show it happened? One line per iteration: timestamp, what happened, per-iteration test result. Where does it live, and how does a human — or the next iteration — read it back to know where the loop left off?
5. **Required actions** — what tools, permissions, or external access does each iteration need (Bash commands, APIs, file writes, credentials)?
6. **Stop condition** — what ends the loop? A condition met, a max iteration count, a time bound, or explicit user cancellation. A loop without one runs forever — name it.
7. **Runner** — `/loop` (interval-based, in-session) or `/schedule` (cron-based, cloud)? State which and why.

The last sub-step of every iteration in the Loop Body is always: append one line to the Progress Record.

Grill until every branch is resolved and the user confirms. Completion criterion: goal, loop body, test strategy, progress record, required actions, and stop condition are all unambiguous, and a runner is chosen.

Get the timestamp: run `date +%Y%m%d-%H%M%S`. Derive a kebab-case slug from the topic.

Write `.context/loop/{timestamp}-{slug}.md`:

```markdown
# {Topic}

## Goal
{What the loop should achieve or watch for, across many iterations}

## Loop Body
{The exact action(s) each iteration performs}

## Test Strategy
- **Per-iteration:** {how to know this one iteration worked}
- **Across iterations:** {how to verify the loop overall — run once, verify many}

## Progress Record
{Format and location of the per-iteration log — e.g. `.context/loop/{timestamp}-{slug}-progress.md`, one line per iteration: timestamp, what happened, test result}

## Required Actions
{Tools, permissions, or external access each iteration needs}

## Stop Condition
{What ends the loop}

## Runner
{/loop or /schedule, and why}
```

`mkdir -p .context/loop` if needed. Tell the user the file path. Next step: hand the spec to whichever runner was chosen (`/loop` or `/schedule`).

Any useful truth discovered during this session — a constraint, a domain fact, a key decision — can also be written to `.context/wiki/` at any time.

**DO NOT START THE LOOP**
