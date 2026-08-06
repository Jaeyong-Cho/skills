---
name: to-journal
description: Summarize this session very short, ELI5-simple, and append it as a formatted entry to today's journal. Invoke as /to-journal.
disable-model-invocation: true
---

# To-Journal

Turn this session into a journal entry a total non-expert could understand at a glance — not a report, a log line.

1. **Follow document style.** Read `../references/document-style.md` first — its size limits govern this entry: 1-3 sentences, prefer key-value/bullets over prose.
2. **Scope the session** — reread it in full. Pull out: what was asked, what changed, what's next (if anything). Completion criterion: each fits in one plain sentence.
3. **Write it ELI5.** No jargon, no file paths unless essential, no internal tool names. Explain it the way you'd explain it to someone with zero context on this codebase. If a sentence needs a technical term to make sense, it's not ELI5 yet — simplify further.
4. **Format the entry** as:
   ```
   - HH:MM:SS: JOURNAL {one-line title}
     - what: {ELI5, 1 sentence}
     - done: {ELI5, 1 sentence}
   ```
   Get the timestamp with `date +%H:%M:%S`.
5. **Append to today's journal** — `~/wiki/journal/YYYY/MM/YYYY-MM-DD.md` (`date +%Y/%m/%Y-%m-%d`), creating the file with a `# YYYY-MM-DD` heading if it doesn't exist yet. Never overwrite existing content.

Tell the user the journal path when done.
