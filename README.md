# SOPHIST Skills — Workflow Guide

SOPHIST is a V-model documentation system for software projects. The skills listed here guide you through the full pipeline from capturing customer intent to verified implementation.

---

## The V-Model Pipeline

```
CuRS (What customers want)
  └─► SRS (Testable requirements)       [sophist-srs reviews & cascades]
        └─► SAD (Architecture)           [sophist-sad reviews & cascades]
              └─► SDD (Detailed design)  [sophist-sdd reviews & finalizes]
                    └─► Code             [sophist-impl writes it]

Tests mirror the V:
  AT  ←── SRS
  SIT ←── SAD
  UT  ←── SDD
```

Each layer produces draft items with review points. You answer the review points inline; the review skill applies your answers and cascades to the next layer.

---

## Main Workflow

### 1. Initialize — `sophist-init`

Run once at the start of a project. Creates the `.sophist/` mdbook structure with all chapter directories, a tag registry, and index stubs. Also asks for the project goal.

If the project already has source code, it reverse-engineers a first draft of all layers (CuRS through UT) from the existing codebase.

```
init sophist
```

---

### 2. Set / Update Goal — `sophist-goal`

Records the project's stated purpose in `.sophist/src/goal.md`. All other skills read this file to stay oriented. Can be updated at any time.

```
sophist-goal
set the goal
```

---

### 3. Capture Requirements — `sophist-curs`

Two modes in one skill:

**Capture mode** — tell it what the customer wants. It:
- Checks for duplicate or overlapping existing items (NEW / ENHANCE / UPDATE / SKIP)
- Creates `CuRS-NNN` items capturing the customer's words
- Derives `SRS-NNN` requirements (testable, traceable)
- Creates `AT-NNN` acceptance tests
- Flags if a Debugger CuRS is missing

**Review mode** — after answering review points inline in the CuRS files. It:
- Applies your inline answers into the item files
- Marks answered CuRS items `reviewed`
- Updates linked SRS items if CuRS content changed

```
sophist-curs
I have a new requirement: <describe what the customer wants>
review CuRS
I answered the CuRS items
```

---

### 4. Review SRS → Architecture — `sophist-srs`

Call it with no arguments to see all pending SRS review points. Call it after answering them inline to:
- Apply your answers into the item files
- Mark answered items `reviewed`
- Create `SAD-NNN` architecture components and `SIT-NNN` integration tests
- Update `AT-NNN` items if SRS content changed

After it runs, open the draft SAD files, answer the review points, then run `sophist-sad`.

```
sophist-srs
review SRS
I answered the SRS items
```

---

### 5. Review SAD → Detailed Design — `sophist-sad`

Same pattern as above, one layer down. After answering SAD review points, it:
- Marks SAD items `reviewed`
- Creates `SDD-NNN` detailed design items (one per function/class) and `UT-NNN` unit tests
- Updates `SIT-NNN` items if component interfaces changed

After it runs, open the draft SDD files, answer the review points, then run `sophist-sdd`.

```
sophist-sad
review SAD
I answered the SAD items
```

---

### 6. Review SDD → Ready to Implement — `sophist-sdd`

Final review layer. After answering SDD review points, it:
- Marks SDD items `reviewed`
- Updates `UT-NNN` items to match any revised algorithms or signatures

When all SDD items under a reviewed SAD are `reviewed`, the design is ready for implementation.

```
sophist-sdd
review SDD
I answered the SDD items
```

---

### 7. Implement — `sophist-impl`

Writes source code from reviewed SDD items. Reads the full upstream chain (SDD → SAD → SRS → CuRS) to understand intent, and instruments the code with debug log calls following the Debugger component spec. When something in the spec is unclear, it writes a review point rather than guessing.

```
sophist-impl
implement SDD-010
implement SAD-003
implement everything ready
```

---

### 8. Code Review — `sophist-codereview`

Two modes:

- **Spec → Code**: you implemented from the spec — AI verifies conformance, marks items `done`
- **Code → Spec**: you edited source directly — AI detects divergences, updates spec where code is right, flags where code is wrong

```
sophist-codereview
I finished implementing SDD-010
I edited the code directly
sync the docs with my changes
```

---

## Shortcut Skills

### `sophist-lazy` — Full pipeline in one pass

Writes CuRS → SRS → SAD → SDD without stopping for review. Every unresolved point gets an explicit "lazy assumption" logged to `.sophist/src/lazy-log.md` and an observability spec so you can detect wrong assumptions at runtime.

Use when speed matters more than design certainty.

```
sophist-lazy
push this through the full pipeline
just run the whole pipeline
```

---

### `sophist-fast` — Quick fix or prototype

Two modes:
- **Fix**: small correction to docs or code (rename, typo, broken link)
- **Prototype**: rough working implementation of an item to test an approach before committing

```
sophist-fast
fix the title of SRS-007
prototype SDD-010
spike this approach
```

---

## Utility Skills

| Skill | What it does |
|-------|-------------|
| `sophist-overview` | Generates a concise bird's-eye summary of all items and their states |
| `sophist-refact` | Finds refactoring opportunities grounded in Deep Module philosophy |
| `sophist-debug` | Debugs a failing run using log files written to the debug directory |
| `sophist-sync` | Syncs existing `.sophist` documents to the current skill templates (run after skill updates) |

---

## Item States

Every item moves through these states:

```
draft → reviewed → done
```

- **draft**: created, has review points to answer
- **reviewed**: all review points resolved; ready for the next layer or implementation
- **done**: implemented and verified (SDD/UT only, set by sophist-codereview)

---

## Full Example Flow

```
1. init sophist                          # sophist-init: set up book + goal
2. I have a new requirement: users       # sophist-curs: CuRS/SRS/AT created (draft)
   should be able to reset their password
3. [answer review points in SRS files]
4. sophist-srs                           # applies answers, creates SAD/SIT (draft)
5. [answer review points in SAD files]
6. sophist-sad                           # applies answers, creates SDD/UT (draft)
7. [answer review points in SDD files]
8. sophist-sdd                           # finalizes design, all reviewed
9. implement SDD-010                     # sophist-impl: writes code
10. I finished implementing SDD-010      # sophist-codereview: marks done
```
