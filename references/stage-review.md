# Stage-Based Multi-Persona Review

Use this protocol for the Requirements → Object-Oriented Design → TDD Implementation workflow. Review each artifact at the stage where a problem is cheapest to correct. Do not maximize review coverage or force every persona to run with equal depth.

## Shared review rules

Every reviewer must:

- adopt only the assigned persona;
- review concerns appropriate to the current stage;
- use evidence from the artifact, repository, or diff;
- distinguish defects from optional improvements;
- explain the concrete consequence of each finding;
- recommend the smallest adequate change;
- avoid unrelated redesign and speculative future-proofing;
- explicitly identify concerns that belong to another stage.

Use this finding format:

```text
Severity: Critical | Major | Minor | Suggestion
Location: <requirement / object / class / method / test>
Finding: <specific problem>
Why it matters: <concrete consequence>
Recommendation: <smallest reasonable fix>
Persona: <assigned persona>
```

The orchestrator merges overlapping findings and ends with:

1. **Must fix before proceeding**
2. **Should improve without blocking**
3. **Deliberately deferred**

Use Critical or Major only when the issue can invalidate the stage outcome, create material risk, or make the next stage expensive or unsafe. Minor and Suggestion findings do not block by themselves.

## 1. Requirement specification review

### Goal

Determine whether we are building the right thing before deciding how to build it. Focus on domain correctness, user needs, completeness, clarity, and testability. Avoid classes, interfaces, frameworks, schemas, and other implementation details unless a technical constraint fundamentally changes the requirement.

### Domain Expert — Primary

Review from the perspective of someone who deeply understands the business domain.

Checklist:

- Do the requirements correctly represent the domain?
- Are important business rules missing?
- Are domain concepts and terminology used consistently?
- Are implicit assumptions made explicit?
- Do any requirements contradict real-world domain behavior?

### User — Primary

Review from the perspective of the actual user or operator.

Checklist:

- Does the workflow make sense from the user's perspective?
- Are important user scenarios missing?
- Are unnecessary steps being introduced?
- What happens when the user makes a mistake?
- Can the user recover from failures?

### Tester

Review the requirements for verifiability and edge cases.

Checklist:

- Can each requirement be objectively verified?
- Are success and failure conditions clearly defined?
- Are boundary conditions specified?
- Are error scenarios missing?
- Are acceptance criteria sufficiently precise?

### Skeptic

Challenge the necessity and complexity of the requirements.

Checklist:

- Is this requirement actually necessary?
- What user or business outcome does it support?
- Could the same outcome be achieved more simply?
- Are speculative requirements being introduced for hypothetical future needs?

Exit question: **Are we confident that we are solving the right problem?**

## 2. Object-oriented design review

### Goal

Determine whether the proposed object-oriented design provides a simple, coherent, and maintainable foundation for implementation. Focus on responsibilities, boundaries, collaborations, dependencies, coupling, cohesion, and likely change scenarios. Defer detailed implementation concerns until real code exists.

### Implementer — Primary

Review the design from the perspective of the developer who must implement it.

Checklist:

- Are object responsibilities clear?
- Can the design be translated naturally into code?
- Are responsibilities assigned to appropriate objects?
- Is cohesion high?
- Is coupling appropriately low?
- Are dependency directions clear?
- Are abstractions justified?
- Are object collaborations understandable?
- Will any part of this design naturally produce complicated implementation code?

Use SOLID and other design principles as diagnostic tools, not goals in themselves.

### Future Developer — Primary

Review the design using realistic future change scenarios.

Checklist:

- What happens if a likely new requirement is introduced?
- Which objects would need to change?
- Would a small feature require changes across many unrelated objects?
- Are likely variation points isolated?
- Is the design rigid where change is reasonably expected?

Prefer concrete change scenarios over speculative extensibility. For example: “The system supports credit-card payments. What would change to support bank transfers?” Use the scenario to expose rigidity and shotgun surgery before implementation makes them expensive.

### Simplifier

Challenge unnecessary design complexity.

Checklist:

- Is this abstraction necessary now?
- Does this interface represent a real variation point?
- Is this layer providing meaningful separation?
- Could this collaboration be expressed more simply?
- Are we designing for hypothetical requirements rather than known needs?
- Are there objects whose existence is not justified by a clear responsibility?

Actively look for premature abstraction, speculative generality, and unnecessary indirection.

### Security / SRE — Risk-Based

Apply this persona only when the system has meaningful security, reliability, distributed-system, or operational concerns.

Checklist:

- Where are the trust boundaries?
- What happens when an external dependency fails?
- Are failure boundaries clear?
- Can partial failures leave the system inconsistent?
- Are authentication and authorization responsibilities located appropriately?
- Are there design decisions that would make production failures difficult to recover from?

Raise only concerns that materially affect the design.

Exit question: **Is this design simple and robust enough to start TDD implementation without creating expensive structural problems?**

## 3. TDD implementation review

### Goal

Evaluate implementation and tests as one evolving design artifact:

```text
Test → Behavior → Implementation → Refactoring
```

Tests are part of implementation and provide design feedback. The central question is not merely whether tests pass, but whether tests and production code express the required behavior through a maintainable design.

