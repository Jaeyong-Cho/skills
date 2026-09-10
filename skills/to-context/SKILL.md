---
name: to-context
description: Run the session capture skills to preserve verified facts, user intent, and constraints as paired context documents. Invoke as /to-context.
disable-model-invocation: true
---

# To-Context

Create a complete session context by running the specialized capture skills.

1. Invoke `@skills/to-facts`.
2. Invoke `@skills/to-intents` after it completes.
3. Invoke `@skills/to-constraint` after it completes.
4. Keep the same confirmed destination and session slug for all outputs. The paired files are `contexts/{NN}-facts-{slug}.md`, `contexts/{NN}-intents-{slug}.md`, and `contexts/{NN}-constraints-{slug}.md`.

Completion criterion: all three files exist in the same `contexts/` directory and use the same `NN` and `{slug}`.

Tell the user all three file paths when done.
