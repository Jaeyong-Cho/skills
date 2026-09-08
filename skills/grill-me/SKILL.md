---
name: grill-me
description: Personal grilling engine — interview the user round by round over a design-tree frontier; any question the user can't answer gets progressive-disclosure clarification before being re-asked. Invoke as /grill-me, or via dev-grill-me's checklists.
disable-model-invocation: false
---

# Grill Me

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

## Scope check

Before round 1: if the topic handed to this skill looks too large for a handful of rounds to converge (a whole system, a whole app, several unrelated features bundled together), **MUST ASK** for confirmation before diving in — show 2-3 candidate narrower sub-scopes, each a single focused target this session could actually finish, with your recommended one marked `➡️`. "No, keep the full scope" is a valid answer — treat it as confirmation and proceed with everything. A topic that's already a single focused target skips this check — go straight to round 1.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the surviving frontier (after the KB check above) in one round, **capped at 3 questions**: number each question and give your recommended answer, then wait for the user's answers before the next round. If the frontier has more than 5, ask the 5 highest-impact/most-blocking ones (per `../references/grill-impact.md` where applicable) and carry the rest into the next round instead of dumping the whole tree at once.

Each question should be formatted like so:
```text
# ❓ Qn — <one precise question?>

<Why this matters, what is already true, and what remains uncertain.>

**Example**
<Concrete scenario, fenced code, or ASCII diagram.>

**Answer with:** <the expected response shape>

➡️ **Recommendation:** <answer and brief reason>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

If needed some experiment to find the question's answer, run the `@skills/experiment`.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Good question framework

Build each question from these parts:

1. **Purpose** — state the goal and why this decision matters.
2. **Grounding** — summarize the relevant evidence, current situation, prior decisions, and constraints.
3. **Gap** — identify the uncertainty or trade-off that remains.
4. **Helpful example (required)** — give one concrete scenario that makes the choice easier to understand.
5. **Focused question (required H1)** — put the complete question at the top as `# ❓ Qn — <actual question?>`. It must be a real question ending in `?`, not a topic or short title.
6. **Response shape** — say whether the useful answer is a choice, comparison, example, priority, constraint, or trade-off.
7. **Recommendation** — for a decision, give the preferred answer and a brief evidence-based reason.

These are ingredients, not mandatory headings. Use natural prose, combine parts when that reads better, and omit anything that adds no value. Two presentation elements are mandatory for every user-facing question, including calibration, scope checks, teach-back, and decision rounds: the question H1 at the top and a helpful example. Give enough context that the user does not have to reconstruct the conversation, but do not bury the question in unrelated detail.

The example must be specific enough for the user to reason from; merely rephrasing the question does not count. Use a fenced code block when syntax, data, requests, or implementation shapes matter. Use an ASCII diagram for flows, relationships, states, boundaries, or alternatives. Do not use Mermaid or image-only diagrams.

```text
# ❓ Qn — <one precise question?>

<Why this matters, what is already true, and what remains uncertain.>

**Example**
<Concrete scenario, fenced code, or ASCII diagram.>

**Answer with:** <the expected response shape>

➡️ **Recommendation:** <answer and brief reason>
```

Keep numbering and recommendations for decision questions. Calibration and teach-back may use a natural response suggestion instead of a recommendation.

Before sending, verify that the question:

- starts with the complete question as an H1 and ends it with `?`;
- includes a concrete helpful example;
- is answerable from the context provided;
- asks one thing rather than bundling dependent decisions;
- uses plain, neutral language and defines necessary jargon;
- does not ask the user for facts you can inspect yourself;
- makes the consequence of the answer clear.

## When the user can't answer one

"I don't know" / "not sure" / "you decide" is itself a valid answer, not a
stall — don't push back or re-ask it. Take the recommended answer (➡️) as
the decision, tag it as an assumption with its uncertainty (per
`../references/grill-impact.md`) so it carries into `@skills/to-plan`'s
Assertions section, and move straight to the rest of the round.

Only when the reply is an actual question back — they're asking *you*
something, not declining to decide — answer it first, in layers, with
`@skills/grill-ai`:

- Core: answer, 1-2 sentences
- Reason: key reasoning, only if they push further
- Detail: examples/edge cases, only if explicitly requested

Re-ask that Qn, unchanged, in the next round alongside whatever else the
frontier opens up. Don't let one unanswered question block recording the
round's other answers.

## Preference
- I don't want to too much over engineering.
- Do not think about the uncertainty not yet encountered.

## Next round

Each round's answers reshape the tree — settled decisions push the frontier
outward and unblock questions that depended on them. Recompute the frontier
and ask the next round.

## Done

The session is done when the frontier is empty: every branch of the design
tree visited, nothing left silently assumed. Do not act on it until the
user confirms shared understanding.
