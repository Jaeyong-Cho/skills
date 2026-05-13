# Skills

A collection of agent skills for software engineering.

---

## PF — Architecture Workflow

PF (Positive Feedback) applies the AEO (Axiology–Epistemology–Ontology) three-layer design philosophy: **why** (user value), **how** (aspect), and **what** (stable objects).

### Workflow

```
[uncertain about design?]
        ↓
   pf-proto  ──→  PoC document
                        ↓
[clear on what to build]
        ↓
      pf    ──→  ADR (written + confirmed)
                        ↓
                   pf-impl  ──→  TDD implementation
                                        ↓
                              code review confirmed
                                        ↓
                               update documentation
```

### Skills

| Skill | When to use |
|-------|-------------|
| `pf-init` | First time — initialize the `.aeo/` book in the project |
| `pf-proto` | Design question is unresolved — build a throwaway prototype, write a PoC document |
| `pf` | Design is clear — run grill-me (or read PoC), write and confirm an ADR |
| `pf-impl` | ADR is confirmed — TDD implementation, RED → GREEN → REFACTOR |
| `pf-docs` | Implementation reviewed — write or update project documentation |
| `pf-docs-migrate` | One-time — migrate old feature-centric docs to layer-centric format |

### Artifacts

```
.aeo/
├── src/
│   ├── adr/    # Architectural Decision Records (0001-slug.md)
│   ├── poc/    # Proof of Concept documents (0001-slug.md)
│   └── docs/   # Project documentation
│       ├── value/    # Why — user goals per component
│       ├── aspect/   # How — workflows per component
│       └── object/   # What — domain objects per component
└── serve.sh    # Start the book server
```

---

## PFJ — Daily Journal Workflow

PFJ (Positive Feedback Journal) is a personal productivity system: daily journaling, goal management, achievement tracking, wiki, and work pattern analysis, rendered via mdbook.

### Workflow

```
[start of day]
      ↓
  pfj-init  ──→  knowledge base ready  (run once)
                        ↓
               write in today.md freely
                        ↓
             [priorities shift mid-day?]
                        ↓
              pfj-adjust  ──→  today's goal updated
                        ↓
               [end of day]
                        ↓
              pfj-review  ──→  daily report written
                                goal progress marked
                                tomorrow seeded
```

### Skills

| Skill | When to use |
|-------|-------------|
| `pfj-init` | First time — initialize the knowledge base in the repo |
| `pfj-adjust` | Mid-day — priorities changed, task blocked, new urgent work |
| `pfj-review` | End of day — close the day, propagate goal progress, seed tomorrow |

---

## Other Skills

| Skill | What it does |
|-------|-------------|
| `grill-me` | Interview relentlessly about any plan or design until shared understanding is reached |
| `caveman` | Ultra-compressed output mode — ~75% fewer tokens |
| `write-a-skill` | Create new agent skills with proper structure and review checklist |

---

## Deprecated

Skills in `deprecated/` are no longer actively used. The `sophist-*` V-model documentation skills have been superseded by the PF workflow.
