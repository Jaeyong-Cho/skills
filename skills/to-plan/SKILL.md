---
name: to-plan
description: Write up this session's decisions as a plan document — spec changes, acceptance criteria, action items. Invoke as /to-plan.
disable-model-invocation: true
---

# To-Plan

Turn this session's decisions into a plan document instead of leaving them to evaporate at the end of the chat.
Write a handoff document summarising the current conversation so a fresh agent can continue the work.

1. **Follow document style.** Read `../references/document-style.md` first — its Introduction/Abstraction/Detailed structure and size limits govern the draft.
2. **Draft the plan**, covering:
   - Target project (e.g. path of the repo)
   - Spec changes
   - Acceptance criteria
   - Action items, each as `- [ ] {item}` — `/do-plan` executes and checks these off in place
3. **Write it** to `plans/{timestamp}-{slug}.md` (kebab-case slug of the plan's topic, timestamp from `date +%Y%m%d-%H%M%S`), creating the directory if needed.

Completion criterion: the file exists, and spec changes, acceptance criteria, and action items are each present and traceable to something decided in this session.

Tell the user the file path, and that `/do-plan` executes it, when done.
