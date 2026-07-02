# Global Instructions

## Project Intents

Before executing any skill, check if a `.sot/` directory exists in the current project root. If it does, read all files in it and let them guide how the skill behaves — they describe the human's goals, priorities, and constraints for this project.

## Workflow Scope

All skills apply to both new development and fixing existing things. `/attack` finds weaknesses in existing code. `/directing` can direct a fix as easily as a new feature. `/planning`, `/action`, and `/evaluate` work the same way regardless of whether the work is greenfield or remediation.

## Wiki

`.sot/wiki/` is a shared knowledge base. Any skill, at any time, can write useful truths to it — domain facts, constraints, key decisions, or anything that should persist across sessions. Files use the format `{timestamp}-{slug}.md`. Read it at the start of every skill for context.