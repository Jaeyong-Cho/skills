---
name: grill-me
description: Calibrate the user's understanding, teach only the knowledge needed for the session, then interview round by round over a design-tree frontier with clear, specific questions. Invoke as /grill-me, or via dev-grill-me's checklists.
disable-model-invocation: false
---

# Grill Me

Interview the user until you reach a shared understanding. First calibrate what the user already understands, then teach only the knowledge needed for this session, then work the decision tree. Do not jump straight into grilling.

## Question format (mandatory)

Every user-facing question must use this format; never send a bare question. Include all three core parts: **Background context**, **Current situation**, and **Specific question**. Explain the background and situation sufficiently for the user to understand why the question is being asked; do not compress either into a single vague or fragmentary sentence. Include the relevant facts, prior decisions, constraints, and uncertainty, while omitting unrelated detail.

Make the question easy to understand with the clearest aid for the topic:
- Use a concrete **example** when the user must compare, predict, or choose.
- Use a fenced **code block** when syntax, data, a request, or an implementation shape is relevant.
- Use an **ASCII diagram** when showing flow, relationships, states, boundaries, or alternatives. Do not use Mermaid or image-only diagrams.

Add one or more of these aids whenever they remove ambiguity; do not add decorative examples or diagrams that do not help answer the question. Also state the **Desired answer** and, when making a decision, the **Recommended answer**. This applies to calibration, teach-back, scope confirmation, and every grill round.

```text
❓ **Qn** - **<short title>**:

**Background context**
- **Goal:** [what we are trying to understand or decide]
- **Why it matters:** [the impact or reason this question is relevant]

**Current situation**
- **Known or observed:** [relevant facts and evidence]
- **Already decided:** [prior answers or constraints]
- **Uncertain:** [the specific gap this question addresses]

**Helpful example / code / ASCII diagram (when useful)**
[one concrete aid tied directly to the question]

**Specific question:** [one precise question]
**Desired answer:** [the response shape wanted: choice, comparison, example, priority, constraint, or trade-off]

➡️ **Recommended answer:** [answer and brief reason, when applicable]
```

## Session sequence

Run these stages in order. Keep the user's learning level and unresolved decisions visible throughout the session.

### 0. Calibrate current understanding

Before explaining the topic or asking design questions, ask one Socratic baseline question. Ask the user to explain, predict, compare, or give an example; do not ask only “Do you understand?”. Use the answer to classify:

- **Known** — the user can explain it accurately.
- **Assumed** — plausible, but not confirmed by the user's answer.
- **Needs teaching** — a concept or fact required for the selected session is missing or incorrect.

Use this format, filling in the real topic and situation:

```
❓ **Q1** - **What is your current model?**:

**Background context**
- **Goal:** We are working on [topic and goal].
- **Why it matters:** [why calibrating your current model matters for this session].

**Current situation**
- **Known or observed:** [what is already known or observed].
- **Already decided:** [any confirmed scope or constraints].
- **Uncertain:** [what is not yet understood].

**Specific question:** In your own words, what do you think is happening, what outcome matters, and which part is uncertain?
**Desired answer:** A short explanation, one example or prediction, and the point you are least sure about.

➡️ **Recommended answer:** Explain your current understanding without looking anything up; uncertainty is useful here.
```

Do not correct or grill yet. First reflect the answer back and record **Known**, **Assumed**, and **Needs teaching**. If the topic is too broad, narrow it after this calibration and before teaching.

### 1. Teach the needed knowledge

Inspect repository and environment facts yourself. Then make a small knowledge map for this session:

1. **Essential** — the minimum concepts, terms, constraints, or facts needed to answer the upcoming questions.
2. **Relevant** — useful context that may affect a decision.
3. **Not needed now** — interesting detail to defer.

Teach only **Essential** knowledge first. For each item, use: plain definition, why it matters here, one concrete example, and the decision it affects. Define jargon before using it. Correct misunderstandings directly but briefly; do not dump documentation or teach unrelated theory.

After the minimum briefing, use one teach-back checkpoint before grilling:

```
❓ **Q2** - **Can we use this model?**:

**Background context**
- **Goal:** We need to decide [the selected session decision].
- **Why it matters:** [why this minimum model is necessary before grilling].

**Current situation**
- **Known or observed:** We now know [the minimum facts or concepts just explained].
- **Already decided:** [the selected scope and any constraints].
- **Uncertain:** [the remaining concept or consequence that needs checking].

**Specific question:** Which part changes your original understanding, and how would you apply it to [one concrete example]?
**Desired answer:** A short restatement and application; say “I don't know” if the explanation is still unclear.

➡️ **Recommended answer:** Restate [the core concept] and apply it to [the example], while naming any remaining uncertainty.
```

If the teach-back reveals a gap, explain only that gap and repeat the checkpoint. Move on when the user can state the selected scope, the key terms, and the consequence relevant to the session. Do not require encyclopedic knowledge.

### 2. Grill with a clear question framework

Only now start the design-tree interview. Every question must make the following explicit:

1. **Background context** — why this question matters.
2. **Current situation** — the facts and decisions already settled.
3. **Specific question** — one decision, not a vague request for opinions.
4. **Desired answer** — the response shape wanted (choice, comparison, example, priority, constraint, or trade-off).

Use plain language, define vague terms, and state the user's available choices when useful. Give enough background and current-situation detail that someone joining the conversation could understand the question without guessing; one-line labels are not sufficient when more explanation is needed. Add a concrete example, fenced code block, or ASCII diagram when it makes the context, trade-off, or expected answer easier to understand. Before sending a question, check: “If someone heard this for the first time, would they know exactly what I need from them?” Include the recommendation and its brief reason.

Continue numbering from the calibration and teach-back questions:

```
❓ **Q3** - **<specific decision>**:

**Background context**
- **Goal:** [what this decision will determine]
- **Why it matters:** [the impact of this decision on the next branch]

**Current situation**
- **Known or observed:** [relevant facts and evidence]
- **Already decided:** [settled facts, prior answers, and constraints]
- **Uncertain:** [the unresolved choice or trade-off]

**Specific question:** [one precise question]
**Desired answer:** [the form and detail of answer wanted]

➡️ **Recommended answer:** [answer and brief reason].
```

## Scope check

After calibration and before building the minimum knowledge map: if the topic looks too large for a handful of rounds to converge (a whole system, a whole app, several unrelated features bundled together), **MUST ASK** for confirmation — show 2-3 candidate narrower sub-scopes, each a single focused target this session could actually finish, with your recommended one marked `➡️`. “No, keep the full scope” is a valid answer — treat it as confirmation and proceed with everything. A topic that's already a single focused target skips this check. Teach only after the slice is selected.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the surviving frontier in one round, **capped at 3 questions**: number each question and give your recommended answer, then wait for the user's answers before the next round. If the frontier has more than 3, ask the 3 highest-impact/most-blocking ones (per `../references/grill-impact.md` where applicable) and carry the rest into the next round instead of dumping the whole tree at once.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

If needed some experiment to find the question's answer, run the `@skills/experiment`.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

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

## Next round

Each round's answers reshape the tree — settled decisions push the frontier
outward and unblock questions that depended on them. Recompute the frontier
and ask the next round.

## Done

The session is done when the frontier is empty: every branch of the design
tree visited, nothing left silently assumed. Do not act on it until the
user confirms shared understanding.
