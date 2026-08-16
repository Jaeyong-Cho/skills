# Document Writing Guidelines

When creating or editing documents, optimize for **accurate communication**, not elegant prose.

The primary goal is:

> Help the reader understand the subject quickly, make the correct judgment, and take the necessary action.

## 1. Understand the Document Before Writing

Before writing, identify:

- Purpose: Why does this document exist?
- Audience: Who will read it?
- Action: What should the reader understand, decide, or do?
- Scope: What is and is not covered?
- Evidence: What facts, files, code, logs, data, or references support the document?

If these are unclear and materially affect the document, ask questions before writing.

Do not invent missing information.

## 2. Structure Before Sentences

Design the document structure before writing individual sentences.

Prefer:

```text
Conclusion / Summary
-> Purpose / Context
-> Problem
-> Evidence
-> Analysis
-> Solution / Decision
-> Details
-> Action / Verification
```

Use a structure appropriate to the document type.

Do not force every document into the same template.

## 3. Put the Important Information First

Do not make the reader search for the conclusion.

Prefer:

```text
Conclusion
Reason
Evidence
Details
```

over:

```text
Background
History
Details
Details
Details
Conclusion
```

The first paragraph should usually make the purpose or main point clear.

## 4. Write for the Reader

Assume that the reader does not know what is inside the author's head.

Do not rely on implicit context.

Before introducing information, consider:

- What does the reader already know?
- What does the reader need to know?
- What question will the reader have next?
- What information is necessary to make the next decision?

Write in the reader's order of understanding, not the author's order of discovery.

## 5. Prefer Simple and Concrete Language

Use simple language unless technical terminology is necessary.

- Prefer concrete expressions over abstract expressions.
- Explain necessary technical terms when they first appear.
- Avoid unnecessary jargon.
- Replace vague expressions with observable facts.
- Do not use sophisticated wording merely to sound professional.

Avoid vague expressions such as:

- "appropriately"
- "efficiently"
- "significantly"
- "various"
- "somewhat"
- "there is a problem"
- "it seems"
- "needs improvement"

When possible, replace them with concrete information.

Example:

Bad:

> Performance is significantly degraded.

Better:

> Average latency increased from 20 ms to 85 ms.

## 6. Keep Sentences Short and Focused

Prefer one main meaning per sentence.

Split a sentence when it contains multiple independent ideas such as:

- problem
- cause
- solution
- exception
- consequence

Avoid unnecessary use of:

- long subordinate clauses
- excessive commas
- "of"
- nominalized expressions
- redundant modifiers
- repeated explanations

Keep the subject and predicate reasonably close.

Do not make every sentence artificially short. Preserve necessary logical relationships.

## 7. Separate Facts, Opinions, and Hypotheses

Clearly distinguish:

- Fact: directly verified information
- Observation: what was observed
- Interpretation: explanation derived from observations
- Hypothesis: an unverified explanation
- Opinion: judgment or preference

Never present an assumption as a fact.

For technical documents, prefer evidence such as:

- source code
- configuration
- logs
- metrics
- test results
- reproduction steps
- screenshots
- specifications
- references

If information cannot be verified, explicitly mark it as uncertain.

## 8. Never Invent Technical Facts

When working with a codebase or project:

- Inspect the relevant code before documenting implementation details.
- Inspect configuration before documenting configuration behavior.
- Inspect tests before claiming behavior is tested.
- Verify commands before documenting how to run them.
- Do not invent APIs, parameters, outputs, file paths, or behavior.
- Do not assume that an old README accurately describes the current implementation.

If the evidence is insufficient, say so.

## 9. Make Problems Concrete

For problems and bugs, prefer:

```text
Environment
-> Reproduction
-> Expected Result
-> Actual Result
-> Evidence
-> Cause
-> Solution
-> Verification
```

Avoid subjective descriptions such as:

> It doesn't work correctly.

Prefer:

> When X occurs under Y environment, Z is returned instead of A.

Use logs, measurements, and reproduction conditions whenever available.

## 10. Make the Reader's Next Action Obvious

A useful document should enable the reader to act.

When appropriate, explicitly state:

- What should be done?
- Who should do it?
- In what order?
- Under what conditions?
- How can success be verified?

For procedures, write steps in the order the reader performs them.

For technical instructions:

```text
Prerequisites
-> Step 1
-> Step 2
-> Step 3
-> Expected Result
-> Verification
-> Troubleshooting
```

