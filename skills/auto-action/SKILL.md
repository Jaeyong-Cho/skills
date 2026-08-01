---
name: auto-action
description: Auto-action skill. Stops immediately if the plan file already lives in `.context/done/plan/`. Otherwise reads a plan (from `.context/inbox/plan/`) and executes the full action sequence — fully autonomous for a regular plan; for a review-plan, writes and tests the entire sequence in one pass (same as a regular plan), then on a later run asks the human to confirm they've walked the plan's Review Sequence against the finished code before marking it done. Use when invoked as /auto-action.
disable-model-invocation: true
---

# Auto-Action

List the plans in `.context/inbox/plan/` (not yet done) and `.context/done/plan/` (finished) before reading any of them — which directory a plan lives in is the sole signal of its completion state. If the plan the user wants is already in `.context/done/plan/`, report **"Auto-action: this plan is already complete."** and stop; do not open it, re-execute, or re-review anything. If multiple plans exist in `.context/inbox/plan/`, list them and ask the user which to use.

Read the plan for the Action Sequence to execute.

Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`.

Check the plan's `**Type:**` line. If it reads `Review-Plan`, check its `## Closeout` checklist: if `[ ] Test` is still unchecked, follow **Review-Plan Execution — Write & Test**. If `[x] Test` is already checked and `[ ] Review` is still unchecked, follow **Review-Plan Execution — Confirm Review** instead. If the plan's Type line is anything other than `Review-Plan` (including absent), follow **Full Execution**.

## Full Execution

Execute the plan's entire Action Sequence straight through — no confirmation between steps. If a step fails or is blocked, stop immediately, report what failed and why, and do not continue.

After all steps are done, report what changed for each step in order. Since the Action Sequence's fixed last step is a full test run, mark `[x] Test` in the plan's `## Closeout` checklist, then move the plan file from `.context/inbox/plan/{timestamp}-{slug}.md` to `.context/done/plan/{timestamp}-{slug}.md` (`mkdir -p .context/done/plan` if needed).

Completion criterion: every step executed and reported, or stopped on first failure with reason. If every step succeeded, the plan's Closeout checklist is fully checked and the file now lives in `.context/done/plan/`.

## Review-Plan Execution — Write & Test

Execute the plan's entire Action Sequence straight through, exactly like Full Execution — every step is fully working code, there are no holes to leave open. If a step fails or is blocked, stop immediately, report what failed and why, and do not continue.

After all steps are done, report what changed for each step in order, then mark `[x] Test` in the plan's `## Closeout` checklist. Leave `[ ] Review` unchecked and do **not** move the plan file yet — the plan isn't done until the human has walked its Review Sequence against this finished code.

Completion criterion: every step written and tested, `[x] Test` checked in the plan file, `[ ] Review` still open, plan file still in `.context/inbox/plan/`. This is a stopping point, not a failure — the plan now waits on the human to review before `/auto-action` can move past it.

## Review-Plan Execution — Confirm Review

Do not rewrite or re-test any file — the code was already written and tested in the prior run. Instead, walk the plan's Review Sequence with the user: for each entry (in the top-down, entry-point-to-leaf order the plan records), name the file/function location and its verification point, and ask the user to confirm whether it holds in the finished code. Record, per entry, whether it was confirmed or flagged.

1. **Confirm.** Go through every Review Sequence entry and get the user's confirmation or a flagged concern for each.
2. **Commit.** Only if every entry was confirmed with no flagged concerns: draft the commit message following this project's standard git commit-message convention (see the top-level git instructions — draft from the actual diff, do not invent a new format), show it to the user along with the files to be staged, and ask them to confirm. Commit only after they confirm; if they decline or ask for changes, leave the working tree as-is and don't retry uninvited. If any entry was flagged, skip this entirely — do not ask to commit code the human hasn't fully confirmed.
3. **Mark Closeout.** If every Review Sequence entry was confirmed, mark `[x] Review` in the plan's `## Closeout` checklist, then move the plan file from `.context/inbox/plan/{timestamp}-{slug}.md` to `.context/done/plan/{timestamp}-{slug}.md` (`mkdir -p .context/done/plan` if needed). This happens regardless of the user's commit decision in step 2. If any entry was flagged, leave both the checklist and the file location unchanged — report the flagged entries so the user can request fixes, then re-run `/auto-action` once resolved.

Completion criterion: every Review Sequence entry confirmed or flagged with a verdict — or stopped with a reason if the plan has no recorded Review Sequence (send the user back to `/co-plan`). If every entry is confirmed, the user has been asked to confirm the commit, and the Closeout checklist and file location both reflect completion.

## When Done

**Already Done:** "Auto-action: this plan is already complete." followed by the plan file's path in `.context/done/plan/`. Do nothing else.

**Full Execution:** "Auto-action complete." followed by the per-step summary. If every step succeeded, report the plan's new path in `.context/done/plan/`. If any step failed, say what failed and note the plan stays in `.context/inbox/plan/`.

**Review-Plan Execution — Write & Test:** "Auto-action complete (review-plan)." followed by which files were modified or created and the test results. Tell the user: walk the plan's Review Sequence against this code, then re-run `/auto-action` on this plan — it will ask you to confirm each Review Sequence entry and, once confirmed, mark the plan done.

**Review-Plan Execution — Confirm Review:** "Auto-action review complete (review-plan)." followed by, per Review Sequence entry, whether the user confirmed it or flagged a concern. If every entry was confirmed, tell the user the plan's Closeout Review item is satisfied and the plan file has moved to `.context/done/plan/`, then show them the drafted commit message and ask them to confirm before committing. If any entry was flagged, say so plainly, note that nothing will be committed and the file was not moved, and do not claim Closeout is satisfied.
