# Refactor Checklist

Every point a `@skills/grill-me` interview must cover to refactor a named function or usecase sequence against `abstraction-levels.md`'s L1/L2/L3 rule. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms.

- Target — the exact function/usecase sequence to refactor (file:line or call chain), not "the payment code somewhere"
- Current shape — which level (L1/L2/L3) each part of the target reads as now, and which `abstraction-levels.md` smell it matches, with evidence (file:line)
- Root cause — why the smell exists (a shortcut taken under time pressure, a missing L2 that never got built, ...), not just "it's messy"
- Behavior-preservation baseline — the existing test(s) that currently pass and pin this target's behavior; if none exist, a characterization test **MUST** be written and green before any structural change, per `tdd-refactoring.md`
- Target decomposition — the new/changed functions the target splits into, one line each, tagged `[L1]`/`[L2]`/`[L3]` per `abstraction-levels.md`, each passing that doc's One-Sentence Test; each new/changed L2/L3 function gets TDD (RED → GREEN → REFACTOR) per that doc's Testing by level section, driven off the behavior-preservation baseline test above
- Interface change — does any public signature/contract change; which callers need updating (scope-in / scope-out)
- Impact scope
- Branch to work this refactor (git)
- New simple and representative testcase with **built program integration test**, not just unit test — name its fixture (real seed data, mock/stub setup, or existing state it needs)
- What I want — the observable outcome (same behavior, clearer shape), not a restatement of the intent above
- How to evaluate it — deterministic check: existing test(s) plus the new one from the line above stay green, per `deterministic-evaluation.md`
- Dogfood test
