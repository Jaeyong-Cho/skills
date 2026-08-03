# Viewpoints stage

Read only when a gate sent you here — either the explore stage directly, or the core stage after a verdict.

**Read the prior stage's output first, whichever stage sent you here.** If `questions/{slug}/experiments/` exists, the core stage ran — use the resolving (or final) attempt's `result.md` plus its `raw/` as the source for what to visualize; don't re-derive by re-reading every attempt's raw output. Prior inconclusive attempts are context, not visualization material — only the attempt that closed (or best approached) the question drives the gallery. If `experiments/` doesn't exist, you arrived straight from explore — use `questions/{slug}/.context/explore/...` as the source instead, and point the gallery subagent at that evidence rather than any `raw/` (there's no execution output to visualize, only what explore found).

**Build the gallery.** **MUST DISPATCH** a claude-sonnet-5 subagent pointed at the resolving attempt's `questions/{slug}/experiments/{n}-{angle-slug}/raw/` (or, on the explore-direct path, `questions/{slug}/.context/explore/`): "with /viewpoints skill, build a gallery over <the results or evidence, drawn from the source identified above — not 'visualize everything'>, output to `questions/{slug}/gallery/`." `run_in_background: false` — Publish reads the gallery's output. Confirm `gallery/index.html` exists on disk before moving on; don't infer completion from the agent's summary alone.

No further gate — continue straight to `../SKILL.md`'s Publish.
