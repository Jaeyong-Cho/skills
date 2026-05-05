# AEO Book Initialization

Run this only when `.aeo/book.toml` does not exist.

## Step 1: Install tooling if needed

```bash
which mdbook || cargo install mdbook
which mdbook-mermaid || cargo install mdbook-mermaid
```

If `cargo` is not available, tell the user to install Rust first: https://www.rust-lang.org/tools/install

## Step 2: Initialize and configure

```bash
mdbook init .aeo --title "AEO" --ignore git
mdbook-mermaid install .aeo/
```

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
```

## Step 3: Create chapter directories and SUMMARY.md

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

## Step 4: Build check

```bash
cd .aeo && mdbook build 2>&1
```

Fix all errors, then return to the main task.
