# Human Checkpoint

Reuse `/skill:grill-me` as the interviewer instead of reimplementing its round logic in each skill.

Before invoking it, provide a narrow prompt containing:

- the current artifact or stage
- the single slice being worked on
- the decisions this skill is allowed to ask about
- what is explicitly out of scope
- the stop condition and artifact the skill needs back

Run the grill in rounds. Keep the frontier limited to the highest-impact questions, no more than three per round. Wait for the human's answers, recompute the frontier, and do not act on unresolved decisions.

Facts are the agent's job to inspect. Decisions belong to the human. If an experiment is required, use `/skill:experiment` rather than guessing. If the human says “I don't know,” use the recommended answer as an explicitly marked assumption and continue.

After `/skill:grill-me` completes, summarize **Confirmed**, **Assumptions**, **Deferred**, and **Next action**. Get confirmation before writing or editing behavior, data, interfaces, or structure.
