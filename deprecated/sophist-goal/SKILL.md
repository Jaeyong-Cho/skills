---
name: sophist-goal
description: |
  Set or update the project goal in a SOPHIST book. Triggers: "sophist-goal", "set the goal", "update the goal", "what's the project goal", "change the project goal", "define the goal", "write the goal", or any time the user wants to record what the project is for.
  Works for both new and existing projects — creates goal.md if missing, updates it if it already exists, and adds it to SUMMARY.md if needed.
---

# sophist-goal: Set or Update the Project Goal

**Goal**: Capture the user's description of the project's purpose and write it to `.sophist/src/goal.md`. If the file already exists, update it. If SUMMARY.md doesn't include goal.md yet, add it.

Read before starting:
- `../sophist-shared/workflow.md` — pipeline order; the goal is set at the start (after sophist-init) and all other skills read it for orientation

---

## Step 1: Get the goal from the user

If the user has already written a goal in their message, use it directly. If not, ask:

> "What is this project for? You can describe it in any way that feels natural — the purpose, who it's for, what success looks like. A few sentences is fine."

Accept whatever form they give: a sentence, a paragraph, bullet points, a rough sketch.

---

## Step 2: Check whether goal.md already exists

```bash
cat .sophist/src/goal.md 2>/dev/null
```

If it exists, show the current content to the user and confirm whether they want to replace it or append to it. Default to replacing unless the user says otherwise.

---

## Step 3: Write goal.md

Write `.sophist/src/goal.md` with the user's text exactly as they gave it, preceded by a heading:

```markdown
# Project Goal

<user's goal, free-form>
```

Do not reformat or restructure — the goal is the user's own words. If you need to clean up obvious typos, do so, but don't paraphrase or add sections.

---

## Step 4: Add to SUMMARY.md (if not already there)

Check whether SUMMARY.md already references goal.md:

```bash
grep "goal.md" .sophist/src/SUMMARY.md 2>/dev/null
```

If it's missing, add it as the first entry under `# Summary`, before Tags:

```markdown
# Summary

- [Goal](./goal.md)
- [Tags](./tags.md)
...
```

---

## Step 5: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -10
```

Fix any broken links before reporting.

---

## Step 6: Report

Tell the user the goal is saved and that other sophist-* skills will now read it for context. Example:

```
Goal saved to .sophist/src/goal.md.

From now on, sophist-curs, sophist-srs, sophist-sad, and the other skills
will read this file when they start. If something you're working on drifts
from the stated goal, they'll mention it.

You can update the goal any time by running sophist-goal again.
```
