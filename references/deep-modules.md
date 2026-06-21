# Deep Modules

From "A Philosophy of Software Design":

**Deep module** = small interface + lots of implementation

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid)

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing interfaces, ask:

- Can I reduce number of methods?
- Can I simplify parameters?
- Can I hide more complexity inside?

## Interface Design for Testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area**
   - Fewer methods = fewer tests needed
   - Fewer params = simpler test setup

---

## Design Smells (shallow module signs)

| Smell | What to look for |
|---|---|
| **Shallow module** | Interface nearly as wide as implementation — many tiny methods |
| **Duplicated logic** | Same rule or algorithm in more than one place |
| **Information leakage** | Same knowledge scattered across call sites instead of owned by one module |
| **Temporal decomposition** | Split by execution order rather than responsibility |
| **Pass-through method** | Function that just calls another with same arguments |
| **Leaky interface** | Callers must know internal details to use module correctly |
| **Conjoined twins** | Two modules always edited together — should probably be one |
