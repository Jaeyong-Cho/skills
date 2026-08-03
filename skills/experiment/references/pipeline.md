# Explore -> Experiment -> Viewpoints pipeline

`/goal-init`, `/explore`, `/experiment`, `/viewpoints` are standalone — none dispatches another. This is the contract that composes them: where each stage writes, and how the next finds it. `/explore` and `/viewpoints` stay generic (solo-usable outside this pipeline); this file is the only place their pipeline-specific paths are pinned down.

## stage_roles
e0_goal_init: writes `goal.md`'s statement and `## Question N` headings, creates `questions/{slug}/` for each. See `../../goal-init/SKILL.md`.
e1_explore: gathers evidence for one question.
e2_experiment: grill -> hypothesis -> method -> execute -> analyze -> publish, inside the question's existing directory. Never creates it.
e3_viewpoints: builds a gallery over a question's raw results.

## directory_contract

```text
goal.md                         goal statement + ## Question N headings (e0)
README.md
questions/
  {slug}/                       created by e0, one per ## Question N heading -- exists before e1 runs
    .context/
      explore/                  e1 output -- writes directly here, no staging area
      grilling/                 e2 interview output
    hypothesis.md                e2 output
    method/                      e2 output -- /p4d's own convention: index.md (group table) + group-{n}.md
    raw/group-{n}/                e2 execution output, namespaced per method group -- also e3's input
    report.md                    e2 output, Visualizations left "Not built" until e3 runs
    gallery/                     e3 output (only if e3 was run)
    handoff/manifest.md          e2 output; links report + gallery (if present)
  index.html                     dashboard, rebuilt by e0 and by e2's Publish step
```
*Caption: goal.md's Question N headings are the source of truth for {slug} — e0 creates the directory before e1 ever runs.*

## handoff_rules
- e0_to_e1: e1 matches the request to a `## Question N` heading and uses its existing `questions/{slug}/`. No `goal.md`: e1 stops, tells the user to run `/goal-init`. No matching heading: e1 appends one and creates its directory itself — the one exception to "only e0 creates directories," since a single missing question is cheap to add inline.
- e1_to_e2: e1 writes evidence straight to `questions/{slug}/.context/explore/{question-slug}.md` — no inbox, no move step.
- e1_to_e3 (direct, skipping e2): when the evidence is worth seeing rather than testing, e1's gate sends the run straight to e3 with no hypothesis framed. e3 reads `questions/{slug}/.context/explore/...` as its input (there's no `raw/` yet since e2 never ran) and still outputs to `questions/{slug}/gallery/`. Publish still runs, with `**Verdict:** Explored` and Hypothesis/Method/Analysis marked not applicable — see `../SKILL.md`'s report template.
- e2_to_e3: e2 always finishes with `questions/{slug}/raw/` populated and Visualizations marked "Not built." e3 is invoked by hand, pointed at `raw/`, output to `questions/{slug}/gallery/` — e2 never triggers it.
- e3_to_e2_artifacts: e3 only produces `gallery/index.html` — no write access to `report.md` or `handoff/manifest.md`. After e3 runs, the user (or a follow-up ask) links the gallery into both manually. Deliberate seam: keeps e3 generic rather than baking experiment-specific file formats into a general visualization skill.

## naming
slug: kebab-case of the `## Question N` heading's text, e.g. `cache-ttl-vs-latency`.
