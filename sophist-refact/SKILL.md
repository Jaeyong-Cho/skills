---
name: sophist-refact
description: |
  SOPHIST refactoring skill. Use this to find and apply refactoring opportunities grounded in the Deep Module philosophy (Ousterhout): simplify interfaces, deepen implementations, eliminate leakage. Reads source code, SDD, and SAD to find shallow or leaky spots, ranks candidates by low outgoing/incoming dependency count so the blast radius stays small, then updates SOPHIST items (SDD → SAD → SRS → UT) to reflect the improved design. Never touches CuRS — customer requirements are unchanged by internal restructuring.
  Triggers: "sophist-refact", "find refactoring points", "refactor the code", "where should I refactor", "deep module refactoring", "find shallow modules", "clean up the design", "simplify the interface", "find leaky abstractions", "improve the architecture", "I've written this three times now", "Rule of Three", "I keep repeating this pattern", "clean up before adding a feature", "refactor while fixing a bug", "tidy up during code review", "this code is a mess", "let me clean this up first".
  Use this instead of sophist-impl when the goal is improving existing structure rather than writing new functionality.
---

# sophist-refact: Find and Apply Deep Module Refactoring

**Goal**: Locate the biggest design debts in the codebase using the Deep Module lens, prioritise them by blast radius (fewest dependents first), propose a small focused set to the human, and update SOPHIST items to reflect the improved design.

The guiding principle: a module is good when its interface is simpler than its implementation. Every refactoring here is in service of that ratio.

If `.sophist/src/goal.md` exists, read it — it clarifies the project's priorities and helps distinguish design debt that matters from debt that doesn't.

---

## When to Refactor

Use this skill whenever any of these signals appear:

### Rule of Three
- **First time**: just get it done.
- **Second time**: do the same thing, note the duplication.
- **Third time**: stop and refactor. The pattern is real; the cost of repetition now exceeds the cost of abstraction.

### Before adding a feature
Refactoring first makes the new feature easier to land cleanly. If the area you're about to change is messy, clean it before writing new code — the cost of reading and understanding dirty code compounds across every future touch. Refactoring also builds familiarity with unfamiliar code you've inherited.

### While fixing a bug
Bugs concentrate in the dirtiest corners of the codebase. If a bug leads you to a convoluted module, refactor it as you fix — clean code makes the error visible. Don't just patch the symptom and leave the mess.

### During a code review
Code review is the last chance to improve structure before the code becomes load-bearing. If you're reviewing a PR and see a refactoring opportunity, raise it here. Pair with the author for simple changes; flag the harder ones for a dedicated pass.

In all three cases, refactoring must update SOPHIST documents to stay in sync — see Step 5 below.

---

## Step 1: Build the dependency picture

Read the SAD index to get the list of components and their declared interfaces:

```bash
cat .sophist/src/sad/index.md
```

Then map what calls what by scanning the source tree:

```bash
# Find import/require relationships
grep -rn "^import\|^from\|^require\|^use " src/ | sort

# Find which source files reference which SAD component locations
# (use the Location fields from SAD items as anchors)
```

Build a rough dependency table:

```
Component      | Depends on          | Depended on by
SAD-001 auth   | SAD-003 db          | SAD-005 api
SAD-002 config | (none)              | SAD-001, SAD-003, SAD-005
SAD-003 db     | SAD-002 config      | SAD-001, SAD-004
...
```

You don't need this to be perfect — good enough to rank candidates by how many things depend on them.

---

## Step 2: Score each component for design debt

For each SAD component (and its child SDD items), look for these Deep Module anti-patterns:

| Anti-pattern | What to look for |
|---|---|
| **Shallow module** | Interface is nearly as wide as the implementation — many small methods each doing one trivial thing, often getter/setter-heavy classes |
| **Information leakage** | The same knowledge appears in two or more places — same config key, same format string, same validation rule duplicated across modules |
| **Temporal decomposition** | Split by execution order rather than by responsibility — `ParseX`, `ProcessX`, `OutputX` as separate classes when they all exist only to handle X |
| **Pass-through method** | A function whose entire body is calling another function with the same arguments — no value added |
| **Conjoined twins** | Two components always edited together, suggesting they should be one |
| **Leaky interface** | Callers need to know internal details to use the module correctly (ordering constraints, magic values, init sequences) |

