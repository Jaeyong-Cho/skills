---
name: to-way
description: Record one selected Wayfinder way and explain why it is needed, how to validate it, and what follows. Invoke as /to-way.
disable-model-invocation: true
---

# To-Way

Turn one selected Wayfinder way into a concise, reusable rationale document. It explains why this way is needed now, not a full design or implementation plan.

## Why this exists

`@skills/wayfinder` produces candidate ways for one problem layer. Its output can disappear into chat or become an unexamined recommendation. `to-way` preserves the selected way's purpose, uncertainty, validation signal, and handoff so later work knows why the way exists and what evidence must come first.

## Workflow

1. **Gather one selected way.** Use the way and current-layer context from this session or from a supplied Wayfinder result. Record the root problem, current layer, immediate objective, relevant constraints, selected way, uncertainty, validation method, supporting signal, rejecting signal, and production handoff. Completion criterion: every listed fact is present or explicitly marked unknown.
2. **Keep the boundary.** Do not choose between multiple ways, rerun the decision, explore deeper layers, invent missing facts, or turn the record into a design or implementation plan. If no way is selected, ask one `❓`/`➡️` question for the user's choice; do not choose silently. If the current-layer facts are missing, tell the user to run `/wayfinder` first.
3. **Explain the need.** Put the selected way's direct connection to the root problem and immediate objective first. Explain what would remain uncertain or unsafe without it. Do not justify it with unrelated future benefits.
4. **Follow document style.** Read `../references/document-style.md` and `../references/document-style/understanding-and-structure.md`. Keep the conclusion before supporting details and use short, concrete language.
5. **Confirm the location.** If this session has not already confirmed a destination, ask one `❓`/`➡️` question using `../references/question-format.md`. Recommend `./ways/` in the current directory. Once confirmed, write `./ways/{nn}-{slug}.md`, where `{nn}` is the next zero-padded sequence in `ways/`; update an existing same-way file instead of creating a duplicate.
6. **Write the record** with this structure:

   ```markdown
   ---
   type: Way Record
   title: <short selected-way name>
   description: <one-line explanation of why this way is needed>
   tags: [wayfinder, validation]
   timestamp: <ISO 8601 datetime>
   ---

   # <short selected-way name>

   ## Why this way is needed
   <Why this way is necessary for the root problem and immediate objective at the current layer.>

   ## Current layer
   - Root problem: ...
   - Current layer: ...
   - Immediate objective: ...
   - Relevant constraints: ...

   ## Selected way
   <The chosen approach and the uncertainty it addresses.>

   ## Validation
   - Cheapest useful test: ...
   - Supporting signal: ...
   - Rejecting signal: ...

   ## Handoff
   - If supported: ...
   - If rejected: ...
   - Deferred beyond this layer: ...
   ```

   Completion criterion: the file explains why the way is needed, names the current layer, and gives a validation method with both supporting and rejecting signals.

Tell the user the file path when done.
