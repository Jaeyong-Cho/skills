---
name: gtd-grill-me
description: Run a @skills/grill-me interview to clarify a brain-dump of tasks using David Allen's GTD method — capture raw items, then for each decide actionable or not, single action or project, do-now/delegate/defer/calendar, until every item lands in one concrete bucket. Invoke as /gtd-grill-me.
disable-model-invocation: true
---

# GTD Grill Me

**MUST RUN** `@skills/grill-me` over the user's raw capture — a brain dump, a single stray thought, or an existing inbox. Phrase every question in plain, ELI5 language.

For every item, work David Allen's **clarify** tree until it lands in exactly one bucket. The frontier is empty only once every captured item has a bucket:

1. **Capture** — write the item down as it came, unedited.
2. **Actionable?**
   - No, but might matter later → **Someday/Maybe**
   - No, worth keeping only for lookup → **Reference**
   - No, truly dead → **Trash** — say so, don't file it anywhere
   - Yes → continue
3. **More than one step to finish?** → **Project** — name its outcome (what done looks like), then recurse: run step 2 on each piece until every leaf is one single, physical, visible next action. "Figure out taxes" is not a leaf; "email accountant the 1099s" is.
4. **Single next action** — decide:
   - Under 2 minutes → **Do now** — note it as done, don't file it.
   - Someone else's move → **Delegate** → **Waiting For** (who, what, follow-up date)
   - Tied to a real date/time → **Calendar** (date)
   - Otherwise → **Next Action** (optional context tag: `@computer`, `@calls`, `@errands`, `@home`...)

**MUST NOT** silently drop a captured item — every one above ends up tagged with its bucket in the transcript, even Trash.
**MUST STOP** grill session when finding the immediately actionable item.

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — ask its Mode question before round 1, then its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark for the rest of this session.

For every point in the checklist above: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round. **MUST NOT** silently drop any checklist point — every one above appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST show evidence, not just a conclusion.** Every `Decision:` line and every `➡️` recommended answer cites what it's based on — a file:line, a grep/command output, or an existing pattern found in the repo — found by a sub-agent per `@skills/grill-me`'s "Finding facts is your job" rule, not asserted from memory. No evidence found → say so and mark uncertainty High instead of guessing.

## When the user can't decide a bucket
Per `@skills/grill-me`'s "When the user can't answer one": take Someday/Maybe as the default bucket rather than stalling the round, tag it as an assumption, and move on.

Once complete, next step is `@skills/to-gtd` to file the recorded buckets into `~/wiki/gtd/`.
