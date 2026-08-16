# Todo Document Convention

A target project's implementation todos live under `todo/**/*.md`, one file per vertical slice — a complete, independently-shippable unit (e.g. one sub-topic from a spec), never a horizontal layer (e.g. not "backend" + "frontend" for one feature).

Todo is temp scratch, not a persisted document like `spec/`: no index, no ceremony. Format only:

```
Spec: spec/{topic-slug}.md#{sub-topic}

- [ ] {action item}
- [ ] {action item}
```

- One file per slice: `todo/{topic-slug}.md`, matching the spec sub-topic it implements.
- First line links back to its spec — the todo lists *how*, the spec already said *what*; don't restate AC or requirements here.
- Checklist ordered so the slice builds end-to-end top to bottom.
- Delete the file once every item is checked — it's disposable, the spec is the record that lasts.
