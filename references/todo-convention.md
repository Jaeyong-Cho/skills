# Todo Document Convention

WBS terms: **EPIC** = a spec topic (`spec/{topic-slug}.md`) — a business-level requirement, a set of related stories. **STORY** = a spec sub-topic — done means the user gets one specific value or feature. **TASK** = one `todo/{task-slug}.md` file — work to build or support a story; a story may need one or more tasks.

A target project's task todos live under `todo/**/*.md`, one file per task, never a horizontal layer (e.g. not "backend" + "frontend" for one story).

Each task file is temp scratch, not a persisted document like `spec/`: no per-file ceremony beyond the link and checklist. Format:

```
Spec: spec/{topic-slug}.md#{sub-topic}

- [ ] {action item}
- [ ] {action item}
```

- One file per task: `todo/{task-slug}.md`.
- First line links back to the story's spec sub-topic — the task lists *how*, the spec already said *what*; don't restate AC or requirements here.
- Checklist ordered so the task completes end-to-end top to bottom.
- Delete the file once every item is checked — it's disposable, the spec is the record that lasts.

## `todo/index.md` — the EPIC / STORY / TASK WBS guide

`todo/index.md` is the work-breakdown-structure: every EPIC's stories, each story's tasks, and task ordering. Format:

```
# EPIC: {topic-slug}

## STORY: {story-slug} — spec/{topic-slug}.md#{sub-topic}
Round 1: {task-slug-a}, {task-slug-b}
Round 2: {task-slug-c}*
```

- One `# EPIC` heading per spec topic, one `## STORY` heading per sub-topic underneath it.
- Under each story, one line per round of its tasks; a round's tasks can run in parallel, later rounds depend on all earlier rounds finishing.
- Mark the critical-path task(s) with `*` and name why in a trailing legend line if it isn't obvious.
- Adding, finishing, or deleting a `todo/{task-slug}.md` updates `todo/index.md` in the same change — an unlisted task is treated as not scheduled.
- Delete a task's line once its file is deleted; delete the STORY heading once no tasks remain; delete `todo/index.md` itself once `todo/` is empty.
