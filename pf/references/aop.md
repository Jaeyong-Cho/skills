# Cross-Cutting Concerns (AOP)

From Aspect-Oriented Programming:

**Cross-cutting concern** = behavior multiple domain objects need, but that belongs to none of them. Authentication, logging, billing, caching, rate-limiting — these cut across `User`, `Order`, `Product` alike. Objects shouldn't know about them.

**Aspect** = cross-cutting concern implemented in one place, applied to many objects from outside.

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
   ┌──────────────────────────────────────────┐
   │           AuditAspect                    │  ← cross-cutting
   └──────────────────────────────────────────┘
```

Objects stay same. Aspects weave in from outside.

---

## Core Rule

**Objects are concern-agnostic. Aspects own concern.**

`User` object should not know it is being audited, billed, or rate-limited. Those concerns live in aspects that use `User` as raw material. When concern leaks into object — object starts checking auth, recording audit logs, or formatting for specific view — object has been contaminated.

---

## Design Pattern

Design each aspect around one question it asks of object:

| Aspect | Concern | What it reads from objects |
|--------|---------|---------------------------|
| `AuthAspect` | "Is this user permitted?" | `user.role`, `user.sessionToken` |
| `BillingAspect` | "Has this user paid?" | `user.plan`, `user.subscriptionStatus` |
| `AuditAspect` | "What happened and who did it?" | `user.id`, `order.id`, `order.status` |
| `CacheAspect` | "Is this result fresh?" | `product.id`, `product.updatedAt` |

Same object appears in multiple aspects. Each aspect uses only properties relevant to its concern.

---

## Code Examples

**Object: concern-agnostic**

```typescript
class User {
  id: string
  email: string
  role: 'admin' | 'member'
  plan: 'free' | 'pro'
  subscriptionStatus: 'active' | 'expired'
  sessionToken: string | null

  hasRole(role: string): boolean { ... }
  isSubscribed(): boolean { ... }
}
```

`User` defines what it *is* — properties, actions, behaviors. No idea who is asking or why.

**Aspect: uses User with one concern**

```typescript
// AuthAspect — cross-cutting concern: authorization
class AuthAspect {
  authorize(user: User, action: string): void {
    if (!user.hasRole('admin') && action === 'delete') {
      throw new UnauthorizedError()
    }
  }
}

// BillingAspect — cross-cutting concern: subscription gating
class BillingAspect {
  requiresPro(user: User): void {
    if (!user.isSubscribed()) {
      throw new PaymentRequiredError()
    }
  }
}

// AuditAspect — cross-cutting concern: audit trail
class AuditAspect {
  record(user: User, action: string, target: Order): void {
    this.log.write({ userId: user.id, action, orderId: target.id })
  }
}
```

Each aspect narrow. Reads only what it needs. Does not store concern-specific state on object.

**Value layer: composes aspects**

```typescript
class DeleteOrderCommand {
  constructor(
    private auth: AuthAspect,
    private audit: AuditAspect,
  ) {}

  execute(user: User, order: Order): void {
    this.auth.authorize(user, 'delete')
    order.delete()
    this.audit.record(user, 'delete', order)
  }
}
```

Value layer decides *which* concerns apply to action and in what order — it is composition point.

---

## Design Smells

| Smell | What it looks like | What's wrong |
|-------|-------------------|--------------|
| **Concern in object** | `user.logAccess()`, `order.checkBilling()` | Object knows about cross-cutting concern — it shouldn't |
| **Duplicated concern** | Auth check copy-pasted across 5 commands | Concern not extracted into aspect |
| **Aspect doing too much** | `SecurityAspect` handles auth, billing, and rate-limiting | One aspect, multiple concerns — split it |
| **Object shaped for one aspect** | `user.authContext`, `user.billingView` | Aspect-specific fields leaked into object |
| **Value layer skips aspect** | Command directly checks `user.role === 'admin'` | Concern escaped into value layer |
