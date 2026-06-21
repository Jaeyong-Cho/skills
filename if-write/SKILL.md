---
name: if-write
description: Design an interface through Socratic grilling, then write the structured IF doc to docs/src/if/<name>.md for if-impl to consume. Use when user wants to design a new interface, write IF docs, mentions "if-write", "design interface", "write IF doc", or wants to plan an interface before implementing it.
---

# IF Write (Design → Doc)

Design an interface through grilling, then output a structured doc for if-impl.

Read [deep-modules](../references/deep-modules.md), [archi](../references/archi.md), [tdd](../references/tdd.md), and [tdd-tests](../references/tdd-tests.md) before starting.

## Step 0: Language (first IF only)

Check whether `src/if/` contains any existing IF files. If none exist, ask the user what programming language the project uses before grilling. Use the answer to set the language for all code blocks in the doc (method signatures, usage examples).

## Step 1: Grill the design

Before asking anything, map the decision space: identify every ambiguous or consequential decision this interface requires. Rank them by impact — which ones, if decided wrong, ripple through the whole design?

Then ask only about the high-impact ambiguous ones, in order of importance. Skip decisions that are obvious, derivable from the codebase, or have a clear default. Do not walk every branch — focus on the ones where the answer genuinely changes the shape of the interface.

Ask one question at a time. When a question has clear discrete options, use `AskUserQuestion` — put your recommended option first and append "(Recommended)" to its label. For open-ended questions, ask in plain text and state your recommendation explicitly.

If a question can be answered by exploring the codebase, explore instead of asking.

User can say "wrap up" to stop early.

## Step 2: Write the doc

Confirm the IF name with the user. The layer is determined from the design (Value / Aspect / Object).

Write to `src/if/<layer>s/<name>.md` (e.g. `src/if/objects/user.md`, `src/if/aspects/auth.md`, `src/if/values/signup.md`) using [DOC_TEMPLATE.md](DOC_TEMPLATE.md).

If this is a new file, add it to `src/SUMMARY.md`. Follow this structure (paths relative to `src/`):

```md
# IF

## Objects

- [Objects](if/objects.md)
  - [IfName](if/objects/name.md)

## Aspects

- [Aspects](if/aspects.md)
  - [IfName](if/aspects/name.md)

## Values

- [Values](if/values.md)
  - [IfName](if/values/name.md)
```

If the layer is new, create `src/if/<layer>.md` as an index page listing the IFs in that layer. If the `# IF` section or `##` layer subsection doesn't exist in SUMMARY.md, create it. Insert new entries in alphabetical order within the subsection.

## Rules

- Grill first, write second — no doc until design is settled.
- Omit sections (CLI, UI) if not applicable to this interface.
- If a design decision conflicts with deep-module or layer rules, surface it during the grill — not after writing.
- **Layer dependency check**: before finalizing the doc, verify every entry in Dependencies points to a same or inner layer IF. Flag any upward reference (inner → outer) as a design error and force a redesign before writing.
- **Testability check**: before finalizing, verify — dependencies injectable? returns results instead of side effects where possible? public surface no wider than needed? If not, surface the conflict during the grill per [tdd](../references/tdd.md) and [deep-modules](../references/deep-modules.md).
