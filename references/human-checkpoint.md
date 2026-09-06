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

## File confirmation

At session completion, distinguish the result from its persistence:

1. Summarize **Confirmed**, **Assumptions**, **Deferred**, **Next action**, and the artifact to preserve.
2. Propose the exact file path relative to the current working directory (`./`). Use an existing local convention when one exists; otherwise recommend a minimal path such as `./requirements/<slice-slug>.md` or `./design/<slice-slug>.md`.
3. Ask the human to confirm both the content and location before writing. Do not silently create, overwrite, or choose a new path.
4. If the result is code or a test, confirm the exact source/test path before editing and report the paths at completion.

A session is not persistently recorded until the human confirms the artifact and path.
