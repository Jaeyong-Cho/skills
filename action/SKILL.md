---
name: action
description: Action skill. Reads the ADR and executes the action sequence one step at a time with user confirmation. Use when invoked as /action.
disable-model-invocation: true
---

# Action

Read the ADR to execute from `source-of-truth/adr/`. If multiple ADRs exist, list them and ask the user which to use. If one exists, use it.

Use this for new implementation or for applying a fix — the ADR's action sequence may describe either.

Work through the Action Sequence one step at a time:

1. State what you are about to do — one plain sentence the user can understand without reading the code.
2. Wait for explicit confirmation before proceeding.
3. Execute that one step only. Nothing adjacent, nothing noticed nearby.
4. Report what changed in one sentence.
5. Move to the next step.

Never execute more than one step without confirmation. If a step is blocked or ambiguous, stop and ask — do not skip or improvise.

Completion criterion: every step in the Action Sequence is done and confirmed, or the user explicitly stops. When done: "Action sequence complete. Run `/evaluate` to assess the result."

Any useful truth discovered during this session — a constraint, a domain fact, a key decision — can also be written to `source-of-truth/wiki/` at any time.
