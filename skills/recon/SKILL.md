---
name: recon
description: Explore a repository and safely experience its behavior with parallel sub-agents, then report verified facts, conflicts, and unknowns to the human.
disable-model-invocation: true
---

# Reconnaissance

Answer a concrete question with evidence before planning or changing code. Recon is fact-finding, not implementation, design, or recommendation.

## Input

- Target: repository, directory, feature, command, or behavior to investigate.
- Question: what the human wants to know.
- Constraints: commands, paths, environments, or runtime actions that are allowed or forbidden.

If the target or question is missing, ask one concise clarification. Do not silently broaden the target.

## Safety boundary

- Do not edit files, commit, push, install dependencies, delete data, or change durable external state.
- Runtime probes must be minimal and safe. Do not run a command merely because it is conventional.
- Do not make network calls unless the human explicitly authorizes the specific call.
- Keep facts separate from inferences, recommendations, and unknowns.
- Preserve exact paths, commands, exit codes, and relevant output as evidence.
- If a useful probe is unsafe, unavailable, or unauthorized, report it as unperformed instead of guessing.

## Recon workflow

### 1. Frame the investigation

State the question, target boundary, allowed runtime actions, and what evidence would answer the question. Read repository instructions and relevant entrypoints before delegating. Do not ask the human for facts you can inspect.

### 2. Run a bounded parallel sub-agent fanout

Use one fresh-context `workflowScript` with at least these independent lanes:

- `recon-explorer`: static repository exploration — files, symbols, configuration, documentation, call paths, and contradictions.
- `recon-experiencer`: safe runtime experience — existing tests, CLI/API probes, and observable behavior with exact commands and results.

Do not impose a two-agent ceiling. Add lanes whenever the question has independent fact clusters that benefit from separate evidence, for example:

- dependency/configuration mapping;
- test and failure-path behavior;
- data-flow or integration boundary tracing;
- history, ownership, or migration evidence;
- security, performance, or user-flow probing when materially relevant.

Use the smallest number of lanes that covers the question. Each additional lane must have a distinct target, evidence source, and output question; do not clone prompts with only a label changed. Reuse `recon-explorer` or `recon-experiencer` for additional lanes when no dedicated custom agent exists. Keep every lane read-only and bounded by the investigation question.

Build the `runs.all` list from those distinct lanes and await every child:

```js
const lanes = [
  { key: "explore-structure", agent: "recon-explorer", task: "<target, question, cwd, static structure contract>" },
  { key: "experience-behavior", agent: "recon-experiencer", task: "<target, question, cwd, safe runtime contract>" },
  // Add only independently useful lanes, each with a distinct task.
];
const results = await runs.all(lanes);
return results.map(result => result.output);
```

Every task must include the exact target, question, repository `cwd`, authority boundary, and required evidence-ledger format. Launch the workflow asynchronously, then wait for all completion results before reporting facts. If a required recon agent is unavailable, stop and report that `./install.sh` must install the recon agents; do not silently substitute an unbounded agent.

### 3. Synthesize without guessing

Compare the two ledgers. Report:

- **Observed facts** — statements directly supported by a path, command, exit code, output, or behavior.
- **Corroborated facts** — facts supported independently by both lanes.
- **Conflicts** — static/runtime or agent disagreements, with both pieces of evidence.
- **Unknowns** — questions neither lane established.
- **Unperformed probes** — useful checks skipped for safety, authorization, or environment reasons.
- **Smallest next probe** — only when it would resolve a material unknown.

Do not average conflicting evidence. Inspect the relevant source or run one narrower safe probe to resolve it.

## Human report

Use this format:

```markdown
# Recon: <target>

## Question
<the exact question>

## Scope and method
<what was inspected and which safe probes were run>

## Facts
| ID | Fact | Evidence | Confidence |
|---|---|---|---|
| F1 | ... | `<path>` / `<command>` / exit code / output | observed / corroborated |

## Conflicts
<None, or each conflict with both sources>

## Unknowns
<None, or the unresolved questions>

## Unperformed probes
<None, or the skipped probes and why>

## Next smallest probe
<None, or one safe, concrete next action>
```

Do not include implementation plans or fixes unless the human asks for them after the fact report.

## Completion criterion

The human receives a concise report whose material claims are evidence-backed, static and runtime evidence are distinguished, conflicts are explicit, unknowns are not disguised as conclusions, and no repository or durable external state was changed.
