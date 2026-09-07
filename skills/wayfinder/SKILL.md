---
name: wayfinder
description: Use one narrow grill-me interview to find validation-first ways forward for a single problem layer and recommend the existing skill that fits each way. Invoke as /wayfinder.
disable-model-invocation: true
---

# Wayfinder

Analyze exactly one current problem layer and return concise, validation-first ways to move it forward. Find the next useful move without designing or implementing deeper layers.

## Why this exists

Broad problems invite premature detail. Wayfinder keeps the discussion at the current layer, names the uncertainty that matters now, and finds a small test before deeper work depends on an unvalidated choice.

## MANDATORY Grill-Me Usage

Always invoke `@skills/grill-me` before producing any output.

Pass only these four inputs to `@skills/grill-me`:

- the root problem
- the current layer
- the immediate objective
- constraints directly relevant to the current layer

Constrain the interview to this layer. Ask only questions whose answers may change the possible ways forward at this layer. If one of the four inputs is missing, ask only for that missing input through `@skills/grill-me`.

Do not ask about:

- deeper layers
- future implementation details
- detailed edge cases of candidate ways
- production requirements that depend on an unresolved decision
- unrelated project context

If `@skills/grill-me` cannot be invoked, stop and report the blocker. Do not produce a way from assumptions.

## Wayfinding Principles

Prefer ways that provide:

- fast feedback
- a small and reversible experiment
- cheap exploration of the key uncertainty
- clear tests or observable signals
- a short feedback loop
- a clear transition into production requirements, design, and implementation

Use prototypes, spikes, thin vertical slices, test doubles, simulations, exploratory scripts, user interviews, measurements, or other low-cost validation methods when appropriate.

Do not choose the cheapest experiment when safety, compliance, data integrity, or irreversible production impact requires stronger validation.

## Decomposition Rules

- Handle exactly one current layer per invocation.
- Keep every way at the same abstraction level as the current layer.
- Do not recursively decompose a way.
- Do not discuss details that belong to a deeper layer.
- Produce two to five materially different ways when multiple valid options exist.
- Do not invent artificial alternatives.
- If only one valid way exists, return only one way.
- If the current layer is already actionable, return it as an execution-ready way without asking deeper questions.

## Skill Handoff

For every way, recommend one existing skill that can execute or validate it. Use the available skill catalog and never invent a skill name. Choose the skill that fits the way's current abstraction level and give a short reason.

A way is actionable only when it names a concrete next move and an observable result at the current layer. If a way is not actionable, recommend `/wayfinder` instead of a downstream skill.

## Output Format

Return only this format:

1. Way 1
    - Explain why this way is needed at this layer and the uncertainty it addresses.
    - Describe the cheapest useful test, experiment, or exploration.
    - Describe the signal that would support or reject the way.
    - Describe how the result informs production work, when relevant.
    - Recommend one existing skill for this way and briefly explain why it fits; if the way is not actionable, recommend `/wayfinder`.

2. Way 2
    - Explain why this way is needed at this layer and the uncertainty it addresses.
    - Describe the cheapest useful test, experiment, or exploration.
    - Describe the signal that would support or reject the way.
    - Describe how the result informs production work, when relevant.
    - Recommend one existing skill for this way and briefly explain why it fits; if the way is not actionable, recommend `/wayfinder`.

Keep the output concise. Do not include headings, summaries, reasoning, extra recommendations, checkpoints, or details beyond the current layer.
