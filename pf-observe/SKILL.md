---
name: pf-observe
description: |
  Build observation scripts and tools to understand system behavior — targets logs, data outputs, runtime state, dependencies, inputs, config, and resources. Grills to clarify what's unknown, writes targeted scripts to surface differences and patterns, then derives causes.
  Use when the user wants to understand why a system behaves a certain way, detect unexpected changes, or build tooling to observe runtime behavior. Triggers: "pf-observe", "observe this", "why is this happening", "build observation script", "I want to understand the system", "detect patterns", "trace this behavior", "what's changing", "log analysis".
---

Read `../pf/references/caveman.md` and apply caveman style throughout.
Check journal: `[ -n "$PFJ_PATH" ] && cat "$PFJ_PATH/today.md" 2>/dev/null`

# System Observation

For what to observe and how to implement CLI flags, logging, and output file conventions — read [REFERENCE.md](REFERENCE.md).

## Step 1: Grill

Read user's concern, known things, and problem. Run `grill-me` focused on those — ask questions to deepen understanding of each. No maximum questions. Keep going until the concern is precise, the known baseline is clear, and the problem is fully understood.

## Step 2: Explore codebase and existing output

Search the codebase to understand what data already flows through the system:

```bash
# Entry points and CLI args
grep -rn "argparse\|click\|argv\|optparse" src/ 2>/dev/null | head -30
# Logging calls
grep -rn "logging\|logger\|log\.\(info\|debug\|error\|warning\)" src/ 2>/dev/null | head -30
# Output file writes
grep -rn "open(\|write(\|json.dump\|to_csv\|to_json" src/ 2>/dev/null | head -30
# Config and env reads
grep -rn "os.environ\|os.getenv\|config\[" src/ 2>/dev/null | head -20
```

Also inspect existing output data:
```bash
ls observe/output/ 2>/dev/null
find . -name "*.log" -o -name "*.jsonl" -o -name "*.json" 2>/dev/null | grep -v node_modules | head -20
```

Read key output files to understand structure — field names, value types, patterns already present.

From this, identify what the system already exposes and what's hidden. Use to inform script design.

## Step 3: Build observation scripts

Scaffold directory if not exists:

```bash
mkdir -p observe
```

Save all scripts directly in `observe/`. No subdirectories — observation often spans multiple concerns and shouldn't be constrained by category.

For each observable, think beyond the obvious target. Consider multiple angles:
- **Snapshot** — current state
- **Delta** — difference over time, across envs, or between versions
- **Distribution** — value ranges, frequencies, outliers
- **Absence** — what's missing that should be there
- **Correlation** — two observables that should move together but don't

Write scripts targeted at what the grill revealed — designed to discover patterns, differences, and trends around the user's concern and problem. One script per angle. Shell for quick captures, Python for structured analysis.

## Step 4: Run and interpret

Run scripts. Show output. Interpret each result — look beyond what was asked. Surface unexpected findings, including things that seem unrelated. Do not dismiss anything before examining it.

If cause found → summarize. If not → identify next observable, repeat Step 3–4.

## Step 5: Done

List all scripts written. Summarize: observation → pattern → cause (or still unknown).
