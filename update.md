# Update: Communication Style Response Preference

## Introduction
- **Objective:** make AI responses (Claude Code, and where possible other tools) default to structured, diagram/table representations instead of prose, because reading unstructured AI output is time-consuming.
- **Background:** the user requested this via `/grilling`, providing two ASCII flow-diagram examples as the target style and a stated priority order: structured format (highest) → concise bullets → detailed description → free text (lowest).
- **Scope:** where this preference should live (global config vs on-demand skill), what content qualifies for diagrams vs tables vs bullets, and how far the rule should extend (chat, docs, commit messages, PR descriptions, other AI tools).
- **Methodology:** a full `/grilling` interview — one question at a time, discrete options via `AskUserQuestion`, each answer resolved before moving to the next branch — followed by implementation and two rounds of scope narrowing/extension driven by follow-up user questions.

## Body

### Decision flow
```
User request: prefer structured AI responses
    |
    v
/grilling interview
    |
    +-- Mechanism      -> global CLAUDE.md (not skill, not output-style)
    +-- Scope           -> broad: docs, questions, responses, descriptions
    +-- Notation        -> ASCII flow/tree diagrams (plain ASCII only)
    +-- Non-flow content -> Markdown tables
    +-- Annotation      -> inline for short labels, legend for long
    +-- Placement       -> one-line conclusion, then structured block
    +-- Trivial floor   -> skip structure for single-fact/confirmation answers
    |
    v
Implementation (round 1)
    |
    +-- skills/references/communication-style.md   (new, full rule)
    +-- skills/CLAUDE.md                          (+ @references/communication-style.md)
    +-- memory/feedback_structured_format.md      (new, why + how)
    |
    v
User question: "Is it ok to add in the global instruction?"
    |
    v
Risk discussion -> commit messages/PRs visible to collaborators
    who didn't opt in; teams have their own commit conventions
    |
    v
Scope narrowed + extended
    |
    +-- communication-style.md: commit/PR -> bullets only, no diagrams
    +-- skills/.github/copilot-instructions.md (new): self-contained
    |     mirror (Communication Rule + communication style rule),
    |     since Copilot instructions don't support @-include
    |
    v
Commit 77bb75a, pushed to origin/main
    |
    v
User: "I want to make document style follow structured format"
    |
    v
Clarified target: req/archi/to-docs skill family, via their
shared references/document-style.md
    |
    v
document-style.md updated: same priority-tier structure layered
on top of its existing bullet-only rules
    |
    v
Commit f48085f, pushed to origin/main
```

### Files changed
| File | Change |
|------|--------|
| `skills/references/communication-style.md` | New — full rule: priority tiers, ASCII-diagram notation, table use, annotation placement, trivial-answer floor, scope |
| `skills/CLAUDE.md` | Added `@references/communication-style.md` include under Communication Rule |
| `skills/.github/copilot-instructions.md` | New — self-contained mirror (Communication Rule + communication style rule) for GitHub's repo-scoped Copilot instructions |
| `skills/references/document-style.md` | Added the same priority-tier structure (structured > bullets > prose > free text) on top of its existing bullet-only guidance; used by `req`, `archi`, `to-docs`, `merge-req`, `merge-archi`, `fs-plan`, `co-plan`, `to-todo`, `create-agent` |
| `memory/feedback_structured_format.md` | New — records the preference and rationale for future sessions |

### Key decisions and rationale
- **Global CLAUDE.md over a skill or output-style:** the user wants this applied to *all* responses without remembering to invoke anything, which only an always-on global rule satisfies.
- **Reference file + `@include`, not inline in CLAUDE.md:** keeps `CLAUDE.md` short; matches the existing `@RTK.md` pattern already in the file.
- **Plain ASCII only, no Unicode box-drawing/arrows:** guarantees correct rendering in every terminal and font.
- **Commit/PR narrowed to bullets-only:** shared git history and PRs are read by collaborators who never opted into this style, and many teams already have their own commit-message conventions (Conventional Commits, Jira-linked formats) that diagrams would clash with.
- **`document-style.md` extended rather than duplicated:** it's the single shared style guide already referenced by nine different skills producing human-facing documents (RDRs, ADRs, plans), so one edit propagates the preference across all of them.

### Finding: incorrect assumption about Copilot's global config
- While researching this `/to-docs` write-up, found a **pre-existing** `skills/copilot-instructions.md` (root level, last modified 2026-07-18, unrelated to this session) that `install.sh`'s `setup_copilot()` symlinks to `~/.copilot/copilot-instructions.md` for the Copilot CLI.
- This *is* the real global-equivalent to `~/.claude/CLAUDE.md` for Copilot — contradicting what was told to the user earlier in the session ("no global equivalent exists for Copilot the way `~/.claude/CLAUDE.md` works for Claude Code").
- The `.github/copilot-instructions.md` created this session serves a different, narrower purpose: GitHub's own repo-scoped Copilot instructions (IDE/PR web context), not the Copilot CLI.
- Net effect: the root `skills/copilot-instructions.md` — the file actually wired into the Copilot CLI — does **not** yet contain the communication style rule.

## Conclusion
- **Key takeaway:** the communication style preference is fully wired for Claude Code (global, via `CLAUDE.md`) and for document-producing skills (via `document-style.md`), both committed and pushed (`77bb75a`, `f48085f`).
- **Gap:** the Copilot CLI's actual global instructions file (`skills/copilot-instructions.md`, root level) is stale — it predates and doesn't include the communication style rule. The `.github/copilot-instructions.md` added this session covers a different Copilot surface (GitHub web/IDE), not the CLI.
- **Recommended next action:** decide whether to fold the communication style rule into `skills/copilot-instructions.md` (the CLI-facing file) as well, and clarify whether the newly created `.github/copilot-instructions.md` should stay as-is or be reconciled with it.
- **Also pending, unrelated to this task:** 8 pre-existing modified files in the repo (`README.md`, `auto-action/SKILL.md`, `co-plan/SKILL.md`, `fs-plan/SKILL.md`, `merge-archi/SKILL.md`, `merge-req/SKILL.md`, `template/plan.md`, `template/self-plan.md`) remain uncommitted from before this session and were left untouched.
