---
name: do-plan
description: Execute a /to-plan document's action items in order, checking each off in place, verify the plan's acceptance criteria, write up the run as a report, and quiz comprehension of the touched code. Invoke as /do-plan.
disable-model-invocation: true
---

# Do-Plan

Turn a written plan into done work instead of leaving its action items unbuilt.

1. **Ask for the plan.** Ask the user for the plan file path — don't guess a directory or assume the most recent plan written in this session. Ask again if the answer is missing or doesn't point to a real file. Completion criterion: user has given a concrete path to an existing plan file, containing spec changes, acceptance criteria, and `- [ ]` action items.
2. **Execute each unchecked action item, in order.** For each: implement it for real, verify the result, then edit the plan file to check it off (`- [x]`) before moving to the next. If the item writes or updates the target project's spec, follow `../references/spec-convention.md` (`spec/**/*.md` per `../template/spec.md`, `spec/index.md` kept in sync). Stop and ask the user if an item is ambiguous or its prerequisite failed — don't skip it. Completion criterion: every action item in the plan is either `- [x]` or explicitly called out as blocked.
3. **Verify acceptance criteria.** Check each one against the real state of the repo (run tests/build where applicable, don't assume from the diff alone) and record pass/fail. If a row names a Verification Method (per `../references/requirement-engineering.md`), confirm that test file actually exists and passes, and that the target project's spec file(s) (named in the plan's Spec changes) and `spec/index.md` contain the matching entry — a criterion whose test, spec entry, or index link is missing is a fail, not a skip.
4. **Write the report.** Read `../references/document-style.md` first — its structure governs the draft: an Introduction (what plan, why run), a Body (each action item done vs. blocked, each acceptance criterion's pass/fail, with evidence), and a Conclusion (overall outcome, next actions for anything blocked or failed). Write it next to the plan file, as `{plan-file}.report.md`.
5. **Write a comprehension quiz.** Read `../references/comprehension-quiz.md` first — its two categories (Structure & Responsibility, Core Logic) and L0/L1 answer format govern the draft. Cover the code touched by this run's action items. Write it next to the plan file, as `{plan-file}.quiz.md`.

**MUST WRITE** for each plan file per report and quiz. 
Completion criterion: every action item is checked or blocked, every acceptance criterion has a stated pass/fail, the report file exists reflecting both, and the quiz file exists covering the touched code at L0 and L1 for both categories.

Tell the user the report and quiz file paths when done.
Tell the user to do `/boy-scout` to refactor
