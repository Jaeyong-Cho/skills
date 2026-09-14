# Verification Tools

Use existing project commands first: compiler, test framework, build system, CLI, static analyzer, linter, `grep`, `jq`, or `git`.

Create a helper only when no existing command can express one required cycle check clearly and deterministically. Put it in the cycle that needs it, name it `NN-{step}.sh`, and keep it focused on one observable question.

A helper should have clear inputs and outputs, a meaningful exit status, and failure evidence. Do not build a generic verification framework or a shared abstraction before repeated concrete use proves it necessary.
