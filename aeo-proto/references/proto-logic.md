# Logic Prototype

Use when the question is about **business logic, state transitions, or data shape**.

## Steps

1. **State the question** — what state model and hypothesis are you testing?
2. **Match the host project's language** — no new dependencies or runtimes
3. **Isolate logic as a pure module** — reducer, state machine, or functions; no I/O, no terminal code
4. **Build a minimal TUI** — current state at top, keyboard shortcuts at bottom, re-render after each action
5. **Add a run command** — integrate with the project's existing task runner
6. **Let the user explore** — conceptual flaws surface when the user says "wait, that shouldn't be possible"
7. **Document findings** — capture what the prototype revealed before discarding the TUI shell

## Rules

- Keep the logic module **pure** — no I/O, no logging for control flow, no terminal code
- The TUI is throwaway; the validated logic module is what transfers into production
- No tests, no abstractions, no real database connections during prototyping