### TDD Practitioner — Primary

Review whether TDD drives behavior and design rather than merely accumulating tests.

Checklist:

- Do tests describe meaningful behavior?
- Is each test motivated by a requirement or discovered behavior?
- Are tests written at an appropriate level?
- Does the test suite provide fast feedback?
- Are tests helping reveal design problems?
- Is implementation evolving through small, understandable steps?
- Is refactoring happening after behavior is established?
- Are tests enabling refactoring rather than preventing it?

Use Red → Green → Refactor as a guide, not ceremony. The important property is useful design feedback.

### Clean Code Reviewer — Primary

Review production code for clarity and maintainability.

Checklist:

- Do names communicate intent?
- Are functions and methods focused?
- Do classes have coherent responsibilities?
- Are abstraction levels consistent?
- Is control flow unnecessarily complicated?
- Are side effects obvious?
- Is duplicated knowledge or behavior present?
- Does the code clearly express domain concepts?

### Tester — Primary

Approach the behavior adversarially.

Checklist:

- How can this behavior be broken?
- What happens at boundary values?
- What happens with invalid input?
- What happens during partial failure?
- What happens when dependencies return unexpected results?
- Are important state transitions tested?
- Are negative paths represented?
- Are relevant concurrency scenarios covered?

Complement TDD rather than demanding more tests for their own sake. Identify meaningful missing behaviors, not maximum test count or coverage percentage.

### Maintainer — Primary

Review tests and production code from the perspective of a developer encountering the code six months later.

Checklist:

- Can a new developer understand intended behavior from the tests?
- Can they understand why the production code exists?
- Are dependencies explicit?
- Are important assumptions hidden?
- Are there surprising side effects?
- Can behavior be changed without understanding unrelated code?
- Is the impact of a change reasonably predictable?

Tests should contribute to understanding rather than obscure it.

### Simplifier

Look for unnecessary complexity in both production code and tests.

Checklist:

- Can production code be deleted or simplified?
- Can test setup be simplified?
- Are there unnecessary mocks, stubs, or test doubles?
- Is a test coupled to an irrelevant implementation detail?
- Is an abstraction justified by actual duplication or variation?
- Did TDD produce small abstractions that no longer provide value?
- Are we generalizing beyond current requirements?

Prefer reducing unnecessary code over adding abstractions.

### Domain Expert — Supporting

Verify that tests and implementation still represent intended domain behavior.

Checklist:

- Do tests encode important business rules?
- Are domain invariants represented?
- Does implementation use domain concepts correctly?
- Did implementation reveal assumptions that should cause requirements to be updated?

### Security Reviewer — Risk-Based

Apply for security-sensitive functionality.

Checklist:

- What happens with malicious or malformed input?
- Can authorization boundaries be bypassed?
- Are sensitive operations tested under invalid permissions?
- Are trust-boundary assumptions represented in tests?
- Are failure paths safe by default?

### Performance / SRE — Risk-Based

Apply for production-critical functionality.

Checklist:

- Are expensive operations hidden inside common code paths?
- What happens when dependencies timeout?
- Are retries safe?
- Are failures observable?
- Can important failures be diagnosed?
- Are there obvious scalability or contention risks?

Do not turn ordinary unit tests into performance or infrastructure tests. Raise these concerns only when they materially affect implementation or design.

### Test quality principles

- **Test behavior, not implementation.** Ask: “Would this test remain valid if internal implementation changed while observable behavior stayed the same?”
- **Support refactoring.** Tests should make structural improvement safer, not freeze accidental implementation decisions.
- **Avoid test-induced design damage.** Ask: “Does this abstraction exist because production design needs it, or only because a test wanted to mock it?” Testability alone does not justify unnecessary production abstractions.
- **Prefer meaningful coverage.** Prioritize business rules, domain invariants, boundary conditions, state transitions, failure behavior, and externally observable behavior.

Exit question: **Do the tests and implementation together express the required behavior through code we are comfortable maintaining and changing?**

## Design feedback loop

Implementation may reveal flaws in the original OOD. Do not force code to conform to an incorrect design:

```text
TDD reveals design friction
        ↓
Identify the underlying design assumption
        ↓
Determine whether the issue is local or architectural
        ↓
Refactor implementation OR revisit OOD
        ↓
Continue TDD
```

Signals that OOD may need reconsideration include:

- objects are difficult to instantiate;
- tests require excessive mocking;
- responsibilities repeatedly move between objects;
- small behaviors require coordinating many objects;
- dependency graphs become complicated;
- domain rules lack a natural owner;
- simple tests require large fixtures;
- small requirement changes cause widespread modifications.

These are design feedback signals, not automatic failures of TDD.

## Review budget and checkpoints

Review depth should follow risk and reversal cost:

- Requirements: 5–10 minutes
- OOD: 10–20 minutes
- TDD: incremental at meaningful checkpoints

Meaningful TDD checkpoints include completion of a requirement or use case, a new domain concept, significant refactoring, unexpected design friction, or before merging a meaningful change. Do not stop every Red–Green–Refactor cycle for a full multi-persona review.
