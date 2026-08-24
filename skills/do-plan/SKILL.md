---
name: do-plan
description: Execute a @skills/to-plan document's action items in order, checking each off in place, verify the plan's acceptance criteria, commit the change, write up the run as a report. Invoke as /do-plan.
disable-model-invocation: true
---

# Do-Plan

Turn a written plan into done work instead of leaving its action items unbuilt.

1. **Ask for the plan.** Ask the user for the plan file path — don't guess a directory or assume the most recent plan written in this session. Ask again if the answer is missing or doesn't point to a real file. Completion criterion: user has given a concrete path to an existing plan file, containing acceptance criteria and `- [ ]` action items.
2. **Execute each unchecked action item, in order.** For each: implement it for real, verify the result, then edit the plan file to check it off (`- [x]`) before moving to the next. Stop and ask the user if an item is ambiguous or its prerequisite failed — don't skip it.
   - **Assert on uncertainty.** If the item touches a function named in the plan's Assertions section, write that line's assert as a real runtime statement in the implementation code, at the exact point it checks (language-native `assert`/equivalent, not a comment, not test-only) — same rigor as Verification Method rows.
   - **STOP before merging a branch or releasing** — these are human-invoked only, `@skills/do-plan` cannot run them. Leave the branch-merge/release item unchecked and **MUST ASK the human to confirm** before either happens; never merge or release on the agent's own judgment.
   - **Dogfood test.**

   Completion criterion: every action item in the plan is either `- [x]` or explicitly called out as blocked.
   - **Clear done TODOs.** If completing an action item resolves a pre-existing entry in the target project's TODO.md, delete that line — don't leave a done item sitting in `## Now`/`## Next`/`## Later`.
3. **Verify acceptance criteria.** Check each one against the real state of the repo (run tests/build where applicable, don't assume from the diff alone) and record pass/fail. If a row names a Verification Method (per `../references/requirement-engineering.md`), confirm that test file actually exists and passes — a criterion whose test is missing is a fail, not a skip.
   - **Run `@skills/experiment` on High-uncertainty ground.** A row whose Assertions-section line is tagged High uncertainty gets more than a passing test: run `@skills/experiment` to see the actual implementation result for real (plan → act → analyze), and record its verdict and file path next to that row — a green test alone isn't trustworthy evidence there.
4. **Commit.** Run the plan's Build line and both its unit and integration test commands for real. Only if the build succeeds, both test suites pass, and every acceptance criterion passes (step 3), commit the change for real in the target project — stage exactly the files this plan touched (never a blind `-A`/`.`; review what's staged first), and use the plan's Commit line as the message. Note the resulting commit hash next to that line in the plan file. If the build fails, either test suite fails, or any acceptance criterion failed, don't commit — tell the user what's broken instead.
5. **Write the report.** Read `../references/document-style.md` first — its structure governs the draft: an Introduction (what plan, why run), a Body (each action item done vs. blocked, each acceptance criterion's pass/fail, with evidence, plus a plain-language "What changed" list — one line per action item, no jargon), and a Conclusion (overall outcome, next actions for anything blocked or failed). **Copy the plan's QA Procedure into the report as a "Try it yourself" checklist**, same order: run each step that doesn't need a human (state the actual observed result next to it), leave `- [ ]` for steps that genuinely need a human's eyes/hands (UI, physical device) so they know exactly what to click and what to expect. For any `- [ ]` step the human can run from a terminal (curl, CLI call, short script), give the exact copy-pasteable command inline in the checklist — if it takes more than one command, write it as a throwaway script next to the report (`{plan-file}.qa/{nn}-{slug}.sh` or equivalent), not into the repo, and reference its path in the checklist item, so the human runs one thing and sees the result themselves instead of reading code. Write it next to the plan file, as `{plan-file}.report.md`.

Completion criterion: every action item is checked or blocked, every acceptance criterion has a stated pass/fail, a commit hash is recorded (or a failing build/test/acceptance-criteria run explains why not), the report file exists reflecting all three.

Tell the user the report file path when done.
