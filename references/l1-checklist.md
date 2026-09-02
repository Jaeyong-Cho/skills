# L1 Sequence Checklist

Every point a `@skills/grill-me` interview must cover to nail down one L1 orchestration flow's step sequence, per `abstraction-levels.md`. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms.

- Target — the exact use case/flow being sequenced, and its one-sentence test (no "and") per `abstraction-levels.md`'s One-Sentence Test — fails it, split into more than one flow
- Trigger — the event, call, or request that starts this flow
- Sequence — the ordered list of steps, each named as the L2 domain rule or L3 mechanism it performs, in the exact order they execute — an order, not a bag of steps
- Branches — any point where the sequence forks (a condition that leads to a different next step), what decides each fork, and each branch's own ordered continuation
- End state — what the flow returns, or the observable outcome that marks it done
- File — which existing file this flow's function belongs in, per the repo's own module/folder convention (evidence: sibling L1 functions found there) — a new file only when no existing one fits
