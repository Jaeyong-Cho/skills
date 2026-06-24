# Meta-Pattern Reference

Source: https://metapatterns.io

## The Coordinate System

Every architecture can be placed on three axes:
- **Abstractness** (vertical) — inversely proportional to distance from the system's clients; a graphical UI is highly abstract (users interact with it directly), while device drivers at the opposite end operate in raw bits and registers; intermediate layers (routing, proxies, OS) are placed toward the top even if not highly abstract, to keep diagrams simple — high-level above, low-level below
- **Subdomain** (horizontal) — distinct functional areas side by side
- **Sharding** (diagonal) — multiple deployed instances of the same module

The shape of the plot *is* the pattern. Minor variations collapse; fundamental structures remain.

## Cohesers & Decouplers

Forces that determine when to consolidate vs split.

**Rule**: Only decouple when a decoupler is present and active. Default to cohesion.

## Basic Patterns

### Monolith
Single unified system. All components run in one process.
- **Properties**: simple deploy, easy shared state, hard to scale parts independently
- **Smell**: becomes a big ball of mud without internal structure discipline

### Shards
Multiple identical instances of the same module, each owning a partition of data/load.
- **Properties**: horizontal scale, no cross-shard coordination, partition key is critical
- **Smell**: business logic that needs cross-shard joins

### Layers
Components stratified by abstraction (e.g. External → Usecase → Logics → Objects).
- **Properties**: inner layers are stable and reusable; outer layers change more often
- **Rule**: dependency always points inward; outer never depended on by inner
- **Smell**: inner layer importing from outer layer

### Services
Independent units that communicate over a network boundary.
- **Properties**: independent deploy, network latency, harder consistency, loose coupling
- **Smell**: services that must be deployed together or share a database

### Pipeline
Sequential stages; data flows in one direction through transforms.
- **Properties**: easy to add/remove stages, stages are stateless, output of one is input of next
- **Smell**: stages that need to call back to earlier stages

## Extension Patterns

### Middleware
Software that provides communication between other components. Acts as glue.

### Shared Repository
Central storage (DB, file system, memory) that multiple components read/write.
- **Caution**: creates implicit coupling through shared schema

### Proxy
Intermediary that controls access to a component. Adds auth, caching, rate limiting without changing the target.

### Orchestrator
Central coordinator that calls other services in sequence and manages their interactions.
- **Contrast with Choreography**: orchestrator knows the flow; choreography delegates via events

### Sandwich
Combines layers with services — a layered internal structure wrapped in a service boundary.

## Implementation Patterns

### Plugins
Extensible core with interchangeable modules behind a defined interface.
- **When**: behavior must vary without changing the core

### Hexagonal Architecture (Ports & Adapters)
Core business logic at center; all I/O (HTTP, DB, CLI, events) plugs in via adapters.
- **Rule**: core has zero knowledge of adapters
- **When**: domain logic must be testable without infrastructure

### Microkernel
Minimal core + specialized plugins. Core routes; plugins do the work.
- **When**: many optional capabilities around a small stable base

### Mesh
Distributed components communicate directly with each other (no central coordinator).
- **When**: fully decentralized, each node is autonomous
