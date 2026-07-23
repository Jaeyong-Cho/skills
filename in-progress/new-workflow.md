## Think about the Software Engineering Process
- These days, I am enjoy making efficient workflow with AI.
- What is the good process?
  - Agaile
  - Water-fall
  - Water-scrum-fall
  - ASPICE
- But it is ambigous
- I need a detailed decision tree when developing

### Exponential Software Development Process from Prototype to Product
- The main loop of the process
```
Goal -> Scen + AC -> Req + AC -> Arch + AC -> Impl + AC -> Test -> Feedback
 ```

- The value of each stage
  - Goal > Feedback > Scen + Test > Req + Test > Arch + Test > Impl


#### Incremental software development
- The loop can be separated.

```
Loop 1: Scenario + Req analyze loop
Goal -> Scen + AC -> Impl -> Test -> Feedback
```
- Feedback action
  - feedback goal
  - feedback scenario
  - specify requirements (RDR: requirement decision record)

```
Loop 2: Req + Arch analyze loop
Scen -> Req + AC -> Impl -> Test -> Feedback
```
- Feedback action
  - feedback scenario
  - feedback requirement
  - specify architecture (ADR: architectural decision record)

```
Loop 3: Archi + Impl analyze loop
Req -> Arch + AC -> Impl -> Test -> Feedback
```
- Feedback action
  - feedback requirement
  - feedback architecture

#### The release rule
- Scenario
  - Scenario should be a one vertical slice
  - Scen: user can add to cart
  - Scen: user can register email
  - Scen: user can exit with button
- One vertical slice done = minimum release unit
- One vertical slice done is mean every stage's are specified and confirmed by human


#### Scenario format
```
# SCN-001 Add Product to Cart

## Goal
User adds a product to the shopping cart.

## Flow
1. User selects a product.
2. User clicks **Add to Cart**.
3. The system adds the product to the cart.
4. The updated cart is shown.

## Exceptions
- Product is out of stock.
```

#### Requirement format
```
# REQ-001

## Requirement
The system shall add the selected product to the shopping cart.

## Acceptance Criteria
- Product appears in the cart.
- Cart count increases by 1.

---

# REQ-002

## Requirement
If the product already exists in the cart, the system shall increase its quantity.

## Acceptance Criteria
- Existing quantity: 2
- Add the same product.
- Result quantity: 3.

---

# REQ-003

## Requirement
The system shall reject adding an out-of-stock product.

## Acceptance Criteria
- An error message is displayed.
- The cart remains unchanged.
```

#### Architecture format
- Component is a reuseable structural element of the system, including its responsibility and relationships with other components
- Sequence is the collaboration of components to satisfy one or more requirements. Each Dynamic is explicitly mapped to the requirements it realizes and includes the interaction flow and acceptance criteria for that collaboration.
  - Mostly it will be mapping with requirements 1:1

```
# CMP-001 Cart API

## Responsibility
Receive cart requests.

## Interfaces

### Input
- POST /cart/items

### Output
- Cart Response

## Depends On
- CMP-002

## Used By
- SEQ-001
- SEQ-002

# CMP-002 Cart Service

## Responsibility
Execute cart business logic.

## Depends On
- CMP-003
- CMP-004

## Used By
- SEQ-001
- SEQ-002
- SEQ-003

# SEQ-001 Add Product to Cart

## Requirement
REQ-001

## Components
- Cart API (CMP-001)
- Cart Service (CMP-002)
- Cart Repo (CMP-003)
- Product Repo (CMP-004)

## Flow

```text
Cart API
    |
    v
Cart Service
  |     |
  |     +--------> Cart Repo
  |
  +--------------> Product Repo

## Sequence

1. Cart API receives the request.
2. Cart Service loads the product.
3. Cart Service loads the cart.
4. Cart Service adds the product.
5. Cart Service saves the cart.
6. Cart API returns the response.

## Acceptance Criteria
1. Cart API forwards the request to Cart Service.
2. Product Repository returns a valid product.
3. Shopping cart is successfully loaded.
4. Product is added or quantity is updated.
5. Shopping cart is persisted.
6. Updated cart is returned to the client.
```

#### Requirement Decision Record Format
```
# RDR-001

## Requirement
- REQ-001 Add product to shopping cart.

## Context
The expected behavior for adding an existing product is not specified.

## Decision
Increase the quantity of the existing cart item.

## Rationale
- Simpler user experience.
- Consistent with common e-commerce systems.

## Alternatives
- Create a new cart item for every addition.

## Consequences
- Cart remains compact.
- Users cannot distinguish additions by time.
```

#### Architectural Decision Record Format
```
# ADR-001

## Architecture
- ARCH-001 Shopping Cart

## Context
The shopping cart must be persisted and shared across requests.

## Decision
Introduce a Cart Repository component.

## Rationale
- Separates business logic from persistence.
- Improves testability and maintainability.

## Alternatives
- Persist directly in Cart Service.

## Consequences
- Cleaner architecture.
- Additional repository abstraction.
```
