---
name: gtd-review
description: Run David Allen's GTD Weekly Review over ~/wiki/gtd/ — sweep every list for stalled projects, overdue Waiting For, past-due Calendar items, and Someday/Maybe worth reconsidering, then grill the user on each and file the decisions. Invoke as /gtd-review.
disable-model-invocation: true
---

# GTD Review

David Allen's Weekly Review, over the system `@skills/to-gtd` writes at `~/wiki/gtd/`: **Get Clear** (nothing left uncaptured), **Get Current** (every list still matches reality), **Get Creative** (Someday/Maybe reconsidered, not just re-read).

1. **Get Clear — empty any loose capture.** If the user has anything on their mind not yet in `~/wiki/gtd/` (a fresh brain-dump, a stray note), run `@skills/gtd-grill-me` on it first, then `@skills/to-gtd` to file it. Completion criterion: nothing left uncaptured.
2. **Get Current — sweep every list for facts, not decisions.** Finding facts is your job, never the user's (per `@skills/grill-me`):
   - **Stalled projects** — every `projects/{slug}.md` with zero unchecked `- [ ]` lines under `## Next Actions`. No open next action means nothing to act on.
   - **Overdue Waiting For** — every `waiting-for.md` line whose follow-up date has already passed.
   - **Past-due Calendar** — every `calendar.md` line whose date has passed and is still `- [ ]` (unchecked — a done one would already be archived).
   - **Someday/Maybe** — the whole `someday-maybe.md` list; the point of review is looking at it again, not filtering it further.
   Completion criterion: every file under `~/wiki/gtd/` except `archive/` and `reference.md` has been read in full this round.
3. **Get Creative — grill the user on what surfaced.** Run `@skills/grill-me` over step 2's findings, one question per surfaced item, capped at 5 per round same as any grill-me round:
   - Stalled project → what's its next action?
   - Overdue Waiting For → follow up now (new Next Action: "chase {who}"), or push the follow-up date out?
   - Past-due Calendar → still needed (reschedule to a new date, or convert to a Next Action), or drop it (cancel)?
   - Someday/Maybe item → activate now (run its `@skills/gtd-grill-me` clarify tree), keep waiting, or Trash it?
   Completion criterion: every item surfaced in step 2 has a decision, none silently dropped — an empty category from step 2 needs no question.
4. **File every decision** via `@skills/to-gtd` — new Next Actions, updated Waiting For dates, rescheduled/cancelled Calendar items, Someday/Maybe promotions or deletions, stalled-project next actions. Its lint step (`scripts/lint_gtd.py`) runs as part of that; don't re-run it separately here.

Tell the user a one-line count per category from step 2 (stalled projects, overdue Waiting For, past-due Calendar, Someday/Maybe reviewed) when done.
