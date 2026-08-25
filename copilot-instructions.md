---
applyTo: "**"
---

# Global Instructions
## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

## Context Structure
- **MUST READ** first 10 line frontmatter when need to read some file — every `~/wiki`/`spec` document and first-party source-code file carries it; format in `references/document-style/frontmatter.md`. Always, even when the path is already known; skip the body entirely if the header alone answers the question. Applies to every wiki file touched by the rules below.
- Working area: `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` — write here during the day, no date path needed. `/end-of-day` archives both into the dated locations below at day's end.
- Journal: `~/wiki/journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,report.md,research/}` — one nested directory per day; the directory contains journal.md (daily log), handoff.md (open items/decisions for tomorrow), report.md (end-of-day synthesis), and research/ (research tasks from that day).
- Index: `index.md` files under `~/wiki/` and `journal/` are nav chains (year -> month -> day). `/end-of-day` rebuilds affected chains on each archive.
- Today's context: before starting work, read `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` (if present) for what's already in progress today.
- Handoff: before starting work, check the most recent `~/wiki/journal/YYYY/MM/YYYY-MM-DD/handoff.md` (highest date, may not be today or this month) for open items and carried decisions from the prior session.

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
