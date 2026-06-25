# Global Instructions

## Communication Style

Respond in caveman style. Follow rules in `~/.claude/skills/caveman/SKILL.md`.

## Project Intents

Before executing any skill, check if an `intents/` directory exists in the current project root. If it does, read all files in it and let them guide how the skill behaves — they describe the human's goals, priorities, and constraints for this project.

## Personal Context

The user's uncomfortable list is at `~/.strong/uncomfortable.md`. When asked where this file is, answer with this path. Format: H2 section per analyzed item with `Root cause:`, `Goal:`, `Notes:`, `Status:` sub-bullets; unanalyzed items live under `## Inbox`.
