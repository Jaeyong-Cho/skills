# Progress Tracking

Three files under `~/study/progress/`. Keep entries concise; don't create a note for every small fact.

## mastery.md

```markdown
| Area | Level | Evidence | Weakness |
|---|---:|---|---|
| DSA | 1-5 | problems solved | ... |
| CS Fundamentals | 1-5 | `cs-fundamentals.md` topic-order self-ratings, current topic | ... |
| OOP | 1-5 | design exercises | ... |
| Architecture | 1-5 | architecture exercises | ... |
| Distributed Systems | 1-5 | system exercises | ... |
| Engineering Judgment | 1-5 | decomposition exercises | ... |
```

Raise a level only when reasoning quality improves, never for completed-problem count alone. Distinguish **completed** (attempted it), **understood** (can explain the trade-offs), and **mastered** (can generalize it to a new problem) — when uncertain, keep the lower label until there's evidence.

### 1-5 difficulty-level rubric

1. **Foundation** — understands basic concepts, needs guidance
2. **Application** — solves standard problems independently
3. **Integration** — combines multiple concepts
4. **Real World** — reasons about ambiguous requirements, failures, trade-offs
5. **Senior Engineering** — makes architectural decisions, spots hidden risks, explains trade-offs clearly

## mistakes.md

A flat list of recurring patterns, e.g.:

```
- Overengineering before understanding requirements
- Choosing abstractions too early
- Weak ownership boundaries
- Ignoring failure modes
- Poor concurrency reasoning
- Premature use of design patterns
- Weak API contracts
- Not considering operational complexity
```

When the same mistake shows up again, say so explicitly ("this is becoming a recurring pattern") and shape the next exercise to target it.

## learning-log.md

One entry per meaningful session:

```
Date:
Problem:
What I attempted:
What I learned:
Key mistake:
Key insight:
Concepts:
What I would change:
Mastery:
Next recommended exercise:
```

## Weekly/monthly review

Read `problems/`, `experience/`, `progress/`, `notes/`, `reviews/` since the last review and answer: what improved, what mistakes are recurring, which concepts are still weak, which problems were too easy or exposed a gap, what to study next, what to revisit, how engineering judgment has changed. Then update the three files above — never fabricate progress.
