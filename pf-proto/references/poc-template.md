# PoC Document Template

> **Caveman style.** Chat and this document. Drop articles, filler, pleasantries. Fragments OK. Short synonyms. Arrows for causality. Technical terms exact.

```markdown
# [ID] Title

**Date:** YYYY-MM-DD
**Question:** <the specific question this prototype answered>
**Type:** Logic | UI

## What was built

Brief description of the prototype.

## Findings

What the prototype revealed — validated, invalidated, and surprising.

## Decisions

Concrete decisions this prototype enables:
- Interfaces, data shapes, or workflows that are now clear
- Options that were ruled out and why

## Architecture

VAO shape derived from the prototype findings:

**Value** — what user goal does this serve? what must succeed, what must never happen?

**Aspect** — which workflows or decision logic connect objects to the user's goal?

**Object** — which stable objects emerged? what do they own (properties, behaviors)?

**Views** — whichever views illuminate the findings for the stakeholders who will act on this PoC. See `../pf/references/views.md` for guidance on which to choose. Omit if the VAO shape above already makes everything clear.

## User feedback

What the user observed while running the prototype — reactions, surprises, corrections, and things that felt wrong. Captured directly from the user, not inferred.

## Open questions

What remains unresolved — to be explored in the ADR grill-me.

## Out of scope

What was deliberately not tested.
```
