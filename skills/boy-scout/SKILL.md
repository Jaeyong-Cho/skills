---
name: boy-scout
description: Understand the code changed in recent work — current branch's diff against its base, or since the last refactor commit — then scan it for one small opportunistic cleanup worth doing while the code is already open. Report only, never edit. Invoke as /boy-scout.
disable-model-invocation: false
---

# Boy Scout

Leave the code cleaner than you found it, scoped to what recent work already touched — not the whole repo (that's `/ponytail-audit`'s job) and not a fix pass (that's `/simplify`'s job).

## Find the patrol area
- On the default branch: diff since the most recent commit whose subject matches `refactor`/`refact` (`git log --grep`); if none exists, diff since `HEAD~10`. (First priority)
- On a non-default branch: diff against `git merge-base <default-branch> HEAD`. (Second priority)

State the base commit chosen before scanning.

## Understand the change
Read the diff and state in 1-3 sentences what it does and why. Skip this and the lens-scan below degrades to a blind pattern-match.

## Scan through four lenses
For every file in the diff, check:
- Architecture fit — per `../references/meta-pattern.md`, decomposed along the wrong axis or wrong level?
- Interface depth — per `../references/deep-modules.md`, a shallow module, leaky interface, or pass-through method touched by the change?
- Clean code - per `../references/clean-code.md`
- Simplicity — `/ponytail-review`'s lens: reinvented stdlib, unneeded dependencies, speculative abstractions, dead flexibility.
- Others (Clean code rule except above)

Every changed file gets checked against all four lenses before ranking.

## Report, don't fix
Lead with the 1-3 sentence understanding from above. Then rank candidates by size — smallest, most self-contained wins — and surface the single best boy-scout tidy: small enough to do in passing, next to code already touched. One line per finding: location, lens, what to cut/change. List up to three only if they're close; say so plainly if nothing clears the bar.

**MUST NOT** edit files or apply the fix. Next step is `/simplify` to apply it, or fix it by hand.
