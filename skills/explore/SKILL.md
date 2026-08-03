---
name: explore
description: Delegate fact-finding to a subagent instead of spending the main thread's context on raw search output — get one evidence file per question - a direct answer backed by cited bullets. Defaults to haiku for lookups and bounded investigations ("where is X defined?", "does config Y exist?", "why does this test fail?"), reserving sonnet only for genuinely open-ended reconnaissance needing judgment ("is this pattern safe to reuse?", "what are the trade-offs before a design decision?") — never opus, since exploring only gathers evidence, it doesn't decide. Use before any non-trivial implementation, design, or debugging task that needs facts first, or when invoked as /explore.
---

# Explore

Research burns context twice: raw tool output, and the reasoning to make sense of it. Neither belongs in the thread still doing the main job. This skill pushes both into a subagent and keeps only the distilled answer — an **evidence file** — for the calling context to read.

## 1. Pose the questions

State each fact the main task needs, one question per fact. Keep questions distinct in scope — step 3 splits by tier, not by question count, so several may still share a subagent later.

## 2. Classify each question's tier

Apply `../../references/model-selection.md`'s three axes (ambiguity, mistake cost, verifiability) per question:

| Tier | Shape of the question | Example |
|---|---|---|
| `haiku-4.5` | Default tier. Locate/lookup, or a bounded investigation where the search path is knowable in advance even if it takes a few hops — a wrong or incomplete answer is cheap to notice and cheap to re-run | "Where is `X` defined?", "Does config `Y` set `Z`?", "List every caller of `F`.", "Why does this specific test fail?" |
| `sonnet-5` | Reserve for genuinely open-ended reconnaissance where what's even relevant is unclear, or the answer requires weighing trade-offs rather than reporting findings | "Is this pattern safe to reuse here?", "What are the trade-offs before we pick a design?" |

Default to `haiku` unless a question clearly needs judgment, not just search. Never escalate to `opus`: exploration only gathers evidence, it doesn't decide — `sonnet` covers a risky question's reasoning without opus's cost.

## 3. Group questions by tier

Bucket questions by tier from step 2 — at most two, `haiku` and `sonnet`. Each non-empty bucket gets exactly **one** subagent dispatch in step 5, however many questions it holds: one dispatch per tier, not per question. Split a bucket further only if it's too large for one subagent to juggle without overload.

## 4. Choose evidence file locations

Write a proper location for evidence files:
- `.../{question-slug}.md`

## 5. Dispatch

For each non-empty bucket from step 3, **MUST DISPATCH** one Agent tool call at that tier's model, `run_in_background: false` — not fire-and-forget, since the calling context needs the answers to proceed. If both buckets are non-empty, issue both calls in the same message so they run in parallel.

Brief each subagent with its bucket's full `{question, evidence path}` list, to:

- Research each question independently — one question's findings shouldn't bleed into another's file.
- Verify the two highest-risk claim shapes directly, not by proxy:
  - **Absence/removal** ("X was already removed," "X doesn't exist," "X is unused"): search for the literal named artifact itself (exact filename, symbol, string). A search that only covers *related* names (e.g. the APIs a file uses) is not evidence the file itself is gone — a proxy match can pass while the literal claim is false.
  - **Full enumeration** ("the only state/hooks/callers/fields are Y"): grep for every instance of the pattern across the whole file/symbol (e.g. every `useState`/`useReducer` call), don't summarize from a partial read. An omitted item is worse than a wrong one — nothing points at it later.
- Write each question's findings to its own path, structured as:
  - **Answer**, first: a direct, complete, concise answer — no padding, no restating evidence in prose, but complete enough that the calling context needs nothing else to understand it.
  - **Evidence**, per `../../references/document-style.md`: one claim per bullet, citation (file:line or URL) nested under it, tagged `[DIRECT]` (the search/read positively confirmed the literal thing claimed) or `[INFERRED]` (deduced without checking the thing itself) — grounds the Answer, doesn't restate it.
  - **Open gaps**: anything unresolved or uncertain — don't bury it by omitting it from the Answer.
- Reply with only the evidence file paths — no summary. The Answer section is the deliverable; a reply-level summary is just an uncontrolled second copy of it.

## 6. Read and use the evidence

Read each evidence file directly before starting the main task — don't re-derive what's already found. Weight confidence by tier: a `haiku` answer is reliable as-is (cheap to re-run if it looks off); a `sonnet` answer is a strong recommendation, not certainty — spot-check any claim that would materially change a risky decision.

Completion criterion: every question posed in step 1 has a written, non-empty evidence file, and the calling context has read each file's content before starting the main task.
