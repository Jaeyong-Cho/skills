---
name: get-me
description: Interview the user about a plan or design like /grilling, but check recorded preferences first and skip any question already answered by one; record new standing preferences as they're confirmed. Use when req/archi (or anything else) needs a grill that doesn't re-ask settled preferences, or uses 'get-me' trigger phrases.
---

# Get-Me

Interview me about every branch of this plan until we reach a shared understanding, the same way `/grilling` does — but don't ask what's already settled. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Before asking a question, check for a recorded preference that already answers it: search `../preferences/**/*.md` (cross-project — general engineering/style rules that hold regardless of which project this is) and `.context/preferences/**/*.md` (this project's own recorded choices) for a matching topic. If one answers the branch, apply it directly and say so inline (e.g. "Using recorded preference `<topic>`: ...") instead of asking — move straight to the next branch.

Ask one question at a time for anything not already answered. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead. Check for a knowledge graph first — `.ua/knowledge-graph.json` or legacy `.understand-anything/knowledge-graph.json` — and query it via `understand-chat` before falling back to raw Read/Grep.

After getting an answer, decide whether it's a one-off for this plan or a standing rule that would apply beyond it. A standing rule is one you'd answer the same way next time regardless of which feature or project prompted it (an API design convention, a testing habit, a naming rule). A one-off is specific to this plan's own constraints (this feature uses Redis because this project already runs Redis). Don't ask the human to classify it — decide and record it yourself; they can edit or delete the file directly if it's wrong.

Record a standing rule by appending to (or creating) a topic file, kebab-case named after the rule's subject:
- `../preferences/{topic}.md` — true across any project (e.g. `../preferences/api-design.md`).
- `.context/preferences/{topic}.md` — true only in this project (e.g. `.context/preferences/tech-stack.md`).

Each entry is the rule stated as a decision, one line, e.g. `- Use plural nouns for REST resource endpoints.` Append under the file's existing bullets; if it's the first entry on that topic, create the file with just that line.
