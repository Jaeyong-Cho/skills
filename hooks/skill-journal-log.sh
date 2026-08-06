#!/usr/bin/env bash
# Hook (PreToolUse on Claude Code and Copilot CLI, both scoped to the
# skill-invocation tool) — logs every skill invocation to today's journal
# file. Deterministic by design: a model reliably forgets a passive
# "remember to log this" instruction over a long session, so the invocation
# moment is logged here instead. tool_name casing differs by platform
# ("Skill" on Claude Code, "skill" on Copilot CLI, confirmed empirically),
# hence the case-insensitive match below — one script covers both.
HOOK_JSON="$(cat 2>/dev/null || true)"
[ -n "$HOOK_JSON" ] || exit 0

TOOL_NAME=$(printf '%s' "$HOOK_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)
[ "$(printf '%s' "$TOOL_NAME" | tr '[:upper:]' '[:lower:]')" = "skill" ] || exit 0

SKILL_NAME=$(printf '%s' "$HOOK_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('skill',''))" 2>/dev/null)
[ -n "$SKILL_NAME" ] || exit 0

JOURNAL="$HOME/wiki/journal/$(date +%Y)/$(date +%m)/$(date +%Y-%m-%d).md"
[ -f "$JOURNAL" ] || exit 0

{
  printf -- '- %s: SKILL invoked\n' "$(date +%H:%M:%S)"
  printf '  - skill: %s\n' "$SKILL_NAME"
} >> "$JOURNAL"
