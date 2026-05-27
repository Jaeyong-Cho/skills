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

Run `grill-me` focused on extracting:
- **Concerns** — what worries the user, what feels wrong or uncertain
- **Already known** — what they've already observed or confirmed
- **Expected** — what they expect to see when they look

No maximum questions. Keep going until all three are clear. These become the baseline — scripts will be built to confirm, challenge, or go beyond what's already known.

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

Write scripts that surface these patterns. Use grill findings as guide: write at least one script that challenges each concern, one that tests each expectation, and one that goes beyond what's already known. One script per angle. Shell for quick captures, Python for structured analysis.

## Step 4: Run and interpret

Run scripts. Show output. For each result, look beyond the expected:
- What's present vs. expected?
- What's absent that should be there?
- Any value that looks wrong — too high, too low, or inconsistent?
- Any pattern that appears where it shouldn't, or is missing where it should be?
- Does this confirm or deny the hypothesis — and does it reveal something else?

Surface unexpected findings explicitly — including things that seem unrelated to the original question. Unrelated observations often carry the most interesting patterns: a dependency version mismatch, an env var set to an unexpected value, a log line that appears too often or not at all. Do not dismiss anything as irrelevant before examining it.

If cause found → summarize. If not → identify next observable, repeat Step 3–4.

## Step 5: Done

List all scripts written. Summarize: observation → pattern → cause (or still unknown).
