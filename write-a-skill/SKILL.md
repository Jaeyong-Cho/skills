---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill.
---

Read `../caveman/SKILL.md` and apply caveman style throughout.

# Write a Skill

## Step 1: Grill

Ask:
- What task/domain?
- Specific use cases?
- Need scripts or just instructions?
- Reference materials?

## Step 2: Draft

Create:
- `SKILL.md` — main instructions
- Extra reference files if content > 100 lines
- Utility scripts for deterministic ops (validation, formatting)

## Step 3: Review

Show draft. Ask: missing anything? Too much? Adjust.

---

## Structure

```
skill-name/
  SKILL.md          ← required
  REFERENCE.md      ← if detail is deep
  scripts/          ← if deterministic ops repeat
```

## SKILL.md template

```md
---
name: skill-name
description: What it does. Use when [specific triggers].
---

# Skill Name

[Steps here]
```

## Description rules

Only thing agent sees when choosing skill. Max 1024 chars.

- First sentence: what it does
- Second sentence: "Use when [triggers]"

Good: `Extract text and tables from PDFs. Use when user mentions PDFs, forms, or document extraction.`
Bad: `Helps with documents.`

## Checklist

- [ ] Description has "Use when..."
- [ ] SKILL.md under 100 lines
- [ ] No time-sensitive info
- [ ] Triggers cover real user phrases
