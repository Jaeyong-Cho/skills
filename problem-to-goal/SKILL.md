---
name: problem-to-goal
description: Convert a defined problem into a clear, actionable goal. Use when user has a problem statement and wants to know what to aim for, says "what should my goal be", "turn this into a goal", "what does success look like", or invokes /goal. Works well after /problem or /clarify defines the root problem.
---

# Problem to Goal

## Core idea

Problem = gap between current state and expected state.
Goal = the expected state, made concrete and achievable.

## Process

### 1. Get the problem
If not provided, ask: "What is the problem?"

### 2. Find the expected state
Ask: "When this problem is solved, what does the situation look like?"
- Probe until user can describe a concrete picture of success.
- If answer is vague ("things are better"), push: "What specifically is better? What can you do then that you can't now?"

### 3. Check the expectation
- "Is that expected state realistic?"
- "Is it in your control?"
- If not realistic → adjust expected state first, then form goal.

### 4. State the goal
Write goal in one sentence:
> "Goal: [achieve X] by [doing Y] so that [problem Z is gone]."

Confirm with user.

### 5. Make it actionable
Ask: "What is the first concrete step toward this goal?"
- One action, doable now or this week.
- Output: goal statement + first step.
