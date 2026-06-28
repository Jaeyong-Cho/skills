---
applyTo: "**"
---

# Global Instructions

## Project Intents

Before executing any skill, check if a `source-of-truth/` directory exists in the current project root. If it does, read all files in it and let them guide how the skill behaves — they describe the human's goals, priorities, and constraints for this project.

## Wiki

`source-of-truth/wiki/` is a shared knowledge base. Any skill, at any time, can write useful truths to it — domain facts, constraints, key decisions, or anything that should persist across sessions. Files use the format `{timestamp}-{slug}.md`. Read it at the start of every skill for context.