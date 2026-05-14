---
name: pf-docs-migrate
description: |
  One-time migration of VAO documentation from the old feature-centric format (numbered chapter directories, each with 01-value.md / 02-aspect.md / 03-object.md) to the new layer-centric format (value/, aspect/, object/ top-level directories, one file per component inside each).
  Triggers: "pf-docs-migrate", "migrate docs", "update docs format", "convert docs structure", or when old-format docs are detected.
---

Read `../pf/references/caveman.md` and apply caveman style throughout — including in all output documents.

# VAO Docs Migration

Converts `.pf/src/docs/` from feature-centric chapters to layer-centric chapters. Run once per project.

## Step 1: Detect old-format docs

```bash
find .pf/src/docs -mindepth 2 -name "01-value.md" 2>/dev/null
```

If nothing is found, tell the user their docs are already in the new format and stop.

---

## Step 2: Read all old content

For each old chapter directory found (e.g. `docs/01-auth/`, `docs/02-checkout/`):

1. Record the component slug — strip the leading number prefix from the directory name (e.g. `01-auth` → `auth`)
2. Assign a number for the new files based on order (first chapter = `01`, second = `02`, etc.)
3. Read all three section files: `01-value.md`, `02-aspect.md`, `03-object.md`

---

## Step 3: Write new layer files

Create the layer directories if they don't exist:

```bash
mkdir -p .pf/src/docs/value .pf/src/docs/aspect .pf/src/docs/object
```

For each component, write its content into the corresponding layer file:
- Old `01-auth/01-value.md` → new `value/01-auth.md`
- Old `01-auth/02-aspect.md` → new `aspect/01-auth.md`
- Old `01-auth/03-object.md` → new `object/01-auth.md`

Preserve all content verbatim — do not rewrite or summarize.

---

## Step 4: Delete old chapter directories

```bash
rm -rf .pf/src/docs/<old-chapter-dir>
```

Delete only the old numbered chapter directories. Do not touch `docs/index.md` yet.

---

## Step 5: Rewrite docs/index.md and layer index files

Replace `docs/index.md` with:

```markdown
# Documentation

This manual documents the current system design using the VAO framework.

## Chapters

- [Value — Why](./value/index.md)
- [Aspect — How](./aspect/index.md)
- [Object — What](./object/index.md)
```

Write (or overwrite) each layer's `index.md` listing the migrated components:

```markdown
# Value

The user goals and outcomes the system exists to deliver.

## Components

- [Auth](./01-auth.md)
- [Checkout](./02-checkout.md)
```

(Same pattern for `aspect/index.md` and `object/index.md`.)

---

## Step 6: Rewrite SUMMARY.md docs entries

Replace the old docs section in `.pf/src/SUMMARY.md` with:

```markdown
- [Documentation](./docs/index.md)
  - [Value](./docs/value/index.md)
    - [Auth](./docs/value/01-auth.md)
  - [Aspect](./docs/aspect/index.md)
    - [Auth](./docs/aspect/01-auth.md)
  - [Object](./docs/object/index.md)
    - [Auth](./docs/object/01-auth.md)
```

Add one entry per component under each layer.

---

## Step 7: Build check

```bash
cd .pf && mdbook build 2>&1
```

Fix all errors before reporting to the user.

---

## Step 8: Done

Show the user a summary of what was migrated. Suggest a commit message using `../pf/references/commit.md`.
