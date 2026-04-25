# SOPHIST Workflow Reference

## Pipeline Order

Each layer is created as `draft`, reviewed inline by the human, then promoted to `reviewed` by running the corresponding review skill. Reviews cascade to the next layer.

```
sophist-init       Create .sophist/ book, capture goal
    ↓
sophist-curs       Customer input → CuRS + SRS + AT (draft)
    ↓ [human answers ### Review needed in CuRS files]
sophist-curs       Apply CuRS answers → CuRS marked reviewed, SRS updated
    ↓ [human answers ### Review needed in SRS files]
sophist-srs        Apply SRS answers → SRS marked reviewed, cascade → SAD + SIT (draft)
    ↓ [human answers ### Review needed in SAD files]
sophist-sad        Apply SAD answers → SAD marked reviewed, cascade → SDD + UT (draft)
    ↓ [human answers ### Review needed in SDD files]
sophist-sdd        Apply SDD answers → SDD marked reviewed
    ↓
sophist-impl       Write code from reviewed SDD items
    ↓
sophist-codereview Verify code against spec, mark items done
```

## Item State Flow

```
draft  →  reviewed  →  done
```

- `draft`: AI created this; human must review it
- `reviewed`: human confirmed it; downstream cascade can proceed
- `done`: code implemented and verified

## Layer Traceability

| Layer | Derived from | Tested by |
|-------|-------------|-----------|
| CuRS  | (customer)  | —         |
| SRS   | CuRS        | AT        |
| SAD   | SRS         | SIT       |
| SDD   | SAD         | UT        |

## Shortcuts and Utilities

| Skill | When to use |
|-------|-------------|
| sophist-lazy | Need the full chain (CuRS → SDD) in one pass without review stops |
| sophist-fast | Small known fix (typo, rename, broken link) or throwaway prototype |
| sophist-codereview | Verify implementation against spec (Spec→Code) or sync docs to code edits (Code→Spec) |
| sophist-overview | Bird's-eye summary of all items and their states |
| sophist-refact | Find refactoring opportunities grounded in Deep Module philosophy |
| sophist-debug | Root-cause analysis from debug output files |
| sophist-sync | Sync existing items to updated skill templates |
| sophist-goal | Set or update `.sophist/src/goal.md` |

## Review Point Convention

Review points use a `### Review needed` heading at the end of the item body:

```markdown
### Review needed
<question or assumption to verify>
```

To answer: add `#### Answer` one level deeper, then run the review skill:

```markdown
### Review needed
<question>

#### Answer
<your answer>
```

Or delete the entire `### Review needed` block to accept the item as-is.
