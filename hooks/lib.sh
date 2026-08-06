#!/usr/bin/env bash
# Shared helpers for hooks/*.sh.

# model_from_transcript <transcript_path>
# Prints the model id from the last assistant turn in a Claude Code
# transcript JSONL, or nothing if unavailable. Copilot CLI's hook payload
# has no transcript_path equivalent, so this only ever resolves on Claude
# Code — callers must handle an empty result.
model_from_transcript() {
  local transcript="$1"
  [ -n "$transcript" ] && [ -f "$transcript" ] || return 0
  tail -50 "$transcript" | python3 -c "
import json, sys
model = ''
for line in sys.stdin:
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get('type') == 'assistant':
        model = d.get('message', {}).get('model', model)
print(model)
" 2>/dev/null
}
