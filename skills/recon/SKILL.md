---
name: recon
description: Recon a goal in parallel — dispatch haiku scouts to explore its sub-questions and sonnet probes to experiment where exploring alone can't resolve them, then synthesize one answer. Invoke as /recon.
disable-model-invocation: true
---

# Recon

Given a goal, gather the information needed to answer it with a team instead of researching alone: dispatch parallel haiku scouts to explore its sub-questions and sonnet probes to experiment on the ones exploring can't resolve, then converge on one evidence-backed answer.

Recon investigates only — scouts and probes never edit product code. `/experiment` probes may run throwaway scripts to test a hypothesis, but any product-code fix belongs to a separate follow-up, not this skill.

1. **Claim the directory and decompose.** Pick a kebab-case slug for the goal and the next `{NN}` (count existing `NN-*` dirs under `~/wiki/today/research/`); `mkdir -p` that directory. Split the goal into independent sub-questions — each answerable on its own, together covering the goal — and number them `01, 02, ...`, each with its own kebab-case slug. Completion criterion: a numbered list of sub-questions covering the goal, plus the claimed directory.

2. **MUST DISPATCH scouts.** For every sub-question, dispatch a separate `subagent_type: general-purpose`, `model: haiku` subagent, all in one batch (parallel — never one at a time). Instruct each one: run `/explore` (Skill tool) for this exact sub-question, but stop at its search step only — if that can't resolve it, report back "unresolved" instead of escalating to `/experiment` itself. Give it the exact file to write: `.../{NN}-{slug}/explores/{nn}-{sub-slug}.md` (its own pre-assigned `{nn}`, so parallel writes never collide). Do not use the `Explore` agent type — it lacks Write access and can't save the file. Completion criterion: every sub-question comes back either answered-with-evidence or flagged unresolved.

3. **MUST DISPATCH probes.** For every sub-question flagged unresolved in step 2, dispatch a separate `subagent_type: general-purpose`, `model: sonnet` subagent, all in one batch (parallel). Instruct each one: run `/experiment` (Skill tool) for this exact sub-question, writing to `.../{NN}-{slug}/experiments/{nn}-{sub-slug}/` (same pre-assigned `{nn}`). Skip this step entirely if step 2 left nothing unresolved. Completion criterion: every flagged sub-question has a stated verdict (supported/refuted/inconclusive).

4. **Synthesize.** Combine every sub-question's answer (scouts and probes) into one answer to the original goal, per `../references/document-style.md`. If this session already wrote a `recon/{nn}-{slug}.md` file for the same goal, update that file in place with the new synthesis instead of creating another one. Otherwise write to `.../{NN}-{slug}/recon/{nn}-{slug}.md`, `{nn}` the next zero-padded sequence number inside `recon/` (count existing files there; starts at `01`). Completion criterion: the file exists, cites every sub-question's finding, and states a direct answer to the goal (or names what's still open).

Completion criterion: the goal has a written, evidence-backed answer filed under the research directory — every sub-question accounted for as answered, refuted, or explicitly open.
