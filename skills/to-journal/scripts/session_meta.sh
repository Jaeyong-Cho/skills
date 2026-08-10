#!/usr/bin/env bash
# Prints this session's start time. Reads the Claude Code transcript JSONL
# if one exists for this cwd; falls back to the GitHub Copilot CLI's
# session-store.db when there is no Claude transcript.
set -euo pipefail

project_dir="$HOME/.claude/projects/$(pwd | tr '/' '-')"
transcript="$(ls -t "$project_dir"/*.jsonl 2>/dev/null | head -1 || true)"

if [ -n "$transcript" ]; then
  python3 -c "
import json
from datetime import datetime

start = None
with open('$transcript') as f:
    for line in f:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        ts = d.get('timestamp')
        if ts:
            start = ts
            break

if start:
    dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone()
    print('START=' + dt.strftime('%H:%M:%S'))
else:
    print('START=unknown')
"
  exit 0
fi

copilot_db="$HOME/.copilot/session-store.db"
if [ -f "$copilot_db" ]; then
  python3 -c "
import sqlite3
from datetime import datetime

conn = sqlite3.connect('$copilot_db')
cur = conn.cursor()
cur.execute('SELECT created_at FROM sessions WHERE cwd = ? ORDER BY updated_at DESC LIMIT 1', ('$(pwd)',))
row = cur.fetchone()

if not row:
    print('START=unknown')
else:
    dt = datetime.fromisoformat(row[0].replace('Z', '+00:00')).astimezone()
    print('START=' + dt.strftime('%H:%M:%S'))
"
  exit 0
fi

echo "START=unknown"
