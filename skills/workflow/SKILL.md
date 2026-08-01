---
name: workflow
description: Run the goal-to-plan pipeline in one pass, skipping the spec stage entirely to save tokens — grill the goal first, then feed the grilled goal straight to fs-plan as the design, then one auto-action write-and-test pass, then visualize the result with viewpoints. Use when invoked as /workflow.
disable-model-invocation: true
---

# Workflow

Grill the goal first, then take the grilled goal directly as "the design" `/fs-plan` expects — no `/spec` stage, no SCN/REQ/CMP/SEQ docs written or read, and no Review Sequence for a human to walk afterward: `/viewpoints` is the review step instead. This trades away spec's traceability and co-plan's human-readable Review Sequence for token cost: skipping scen -> req -> cmp -> seq means one grilled goal turns straight into one plan instead of fanning out a full doc tree first. Reach for `/spec` + `/co-plan`'s original per-SEQ fan-out instead when that traceability, a human code walkthrough, or a goal genuinely large enough to need splitting into multiple SEQs, matters more than the token savings.

```
Goal --> [main thread: grilling] --> grilled Goal
                                          |
                                          v
                              [main thread: fs-plan] --> plan
                                                              |
                                                              v
                                                    [subagent: auto-action (haiku)] --> Write & Test
                                                              |
                                                              v
                                                    Report --> viewpoints gallery
```

## 1. Grill the goal

Input: the goal (prose in the invocation, or a goal file the user names) — the same input `/spec`'s `to_scen` takes.

Before dispatching anything, run `../grilling/SKILL.md` yourself, in the main thread, against this goal — grilling is interactive (it asks the user one question at a time via `AskUserQuestion`), so it cannot run inside a dispatched subagent; step 3's subagent runs unattended for that reason. Interview the user until the goal's open decisions are resolved, then treat the grilled result as the goal for step 2.

Completion criterion: grilling's own — a shared understanding reached on every branch of the goal that has discrete decisions to make. Don't proceed to step 2 on a goal that's still ambiguous.

## 2. Run fs-plan directly on the grilled goal

No `/spec` stage, no subagent fan-out here — run `../fs-plan/SKILL.md` yourself, in the main thread, taking the grilled goal from step 1 directly as "the design" `/fs-plan` expects. There's no SCN/REQ/CMP/SEQ paper trail to link back to; the plan's own Action Sequence is what carries the goal's intent forward from here.

Run `/fs-plan`'s process exactly. Write the plan and note its file path for step 3.

Completion criterion: fs-plan's own, unchanged — the plan's action sequence is fully ordered, test-before-implementation on every unit of work, ending in the fixed full-suite test step.

## 3. Dispatch one subagent running auto-action

Dispatch a single subagent with the claude-haiku-4.5 model, brief it to:

- Read `../auto-action/SKILL.md` in full.
- Run `/auto-action` on step 2's plan file path exactly as written — do not skip or reinterpret its branching logic.
- Since this is a plan with no `**Type:**` line, this will follow the **Full Execution** branch: the whole action sequence gets written and tested, and once every step succeeds the plan moves from `.context/inbox/plan/` to `.context/done/plan/` — that's the expected stopping point. Report back what changed and the test results.
- If a step fails or auto-action stops for any other reason, report exactly what failed and why — do not retry or work around it.

Completion criterion: the plan from step 2 has been run through auto-action's Full Execution pass, with results reported — or a reported failure reason if it didn't finish.

## 4. Report

Once the subagent returns, report the plan path next to its auto-action test results — or the reason it didn't finish, if it failed. If it succeeded, tell the user the plan has moved to `.context/done/plan/`; the viewpoints gallery in step 5 is the review, so no further human walkthrough step is needed unless the user wants one.

## 5. Visualize the result

Once step 4's report is written, run `../viewpoints/SKILL.md` against it. The subject is the workflow's own output, not external data: the grilled goal, the plan, and its auto-action Write & Test result (pass/fail, files touched). This is a structural/comparison subject — expect the shortlist to lean on structure & flow forms (e.g. a Goal -> plan -> test-result flow diagram) and comparison forms (e.g. plan vs. test outcome) rather than statistical charts. Follow viewpoints' steps through its gallery assembly, then report the gallery path/URL to the user alongside the step 4 report — do not run its server step yourself, same as viewpoints' own instruction.

Completion criterion: viewpoints' gallery `index.html` exists and its path has been reported to the user — this gallery is the workflow's review step, in place of a human-walked Review Sequence.
