# Function and OOP Abstraction Guidelines

Full rule set behind `../abstraction-levels.md`'s quick-reference table — open this file when a smell needs the reasoning or a Good/Bad example, not for routine grilling.

Design code around three levels of abstraction:

- **L1 — Intent / Public Contract**
- **L2 — Domain / Business Behavior**
- **L3 — Implementation / Mechanism**

The primary goal is to make code readable from top to bottom as a description of what the system does, while hiding unnecessary implementation details behind meaningful abstractions.

---

## 1. L1 — Intent / Public Contract

### Purpose

L1 expresses **what the system or component does** from the perspective of its caller.

Typical examples:

- Public APIs
- Use cases
- Application services
- Public entry points
- Interfaces / Protocols
- High-level orchestration methods

Example:

```python
class OrderService:

    def checkout(self, order):
        self.validate_order(order)
        self.calculate_total(order)
        self.process_payment(order)
        self.complete_order(order)
```

A developer should be able to understand the overall behavior of `checkout()` without reading its implementation details.

### Rules

- L1 should read like a natural-language description of the system's behavior.
- Express high-level intent and business flow.
- Use meaningful domain-oriented function names.
- Avoid database, HTTP, JSON, file-system, SDK, or framework details.
- Do not expose unnecessary implementation details.
- Prefer calling L2 operations rather than implementing detailed business rules directly.
- Do not directly call low-level infrastructure APIs.
- The sequence of L1 operations should communicate the main workflow clearly.

#### Good

```python
def checkout(order):
    validate_order(order)
    calculate_total(order)
    process_payment(order)
    complete_order(order)
```

#### Bad

```python
def checkout(order):
    response = requests.post("/payment", json=order)
    cursor.execute("INSERT INTO orders ...")
    ...
```

The second version exposes implementation details and makes the high-level behavior harder to understand.

---

## 2. L2 — Domain / Business Behavior

### Purpose

L2 expresses **what the system should do according to domain rules**.

Typical examples:

- Domain logic
- Business rules
- Validation
- Calculations
- Policies
- State transitions
- Domain behavior
- Meaningful internal operations

Example:

```python
class Order:

    def calculate_total(self):
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        shipping = self.calculate_shipping()

        return subtotal - discount + shipping
```

### Rules

- Express domain concepts and business rules.
- Use domain terminology rather than technical terminology.
- Conditional logic and loops are allowed when they represent business behavior.
- Keep business rules independent from infrastructure details.
- Do not directly depend on database, HTTP, file-system, or framework details when avoidable.
- L2 may depend on L3 abstractions to perform technical operations.
- Each function should represent one meaningful domain concept or responsibility.

#### Good

```python
def calculate_discount(order):
    if order.customer.is_vip:
        return order.total * 0.1

    return 0
```

The rule is about the business domain, so it belongs to L2.

#### Bad

```python
def calculate_discount(order):
    response = requests.get("/customers/" + order.customer_id)
    ...
```

The business rule is now mixed with HTTP implementation details.

---

## 3. L3 — Implementation / Mechanism

### Purpose

L3 expresses **how something is technically performed**.

Typical examples:

- Database access
- HTTP requests
- External APIs
- File-system operations
- Network communication
- Serialization / deserialization
- ORM operations
- SDK calls
- Framework-specific code
- Operating-system interactions

Example:

```python
class StripePaymentGateway:

    def pay(self, payment):
        payload = self._create_payload(payment)

        response = self._client.post(
            "/payments",
            json=payload
        )

        return self._parse_response(response)
```

### Rules

- Focus on technical mechanisms.
- Hide infrastructure details behind meaningful interfaces.
- Do not contain business decisions unless strictly required by the technical mechanism.
- Changes to infrastructure, libraries, or external services should be isolated here.
- L3 should expose a simple interface to higher-level code.
- Do not allow technical details to leak upward into L1.

---

## 4. Public / Private Is a Different Axis

Do **not** equate:

```text
public = L1
private = L2/L3
```

Public/private and L1/L2/L3 describe different things.

**Access modifier answers:** Who can use this?

**Abstraction level answers:** What kind of concept does this code represent?

Therefore, a public method can be L1 **or L2**.

```python
class Order:

    # Public L2 domain behavior
    def calculate_total(self):
        ...

    # Public L2 domain behavior
    def can_checkout(self):
        ...
```

These methods may be public because callers legitimately need them, but they still represent domain behavior rather than high-level system intent.

Conversely, an L1 operation may internally use private L2/L3 methods.

---

## 5. Public API Should Reveal Intent

When a class exposes a public method, prefer exposing a meaningful concept rather than an implementation mechanism.

**Prefer**

```python
order.checkout()
order.cancel()
order.calculate_total()
```

**Avoid**

```python
order.execute_step()
order.update_database()
order.send_http_request()
order.process_data()
```

Public APIs should communicate **what the object means or does**, not how it performs the operation.

---

## 6. Interfaces Define Contracts, Not Mechanisms

Interfaces / Protocols should generally describe **capabilities and intent**, not implementation details.

**Good**

```python
class PaymentGateway(Protocol):

    def pay(self, payment) -> PaymentResult:
        ...
```

The interface says: "Something capable of processing a payment." It does not say whether the implementation uses Stripe, PayPal, HTTP, or a database.

**Implementation**

```python
class StripePaymentGateway(PaymentGateway):

    def pay(self, payment):
        ...
```

The concrete implementation contains the technical mechanism.

The dependency structure should look like:

```text
Application / Domain
        │
        ▼
PaymentGateway
   (contract)
        │
        ▼
StripePaymentGateway
   (implementation)
        │
        ▼
Stripe SDK / HTTP
```

