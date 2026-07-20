---
name: get-me
description: Interview the user about a plan or design like /grilling, but check recorded preferences first and skip any question already answered by one; record new standing preferences as they're confirmed. Use when req/archi (or anything else) needs a grill that doesn't re-ask settled preferences, or uses 'get-me' trigger phrases.
---

# Get-Me

Interview me relentlessly about every aspect of this plan until we reach a shared understanding, but don't ask what's already settled by a recorded preference. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Before asking a question, check for a recorded preference that already answers it: search `../preferences/**/*.md` (cross-project — general engineering/style rules that hold regardless of which project this is) and `.context/preferences/**/*.md` (this project's own recorded choices) for a matching topic. If one answers the branch, apply it directly and say so inline (e.g. "Using recorded preference `<topic>`: ...") instead of asking — move straight to the next branch.

Ask one question at a time for anything not already answered. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead. Check for a knowledge graph first — `.ua/knowledge-graph.json` or legacy `.understand-anything/knowledge-graph.json` — and query it via `understand-chat` before falling back to raw Read/Grep.

After getting an answer, decide whether it's a one-off for this plan or a standing rule that would apply beyond it — see `../references/preference-format.md` for the standing-vs-one-off test. Don't ask the human to classify it — decide and record it yourself; they can edit or delete the file directly if it's wrong.

Record a standing rule per `../references/preference-format.md` (file location and entry format).
