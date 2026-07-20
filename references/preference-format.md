# Preference Format

Where a recorded preference lives, and how each entry is written. Used by `get-me` and `to-preference`.

## Standing vs one-off

A **standing** preference is one you'd answer the same way next time, regardless of which feature or project prompted it — an API design convention, a testing habit, a naming rule. A **one-off** is specific to this task's own constraints (this feature uses Redis because this project already runs Redis). Only standing preferences get recorded; one-offs stay in the session.

## File location

- `../preferences/{topic}.md` — true across any project. `{topic}` is a kebab-case slug of the rule's subject (e.g. `../preferences/api-design.md`).
- `.context/preferences/{topic}.md` — true only in the current project (e.g. `.context/preferences/tech-stack.md`).

## Entry format

Each entry is the rule stated as a decision, one line: `- Use plural nouns for REST resource endpoints.` Append under the file's existing bullets. If it's the first entry on that topic, create the file with just that line.
