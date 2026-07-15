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

## Understanding gaps

Sometimes a node can't be split correctly because a real piece of information is missing — not indecision, a genuine unknown the split depends on. Don't guess at children you can't yet name correctly. When it surfaces, turn the gap into its own node under whichever parent you were splitting when you hit it: `[?] {path}: Understand {the unknown}`.

- If the answer would change how the rest of *that same parent's* children get named, it blocks: insert it as the parent's first child, stop there, and only finish naming the parent's remaining children once it's answered.
- If the parent's other children don't depend on the answer, name them too and add the understand-node alongside as one more sibling under that parent.
- Understand-nodes resolve manually, outside the tree: whoever finds the answer reports it back, the node is checked off with the answer recorded inline, and drilling resumes from there.
- Understand-nodes are atomic — they don't get split further. If answering one surfaces a second unknown, that's a new understand-node, not a child of the first.

### Example
```
Root: Make Tetris
- [x] A: Make main menu
- [ ] B: Make ranking system
  - [?] B0: Understand whether ranking needs online sync
- [ ] C: Make game logic
```
The root split into A, B, C didn't need this answer — menu, ranking, and game logic are MECE regardless of how ranking works internally. The gap only surfaced one level down, while drilling into B: a synced ranking system and a local-only one decompose into different children (sync service, conflict resolution, vs. just local score storage), so B0 blocks — B gets no other children until it's answered. Once it is, B splits for real using that answer, same as any other node.
