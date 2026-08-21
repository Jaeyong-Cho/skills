---
name: boy-scout
description: Understand the code changed in recent work — current branch's diff against its base, or since the last refactor commit, or a user-named target when given one — then scan it for one small opportunistic cleanup or code-review issue (bug, missed edge case, wrong behavior) worth flagging while the code is already open, and grill the user on whether/how to fix it. Report only, never edit. Invoke as /boy-scout.
disable-model-invocation: true
---

# Boy Scout

Leave the code cleaner than you found it, and catch what it got wrong along the way — scoped to what recent work already touched — not the whole repo (that's `/ponytail-audit`'s job) and not a fix pass (that's `/simplify`'s job).

## Purpose
Run this after implementation is done. Understanding the diff you just
wrote is the point — cleaning follows from that understanding, not from
pattern-matching the code cold.

## Find the patrol area
- User names a specific target (a function, file, or "this is hard to read"): scan exactly that, skip the diff entirely — the patrol area is the user's ask, not recent history. (Highest priority, only when given)
- User gives a `@skills/to-plan` plan file path: read its Target project field, work in that project, then patrol the changed area there per the branch/tag rules below — the plan file names *where*, not *what*, to scan. (Second priority, only when given)
- On the default branch: diff since the most recent commit whose subject matches `refactor`/`refact` (`git log --grep`); if none exists, diff since `HEAD~10`. (Third priority)
- On a non-default branch: diff against `git merge-base <default-branch> HEAD`. (Fourth priority)
- Given a tag or tag range (e.g. `/boy-scout v1.2.0..v1.3.0`): diff between those tags instead. (Fifth priority, only when asked)

State the base commit or tag range chosen before scanning — or, for a user-named target, state the file/function scanned instead of a base commit.

## Understand the change
List the patrol area first — the base commit/tag and every changed file, or the user-named file/function — then teach it back in three layers, ELI5 language: L0 — what it does and why (for a diff: what changed and why), 1-3 sentences; L1 — how it works, the mechanism tied to specific file/line; L2 — one concrete example, a sample input/call and its result. Skip this and the lens-scan below degrades to a blind pattern-match.

## Scan through seven lenses
For every file in the patrol area, check:
- Correctness — is the diff's behavior actually right? Per `../references/clean-code.md`'s ch07 (error handling) and `17-smells-and-heuristics.md` (G3 boundary/edge-case bugs, G21 algorithm misunderstood, G26 type/comparison imprecision), look for a missed edge case, wrong condition, silent failure path, or behavior the diff plainly gets wrong.
- Architecture fit — per `../references/meta-pattern.md`, decomposed along the wrong axis/level? Check line count against its Level-of-Pain table (~10/100/5k/100k lines) for size fit.
- Interface depth — per `../references/deep-modules.md`, a shallow module, leaky interface, or pass-through method touched by the change?
- Naming — per `../references/naming.md`'s Smells table, which apply and where
- Clean code — per `../references/clean-code.md`'s map, open only the chapter(s) matching what the diff touches
- Simplicity — `/ponytail-review`'s lens: reinvented stdlib, unneeded dependencies, speculative abstractions, dead flexibility, independent work serialized for no reason when it could just run in parallel.
- Ambitious restructuring — per `../references/thermo-nuclear-code-quality-review.md`: a "code judo" move that deletes whole branches/layers, a file crossing the 1k-line threshold, spaghetti/ad-hoc branching, or boundary/type sloppiness (casts, `any`, unjustified optionality).

Every changed file gets checked against all seven lenses before ranking.

## Priority
- Correctness first: a Correctness-lens finding outranks every style/refactor finding regardless of size — it's a defect, not a preference.
- Among the rest, high priority for high abstraction layer (`../references/meta-pattern.md`) close to clients, business logic. Make readable the business logic.
- Low priority for low abstraction layer far from clients, e.g. algorithm. Just consider their function's interface.

## Report, then grill
Lead with the 1-3 sentence understanding from above. Then rank candidates: any Correctness finding first, then the rest by size — smallest, most self-contained wins — and surface the single best finding, tidy or bug: small enough to do in passing, next to code already touched. One line per finding: location, lens, what's wrong and what to cut/change. List up to three only if they're close; say so plainly if nothing clears the bar.

**MUST REPORT** with example and ELI5

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark.
**MUST NOT** skip this reference for low-impact findings: every finding still gets marked with its impact level and uncertainty and shown, even when the Action rule says to skip asking it outright.

Run `@skills/grill-me` on the surfaced finding(s) to reach a shared decision on whether and how to fix or tidy — cover: value (what gets easier/safer/more correct after), the finding's own proof bar (a tidy proves behavior didn't change; a Correctness bug proves the wrong behavior is now right — state which), impact scope (every caller touched), and testability. Classify each of these four (value, proof bar, impact scope, testability) by impact level and uncertainty before asking: Low impact level → **do not ask** — state the auto-decided answer as a plain `Decision:` line and move on; only High impact ones become `❓` questions.

**MUST NOT** edit files or apply the fix during this skill. Once the grill settles, fix it by hand or via `@skills/to-plan` → `@skills/do-plan` — per `../references/workflow.md`, that plan resumes the feature/fix plan that led here and does not require another `/boy-scout` pass.
