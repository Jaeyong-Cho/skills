# Goal Tree: {Title}

> Nested checklist, depth-first, leftmost-first. Indentation = depth. Siblings at each level must be MECE — mutually exclusive, collectively exhaustive (see `../references/top-down-depth-first.md`). Three states: `[ ]` pending action, `[?]` pending understanding — a named unknown blocking a correct split, resolved manually and recorded inline, not researched by the skill — `[x]` done. An action line is done once its RDR and ADR are committed; an understand line is done once its answer is recorded; a non-leaf line is done once every child under it is done. A leaf is a node reducible to one scenario, one actor, one path — describable without "and."

- [ ] Root: {goal text}
  - [ ] A: {goal text}
    - [ ] A1: {goal text}

e.g.
- [ ] Root: Make Tetris
  - [ ] A: Make main menu
    - [x] A1: Make main menu UI → rdr: `.context/req/main-menu-ui.md`, adr: `.context/adr/main-menu-ui.md`
    - [ ] A2: Make game-start logic
    - [ ] A3: Make settings logic
    - [ ] A4: Make ranking-dashboard view logic
    - [ ] A5: Make exit logic
  - [ ] B: Make ranking system
    - [?] B0: Understand whether ranking needs online sync
  - [ ] C: Make game logic
