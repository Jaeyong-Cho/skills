---
name: do-plan
description: Execute a @skills/to-plan document's action items in order, checking each off in place, verify the plan's acceptance criteria, write up the run as a report. Invoke as /do-plan.
disable-model-invocation: true
---

# Do-Plan

Turn a written plan into done work instead of leaving its action items unbuilt.

1. **Ask for the plan.** Ask the user for the plan file path — don't guess a directory or assume the most recent plan written in this session. Ask again if the answer is missing or doesn't point to a real file. Completion criterion: user has given a concrete path to an existing plan file, containing spec changes, acceptance criteria, and `- [ ]` action items.
2. **Execute each unchecked action item, in order.** For each: implement it for real, verify the result, then edit the plan file to check it off (`- [x]`) before moving to the next. If the item writes or updates the target project's spec, follow `../references/spec-convention.md` (`spec/{epic-slug}/{story-slug}.md` per `../template/spec.md`, its `spec/{epic-slug}/index.md` and the top-level `spec/index.md` kept in sync). Stop and ask the user if an item is ambiguous or its prerequisite failed — don't skip it. Completion criterion: every action item in the plan is either `- [x]` or explicitly called out as blocked. **MUST CHECK** the spec document has acceptance criteria)
   - **STOP before merging a branch or releasing.** `/boy-scout` is human-invoked only — `@skills/do-plan` cannot run it. Leave the branch-merge/release item unchecked, tell the user to run `/boy-scout` and act on its finding, then resume once they confirm.
3. **Verify acceptance criteria.** Check each one against the real state of the repo (run tests/build where applicable, don't assume from the diff alone) and record pass/fail. If a row names a Verification Method (per `../references/requirement-engineering.md`), confirm that test file actually exists and passes, and that the target project's STORY spec file (named in the plan's Spec changes), its `spec/{epic-slug}/index.md`, and the top-level `spec/index.md` all contain the matching entry — a criterion whose test, spec entry, or either index link is missing is a fail, not a skip.
4. **Write the report.** Read `../references/document-style.md` first — its structure governs the draft: an Introduction (what plan, why run), a Body (each action item done vs. blocked, each acceptance criterion's pass/fail, with evidence), and a Conclusion (overall outcome, next actions for anything blocked or failed). Write it next to the plan file, as `{plan-file}.report.md`.
   
**MUST WRITE** for each plan file per report. 

Completion criterion: every action item is checked or blocked, every acceptance criterion has a stated pass/fail, the report file exists reflecting both.

Tell the user the report file path when done.
Tell the user to do `@skills/boy-scout` to refactor
