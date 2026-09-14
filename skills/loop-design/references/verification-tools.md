# Verification Tools

Custom verification tools are local to the current development loop:

```text
loop/tools/
```

`verify/` states **what MUST be true**. `tools/` supplies a small mechanism to determine **whether it is true**.

## Decision rule

Before writing a helper, use this sequence:

```text
Need verification
      ↓
Can an existing mechanism express it?
├── yes → use it
└── no  → create the smallest helper
```

Existing mechanisms include the compiler, test framework, build system, project CLI, `grep`, `jq`, `git`, installed linters, and static analyzers.

## Requirements

A custom helper should:

- serve one concrete verification need;
- be deterministic where practical;
- accept clear inputs and produce clear output;
- return a meaningful exit status;
- present useful failure evidence; and
- remain small and focused.

Examples:

```text
loop/tools/check_api.py
loop/tools/check_dependency.py
loop/tools/inspect_cli.py
```

Do not create a generic verification framework because several scripts look similar. Wait for repeated concrete use to demonstrate a stable abstraction. The maintenance cost of the loop must remain substantially lower than its feedback value.
