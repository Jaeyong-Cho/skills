---
name: question-brainstorm
description: Brainstorm candidate `## Question N` entries for goal.md instead of leaving the user to invent them alone — reads the goal statement, existing questions, root README, .context/ intents, and (when the goal is codebase-relevant) a fresh /explore pass, then proposes 3-5 falsifiable questions aimed at the riskiest unresolved assumption blocking the goal. Use when the user has a goal but no question yet, wants help figuring out what to validate next, or asks things like "what should I even be asking here" / "what's the riskiest assumption in this goal". Runs before /goal-init's directory-creation step, or after it to add more questions to an existing goal.
disable-model-invocation: true
allowed-tools: Read, Write, Skill, AskUserQuestion
---

# Question Brainstorm

Turns a goal statement into candidate questions instead of requiring the user to already know what to ask. Slots into the Goal-to-Implementation Loop (root `README.md`) right after `/goal-init` writes the goal statement, and writes its output the same way `/goal-init` step 2 would — directly into `goal.md`'s `## Question N` headings — so `/goal-init` can pick up from there and create directories.

- `goal.md` must already exist with a goal statement. No `goal.md` -> stop and tell the user to run `/goal-init` first.
- Every proposed question must be falsifiable (a report could come back Supported, Refuted, or Inconclusive against it) — not a vague topic to explore.
- Don't propose a question that duplicates or trivially rephrases one already in `goal.md`.
- **DO NOT** read the codebase directly — use `/explore`.

## Steps

1. **Read the goal and existing questions.** Parse `goal.md`: the latest goal statement, every existing `## Question N` heading (and its `**Answer:**` line, if `/experiment` already closed it — a closed question is context, not something to re-propose).

2. **Gather cheap context.** Read root `README.md` and every file in `.context/` if either exists — these carry constraints, priorities, and prior decisions that shape which questions are actually worth asking, per this repo's Project Intents convention.

3. **Decide whether the goal is codebase-relevant.** If the goal concerns this project's code, architecture, or data (most goals in a code repo do), **MUST RUN** `../explore/SKILL.md` posing 2-4 factual questions about the current state relevant to the goal (e.g. "does a caching layer already exist?", "what does the current data model look like?") — grounds the brainstorm in what's actually true instead of inventing questions about a codebase state that doesn't exist. Direct it to save the combined evidence to `questions/.context/explore/goal-context.md` (create the directory if missing) instead of its default per-question path — this is goal-level evidence, gathered before any question's own directory exists, and step 8 propagates it forward so later stages don't re-explore the same ground. Skip this step only for goals with no codebase angle at all (e.g. purely product/strategy goals).

4. **Brainstorm 3-5 candidates.** Each should target a distinct risk or unresolved assumption standing between the current state and the goal — not 5 phrasings of the same uncertainty. Favor the question whose answer would most change what happens next; a question whose answer is already implied by the explore evidence or existing report isn't a good candidate. State each candidate as a single falsifiable sentence, the same form a `## Question N` heading takes (e.g. "Does the cache TTL bound P99 latency?").

5. **Let the user pick and edit.** Present the candidates via `AskUserQuestion` (multiSelect) so the user can select any subset — they can also use "Other" to submit edited wording or a question you missed entirely. Don't auto-commit anything before this step; brainstormed questions are proposals, not decisions.

6. **Append the chosen questions to `goal.md`.** For each one selected (in the user's final wording), append a `## Question N` heading, continuing numbering from the highest existing one — same format `/goal-init` step 2 uses:
   ```
   ## Question 4
   Does the cache TTL bound P99 latency?
   ```

7. **Hand off to `/goal-init`.** Invoke it to create `questions/{slug}/` for the newly added headings and rebuild `questions/index.html` — steps 3-5 of that skill are idempotent for headings that already have a directory, so this is safe to call even if some questions in `goal.md` were added earlier by other means.

8. **Propagate the explore evidence.** If step 3 ran, copy `questions/.context/explore/goal-context.md` into `questions/{slug}/.context/explore/goal-context.md` for each question created in step 7 — not moved, since one brainstorm pass covers every candidate it produced. `/experiment`'s explore stage checks for this file before dispatching its own `/explore` (see its `references/explore-stage.md`), so this is what lets it skip re-exploring ground this stage already covered.
