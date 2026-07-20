---
applyTo: "**"
---

# Global Instructions

## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

## Communication Style Rule

Prefer structured, visual representations over prose. Reading structured output is faster than reading paragraphs.

### Priority order (use the highest tier that fits the content)

1. **Structured** (diagram or table) — highest preference
2. **Concise bullets**
3. **Detailed prose**
4. **Free text** — lowest preference, avoid unless nothing else fits

### Which structured form to use

- **Flow, pipeline, hierarchy, or dependency content** → ASCII tree/flow diagram, plain ASCII characters only (`|`, `v`, `+--`, `->`). No Unicode box-drawing or arrow glyphs — plain ASCII renders correctly everywhere.
- **Comparison content** (options, trade-offs, parallel attributes) → Markdown table.
- **List-like content with no flow or comparison shape** → concise bullets (tier 2), not a forced diagram.

Example flow diagram:
```
Requirement
    |
    v
Design Module
    |
    +-- Responsibility
    +-- API
    +-- Data
    +-- Algorithm
    |
    v
Code Artifact
    |
    v
Test Case
```

### Annotating edges/nodes

- Short labels (roughly 4 words or fewer) go inline on the arrow: `User Task \n    v - register task \n Priority Calculator`.
- Longer explanations don't fit on the arrow — drop a numbered/bulleted legend below the diagram instead.

### Placement

Lead with a one-line conclusion (per the Communication Rule), then follow with the structured block. The diagram/table supports the conclusion; it doesn't replace it.

### Floor — when to skip structure

A single fact, a yes/no answer, or a one-item confirmation ("Build passed.", "Yes.") stays plain text. Don't wrap trivial answers in a diagram, table, or bullet just for consistency.

### Scope

Applies to: chat responses, explanations, plans, standalone docs (README, design docs), and `AskUserQuestion` calls — question text and option `description`s follow the bullet rules (tier 2: concise, one idea each); use an option's `preview` field for tier-1 structured content (diagram, table, code) when the options are concrete artifacts worth comparing side by side.

Narrowed: commit messages and PR descriptions use bullets only (tier 2) — no ASCII diagrams. Shared history/PRs are visible to collaborators who didn't opt into this style, and many teams have their own commit-message conventions (Conventional Commits, Jira-linked format, etc.) that diagrams would break.

Does not apply to: code comments — those stay governed by the existing minimal-comment rule (no comments unless the WHY is non-obvious).

## Project Intents
Before executing any skill, check if a `.context/` directory exists in the current project root. If it does, read all files in it and let them guide how the skill behaves — they describe the human's goals, priorities, and constraints for this project.

<!-- rtk-instructions v2 -->
# RTK — Token-Optimized CLI

**rtk** is a CLI proxy that filters and compresses command outputs, saving 60-90% tokens.

## Rule
Always prefix shell commands with `rtk`:

```bash
# Instead of:              Use:
git status                 rtk git status
git log -10                rtk git log -10
cargo test                 rtk cargo test
docker ps                  rtk docker ps
kubectl get pods           rtk kubectl pods
```
<!-- /rtk-instructions -->
