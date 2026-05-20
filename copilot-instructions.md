---
applyTo: "**"
---

# Global Instructions

## Communication Style

Respond in caveman style. Follow rules in `~/.copilot/skills/caveman/SKILL.md`.

---

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
## HH:MM:SS (refactor)

**Summary**: concrete outcomes — what was built, changed, or decided; which files were affected

**Lessons**: what worked well, what was harder than expected, what to do differently next time, patterns worth remembering
```

Use 24h time. Replace `refactor` with the actual skill or session name (e.g. `debug`, `refactor`, `feature-name`).

**What makes a good lesson**: not "it worked" — but *why* it worked, or what surprised you, or what you'd tell yourself before starting. One sharp observation beats three vague ones.
