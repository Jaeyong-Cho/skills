---
name: problem-decompose
description: Decompose a problem top-down into one level of direct sub-problems. Use when user has a defined problem and wants to break it down, says "what are the sub-problems", "break this down", "decompose", "top-down", or invokes /decompose. Works well after /problem or /clarify defines the root problem.
---

# Problem Decompose

## Goal

Given a root problem, find the direct sub-problems that together fully explain it. One level only — no recursion.

## Process

### 1. Get the root problem
If not provided, ask: "What is the problem to decompose?"

### 2. Decompose
Ask: "What are the direct causes or parts that make up this problem?"
- Probe until 3–6 sub-problems surface
- Each sub-problem must be:
  - **Direct** — one hop from root, not a grandchild
  - **Distinct** — no overlap with other sub-problems
  - **Complete** — together they cover the root problem fully
- If user lists symptoms, push back: "Is that a sub-problem or a consequence?"

### 3. Present
Show as a simple tree:

```
Root problem
├── Sub-problem A
├── Sub-problem B
└── Sub-problem C
```

### 4. Confirm + Prioritize
Ask: "Does this cover it? Which sub-problem is most important to solve first?"

Output: confirmed tree + one highlighted priority sub-problem.
