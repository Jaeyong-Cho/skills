# Global Instructions

## Skill Session Logging

After completing any skill or significant AI-assisted work session, log a summary to the journal.

**Check config:**
```bash
echo $PFJ_PATH
```

If `PFJ_PATH` is not set or empty: tell the user to set `PFJ_PATH` in `~/.claude/settings.json` under `env`, then stop.

If set, check today.md exists:
```bash
ls $PFJ_PATH/today.md 2>/dev/null
```

If today.md does not exist: skip silently.

If it exists, append at the bottom of `$PFJ_PATH/today.md`:

```markdown
## HH:MM:SS (skill-name)

**Summary**: concrete outcomes — what was built, changed, or decided; which files were affected

**Lessons**: what worked well, what was harder than expected, what to do differently next time, patterns worth remembering
```

Use 24h time. Use the skill name as the mark (e.g. `pf`, `pf-impl`, `pfj-grill`). For non-skill sessions use a short label (e.g. `debug`, `refactor`).

**What makes a good lesson**: not "it worked" — but *why* it worked, or what surprised you, or what you'd tell yourself before starting. One sharp observation beats three vague ones.
