#!/usr/bin/env bash
# Prints this session's start time, model(s), and skills used, read from its
# own Claude Code transcript JSONL — the same data skill-journal-log.sh used
# to capture per-invocation, now pulled once at /to-journal time instead.
set -euo pipefail

project_dir="$HOME/.claude/projects/$(pwd | tr '/' '-')"
transcript="$(ls -t "$project_dir"/*.jsonl 2>/dev/null | head -1 || true)"

if [ -z "$transcript" ]; then
  echo "START=unknown"
  echo "MODEL=unknown"
  echo "SKILLS=none"
  exit 0
fi

python3 -c "
import json
from datetime import datetime

start = None
models = []
skills = []

with open('$transcript') as f:
    for line in f:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        ts = d.get('timestamp')
        if ts and start is None:
            start = ts
        message = d.get('message', {})
        if d.get('type') == 'assistant':
            m = message.get('model')
            if m and m not in models:
                models.append(m)
        content = message.get('content')
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name', '').lower() == 'skill':
                    s = item.get('input', {}).get('skill')
                    if s and s not in skills:
                        skills.append(s)

if start:
    dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone()
    print('START=' + dt.strftime('%H:%M:%S'))
else:
    print('START=unknown')
print('MODEL=' + (','.join(models) or 'unknown'))
print('SKILLS=' + (','.join(skills) or 'none'))
"
