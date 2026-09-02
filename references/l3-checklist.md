# L3 Mechanism Checklist

Every point a `@skills/grill-me` interview must cover to nail down one L3 technical operation, per `abstraction-levels.md`. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms.

- Target — the exact technical operation being defined, and its one-sentence test (no "and"), in mechanism terms, per `abstraction-levels.md`'s One-Sentence Test — fails it, split into more than one operation
- Interface — the contract this implements for L2 to depend on; does it already exist, or is this its first implementation
- Mechanism — the technical operation itself (DB query, HTTP call, SDK call, filesystem op) and any technical policy it needs (retry, timeout, serialization) — no business decision
- Failure modes — what happens on error/timeout at this mechanism, surfaced up through the interface, not swallowed
- File — which existing file this mechanism's function/interface belongs in, per the repo's own module/folder convention (evidence: sibling L3 functions or the interface's existing home) — a new file only when no existing one fits
