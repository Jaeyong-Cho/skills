---
name: req
description: Turn prototype and repository context into an approved inventory of vertical requirement slices, then write one requirement document per slice with concrete edge cases and testable acceptance criteria. Use before OOD.
disable-model-invocation: true
---

# Requirements

Cover the complete requirement set for one product goal in one invocation. The primary output is not a conversation transcript: it is one approved, independently verifiable requirement document per vertical slice plus the inventory that links them.

A batch may contain one slice. A slice owns one actor, purpose, outcome, and execution boundary. Keep its happy path and directly relevant edge, boundary, alternate, and failure cases together. Do not split by UI, backend, database, or other horizontal layers.

## Input

- Product goal and the prototype verdict, trial results, and context
- An optional candidate-slice inventory from the caller
- Existing repository instructions, specs, code, tests, and conventions needed to define observable behavior

If no inventory is supplied, derive one from the prototype and context before drafting documents. Do not guess around a blocking unknown; use the smallest executable experiment when execution is the only way to learn it.

## Output

- An approved inventory of non-overlapping vertical slices in dependency order
- One requirement document per approved slice
- One index entry for every document
- Each document's concrete edge, boundary, alternate, and failure decisions
- Given–When–Then acceptance criteria with a deterministic Verification Method for every in-scope case

Default paths, unless the target repository has another convention:

```text
spec/index.md
spec/<epic>/index.md
spec/<epic>/<slice>.md
```

Follow `../references/spec-convention.md`, `../references/document-style.md`, `../references/document-style/frontmatter.md`, and `template/spec.md`. Add the required metadata to Story documents and update both indexes with the same change. Do not create a combined `requirements.md` file when the repository uses the Story layout.

## Boundaries

This skill defines **what** must be true. It does not:

- design Objects, classes, APIs, schemas, or infrastructure;
- choose libraries or implementation mechanisms;
- write production code or feature tests;
- pull deferred topics into a slice;
- invent every hypothetical failure.

Those belong to `/skill:ood`, `/skill:tdd`, and `/skill:to-plan`.

## Workflow

### 1. Establish the slice inventory

1. Read the prototype verdict, trial results, context, current spec indexes, relevant repository code/tests, and target conventions.
2. If the caller supplied an inventory, validate it. If not, use `../references/top-down-decompose.md` to derive candidate behaviors from the product goal.
3. For every candidate, write one line for the actor, trigger, observable outcome, execution boundary, dependency, and proposed slug.
4. Split overlapping candidates and expose gaps. Mark each candidate `accepted`, `not yet specified`, `out of scope`, or `blocked by [unknown]`.
5. Order accepted slices by dependency and user value.

If an unresolved decision changes the observable behavior, ask only the blocking questions needed to settle it. Batch up to three questions, use `../references/question-format.md`, and state a recommended answer. If the answer can only be learned by running something, use `/skill:experiment` instead of guessing.

**Completion criterion:** every accepted candidate has one actor, trigger, outcome, boundary, and slug; candidates do not overlap; gaps and blockers are explicit; and the inventory has an approved order.

### 2. Define each slice and its edge cases

For every accepted slice, create a requirement card from the prototype, context, repository evidence, and confirmed inventory. Keep decisions behavior-focused.

```markdown
## Slice
- ID/slug: [stable identifier]
- Category: [feature | fix | refactor | other]
- Actor/system: [who or what uses it]
- Trigger/context: [what starts it]
- Purpose: [one outcome]

## Scope
- In scope: [smallest useful behavior]
- Out of scope: [nearby behavior intentionally excluded]
- Deferred topics: [topic + condition that would reopen it]

## Requirement
When [trigger], [actor/system] shall [action] so that [observable outcome].

## Preconditions and dependencies
- [only state/data/dependency required to define or verify this slice]

## Edge cases
| Case | Concrete trigger | Scope | Decision | Verification |
|---|---|---|---|---|
| [case] | [input/state/call sequence] | in/out/deferred | [observable behavior or condition] | [test/check] |

## Acceptance criteria
| Category | Given | When | Then | Verification |
|---|---|---|---|---|
| Normal | ... | ... | ... | ... |
| Boundary/exception | ... | ... | ... | ... |

## First executable action
[one safe, reversible action and expected result]
```

Use a concrete trigger for every edge case. Include only cases that affect this slice's outcome or safe execution. A relevant edge case must appear in both the card and its acceptance criteria or be explicitly deferred with a condition.

**Completion criterion:** every accepted slice has a complete card with a happy path, concrete relevant edge/boundary/failure cases, exclusions, dependencies, and testable acceptance criteria. No design decision is hidden in the card.

### 3. Validate the batch

Check the whole set before writing:

- every product-goal outcome belongs to exactly one accepted slice or is explicitly out of scope/deferred;
- every slice has one coherent boundary and can be implemented independently in its listed order;
- acceptance criteria are SMART and Given–When–Then per `../references/requirement-engineering.md`;
- every Verification Method names an integration test, E2E test, query, or genuinely manual check with an observable result, per `../references/deterministic-evaluation.md`;
- no acceptance criterion chooses a class, API, library, database shape, or other implementation detail;
- the prototype's known states and trial findings are reflected or explicitly rejected.

If validation exposes a behavior change, update only the affected card and recheck its neighboring slice boundaries. Do not silently widen the batch.

**Completion criterion:** the inventory and every card pass the whole-batch check, with no unclassified overlap, missing outcome, or undecided in-scope behavior.

### 4. Approve and write every document

Before writing, show the human:

- the final inventory and order;
- one compact summary per slice;
- the exact requirement path for every slice;
- the unresolved assumptions and deferred topics.

Ask one batch approval question using `../references/question-format.md`:

> Do you approve these requirement slices and paths, or should I change anything before writing them?

Do not write the documents until the human confirms. If the human changes one slice, update its card and the inventory, then ask for approval again. After approval:

1. Write one Story document at `spec/<epic>/<slice>.md` for every accepted slice.
2. Preserve the card's edge-case table and acceptance criteria in the Story's `Spec` and `AC` sections.
3. Update `spec/<epic>/index.md` and `spec/index.md`; keep not-yet-specified and out-of-scope candidates visible where the convention supports them.
4. Link each requirement document to its prototype/context evidence and leave a placeholder for its later design and plan paths when the target convention permits it.

**Completion criterion:** all approved requirement files exist at their confirmed paths, every file contains its slice's edge cases and deterministic acceptance criteria, both indexes link to every file, and no unapproved file was written.

## Handoff

Pass the complete inventory and all written requirement paths to `/skill:ood`. OOD must process the same slices and must not reintroduce deferred topics or invent missing requirements.

## Completion criterion

This skill is complete only when one approved inventory exists, every accepted slice has exactly one requirement document, each document contains its happy path and concrete relevant edge cases, every in-scope behavior has a deterministic acceptance criterion, indexes are synchronized, and the human-approved scope is unchanged.
