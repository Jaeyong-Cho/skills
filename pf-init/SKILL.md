---
name: pf-init
description: |
  Initialize the AEO book (.aeo/) in the current project. Creates the mdbook structure, theme, chapters (adr, poc, docs), and serve script.
  Triggers: "pf-init", "initialize pf", "set up pf book", "create pf book", or when any pf skill detects .aeo/book.toml does not exist.
---

> Use `/caveman` for compressed output during this session.

# AEO Initialization

## Step 1: Install tooling if needed

```bash
which mdbook || cargo install mdbook
which mdbook-mermaid || cargo install mdbook-mermaid
```

If `cargo` is not available, tell the user to install Rust first: https://www.rust-lang.org/tools/install

## Step 2: Initialize mdbook

```bash
mdbook init .aeo --title "AEO" --ignore git
mdbook-mermaid install .aeo/
```

## Step 3: Generate theme and set content width

```bash
cd .aeo && mdbook init --theme
```

Replace the existing `--content-max-width` in `.aeo/theme/css/variables.css` — do not add a new line:

```bash
sed -i '' 's/--content-max-width:[^;]*/--content-max-width: 80%/' .aeo/theme/css/variables.css
```

## Step 4: Configure book.toml

Replace `.aeo/book.toml` with:

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
mkdir -p .aeo/src/adr .aeo/src/poc .aeo/src/docs/value .aeo/src/docs/aspect .aeo/src/docs/object
```

Find the pf-init skill directory (typically `~/.claude/skills/pf-init/`) and copy:

```bash
cp <skill-path>/templates/SUMMARY.md .aeo/src/SUMMARY.md
cp <skill-path>/templates/adr-index.md .aeo/src/adr/index.md
cp <skill-path>/templates/poc-index.md .aeo/src/poc/index.md
cp <skill-path>/templates/docs-index.md .aeo/src/docs/index.md
cp <skill-path>/templates/docs-value-index.md .aeo/src/docs/value/index.md
cp <skill-path>/templates/docs-aspect-index.md .aeo/src/docs/aspect/index.md
cp <skill-path>/templates/docs-object-index.md .aeo/src/docs/object/index.md
```

## Step 6: Build check

```bash
cd .aeo && mdbook build 2>&1
```

Fix all errors before continuing.

## Step 7: Copy serve script

Find the pf skill directory (where this skill lives, typically `~/.claude/skills/pf/`) and copy:

```bash
cp <skill-path>/scripts/serve.sh .aeo/serve.sh
chmod +x .aeo/serve.sh
```

Tell the user they can start the book server anytime with:

```bash
.aeo/serve.sh
```

Then return to the task that triggered initialization.

