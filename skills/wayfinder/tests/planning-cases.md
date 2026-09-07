# Wayfinder / To-Way behavioral checks

Run each case in a fresh session with the current skill text. These are behavioral acceptance cases, not an automated model test. Judge planning meaning, not exact titles, IDs, or task counts. For planning cases, answer the grill-me rounds and explicitly confirm the shared-understanding summary before evaluating the final plan. For recording checks, use a temporary destination, never the original wiki output.

## 0. Grill-me launches and gates finalization

Use the modal-editing input from case 1. Inspect the conversation before answering, then continue through confirmation.

Pass when:

- Wayfinder reads and runs grill-me itself in the current conversation, rather than asking the user to invoke it or immediately returning a final plan.
- Its first question calibrates understanding of the editor goal using a concrete scenario, an H1 question, and a wait for the answer. Essential teaching and teach-back precede decision rounds.
- The interview covers the goal's success/scope, the proposed ways and their boundaries, consequential unknowns, and dependency/parallel constraints—not Wayfinder configuration or a lifecycle checklist.
- Grill-me's mode selection and question framework are reused, not replaced by a second questionnaire.
- Draft ways evolve with answers. If the user changes explicit saving to autosave, affected tasks and dependencies are revised rather than retaining a stale explicit-save plan.
- “You decide” keeps recommendations provisional and does not turn uninspected file-policy assumptions into evidence or trigger an experiment.
- The summary includes the goal, ways, execution constraints, and remaining blockers. No final plan, implementation, or recorded files appear before user confirmation.
- A correction to the summary reopens affected decisions. Confirmation of an explicitly partial plan preserves its blockers.

## 1. Modal editing: concrete work and dependency-driven parallelism

Input:

> Plan modal ASCII insertion and explicit saving for an existing editor. Normal navigation and rendering already work. Insertion must only change text in insert mode and keep the cursor valid. Write must save the current buffer without quitting. A failed save must preserve the original file and recoverable in-memory edits. Buffer, command loop, and file writer are separate modules. The save request/result contract is not agreed yet. Supported paths and symlink/metadata preservation policy are unknown. Treat these as supplied facts, not as code you inspected.

Pass when:

- No repeated requirements/design/implement/test chains or renamed one-child wrappers appear.
- Every executable leaf has Why (the outcome/risk and consequence of omission), What (a scoped result, not a repeated title), How (concrete approach/steps), and a separate observable completion signal.
- How names meaningful actions such as tracing mode dispatch and checking the same key in both modes—not a generic lifecycle chain. Unknown file policy blocks selection of a persistence mechanism rather than inviting a guessed implementation.
- Existing navigation/rendering is reused; relevant regressions are checked rather than planned as new capabilities.
- File-policy uncertainty has a resolving action, an exit signal, affected work, and consequences for different answers.
- Save-contract agreement is a shared prerequisite, not duplicated in command and writer branches.
- Buffer work can begin without waiting for file policy. Command work can begin after its contract is agreed without waiting for the writer.
- Command/writer parallelism names the settled contract and separate-module boundary; end-to-end validation joins the relevant editing, command, and persistence tasks.
- No proposed inspection/experiment is claimed as evidence already obtained.

## 2. Small, already-understood change

Input:

> Change the existing settings label from "Colour" to "Color". There is one occurrence, no localization, no generated files, and no behavior change. The existing UI snapshot must reflect the new label. These facts are confirmed; plan only.

Pass when: a small concrete task with a snapshot completion check suffices; no invented discovery/design work, uncertainty, sub-way wrappers, or parallel lanes. Why explains the requested spelling consistency; What scopes the label change without behavior changes; How says to replace the label and update/check the existing snapshot, without padding the task into phases. Recording needs only `0-goal.md`, with the task inline.

## 3. A blocked branch and a shared write surface

Input:

> Add a local score display and a leaderboard. Local score calculation already exists. The owner has not decided whether the leaderboard is local-only or online; that answer changes the architecture. Score display and leaderboard UI both modify the same screen module. Do not assume isolation or a settled shared UI contract.

Pass when:

- Leaderboard scope has an owner question with consequences and a recommendation, not an invented decision.
- The affected leaderboard branch stays partial; guessed sync/auth/database tasks do not appear.
- Local score display can proceed independently of that decision.
- UI implementation is not promised as safe parallel work merely because it belongs to separate ways; the shared file conflict is explicitly sequenced or conditioned on an isolation/integration strategy.

## 4. Recording and invalid-source handling

Record a valid result of case 1 with `/to-way` in a confirmed temporary directory.

Pass when:

- Root/ways have files; task, uncertainty, and checkpoint leaves have inline anchors, not separate files.
- Every source node has one canonical location; the root links the whole hierarchy.
- Every dependency link resolves to the original ID and keeps its reason. Why/What/How details (including ordered steps, scope boundaries, and evidence references), uncertainty resolution details, completion signals, statuses, and parallel conditions survive unchanged.
- Numbering follows source presentation order without introducing serial prerequisites; nested ways use full ancestry without path collisions.
- A blocked partial plan from case 3 can also be recorded without filling its missing branch.

Negative checks (each must stop before writing and request source correction):

- Supply the legacy modal-editing tree consisting of repeated requirements/design/implement/test leaves.
- Remove a task's Why, What, How, completion signal, or prerequisites field without explicitly marking a partial branch. Missing detail must not be silently invented by the recorder.
- Replace Why with “needed for the feature,” What with only the title, or How with “design, implement, test.”
- Add a dependency on an absent ID, or introduce a dependency cycle.
- Mark a task ready despite its unresolved prerequisite, or assert parallelism across a dependency path.

Update check: place old task files or human completion annotations in the destination. Recording must not silently delete them, overwrite their evidence, or report completion while leaving contradictory legacy files mixed with the new plan.
