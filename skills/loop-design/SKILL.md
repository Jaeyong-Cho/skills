---
name: loop-design
description: Design and run a deterministic development loop for one concrete software goal. Use when a development task needs executable acceptance checks, fast feedback, a RED-to-GREEN path, or ordered verification before implementation.
disable-model-invocation: true
---

# Loop Design

Turn one concrete development goal into a tight, observable loop:

```text
Goal → Setup → Executable Verification → First Gap → Change → Verification → Repeat
```

Completion is `loop/verify/run.sh` exiting `0`, not an implementation narrative. Reuse fresh evidence only for intermediate decisions when the verifier's command, environment, and observed inputs remain unchanged; final acceptance MUST run full verification.

## Principles

- Verification defines completion; prefer executable evidence to interpretation.
- Start at the first meaningful failing verification.
- Order feedback cheap, fast, local, and specific before broad or expensive; reuse still-valid evidence rather than rerunning it.
- Convert important mechanically checkable design constraints into checks.
- If the gap is unclear, improve observability before adding reasoning.
- Keep loop infrastructure smaller than the problem it supports.

## Required prerequisite

Before designing a loop, **MUST run `@skills/grill-me` session** for the goal. Do not begin loop design, setup, verification, or implementation until that session reaches shared understanding and the user confirms it.

## Scope and inspect

1. Use the confirmed grill-me outcome to state the single goal's behavior, observable outputs, interfaces, enforceable architectural constraints, required repositories/environment, and completion conditions. Do not implement yet.
2. Inspect the current state: repositories and Git status, build/test/CI commands, architecture, project tools, and existing observability. Reuse sufficient mechanisms.
3. Create only the necessary structure:

   ```text
   loop/
   ├── README.md
   ├── setup/{run.sh,NN-{slug}.sh}
   ├── verify/{run.sh,NN-{slug}.sh}
   ├── tools/
   ├── config/
   ├── workspace/
   └── runs/{timestamp}/
   ```

   Create or update `loop/README.md` with the confirmed goal, scope, setup command, ordered verifiers, how to run the loop, and completion condition. It is the loop's navigation record, not a generated run report. Omit unused directories. Number executable scripts `00` through `99` in execution order only. Make `setup/run.sh` run setup scripts numerically and idempotently where practical.

## Define verification

Ask, “What MUST be true when this is complete?” Decompose that answer into ordered `verify/NN-{slug}.sh` invariants rather than implementation tasks.

- Each check exits `0` on pass and non-zero on failure.
- A failed check reports `Expected`, `Actual`, and `Evidence`.
- `verify/run.sh` runs checks numerically, stops at the first failure, and creates `loop/runs/{timestamp}/` for useful logs, metadata, failure evidence, and artifacts.
- Prefer a genuine RED check before implementation when practical; never manufacture RED merely for ceremony.
- Read [verification-design.md](references/verification-design.md) before non-trivial behavior, API, CLI, structural, or architecture checks.

Use existing project commands first. Create a small helper in `loop/tools/` only if a required invariant cannot otherwise be expressed clearly and deterministically. Read [verification-tools.md](references/verification-tools.md) before creating one.

## Hand off to loop-run

Once the goal, reproducible setup, and ordered verification are ready, invoke `@skills/loop-run` to execute the baseline, implementation, sub-agent assessment, and verification cycle. `loop-design` defines the loop; `loop-run` operates it.

## Guardrails

- Do not declare success with a failing verifier or bypass an earlier meaningful failure without a concrete reason.
- Keep one loop focused on one goal.
- Do not build generic setup, tooling, or verification frameworks speculatively.
- Enforce material, checkable design decisions—not every architectural preference.
- Do not substitute AI judgment for deterministic verification when the latter is practical.
