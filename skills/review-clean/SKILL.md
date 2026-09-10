---
name: review-clean
description: Review whether a change leaves the code simpler, clearer, cohesive, and easier to change while preserving behavior. Use as the final cleanup and refactoring stage.
disable-model-invocation: true
license: MIT
---

# Clean and Refactoring Review

Review only whether the changed code can be made simpler, clearer, more cohesive, and safer to change without altering accepted behavior. This is the final cleanup stage. Do not reopen product intent, risk analysis, or test strategy unless a cleanup would invalidate accepted behavior or tests.

## Inputs

Accept any combination of:

- **Context:** a directory, file, repository snapshot, or surrounding implementation.
- **Changed code:** a diff, branch, commit, pull request, or current `HEAD`.
- **Result evidence:** logs, data, test output, or behavior that defines what must remain unchanged.

Inspect surrounding code only to understand duplication, ownership, cohesion, or structural consequences of the change.

## Review scope

Look for one of these connected cleanliness problems:

- **Unnecessary complexity:** duplicated knowledge, special-case branches, flags, thin wrappers, magic mechanisms, needless layers, oversized files, or complexity moved rather than removed.
- **Weak cohesion:** functions, classes, or modules combining unrelated responsibilities or state.
- **Unclear intent:** names, comments, or interfaces that make the code harder to understand or safely change.
- **Unsafe refactoring shape:** a structural change that does not preserve accepted behavior, makes future refinement harder, or leaves the code less maintainable.

Treat the thermo-nuclear standard as an escalation mode within this review: actively look for a behavior-preserving simplification that deletes concepts, branches, helpers, or layers. Do not demand abstraction for its own sake.

## Priority checks

- [ ] [Abstraction levels](../references/abstraction-levels.md) — keep each responsibility at the right level and prevent layer mixing.
- [ ] [Deep modules](../references/deep-modules.md) — prefer small interfaces that hide substantial implementation complexity.
- [ ] Complexity — delete duplicated knowledge, branches, flags, wrappers, and needless layers.
- [ ] Dependency direction — keep higher-level policy independent from lower-level mechanisms and concrete details.

## Review checklist

- [ ] [Functions](../references/clean-code/03-functions.md) — keep responsibilities small and focused.
- [ ] [Meaningful names](../references/clean-code/02-meaningful-names.md) — make intent and constraints obvious.
- [ ] [Comments](../references/clean-code/04-comments.md) — retain only comments that explain non-obvious constraints.
- [ ] [Objects and data structures](../references/clean-code/06-objects-and-data-structures.md) — keep data and behavior boundaries clear.
- [ ] [Classes](../references/clean-code/10-classes.md) — preserve cohesion and single responsibility.
- [ ] [Emergent design](../references/clean-code/12-emergence.md) — prefer simple structure that supports the current behavior.
- [ ] [Successive refinement](../references/clean-code/14-successive-refinement.md) — simplify in small, behavior-preserving steps.
- [ ] [Code-smell prompts](../references/clean-code/17-smells-and-heuristics.md) — look for deletable complexity and duplication.
- [ ] [Naming](../references/naming.md) — use names that reduce reader effort.
- [ ] [Architecture forces](../references/meta-pattern.md) — check that structure follows real constraints.

## Review process

1. Establish the behavior and constraints that must remain unchanged.
2. Compare the changed structure with the previous structure.
3. State the responsibility of each materially changed function, class, or module in one sentence.
4. Look for deletion before rearrangement: fewer branches, concepts, flags, helpers, layers, special cases, or files.
5. Check whether names and comments reveal meaning, side effects, and non-obvious constraints.
6. Check whether a refactor reduces the reader’s mental load rather than moving complexity elsewhere.
7. Check for a healthy decomposition boundary, especially when a change pushes a file beyond roughly 1,000 lines.
8. Rank cleanup findings by reader and maintenance impact, prioritizing simplifications that remove the most risk or complexity. Show the highest-impact target first.
9. Report one primary cleanup target at a time and prefer the smallest safe simplification.

Passing tests are evidence of behavior, not approval of structure. Do not flood the review with cosmetic preferences.

## Output

Return the review directly in the current session. Do not create or modify a review report file unless explicitly asked. Every finding must have a separate `Example` section using a fenced code block for real code, before/after structure, data, or an ASCII flow diagram.

```markdown
# Clean and Refactoring Review

## Verdict
[Clean enough | Cleanup target found | Refactoring risk found | Cannot determine]

## Evidence reviewed
- [context]
- [changed code]
- [result evidence]

## Findings
### [Blocker|High|Medium|Low] — [short title]
- **Location:** [file, symbol, or diff hunk]
- **Problem:** [complexity, cohesion, unclear intent, or unsafe refactoring shape]
- **Reason:** [why readers, maintainers, or future changes pay for it]

### Example

```text
[real code, before/after structure, data, or ASCII flow]
```

- **Recommended handling:** [delete, collapse, extract by meaning, rename, move responsibility, reuse an existing path, or simplify the model]
- **Behavior check:** [what must remain unchanged and how it is evidenced]

## Simplification opportunities
- [high-confidence deletion or restructuring, if any]
```

Do not approve merely because the implementation works when a clear, behavior-preserving simplification is visible.
