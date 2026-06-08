---
name: pf-observe
description: |
  Build observation scripts and tools to understand system behavior — targets source code, logs, data outputs, runtime state, dependencies, inputs, config, and resources. Grills to clarify what's unknown, writes targeted scripts to surface differences and patterns, then derives causes.
  Use when the user wants to understand why a system behaves a certain way, detect unexpected changes, or build tooling to observe runtime behavior or source code structure. Triggers: "pf-observe", "observe this", "why is this happening", "build observation script", "I want to understand the system", "detect patterns", "trace this behavior", "what's changing", "log analysis".
---


# System Observation

For what to observe and how to implement CLI flags, logging, and output file conventions — read [REFERENCE.md](REFERENCE.md).

## Step 1: Grill

Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: understand what's unknown and where to look. Starting context: the user's concern, known things, and problem.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

Unrelated topics are welcome — they often lead somewhere interesting.

## Step 2: Explore codebase and existing output

Explore freely. Understand:
- Project language and structure
- Where logging, config reads, and file writes happen in source code
- Key source files — entry points, core modules, anything that looks surprising
- Existing output files (logs, JSON, JSONL)
- Existing `observe/` scripts — what they cover, what CLI flags and output format they use (new scripts must follow the same conventions)

Use whatever tools fit. Identify what the system already exposes and what's hidden — in both runtime data and source code.

## Step 3: Build observation scripts

Scaffold directory if not exists:

```bash
mkdir -p observe
```

Save all scripts directly in `observe/`. No subdirectories — observation often spans multiple concerns and shouldn't be constrained by category.

**Reuse existing scripts where they fit** — run them as-is or with different arguments before writing new ones. When writing new scripts, match the conventions of existing ones: same CLI flag names, same output format, same file naming pattern.

Every script must accept paths and config via CLI options — never hardcode. See [REFERENCE.md](REFERENCE.md) for script rules, CLI flag conventions, and templates.

Apply these lenses to any target (logs, data, runtime state, config, source code):
- **Snapshot** — what does it look like right now?
- **Delta** — what changed over time, across envs, or between versions?
- **Distribution** — value ranges, frequencies, outliers
- **Pattern** — recurring structures, regularities, anomalies
- **Absence** — what's missing that should be there?
- **Correlation** — two things that should move together but don't

Start from the grill findings but don't stop there — unexpected findings from unrelated areas are often most valuable. One script per angle. Shell for quick captures, Python for structured analysis.

## Step 4: Run and interpret

Run scripts. Show output. Interpret each result — look beyond what was asked. Surface unexpected findings, including things that seem unrelated. Do not dismiss anything before examining it.

If a visual communicates the pattern faster — visualize. See [REFERENCE.md](REFERENCE.md) for options. Save output files to `observe/` and print the path.

If cause found → summarize. If not → identify next observable, repeat Step 3–4.

## Step 5: Derive actions

From the findings, think about what they imply. For each significant pattern or cause found, consider:

| Finding type | Action to consider |
|---|---|
| Value that should always hold | Add assertion or invariant |
| State that was hard to see | Improve logging — what, where, at what level |
| Structural cause (wrong layer, wrong coupling) | Propose architecture decision (ADR) |
| Gap or unmet behavior the system reveals | New feature strategy — who needs it, what it changes |

Not every finding needs an action. Surface only what's clearly warranted. State reasoning.

## Step 6: Done

Write `observe/observe_report.md` — free-form markdown, no required structure. Write what matters: what was found, what caused it, what to do. Include visuals (tables, code blocks, diagrams) only if they add clarity. Skip sections that have nothing to say.

List all scripts written. Summarize: observation → pattern → cause → action (or still unknown).
