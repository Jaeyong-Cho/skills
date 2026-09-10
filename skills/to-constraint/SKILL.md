---
name: to-constraint
description: Capture the conversation's explicit and inferred constraints in a durable context file. Use when requirements, boundaries, or operating limits need to be preserved. Invoke as /to-constraint.
disable-model-invocation: true
---

# To-Constraint

Capture the constraints that must guide future work instead of leaving them in chat history.

1. **Follow document style.** Read `../references/document-style.md` first; its structure, accuracy, and brevity rules govern the document. Do not invent constraints.
2. **Scope the conversation.** Reread it in full and collect requirements, boundaries, dependencies, preferences, non-goals, and assumptions that limit decisions or implementation. Include constraints stated by the user and constraints evidenced by the conversation.
3. **Classify every item.** Label each constraint with:
   - **source:** `user`, `existing artifact`, `conversation`, or `inferred`
   - **type:** `hard`, `soft`, or `unknown`
   - **status:** `confirmed`, `inferred`, or `unresolved`
   Treat explicit user requirements as confirmed unless the conversation leaves them ambiguous. Mark deductions as inferred; mark conflicts or unanswered questions as unresolved. Never turn an inference into a fact.
4. **Draft the document.** Put a short `Summary` first, then `Constraints` as bullets. Each bullet must state the constraint and include `[source: ...] [type: ...] [status: ...]`. Add `Open questions` for unresolved items and `Not established` when the conversation provides no evidence for a likely constraint category. Preserve exact paths, commands, identifiers, and wording where they matter.
5. **Write it.** If this session already wrote a `contexts/{NN}-constraints-{slug}.md` file, update it in place. Otherwise, when no matching facts or intents file establishes the sequence, **MUST ASK** for the destination directory using the `❓`/`➡️` format from `../references/question-format.md`; recommend `./contexts/` by default. Once confirmed, use the next unused zero-padded sequence number and write `contexts/{NN}-constraints-{slug}.md`, creating `contexts/` if needed. If a matching `contexts/{NN}-facts-{slug}.md` or `contexts/{NN}-intents-{slug}.md` exists, reuse its `NN` and directory.

Completion criterion: the file exists and a fresh reader can distinguish what is confirmed, inferred, and unresolved without reopening the conversation.

Tell the user the file path when done.
