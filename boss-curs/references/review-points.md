# Review Points

After AI drafts or updates items, it must provide **review points** — explicit questions or checks the human must resolve before promoting state from `draft` to `reviewed`.

---

## Format

Review points are placed in two locations:

### 1. Inline `> Review needed` callout (per item)

At the end of the item body, a rendered blockquote with the specific question for that item:

```markdown
> **Review needed** — verify lockout threshold (5 attempts) and whether unlock is automatic (time-based) or manual (admin action)
```

For multiple questions on one item:

```markdown
> **Review needed**
> - Is the lockout threshold 5 attempts or configurable per deployment?
> - Should the error message distinguish "wrong password" from "user not found"?
```

This blockquote is **visible in the rendered book** — the human sees it when reading the page.
When the human has resolved the question, they delete the blockquote before asking AI to promote the item to `reviewed`.

### 2. End-of-session review summary

After completing all updates, AI reports a consolidated review summary:

```
## Review Points

### Must Resolve (blocks downstream work)
- [ ] SRS-007: Is account lockout automatic (time-based) or manual (admin action)?
- [ ] SAD-002: Does the auth service own the session store, or does it delegate to a cache layer?

### Should Verify (content correctness)
- [ ] SRS-003: Confirm that 2FA is out of scope for this release.
- [ ] SDD-009: Check that the bcrypt cost factor (12) matches your production security policy.

### For Awareness (no action needed unless you disagree)
- [ ] SRS-001 → SAD-001 trace added. Review that the mapping is correct.
- [ ] New tag #lockout created. Confirm this is distinct from #security.
```

---

## Review Point Categories

| Category | Meaning |
|----------|---------|
| **Must Resolve** | Ambiguity that will cause downstream items to be wrong if not resolved. Do not proceed until answered. |
| **Should Verify** | AI made an assumption. Human should confirm it is correct. |
| **For Awareness** | Informational. AI is confident but wants a human eye on it. |

---

## Review Checklist per Document Layer

When reviewing SRS items, check:
- [ ] Is the requirement testable? (Can AT be written for it?)
- [ ] Is the requirement in scope for this release?
- [ ] Are conflicting requirements identified?

When reviewing SAD items, check:
- [ ] Does the architecture satisfy all `reviewed` SRS items?
- [ ] Are component boundaries clear (one responsibility per component)?
- [ ] Are directory and file names final? (These are what the human will create)
- [ ] Are external dependencies justified?

When reviewing SDD items, check:
- [ ] Is every function signature unambiguous? (Name, parameters, return type)
- [ ] Is the algorithm described in enough detail to implement without guessing?
- [ ] Are variable names and types specified?
- [ ] Is error handling specified?

When reviewing test items (AT / SIT / UT), check:
- [ ] Does each test trace to exactly one upstream item?
- [ ] Is the pass/fail criterion objective and measurable?
- [ ] Are edge cases and failure paths covered?
