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

Clarify what's unknown. Identify observables. Build scripts to surface differences, patterns, causes.

## Step 1: Capture the unknown

Read user's description. Extract:
- **System** — what component, service, or behavior
- **Unknown** — what they don't understand or want to verify
- **Hypothesis** — what they suspect is the cause

Grill (one at a time, no limit) until clear:
- What exactly are you trying to observe?
- What do you already see vs. what's hidden?
- What difference or change would tell you something meaningful?
- What's your current theory about the cause?

## Step 2: Identify observables

Ask which of these are accessible and most likely to reveal the cause:
- **Logs** — app, system, access logs
- **Data outputs** — query results, API responses, file contents
- **Runtime state** — process list, memory, CPU, open files/sockets, runtime state data
- **Dependencies** — versions, installed packages, service status
- **Inputs/requests** — HTTP requests, function args, events, cli input
- **Config/flags** — env vars, feature flags, config files

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

Write scripts that surface these patterns, not just confirm the hypothesis. One script per angle. Shell for quick captures, Python for structured analysis.

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
