---
name: refact-grill-me
description: Run a @skills/grill-me interview to build understanding of a codebase you don't know well yet, through four lenses — architecture fit, interface depth, naming, simplicity — before deciding whether and how to refactor it. Invoke as /refact-grill-me.
disable-model-invocation: true
---

# Refact Grill Me

Reach for this when a target's code isn't understood well yet — the grilling below forces the investigation that builds that understanding; only once it's answered does a real refactor decision follow.

Run `@skills/grill-me` covering every point below. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical:

- Target scope — which file, module, or directory, and what's unclear about it
- Architecture fit (meta-pattern) — per `../references/meta-pattern.md`'s Level-of-Pain table, is the target decomposed too early, too late, or split along the wrong axis (Abstractness / Subdomain / Sharding)?
- Interface depth (deep-module) — per `../references/deep-modules.md`'s Design Smells table, which smells apply and where (shallow module, duplicated logic, information leakage, temporal decomposition, pass-through method, leaky interface, conjoined twins)
- Naming — per `../references/naming.md`'s Smells table, which apply and where
- Simplicity (ponytail) — run `/ponytail-review`'s lens: reinvented stdlib, unneeded dependencies, speculative abstractions, dead flexibility
- Clean code - `../references/clean-code.md` 
- Value — now that the target is understood, what gets easier or safer after refactoring, for which future change
- Behavior preservation — what proves nothing changed: existing tests, or new characterization tests written first if none exist
- Impact scope — every caller or consumer touched
- Testability
- Branch (git)
- Release and ship plan



**MUST NOT** implementation work has started.
Once complete, next step is `@skills/to-plan` to dump the recorded answers into a plan document.
