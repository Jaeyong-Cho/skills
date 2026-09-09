---
name: to-context
description: Run both session capture skills to preserve verified facts and user intent as paired context documents. Invoke as /to-context.
disable-model-invocation: true
---

# To-Context

Create a complete session context by running both specialized capture skills.

1. Invoke `@skills/to-facts`.
2. Invoke `@skills/to-intents` after it completes.
3. Keep the same confirmed destination and session slug for both outputs. The paired files are `contexts/{NN}-facts-{slug}.md` and `contexts/{NN}-intents-{slug}.md`.

Completion criterion: both files exist in the same `contexts/` directory and use the same `NN` and `{slug}`.

Tell the user both file paths when done.
