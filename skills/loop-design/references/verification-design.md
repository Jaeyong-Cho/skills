# Verification Design

Verification is an executable description of expected system state. For every invariant, establish:

```text
What MUST be true?
How is it observed?
What evidence demonstrates failure?
```

## Categories

Choose the smallest check that observes the requirement.

- **Behavior:** build, existing tests, valid/invalid input, integration, regression, or E2E outcome.
- **API:** required or forbidden API, signature, parameters, return type, visibility, or compatibility.
- **Class / structure:** class or method presence, interface implementation, inheritance, ownership, visibility, or source/module placement.
- **CLI:** option presence or absence, defaults, argument requirements, invalid-input behavior, and exit status.
- **Architecture:** dependency direction, forbidden dependency, layer/module boundary, cycle prevention, or required component relationship.

Select architecture constraints whose violation would materially damage the design; do not attempt to encode the entire architecture. For example:

```text
Design: Domain MUST NOT depend on UI.
Check:  04-domain-no-ui-dependency.sh
```

## Check contract

Every `verify/NN-{slug}.sh` returns `0` on PASS and non-zero on FAIL. On failure, expose useful, concrete output:

```text
Expected: <expected state>
Actual:   <observed state>
Evidence: <command output, diff, path, response, or artifact>
```

Prefer deterministic checks. A check should observe the claimed result, rather than use a passing command as indirect proof.

## RED and ordering

When practical, write a check for a genuine missing requirement, observe it fail, implement, then observe it pass:

```text
Expected state → verification → RED → implementation → GREEN
```

Never create an artificial failure just to follow this pattern.

Order checks for diagnostic value and cost: cheap, fast, local, specific checks precede broad, slow, or expensive checks. A typical order might be:

```text
00 build
01 static or interface check
02 focused behavior
03 integration
04 architecture
05 regression
06 E2E
```

This is an example, not a taxonomy. Use the actual cost and signal of the project.

## Green prefix

After fixing check `N`, rerun checks `00` through `N`, not only `N`:

```text
V0
V0 ∧ V1
V0 ∧ V1 ∧ V2
```

The valid prefix should grow. A full pass remains the completion condition.

## Design decisions

Use this translation when a decision is mechanically checkable:

```text
Design decision → executable invariant → verification
```

Keep subjective rationale and non-enforceable preferences in documentation instead of forcing them into a linter.
