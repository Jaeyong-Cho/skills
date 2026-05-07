---
name: aeo-init
description: |
  Initialize the AEO book (.aeo/) in the current project. Creates the mdbook structure, theme, chapters (adr, poc, docs), and serve script.
  Triggers: "aeo-init", "initialize aeo", "set up aeo book", "create aeo book", or when any aeo skill detects .aeo/book.toml does not exist.
---

# AEO Initialization

Run this only when `.aeo/book.toml` does not exist.

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

Replace `PROJECT_NAME` with the actual project name.

## Step 5: Create chapter directories and SUMMARY.md

```bash
mkdir -p .aeo/src/adr .aeo/src/poc .aeo/src/docs
```

Write `.aeo/src/SUMMARY.md`:

```markdown
# Summary

- [ADR](./adr/index.md)
- [PoC](./poc/index.md)
- [Documentation](./docs/index.md)
```

Create an `index.md` stub in each directory with content `# <Chapter Name>\n\n_No entries yet._`

## Step 6: Build check

```bash
cd .aeo && mdbook build 2>&1
```

Fix all errors before continuing.

## Step 7: Copy serve script

Find the aeo skill directory (where this skill lives, typically `~/.claude/skills/aeo/`) and copy:

```bash
cp <skill-path>/scripts/serve.sh .aeo/serve.sh
chmod +x .aeo/serve.sh
```

Tell the user they can start the book server anytime with:

```bash
.aeo/serve.sh
```

Then return to the task that triggered initialization.
