# Implementation and Refactoring Mode

**Always write the plan document and get confirmation before touching any code.**

**Write simple, readable code. Prefer straightforward constructs over clever or advanced techniques. If a junior developer would have to pause to understand it, simplify it.**

---

## Implementation

Output: `.aeo/src/impl/<ID>-<slug>.md`

### ID assignment

```bash
ls .aeo/src/impl/*.md 2>/dev/null | wc -l
```

Zero-padded 4-digit format: `0001`, `0002`, etc.

### Document structure (ADR format)

Each implementation plan is an Architecture Decision Record. Use this structure:

```markdown
# [ID] Title

**Status:** Proposed | Accepted | Deprecated | Superseded by [ID]

## Context

What feature or requirement is being implemented, and why now?
What existing code or constraints does this touch?

## Decision

What was decided about how to implement this. Walk through the three layers:

**Entity** — Which objects need to be created or used? Are they stable
enough to be shared across multiple aspects? Is the abstraction level right?

**Method** — From what angle are the entities being used? What algorithm
makes the decision? How do the components interact to produce the outcome?

**Value** — What does the end user need from this feature? What does a
good result look like from their perspective? What must the implementation
never do?

## Alternatives Considered

Other approaches evaluated and why they were ruled out.

## Consequences

Trade-offs, risks, and what this decision makes easier or harder.

## Before / After

Show a before/after Mermaid diagram of the layer structure.
If greenfield, show only the target architecture.

```mermaid
graph TD
  ...
```

## Step-by-Step Plan

Ordered tasks. Each step names the file, what it does, and which layer it
belongs to. Use the project's own directory naming — the label in brackets
shows which AEO layer it is.

1. Create `src/models/user.ts` — User entity [entity]
2. Create `src/services/auth.ts` — authentication workflow [method]
3. Create `src/commands/login.ts` — login use-case entry point [value]
4. ...
```

After writing the plan, ask:

> "Here's the implementation plan. Does this look right? I'll write the code once you confirm."

Do not write source code before the user confirms.

### SUMMARY.md entry

```markdown
  - [[<ID>] <title>](./impl/<ID>-<slug>.md)
```

---

## Refactoring

Output: `.aeo/src/refact/<ID>-<slug>.md`

### ID assignment

```bash
ls .aeo/src/refact/*.md 2>/dev/null | wc -l
```

### Deep Module checklist

Before writing the plan, assess the current code against these anti-patterns. Each one is a refactoring target:

| Anti-pattern | What to look for |
|---|---|
| **Shallow module** | Interface nearly as wide as the implementation — many tiny methods, getter/setter heavy |
| **Duplicated logic** | Same algorithm or rule in two or more places — changing it requires touching every copy |
| **Information leakage** | Same knowledge (config key, format, validation rule) scattered across call sites |
| **Temporal decomposition** | Split by execution order rather than responsibility — `ParseX`, `ProcessX`, `OutputX` as separate classes when all exist only to serve X |
| **Pass-through method** | A function whose body is just calling another function with the same arguments |
| **Leaky interface** | Callers must know internal details (ordering, magic values, init sequences) to use the module |
| **Conjoined twins** | Two modules always edited together — should probably be one |

The goal of any refactoring is to make the interface simpler than the implementation, and to reduce how many modules must change when internals change. If the refactoring doesn't move those numbers down, it is not achieving its purpose.

### Document structure (ADR format)

Each refactoring plan is an Architecture Decision Record. Use this structure:

```markdown
# [ID] Title

**Status:** Proposed | Accepted | Deprecated | Superseded by [ID]

## Context

What layer violations exist in the current code? Why do they matter?
What symptom or pain point prompted this refactoring?

Answer:
- Which entity objects are being shaped by a specific aspect? (leakage into method layer)
- Where is the user value implicit rather than encoded? (leakage into method or entity layer)
- Which method units are not composable or swappable?
- Is any object's abstraction level mismatched to its concern?

## Decision

What restructuring was decided and why it resolves the violations.

## Alternatives Considered

Other approaches and why they were ruled out.

## Consequences

Trade-offs, risks, and what becomes easier or harder after this refactoring.

## Before / After

Required. Show the current structure and the target structure side by side.

**Before:**
```mermaid
graph TD
  ...
```

**After:**
```mermaid
graph TD
  ...
```

## Step-by-Step Plan

Ordered tasks to move from the current state to the target. Be specific — name
files, what moves where, and which layer each belongs to. Use the project's own
directory naming — the label in brackets shows which AEO layer it is.

1. Extract `User` from `src/services/auth.ts` into `src/models/user.ts` [entity]
2. Move selection logic from `auth.ts` into `src/commands/login.ts` [value]
3. Update `src/services/auth.ts` to call the extracted model [method]
4. Delete now-unused code in `src/old/handler.ts`
5. ...
```

After writing the plan, ask:

> "Here's the refactoring plan. Does this look right? I'll apply the changes once you confirm."

Do not modify source code before the user confirms.

### SUMMARY.md entry

```markdown
  - [[<ID>] <title>](./refact/<ID>-<slug>.md)
```
