---
name: brainstorm
description: Brainstorm skill. Reads the codebase and asks questions to surface good ideas. Use when invoked as /brainstorm.
disable-model-invocation: true
---

# Brainstorm

Read the codebase. Read `.context/wiki/` and `.context/direction/` if they exist. Understand what the project does, what it can't do, and where it hurts.

Run `/grilling` to brainstorm — diverge across:
- **Gaps** — what is the codebase unable to do that it probably should?
- **Pain** — what is unnecessarily hard, slow, or fragile?
- **Leverage** — what small change would unlock the most value?
- **Surprise** — what would make this project 10x better?
- **Risk** — what is the most important thing that could go wrong?

Do not propose solutions during the brainstorm — ask, listen, and follow the thread. The user says "wrap up" to stop.

When the user wraps up, synthesize: list the best ideas that surfaced, ranked by potential impact. Each idea in one sentence.

Any useful truth discovered — a constraint, a domain fact, a key decision — can also be written to `.context/wiki/` at any time.
