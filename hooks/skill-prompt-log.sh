#!/usr/bin/env bash
# UserPromptSubmit hook — catches the case skill-journal-log.sh structurally
# can't see: the user typing "/skill-name" directly. A typed slash command is
# intercepted by the CLI's own command layer and never becomes a tool call,
# so no PreToolUse/PostToolUse event fires for it — this hook pattern-matches
# the raw prompt text instead. Valid skill names are read live from the
# installed skills directory, not hardcoded, so this doesn't go stale when
# skills are added/renamed/removed.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

HOOK_JSON="$(cat 2>/dev/null || true)"
[ -n "$HOOK_JSON" ] || exit 0

PROMPT=$(printf '%s' "$HOOK_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('prompt', d.get('message', '')))" 2>/dev/null)
[ -n "$PROMPT" ] || exit 0

# Match a leading "/skill-name" (word chars and hyphens), ignoring anything after.
SLASH_WORD=$(printf '%s' "$PROMPT" | python3 -c "
import re, sys
m = re.match(r'^/([a-zA-Z0-9-]+)', sys.stdin.read())
print(m.group(1) if m else '')
" 2>/dev/null)
[ -n "$SLASH_WORD" ] || exit 0

SKILLS_ROOT="$HOME/.claude/skills"
[ -d "$SKILLS_ROOT" ] || SKILLS_ROOT="$HOME/.copilot/skills"
[ -d "$SKILLS_ROOT/$SLASH_WORD" ] || exit 0

JOURNAL="$HOME/wiki/journal/$(date +%Y)/$(date +%m)/$(date +%Y-%m-%d).md"
[ -f "$JOURNAL" ] || exit 0

TRANSCRIPT=$(printf '%s' "$HOOK_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('transcript_path',''))" 2>/dev/null)
MODEL=$(model_from_transcript "$TRANSCRIPT")

{
  if [ -n "$MODEL" ]; then
    printf -- '- %s: SKILL invoked (typed command, model: %s)\n' "$(date +%H:%M:%S)" "$MODEL"
  else
    printf -- '- %s: SKILL invoked (typed command)\n' "$(date +%H:%M:%S)"
  fi
  printf '  - skill: %s\n' "$SLASH_WORD"
} >> "$JOURNAL"
