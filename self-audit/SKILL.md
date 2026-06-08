---
name: self-audit
description: Audit the user's metacognitive state on a topic — what they know, what they're uncertain about, what they don't know they don't know, and what they know they don't know. Grills the user with targeted questions, then writes a structured knowledge-map markdown report. Use when user says "self-audit", "audit my knowledge", "what do I know about", "knowledge check", "metacognition check", or "map my understanding of".
---

# self-audit

Grill the user to surface their knowledge state on a topic. Write a `self-audit-<topic>-YYYY-MM-DD.md` report.

## Knowledge states

| State | Label | Meaning |
|-------|-------|---------|
| Knows it and can explain it | **Known** | Confident, accurate understanding |
| Knows something but gaps or fuzzy | **Uncertain** | Partial or shaky — could be right or wrong |
| Knows they don't know | **Known Unknown** | Explicit awareness of a gap |
| Hasn't encountered it at all | **Unknown** | Blank spot — not yet on their radar |

## Process

1. **Get topic** — user provides topic (or infer from context). Confirm scope in one sentence.
2. **Grill**

   Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: surface the user's true knowledge state — what they know, what's shaky, what they're missing.

   Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

   Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

   If a question can be answered by exploring the codebase, explore the codebase instead.

   There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.
3. **Classify** — from answers, assign each topic/concept to a state
4. **Identify unknown unknowns** — after grilling, explicitly introduce 2–3 concepts the user didn't mention. Ask if they've encountered them. These surface unknowns.
5. **Write report** — save to `./self-audit-<slug>-YYYY-MM-DD.md`

## Report format

```md
# Self-Audit: <Topic> — YYYY-MM-DD

## Known
- <concept>: <one-line summary of what they know>

## Uncertain
- <concept>: <what they got right, what's shaky>

## Known Unknown
- <concept>: <what they know they don't know>

## Unknown
- <concept>: <blank spots surfaced during grilling>

## Recommended next steps
- <1–3 focused things to study based on gaps>
```

## Rules

- One question at a time — don't batch
- Don't reveal the state classification during grilling; do it at the end
- File name: `self-audit-<kebab-slug>-YYYY-MM-DD.md` in cwd
- Recommended next steps should be specific, not generic ("read the docs")
