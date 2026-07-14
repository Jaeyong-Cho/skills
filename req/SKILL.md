---
name: req
description: Requirements-engineering skill. Grills to find the goal, elicit and prioritize functional and non-functional requirements, and commit to a testable spec. Use when invoked as /req.
disable-model-invocation: true
---

# Req

Read `../references/requirement-engineering.md` — the key activities (elicitation, analysis, specification, validation) and the functional/non-functional split shape the grill below. Read `../template/requirements.md` — its sections (Requirements, Decision, Out of Scope, User Scenario, Acceptance Criteria) are what each grill item below fills in, so grill toward that shape from the first question rather than only at write-time.

Check `.context/req/` — if an existing spec covers the same topic, read it and revise it rather than creating a new one.

Use this for new goals or to rescope an existing one. Run a `/grilling` skill to reach a committed, testable spec:

1. **Goal & scenario** — what does success actually look like? Push past the surface request to the real outcome the user needs. Narrate it as the concrete story the user lives through: who wants this, what they're trying to do, why — not a feature list.
2. **Elicitation** — draw out functional requirements (what the system must do) and non-functional requirements (performance, security, availability, usability — how it must behave). State each testably; reject vague verbs ("support", "handle") with no condition attached.
3. **Analysis & decision** — where do requirements conflict, compete, or admit more than one valid implementation? For each, what's the resolution and why — not the requirement itself, the choice made among alternatives. Not every requirement earns equal depth: press hardest on the ones disputed, high-risk, or blocking a choice; move fast past the ones nobody contests.
4. **Constraints & scope** — what's fixed vs. merely assumed? Challenge assumed constraints. What's explicitly excluded so it isn't silently re-litigated later?
5. **Validation** — what does bad look like, and where's the ambiguous middle zone where partial success might be acceptable? Convert every requirement into a SMART, Given–When–Then acceptance criterion; the bad and ambiguous cases just surfaced become the Exception and Boundary rows, not just Normal. Each row needs a concrete verification method (manual test, e2e test, unit test, query).

Grill until every branch resolves and requirements are stated testably. Completion criterion: the user has confirmed a committed spec in their own words, and every acceptance criterion has a verification method.

Derive a kebab-case slug from the topic.

Fill in `../template/requirements.md` with the resolved requirements, decision, out-of-scope, user scenario, and acceptance criteria table, and write it to `.context/req/{slug}.md`.

`mkdir -p .context/req` if needed. Tell the user the file path. Next step: `/planning`.

**DO NOT START IMPLEMENT**
