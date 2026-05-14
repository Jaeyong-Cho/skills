# Global Instructions

## Skill Session Logging

After completing any skill session, log a summary to the journal.

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

**Summary**: what was done this session — concrete outcomes, files changed, decisions made

**Lessons**: key insights, patterns noticed, or things to do differently next time
```

Use 24h time. Use the skill name as the mark (e.g. `pf`, `pf-impl`, `pfj-grill`). Keep both fields tight — this is a reflection entry, not a report.
