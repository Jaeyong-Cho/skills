<!-- Global rules for writing documents -->
Write in a clear, concise, and professional report style.

- Use short, simple sentences. Prefer one idea per sentence.
- Avoid long or complex sentence structures.
- Place key information first, especially important findings, numbers, changes, risks, or issues.
- Use transition words (e.g., Therefore, However, In addition, As a result) to maintain logical flow.
- Keep paragraphs brief and focused on a single topic.
- Follow a logical report structure:
  - Introduction: objective, background, scope, and methodology.
  - Body: facts, analysis, findings, and supporting evidence.
  - Conclusion: key takeaways, insights, recommendations, and next actions.
- Prioritize clarity over stylistic or decorative writing.
- Use direct, objective, and business-oriented language.
- Present conclusions and recommendations explicitly rather than implying them.
<!-- Global rules for writing documents -->

# Architecture: {Title}

**ADR:** {path to `.context/adr/{slug}.md`}

## Static View
> Directory structure, classes — each with purpose and description — and their dependency relationships, placed per archi.md's layers (Objects/Logics/Usecase/External). Dependencies as a Mermaid diagram; an arrow pointing from an inner layer to an outer one is a design error.

**Directory structure**
```
e.g.
src/auth/
  service.py   # AuthService (Usecase)
  cache.py     # TokenCache (Logics)
```

**Classes**
|Class|Layer|Purpose|
|--|--|--|
|e.g. `AuthService`|Usecase|Orchestrates token validation: cache first, DB fallback|
|e.g. `TokenCache`|Logics|Reads/writes validated tokens in Redis with a 5-minute TTL|

**Dependencies**
```mermaid
graph LR
    AuthService["AuthService · Usecase"] --> TokenCache["TokenCache · Logics"]
    TokenCache --> Redis[("Redis")]
    AuthService --> DB[("DB")]
```

## Dynamic View
> One Mermaid sequence diagram per scenario in the requirements spec's User Scenario section — name the subsection to match.

### {Scenario name}
```mermaid
e.g.
sequenceDiagram
    participant C as Client
    participant A as AuthService
    participant T as TokenCache
    participant D as DB
    C->>A: validate(token)
    A->>T: get(token)
    alt cache hit
        T-->>A: cached result
    else cache miss
        A->>D: validate(token)
        D-->>A: result
        A->>T: set(token, result)
    end
    A-->>C: result
```
