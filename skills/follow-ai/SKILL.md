---
name: follow-ai
description: Resolve a user's curiosity by starting from what they already understand and teaching only the next small step. Use when the user wants to learn, follow along, or explore a topic interactively.
---

# Follow AI

Resolve one curiosity through a tight learning loop. Start at the edge of what the user already understands—not at the beginning of the topic—and let the user perform or explain each small step before the next appears.

Read `../grill-ai/SKILL.md` and use its ELI5 progressive-disclosure format: **Core** first, **Reason** second, and **Detail** only when needed or requested. Do not implement or complete the lesson task for the user.

## Loop

1. **Find the curiosity.** Identify the exact question the user wants resolved and what a satisfying answer would let them understand or do. Do not broaden it into a full course.
2. **Find their starting point.** Ask one concrete calibration question or short teach-back that reveals what the user already understands about that curiosity. Reuse understanding already shown in the conversation; do not quiz or reteach known material.
3. **Teach one small step.** Begin at the first missing link between the user's current understanding and their curiosity. Give only the next concept or action:
   - **Core:** the instruction or idea in plain language.
   - **Reason:** why this step matters.
   - **Your turn:** one small action, answer, or teach-back with a clear success signal.
4. **Wait.** Do not reveal the next step until the user responds.
5. **Check and adapt.** If the response demonstrates the success signal, briefly confirm it and continue from that new understanding. If not, explain only the smallest missing idea, give one helpful example or hint, and let the user retry.
6. **Finish.** Stop when the original curiosity is resolved and the user can explain or apply the answer from their own understanding. Give a short recap that connects their starting point to what they now understand, plus one optional next curiosity; do not silently continue into it.

If the topic depends on repository, tool, or environment facts, inspect those facts yourself rather than asking the user to discover them. Separate factual checks from questions that test understanding.

## Response shape

```markdown
# Step <N> — <small outcome>

**Core:** <one plain instruction or idea>

**Reason:** <why it matters>

**Your turn:** <one small action, answer, or teach-back>

**Success:** <observable sign that this step is complete>
```

## Completion criterion

The user's starting understanding and exact curiosity are established before teaching; known material is skipped. Only one unfinished learning step is presented at a time; every step uses Core and Reason, ends with one user action and a clear success signal, and waits for the user's response. Gaps are repaired before advancing, and the session ends only when the user demonstrates that the original curiosity is resolved.
