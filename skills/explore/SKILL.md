---
name: explore
description: Delegate fact-finding and codebase/web research to a subagent instead of spending the main thread's context on raw search output — get back one evidence file per question instead, a direct answer backed by cited bullets, not a raw dump. Tiers the subagent's model to the question's ambiguity (haiku for a narrow lookup like "where is X defined" or "does config Y exist"; sonnet for open-ended reconnaissance like "assess whether this pattern is safe to reuse" or "survey the trade-offs before a design decision" — never escalates to opus, since exploration only gathers evidence, it doesn't make the decision). Use before any non-trivial implementation, design, or debugging task that needs facts gathered first, or when invoked as /explore.
---

# Explore

Research burns context two ways: the raw tool output (file contents, grep hits, search results) and the reasoning needed to make sense of it. Neither belongs in the thread that still has to do the main job. This skill pushes both into a subagent and keeps only the distilled answer — an **evidence file** — for the calling context to read.

## 1. Pose the questions

State each fact that must be known before the main task can proceed, one question per fact. Keep questions distinct in scope even though several may later share a subagent — the split in step 3 is by tier, not by how many questions exist.

## 2. Classify each question's tier

Apply `../../references/model-selection.md`'s three axes (ambiguity, mistake cost, verifiability) per question:

| Tier | Shape of the question | Example |
|---|---|---|
| `haiku` | Narrow locate/lookup; a wrong or incomplete answer is cheap to notice and cheap to re-run | "Where is `X` defined?", "Does config `Y` set `Z`?", "List every caller of `F`." |
| `sonnet` | Anything else — a bounded investigation needing some reasoning, or open-ended reconnaissance with high ambiguity in what's even relevant | "Why does this specific test fail?", "Is this pattern safe to reuse here?", "What are the trade-offs before we pick a design?" |

Never escalate a dispatch to `opus`: exploration only gathers evidence for the calling context's decision, it doesn't make the decision itself, so `sonnet` covers the reasoning a risky question needs without paying for a stronger model on a research step.

## 3. Group questions by tier

Bucket all posed questions by the tier from step 2 — at most two buckets, `haiku` and `sonnet`. Each non-empty bucket gets exactly **one** subagent dispatch in step 5, regardless of how many questions land in it: a same-tier batch of questions is one dispatch handling all of them, not one dispatch per question. Only split a bucket further if it's large enough that one subagent's context would get overloaded juggling every question's findings at once.

## 4. Prepare the evidence paths

Run `date +%Y%m%d-%H%M%S` once per explore session (reuse it across every question dispatched together). Derive a kebab-case task-slug from the overall task and a kebab-case question-slug per question, then:

```bash
mkdir -p .context/explore/{timestamp}-{task-slug}
```

Each question's evidence file path: `.context/explore/{timestamp}-{task-slug}/{question-slug}.md` — one file per question, even when a subagent is answering several.

## 5. Dispatch

For each non-empty tier bucket from step 3, dispatch one Agent tool call at that tier's model, `run_in_background: false` — the calling context needs the answers before it can proceed, so this is not fire-and-forget. If both buckets are non-empty, issue both Agent calls in the same message so they run in parallel.

Brief each subagent with the full list of its bucket's `{question, evidence path}` pairs, to:

- Research each question in the list independently — findings from one question shouldn't bleed into another's file.
- Write each question's findings to its own evidence path with this structure:
  - An **Answer** section, first: a direct, complete answer to the question, written concisely and compactly — as few sentences as fully answer it, no padding, no restating the evidence in prose, but also not squeezed below what the question actually needs. The calling context must be able to understand the full answer from this section alone, without piecing it together from the evidence bullets below.
  - An **Evidence** section following `../../references/document-style.md`: one supporting claim per bullet, citation (file:line, or URL) nested under the claim it backs, no prose paragraphs — this is what grounds the Answer section, not a restatement of it.
  - An **Open gaps** section noting anything it couldn't resolve or is unsure of — don't paper over uncertainty by omitting it from the Answer.
- Reply with only the list of evidence file paths — no restated summary. The file's Answer section is the deliverable; a reply-level summary would just be a second, uncontrolled-length copy of it.

## 6. Read and use the evidence

Read each evidence file's content directly before starting the main task — don't re-derive what the subagent already found. Weight the confidence in what you read by its tier: a `haiku` answer to a narrow lookup is reliable as-is (cheap to re-run if a claim looks off later); a `sonnet` answer to an open-ended question is a strong recommendation, not certainty — spot-check any claim that would materially change a risky decision before committing to it.

Completion criterion: every question posed in step 1 has a written, non-empty evidence file, and the calling context has read each file's content before starting the main task.
