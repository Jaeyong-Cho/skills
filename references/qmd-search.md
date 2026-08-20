# Searching `~/wiki` with qmd

How to find candidate documents — in the personal `~/wiki` or a project's own `~/wiki/projects/{slug}/wiki/` — before reading them. This is the discovery step; once you have a candidate file, `document-style/frontmatter.md` governs reading it (header/frontmatter before body).

1. **Search with `qmd query`** — the primary path if a `qmd` collection exists for what you're looking for. Start with `qmd query "<question>" -c kb` to search synthesized knowledge first, then `qmd query -c journal -c roadmap -c today` if that misses. For a project's own wiki, search `-c {project-slug}`. Returns candidates with snippets and context tags — read those before opening the full file. For query syntax (`intent:`/`lex:`/`vec:`/`hyde:`), see the installed `qmd` skill (`qmd skill show`, or `~/.claude/skills/qmd/SKILL.md` once installed).
2. **If `qmd` returns nothing** (not yet embedded, or no collection set up for this project) — fall back to the `index.md` chain-walk:
   - Walk the `index.md` chain down from the relevant document root (`journal/`, `roadmap/`, or `spec/`) toward the likely date/project/EPIC — each `index.md` narrows which subdirectory to enter next. For source code, use the repository's package/module path and any local index.
   - Once in a candidate directory, read each candidate's frontmatter/header first (`document-style/frontmatter.md`) before its body — resolve from metadata alone whenever it can.

Every skill that reads or searches `~/wiki`/`spec/` (`/explore`, `/recon`, `kb-ingest`, `project-wiki`, ...) points here instead of restating this procedure inline — inlining it is how `/explore` drifted out of sync with `qmd` in the first place.

## Keeping it fresh

`qmd update` re-scans every registered collection for new/changed/removed files (lexical/BM25 index only); `qmd embed` computes vectors for whatever `update` queued as pending. Neither alone is enough — `update` doesn't compute vectors, `embed` doesn't discover new files. `skills/kb-ingest/scripts/qmd_sync.sh` runs both in sequence and is the one place this logic lives; every trigger point (`kb-ingest`, `project-wiki`, `/do-plan`, `install.sh`) calls it instead of re-typing the two commands.
