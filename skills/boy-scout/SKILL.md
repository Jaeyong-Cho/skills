---
name: boy-scout
description: Understand the code changed in recent work — current branch's diff against its base, or since the last refactor commit — then scan it for one small opportunistic cleanup worth doing while the code is already open, and grill the user on whether/how to do it. Report only, never edit. Invoke as /boy-scout.
disable-model-invocation: true
---

# Boy Scout

Leave the code cleaner than you found it, scoped to what recent work already touched — not the whole repo (that's `/ponytail-audit`'s job) and not a fix pass (that's `/simplify`'s job).

## Purpose
Run this after implementation is done. Understanding the diff you just
wrote is the point — cleaning follows from that understanding, not from
pattern-matching the code cold.

## Find the patrol area
- On the default branch: diff since the most recent commit whose subject matches `refactor`/`refact` (`git log --grep`); if none exists, diff since `HEAD~10`. (First priority)
- On a non-default branch: diff against `git merge-base <default-branch> HEAD`. (Second priority)
- Given a tag or tag range (e.g. `/boy-scout v1.2.0..v1.3.0`): diff between those tags instead. (Third priority, only when asked)

State the base commit or tag range chosen before scanning.

## Understand the change
Read the diff and state in 1-3 sentences what it does and why. Skip this and the lens-scan below degrades to a blind pattern-match.

## Scan through five lenses
For every file in the diff, check:
- Architecture fit — per `../references/meta-pattern.md`, decomposed along the wrong axis/level? Check line count against its Level-of-Pain table (~10/100/5k/100k lines) for size fit.
- Interface depth — per `../references/deep-modules.md`, a shallow module, leaky interface, or pass-through method touched by the change?
- Naming — per `../references/naming.md`'s Smells table, which apply and where
- Clean code — per `../references/clean-code.md`'s map, open only the chapter(s) matching what the diff touches
- Simplicity — `/ponytail-review`'s lens: reinvented stdlib, unneeded dependencies, speculative abstractions, dead flexibility.

Every changed file gets checked against all five lenses before ranking.

## Priority
- High priority for high abstraction layer (`../references/meta-pattern.md`) close to clients, business logic. Make readable the business logic.
- Low priority for low abstraction layer far from clients, e.g. algorithm. Just consider their function's interface.

## Report, then grill
Lead with the 1-3 sentence understanding from above. Then rank candidates by size — smallest, most self-contained wins — and surface the single best boy-scout tidy: small enough to do in passing, next to code already touched. One line per finding: location, lens, what to cut/change. List up to three only if they're close; say so plainly if nothing clears the bar.

**MUST REPORT** with example and ELI5

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark.

Then run `@skills/grill-me` on the surfaced finding(s) to reach a shared decision on whether and how to tidy — cover: value (what gets easier/safer after), behavior preservation (what proves nothing changed), impact scope (every caller touched), and testability.

**MUST NOT** edit files or apply the fix during this skill. Once the grill settles, fix it by hand or via `@skills/to-plan` → `@skills/do-plan` — per `../references/workflow.md`, that plan resumes the feature/fix plan that led here and does not require another `/boy-scout` pass.
