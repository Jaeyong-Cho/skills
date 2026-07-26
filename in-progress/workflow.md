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
Goal -> Scen + AC -> Req + AC -> Arch + AC -> Algo + AC -> Impl + AC -> Test -> Feedback
 ```

- The value of each stage
  - Goal > Feedback > Scen + Test > Req + Test > Arch + Test > Impl

#### Interface vs internal responsibility
- Interface = the interaction between components at that stage's level of abstraction, not any single component's internals.
- Interface is a contract between components/stages — get it wrong and every dependent component breaks, so it deserves the most careful design attention.
- Internal details are implementation choices within that contract; they can be revised freely as long as the interface holds.

##### What "interface" means per stage
- Scenario: the components are Client/User, Program/System, and Output/Data. The interface is their interaction — the Flow steps that cross the boundary (user action in, system response/output data out).
- Requirement: the interface is the boundary between the triggering input/condition and the guaranteed output, captured in Acceptance Criteria.
- Architecture: a Component's Interfaces section (method/API signatures) is literally the interface — the contract between components.

#### The release rule
- Scenario
  - Scenario should be a one vertical slice
  - Scen: user can add to cart
  - Scen: user can register email
  - Scen: user can exit with button
- One vertical slice done = minimum release unit
- One vertical slice done is mean every stage's are specified and confirmed by human
- The Scenarios should be defined with real situation ordered.
  - Scenario: As a user, I want to product list when open the app, so that I can select a product to buy.
  - Scenario: As a user, I want to add a product to my shopping cart, so that I can purchase it later.
  - Scenario: As a user, I want to checkout my shopping cart, so that I can complete my purchase.

#### Scenario format
- The components at this stage are Client/User, Program/System, and Output/Data. The interface is their interaction, so each Flow step is tagged with which components it crosses.
```
# SCN-001 Add Product to Cart
- Status: Draft/Reviewed/Done

## User Scenario
As a User, I want to add a product to my shopping cart so that I can purchase it later.

## Components
- Client/User: the shopper
- Program/System: the cart service
- Output/Data: the cart shown back to the user

## Flow (Interface: Client/User <-> Program/System <-> Output/Data)
1. [Client/User -> Program/System] User selects a product.
2. [Client/User -> Program/System] User clicks **Add to Cart**.
3. [Program/System -> Output/Data] The system adds the product to the cart.
4. [Program/System -> Client/User] The updated cart is shown.

## Exceptions
- Product is out of stock.
```

#### Requirement format
- The interface at this stage is the boundary between the triggering input/condition and the guaranteed output, so each requirement states that boundary explicitly before the Acceptance Criteria spell it out as test cases.
```
# REQ-001
- Status: Draft/Reviewed/Done

## Requirement
The system shall add the selected product to the shopping cart.

## Interface (Input -> Output)
- Input: selected product, current cart
- Output: cart with the product added

## Acceptance Criteria
- Product appears in the cart.
- Cart count increases by 1.

---

# REQ-002
- Status: Draft/Reviewed/Done

## Requirement
If the product already exists in the cart, the system shall increase its quantity.

## Interface (Input -> Output)
- Input: product already in cart, additional quantity
- Output: cart with the existing item's quantity increased

## Acceptance Criteria
- Existing quantity: 2
- Add the same product.
- Result quantity: 3.

---

# REQ-003
- Status: Draft/Reviewed/Done

## Requirement
The system shall reject adding an out-of-stock product.

## Interface (Input -> Output)
- Input: out-of-stock product
- Output: error response, cart unchanged

## Acceptance Criteria
- An error message is displayed.
- The cart remains unchanged.
```

#### Architecture format
- Component is a reuseable structural element of the system, including its responsibility and relationships with other components
  - Component can be may be class, struct, file...
  - Match a component to a class/struct/type when that concept exists for its responsibility (e.g. it holds state). If no class concept exists (e.g. a stateless function or a set of functions), the component is the file/module instead.
  - Component's interface can be public method, public function, public API, public endpoint...
- Sequence is the collaboration of components to satisfy one or more requirements. Each Dynamic is explicitly mapped to the requirements it realizes and includes the interaction flow and acceptance criteria for that collaboration.
  - Mostly it will be mapping with requirements 1:1
  - Each Sequence step that invokes another component must cite that component's actual interface (method/endpoint signature from its CMP doc), not just a prose description — this keeps the sequence traceable to each component's Interfaces section and catches drift if a signature changes.

```
# CMP-001 Cart API
- Status: Draft/Reviewed/Done

## Responsibility
Receive cart requests.

## Interfaces

- POST /cart/items
- Cart Response

## Depends On
- CMP-002

## Used By
- SEQ-001
- SEQ-002

# CMP-002 Cart Service
- Status: Draft/Reviewed/Done

## Responsibility
Execute cart business logic.

## Interfaces

- addProductToCart(productId: string, quantity: number): Cart

## Depends On
- CMP-003
- CMP-004

## Used By
- SEQ-001
- SEQ-002
- SEQ-003

# SEQ-001 Add Product to Cart
- Status: Draft/Reviewed/Done

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

1. Cart API's `POST /cart/items` receives the request.
2. Cart Service calls Product Repo's `getProduct(productId: string): Product` to load the product.
3. Cart Service calls Cart Repo's `getCart(cartId: string): Cart` to load the cart.
4. Cart Service's `addProductToCart(productId: string, quantity: number): Cart` adds the product to the cart.
5. Cart Service calls Cart Repo's `saveCart(cart: Cart): void` to save the cart.
6. Cart API returns the `Cart Response`.

## Acceptance Criteria
1. Cart API forwards the request to Cart Service.
2. Product Repository returns a valid product.
3. Shopping cart is successfully loaded.
4. Product is added or quantity is updated.
5. Shopping cart is persisted.
6. Updated cart is returned to the client.
```

#### Algorithm Design Format
- Algorithm will defined for each architecture component's interfaces
```
# ALG-001
- Status: Draft/Reviewed/Done

## Component
- CMP-002 Cart Service

## Interface
- addProductToCart(productId: string, quantity: number): Cart

## Algorithm
1. Load the product using Product Repository.
2. If the product is out of stock, throw an error.
3. Load the shopping cart using Cart Repository.
4. If the product already exists in the cart, increase its quantity.
5. If the product does not exist, add it to the cart with the specified quantity.
6. Save the updated cart using Cart Repository.

## Acceptance Criteria
1. Product is successfully loaded.
2. Out-of-stock products are rejected.
3. Shopping cart is successfully loaded.
4. Product quantity is updated or added correctly.
5. Updated cart is persisted and returned.
```


#### Requirement Decision Record Format
```
# RDR-001
- Status: Draft/Reviewed/Done

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
- Status: Draft/Reviewed/Done

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

