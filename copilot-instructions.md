---
applyTo: "**"
---

# Global Instructions
## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

## Context Structure
- Journal: `~/wiki/journal/YYYY/MM/YYYY-MM-DD.md` — one file per day, daily log.
- Research: `~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{job}/` — one directory per day; `NN-{job}` is a zero-padded sequence number plus a short slug per research task that day (e.g. `01-vendor-eval/`).
- Advisor: `~/wiki/advisor/YYYY/MM/YYYY-MM-DD.md` — one file per day, recurring friction and automation candidates from the last 14 days.
- Handoff: before starting work, check the most recent `~/wiki/journal/YYYY/MM/YYYY-MM-DD-handoff.md` (highest date, may not be today or this month) for open items and carried decisions from the prior session.

## **MUST DO** Skill Journal Logging
Today's journal file: `~/wiki/journal/$(date +%Y)/$(date +%m)/$(date +%Y-%m-%d).md`. If it doesn't exist, skip logging.

- On invoking any skill, append: `- HH:MM:SS: SKILL start (model: MODEL_ID)` then an indented `  - skill: SKILL_NAME` line.
- On finishing that skill's work, append: `- HH:MM:SS: SKILL end` then an indented `  - summary: ONE_LINE_SUMMARY` line and `  - result: ONE_LINE_SUMMARY` line.
- Use `date +%H:%M:%S` for timestamps and append with `>>` (never overwrite).

@references/document-style.md

<!-- rtk-instructions v2 -->
# RTK — Token-Optimized CLI

**rtk** is a CLI proxy that filters and compresses command outputs, saving 60-90% tokens.

## Rule

Always prefix shell commands with `rtk`:

```bash
# Instead of:              Use:
git status                 rtk git status
git log -10                rtk git log -10
cargo test                 rtk cargo test
docker ps                  rtk docker ps
kubectl get pods           rtk kubectl pods
```

## Meta commands (use directly)

```bash
rtk gain              # Token savings dashboard
rtk gain --history    # Per-command savings history
rtk discover          # Find missed rtk opportunities
rtk proxy <cmd>       # Run raw (no filtering) but track usage
```
<!-- /rtk-instructions -->
