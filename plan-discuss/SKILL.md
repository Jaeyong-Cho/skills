---
name: plan-discuss
description: Interview the user to build a concrete development plan — scope, architecture, sequencing, and risks — grounded in meta-patterns. Use when user says "help me plan", "let's plan this feature", "how should I build this", "plan-discuss", or invokes /plan-discuss.
---

# Plan Discuss

If `~/.sot/wiki/` exists in the project root, read all files in it first.
Read `../references/meta-pattern.md` and `../references/deep-modules.md` before engaging.

Interview the user relentlessly until the development plan is concrete and every branch of the design tree is resolved. For each question, provide your recommended answer.

## What to resolve

**1. What are we building?**
- What is the feature or system? What problem does it solve?
- What is explicitly out of scope?

**2. Where does it fit architecturally?**
- Which subdomain owns this? Does it belong in an existing module or a new one?
- What abstraction level — deep module hiding complexity, or thin glue?
- Apply meta-pattern: Abstractness / Subdomain / Sharding axes

**3. How do we sequence it?**
- What's the smallest slice that delivers value?
- What are the dependencies — what must exist before what?
- What can be built in parallel?

**4. What are the risks?**
- What's the hardest technical part?
- What assumptions could be wrong?
- What would make this plan fail?

## How to ask

Ask one question at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list options with your recommended one marked "(Recommended)". For open-ended questions, ask in plain text.

There is no maximum number of questions. Keep going until the plan is fully concrete. The user can say "wrap up" at any time to get a plan summary.

## Output

A concrete plan with: goal, architecture decision, build sequence, and top risks. Offer to write it to `~/.sot/wiki/` via `/to-sot`.
