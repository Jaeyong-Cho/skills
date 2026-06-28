---
applyTo: "**"
---

# Global Instructions

## Project Intents

Before executing any skill, check if a `source-of-truth/` directory exists in the current project root. If it does, read all files in it and let them guide how the skill behaves — they describe the human's goals, priorities, and constraints for this project.

## Implementation Gate

Do not implement, write code, or make changes until the user explicitly confirms they are satisfied with the plan. Before any implementation:

1. Discuss the plan fully — what will change, why, and how
2. Ask questions until every ambiguity is resolved
3. Wait for explicit approval ("looks good", "do it", "go ahead", or similar)

If the user is not satisfied, keep discussing. There is no limit on how long the discussion goes. Do not proceed to implementation until the user says so.
