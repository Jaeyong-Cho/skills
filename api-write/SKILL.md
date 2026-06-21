---
name: api-write
description: Design an API through Socratic grilling, then write the structured API doc to docs/src/api/<name>.md for api-impl to consume. Use when user wants to design a new API, write API docs, mentions "api-write", "design API", "write API doc", or wants to plan an API before implementing it.
---

# API Write (Design → Doc)

Design an API through grilling, then output a structured doc for api-impl.

Read [deep-modules](../references/deep-modules.md) and [archi](../references/archi.md) before starting.

## Step 0: Language (first API only)

Check whether `src/api/` contains any existing API files. If none exist, ask the user what programming language the project uses before grilling. Use the answer to set the language for all code blocks in the doc (method signatures, usage examples).

## Step 1: Grill the design

Before asking anything, map the decision space: identify every ambiguous or consequential decision this API requires. Rank them by impact — which ones, if decided wrong, ripple through the whole design?

Then ask only about the high-impact ambiguous ones, in order of importance. Skip decisions that are obvious, derivable from the codebase, or have a clear default. Do not walk every branch — focus on the ones where the answer genuinely changes the shape of the API.

Ask one question at a time. When a question has clear discrete options, use `AskUserQuestion` — put your recommended option first and append "(Recommended)" to its label. For open-ended questions, ask in plain text and state your recommendation explicitly.

If a question can be answered by exploring the codebase, explore instead of asking.

User can say "wrap up" to stop early.

## Step 2: Write the doc

Confirm the API name with the user. The layer is determined from the design (Value / Aspect / Object).

Write to `src/api/<layer>s/<name>.md` (e.g. `src/api/objects/user.md`, `src/api/aspects/auth.md`, `src/api/values/signup.md`) using [DOC_TEMPLATE.md](DOC_TEMPLATE.md).

If this is a new file, add it to `src/SUMMARY.md`. Follow this structure (paths relative to `src/`):

```md
# API

## Objects

- [Objects](api/objects.md)
  - [ApiName](api/objects/name.md)

## Aspects

- [Aspects](api/aspects.md)
  - [ApiName](api/aspects/name.md)

## Values

- [Values](api/values.md)
  - [ApiName](api/values/name.md)
```

If the layer is new, create `src/api/<layer>.md` as an index page listing the APIs in that layer. If the `# API` section or `##` layer subsection doesn't exist in SUMMARY.md, create it. Insert new entries in alphabetical order within the subsection.

## Rules

- Grill first, write second — no doc until design is settled.
- Omit sections (CLI, UI) if not applicable to this API.
- If a design decision conflicts with deep-module or layer rules, surface it during the grill — not after writing.
- **Layer dependency check**: before finalizing the doc, verify every entry in Dependencies points to a same or inner layer API. Flag any upward reference (inner → outer) as a design error and force a redesign before writing.
