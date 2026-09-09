---
name: to-intents
description: Capture the session's user intent — goals, desired outcomes, motivations, constraints, and boundaries — in a reusable context file. Use when the user wants intent recorded, requirements clarified for a fresh agent, or a session's desired outcome preserved. Invoke as /to-intents.
---

# To-Intents

Turn the conversation's intent into a source of truth instead of leaving it in chat history.

1. **Follow document style.** Read `../references/document-style.md` first — its structure and size limits govern the draft.
2. **Scope the session** — reread it in full. Extract:
   - **Primary intent:** what the user is trying to accomplish.
   - **Desired outcome:** what should be observably true when the intent is satisfied.
   - **Motivation:** why the user wants it or why now.
   - **Constraints and preferences:** limits, required technologies, style, scope, or priorities the user stated.
   - **Non-goals:** what the user explicitly does not want or what is out of scope.
   - **Decisions and open questions:** settled choices and unresolved choices that affect the intent.
   Completion criterion: every category has traceable content or is explicitly marked empty; do not fill gaps with guesses.
3. **Separate intent from context.** Keep implementation facts, research findings, and session history out unless they define a constraint or clarify the desired outcome. Mark each inferred intent as `[inferred]`; treat unstated intent as unknown rather than fact.
4. **Draft the document.** Use key-value blocks for Primary intent, Desired outcome, and Motivation. Use bullets for Constraints and preferences, Non-goals, Decisions, and Open questions. Preserve exact file paths, commands, identifiers, and user wording where ambiguity matters. Do not invent requirements.
5. **Write it.** If this session already wrote a `contexts/{NN}-intents-{slug}.md` file, update it in place with the latest intent instead of creating another one. If the matching `contexts/{NN}-facts-{slug}.md` file already exists, reuse its `NN`; otherwise use the next unused zero-padded sequence number in the chosen `contexts/` directory, starting at `01`. **MUST ASK** confirmation of the directory first when neither file exists, per `../references/question-format.md`'s ❓/➡️ format — recommend the current directory (`./contexts/`) as the default, unless the user asks to file it under the wiki instead, in which case read `../references/research-topic-directory.md` first and confirm the topic directory; skip re-asking if already confirmed earlier this session. Once confirmed, write to `./contexts/{NN}-intents-{slug}.md` (creating `contexts/` if needed) or `{topic-NN}-{topic-slug}/contexts/{NN}-intents-{slug}.md` under `~/wiki/today/research/`, whichever was confirmed. Wiki documents MUST include the OKF frontmatter required by `../references/document-style/frontmatter.md`.

Completion criterion: the file exists, and a fresh reader with zero session history can state what the user wants, why, the boundaries, and what remains undecided without opening the chat transcript.

Tell the user the file path when done.