## 11. Use Evidence-Based Reasoning

For arguments and technical decisions, prefer:

```text
Claim
-> Reason
-> Evidence
-> Example
```

For causal explanations:

```text
Observation
-> Cause
-> Evidence
-> Consequence
```

Do not mix cause and result.

For comparisons:

```text
Options
-> Evaluation Criteria
-> Comparison
-> Trade-offs
-> Decision
-> Rationale
```

For decisions, explain not only what was chosen but why it was chosen and what trade-offs were accepted.

## 12. Choose the Appropriate Document Structure

Adapt the structure to the document type.

### README

```text
What is this?
Why does it exist?
Prerequisites
Installation
Usage
Examples
Configuration
Troubleshooting
Limitations
```

### Bug Report

```text
Problem
Environment
Steps to Reproduce
Expected Result
Actual Result
Evidence
Cause
Fix
Verification
```

### Technical Design / Decision

```text
Summary
Context
Problem
Requirements
Options
Evaluation
Decision
Rationale
Trade-offs
Consequences
```

### Meeting Notes

```text
Purpose
Key Decisions
Discussion
Action Items
Owner
Due Date
Open Questions
```

### Work Report

```text
Result
Completed Work
Evidence
Issues
Remaining Work
Next Action
```

Do not include sections that provide no useful information.

## 13. Titles and Headings

Titles should accurately describe the content.

Prefer specific titles over vague titles.

Bad:

> System Improvement

Better:

> Reduce Login API Timeout from 30s to 10s

Headings should help the reader navigate the document.

Use headings to separate meaningful conceptual units, not every small paragraph.

## 14. Use Examples When They Reduce Ambiguity

Use examples when an abstract explanation could be misunderstood.

For technical documentation, examples should be:

- realistic
- consistent with the actual implementation
- minimal
- executable when presented as executable commands

Never fabricate example outputs that contradict the actual system.

## 15. Avoid Performative Writing

Do not optimize for:

- sounding intelligent
- sounding formal
- sounding authoritative
- impressive vocabulary
- unnecessary verbosity
- rhetorical flourishes

Optimize for:

```text
Accuracy
-> Clarity
-> Brevity
-> Usability
```

## 16. Revise by Removing Before Adding

When editing a document, first look for:

1. unnecessary sections
2. unnecessary sentences
3. repeated information
4. vague expressions
5. unsupported claims
6. overly long sentences
7. unnecessary jargon
8. information unrelated to the document's purpose

Do not add information merely to make the document look more complete.

## 17. Review Before Finalizing

Before returning the final document, perform these checks.

### Purpose

- Is the purpose obvious?
- Is the intended audience clear?
- Is the main conclusion easy to find?

### Structure

- Is the information ordered according to the reader's needs?
- Is the logical relationship between sections clear?
- Are cause and effect separated?

### Clarity

- Does each sentence have a clear meaning?
- Are vague expressions minimized?
- Are technical terms necessary and understandable?

### Accuracy

- Are facts distinguishable from assumptions?
- Are technical claims supported by evidence?
- Did you invent anything?
- Do examples match the actual system?

### Completeness

- Is information required for understanding missing?
- Can the reader perform the intended action?
- Are important exceptions or limitations documented?

### Brevity

- Can any sentence be removed without losing meaning?
- Can repeated information be removed?
- Can long sentences be split?

### Final Reader Test

Ask:

> If the reader has no access to my thoughts and only has this document, can they understand what matters and what they should do?

If not, revise the document.

## 18. Writing Workflow

Use this workflow by default:

```text
Understand
-> Identify Audience / Purpose
-> Gather Evidence
-> Design Structure
-> Draft
-> Verify Facts
-> Check Logic
-> Remove Ambiguity
-> Remove Redundancy
-> Final Reader Check
```

When important information is missing, do not guess.

Ask the user for the missing information instead.

## 19. ASCII Diagrams

- chars: only `|` `v` `+--` `->`
- avoid: arrows (`→` `⇒` `➜`), box-drawing (`─` `│` `┌` `└` `├` `┬`), bullet glyphs (`•` `▪`)
- fence: always ` ```text ` (never bare ` ``` `) — stops renderers from syntax-highlighting or reflowing the layout
- caption: one sentence stating what the diagram depicts, placed directly above or below it
- labels: inline on the arrow if <=4 words; longer explanations go to a numbered/bulleted legend below
