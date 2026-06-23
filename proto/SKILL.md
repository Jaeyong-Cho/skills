---
name: proto
description: Build a throwaway prototype to explore an idea or test something quickly — network calls, API responses, output formats, data wrangling, language features, anything. No architecture, no interactivity — just write a runnable file and see what happens. Use when user wants to spike an idea, experiment, test an API, check a format, explore a concept, or says "proto", "prototype this", "just try it", "quick experiment".
---

# Proto

Each prototype lives in `proto/<slug>/`. Goal is discovery, not correctness.
## Structure

```
proto/
  my-idea/
    <entry>           ← the prototype (prefer single file)
    run.sh            ← numbered use cases
    output/           ← data files produced by the prototype (if needed)
    observe/
      20260623-143000-my-idea.md   ← analysis report per run
```

## Rules

- **Default language: Python** — use `.py` unless the idea is language-specific
- **Prefer single file** — one entry file; split only if the idea genuinely can't fit
- **Not interactive** — runs and exits, prints output
- **Reuse freely** — copy or reference existing project code if it helps; not required, the prototype's purpose comes first

## run.sh rules

- One numbered case per use case with a short description
- No-arg invocation lists all cases with descriptions
- Output can be anything: stdout, files in `output/`, network responses, etc.

## Workflow

1. **Read project context** — check for `CLAUDE.md`, `README.md`, or similar at the project root to understand the codebase; skip if not a project root
2. **Read expected results** — if the user specifies a target (e.g. `expected/foo.md`), read it and use it to shape what the prototype should produce; otherwise skip
3. Pick a slug: short noun phrase, kebab-case (e.g. `llm-latency`, `json-diff`)
3. Write the entry file in `proto/<slug>/` — name it whatever fits, self-contained
5. Write `proto/<slug>/run.sh` — one case per use case with a short description
6. Do NOT create tests, docs, or helper modules

## Done when

Prototype runs. Use `/observe` to analyze and report.
