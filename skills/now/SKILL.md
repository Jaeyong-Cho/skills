---
name: now
description: Break out of whatever's running — a grill-me round, any conversation — and get one task done immediately, then resume exactly where it paused. Invoke as /now.
disable-model-invocation: true
---

# Now

Do the task immediately, no plan, no round, no confirmation — then pick the interrupted flow back up exactly where it paused.

1. **Take the task.** Whatever accompanies this invocation is the task; if nothing was given, the thing already under discussion (the message right before `/now`) is the task. Ambiguous which thing is meant → ask once; otherwise proceed without clarifying.
2. **Do it directly.** Run `/ponytail`'s reflex — reuse before you build, smallest working change — and use whatever tool or skill actually fits the task. No plan file, no confirmation round, no routing back through `grill-me` or any interview to get permission first.
3. **Resume.** Interrupted another skill's flow (a `grill-me` round, a checklist, an in-progress step) → pick it back up exactly where it paused, same open questions, nothing dropped. If the task's real result settles one of those open questions, say so inline (cite what changed) instead of re-asking it blind; otherwise re-ask it unchanged next round. Nothing was interrupted → there's nothing to resume, stop after step 2.

Completion criterion: the task is done for real, not deferred to a plan, and any interrupted flow is back in its own next step with nothing silently skipped.
