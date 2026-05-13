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

- Tests a user-facing outcome
- Uses only the public interface (`checkout`)
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
- Passes even if the behavior is wrong

## Rule

If the test breaks after a refactor but the behavior hasn't changed, the test was wrong.
A good test reads like a specification — it says what the system can do, not how it does it.