Score each component 0–3 (0 = clean, 3 = serious debt) on each dimension. You don't need to be precise — the ranking matters more than the scores.

---

## Step 3: Rank candidates by complexity and blast radius

**Primary sort: highest debt score first** — the goal is to find the components that most need simplification, regardless of how many things depend on them. A deeply broken component with many callers is exactly the kind of place where a refactor pays off most — callers suffer every day it stays broken.

**Secondary sort: fewest inbound dependencies** — when two candidates have similar debt scores, prefer the one with fewer callers. This reduces the ripple risk and keeps the first refactoring self-contained.

Show the blast radius clearly for each candidate so the human can make an informed tradeoff. A high-debt component with many dependents is worth listing even if it means a larger change — the human may choose to take it on anyway.

Present the top 3 candidates:

```
## Refactoring Candidates

### 1. SAD-003 DbAdapter  (debt score: 8/9, 3 inbound deps)
- Temporal decomposition: connect(), query(), disconnect() are always called in sequence by every caller.
- Leaky interface: callers must manage connection lifecycle manually — internal state leaks through the API.
- Proposed direction: a single `withConnection(fn)` context manager hides the sequence and lifecycle inside.
- Blast radius: 3 components need call-site updates if the interface changes.

### 2. SAD-002 ConfigLoader  (debt score: 7/9, 0 inbound deps)
- Shallow: 14 getter methods, each one line. Callers must know which key to ask for.
- Leaky interface: callers pass raw string keys — config schema knowledge is spread across 6 call sites.
- Proposed direction: collapse getters into one `get(key)` and push validation inside.
- Blast radius: 0 — safe to change without touching any other component.

### 3. SAD-001 AuthService  (debt score: 5/9, 2 inbound deps)
- Pass-through: AuthService.validate() calls TokenValidator.validate() verbatim.
- Proposed direction: absorb TokenValidator into AuthService; callers don't need to know it exists.
- Blast radius: 2 components affected if the interface narrows.
```

Ask the human: "Which of these would you like to tackle first? I'll start with #1 — it has the worst design debt — unless the blast radius makes you prefer #2 which is self-contained."

---

## Step 4: Plan the refactoring

For the chosen candidate, define exactly what changes:

- **Interface delta**: which methods/functions disappear, which are added, which signatures change
- **Behavior preservation**: what observable behavior must stay identical (this constrains the refactor)
- **Affected SDD items**: list every SDD item whose Signature, Algorithm, or Variables will change
- **Affected SAD items**: does the component boundary change? Does the Location field change?
- **Affected UT items**: which tests break because signatures changed? Which new tests are needed to cover the deeper behavior now visible?

Write this plan out before touching any files. The plan is a contract — the human can stop you here if the scope is wrong.

---

## Step 5: Update SOPHIST items

Work top-down: SAD before SDD, SDD before UT. Never touch CuRS.

### 5a: Update SAD

If the component's Interface or Location changes, update the SAD item:

