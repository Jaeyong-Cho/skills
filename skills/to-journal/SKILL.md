---
name: to-journal
description: Summarize this session very short, ELI5-simple, and append it as a formatted entry to today's journal. Invoke as /to-journal.
disable-model-invocation: true
---

# To-Journal

Turn this session into a journal entry a total non-expert could understand at a glance — not a report, a log line.

1. **Follow document style.** Read `../references/document-style.md` first — its size limits govern this entry: 1-3 sentences, prefer key-value/bullets over prose.
2. **Scope the session** — reread it in full. Pull out: what was asked, what changed, what's next (if anything). Completion criterion: each fits in one plain sentence.
3. **Read session info directly** — no script. Find this session's transcript with `ls -t ~/.claude/projects/$(pwd | tr '/' '-')/*.jsonl | head -1` and read it: the `timestamp` of its first line is the start time (convert to local `HH:MM:SS`); every distinct `input.skill` from a tool call named `Skill` is a skill used this session. If no transcript exists, use `unknown` for start and omit skills.
4. **Write it ELI5, exact where it matters.** No jargon, no file paths unless essential, no internal tool names. Explain it the way you'd explain it to someone with zero context on this codebase. If a sentence needs a technical term to make sense, it's not ELI5 yet — simplify further. When a file, command, or identifier is essential enough to include, write it as its exact string (`references/good-harness.md`, not "a reference doc") — never paraphrased.
5. **Format the entry** as:
   ```
   - HH:MM:SS: AI {one-line title}
     - start: {START from step 3}
     - skills: {comma-separated skills from step 3, omit line if none}
     - what: {ELI5, 1 sentence}
     - done: {ELI5, 1 sentence}
   ```
   Get the timestamp with `date +%H:%M:%S`.
6. **Append to today's journal** — `~/wiki/today/journal.md`, creating the file with a `# YYYY-MM-DD` heading (`date +%Y-%m-%d`) if it doesn't exist yet. Never overwrite existing content. `@skills/end-of-day` archives it into the dated `~/wiki/journal/` path at day's end — write to `today/journal.md` regardless of what day it is.

Tell the user the journal path when done.
