# Question Format (❓ / ➡️)

When a skill needs to ask the human a question mid-task, format each one so the ❓/➡️ markers render as intended (not swallowed into a paragraph or split across a numbered list) instead of asking in plain prose:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

- A blank line before and after the block, and never inline mid-sentence or mid-numbered-step — it must stand on its own so the emoji/bold render instead of collapsing into surrounding text.
- Number each question (`Q1`, `Q2`, ...) even when there's only one — a reader answering out of order can point at "Q2" precisely.
- Every question carries a recommended answer (➡️) — never ask without one. "I don't know" / "not sure" / "you decide" is itself a valid reply, not a stall: take the recommended answer as the decision rather than re-asking.
- Batch related questions instead of asking one at a time when several are ready at once, but keep each its own self-contained ❓/➡️ block.

For a full round-based interview (a frontier of questions capped per round, re-asked as answers unblock more) rather than one or two inline questions, use `@skills/grill-me` instead of hand-rolling this.
