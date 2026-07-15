---
name: drill
description: Goal-decomposition skill. Drills a broad goal top-down into a persisted tree of narrower sub-goals, depth-first, until reaching a leaf small enough for /req. Use when invoked as /drill.
disable-model-invocation: true
---

# Drill

Manages a persisted goal tree so a broad goal never lands on `/req` in one oversized piece. Read `../references/top-down-depth-first.md` — the drill order below (descend one branch to a leaf, act, only then return to siblings) is that methodology applied to the goal tree. Read `.context/tree/` first.

**Clarifying a goal, by default:** every goal text written into the tree — root or child — is grilled first, not taken as-is. Resolve ambiguous phrasing (what exactly is and isn't included), push past the surface ask to the intrinsic goal — the real outcome wanted, not just the words handed to you, the same instinct `/req`'s Context and Goal steps apply — and get concrete about the technical detail: which existing systems, files, or interfaces this goal actually touches, and a leaning on technical approach where one's already obvious (e.g. "cache via Redis," not just "add a cache"). This isn't `/archi`'s job of committing the design — just enough technical grounding that the split reflects real boundaries and `/req` starts from a well-scoped, technically legible goal instead of a vague label. Write the clarified, detailed text as the node's goal, not the raw input. This has to happen before the leaf check too — "one scenario, no and" can't be judged against a goal that isn't pinned down yet.

**Starting a new tree:** if invoked with a goal argument, derive a kebab-case slug from the clarified goal. If `.context/tree/{slug}.md` doesn't exist, create it from `../template/tree.md` with the clarified goal as the root node and proceed to split it (below). If it already exists, ignore the argument and resume it instead.

**Resuming:** if invoked with no argument, look in `.context/tree/`. One file — resume it. Several — list them and ask the user which. None — tell the user to run `/drill {goal}` to start one, and stop.

**Finding the frontier:** walk the tree depth-first, leftmost-first. A node is done when: an action leaf (`[ ]`) — its slug's RDR and ADR are committed (`.context/req/{slug}.md` and `.context/adr/{slug}.md` exist, with no unmerged draft left in `.context/rdr/` or `.context/adr/` for that slug); an understand-node (`[?]`) — its question has been answered and the answer recorded inline; a non-leaf — every child under it is done. If the current node is done, check it off (`[x]`, leaves get rdr/adr links, understand-nodes keep their recorded answer), then continue the walk — a sibling if any remain unchecked, otherwise back up to the parent (checking it off too once every child is done) and on to the parent's next sibling. Stop at the first node that isn't done. If the walk reaches the end with everything checked off, tell the user the goal tree is complete and stop.

**At that node:**
- **Understand-node (`[?]`), unresolved** — ask the user directly what they found out; don't research it yourself. Record the answer inline, mark it `[x]`, and immediately resume the walk from there — finish naming the parent's remaining children if this one was blocking them, or move on to the next sibling if it wasn't.
- **Leaf, not yet started** — tell the user this leaf's goal text and slug, and that the next step is `/req` with that goal as the topic. Stop; do not run `/req` yourself.
- **Leaf, in progress** (an unmerged draft RDR or ADR already exists for its slug) — tell the user where it's at (which of `/req` / `/archi` / `/planning` / `/auto-action` / `/merge-req` / `/merge-archi` looks next) and stop.
- **Not a leaf, no children yet** — run a `/grilling` skill to name this node's children — the same grill both clarifies each child's goal text (per "Clarifying a goal" above) and decides the split. The children must be MECE — mutually exclusive (no two overlap in scope) and collectively exhaustive (nothing the parent covers is left out); see `../references/top-down-depth-first.md`'s Tetris example. A child is a leaf when it reduces to one scenario, one actor, one path — describable without "and," the same bar `/planning` applies to a single step. If naming a child correctly depends on information you don't have, that's an understanding gap (same reference's "Understanding gaps" section): if the answer would change how this node's *other* children get named, insert `[?] {path}0: Understand {the unknown}` as the first child and stop the split there — name nothing else under this node until it's answered. If the other children don't depend on the answer, name them too and add the understand-node alongside as one more sibling. Otherwise name the full set of children eagerly, all at once — siblings aren't named one at a time. Write all children into the tree as pending, then descend into the first and re-run this check on it immediately — don't stop until you've handed a real leaf to `/req`, found one already in progress, or hit an unresolved understand-node.

Never reopen a checked-off sibling to rescope it based on what a later leaf revealed — the split, once made, stands. Only new information about the *current* frontier node changes its own children; resolving an understand-node and then finishing that same parent's split is expected, not a reopening.

Fill in `../template/tree.md`'s nested checklist and write it to `.context/tree/{slug}.md` — no timestamp, no draft/merged split; it's a single living document updated in place as the tree is drilled and leaves complete.

`mkdir -p .context/tree` if needed.

Completion criterion: either a leaf's goal and slug have been handed to the user with `/req` named as next step, an in-progress leaf's next command has been reported, or the entire tree is checked off and the user has been told the goal is complete.

**DO NOT START IMPLEMENT**
