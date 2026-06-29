---
name: brainstorm
description: Brainstorm skill. Reads the codebase and asks questions to surface good ideas. Use when invoked as /brainstorm.
disable-model-invocation: true
---

# Brainstorm

Read the codebase. Read `source-of-truth/wiki/`, `source-of-truth/direction/`, and `source-of-truth/attack/` if they exist. Understand what the project does, what it can't do, and where it hurts.

Then brainstorm — ask questions one at a time to draw out ideas. The goal is to diverge: surface possibilities, not decisions.

Questions should probe across:
- **Gaps** — what is the codebase unable to do that it probably should?
- **Pain** — what is unnecessarily hard, slow, or fragile?
- **Leverage** — what small change would unlock the most value?
- **Surprise** — what would make this project 10x better?
- **Risk** — what is the most important thing that could go wrong?

Ask one question at a time. When a question has clear options, use the `AskUserQuestion` tool. For open-ended questions, ask in plain text. Do not propose solutions during the brainstorm — ask, listen, and follow the thread.

There is no limit on questions. The user says "wrap up" to stop.

When the user wraps up, synthesize: list the best ideas that surfaced, ranked by potential impact. Each idea in one sentence.

Any useful truth discovered — a constraint, a domain fact, a key decision — can also be written to `source-of-truth/wiki/` at any time.
