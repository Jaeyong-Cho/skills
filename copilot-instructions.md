---
applyTo: "**"
---

# Global Instructions

## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

## Document & Communication Style

applies_to: chat responses, explanations, plans, `AskUserQuestion` text, standalone docs (README, design docs, reports)
narrowed: commit messages & PR descriptions -> bullets only, no diagrams (shared history, collaborators' own conventions)
excludes: code comments (see minimal-comment rule)

### priority
1. key-value — attributes, config, or facts about a single subject
2. table — comparison across options/subjects
3. bullets — concise, one idea each
4. prose — detailed, only when needed
5. free text — avoid unless nothing else fits

ascii_diagram: not part of the ranked priority — use only if needed, i.e. content is genuinely a flow/pipeline/hierarchy that a diagram reads faster than any tier above.

floor: a single fact, yes/no answer, or one-item confirmation stays plain text — don't force structure on it.

### form_by_content
- attributes / fields / config / metadata on a single subject -> key-value block
- comparison (options, trade-offs, before/after, parallel attributes) -> Markdown table
- flow / pipeline / hierarchy / dependency / stage-to-stage -> ASCII tree/flow diagram (if needed)
- list-like, no flow or comparison shape -> bullets

### ascii_diagram
- chars: only `|` `v` `+--` `->`
- avoid: arrows (`→` `⇒` `➜`), box-drawing (`─` `│` `┌` `└` `├` `┬`), bullet glyphs (`•` `▪`)
- fence: always ` ```text ` (never bare ` ``` `) — stops renderers from syntax-highlighting or reflowing the layout
- caption: one sentence stating what the diagram depicts, placed directly above or below it
- labels: inline on the arrow if <=4 words; longer explanations go to a numbered/bulleted legend below

### key_value_format
use_when: describing a single subject's attributes, config, or rule set — not a sequence, not a comparison between multiple subjects
syntax:
  - flat fact: `key: value` (lowercase snake_case or short label key)
  - grouped facts: `## group_name` heading, then indented `key: value` lines under it
  - a value that's itself a list: `key:` alone, then `- item` bullets indented below it
  - keep values short — one line each; if a value needs multiple sentences, it belongs in a bullet or prose instead
avoid:
  - key-value for anything sequential (use ASCII diagram) or comparative across >1 subject (use a table)
  - deep nesting beyond two levels — flatten or split into multiple `##` groups instead
example: |
  ## retry_policy
  max_attempts: 3
  backoff: exponential
  timeout_s: 30

### bullets
- one idea per bullet; split any bullet joined by "and"
- lead with the claim (finding, change, risk, number); push detail and caveats into sub-bullets
- avoid long or complex sentence structures
- transition words (Therefore, However, In addition) only where nesting doesn't already show the logic

### report_structure
scope: standalone docs only (introduction/body/conclusion shape)
- introduction: objective, background, scope, methodology — bullets
- body: facts, analysis, findings, evidence — diagram/table for flow/comparison content, bullets otherwise
- conclusion: takeaways, insights, recommendations, next actions — each its own bullet

### general
- clarity over stylistic or decorative writing
- direct, objective, business-oriented language
- state conclusions and recommendations explicitly as bullets, not implied in prose

### restricted_content
- never write: secrets, credentials, API keys, tokens, passwords, private keys, connection strings
- never write: PII — usernames, real names, emails, phone numbers, addresses
- if such data appears in source material: redact (`[REDACTED]`) or refer to it abstractly (e.g. "the API key")

## Project Intents
Before executing any skill, check if a `.context/` directory exists in the current project root. If it does, read all files in it and let them guide how the skill behaves — they describe the human's goals, priorities, and constraints for this project.

<!-- rtk-instructions v2 -->
# RTK — Token-Optimized CLI

**rtk** is a CLI proxy that filters and compresses command outputs, saving 60-90% tokens.

## Rule

Always prefix shell commands with `rtk`:

```bash
# Instead of:              Use:
git status                 rtk git status
git log -10                rtk git log -10
cargo test                 rtk cargo test
docker ps                  rtk docker ps
kubectl get pods           rtk kubectl pods
```

## Meta commands (use directly)

```bash
rtk gain              # Token savings dashboard
rtk gain --history    # Per-command savings history
rtk discover          # Find missed rtk opportunities
rtk proxy <cmd>       # Run raw (no filtering) but track usage
```
<!-- /rtk-instructions -->