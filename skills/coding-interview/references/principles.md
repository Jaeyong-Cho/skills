# Principles and Question Bank

## Simple until complexity is justified

Never recommend microservices, Kafka, Redis, Kubernetes, event-driven architecture, distributed databases, or a design pattern by default. For every non-trivial choice ask: what problem does this solve, what complexity does it introduce, is that complexity justified by an actual requirement in front of us (not an imagined future one)?

## Socratic challenge questions (Problem Workflow round 3)

- Why did you choose this abstraction?
- Why is this responsibility here?
- Why not composition?
- What happens if this requirement changes?
- What happens under concurrency?
- What happens if this dependency fails?
- What happens at 10x scale? At 100x?
- Can this be tested easily?
- What is the simplest alternative?
- What trade-off are you making?
- What would you change if the team doubled?
- What would you remove from this design?

Each question should expose one concrete engineering principle, not just poke at the design.

## Core engineering questions, by category

- **Requirements** — what are we actually solving? Who are the users? What constraints matter?
- **Design** — what are the responsibilities? Where's the boundary? What depends on what?
- **Data** — what state exists, who owns it, how is it stored, what consistency does it need?
- **Failure** — what can fail, how does the system recover, what happens if a dependency is down?
- **Scale** — what happens at 10x, what becomes the bottleneck?
- **Change** — what happens when requirements change, what part is most likely to change?
- **Simplicity** — what's the simplest solution, is this a real problem or an imagined future one?
- **Trade-offs** — what are we gaining, what are we sacrificing, why is that acceptable?

Train the user to ask these unprompted, not just answer them when asked.

## Books as just-in-time references

Don't assign books as homework. When a session surfaces a concept gap, recommend a targeted reference for that concept only, then return to the problem:

- Design Patterns → *Head First Design Patterns*
- Software Architecture → *Fundamentals of Software Architecture*
- Distributed/data systems → *Designing Data-Intensive Applications*
- Software design → *A Philosophy of Software Design*
- Code quality → *Clean Code*
- System design → *System Design Interview*

Record useful ones in `~/study/references/books.md`.
