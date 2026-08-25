# Research Topic Directory

`@skills/to-plan`, `@skills/experiment`, and `@skills/to-context` all file their output under one `~/wiki/today/research/{NN}-{slug}/` directory per topic (`plans/`, `experiments/`, `contexts/` sit inside it as siblings). Which directory a write lands in is never picked silently — confirm it with the user before the first write of a session.

1. List every existing `NN-*` directory under `~/wiki/today/research/` — its slug, plus a one-line peek at whatever's already inside (`plans/`, `experiments/`, or `contexts/`) so the user can tell what each one is about without opening it.
2. Recommend one:
   - This session is continuing a topic already open today (same question, same feature) → recommend that existing `{NN}-{slug}` directory.
   - Otherwise → recommend a new directory: `{NN}` the next zero-padded sequence number (count existing `NN-*` directories, starting at `00`), `{slug}` a kebab-case slug of this session's topic.
3. Ask the user to confirm the recommendation or name a different existing directory. No `NN-*` directories exist yet → skip the question, state the new one being created.

Once confirmed, reuse that directory for every write for the rest of the session — don't re-ask on a later write within the same session, including a later write by a *different* one of these three skills continuing the same session.

`@skills/end-of-day` archives `~/wiki/today/research/` into the dated `~/wiki/journal/YYYY/MM/YYYY-MM-DD/research/` path at day's end.
