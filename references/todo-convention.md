# Todo Document Convention

A target project's implementation todos live under `todo/**/*.md`, one file per vertical slice — a complete, independently-shippable unit (e.g. one sub-topic from a spec), never a horizontal layer (e.g. not "backend" + "frontend" for one feature).

Each todo file is temp scratch, not a persisted document like `spec/`: no per-file ceremony beyond the link and checklist. Format:

```
Spec: spec/{topic-slug}.md#{sub-topic}

- [ ] {action item}
- [ ] {action item}
```

- One file per slice: `todo/{topic-slug}.md`, matching the spec sub-topic it implements.
- First line links back to its spec — the todo lists *how*, the spec already said *what*; don't restate AC or requirements here.
- Checklist ordered so the slice builds end-to-end top to bottom.
- Delete the file once every item is checked — it's disposable, the spec is the record that lasts.

## `todo/index.md` — the WBS guide

`todo/index.md` is the work-breakdown-structure across all active slices: which slices block which, and what can run in parallel. Format:

```
Round 1: {slug-a}, {slug-b}
Round 2: {slug-c}*
```

- One line per round; a round's slugs can run in parallel, later rounds depend on all earlier rounds finishing.
- Mark the critical-path slug(s) with `*` and name why in a trailing legend line if it isn't obvious (e.g. `* longest chain — blocks release`).
- Adding, finishing, or deleting a `todo/{topic-slug}.md` updates `todo/index.md` in the same change — an unlisted slice is treated as not scheduled.
- Delete a slug's line once its file is deleted; delete `todo/index.md` itself once `todo/` is empty.
