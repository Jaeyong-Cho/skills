---
name: grill-me
description: Calibrate the user's understanding, teach only the knowledge needed for the session, then interview round by round over a design-tree frontier with clear, specific questions. Invoke as /grill-me, or via dev-grill-me's checklists.
disable-model-invocation: false
---

# Grill Me

Interview the user until you reach a shared understanding. Calibrate first, teach only what this session needs, then work through the decision tree. Do not jump straight into grilling.

## Ask understandable questions

Each question must give the user enough information to answer without reconstructing the conversation. Cover:

- **Background context** — the goal and why the decision matters.
- **Current situation** — relevant facts, prior decisions, constraints, and remaining uncertainty.
- **Specific question** — one clear decision or teach-back prompt.
- **Expected response** — the useful answer shape.

These are content requirements, not a rigid form. Use natural prose, combine sections when that reads better, and omit empty labels. Do not reduce context to vague one-line fragments when the user needs more explanation.

Include one concrete **helpful example** by default. An example should let the user compare, predict, or choose rather than merely repeat the question. Replace or support it with:

- a fenced code block for syntax, data, requests, or implementation shapes;
- an ASCII diagram for flows, relationships, states, boundaries, or alternatives.

Use only aids that clarify the decision. Do not use Mermaid or image-only diagrams.

A good default—not a mandatory template—is:

```text
❓ **Qn — <short title>**

<Background and current situation in enough detail to make the question self-contained.>

**Example**
<Concrete scenario, fenced code, or ASCII diagram.>

**Question:** <one precise question>
**Answer with:** <choice, comparison, example, priority, constraint, or trade-off>

➡️ **Recommendation:** <answer and brief reason>
```

Adapt the format to the question. Keep numbering and recommendations for decision questions; calibration and teach-back prompts may use a more natural response suggestion instead of prescribing a decision.

Before sending, check: “Could someone joining now understand why this matters, what is already true, and exactly what answer I need?”

## Session sequence

Run these stages in order. Keep the user's learning level and unresolved decisions visible.

### 0. Calibrate current understanding

Ask one Socratic baseline question about the real topic. Ask the user to explain, predict, compare, or give an example; do not ask only “Do you understand?” Include a concrete scenario they can reason about.

Reflect their answer without correcting it yet, then record:

- **Known** — explained accurately.
- **Assumed** — plausible but unconfirmed.
- **Needs teaching** — required knowledge that is missing or incorrect.

### Scope check

If the topic is too large for a handful of rounds, ask the user to choose among 2–3 focused sub-scopes and mark the recommended one with `➡️`. “Keep the full scope” is valid. Skip this check for an already focused topic.

### 1. Teach only what is needed

Inspect repository and environment facts yourself. Build a small knowledge map:

1. **Essential** — required to answer this session's questions.
2. **Relevant** — may affect a decision.
3. **Not needed now** — defer.

Teach only **Essential** items first. For each, give a plain definition, why it matters here, one concrete example, and the decision it affects. Define jargon before using it; correct misunderstandings briefly.

Then ask one teach-back question: have the user restate the core concept and apply it to a concrete example. If it exposes a gap, teach only that gap and repeat. Continue when the user can state the scope, key terms, and relevant consequence.

### 2. Grill the decision tree

The **frontier** is every decision whose prerequisites are settled. Ask the surviving frontier in rounds of at most three questions, prioritizing the highest-impact or most-blocking decisions per `../references/grill-impact.md` where applicable.

For each decision question:

- ask one precise decision;
- include a helpful example;
- show available choices when useful;
- give a recommended answer with a brief reason.

After each response, record the decisions, recompute the frontier, and ask the next round. Do not ask a question while one of its prerequisites remains unresolved.

Finding facts is your job, not the user's. Inspect the environment or dispatch a sub-agent when needed. While exploration runs, ask unrelated frontier questions and defer only dependent ones. If evidence requires an experiment, use `@skills/experiment`.

## When the user cannot answer

“I don't know,” “not sure,” or “you decide” is a valid answer. Adopt the recommendation, mark it as an assumption with uncertainty per `../references/grill-impact.md`, and continue.

If the user asks you a question instead, answer it with `@skills/grill-ai`:

- **Core:** 1–2 sentence answer.
- **Reason:** only if they ask further.
- **Detail:** examples or edge cases only when requested.

Re-ask the original decision in the next round without discarding other answers from the current round.

## Done

Finish when the frontier is empty and nothing remains silently assumed. Summarize the shared understanding and ask the user to confirm it. Do not begin implementation before confirmation.
