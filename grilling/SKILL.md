---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask one question at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead. Check for a knowledge graph first — `.ua/knowledge-graph.json` or legacy `.understand-anything/knowledge-graph.json` — and query it via `understand-chat` before falling back to raw Read/Grep.

Before interviewing, list the filenames in `../references/` and `../template/` (no need to read contents yet). If a branch of the interview touches a topic one of them covers, read that specific file then and let it inform your questions.
