# SPEC - {title}

## Context
> The problem or trigger, and the current state before this spec — why this work exists at all.

-

## Requirements
> What must be true. One requirement per line, testable — avoid vague verbs like "support" or "handle" without a condition attached.

-

## Decision
> The choice made among alternatives, and why. Not the requirement itself — the resolution when a requirement was ambiguous or had multiple valid implementations.

-

## Out of Scope
> What was explicitly excluded, so it isn't silently re-litigated later.

-

# User Scenario
> One scenario per subsection — split into multiple when a single sequence grows too large to follow, or covers more than one path or actor. Narrate each as the sequence the user lives through: {action} → {reaction} → {action} → ... down to the outcome — not a feature list.

## {Scenario name}
{action} → {reaction} → {action} → {reaction}

# Acceptance Criteria
> SMART AC — Specific, Measurable, Achievable, Relevant, Time-bound. Each row is one verifiable condition, phrased as Given–When–Then.

|AC|Category|Verification Method|
|--|--|--|
|Given {starting state} - When {action} - Then {expected result}|Normal, Exception or Boundary|{how this gets checked — manual test, e2e test, unit test, test name, or query}|
