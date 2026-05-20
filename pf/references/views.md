# Architecture Views (ISO 42010)

**Concern** — something stakeholder cares about. **Viewpoint** — rules for constructing view that addresses concern. **View** — actual diagram/document produced by applying viewpoint to system.

Discipline: identify stakeholders → surface concerns → select viewpoints → produce views.

---

## Common viewpoints

| Viewpoint | Stakeholder concern | Typical diagram |
|---|---|---|
| Module / decomposition | What exists, what each unit owns, what can change independently | Package/layer diagram |
| Component-and-Connector | Runtime elements, data flow, failure points, latency | Sequence, flow diagram |
| Allocation / deployment | Where things run, operational dependencies | Deployment diagram |

Not every ADR needs all three. Include only views that address actual stakeholder concern for this decision.

---

## In VAO context

- Object layer → Module viewpoint (what stable units exist)
- Aspect layer → C&C viewpoint (how they interact at runtime)
- Allocation → separate concern, add when deployment is affected

If stakeholder's concern cannot be read from VAO Decision section, that concern needs a view.
