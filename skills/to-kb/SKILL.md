---
name: to-kb
description: Review the whole session for findings worth keeping, gate them against KB scope, confirm any KB citation's hits/misses, then create/update/deprecate ~/wiki/kb entries accordingly — the only thing that writes hit_count/last_hit_at. Invoke as /to-kb.
disable-model-invocation: true
---

# To-KB

Any session can cite an existing `~/wiki/kb` doc while answering something — nothing that reads the KB live writes back to it. This skill is the write side, for any finished session, not a particular skill: run it afterward to turn what actually happened into KB updates, using `kb.py` (never hand-edit frontmatter).

1. **Scan the whole session for findings.** Reread this session's own context in full — every message, decision, and file touched. Pull out every candidate finding as one sentence: a settled decision, a fact, a procedure, a resolved problem. Completion criterion: a list of candidate findings (may be empty).

2. **Gate each candidate against KB scope.** A KB entry earns its keep only by being reused; most of a session isn't KB material. Tag each candidate:

   | IN | OUT |
   | --- | --- |
   | Policy/standard (convention, guideline) | Transient one-off chat, brainstorming with no landed decision |
   | Architecture/domain (structure, data flow, business rule) | Code-level implementation detail — clean code + inline comments cover that |
   | SOP/how-to (a fixed, repeatable procedure) | A third-party doc's content restated — link to it, document only the team-specific usage |
   | Post-mortem/runbook (a recurring incident's resolution) | Personal notes / WIP drafts — keep those private until finalized |

   Drop every OUT candidate — don't file it. Completion criterion: every candidate from step 1 tagged IN or OUT.

3. **Classify each KB citation as hit or miss.** List every point in this session where an existing `~/wiki/kb` doc was cited as the answer to something (however it was marked — 📚 or otherwise) and which doc it was, empty if none this session. A citation is a **hit** only if both hold:
   - **Negative rule** — the KB answer was never contradicted or overridden later in this same session.
   - **Positive rule** — something the session produced (a plan, a commit, a file) actually used that fact downstream.
   Anything else (contradicted, or never actually built on) is a **miss** — leave its `hit_count`/`last_hit_at` untouched; note it as a signal the doc may be stale or mis-tagged, but don't guess a fix without evidence. Completion criterion: every citation tagged hit or miss.

4. **Record hits.** For each hit from step 3, run `python3 scripts/kb.py hit {doc.md}` (relative to this skill's directory). Completion criterion: every hit doc's `hit_count`/`last_hit_at` updated.

5. **File IN findings — Single Source of Truth first.** For each IN candidate from step 2, and only once the human has actually confirmed it (never from an assumption alone): walk the `index.md` chain down from `~/wiki/kb/index.md` toward the finding's domain/category first, same as any other `~/wiki` lookup. An existing doc already covering this topic — update it in place (edit its body, bump `timestamp`) instead of filing a duplicate; one topic gets exactly one canonical doc. Nothing existing covers it — write a new `{domain}/{category}/{slug}.md` under `~/wiki/kb` with the full extended-OKF frontmatter (`type, title, description, tags, timestamp, created_at, owner, last_hit_at, hit_count` — see `scripts/lint_kb.py`'s docstring for the exact schema), `hit_count: 0`, `last_hit_at`/`created_at`/`timestamp` = today, body written lean (50-300 lines) from the start rather than trimmed later. Add or update that directory's `index.md` entry. Completion criterion: every IN candidate is either merged into an existing doc or filed as a new one.

6. **Lint.** Run `python3 scripts/lint_kb.py`. Fix every reported error (warnings are informational). If it reports pruning candidates, deprecate each with `python3 scripts/kb.py deprecate {doc.md}` — moves it to `~/wiki/kb-deprecated`, never a plain delete.

Completion criterion: every session finding is gated IN/OUT, every KB citation is classified and (if a hit) recorded, every IN finding is merged or filed, and `lint_kb.py` is clean of errors.

Tell the user what was recorded (hits, docs merged/filed, anything deprecated, anything dropped as OUT-of-scope) when done.
