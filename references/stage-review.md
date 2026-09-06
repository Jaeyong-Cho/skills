# Stage Review Protocol

Use this protocol for the three review skills: requirements, object-oriented design (OOD), and TDD implementation.

## Purpose

Review an artifact at the stage where a problem is cheapest to fix. Review only the current stage; defer concerns that require a later artifact. Review depth follows reversal cost and risk.

Every reviewer must:

- adopt only the assigned persona;
- use evidence from the artifact, repository, or diff;
- distinguish defects from optional improvements;
- explain the concrete consequence of each finding;
- recommend the smallest adequate change;
- avoid unrelated redesign and speculative future-proofing;
- explicitly list concerns deferred to another stage.

## Finding format

```text
Severity: Critical | Major | Minor | Suggestion
Location: <section / object / class / method / test>
Finding: <specific problem>
Why it matters: <concrete consequence>
Recommendation: <smallest reasonable fix>
Persona: <assigned persona>
```

The orchestrator merges duplicates and ends with:

1. **Must fix before proceeding**
2. **Should improve without blocking**
3. **Deliberately deferred**

Use `Critical` or `Major` only when the issue can invalidate the stage outcome, cause material risk, or make the next stage expensive or unsafe. `Minor` and `Suggestion` never block by themselves.

## Stage lenses

### Requirements

Goal: decide whether the right problem is specified, without designing its implementation.

- **Domain Expert — primary:** domain correctness, rules, terminology, assumptions, contradictions.
- **User:** understandable workflow, missing scenarios, mistakes, recovery, unnecessary steps.
- **Tester:** objective verification, success/failure conditions, boundaries, error cases, precise acceptance criteria.
- **Skeptic:** necessity, outcome, simpler alternatives, speculative scope.

Defer classes, interfaces, frameworks, schemas, and implementation choices unless a technical constraint changes the requirement.

Exit question: **Are we confident we are solving the right problem?**

### OOD

Goal: decide whether the design is simple, coherent, and robust enough to implement.

- **Implementer — primary:** clear responsibilities, cohesion, coupling, dependency direction, understandable collaborations, justified abstractions.
- **Future Developer — primary:** concrete likely change scenarios, variation points, rigidity, shotgun surgery.
- **Simplifier:** premature abstraction, indirection, layers, objects, and interfaces without a current responsibility or substitution boundary.
- **Security / SRE — risk-based:** trust and failure boundaries, external dependency failure, partial inconsistency, authorization placement, recoverability.

Do not review code-level details that cannot be known until implementation exists. Use concrete change scenarios, not hypothetical extensibility.

Exit question: **Is this design simple and robust enough to start TDD without expensive structural problems?**

### TDD implementation

Goal: review tests and production code as one evolving design artifact:

```text
Test → Behavior → Implementation → Refactoring
```

- **TDD Practitioner — primary:** behavior-driven tests, fast feedback, small steps, useful Red/Green/Refactor feedback, tests that permit refactoring.
- **Clean Code Reviewer — primary:** intent-revealing names, focused methods, coherent responsibilities, consistent abstraction levels, explicit side effects, domain clarity.
- **Tester — primary:** meaningful boundary, invalid-input, failure, state-transition, dependency, and relevant concurrency behavior.
- **Maintainer — primary:** six-month readability, explicit dependencies, visible assumptions, predictable change impact.
- **Simplifier:** deletable code, simpler setup, justified mocks and abstractions, no test-induced design damage.
- **Domain Expert — supporting:** business rules, invariants, correct domain concepts, requirement feedback.
- **Security Reviewer — risk-based:** malformed or malicious input, authorization, trust boundaries, safe failure.
- **Performance / SRE — risk-based:** timeout/retry safety, observability, expensive paths, contention and scalability risks when material.

Test observable behavior rather than implementation details. Prioritize business rules, invariants, boundaries, state transitions, failure behavior, and user-visible outcomes over test count or coverage percentage.

Exit question: **Do tests and implementation express the required behavior through maintainable, changeable code?**

## Review budget

Use a lightweight default:

- Requirements: 5–10 minutes
- OOD: 10–20 minutes
- TDD: incremental at a meaningful checkpoint, not every Red/Green/Refactor cycle

Meaningful checkpoints include a completed requirement or use case, a new domain concept, significant refactoring, design friction, or a meaningful merge.
