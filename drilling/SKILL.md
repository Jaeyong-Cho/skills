---
name: drilling
description: Goal-decomposition skill. Splits a broad goal top-down into a persisted tree of atomic, junior-developer-executable sub-goals, one per leaf small enough for /req. Use when invoked as /drilling.
disable-model-invocation: true
---

# Drill

Manages a persisted goal tree so a broad goal never lands on `/req` in one oversized piece. Read `../references/top-down-decompose.md` for the decomposition method: split every node MECE, recurse until every leaf is atomic. Building the tree is /drilling's whole job — it doesn't pick execution order; that's the user's call once the tree exists. Read `.context/tree/` first.

**Clarifying a goal, by default:** every goal text written into the tree — root or child — is grilled first, not taken as-is. Resolve ambiguous phrasing (what exactly is and isn't included), push past the surface ask to the intrinsic goal — the real outcome wanted, not just the words handed to you, the same instinct `/req`'s Context and Goal steps apply — and get concrete about the technical detail: which existing systems, files, or interfaces this goal actually touches, and a leaning on technical approach where one's already obvious (e.g. "cache via Redis," not just "add a cache"). This isn't `/archi`'s job of committing the design — just enough technical grounding that the split reflects real boundaries and `/req` starts from a well-scoped, technically legible goal instead of a vague label. Write the clarified, detailed text as the node's goal, not the raw input. This has to happen before the atomic check too — "single task, under 20 words, no and/or/then, junior-developer-executable" can't be judged against a goal that isn't pinned down yet.

**Starting a new tree:** if invoked with a goal argument, derive a kebab-case slug from the clarified goal. If `.context/tree/{slug}.md` doesn't exist, create it from `../template/tree.md` with the clarified goal as the root node and build out the tree (below). If it already exists, ignore the argument and resume it instead.

**Resuming:** if invoked with no argument, look in `.context/tree/`. One file — resume it. Several — list them and ask the user which. None — tell the user to run `/drilling {goal}` to start one, and stop.

**Building the tree:** walk every node — order doesn't matter, since nothing here gets executed yet.
- **Node isn't atomic and has no children yet** — run a `/grilling` skill to name its children — the same grill both clarifies each child's goal text (per "Clarifying a goal" above) and decides the split. The children must be MECE — mutually exclusive (no two overlap in scope) and collectively exhaustive (nothing the parent covers is left out); see `../references/top-down-decompose.md`'s Tetris example. A child is atomic when it's a single task — one sentence under 20 words, no "and," "or," or "then" — and concrete enough that a junior developer could execute it without making a design decision, the same bar `/planning` applies to its own steps; falling short on any of those means it's still more than one task and isn't atomic yet. If clarifying (technical grounding especially) surfaces multiple distinct sub-parts bundled into what looked like one sentence — e.g. a UI element, the state behind it, and how that state persists — that's proof it isn't atomic either, even without an "and" in sight: split it into a real child per sub-part instead of compressing them into one sentence. Never park that detail in a comment or note beside the tree — anything concrete enough to matter is a node. There's no depth limit: a child that's still compound gets split again the same way, however many levels it takes. If naming a child correctly depends on information you don't have, that's an understanding gap (same reference's "Understanding gaps" section): if the answer would change how this node's *other* children get named, insert `[?] {path}0: Understand {the unknown}` as the first child and stop splitting this node there — name nothing else under it until it's answered. If the other children don't depend on the answer, name them too and add the understand-node alongside as one more sibling. Write all children into the tree as pending, then recurse into every one of them the same way — build out every branch, not just one, until the whole tree bottoms out at atomic leaves or unresolved understand-nodes.
- **Understand-node (`[?]`), unresolved** — ask the user directly what they found out; don't research it yourself. Record the answer inline, mark it `[x]`, and continue building whatever it was blocking.
- **Node is atomic** — leave it as a leaf; nothing more to split there.

Never reopen a checked-off sibling to rescope it based on what building another branch revealed — the split, once made, stands. Only new information about a node's own children changes them.

**Reporting status:** every run — whether just finished building or resuming an existing tree — scan every node before reporting. A leaf (`[ ]`) is done once its slug's RDR and ADR are committed (`.context/req/{slug}.md` and `.context/adr/{slug}.md` exist, with no unmerged draft left in `.context/rdr/` or `.context/adr/` for that slug); mark it `[x]` with links. A non-leaf is done once every child is done; mark it `[x]` too. Then tell the user the tree's current state: which leaves are done, which are pending and ready for `/req`, which are blocked on an unresolved understand-node. Don't pick one as next — that's the user's call.

Fill in `../template/tree.md`'s nested checklist and write it to `.context/tree/{slug}.md` — no timestamp, no draft/merged split; it's a single living document updated in place as the tree is built and leaves complete.

`mkdir -p .context/tree` if needed.

Completion criterion: every node in the tree is either an atomic leaf, a resolved understand-node, or checked off done, and the user has been shown the tree's current status.

**DO NOT START IMPLEMENT**
