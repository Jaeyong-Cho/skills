---
name: write-blog
description: Write a blog post from a raw memo file — a goal-and-why, what-done, what-learned narrative for readers outside the work. Invoke as /write-blog {memo file path}.
disable-model-invocation: true
---

# Write Blog

Turns a raw memo — rough personal notes on finished work — into a blog post for readers outside that work. Every blog carries the same three pillars, in order: **Goal & Why** (the problem and why it mattered), **What Done** (the concrete work), **What Learned** (the insight worth keeping). Unlike `../references/document-style.md`'s bullet report, a blog reads as flowing narrative prose — no bullet-per-fact.

1. **Read & ground** — read the memo at the path the user gave; ask for one if none was given. Identify the three pillars from its content. If a pillar is thin or missing (e.g. it lists what was done but never says why), ask the user rather than inventing it. Completion criterion: goal-and-why, what-done, and what-learned are each traceable to the memo's own words or an answer the user gave — none fabricated.
2. **Draft the blog** — title it, then write the three pillars in order as narrative prose (a few paragraphs per pillar, not bullets). Completion criterion: title present; sections appear in Goal & Why → What Done → What Learned order; each reads as prose for an outside reader, not an internal report.
3. **Confirm the destination** — ask the user for the file path to write to. Completion criterion: user has given a concrete file path.
4. **Write the file** — `mkdir -p` the parent directory if needed, then write the draft. Completion criterion: the file exists at the confirmed path.

Tell the user the file path when done.

## Example

Raw memo, `notes/2026-07-10-ci-speedup.md`:
```
2026-07-10
Goal: cut CI pipeline time, was at 22 min, blocking fast iteration on PRs.
Did: parallelized test shards (4 -> 12 workers), cached the docker layer build,
     moved lint to its own job that runs first instead of last.
Result: pipeline down to 7 min.
Learned: lint failures were 80% of red builds — running lint first saved more
     wall-clock time than the parallelization did.
```

Resulting blog, `notes/2026-07-10-ci-speedup-blog.md`:
```
# How We Cut CI From 22 Minutes to 7

## Goal & Why
Our CI pipeline had crept up to 22 minutes, and it was starting to cost us —
every PR round-trip meant a 22-minute wait before you knew if you'd broken
anything, so people batched changes instead of iterating. We set out to bring
that down enough to make fast iteration normal again.

## What Done
We split the test suite across more workers, going from 4 shards to 12. We
cached the Docker layer build so it wasn't rebuilding from scratch every run.
And we pulled linting into its own job, moved to run first instead of last.

## What Learned
The parallelization helped, but the real win was reordering: lint failures
turned out to be causing 80% of our red builds, and running lint first meant
we caught those in seconds instead of after a 15-minute test run. Fixing the
order saved more wall-clock time than adding workers did.
```
