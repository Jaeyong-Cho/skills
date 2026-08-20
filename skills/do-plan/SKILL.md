---
name: do-plan
description: Execute a @skills/to-plan document's action items in order, checking each off in place, verify the plan's acceptance criteria, write up the run as a report. Invoke as /do-plan.
disable-model-invocation: true
---

# Do-Plan

Turn a written plan into done work instead of leaving its action items unbuilt.

1. **Ask for the plan.** Ask the user for the plan file path — don't guess a directory or assume the most recent plan written in this session. Ask again if the answer is missing or doesn't point to a real file. Completion criterion: user has given a concrete path to an existing plan file, containing spec changes, acceptance criteria, and `- [ ]` action items.
2. **Execute each unchecked action item, in order.** For each: implement it for real, verify the result, then edit the plan file to check it off (`- [x]`) before moving to the next. Stop and ask the user if an item is ambiguous or its prerequisite failed — don't skip it.
   - **Assert on uncertainty.** If the item touches a function named in the plan's Assertions section, write that line's assert as a real runtime statement in the implementation code, at the exact point it checks (language-native `assert`/equivalent, not a comment, not test-only) — same rigor as Verification Method rows.
   - **Keep the spec in sync.** If the item writes or updates the target project's spec, follow `../references/spec-convention.md`: `spec/{epic-slug}/{story-slug}.md` per `../template/spec.md`, with its `spec/{epic-slug}/index.md` and the top-level `spec/index.md` kept in sync.
   - **STOP before merging a branch or releasing** — unless the plan's Next step line (per `../references/workflow.md`) says this plan is itself a `/boy-scout` cleanup plan, in which case there's no branch/release step to stop at. Otherwise: `/boy-scout` is human-invoked only — `@skills/do-plan` cannot run it. Leave the branch-merge/release item unchecked, tell the user to run `/boy-scout` and act on its finding, then resume once they confirm.

   Completion criterion: every action item in the plan is either `- [x]` or explicitly called out as blocked.
3. **Verify acceptance criteria.** Check each one against the real state of the repo (run tests/build where applicable, don't assume from the diff alone) and record pass/fail. If a row names a Verification Method (per `../references/requirement-engineering.md`), confirm that test file actually exists and passes, and that the target project's STORY spec file (named in the plan's Spec changes), its `spec/{epic-slug}/index.md`, and the top-level `spec/index.md` all contain the matching entry — a criterion whose test, spec entry, or either index link is missing is a fail, not a skip.
4. **Write the report.** Read `../references/document-style.md` first — its structure governs the draft: an Introduction (what plan, why run), a Body (each action item done vs. blocked, each acceptance criterion's pass/fail, with evidence), and a Conclusion (overall outcome, next actions for anything blocked or failed). Write it next to the plan file, as `{plan-file}.report.md`.

Completion criterion: every action item is checked or blocked, every acceptance criterion has a stated pass/fail, the report file exists reflecting both.

5. **Update the project's wiki** — if the plan has a `Target project` field, invoke `@skills/project-wiki {target-project} {plan-file} {report-file}` to synthesize the plan's findings into the project-scoped wiki. Read the `Target project` value from the plan file. Skip this step if the plan has no Target project field (a plan that isn't scoped to a single project). Completion criterion: the skill completes successfully or is skipped due to missing field.

6. **Update the global kb** — invoke `@skills/kb-ingest {plan-file} {report-file}` unconditionally, every cycle (unlike step 5, no `Target project` gate — the global kb isn't project-scoped). This uses `kb-ingest`'s new per-cycle mode — the cycle's own plan and report are the delta, no day-wide re-read. Note that `kb-ingest`'s step 8 already refreshes every `qmd` collection, which is why the old standalone sync step is removed rather than kept alongside. Completion criterion: the skill completes and `~/wiki/kb/log.md` has a new line for today.

Tell the user the report file path when done.
Tell the user the plan's Next step line (per `../references/workflow.md`): run `@skills/boy-scout` if this plan wasn't itself a `/boy-scout` cleanup plan; otherwise resume the feature/fix plan it named — don't suggest another `/boy-scout` run.
