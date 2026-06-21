# VAO Layers

| Layer | Question |
|-------|----------|
| **Value** | What user goal is worth automating? |
| **Aspect** | What algorithm realizes that goal, and from which angle? |
| **Object** | What stable domain things does the system operate on? |

Each class belongs to exactly one layer. If a class is hard to place, the boundary is probably wrong.

---

## Value — Why

Encodes what end user needs. Entry point in code: use-case, command, or application service. Defines which needs are worth satisfying, what success looks like, what must never happen, and which aspect delivers the result. If user's need only lives in a comment or ticket, it hasn't been encoded yet.

---

## Aspect — How

Two roles — keep them separate:

**Algorithm** — the workflow, strategy, or computation that realizes the user goal. In DDD terms this is a **Domain Service**: stateless, no identity, coordinates multiple objects when the operation does not naturally belong to any single one.

```
// TransferService coordinates two Accounts — belongs to neither
class TransferService {
    transfer(source, destination, amount) {
        source.withdraw(amount);      // each object owns its own rule
        destination.deposit(amount);
    }
}
```

Use an Aspect (service) only when the behavior genuinely spans multiple objects. If it only touches one, push it into the object.

**Lens** — cross-cutting behavior that multiple objects need but belongs to none of them. Auth, logging, billing, caching — these cut across `User`, `Order`, `Product` alike. Each aspect asks one question of the object; reads only the properties relevant to its concern.

```
        User          Order         Product
          │              │               │
          ▼              ▼               ▼
   ┌──────────────────────────────────────────┐
   │           AuthAspect                     │  ← cross-cutting
   └──────────────────────────────────────────┘
   ┌──────────────────────────────────────────┐
   │           BillingAspect                  │  ← cross-cutting
   └──────────────────────────────────────────┘
```

**Core rule**: Objects are concern-agnostic. Aspects own concern. Aspects are injected into the Value layer via constructor — no proxies, no weaving.

| Aspect | Concern | Reads from objects |
|--------|---------|-------------------|
| `AuthAspect` | "Is this user permitted?" | `user.role`, `user.sessionToken` |
| `BillingAspect` | "Has this user paid?" | `user.plan`, `user.subscriptionStatus` |
| `AuditAspect` | "What happened and who did it?" | `user.id`, `order.id`, `order.status` |
| `CacheAspect` | "Is this result fresh?" | `product.id`, `product.updatedAt` |

Structure into composable units — strategies, workflows, pipelines — so aspects can be swapped without changing objects or value definition.

---

## Object — What

Domain objects are not data containers. Defines full identity: properties, actions, behaviors, relationships. Logic scattered upward into services or aspects is leakage — object is too thin.

In DDD terms, an Object is an **Entity**: it has a unique identity, mutable state, a lifecycle, and enforces its own invariants. The object owns the rules that govern its own state — not the aspect above it.

```
// Rich object — owns its own invariant
class Order {
    cancel() {
        if (status == SHIPPED) throw new Error("Cannot cancel shipped order");
        status = CANCELLED;
    }
}

// Anemic object — leaked invariant
class Order { status; }
class OrderService {
    cancel(order) {         // ← invariant doesn't belong here
        if (order.status == SHIPPED) throw ...
        order.status = CANCELLED;
    }
}
```

**Ask**: "Whose business rule is this?" If it depends on the state of one object, it belongs inside that object. If it coordinates multiple objects, it belongs in an Aspect.

**Size must match concern**: too large covers things outside concern; too small forces callers to reconstruct meaning.

**Invariance principle**: object must remain same regardless of which aspect looks at it. If object changes shape for a specific use case, it has leaked into the aspect layer.

For relationships: decide cardinality, ownership (who controls lifecycle), navigability (which direction), aggregate boundary (what changes atomically together). View-specific joins belong in aspect layer, not object.

---

## How They Relate

```
value layer   →  defines what is worth doing (user need)
    ↓
aspect layer  →  defines how to do it, from which aspect
    ↓
object layer  →  defines what exists to operate on
```

Objects remain stable — not shaped by any single aspect or value concern. Design order: value → aspects → objects (iterative in practice).

---

## Dependency Rule

**Outer layers reference inner. Inner layers never reference outer.**

```
Value   → may depend on Aspect, Object
Aspect  → may depend on Object
Object  → depends on nothing above it
```

An inner layer that references an outer layer is a design error. Example violations:
- `Object` holds a reference to an `Aspect` → object is too thin; logic leaked upward
- `Aspect` calls into a `Value` use-case → aspect is doing selection logic, not computation
- `Aspect` calls another `Aspect` directly → cross-cutting logic should compose at the Value layer

This is checked in the **Dependencies** section of every API doc.

---

## Design Smells

| Smell | What it looks like | Layer |
|-------|-------------------|-------|
| Selection logic duplicated across callers | Value layer not extracted | Value |
| Algorithm with magic thresholds | Value mixed into aspect layer | Value |
| User need only in docs | Value layer implicit, not encoded | Value |
| Aspect with no clear algorithm | Pass-through, not a real layer | Aspect |
| Aspect duplicates object logic | Object too thin — logic leaked upward | Aspect |
| Aspect doing too much | One aspect, multiple unrelated concerns | Aspect |
| Aspect calls aspect | `AuthAspect` calls `AuditAspect` directly | Aspect |
| Aspect holds domain state | `BillingAspect` stores `user.plan` internally | Aspect |
| Value layer skips aspect | Command directly checks `user.role === 'admin'` | Value |
| Anemic object | Object has state but no behavior; rules live in Aspect | Object |
| Concern in object | `user.logAccess()`, `order.checkBilling()` | Object |
| Object shaped for one aspect | `user.authContext`, `user.billingView` | Object |
| God object | Evaluates, executes, and models domain | Object |
| Object size mismatch | Too large or too small for concern being served | Object |
