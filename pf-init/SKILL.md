---
name: pf-init
description: |
  Initialize the VAO book (.pf/) in the current project. Creates the mdbook structure, theme, chapters (adr, poc, docs), and serve script.
  Triggers: "pf-init", "initialize pf", "set up pf book", "create pf book", or when any pf skill detects .pf/book.toml does not exist.
---

Read `../pf/references/caveman.md` and apply caveman style throughout — including in all output documents.

# VAO Initialization

## Step 1: Install tooling if needed

```bash
which mdbook || cargo install mdbook
which mdbook-mermaid || cargo install mdbook-mermaid
```

If `cargo` not available, tell user to install Rust first: https://www.rust-lang.org/tools/install

## Step 2: Initialize mdbook

```bash
mdbook init .pf --title "VAO" --ignore git
mdbook-mermaid install .pf/
```

## Step 3: Generate theme and set content width

```bash
cd .pf && mdbook init --theme
```

Replace existing `--content-max-width` in `.pf/theme/css/variables.css` — do not add new line:

```bash
sed -i '' 's/--content-max-width:[^;]*/--content-max-width: 80%/' .pf/theme/css/variables.css
```

## Step 4: Configure book.toml

Replace `.pf/book.toml` with:

```toml
[book]
language = "en"
src = "src"
title = "PROJECT_NAME"

[preprocessor.mermaid]
command = "mdbook-mermaid"

[output.html]
additional-js = ["mermaid.min.js", "mermaid-init.js"]
additional-css = ["theme/css/variables.css"]
```

## Step 5: Create chapter directories and copy templates

```bash
mkdir -p .pf/src/adr .pf/src/poc .pf/src/docs/value .pf/src/docs/aspect .pf/src/docs/object
```

Find pf-init skill directory (typically `~/.claude/skills/pf-init/`) and copy:

```bash
cp <skill-path>/templates/SUMMARY.md .pf/src/SUMMARY.md
cp <skill-path>/templates/adr-index.md .pf/src/adr/index.md
cp <skill-path>/templates/poc-index.md .pf/src/poc/index.md
cp <skill-path>/templates/docs-index.md .pf/src/docs/index.md
cp <skill-path>/templates/docs-value-index.md .pf/src/docs/value/index.md
cp <skill-path>/templates/docs-aspect-index.md .pf/src/docs/aspect/index.md
cp <skill-path>/templates/docs-object-index.md .pf/src/docs/object/index.md
```

## Step 6: Build check

```bash
cd .pf && mdbook build 2>&1
```

Fix all errors before continuing.

## Step 7: Copy serve script

Find pf skill directory (where this skill lives, typically `~/.claude/skills/pf/`) and copy:

```bash
cp <skill-path>/scripts/serve.sh .pf/serve.sh
chmod +x .pf/serve.sh
```

Tell user they can start book server anytime with:

```bash
.pf/serve.sh
```

Then return to task that triggered initialization.
