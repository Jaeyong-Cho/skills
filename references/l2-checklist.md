# L2 Rule Checklist

Every point a `@skills/grill-me` interview must cover to nail down one L2 business rule, per `abstraction-levels.md`. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms.

- Target — the exact business rule being defined, and its one-sentence test (no "and"), in domain terms not technical terms, per `abstraction-levels.md`'s One-Sentence Test — fails it, split into more than one rule
- Input — the domain state/values this rule decides over
- Rule — the decision logic itself: every condition/branch, stated precisely in domain terms
- L3 dependency — does deciding this rule need a technical capability (current price, inventory count, a stored record, ...)? If so, the interface it depends on (never a concrete implementation) — does that interface already exist?
- Output — what this function returns, or the state transition it produces
