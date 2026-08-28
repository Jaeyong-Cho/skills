# Subagents vs. Skills

Subagents are specialized assistants that an AI agent can delegate tasks to. Characteristics:
- Isolated context: Each subagent has its own context window
- Parallel execution: Multiple subagents can run simultaneously
- Specialization: Configured with specific prompts and expertise
- Reusable: Defined once, used in multiple contexts

## When to use subagents vs. skills

```
Is the task complex with multiple steps?
├─ YES → Does it require isolated context?
│         ├─ YES → Use SUBAGENT
│         └─ NO → Use SKILL
│
└─ NO → Use SKILL
```

Use subagents for:
- Complex workflows requiring isolated context
- Long-running tasks that benefit from specialization
- Verification and auditing (independent perspective)
- Parallel workstreams

Use skills for:
- Quick, one-off actions
- Domain knowledge without context isolation
- Reusable procedures that don't need isolation
