# Viewpoints stage

Read only when a gate sent you here — either the explore stage directly, or the core stage after a verdict.

**Read the prior stage's output first, whichever stage sent you here.** If `questions/{slug}/hypothesis.md` exists, the core stage ran — use it plus the verdict/analysis as the source for what to visualize; don't re-derive by re-reading everything under `raw/`. If it doesn't exist, you arrived straight from explore — use `questions/{slug}/.context/explore/...` as the source instead, and point the gallery subagent at that evidence rather than `raw/` (there's no execution output to visualize, only what explore found).

**Build the gallery.** **MUST DISPATCH** a claude-sonnet-5 subagent pointed at `questions/{slug}/raw/` (or, on the explore-direct path, `questions/{slug}/.context/explore/`): "with /viewpoints skill, build a gallery over <the results or evidence, drawn from the source identified above — not 'visualize everything'>, output to `questions/{slug}/gallery/`." `run_in_background: false` — Publish reads the gallery's output. Confirm `gallery/index.html` exists on disk before moving on; don't infer completion from the agent's summary alone.

No further gate — continue straight to `../SKILL.md`'s Publish.
