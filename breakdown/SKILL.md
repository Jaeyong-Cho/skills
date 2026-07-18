---
name: breakdown
description: Breaks a goal down into a MECE tree of atomic, actionable sub-goals — one decomposition axis per level, recursed until every leaf is a single verb-object-done action. Use via /breakdown.
disable-model-invocation: true
---

# Breakdown

Decompose one goal at a time into a tree, level by level. At each node, do the same steps: state the goal as an outcome, pick one axis, split, then test.

1. **State the node as an outcome, not an activity** — the state of the world that exists when it's done, not the work you'll be doing. If the input goal is too vague to state that way ("improve onboarding"), rewrite it as a concrete, verifiable outcome before splitting it; ask the user if you genuinely can't tell what "done" means from context.

2. **Pick exactly one decomposition axis for this level**, and name it before listing children. Common axes: sequence (phases/stages the work passes through), component (parts of the system or deliverable), actor (who does the work), case (segments, scenarios, or conditions the goal must cover). Mixing axes within one level is the single most common way a split stops being mutually exclusive — a "by phase" child sitting next to a "by team" child will always overlap somewhere.

3. **Split along that axis, then test the split for MECE against the parent:**
   - *Mutually exclusive* — for any piece of work, exactly one child owns it. If you can't say which child a task belongs to, the children overlap; merge them or repick the axis.
   - *Collectively exhaustive* — the children, summed, fully reconstitute the parent. Ask "what's left over once every child is done?" — anything left over is a missing child, not an acceptable gap.

4. **Test each child for atomic; recurse on any that fail.** A node is atomic when it's describable without "and", has one owner, and produces one deliverable. A node that still bundles more than one outcome, or that a single person can't finish in one sitting, is not a leaf yet — return to step 2 for that node with a fresh axis, and keep splitting until it is.

5. **Rewrite every atomic leaf as actionable: verb + concrete object + done condition.** Reject vague verbs with no observable end-state ("support", "improve", "explore", "handle") — replace each with the concrete action it was standing in for. A leaf that can't be pinned to a done condition isn't atomic yet; send it back through step 4.

6. **Order the leaves.** For every pair of leaves, ask whether one must finish before the other can start (it consumes something the other produces, or needs a state the other creates) — record only real dependencies, not the order they happen to appear in the tree. Topologically sort on those dependencies: a leaf with no unresolved dependency is ready to schedule next. Leaves with no dependency between them are parallelizable — mark them as such side by side rather than inventing a sequence between them.

7. **Present the full tree**, indented by level with the axis used at each level labeled inline (e.g. `by phase:`, `by component:`), then the numbered execution order from step 6 as a flat list, grouping parallelizable leaves under the same number.

Completion criterion: every leaf is atomic (no "and", one owner, one deliverable) and actionable (verb + object + done condition); every level's children pass both the mutually-exclusive and collectively-exhaustive tests against their parent; the axis used at each level is stated; every leaf has a position in the dependency-ordered execution list or is marked parallelizable with the leaf(s) it's parallel to.
