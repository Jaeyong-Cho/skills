---
name: drill
description: Goal-decomposition skill. Drills a broad goal top-down into a persisted tree of narrower sub-goals, depth-first, until reaching a leaf small enough for /req. Use when invoked as /drill.
disable-model-invocation: true
---

# Drill

Manages a persisted goal tree so a broad goal never lands on `/req` in one oversized piece. Read `../references/top-down-depth-first.md` — the drill order below (descend one branch to a leaf, act, only then return to siblings) is that methodology applied to the goal tree. Read `.context/tree/` first.

**Starting a new tree:** if invoked with a goal argument, derive a kebab-case slug from it. If `.context/tree/{slug}.md` doesn't exist, create it from `../template/tree.md` with that goal as the root node and proceed to split it (below). If it already exists, ignore the argument and resume it instead.

**Resuming:** if invoked with no argument, look in `.context/tree/`. One file — resume it. Several — list them and ask the user which. None — tell the user to run `/drill {goal}` to start one, and stop.

**Finding the frontier:** walk the tree depth-first, leftmost-first. For each unchecked leaf, check whether it's actually done: its slug's RDR and ADR are committed (`.context/req/{slug}.md` and `.context/adr/{slug}.md` exist, with no unmerged draft left in `.context/rdr/` or `.context/adr/` for that slug). If done, check it off with links to those files, then continue the walk — a sibling if any remain unchecked, otherwise back up to the parent (checking the parent off too once every child is done) and on to the parent's next sibling. Stop at the first node that isn't done. If the walk reaches the end with everything checked off, tell the user the goal tree is complete and stop.

**At that node:**
- **Leaf, not yet started** — tell the user this leaf's goal text and slug, and that the next step is `/req` with that goal as the topic. Stop; do not run `/req` yourself.
- **Leaf, in progress** (an unmerged draft RDR or ADR already exists for its slug) — tell the user where it's at (which of `/req` / `/archi` / `/planning` / `/auto-action` / `/merge-req` / `/merge-archi` looks next) and stop.
- **Not a leaf, no children yet** — run a `/grilling` skill to name this node's full set of immediate children, all at once (e.g. root splits into A, B, C together — siblings are named eagerly, not one at a time). The children must be MECE — mutually exclusive (no two overlap in scope) and collectively exhaustive (nothing the parent covers is left out); see `../references/top-down-depth-first.md`'s Tetris example. A child is a leaf when it reduces to one scenario, one actor, one path — describable without "and," the same bar `/planning` applies to a single step; a node that still needs "and" to describe isn't a leaf yet and gets split again once it's reached. Write all children into the tree as pending, then descend into the first child and re-run the leaf check on it immediately — don't stop until you've either handed a real leaf off to `/req` or found one already in progress.

Never reopen a checked-off sibling to rescope it based on what a later leaf revealed — the split, once made, stands. Only new information about the *current* frontier node changes its own children.

Fill in `../template/tree.md`'s nested checklist and write it to `.context/tree/{slug}.md` — no timestamp, no draft/merged split; it's a single living document updated in place as the tree is drilled and leaves complete.

`mkdir -p .context/tree` if needed.

Completion criterion: either a leaf's goal and slug have been handed to the user with `/req` named as next step, an in-progress leaf's next command has been reported, or the entire tree is checked off and the user has been told the goal is complete.

**DO NOT START IMPLEMENT**
