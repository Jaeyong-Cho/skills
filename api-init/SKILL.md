---
name: api-init
description: Initialize an mdBook API docs project with mdbook-mermaid, catppuccin theme, and kanagawa theme. Use when user wants to set up a new API docs book, mentions "api-init", "init api docs", or "set up mdbook".
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
~/.claude/skills/api-init/init.sh <title>
```

This script:
1. Runs `mdbook init <title>` — creates book structure
2. Runs `mdbook-mermaid install <title>` — adds preprocessor to book.toml
3. Downloads `catppuccin.css` from the latest catppuccin/mdBook GitHub release
4. Copies `kanagawa.css` from this skill's directory to `<title>/theme/`
5. Downloads catppuccin's `index.hbs` (adds latte/frappe/macchiato/mocha theme buttons)
6. Patches `index.hbs` to add a **Kanagawa** button after Mocha
7. Appends `[output.html]` to `book.toml` with both CSS files and kanagawa as default theme

## Step 3: Done

Tell the user:
```
cd <title> && mdbook serve
```
