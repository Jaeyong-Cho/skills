---
name: sophist-lazy
description: |
  SOPHIST lazy pipeline skill. Use this when the human has a new requirement and wants the full V-model chain (CuRS → SRS → SAD → SDD) written in one uninterrupted pass — without stopping for review at each stage. Every unresolved review point gets a "lazy assumption" (explicit best-guess decision) plus a runtime guard (assert, log, monitor, or must-review panic) so that assumptions which were never validated by a human will surface when the software runs. All assumptions are also collected into book/src/lazy-log.md for later triage.
  Triggers: "sophist-lazy", "push this through the full pipeline", "draft the full chain for this requirement", "lazy pipeline", "one-shot from requirement to SDD", "quick design pass", "draft everything end to end", "just run the whole pipeline", "don't stop for review", "full V-model from this requirement".
  Use this when speed matters more than design certainty, and when you're willing to have the gaps flagged at runtime rather than at review time.
---

# sophist-lazy: Full Pipeline — Requirement to SDD in One Pass

**Goal**: Take a customer requirement and produce a complete CuRS → SRS → SAD → SDD chain without pausing for human review. Every time a review point would normally block forward progress, make an explicit lazy assumption instead, attach a runtime guard to the relevant SDD item, and log the assumption. The human reviews *lazy-log.md* after the fact rather than inline during the pipeline.

The guiding principle: what isn't reviewed at design time must be *observable* at runtime. A lazy assumption that turns out to be wrong should produce a clear, traceable signal — not a silent mismatch.

---

## Step 0: Get the requirement

If the human has not provided a requirement, ask:

> "What does the customer need? Describe it in plain terms — I'll handle the translation into SOPHIST items."

Accept any form: a sentence, a paragraph, a user story, a feature name. The only requirement is enough to work with.

---

## Step 1: CuRS pass

### 1a. Check for existing coverage

Search for related existing CuRS items before creating new ones:

```bash
ls book/src/curs/ | grep "^CuRS-" | sort -t- -k2 -n | tail -1   # next ID
grep -ril "<keyword>" book/src/curs/ book/src/srs/                # similarity
```

