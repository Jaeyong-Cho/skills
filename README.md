# Skills

A collection of agent skills for software engineering.

---

## AEO — Architecture Workflow

AEO (Axiology–Epistemology–Ontology) is a three-layer design philosophy for building software with clear separation of **why** (user value), **how** (method/aspect), and **what** (stable entities).

### Workflow

```
[uncertain about design?]
        ↓
   aeo-proto  ──→  PoC document
                        ↓
[clear on what to build]
        ↓
      aeo    ──→  ADR (written + confirmed)
                        ↓
                   aeo-impl  ──→  TDD implementation
                                        ↓
                              code review confirmed
                                        ↓
                               update documentation
```

### Skills

| Skill | When to use |
|-------|-------------|
| `aeo-init` | First time — initialize the `.aeo/` book in the project |
| `aeo-proto` | Design question is unresolved — build a throwaway prototype, write a PoC document |
| `aeo` | Design is clear — run grill-me (or read PoC), write and confirm an ADR |
| `aeo-impl` | ADR is confirmed — TDD implementation, RED → GREEN → REFACTOR |
| `aeo-docs` | Implementation reviewed — write or update project documentation |

### Artifacts

```
.aeo/
├── src/
│   ├── adr/    # Architectural Decision Records (0001-slug.md)
│   ├── poc/    # Proof of Concept documents (0001-slug.md)
│   └── docs/   # Project documentation
└── serve.sh    # Start the book server
```

---

## POFE — Daily Journal Workflow

POFE is a personal productivity system: daily journaling, goal management, achievement tracking, wiki, and work pattern analysis, rendered via mdbook.

### Workflow

```
[start of day]
      ↓
  pofe-init  ──→  knowledge base ready  (run once)
                        ↓
               write in today.md freely
                        ↓
             [priorities shift mid-day?]
                        ↓
              pofe-adjust  ──→  today's goal updated
                        ↓
               [end of day]
                        ↓
              pofe-review  ──→  daily report written
                                goal progress marked
                                tomorrow seeded
```

### Skills

| Skill | When to use |
|-------|-------------|
| `pofe-init` | First time — initialize the knowledge base in the repo |
| `pofe-adjust` | Mid-day — priorities changed, task blocked, new urgent work |
| `pofe-review` | End of day — close the day, propagate goal progress, seed tomorrow |

---

## Other Skills

| Skill | What it does |
|-------|-------------|
| `write-a-skill` | Create new agent skills with proper structure and review checklist |

---

## Deprecated

Skills in `deprecated/` are no longer actively used. The `sophist-*` V-model documentation skills have been superseded by the AEO workflow.
