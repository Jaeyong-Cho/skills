---
name: buimpl
description: Bottom-up implementation driven by a tdgoal report — writes IF docs and implements each component layer by layer from Objects up to External. Use when user has a tdgoal report and wants to implement it, mentions "buimpl", "implement from goal", or "bottom-up implement".
---

# BUImpl (Bottom-Up Implementation)

Read a tdgoal report and implement all components bottom-up: Objects → Logics → Usecase → External. For each component, write the IF doc then implement via TDD before moving to the next layer.

Read [deep-modules](../references/deep-modules.md), [archi](../references/archi.md), [tdd](../references/tdd.md), [tdd-tests](../references/tdd-tests.md), [tdd-mocking](../references/tdd-mocking.md), and [tdd-refactoring](../references/tdd-refactoring.md) before starting.

## Step 0: Language

Check whether `src/if/` contains any existing IF files. If none exist, ask the user what programming language the project uses. Use the answer for all code blocks in IF docs.

## Step 1: Read the tdgoal report

User provides the path to a tdgoal report (`{timestamp}_{slug}.md`). Read it and extract all components across all scenarios, deduplicated, grouped by layer:

- **Objects** — all objects referenced across scenarios
- **Logics** — all logics, noting which objects each uses
- **Usecase** — all usecases, noting which logics each calls in order
- **External** — all triggers, noting which usecase each invokes

Flag any component marked `remove` — confirm with the user before deleting anything.

## Step 2: Implement bottom-up — one layer at a time

Work through layers in this order: **Objects → Logics → Usecase → External**. Within each layer, implement components in dependency order (no component before its dependencies).

For each component:

### 2a. Write the IF doc (if-write rules)

Write to `src/if/<layer>s/<name>.md` using the [if-write DOC_TEMPLATE](../if-write/DOC_TEMPLATE.md).

- Derive the public methods, signatures, and algorithm from the tdgoal report
- For `create`: write a full new doc
- For `update`: read the existing doc, update only the changed parts
- For `remove`: confirm with the user, then delete the file and remove from `src/SUMMARY.md`
- **Layer dependency check**: every dependency must point to a same or inner layer. Flag upward references before writing.
- **Testability check**: dependencies injectable? results over side effects? surface narrowed?

### 2b. Implement via TDD (if-impl rules)

For each public entry point in the doc, follow RED → GREEN → REFACTOR:

**RED** — write a failing test that calls the public method and asserts specified behavior.

**GREEN** — write minimal code to pass:
1. Match signature exactly
2. Follow the algorithm from the doc
3. Accept dependencies as injected params
4. Run tests — confirm GREEN before continuing

**REFACTOR** — with tests green: narrow interfaces, extract private helpers, hide complexity. Run tests after each step.

Do not move to the next component until current one is GREEN and refactored.

## Step 3: Done

List all implemented components by layer. Flag any deviations from the tdgoal report with reason.
