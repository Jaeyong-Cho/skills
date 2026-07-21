---
name: to-todo
description: Turn a completed /breakdown tree into an inbox TODO.md — objective/background/scope framing, a checkbox body numbered by the breakdown's dotted ids, and a conclusion with critical path and parallel-ready execution order. Invoke as /to-todo.
disable-model-invocation: true
---

# To-Todo

Read `../references/document-style.md` first — the Introduction follows its bullet/paragraph conventions; the Body swaps prose bullets for checkboxes; the Conclusion's execution order swaps bullets for an ASCII flow diagram, since round-to-round dependency is flow-shaped content.

1. **Find the breakdown** — use the most recent `/breakdown` tree in this session: its top-level sections, dotted leaf ids, execution order, and critical path. If none exists, tell the user to run `/breakdown` first and stop.
2. **Ground the frame** — reread the session (and any file the user points to) for the Objective, Background, Scope (what's covered, and anything explicitly excluded), Methodology (the axes `/breakdown` split on), and Current state, each in a sentence or two sourced from the conversation, not invented. Ask the user for anything genuinely missing rather than guessing. Completion criterion: all five are stated and each traces to something said or read.
3. **Draft the Body** — one numbered section per breakdown top-level branch (its name), each holding its leaves as `- [ ] {dotted id} {leaf text}` in tree order, plus a closing "Explicitly out of scope" list for anything Scope named as excluded. Completion criterion: every leaf from the breakdown appears exactly once, ids matching the breakdown's.
4. **Draft the Conclusion** — Key takeaway (current state in one sentence), Recommended execution order as an ASCII flow diagram (plain characters only — `|`, `v`, `+--`, `->`; see `../references/document-style.md`) with one stage per round, parallel-ready ids listed together within a stage, and the critical-path chain called out (e.g. with a `*` marker and a legend line naming the most slip-exposed id and why), and Next action (round 1's ids spelled out as concrete steps, noting they're order-free within the round). Completion criterion: the diagram's rounds, groupings, and critical path match the breakdown exactly — no re-deriving dependencies here, only re-rendering them structured.
5. **Write to the inbox** — derive a kebab-case slug from the TODO topic and get a fresh timestamp with `date +%Y%m%d-%H%M%S`. Write the draft to `.context/inbox/todo/{timestamp}-{slug}.md`, creating `.context/inbox/todo` if needed. Completion criterion: the file exists at that path. Once every checkbox is checked, the user manually moves it unchanged to `.context/done/todo/`; the directory is its completion signal.

Tell the user the inbox file path and the done-directory move rule when done.
