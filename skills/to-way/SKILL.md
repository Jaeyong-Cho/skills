---
name: to-way
description: Record all Wayfinder ways for one problem layer, why each is needed, how each is validated, and which existing skill fits. Invoke as /to-way.
disable-model-invocation: true
---

# To-Way

Turn one complete Wayfinder result into a concise, reusable rationale document containing every way for one problem layer. It explains why each way is needed now, not a full design or implementation plan.

## Why this exists

`@skills/wayfinder` produces candidate ways for one problem layer. Its alternatives can disappear into chat or become an unexamined recommendation. `to-way` preserves the complete set of ways, each way's purpose, uncertainty, validation signal, and existing skill handoff so later work can compare them without losing the current-layer boundary.

## Workflow

1. **Gather one layer's ways.** Use the complete Wayfinder result from this session or from a supplied source. Record the root problem, current layer, immediate objective, relevant constraints, and every way in the result. For each way, record its uncertainty, validation method, supporting signal, rejecting signal, recommended existing skill, and production handoff. Completion criterion: every way in the source is included; if the source has one way, include that one way.
2. **Keep the boundary.** Do not select, rank, discard, or merge ways; rerun the decision; explore deeper layers; invent missing facts; or turn the record into a design or implementation plan. If no Wayfinder result is available, tell the user to run `/wayfinder` first. If current-layer facts are missing, do not fill them from assumptions. Preserve `/wayfinder` as the recommendation for any way that is not actionable.
3. **Explain each need.** For every way, put its direct connection to the root problem and immediate objective first. Explain what would remain uncertain or unsafe without that way. Do not justify a way with unrelated future benefits.
4. **Follow document style.** Read `../references/document-style.md` and `../references/document-style/understanding-and-structure.md`. Keep the conclusion before supporting details and use short, concrete language.
5. **Confirm the location.** If this session has not already confirmed a destination, ask one `❓`/`➡️` question using `../references/question-format.md`. Recommend `./ways/` in the current directory. Once confirmed, write `./ways/{nn}-{slug}.md`, where `{nn}` is the next zero-padded sequence in `ways/`; update an existing same-layer file instead of creating a duplicate.
6. **Write the record** with this structure:

   ```markdown
   ---
   type: Way Record
   title: <short current-layer name>
   description: <one-line explanation of why this layer needs these ways>
   tags: [wayfinder, validation]
   timestamp: <ISO 8601 datetime>
   ---

   # <short current-layer name>

   ## Why this layer needs a way
   <Why these ways are necessary for the root problem and immediate objective at the current layer.>

   ## Current layer
   - Root problem: ...
   - Current layer: ...
   - Immediate objective: ...
   - Relevant constraints: ...

   ## Ways

   ### Way 1 — <short way name>
   - Why this way is needed: ...
   - Approach and uncertainty: ...
   - Cheapest useful test: ...
   - Supporting signal: ...
   - Rejecting signal: ...
   - Recommended skill: `/skill-name` — why it fits; use `/wayfinder` if the way is not actionable.
   - Handoff: ...

   ### Way 2 — <short way name>
   - Why this way is needed: ...
   - Approach and uncertainty: ...
   - Cheapest useful test: ...
   - Supporting signal: ...
   - Rejecting signal: ...
   - Recommended skill: `/skill-name` — why it fits; use `/wayfinder` if the way is not actionable.
   - Handoff: ...

   <Repeat the Way block for every way in the result.>

   ## Deferred beyond this layer
   ...
   ```

   Completion criterion: the file includes every way from one Wayfinder result, explains why each way is needed, names the current layer, gives each way a validation method with supporting and rejecting signals, and records one existing next skill or `/wayfinder` when a way is not actionable.

Tell the user the file path when done.
