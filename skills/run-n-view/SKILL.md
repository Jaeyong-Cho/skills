---
name: run-n-view
description: Run something for real, then build a /viewpoints gallery over its output — launch/drive a command, script, test suite, or app via the run skill, capture the real output, and hand it to /viewpoints for a gallery of charts/diagrams instead of raw text. Use when invoked as /run-n-view.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Agent, Skill, AskUserQuestion
---

# Run-n-View

Chain two skills into one pass: **run** something for real, then **view** its output as a gallery instead of raw text or logs. No hypothesis, no verdict, no report — just execution plus a gallery. For a full scientific-method run (hypothesis -> method -> analysis -> report), use `/experiment` instead; this skill is the bare run+view primitive.

## Steps

1. **Identify the target.** Pin down exactly what gets run — a command, script, test suite, or "the app" — from the user's request or the project's existing run configuration. Ask the user if it's ambiguous. Slugify a short name for it (`{slug}`, kebab-case) and create `run-n-view/{slug}/`. Done when the exact command/target and `{slug}` are both fixed.

2. **Run it for real via the `run` skill.** Invoke `run` (Skill tool) against the target so it's actually launched and driven, not guessed at or summarized from memory. Save every real artifact it produces — stdout/stderr, generated files, screenshots, logs — under `run-n-view/{slug}/raw/`. Done when every artifact the run produced is saved on disk under `raw/`.

3. **Build the gallery in a subagent.** Dispatch a subagent (Agent tool, claude-sonnet-5 model, `run_in_background: false`) pointed at `run-n-view/{slug}/raw/` with the instruction: "with /viewpoints, build a gallery over <describe the raw output>, output to `run-n-view/{slug}/gallery/`." Isolating this keeps viewpoints' own profiling/shortlisting/rendering legwork out of the main run; `run_in_background: false` is required because step 4 reads the gallery's output. Done when `run-n-view/{slug}/gallery/index.html` exists on disk — confirm with a file check, not the subagent's summary alone.

4. **Report.** Tell the user where the raw output (`run-n-view/{slug}/raw/`) and the gallery (`run-n-view/{slug}/gallery/index.html`) live, and how to open the gallery — run `gallery/serve.sh` if viewpoints produced one, otherwise open `index.html` directly.
