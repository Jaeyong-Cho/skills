---
name: docs-init
description: Initialize an mdBook API docs project with mdbook-mermaid, catppuccin theme, and kanagawa theme. Use when user wants to set up a new API docs book, mentions "docs-init", "init api docs", or "set up mdbook".
---

# API Init

Set up a new mdBook project for API docs with mermaid diagrams and kanagawa/catppuccin themes.

## Prerequisites check

Verify these are installed before running; if missing, tell the user:
- `mdbook` — `cargo install mdbook`
- `mdbook-mermaid` — `cargo install mdbook-mermaid`
- `curl` and `python3` — standard on macOS/Linux

## Step 1: Confirm project title

Default is the current directory name (`basename "$PWD"`). Confirm with the user.

## Step 2: Run the init script

```bash
~/.claude/skills/docs-init/init.sh <title>
```

`<title>` is the book title only — the directory is always `docs/`.

This script:
1. Runs `mdbook init docs --title <title>` — creates book structure
2. Runs `mdbook-mermaid install docs` — adds preprocessor to book.toml
3. Downloads `catppuccin.css` from the latest catppuccin/mdBook GitHub release into `docs/theme/`
4. Copies `kanagawa.css` from this skill's directory to `docs/theme/`
5. Copies `serve.sh` from this skill's directory to `docs/`
6. Downloads catppuccin's `index.hbs` (adds latte/frappe/macchiato/mocha theme buttons)
7. Patches `index.hbs` to add a **Kanagawa** button after Mocha
8. Appends `[output.html]` to `book.toml` with both CSS files and kanagawa as default theme

## Step 3: Done

Tell the user:
```
cd docs && ./serve.sh
```