- Change the `## Interface` section to reflect the new surface
- Add a `> **Review needed**` note if the interface change affects callers outside this component (i.e., it touches another SAD component's SDD items)
- If the refactoring splits one component into two, create a new SAD item using the SAD template from `../sophist-shared/items.md`
- If it merges two components into one, mark the absorbed component `deprecated` and note the replacement in its header

Keep the SAD item in `reviewed` state only if the changes are internal (no interface change visible to callers). Otherwise set it back to `draft` so it goes through the review cycle.

### 5b: Update SDD items

For each SDD item affected:

- Rewrite the `## Signature` to match the new interface
- Update `## Algorithm` steps that change — keep the steps numbered and concrete
- Update `## Variables` if names or types change
- Add or remove `## Error cases` to match the new contract
- If the refactoring absorbs a function, mark the removed SDD item `deprecated` in its state line and add: `> Absorbed into [SDD-NNN] as part of deep module refactoring.`
- If new functions are introduced, create new SDD items from the template

Set changed SDD items to `draft` — they need a review pass before re-implementation.

### 5c: Update SRS (only if public contract changes)

SRS items describe behavior visible to users or other systems. If the refactoring changes nothing observable (pure internal restructuring), skip this step entirely.

If the refactoring does change an observable contract (e.g., an error message, a response shape, an event name), locate the relevant SRS item and add a review point:

```markdown
### Review needed
Interface refactoring in SAD-002 changes how config errors surface to callers. Confirm whether the error type change in SDD-015 aligns with SRS-007's error behavior specification.
```

Do not update SRS content directly — the human must confirm the intent before the spec changes.

### 5d: Update UT items

For each UT item linked to a changed SDD:

- Update `## Input` and `## Expected output` to match the new signature
- If a test can no longer exist (because the function was absorbed), mark it `deprecated`
- If the deeper implementation now has testable logic that was previously hidden behind a pass-through, create new UT items for those cases

Keep UT items in `draft` — the human writes the assertions.

---

## Step 6: Update indexes and tags

```bash
# Update relevant index files
.sophist/src/sad/index.md     — state changes, new/deprecated components
.sophist/src/sdd/index.md     — state changes, new/deprecated items
.sophist/src/ut/index.md      — new or deprecated UT items
.sophist/src/tags.md          — any new tags (e.g. `refactor`, `deprecated`)
.sophist/src/SUMMARY.md       — new files need entries
```

---

## Step 7: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -20
```

Fix broken links before reporting.

---

## Step 8: Report

```
## Refactoring Report

### Candidate chosen
SAD-002 ConfigLoader — shallow interface, 0 inbound dependencies

### Design intent
[One paragraph explaining the Deep Module improvement: what interface shrank,
what behavior moved inside, and why callers are better off not knowing it.]

### SOPHIST items updated
| Item | Change |
|------|--------|
| SAD-002 | Interface collapsed from 14 getters to get(key) + validate() |
| SDD-015 | Signature updated; algorithm extended with internal key validation |
| SDD-016 | Marked deprecated — absorbed into SDD-015 |
| UT-015 | Input/output updated to match new signature |
| UT-020 | New — tests config validation that was previously spread across callers |

### Items set back to draft (need sophist-sdd before re-implementation)
| Item | Reason |
|------|--------|
| SDD-015 | Algorithm changed — needs review before implement |

### SRS review points added (if any)
| SRS | Question |
|-----|---------|
| SRS-007 | Confirm error surface change is acceptable |

### What to do next
1. Answer any SDD review points inline, then run **sophist-sdd** to finalize
2. Run **sophist-impl** for items back in `draft` once reviewed
3. Run **sophist-codereview** when implementation is done
4. When ready, move to the next candidate: SAD-003 DbAdapter
```

---

## Debug output

If the skill was invoked with `--debug-level=VERBOSE`, write a debug session. Create the output directory from `--debug-output-dir` (default: `.sophist/debug/`):

```bash
mkdir -p <value of --debug-output-dir, or .sophist/debug>
```

Create a timestamped directory inside it (e.g. `20240115-143022-refact/`) and write:

| File | Contents |
|------|----------|
| `00-candidates.md` | All scored candidates — component, dependency count, debt score per anti-pattern, and ranking rationale |
| `01-plan.md` | The chosen candidate's refactoring plan — interface delta, behavior preservation constraints, and all affected items |
| `02-changes.md` | Each SOPHIST item updated — what field changed, old value, new value, and new state |

---

## Constraints

- **One candidate at a time.** Do not update items for multiple refactoring candidates in the same pass. Keeping the diff small makes review tractable.
- **Never touch CuRS.** Customer requirements are not altered by internal restructuring.
- **Preserve observable behavior.** If a refactoring would change what an SRS item says about user-visible behavior, add a review point — don't silently alter the spec.
- **Prefer fewer, deeper modules over many shallow ones.** If two candidates could be merged, that merge is usually better than polishing each one separately.
- **Set items back to draft honestly.** It is tempting to leave items as `reviewed` after editing them. Don't. If the algorithm changed, it needs another review pass.
