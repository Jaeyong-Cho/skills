# Flag System

Flags are HTML comments embedded in book markdown files. They are the communication channel between human and AI. **The book is never silently modified** — every AI change is flagged and waits for human review.

## Flag Reference

| Flag | Who places it | Meaning |
|------|--------------|---------|
| `DRAFT` | AI only | AI wrote or revised this section; awaiting human review |
| `IMPLEMENT` | Human only | Design is approved; code must be written |
| `FIX` | AI or Human | Something is wrong here; needs correction |

**Rule: Only humans remove or promote flags. AI places flags; humans resolve them.**

## Flag Syntax

Always include a description — never a bare flag.

```markdown
<!-- DRAFT: rewrote token expiry section based on new 24h requirement -->

<!-- IMPLEMENT: UserService.refreshToken() — refresh token within 1h of expiry, return new JWT -->

<!-- FIX: book says tokens are stateless but AuthService.logout() maintains a denylist — reconcile -->
```

## Promotion Path

```
Human writes intent or bug report
        ↓
AI drafts/revises book → places [DRAFT] → human reviews
                                               ↓
                                  approved → human promotes to [IMPLEMENT] or removes flag
                                  needs change → human edits inline → AI revises → new [DRAFT]
                                               ↓
                             [IMPLEMENT] → AI writes code (lb-implement) → flag removed
```

## Scanning for Flags

```bash
# All flags
grep -rn "<!-- DRAFT:\|<!-- IMPLEMENT:\|<!-- FIX:" book/src/

# By type
grep -rn "<!-- IMPLEMENT:" book/src/
grep -rn "<!-- DRAFT:" book/src/
grep -rn "<!-- FIX:" book/src/
```
