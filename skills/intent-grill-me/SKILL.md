---
name: intent-grill-me
description: Run a @skills/grill-me interview to uncover the real intent behind a request — motivation, need, pain/friction, desired outcome, constraints, assumptions — before any current-state, problem, or solution work starts. Writes the result to intents.md. First stage of the intent-to-cycle skill set. Invoke as /intent-grill-me.
disable-model-invocation: true
---

# Intent Grill Me

**MUST RUN** `@skills/grill-me` covering every point in `../references/intent-checklist.md`, starting from the exact request the user just made. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms.

## Impact Level and Uncertainty

Read `../references/grill-impact.md` first — ask its Mode question before round 1, then its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark for the rest of this session.

For every point in `../references/intent-checklist.md`: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round. **MUST NOT** silently drop any checklist point — every one appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST show evidence, not just a conclusion.** Every `Decision:` line and every `➡️` recommended answer cites what it's based on — a file:line, a grep/command output, or an existing pattern found in the repo — found by a sub-agent per `@skills/grill-me`'s "Finding facts is your job" rule, not asserted from memory. No evidence found → say so and mark uncertainty High instead of guessing.

**MUST NOT** cover scope-in/scope-out, architecture, root cause, or release plan — those belong to `@skills/dev-grill-me` / `@skills/req-grill-me`, once the intent behind the request is settled. This skill stops at *why* and *what outcome*, never *how*.
**MUST NOT** start any current-state exploration or solution work before the frontier is empty.

## Write it

Once the frontier is empty, **MUST ASK** confirmation of the file path, per `../references/question-format.md`'s ❓/➡️ format — recommend the current directory (`./intents.md`) as the default, unless the user asks to file it under the wiki instead, in which case read `../references/research-topic-directory.md` first and confirm the `{NN}-{slug}` topic directory the same way (`~/wiki/today/research/{NN}-{slug}/intents.md`). Skip re-asking if already confirmed earlier this session.

Once confirmed, write it as an OKF document per `../references/document-style/frontmatter.md`: the six-field frontmatter block (`type: Research Intent`, `title`, `description`, `tags`, `timestamp`; omit `resource` — no canonical URI here), followed by one section per `intent-checklist.md` point (Explicit request, Intent/motivation, Need, Pain/friction, Desired outcome, Constraints, Assumptions), each carrying its impact/uncertainty tag and evidence, and marking any assertion-worthy assumption. Do not add `hit_count`/`last_hit_at`/`created_at`/`owner` — those are the extended `~/wiki/kb` schema, and only `@skills/to-kb` writes them; this is a per-topic research artifact, not a KB entry.

## Lint it

Run `python3 ../to-kb/scripts/lint_kb.py --plain {path to intents.md}` (relative to this skill's directory) — checks the frontmatter carries all five plain-OKF fields and the file isn't oversized. Fix every reported error and re-run until clean.

Completion criterion: `intents.md` exists at the confirmed path, carries valid OKF frontmatter, `lint_kb.py --plain` is clean, every checklist point has a section, nothing left silently assumed.

Once complete, tell the user the file path. Next step in this skill set (current-state capture, problem definition) is not built yet — say so rather than inventing it.
