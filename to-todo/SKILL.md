---
name: to-todo
description: Turn a completed /breakdown tree into a TODO.md — objective/background/scope framing, a checkbox body numbered by the breakdown's dotted ids, and a conclusion with critical path and parallel-ready execution order. Invoke as /to-todo.
disable-model-invocation: true
---

# To-Todo

Read `../references/document-style.md` first — the Introduction and Conclusion below follow its bullet/paragraph conventions; the Body swaps prose bullets for checkboxes.

1. **Find the breakdown** — use the most recent `/breakdown` tree in this session: its top-level sections, dotted leaf ids, execution order, and critical path. If none exists, tell the user to run `/breakdown` first and stop.
2. **Ground the frame** — reread the session (and any file the user points to) for the Objective, Background, Scope (what's covered, and anything explicitly excluded), Methodology (the axes `/breakdown` split on), and Current state, each in a sentence or two sourced from the conversation, not invented. Ask the user for anything genuinely missing rather than guessing. Completion criterion: all five are stated and each traces to something said or read.
3. **Draft the Body** — one numbered section per breakdown top-level branch (its name), each holding its leaves as `- [ ] {dotted id} {leaf text}` in tree order, plus a closing "Explicitly out of scope" list for anything Scope named as excluded. Completion criterion: every leaf from the breakdown appears exactly once, ids matching the breakdown's.
4. **Draft the Conclusion** — Key takeaway (current state in one sentence), Critical path and Recommended execution order (`{round}. {dotted ids…}` per round) transcribed from the breakdown as-is, and Next action (round 1's ids spelled out as concrete steps, noting they're order-free within the round). Completion criterion: critical path and execution order match the breakdown exactly — no re-deriving dependencies here.
5. **Confirm the destination and write** — ask the user for the file path. `mkdir -p` the parent directory if needed, then write the draft. Completion criterion: the file exists at the confirmed path.

Tell the user the file path when done.
