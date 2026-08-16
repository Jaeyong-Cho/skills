# Todo Document Convention

A target project's implementation todos live under `todo/**/*.md`, one file per vertical slice — a complete, independently-shippable unit (e.g. one sub-topic from a spec), never a horizontal layer (e.g. not "backend" + "frontend" for one feature).

- One file per slice: `todo/{topic-slug}.md`, matching the spec sub-topic it implements.
- Each file is a checklist: `- [ ] {action item}`, ordered so the slice can be built end-to-end top to bottom.
- The file's first line links back to its spec: `Spec: spec/{topic-slug}.md#{sub-topic}` — the todo lists *how*, the spec already said *what*; don't restate AC or requirements here.
- `todo/index.md` is the table of contents: one heading per top-level area, every todo file listed underneath as a link to its path.
- If `todo/` doesn't exist yet in the target project, create it and note that in the plan/report.
- Adding or updating a todo file always updates `todo/index.md` in the same change — an unlisted todo file is treated as not done.
