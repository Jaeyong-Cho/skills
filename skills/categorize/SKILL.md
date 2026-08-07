---
name: categorize
description: Sort a directory's loose files into topic sub-directories with an index.md table of contents. Invoke as /categorize.
disable-model-invocation: true
---

# Categorize

Turn a directory of loose files into topic sub-directories plus an `index.md` table of contents, instead of leaving everything flat.

1. **Ask for the target directory** — ask the user for the directory path. Do not assume one. Completion criterion: user has given a concrete, existing directory path.
2. **Inventory the loose files** — list every file sitting directly in that directory (skip files already inside a subdirectory; those are left alone). Read enough of each — name and content — to state its topic in one line. Completion criterion: every loose file has a one-line topic.
3. **Choose MECE categories** — group the files so the categories are Mutually Exclusive (each file fits exactly one) and Collectively Exhaustive (every file lands somewhere). Name each category a short kebab-case slug. A catch-all for genuine outliers is fine, capped at one such category — a category holding a single file that's really just that file's name restated is not a category, merge it back in. Completion criterion: every loose file is assigned to exactly one category slug.
4. **Move files into place** — for each category, `mkdir -p {dir}/{category}/`, then move every assigned file into it (`git mv` if `{dir}` is inside a git repo, so history follows the file; plain `mv` otherwise). Completion criterion: the directory's top level holds only category sub-directories (plus `index.md` once step 5 runs) — no loose files remain.
5. **Write index.md** — build `{dir}/index.md`: a `# {directory name}` heading, then one sub-heading per category with each moved file listed under it as a link to its new path (`./{category}/{file}`). Completion criterion: `index.md` exists, every category from step 3 is a heading, and every moved file appears once as a link under its category.

Tell the user the directory path and the category breakdown when done.
