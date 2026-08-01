---
name: workflow
description: Run the goal-to-plan pipeline in one pass — grill the goal first, then spec's scen -> req -> cmp -> seq stages straight through in one subagent, then one co-plan review-plan per resulting sequence, then one auto-action write-and-test pass per plan, each dispatched to its own subagent one at a time. Use when invoked as /workflow.
disable-model-invocation: true
---

# Workflow

Grill the goal first, then chain `/spec` from that goal to SEQ docs, then work the SEQ list one at a time: each gets its own subagent running `/co-plan` scoped to just that sequence, then its own subagent running `/auto-action` on the resulting plan.

```
Goal --> [main thread: grilling] --> grilled Goal
                                          |
                                          v
                        [subagent: to_scen->to_req->to_cmp->to_seq] --> SEQ list
                                                                          |
                                                                (per SEQ, one at a time)
                                                                          v
                                                                co-plan --> review-plan
                                                                          |
                                                                (per plan, one at a time)
                                                                          v
                                                                auto-action (haiku) --> Write & Test
```

## 1. Grill the goal

Input: the goal (prose in the invocation, or a goal file the user names) — the same input `/spec`'s `to_scen` takes.

Before dispatching anything, run `../grilling/SKILL.md` yourself, in the main thread, against this goal — grilling is interactive (it asks the user one question at a time via `AskUserQuestion`), so it cannot run inside a dispatched subagent; every subagent from step 3 onward runs unattended and explicitly skips confirmation steps for that reason. Interview the user until the goal's open decisions are resolved, then treat the grilled result as the goal for step 2.

Completion criterion: grilling's own — a shared understanding reached on every branch of the goal that has discrete decisions to make. Don't proceed to step 2 on a goal that's still ambiguous.

## 2. Resolve the goal

Take the grilled goal from step 1 as the input to `/spec`'s `to_scen`.

## 3. One subagent runs scen -> req -> cmp -> seq, in order

Dispatch a single subagent with claude-sonnet-5 model to run the whole chain, and wait for it to finish. Isolating this in a subagent keeps the (potentially large) SCN/REQ/CMP/SEQ doc content out of your own context — you only need the resulting SEQ list for step 4, not the full doc bodies. Brief the subagent to:

- Read `../spec/SKILL.md` once, then execute its `to_scen`, `to_req`, `to_cmp`, `to_seq` sections itself, in this order, as one continuous pass in its own context — reading the chain as one continuous thread is what lets a slip in `to_req` get caught before it propagates into `to_cmp`.
  1. `to_scen`: goal -> `spec/scen/SCN-*.md`.
  2. `to_req`: those SCN docs -> `spec/req/REQ-*.md`.
  3. `to_cmp`: those REQ docs -> `spec/cmp/CMP-*.md`.
  4. `to_seq`: REQ + CMP docs -> `spec/seq/SEQ-*.md`.
- Follow each section's own completion criterion before starting the next. If a stage stops (ambiguous goal, missing upstream content), stop the whole chain there and report why — never invent content to force the chain forward.
- Report back: the list of SEQ ids and file paths written (or the stage it stopped at and why, if it didn't reach `to_seq`).

If the subagent reports a stopped chain instead of a SEQ list, stop the whole workflow here and report why to the user — do not proceed to step 4 with a partial or invented SEQ list.

## 4. One subagent per SEQ, sequentially

Take the SEQ docs written in step 3 in order. For each one, dispatch a single subagent with claude-sonnet-5 model and wait for it to finish and report its review-plan path before dispatching the next — never more than one subagent running at a time. Brief each subagent to:

- Read `../co-plan/SKILL.md` in full.
- Treat this one SEQ, plus its linked REQ and CMP docs (follow the SEQ's `## Requirement` and `## Components` references), as "the design" `/co-plan` expects — not the whole spec tree.
- Consider the previous plans from earlier SEQs as context for consistency.
- Run `/co-plan`'s process exactly, with one exception: skip the interactive "ask for confirmation" step — a dispatched subagent can't hold that conversation. Write the review-plan straight through and report its file path back.
- Derive the plan's slug from the SEQ's title, so the human can tell which SEQ produced which plan.

Each subagent's completion criterion is co-plan's own, unchanged: the review-plan's action sequence is fully ordered, test-before-implementation on every unit of work, and the Review Sequence covers every implementation step top-down along the flow with a concrete verification point.

## 5. One subagent per plan, sequentially, running auto-action

Take the review-plan paths written in step 4, in the same order. For each one, dispatch a single subagent with the claude-haiku-4.5 model and wait for it to finish and report its result before dispatching the next — never more than one subagent running at a time, since these subagents write real code and running them concurrently risks file conflicts across plans that touch overlapping code. Brief each subagent to:

- Read `../auto-action/SKILL.md` in full.
- Run `/auto-action` on this one plan's file path exactly as written — do not skip or reinterpret its branching logic.
- Since this is a freshly-written review-plan, this will follow the **Review-Plan Execution — Write & Test** branch: the whole action sequence gets written and tested, `[x] Test` is checked, and the plan stays in `.context/inbox/plan/` with `[ ] Review` open — that's the expected stopping point, not a failure. Report back what changed and the test results.
- If a step fails or auto-action stops for any other reason, report exactly what failed and why — do not retry or work around it.

Completion criterion: every review-plan from step 4 has been run through auto-action's Write & Test pass, with results reported — or a reported failure reason if one didn't finish.

## 6. Report

Once every subagent returns, list each SEQ id next to its review-plan path and its auto-action test results — or the reason it didn't finish, if one failed. Tell the user each plan now needs a human to walk its Review Sequence against the finished code, then re-run `/auto-action` on it themselves to confirm review and close it out.

Completion criterion: every SEQ from step 3 has either a review-plan path with auto-action results, or a reported failure reason — nothing left dispatched-and-unaccounted-for.

**DO NOT run the Confirm Review pass yourself** — that step asks the human to confirm each Review Sequence entry, which only the human can genuinely do; workflow's job ends at Write & Test.
