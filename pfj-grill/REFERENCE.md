# pfj-grill Reference

## Workspace Resolution

Before invoking any pf-* skill:

1. Check if discussion mentioned a project path — if yes, use it.
2. Otherwise check cwd: `ls .pf/book.toml 2>/dev/null`
3. If not found, ask via `AskUserQuestion`: "Which project to run [skill] in? Provide the path."
4. Verify: `ls <project-path>/.pf/book.toml 2>/dev/null` — if missing, tell user to run `/pf-init` there first. Stop.

---

## Journal Entry Format

Append to `$PFJ_PATH/today.md`:

```markdown
## HH:MM:SS (grill)

**Topic**: one-line description of what was discussed

**Outcome**: key decisions / conclusions reached

**Steps**: (omit if no concrete steps surfaced)
1. Step one
2. Step two
   ```bash
   exact command here
   ```

**Report**: $PFJ_PATH/discuss/YYYY/MM-DD-topic-slug.html
```

Write concrete commands, code snippets, config values, ordered steps verbatim. Do not summarize technical details.

---

## Goals Format

```
- [ ] Task *(Priority)* *(ai: /skill-name — what it does)* — rationale *(→ Weekly: deliverable)*
```

Place in correct topic section at correct priority position. Sub-tasks under parent. If no skill fits, describe how AI helps instead of naming a skill.
