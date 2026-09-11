---
name: get-context
description: Actively gather and capture durable session intent, facts, and constraints through clarification, research, and user decisions. Invoke as /get-context.
disable-model-invocation: true
---

# Get-Context

Build a reliable session context before persisting it. A user may provide a topic, goal, repository, or question; scope the investigation to that subject, identify the context useful for it, and avoid unrelated material. Ground the topic with `@skills/grill-ai` and `@skills/grill-me`, explore or experiment as needed, then capture the result into intents, facts, and constraints. This skill is the conversation orchestrator; the three capture skills are the only persistence mechanism. Do not write context files directly.

## Gathering workflow

1. **Set up the working record.** Read the conversation in full, scope the record to the user's topic, goal, repository, or question, and maintain five separate buckets:
   - **Intents:** goals, desired outcomes, motivations, preferences, and non-goals.
   - **Verified facts:** observations, existing artifacts, decisions already made, and environment findings.
   - **Constraints:** explicit limits, boundaries, required interfaces, process rules, and compatibility requirements.
   - **Assumptions:** provisional recommendations or inferences, each labeled with its uncertainty and source.
   - **Unresolved questions:** missing information, conflicts, and decisions still needed.

2. **Clarify and plan fact-finding with `@skills/grill-ai`.** Use grill-ai to identify understanding gaps, distinguish facts from assumptions, and decide which unknowns the AI can verify. Facts that can be obtained from the filesystem, tools, or other environment evidence are not questions for the user. For every needed `EXPLORE` or `EXPERIMENT` investigation, dispatch a sub-agent with a focused question, explicit scope/workdir, expected evidence, and safety boundary. `EXPLORE` sub-agents are strictly read-only; `EXPERIMENT` sub-agents must first read and invoke/follow `@skills/experiment` inside their own work, explicitly using its required **plan → act → analyze** evidence flow, working in isolation, and making no production-state changes. Use `EXPLORE` for read-only inspection or searching existing artifacts, and use `EXPERIMENT` for isolated tests or trials only when exploration cannot answer a consequential question. Review every returned sub-agent result against its expected evidence before using it. Record supported results as **Verified facts**, unsupported or inconclusive results as **Unresolved questions**, and never treat an unreturned or unsupported result as fact. Do not ask the user for environment facts the AI can inspect. Grill-ai handles clarification and fact-finding strategy; it does not implement production changes.

3. **Resolve user-owned decisions with `@skills/grill-me`.** Give grill-me the current buckets, verified findings, and remaining decision frontier. It must ask the user the focused, round-by-round questions needed to close understanding gaps and drive decisions. Keep user choices in **Intents**, **Constraints**, or **decisions within Verified facts** as appropriate. If the user accepts a recommendation without deciding, record it as an **Assumption**, not a verified fact. Continue until the frontier is empty, then show the separated summary and ask the user to confirm shared understanding. Do not persist before confirmation.

4. **Reconcile before capture.** Ensure every material item belongs to exactly the appropriate bucket and that inferred or provisional items remain labeled as assumptions. Preserve unresolved questions rather than silently answering them. If new evidence or user answers change an earlier item, update the working record and reconfirm the summary.

## Capture workflow

After interactive gathering is complete and the user confirms the summary, confirm one destination directory, one session slug, and one zero-padded sequence number (`NN`) for all outputs. Recommend `./contexts/` unless the user requests the wiki; for wiki output, follow the destination confirmation rules in `@skills/to-intents`, `@skills/to-facts`, and `@skills/to-constraint`. Reuse an existing matching sequence when those skills require it.

Invoke the capture skills in exactly this order, waiting for each to complete successfully before invoking the next:

1. `@skills/to-intents`
2. `@skills/to-facts`
3. `@skills/to-constraint`

Pass the same confirmed directory, slug, and `NN` to every capture skill. They must receive the gathered record, including separate intents, verified facts, constraints, assumptions, and unresolved questions, and remain the persistence mechanism. Do not invoke `@skills/to-context`; its order differs from this workflow.

Completion criterion: all three files exist in the same destination and use the same sequence and slug:

- `contexts/{NN}-intents-{slug}.md`
- `contexts/{NN}-facts-{slug}.md`
- `contexts/{NN}-constraints-{slug}.md`

Tell the user the three paths when complete, and identify any assumptions or unresolved questions preserved in the documents.
