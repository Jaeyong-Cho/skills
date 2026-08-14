---
name: dev-grill-me
description: Run a @skills/grill-me interview covering both feature and fix concerns in one pass — intent, scope, value, root cause, architecture, impact, observability/monitoring, testability, release plan.
disable-model-invocation: true
---

# Dev Grill Me

Run `@skills/grill-me` covering every point below, whether the work is a feature or a fix. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical:

- Intent and purpose
- Scope-in / scope-out
- Value for end-user
- Expected
- Root cause (for fix)
- Fundamental Solution (**MUST NOT** Ad-Hoc or Workaround)
- Architecture — components and interfaces
- Impact scope
- Observability and Monitoring
- Testability
- Branch (git)
- New simple and representative testcase
- Release and ship plan

## Impact Level
**MUST MARK** for each question's impact level

### Low Level (0)
- Constant value
- Configuration value
- Local variable / internal logic
- Function implementation
- Single-module internal structure
- Single-module data structure

### Medium Level (1)
- Multi-function logic
- Multi-file change
- Module internal behavior
- Module interface
- Shared data structure

### High Level (2)
- Database schema
- Cross-service logic
- API contract
- Data migration
- External library / service integration
- Protocol / file format
- Deployment architecture
- System architecture
- Cross-system contract
- Platform / OS / hardware dependency
- External organization / vendor contract
- Production-scale breaking change

## Uncertainty
**MUST MARK** for each questions uncertainty
- High: Can not known until execute and see the result
- Low: Obviously know the expected result

## Action
- Low impact level + Low uncertainty = Skip question. Just show.
- Low impact level + High uncertainty = Skip question. Mark to add assertion point (like assert in c++ or something)
- High impact level + Low uncertainty = Ask question and confirm.
- High impact level + High uncertainty = Ask question and confirm. Mark to add assertion point  

**MUST** Use assertions aggressively wherever there is any uncertainty
**MUST NOT** implementation work has started.
Once complete, next step is `@skills/to-plan` to dump the recorded answers into a plan document.
