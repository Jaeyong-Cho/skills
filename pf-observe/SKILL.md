---
name: pf-observe
description: |
  Build observation scripts and tools to understand system behavior — targets logs, data outputs, runtime state, dependencies, inputs, config, and resources. Grills to clarify what's unknown, writes targeted scripts to surface differences and patterns, then derives causes.
  Use when the user wants to understand why a system behaves a certain way, detect unexpected changes, or build tooling to observe runtime behavior. Triggers: "pf-observe", "observe this", "why is this happening", "build observation script", "I want to understand the system", "detect patterns", "trace this behavior", "what's changing", "log analysis".
---


# System Observation

For what to observe and how to implement CLI flags, logging, and output file conventions — read [REFERENCE.md](REFERENCE.md).

## Step 1: Grill

Read user's concern, known things, and problem. Run `grill-me` — start from those but follow any thread that opens up. No maximum questions. Unrelated topics are welcome — they often lead somewhere interesting.

## Step 2: Explore codebase and existing output

Detect project language:
```bash
ls package.json go.mod Cargo.toml pyproject.toml setup.py Gemfile mix.exs pom.xml 2>/dev/null
```

Then grep for logging, file writes, and env/config reads using file extensions that match the detected language. Exclude `node_modules`, `vendor`, `.git`. Limit each to `head -20`. Examples by language:

| Language | Extensions | Logging keywords | Config keywords |
|----------|-----------|-----------------|----------------|
| Python | `*.py` | `logging.`, `logger.` | `os.environ`, `os.getenv` |
| Go | `*.go` | `log.`, `zap.`, `logrus.` | `os.Getenv`, `viper.` |
| JS/TS | `*.js`, `*.ts` | `console.`, `winston`, `pino` | `process.env` |
| Rust | `*.rs` | `log::`, `tracing::` | `std::env` |
| Ruby | `*.rb` | `Rails.logger`, `logger.` | `ENV[` |

Also inspect existing output files and the `observe/` directory:
```bash
find . \( -name "*.log" -o -name "*.jsonl" -o -name "*.json" \) \
  -not -path "*/node_modules/*" -not -path "*/vendor/*" 2>/dev/null | head -20
ls observe/ 2>/dev/null
```

Read existing `observe/` scripts. Note: what CLI flags they use, what output format they produce, what they already cover. This is the established convention — new scripts must follow it.

Read key output files. From this, identify what the system already exposes and what's hidden.

## Step 3: Build observation scripts

Scaffold directory if not exists:

```bash
mkdir -p observe
```

Save all scripts directly in `observe/`. No subdirectories — observation often spans multiple concerns and shouldn't be constrained by category.

**Reuse existing scripts where they fit** — run them as-is or with different arguments before writing new ones. When writing new scripts, match the conventions of existing ones: same CLI flag names, same output format, same file naming pattern.

**Every script must accept paths and config via CLI options — never hardcode.**
Bad: `LOG_PATH = "/var/log/app.log"` or `OUTPUT = "observe/output/run.jsonl"`
Good: `--log-path`, `--output-dir`, `--since`, `--env` — caller decides. See [REFERENCE.md](REFERENCE.md) for the pattern.

For each observable, think beyond the obvious target. Consider multiple angles:
- **Snapshot** — current state
- **Delta** — difference over time, across envs, or between versions
- **Distribution** — value ranges, frequencies, outliers
- **Absence** — what's missing that should be there
- **Correlation** — two observables that should move together but don't

Write scripts to discover patterns, differences, and trends — start from the grill findings but don't stop there. Scripts that look at unrelated areas are encouraged. Unexpected findings from outside the original concern are often the most valuable. One script per angle. Shell for quick captures, Python for structured analysis.

## Step 4: Run and interpret

Run scripts. Show output. Interpret each result — look beyond what was asked. Surface unexpected findings, including things that seem unrelated. Do not dismiss anything before examining it.

**If a visual would communicate the pattern faster than raw text — visualize.** Any method is fine: ASCII, table, SVG, HTML, diagram — whatever makes the observation clearest. See [REFERENCE.md](REFERENCE.md) for options. Save output files to `observe/` and print the path.

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
