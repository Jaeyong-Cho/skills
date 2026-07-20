---
name: write-blog
description: Write a blog post from a raw memo file — a goal, what-learned, what-done journal entry. Invoke as /write-blog {memo file path}.
disable-model-invocation: true
---

# Write Blog

Turns a raw memo — rough personal notes on finished work — into a blog post with three parts, in order: **Goal** (kept exactly as the memo states it), **What I Learned** (one topic per subsection, each grounded in an example), **What I Done** (one task per subsection, each grounded in an example).

1. **Read & ground** — read the memo at the path the user gave; ask for one if none was given. Identify the memo's own top-level header and its Goal section, plus every learning and every task described. If learnings or tasks are thin or missing, ask the user rather than inventing them. Completion criterion: every subsection is traceable to the memo's own words or an answer the user gave — none fabricated.
2. **Draft the blog** — reuse the memo's own top-level header, its date, and its Goal section verbatim: same title wording, same date, same Goal bullets, unchanged. Do not invent a new title or rewrite Goal into prose. After it, write `## What I Learned`, with one `### <topic>` subsection per concept, each explained through a concrete example (code, before/after, or a worked number) rather than narrative paragraphs. Then write `## What I Done`, with one `### <task>` subsection per piece of work, each also grounded in a concrete example. Completion criterion: header, date, and Goal match the memo unchanged; sections appear in Goal → What I Learned → What I Done order; every subsection carries an example.
3. **Confirm the destination** — ask the user for the file path to write to. Completion criterion: user has given a concrete file path.
4. **Write the file** — `mkdir -p` the parent directory if needed, then write the draft. Completion criterion: the file exists at the confirmed path.

Tell the user the file path when done.

## Example

Raw memo, `notes/2026-07-10-ci-speedup.md`:
```
# CI Speedup 1
2026-07-10

## Goal
- Cut CI pipeline time, was at 22 min, blocking fast iteration on PRs

## Raw Memo
- Parallelized test shards (4 -> 12 workers)
- Cached the docker layer build
- Moved lint to its own job that runs first instead of last
- Result: pipeline down to 7 min
- Learned: lint failures were 80% of red builds — running lint first saved more
  wall-clock time than the parallelization did
```

Resulting blog, `notes/2026-07-10-ci-speedup-blog.md`:
```
# CI Speedup 1
- date: 2026-07-10

## Goal
- Cut CI pipeline time, was at 22 min, blocking fast iteration on PRs

## What I Learned
### Lint failures dominate red builds
- 80% of red builds were caused by lint failures, not test failures. e.g. moving
  lint to run first instead of last meant a broken PR failed in seconds instead
  of after a 15-minute test run — reordering saved more wall-clock time than
  parallelizing the tests did.

## What I Done
### Parallelized test shards
- Went from 4 workers to 12. e.g. a run that took 12 minutes across 4 shards
  dropped to roughly 4 minutes across 12.
### Cached the Docker layer build
- Stopped rebuilding image layers from scratch every run, reusing the cache
  when the Dockerfile and lockfiles were unchanged.
### Reordered lint to run first
- Moved lint into its own job ahead of the test suite, instead of after it.
```
