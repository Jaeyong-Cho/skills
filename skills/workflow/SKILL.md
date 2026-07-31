---
name: workflow
description: Run the goal-to-plan pipeline in one pass — spec's scen -> req -> cmp -> seq stages straight through, then one co-plan self-plan per resulting sequence, dispatched to its own subagent one sequence at a time. Use when invoked as /workflow.
disable-model-invocation: true
---

# Workflow

Chain `/spec` from a goal to SEQ docs, then work the SEQ list one at a time: each gets its own subagent running `/co-plan` scoped to just that sequence.

```
Goal --to_scen--> SCN --to_req--> REQ --to_cmp--> CMP --to_seq--> SEQ
                                                            |
                                                  (per SEQ, one at a time)
                                                            v
                                                  co-plan --> self-plan
```

## 1. Resolve the goal

Input: the goal (prose in the invocation, or a goal file the user names) — the same input `/spec`'s `to_scen` takes.

## 2. Run scen -> req -> cmp -> seq directly, in order

Read `../spec/SKILL.md` once, then execute its `to_scen`, `to_req`, `to_cmp`, `to_seq` sections yourself, in this order, in your own context — do not dispatch a subagent for this part. Each stage's output feeds the next stage's input, and reading the chain as one continuous thread is what lets a slip in `to_req` get caught before it propagates into `to_cmp`.

1. `to_scen`: goal -> `spec/scen/SCN-*.md`.
2. `to_req`: those SCN docs -> `spec/req/REQ-*.md`.
3. `to_cmp`: those REQ docs -> `spec/cmp/CMP-*.md`.
4. `to_seq`: REQ + CMP docs -> `spec/seq/SEQ-*.md`.

Follow each section's own completion criterion before starting the next. If a stage stops (ambiguous goal, missing upstream content), stop the whole workflow there and report why — never invent content to force the chain forward.

## 3. One subagent per SEQ, sequentially

Take the SEQ docs written in step 2 in order. For each one, dispatch a single subagent with claude-sonnet-5 model and wait for it to finish and report its self-plan path before dispatching the next — never more than one subagent running at a time. Brief each subagent to:

- Read `../co-plan/SKILL.md` in full.
- Treat this one SEQ, plus its linked REQ and CMP docs (follow the SEQ's `## Requirement` and `## Components` references), as "the design" `/co-plan` expects — not the whole spec tree.
- Consider the previous plans from earlier SEQs as context for consistency.
- Run `/co-plan`'s process exactly, with one exception: skip the interactive "ask for confirmation" step — a dispatched subagent can't hold that conversation. Write the self-plan straight through and report its file path back.
- Derive the plan's slug from the SEQ's title, so the human can tell which SEQ produced which plan.

Each subagent's completion criterion is co-plan's own, unchanged: the self-plan's action sequence is fully ordered, every implementation step's hole/working decision is recorded, the ~30/70 budget holds, and the Recommended Human Work Order is filled in.

## 4. Report

Once every subagent returns, list each SEQ id next to the self-plan path its subagent produced — or the reason it didn't finish, if one failed. Tell the user the next step for each plan is `/auto-action`.

Completion criterion: every SEQ from step 2 has either a self-plan path or a reported failure reason — nothing left dispatched-and-unaccounted-for.

**DO NOT run `/auto-action` yourself** — that stays a separate, explicit step per plan, same as everywhere else in this pipeline.
