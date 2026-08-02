---
name: workflow
description: Run the goal-to-plan pipeline in one pass, skipping the spec stage to save tokens — grill the goal, run /explore once for the grilled intent (one haiku-tier question) plus any codebase facts the plan needs, feed that evidence straight to fs-plan as the design, then one auto-action write-and-test pass, then visualize with viewpoints. Use when invoked as /workflow.
disable-model-invocation: true
---

# Workflow

Grill the goal, then take the grilled intent directly as "the design" `/fs-plan` expects — no `/spec` stage, no SCN/REQ/CMP/SEQ docs, no Review Sequence: `/viewpoints` is the review step instead. This trades spec's traceability and co-plan's human-readable Review Sequence for token cost — skipping scen -> req -> cmp -> seq turns one grilled goal straight into one plan instead of a full doc tree. Reach for `/spec` + `/co-plan`'s per-SEQ fan-out instead when traceability, a human code walkthrough, or a goal large enough to need multiple SEQs matters more than the savings.

```
Goal --> [main thread: grilling] --> interview
                                          |
                                          v
                              [subagent(s): explore] --> evidence file(s)
                                (user-intent + any codebase facts)
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

Input: the goal (prose in the invocation, or a goal file the user names) — same input `/spec`'s `to_scen` takes.

Run `../grilling/SKILL.md` yourself, in the main thread, unmodified — it's interactive (`AskUserQuestion`, one question at a time), so it can't run in a dispatched subagent; that's why step 4's subagent can run unattended. Interview until the goal's open decisions are resolved.

Completion criterion: grilling's own — shared understanding on every branch with a discrete decision. Don't proceed on a goal that's still ambiguous.

## 2. Explore for the grilled intent and any facts the plan needs

Run `../explore/SKILL.md` once, posing every question step 3 needs answered — the grilled intent is just one more question in that batch, not a separate mechanism:

- **The grilled intent**: "What is the resolved goal, and the key decisions behind it, from this interview?" — give the full interview (every question asked, what it resolved to) as context. It's a write-up of an already-decided outcome, not a new judgment call, so it's explore's `haiku` tier: the source of truth already exists.
- **Any codebase fact** step 3 needs but the interview doesn't state — where affected code/tests live, what an existing pattern looks like, whether a dependency exists. Skip if the interview is already self-contained.

Let explore bucket, dispatch, and write every question — the intent one included — into one `.context/explore/{timestamp}-{task-slug}/` session. Treat those evidence files, not the raw transcript, as "the design" from here on.

Completion criterion: explore's own — every posed question, intent included, has a written, read evidence file.

## 3. Run fs-plan directly on the grilled intent

No `/spec` stage, no subagent fan-out — run `../fs-plan/SKILL.md` yourself, in the main thread, taking step 2's evidence files directly as "the design" it expects. No SCN/REQ/CMP/SEQ trail; the plan's own Action Sequence carries the goal's intent forward.

Run `/fs-plan`'s process exactly. Write the plan; note its path for step 4.

Completion criterion: fs-plan's own — action sequence fully ordered, test-before-implementation throughout, ending in the fixed full-suite test step.

## 4. Dispatch one subagent running auto-action

Dispatch a single subagent with the claude-haiku-4.5 model, brief it to:

- Read `../auto-action/SKILL.md` in full.
- Run `/auto-action` on step 3's plan path exactly as written — don't skip or reinterpret its branching logic.
- With no `**Type:**` line, this follows the **Full Execution** branch: the whole sequence gets written and tested, and once every step succeeds the plan moves to `.context/done/plan/` — the expected stop. Report what changed and the test results.
- If a step fails or auto-action stops otherwise, report exactly why — don't retry or work around it.

Completion criterion: the plan from step 3 has run through auto-action's Full Execution pass, results reported — or a reported failure reason.

## 5. Report

Once the subagent returns, report the plan path next to its test results — or why it didn't finish. If it succeeded, tell the user the plan moved to `.context/done/plan/`; step 6's viewpoints gallery is the review, so no further walkthrough is needed unless the user wants one.

## 6. Visualize the result

Once step 5's report is written, run `../viewpoints/SKILL.md` against it. Subject: the workflow's own output — step 2's evidence files, the plan, and its Write & Test result (pass/fail, files touched). A structural/comparison subject — expect flow forms (Goal -> plan -> test-result) and comparison forms (plan vs. test outcome) over statistical charts. Follow viewpoints' gallery assembly, then report the gallery path/URL alongside step 5's report — don't run its server step yourself.

Completion criterion: viewpoints' gallery `index.html` exists, its path reported to the user — this gallery is the workflow's review step, replacing a human-walked Review Sequence.
