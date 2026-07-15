# Top-Down-Depth-First

- Top-down depth-first is a methodology for making progress on tasks that are complex, difficult, or unfamiliar.
- From the top goal, drill down: at each node, decide what you need to understand and what you need to do next.
- Split each node into children that are MECE — Mutually Exclusive (no two children overlap in scope) and Collectively Exhaustive (together they cover everything the parent needed). A gap or overlap at one level compounds at every level below it.
- When you reach a leaf task — small enough to do immediately, with no unresolved dependency — complete it right away.
- This keeps you focused on one task at a time, avoids context switching, and gives you fast feedback as each leaf closes.
- So when starting toward a goal, go straight for the smallest actionable subtask and do it immediately, rather than mapping the whole tree first — descend one branch to a leaf and finish it before naming what's inside the next sibling.

## Example: Tetris

```
Root: Make Tetris
- A: Make main menu
  - A1: Make main menu UI
  - A2: Make game-start logic
  - A3: Make settings logic
  - A4: Make ranking-dashboard view logic
  - A5: Make exit logic
- B: Make ranking system
- C: Make game logic
```

A, B, C are MECE at the root: menu, ranking, and game logic don't overlap, and together they're everything Tetris needs. A's five children are MECE the same way one level down — UI, start, settings, ranking-view, and exit each own a distinct slice of the main menu, nothing else belongs there. Depth-first order: finish A1, then A2, then A3, A4, A5 — each already a leaf, one actor, one path, no "and" — before B or C get touched, even though B and C were named in the same breath as A.
