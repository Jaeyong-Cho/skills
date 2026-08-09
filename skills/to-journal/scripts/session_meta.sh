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
usage_by_id = {}  # dedupe streamed re-emits of the same assistant message; mid -> (model, usage)

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
                usage_by_id[mid] = (m, usage)
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

usages = [u for _, u in usage_by_id.values()]
inp = sum(u.get('input_tokens', 0) for u in usages)
out = sum(u.get('output_tokens', 0) for u in usages)
cache_w = sum(u.get('cache_creation_input_tokens', 0) for u in usages)
cache_r = sum(u.get('cache_read_input_tokens', 0) for u in usages)
total = inp + out + cache_w + cache_r
if usage_by_id:
    print(f'TOKENS={total:,} (in:{inp:,} out:{out:,} cache_write:{cache_w:,} cache_read:{cache_r:,})')
else:
    print('TOKENS=unknown')

# \$/1M tokens (input, output). Cache write: 1.25x input (5m) / 2x input (1h). Cache read: 0.1x input.
PRICING = [
    ('claude-sonnet-5', 3.00, 15.00),
    ('claude-opus-5', 5.00, 25.00),
    ('claude-haiku-4-5', 1.00, 5.00),
]
def price_for(model):
    for prefix, p_in, p_out in PRICING:
        if model and model.startswith(prefix):
            return p_in, p_out
    return None

cost = 0.0
unpriced = 0
for model, u in usage_by_id.values():
    price = price_for(model)
    if not price:
        unpriced += 1
        continue
    p_in, p_out = price
    cc = u.get('cache_creation') or {}
    w5m = cc.get('ephemeral_5m_input_tokens', 0)
    w1h = cc.get('ephemeral_1h_input_tokens', 0)
    r = u.get('cache_read_input_tokens', 0)
    cost += (
        u.get('input_tokens', 0) * p_in
        + w5m * p_in * 1.25
        + w1h * p_in * 2.0
        + r * p_in * 0.1
    ) / 1e6
    cost += u.get('output_tokens', 0) * p_out / 1e6

if usage_by_id and cost > 0:
    suffix = f' (approx; {unpriced} unpriced msgs)' if unpriced else ''
    print(f'AIU=\${cost:.4f}{suffix}')
else:
    print('AIU=unknown')
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
