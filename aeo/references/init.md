# AEO Book Initialization

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

This creates `.aeo/theme/`. Open `.aeo/theme/css/variables.css` and add `--content-max-width` at the top of the `:root` block:

```css
:root {
    --content-max-width: 80%;
}
```

Leave all other variables intact.

## Step 4: Configure book.toml

Replace `.aeo/book.toml` with:

```toml
[book]
language = "en"
src = "src"
title = "AEO"

[preprocessor.mermaid]
command = "mdbook-mermaid"

[output.html]
additional-js = ["mermaid.min.js", "mermaid-init.js"]
additional-css = ["theme/css/variables.css"]
```

## Step 5: Create chapter directories and SUMMARY.md

```bash
mkdir -p .aeo/src/design .aeo/src/reviews .aeo/src/refact .aeo/src/impl .aeo/src/docs
```

Write `.aeo/src/SUMMARY.md`:

```markdown
# Summary

- [Design](./design/index.md)
- [Code Reviews](./reviews/index.md)
- [Refactoring Plans](./refact/index.md)
- [Implementation Plans](./impl/index.md)
- [Documentation](./docs/index.md)
```

Create an `index.md` stub in each chapter directory with content `# <Chapter Name>\n\n_No entries yet._`

## Step 6: Build check

```bash
cd .aeo && mdbook build 2>&1
```

Fix all errors before continuing.

## Step 7: Copy serve script

```bash
cp <skill-path>/scripts/serve.sh .aeo/serve.sh
chmod +x .aeo/serve.sh
```

Replace `<skill-path>` with the path to the aeo skill directory. Tell the user they can start the book server anytime with:

```bash
.aeo/serve.sh
```

Then return to the main task.