If a full duplicate exists, stop and tell the human — there is nothing to do. If partial overlap, note it but continue creating the new chain (don't stall).

### 1b. Create the CuRS item

Create `book/src/curs/CuRS-{NNN}.md` — record the customer's words accurately, do not over-interpret:

```markdown
# CuRS-{NNN}: <short title>

## State
`draft`

## Tags
`#lazy`

## Why
<one sentence — business motivation>

## Traces
- → [SRS-{NNN}](../srs/SRS-{NNN}.md): <aspect being formalized>

## Input
> "<customer's words verbatim or near-verbatim>"

## Context
<when stated and any relevant background>

> **Review needed** — confirm this captures the customer's intent accurately
>
> **Lazy assumption**: taken at face value — no alternative interpretation attempted
> **Guard type**: `log`
```

Mark state `draft` and tag `#lazy`. Add a row to `book/src/curs/index.md` and an entry to `SUMMARY.md`.

---

## Step 2: SRS pass

Derive one or more SRS items from the CuRS item. Each SRS item must be testable — if you can't imagine an AT for it, split or reframe it.

Create `book/src/srs/SRS-{NNN}.md`:

```markdown
# SRS-{NNN}: <requirement title>

## State
`draft`

## Tags
`#lazy`

## Why
<one sentence — why this requirement exists>

## Traces
- ← [CuRS-{NNN}](../curs/CuRS-{NNN}.md): <derivation rationale>
- → [AT-{NNN}](../at/AT-{NNN}.md): <what the acceptance test validates>

## Description
<Requirement text — "shall" for mandatory, "should" for preferred.>
```

### SRS review point handling

For each ambiguity you encounter — scope, performance constraint, actor identity, error behavior, or interface contract — apply the lazy assumption protocol:

1. Write the original review point as normal
2. Immediately below it, write your assumption and assign a guard level

```markdown
> **Review needed** — <original question>
>
> **Lazy assumption**: <what was assumed and why — one sentence>
> **Guard level**: `assert` | `log` | `monitor` | `must-review`
```

**Guard level guide**:

| Level | When to use | What it generates in code |
|---|---|---|
| `must-review` | Security, auth, data integrity — wrong assumption causes harm | Startup panic / `raise` at module load |
| `assert` | Functional invariant — wrong assumption causes incorrect behavior | `assert <condition>, "LAZY-[ID]: ..."` at the call site |
| `log` | Soft assumption — wrong assumption degrades quality but doesn't break | `logger.warning("LAZY-[ID]: ...")` on first use |
| `monitor` | Scale or performance assumption | Metric emission; counter or histogram |

Add to lazy log (see Step 5) for every review point handled here.

Create the AT item as well (`book/src/at/AT-{NNN}.md`). The AT represents the intended behavior even if some design details are lazy — keep it honest about what the system should *do*, not how it should work internally.

---

## Step 3: SAD pass

Derive SAD component(s) from SRS items. Follow the standard SAD item format, but do not stop for review — apply the lazy assumption protocol to every open question.

Create `book/src/sad/SAD-{NNN}.md`:

```markdown
# SAD-{NNN}: <component title>

## State
`draft`

## Tags
`#lazy`

## Why
<one sentence — what this component's existence solves>

## Traces
- ← [SRS-{NNN}](../srs/SRS-{NNN}.md): <responsibility derivation>
- → [SDD-{NNN}](../sdd/SDD-{NNN}.md): <function to be designed>

## Responsibility
<What this component owns — one paragraph. Prefer deep modules: hide decisions inside,
expose only what callers need to know.>

## Interface
<Public API surface — function names, inputs, outputs, errors raised>

## Location
`src/<path>/<filename>`

## Dependencies
- [SAD-{MMM}](SAD-{MMM}.md): <why this dependency exists>
```

Apply the lazy assumption protocol for every review point (technology choice, component boundary, interface shape, etc.).

---

## Step 4: SDD pass

Derive SDD items from each SAD component. This is where runtime guards are generated. Every lazy assumption from steps 2–3 that affects function behavior must appear in `## Lazy guards` of the relevant SDD item.

Create `book/src/sdd/SDD-{NNN}.md`:

```markdown
# SDD-{NNN}: <function title>

## State
`draft`

## Tags
`#lazy`

## Why
<one sentence>

## Traces
- ← [SAD-{NNN}](../sad/SAD-{NNN}.md): <component this belongs to>
- → [UT-{NNN}](../ut/UT-{NNN}.md): <test coverage>

## Signature
<function_name(param: Type, ...) -> ReturnType>

## Algorithm
1. <step>
2. <step>
...

## Variables
| Name | Type | Purpose |
|------|------|---------|

## Error cases
| Condition | Behavior |
|-----------|----------|

## Side effects
<none | list>

## Lazy guards
<Guards that sophist-impl must emit for unreviewed assumptions.
One line per assumption, in the form the implementation should produce.>
```

### How to write lazy guards

Each guard corresponds to a lazy assumption from any upstream item (CuRS, SRS, or SAD). Pull them all into the SDD that implements the affected logic. Format them as concrete code-level expressions — the implementing agent copies these verbatim:

```markdown
## Lazy guards
- `assert isinstance(user_id, str) and len(user_id) > 0, "LAZY-SRS-007: assumed non-empty string user_id — review input format"`
- `logger.warning("LAZY-SAD-003: single-database assumption — multi-tenant not validated")  # emit once at startup`
- `assert config.get("max_retries") is not None, "LAZY-SDD-010: assumed max_retries always set in config"`
```

Guard syntax by language:

| Language | assert | log | monitor | must-review |
|---|---|---|---|---|
| Python | `assert <cond>, "LAZY-..."` | `logger.warning("LAZY-...")` | `metrics.increment("lazy.<id>")` | `raise AssertionError("LAZY-...")` at import |
| TypeScript | `if (!<cond>) throw new Error("LAZY-...")` | `console.warn("LAZY-...")` | `metrics.count("lazy.<id>")` | top-level `throw` |
| Go | `if !<cond> { panic("LAZY-...") }` | `log.Warn("LAZY-...")` | `metrics.Inc("lazy.<id>")` | `func init() { panic(...) }` |

Apply the lazy assumption protocol for any new review points that emerge at SDD level too.

Create UT items (`book/src/ut/UT-{NNN}.md`) for each SDD item. UT items are left `draft` with empty assertion bodies — the human writes those after review.

---

## Step 5: Write the lazy log

Create or update `book/src/lazy-log.md`. This is the human's triage sheet — one row per lazy assumption across the entire pipeline run.

```markdown
# Lazy Log

Items marked `#lazy` have unreviewed assumptions. Each row below traces an assumption
to its source item, the decision made, the guard level, and the guard that will be
emitted in code. Review and replace with a real design decision when you have time.

| ID | Item | Assumption | Guard level | Guard expression | Status |
|----|------|-----------|-------------|-----------------|--------|
| L-001 | SRS-007 | user_id is always a non-empty string | assert | `assert isinstance(user_id, str)...` | ⬜ open |
| L-002 | SAD-003 | single database, no replica reads | log | `logger.warning("LAZY-SAD-003...")` | ⬜ open |
| L-003 | SDD-010 | max_retries always set in config | assert | `assert config.get(...) is not None...` | ⬜ open |
```

Status column: `⬜ open` until the human reviews and replaces the assumption; `✅ resolved` when a proper review point is answered and the lazy tag removed.

Add `book/src/lazy-log.md` to `SUMMARY.md` if not already there.

---

## Step 6: Update indexes and build

Update `index.md` for each document type touched (CuRS, SRS, AT, SAD, SDD, UT), `book/src/tags.md` for the `#lazy` tag, and `SUMMARY.md` for all new files.

```bash
cd book && mdbook build 2>&1 | tail -20
```

Fix broken links before reporting.

---

## Step 7: Report

```
## Lazy Pipeline Complete

### Items created
| ID | Title | Type | Lazy assumptions |
|----|-------|------|-----------------|
| CuRS-003 | ... | CuRS | 1 |
| SRS-007  | ... | SRS  | 2 |
| AT-007   | ... | AT   | 0 |
| SAD-005  | ... | SAD  | 1 |
| SDD-012  | ... | SDD  | 3 (guards written) |
| UT-012   | ... | UT   | stub only |

### Lazy log summary
N assumptions logged in book/src/lazy-log.md

| Guard level | Count |
|---|---|
| must-review | N |
| assert      | N |
| log         | N |
| monitor     | N |

### ⚠ Must-review items (address before deploying)
These assumptions affect security, auth, or data integrity.
Running the code without resolving them will panic at startup.

- L-00X (SRS-00X): <assumption text>

### Next steps
- Open **book/src/lazy-log.md** and work through `⬜ open` rows
- For each resolved assumption: remove the lazy blockquote from the item, clear the `#lazy` tag, mark `✅ resolved` in the log
- Run **sophist-srs**, **sophist-sad**, **sophist-sdd** in sequence to promote items through proper review
- Run **sophist-impl** to generate code — lazy guards will be emitted automatically from `## Lazy guards` sections
```

---

## Commit message

After all file writes are complete, propose a commit message:

```
docs(lazy): <short description of the requirement under 72 chars>

Why: <the customer need that triggered this pipeline run>
What: <which CuRS/SRS/SAD/SDD items were created and how many lazy assumptions remain>
Lazy: N assumptions logged — M must-review
```

---

## Constraints

- **Never block for review.** If a decision is needed, make the lazy assumption and move on.
- **Never skip a guard.** Every review point must produce a guard entry in both the relevant SDD's `## Lazy guards` and in `lazy-log.md`. Invisible assumptions are the most dangerous kind.
- **must-review assumptions must panic at startup**, not silently pass. A wrong security assumption caught at first boot is far better than a wrong assumption caught in production.
- **Keep CuRS honest.** Record the customer's actual words. Lazy assumptions belong in SRS and below — CuRS is the contract, not the interpretation.
- **Deep module principle still applies.** Even lazy SAD components should aim to hide complexity. A lazy interface that leaks internal details just moves the review debt to every call site.
