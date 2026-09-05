# 500-Problem Curriculum

Long-term roadmap, not a checklist to rush. Numbers are problem-slug prefixes under `~/study/problems/`.

| Phase | Problems | Focus | Examples |
|---|---|---|---|
| 1. Programming & DSA | #1-50 | arrays, strings, hash maps, stacks/queues, linked lists, trees, graphs, recursion, sorting/searching, heaps, complexity | LRU Cache, Rate Limiter |
| 2. OOP & Code Design | #51-100 | encapsulation, polymorphism, composition vs. inheritance, responsibility assignment, coupling/cohesion, SOLID | Parking Lot, Elevator System |
| 3. Refactoring & Clean Code | #101-150 | code smells, large functions, duplicated logic, hidden dependencies, testability, legacy code | Refactor a 500-line function, make legacy code testable |
| 4. Design Patterns | #151-200 | Strategy, Factory, Adapter, Observer, Decorator, Command, State, Template Method, Builder, Chain of Responsibility, DI — learned through problems, not memorized | Payment Strategy, Plugin Architecture |
| 5. Software Architecture | #201-250 | module boundaries, layering, dependency direction, modular monolith vs. services, event-driven, ports and adapters | Layered Architecture, Service Boundary Design |
| 6. API & Data Modeling | #251-300 | REST/RPC contracts, resource modeling, validation, pagination, versioning, idempotency, domain models, state transitions | Order API, Idempotent Payment API |
| 7. Databases & Data Systems | #301-350 | relational/NoSQL choice, indexes, transactions, isolation, locking, normalization, query optimization | Design Indexes, Optimize a Slow Query |
| 8. Distributed Systems | #351-400 | replication, partitioning, consistency, distributed locks, queues, retries/timeouts, idempotency, leader election | Distributed Job Queue, Distributed Lock |
| 9. Production Engineering | #401-450 | debugging, observability, logging/metrics/tracing, incidents, performance, capacity, deployment/rollback | Memory Leak Investigation, Production Incident Investigation |
| 10. Decomposition & Judgment | #451-500 | ambiguous requirements, stakeholder needs, system decomposition, prioritization, trade-offs, product thinking | Enterprise Document Search, One-Year Engineering Ownership Review |

Raw CS-fundamentals gaps underneath any phase (a shaky data structure, sorting algorithm, complexity call) — see `cs-fundamentals.md`'s topic order, close the gap via its linked resource, then return to the problem. `cs-fundamentals.md` is the direction for *how* a topic gets learned (interleaved practice, talk-and-write-it-out, spaced repetition); this file is the direction for *which* problem exercises that topic.

For every pattern in Phase 4, ask: what problem does it solve, what problem does it create, when should it *not* be used.

## Repetition

Solving something once is not understanding it. When the user struggles with a concept (e.g. composition vs. inheritance), revisit it later through a different problem in a different phase (payment system, then notification system, then plugin system) to test whether they can generalize the principle — not just recall the first answer.

## Palantir-oriented emphasis

When prep is specifically for Palantir-style interviews, weight problems toward: coding, problem decomposition, ambiguous requirements, practical OOP/code design, learning unfamiliar systems fast, debugging/re-engineering, technical communication, product/user thinking, engineering trade-offs — turning a vague operational problem into Requirements → Domain Model → Responsibilities → Data Model → APIs → Workflow → Edge Cases → Failure Modes → Trade-offs, not a traditional system-design template.
