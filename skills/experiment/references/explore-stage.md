# Explore stage

Read only when you've reached this stage.

**Locate the question's directory.** Match the request to a `## Question N` heading in root `goal.md` (per `pipeline.md`'s `handoff_rules`):
- No `goal.md`: stop, tell the user to run `/goal-init` first.
- No matching heading: append a new `## Question N` and create its `questions/{slug}/` yourself, using the same kebab-case slugging `/goal-init` uses.
- Matching heading: use its existing `questions/{slug}/` — already created by `/goal-init`.

**Explore.** Check `questions/{slug}/.context/explore/goal-context.md` first — `/question-brainstorm` writes it there when it originated this question, per its own explore pass over the goal. If present, read it before deciding whether to explore further:
- **Covers the request already:** skip the dispatch below, cite this file as the evidence.
- **Goal-level but not specific enough** (e.g. it answered "does a cache exist" but this request needs "what's the current TTL"): still **MUST RUN** the dispatch below, but scope the question to the gap rather than re-asking what `goal-context.md` already covers.

No `goal-context.md`, or it left a gap: **MUST RUN** `../../explore/SKILL.md` — sonnet tier (open-ended reconnaissance, not a lookup) — posing: "What codebase/domain context is relevant to <the request>, and what would ground an interview about it?" Save the evidence directly to `questions/{slug}/.context/explore/{question-slug}.md` — the directory already exists, so no staging area or move step.

## Gate — resolve here, or continue?

- **Evidence alone answers the request** (a lookup, not a claim to test): answer directly from the evidence, citing it. Stop — no further stage.
- **Evidence is worth seeing, not testing** (the request wanted to understand or explore something — a structure, a dataset, a codebase shape — not verify a claim): ask the user via `AskUserQuestion` whether to build a gallery (`../references/viewpoints-stage.md`) before Publish, or skip straight to Publish. No hypothesis, no core stage either way.
- **Request needs a claim tested** (comparative/causal — "does X actually help/hurt Y", "which is faster/safer/correct"): continue to `../references/core-stage.md` for attempt 1. Judge the starting tier from the evidence: `cheap` if a single quick check could plausibly settle it, `full` only if it's inherently comparative/causal at a scale no one-shot check can cover — don't default to `full` just because a claim needs testing.
