#!/usr/bin/env bash
# Prints this session's start time, model(s), and skills used. Reads the
# Claude Code transcript JSONL if one exists for this cwd, the same data
# skill-journal-log.sh used to capture per-invocation, now pulled once at
# /to-journal time instead. Falls back to the GitHub Copilot CLI's
# session-store.db when there is no Claude transcript.
set -euo pipefail

project_dir="$HOME/.claude/projects/$(pwd | tr '/' '-')"
transcript="$(ls -t "$project_dir"/*.jsonl 2>/dev/null | head -1 || true)"

if [ -n "$transcript" ]; then
  python3 -c "
import json
from datetime import datetime

start = None
models = []
skills = []
usage_by_id = {}  # dedupe streamed re-emits of the same assistant message

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
            usage = message.get('usage')
            mid = message.get('id')
            if usage and mid:
                usage_by_id[mid] = usage
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

inp = sum(u.get('input_tokens', 0) for u in usage_by_id.values())
out = sum(u.get('output_tokens', 0) for u in usage_by_id.values())
cache_w = sum(u.get('cache_creation_input_tokens', 0) for u in usage_by_id.values())
cache_r = sum(u.get('cache_read_input_tokens', 0) for u in usage_by_id.values())
total = inp + out + cache_w + cache_r
if usage_by_id:
    print(f'TOKENS={total:,} (in:{inp:,} out:{out:,} cache_write:{cache_w:,} cache_read:{cache_r:,})')
else:
    print('TOKENS=unknown')
print('AIU=n/a')
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
cur.execute('SELECT id, created_at FROM sessions WHERE cwd = ? ORDER BY updated_at DESC LIMIT 1', ('$(pwd)',))
row = cur.fetchone()

if not row:
    print('START=unknown')
    print('MODEL=unknown')
    print('SKILLS=none')
    print('TOKENS=unknown')
    print('AIU=unknown')
else:
    session_id, created_at = row
    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00')).astimezone()
    print('START=' + dt.strftime('%H:%M:%S'))

    cur.execute('SELECT DISTINCT model FROM assistant_usage_events WHERE session_id = ?', (session_id,))
    models = [r[0] for r in cur.fetchall() if r[0]]
    print('MODEL=' + (','.join(models) or 'unknown'))

    # Copilot has no per-skill tool_use log — approximate from slash commands typed by the user.
    cur.execute('SELECT user_message FROM turns WHERE session_id = ? ORDER BY turn_index', (session_id,))
    skills = []
    for (msg,) in cur.fetchall():
        if msg and msg.startswith('/'):
            s = msg[1:].split()[0]
            if s and s not in skills:
                skills.append(s)
    print('SKILLS=' + (','.join(skills) or 'none'))

    cur.execute('''
        SELECT COALESCE(SUM(input_tokens), 0), COALESCE(SUM(output_tokens), 0),
               COALESCE(SUM(cache_read_tokens), 0), COALESCE(SUM(cache_write_tokens), 0),
               COALESCE(SUM(total_nano_aiu), 0)
        FROM assistant_usage_events WHERE session_id = ?
    ''', (session_id,))
    inp, out, cache_r, cache_w, nano_aiu = cur.fetchone()
    total = inp + out + cache_r + cache_w
    if total:
        print(f'TOKENS={total:,} (in:{inp:,} out:{out:,} cache_write:{cache_w:,} cache_read:{cache_r:,})')
    else:
        print('TOKENS=unknown')
    # total_nano_aiu is AIU (Copilot's premium-request billing unit) scaled by 1e9.
    print(f'AIU={nano_aiu / 1e9:.4f}' if nano_aiu else 'AIU=unknown')
"
  exit 0
fi

echo "START=unknown"
echo "MODEL=unknown"
echo "SKILLS=none"
echo "TOKENS=unknown"
echo "AIU=unknown"
