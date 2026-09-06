---
name: to-agent
description: Build or update one custom agent, skill, or CLI tool for a specific purpose, directly — same target as @skills/system-grill-me but confirmed once instead of grilled round by round. Invoke as /to-agent.
disable-model-invocation: true
---

# To-Agent

One purpose, one build: a single custom agent, skill, or CLI tool — the same three kinds `@skills/system-grill-me` designs a whole unattended team of, but confirmed once instead of grilled round by round. Reach for `@skills/system-grill-me` instead when the goal needs more than one of these working together as a team; reach for this skill when the purpose already fits one.

1. **Confirm the target, once.** **MUST ASK** — up to three ❓/➡️ questions in one batched round per `../references/question-format.md`, never `@skills/grill-me`'s multi-round frontier: the specific purpose this serves, which kind it is (agent / skill / CLI tool), and the build target path (default: the current directory; recommend it as the answer unless the user names a different location, any location, not necessarily a repo). Skip asking whatever the user already said. Check the target path first — an existing matching file there makes this an update pass, not a fresh build; read it before asking, and say so in the question instead of asking as if starting from nothing. Completion criterion: purpose, kind, and target path are each either stated by the user or an explicit recommended answer, never silently guessed.
2. **Follow the kind's own convention, don't invent one.** Deciding agent vs. skill in the first place → read `../references/subagents-vs-skills.md`.
   - **Skill** → read `@skills/writing-great-skills` in full before drafting — its invocation choice, information hierarchy, leading words, and pruning discipline govern the new `SKILL.md` the same way they govern this one.
   - **Custom agent** (a Leader/sub-agent definition) → read `../references/pi-custom-subagent.md` for the per-platform mechanic (Claude's Task tool, Copilot's `--agent`, pi's `pi-interactive-subagents` plugin); detect the real installed platform by checking the tool itself (`--help`, its docs), never assumed from memory.
   - **CLI tool** → classify it per `../references/good-harness.md`'s axes (structural vs. behavioral, objective vs. judgment) before writing a line of it — the classification is what step 4's check ends up checking.
3. **Build it at the confirmed target.** Create the file(s) fresh if step 1 found nothing there, or edit the existing ones in place if it did — never a second copy alongside the original. Stay inside the one purpose step 1 confirmed; a second, unrelated purpose belongs in its own `to-agent` run, not folded into this one.
4. **Leave one runnable check.** Every kind ends with something that fails if the build breaks, not just prose describing it: a skill's own self-test (the `--test` pattern used by `experiment/scripts/lint_report.py`), a CLI tool's `demo()`/`__main__` self-check or a `test_*` file, a custom agent's one real dispatch. No check written is not a done build.

Completion criterion: the artifact exists at the confirmed target — fresh or updated in place — and step 4's check passes for real, run and observed, not assumed.

Tell the user the file path(s) and the exact command to run the check, when done.
