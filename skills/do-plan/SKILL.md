---
name: do-plan
description: Execute a /to-plan document's action items in order, checking each off in place, then verify the plan's acceptance criteria. Invoke as /do-plan.
disable-model-invocation: true
---

# Do-Plan

Turn a written plan into done work instead of leaving its action items unbuilt.

1. **Ask for the plan.** Ask the user for the plan file path — don't guess a directory or assume the most recent plan written in this session. Ask again if the answer is missing or doesn't point to a real file. Completion criterion: user has given a concrete path to an existing plan file, containing spec changes, acceptance criteria, and `- [ ]` action items.
2. **Execute each unchecked action item, in order.** For each: implement it for real, verify the result, then edit the plan file to check it off (`- [x]`) before moving to the next. Stop and ask the user if an item is ambiguous or its prerequisite failed — don't skip it. Completion criterion: every action item in the plan is either `- [x]` or explicitly called out as blocked.
3. **Verify acceptance criteria.** Check each one against the real state of the repo (run tests/build where applicable, don't assume from the diff alone) and record pass/fail.

Completion criterion: every action item is checked or blocked, and every acceptance criterion has a stated pass/fail.

Report back: which action items were done vs. blocked, and each acceptance criterion's pass/fail.