---

## 7. Keep One Abstraction Level Per Function

A function should not mix unrelated abstraction levels.

**Bad**

```python
def checkout(order):
    validate_order(order)
    calculate_total(order)

    response = requests.post(
        "/payment",
        json=order
    )

    database.execute(...)
```

This mixes business behavior, HTTP implementation, and database implementation.

**Good**

```python
def checkout(order):
    validate_order(order)
    calculate_total(order)
    process_payment(order)
    save_order(order)
```

Technical details are delegated downward.

---

## 8. Prefer a Clear Dependency Direction

The rule is **never call upward** — not "always exactly one hop down." The preferred conceptual direction is:

```text
L1 — Intent
 ↓
L2 — Domain / Business Behavior
 ↓
L3 — Implementation / Mechanism
```

but two shapes both satisfy the rule and are both normal, not exceptions:

- **Same-level composition** — an L1 function calling another L1 function (`L1 → L1 → L2`), an orchestration composed of orchestrations. Same for L2 calling L2.
- **Level skip** — an L1 function calling L3 directly (`L1 → L3`), when there's genuinely no business rule between the intent and the mechanism and the direct call still reads as intent. Skip only because there's truly nothing for L2 to add — not to avoid writing a domain rule that should exist. Skipping *that* rule, not the absence of one, is the smell (Missing L2, in `../abstraction-levels.md`'s smells table).

What's never acceptable, regardless of shape: L3 calling L2 or L1, or L2 calling L1 — a dependency pointing toward more abstract code from more mechanical code.

Higher-level code should also depend on **abstractions**, not necessarily concrete L3 implementations.

```text
             L1
              │
              ▼
             L2
              │
              ▼
       PaymentGateway
          (interface)
              ▲
              │
             L3
              │
       StripePaymentGateway
```

The important principle: higher-level code should not need to know which concrete technology performs the operation.

---

## 9. Use the One-Sentence Test

Every meaningful function should be explainable in one clear sentence.

```python
calculate_discount(order)
```

can be explained as: "Calculate the discount according to the applicable business rules." Good.

But if explaining a function requires: "It validates the order, retrieves customer information, calculates the discount, saves the result, and sends an event..." then the function probably contains multiple responsibilities or abstraction levels. Consider decomposing it.

---

## 10. Extract Functions Based on Meaning, Not Size

Do not create functions merely because a block of code is long. Create a function when the code represents a **meaningful concept, responsibility, or operation**.

Ask: **"Does giving this code a name make the program easier to understand?"**

If yes, extraction is likely useful. If no, keeping the code inline may be clearer.

A three-line function can be valuable:

```python
calculate_shipping(order)
```

while a thirty-line function may still be appropriate if it represents one coherent concept.

---

## 11. Prefer Intent-Revealing Names

Function names should describe **what the operation means**, rather than how it is implemented.

**Prefer**

```python
validate_order()
calculate_total()
process_payment()
save_order()
notify_customer()
```

**Avoid**

```python
run_calculation()
execute_step()
handle_data()
process_request()
do_operation()
```

Names should help the reader understand the system without opening the function immediately.

---

## 12. Allow Public L2 Methods When They Represent Real Domain Behavior

Do not force every public method into L1.

```python
class Order:

    def calculate_total(self):
        ...

    def can_cancel(self):
        ...

    def cancel(self):
        ...
```

These can all be public because they are legitimate operations on an `Order`. However, their abstraction level is L2 because they express domain behavior.

A higher-level L1 operation might be:

```python
class OrderService:

    def checkout(self, order):
        order.validate()
        order.calculate_total()
        self.payment_gateway.pay(order)
        order.complete()
```

This distinction should be preserved.

---

## 13. Hide Mechanics, Not Meaning

Private methods should primarily hide **implementation mechanics**, not meaningful domain behavior.

**Good**

```python
def _build_payment_payload(payment):
    ...

def _parse_payment_response(response):
    ...

def _create_database_record(order):
    ...
```

These are implementation details.

**Be careful with**

```python
def _calculate_discount(order):
    ...
```

If discount calculation is an important domain concept, hiding it merely because it is implemented as a private method may make the domain model less expressive.

The question is not "Is this private?" The question is "Is this a meaningful concept that callers or developers should be able to understand?"

---

## 14. Use the Three-Level Decision Test

When creating or modifying a function, ask these questions in order:

1. Does this describe the overall purpose or workflow? → **L1**
2. Does this express a business rule, domain concept, or state transition? → **L2**
3. Does this describe a technical mechanism or interaction with infrastructure? → **L3**
4. Is the method public or private? Treat this as a **separate decision** — public/private determines accessibility, L1/L2/L3 determines abstraction. Do not use one classification as a substitute for the other.

---

## 15. Optimize for Progressive Disclosure

The codebase should allow developers to understand the system progressively. The preferred reading experience is:

```text
L1
"What does the system do?"
        ↓
L2
"What business rules make it work?"
        ↓
L3
"How is it technically implemented?"
```

A developer should not have to read database queries, HTTP requests, or framework code to understand the main business flow. The developer should be able to **drill down only when more detail is needed**.

---

## Core Principle

The primary design goal is: **make the code read like a description of the system at the appropriate level of abstraction.**

Use:

```text
L1 → Intent
L2 → Business Meaning
L3 → Technical Mechanism
```

while independently managing:

```text
Public / Private → Accessibility
Interface / Implementation → Contract vs Mechanism
```

Do not optimize primarily for the number of functions or lines per function. Optimize for: **clear intent → clear business behavior → isolated implementation details.**
