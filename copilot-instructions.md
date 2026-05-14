# Global Instructions

## Session Logging

After completing any significant work session, log a summary to the journal.

Check if `PFJ_PATH` is set:
```bash
echo $PFJ_PATH
```

If not set or empty: tell the user to set `PFJ_PATH` as an environment variable pointing to their journal directory, then stop.

If set, check today.md exists:
```bash
ls $PFJ_PATH/today.md 2>/dev/null
```

If today.md does not exist: skip silently.

If it exists, append at the bottom of `$PFJ_PATH/today.md`:

```markdown
## HH:MM:SS (session-label)

**Summary**: concrete outcomes — what was built, changed, or decided; which files were affected

**Lessons**: what worked well, what was harder than expected, what to do differently next time, patterns worth remembering
```

Use 24h time. Use a short label for the session (e.g. `debug`, `refactor`, `feature-name`).

**What makes a good lesson**: not "it worked" — but *why* it worked, or what surprised you, or what you'd tell yourself before starting. One sharp observation beats three vague ones.

## Session Feedback

After logging the session summary, ask for feedback using the `ask_user` tool. Generate 2–4 options relevant to what actually happened in this session — not a fixed list. Think about what could have gone better: was it slow, confusing, off-target, missing context, too many questions, wrong output format? Pick the options most likely to matter for this specific session. Use multi-select.

If the user gives feedback, note it in the summary under a **Feedback** field.
