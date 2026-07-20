---
name: study-guide
description: Generate an interactive HTML study guide — explains a document or codebase, then quizzes the reader on it. Invoke as /study-guide {path or topic}.
disable-model-invocation: true
---

# Study Guide

Turn the specified document or code into a study guide: a page that teaches it, then tests whether the reading landed.

## Steps

1. **Scope the target.** Read the specified file(s) or topic. If it's code, explore broadly enough to explain it — callers, dependencies, the surrounding system — not just the file in isolation.
   Done when: you can state, unprompted and in one paragraph, what the target does and why it exists.

2. **Draft the content**, one section per concern:
   - *Background* — the existing system relevant to the target. Give a deep-enough background for a newcomer (skippable if the reader already knows it), then a narrower background specific to the target.
   - *Core concepts* — the essence, not the full detail. Ground every non-obvious claim in one worked example using real values from the target itself (real function names, real data, real config) rather than invented toy data — a reader learns from a concrete case, not an abstract description. Use diagrams liberally.
   - *Walkthrough* — a structured tour of the target's actual content or code, grouped for understanding (by concept or flow), not just read top-to-bottom.
   Done when: every non-obvious part of the target is covered by some section, and each core concept has at least one worked example.

3. **Write the quiz.** Five multiple-choice questions, medium difficulty — hard enough that answering requires having understood the substance, not spotting a gotcha. Each option is marked correct or incorrect.
   Done when: exactly five questions exist, each with exactly one option marked correct.

4. **Render it.** Assemble a JSON content spec matching the schema in `render.py`'s docstring (run `python3 render.py --help` if unsure), then run:
   ```
   python3 <this skill's directory>/render.py spec.json
   ```
   Write section `html` fields as real HTML, not markdown — see Content classes below.
   Done when: the command exits 0 and prints the output HTML path.

5. Report the output path to the user.

## Content classes

Write raw HTML into each section's `html` field, using these renderer-supported classes instead of ad hoc markup:

- `<pre><code>` — code blocks (pre-styled `white-space: pre-wrap`).
- `.diagram` / `.flow` / `.box` / `.box.fail` — flow diagrams (a simplified UI view, or a system/data-flow diagram with example data). Never use ASCII diagrams — always these classes.
- `.callout` — key definitions and edge cases.
- `.example` — a worked example grounding a concept in real values.
- `<table>` — comparisons.

## Prose style

Write with the clarity and flow of Martin Kleppmann: engaging, classic style, smooth transitions between sections — never a bare list of disconnected facts.
