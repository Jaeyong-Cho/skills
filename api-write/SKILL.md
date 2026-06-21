---
name: api-write
description: Design an API through Socratic grilling, then write the structured API doc to docs/src/api/<name>.md for api-impl to consume. Use when user wants to design a new API, write API docs, mentions "api-write", "design API", "write API doc", or wants to plan an API before implementing it.
---

# API Write (Design → Doc)

Design an API through grilling, then output a structured doc for api-impl.

Read [deep-modules](../pf/references/deep-modules.md) and [layers](../pf/references/layers.md) before starting.

## Step 1: Grill the design

Using the Socratic method — question assumptions, probe deeper. Starting context: the user's API scenario.

Interview me relentlessly about every aspect of this API until we reach a shared understanding. Walk down each branch of the design tree one decision at a time. For each question, provide your recommended answer.

Ask one question at a time. When a question has clear discrete options, use `AskUserQuestion` — put your recommended option first and append "(Recommended)" to its label. For open-ended questions, ask in plain text and state your recommendation explicitly.

If a question can be answered by exploring the codebase, explore instead of asking.

Keep going until every branch is resolved. User can say "wrap up" to stop early.

## Step 2: Write the doc

Confirm the API name with the user. The layer is determined from the design (Value / Aspect / Object).

Append a new section to `docs/src/api/<layer>.md` (e.g. `object.md`, `aspect.md`, `value.md`) using the section template in [DOC_TEMPLATE.md](DOC_TEMPLATE.md). Each file groups all APIs of that layer; each API is one H2 section within it.

If `docs/src/api/<layer>.md` does not exist yet, create it with an H1 header (`# <Layer> APIs`) before appending the section, then add it to `docs/src/SUMMARY.md` under the API section:

```md
- [Object APIs](api/object.md)
```

## Rules

- Grill first, write second — no doc until design is settled.
- Omit sections (CLI, UI) if not applicable to this API.
- If a design decision conflicts with deep-module or layer rules, surface it during the grill — not after writing.
- **Layer dependency check**: before finalizing the doc, verify every entry in Dependencies points to a same or inner layer API. Flag any upward reference (inner → outer) as a design error and force a redesign before writing.
