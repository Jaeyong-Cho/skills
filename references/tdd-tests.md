# Writing Good Tests

Tests verify behavior through public interfaces — not implementation details.

## Good test

```typescript
// Describes what the system does from the outside
it("user can checkout with a valid cart", async () => {
  const cart = Cart.withItems([item("book", 10)])
  const result = await checkout(cart, validPayment())
  expect(result.status).toBe("confirmed")
  expect(result.orderId).toBeDefined()
})
```

- Tests user-facing outcome
- Uses only public interface (`checkout`)
- Survives any internal refactor

## Bad test

```typescript
// Coupled to implementation
it("calls PaymentGateway.charge", async () => {
  const gateway = jest.fn()
  await checkout(cart, gateway)
  expect(gateway).toHaveBeenCalledWith(10)
})
```

- Tests how, not what
- Breaks when you rename or restructure internals
- Passes even if behavior is wrong

## Tautological test

Expected value must be an independent literal, not recomputed the same way the implementation does — otherwise the test passes by construction even when the logic is wrong.

```typescript
// Bad — expected value recomputed via the same formula the code uses
it("sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }]
  const expected = items.reduce((sum, i) => sum + i.price, 0)
  expect(calculateTotal(items)).toBe(expected)
})

// Good — expected value is a known literal
it("sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15)
})
```

## Verify through the interface, not storage

Checking a database row directly after a call couples the test to L3 (per `abstraction-levels.md`) instead of the function's actual contract.

```typescript
// Bad — bypasses the interface to verify
it("createUser saves to database", async () => {
  await createUser({ name: "Alice" })
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"])
  expect(row).toBeDefined()
})

// Good — verifies through the interface
it("createUser makes the user retrievable", async () => {
  const user = await createUser({ name: "Alice" })
  expect((await getUser(user.id)).name).toBe("Alice")
})
```

## Rule

If test breaks after refactor but behavior hasn't changed, test was wrong.
Good test reads like specification — says what system can do, not how it does it.
