---
name: spec
description: Scaffold spec-pipeline docs from the stage above them — scenarios, requirements, components, sequences — each transformed from its upstream artifact in the workflow.md format. Use when invoked as /spec with to_scen | to_req | to_cmp | to_seq.
disable-model-invocation: true
---

# Spec

Advance one spec stage. The arg picks the stage; each stage reads the artifact above it and writes the stage below, filled in.

```
Goal --to_scen--> SCN --to_req--> REQ --to_cmp--> CMP --to_seq--> SEQ
                                                    ^______________|
                                              (to_seq reads REQ + CMP)
```

| arg       | reads         | writes             |
|-----------|---------------|--------------------|
| `to_scen` | a goal        | `spec/scen/SCN-*.md` |
| `to_req`  | SCN docs      | `spec/req/REQ-*.md`  |
| `to_cmp`  | REQ docs      | `spec/cmp/CMP-*.md`  |
| `to_seq`  | REQ + CMP docs| `spec/seq/SEQ-*.md`  |

Read the upstream from `spec/<stage>/` by default; if the user named a file or path in the invocation, use that instead. Write the new docs to `spec/<stage>/{ID}.md`, one file per doc, `mkdir -p` the folder first.

## Conventions (every stage)

- **Interface first.** At each stage the interface is the contract between the stage's parts — get it wrong and every dependent breaks; internal detail can be revised freely as long as the interface holds. Nail the interface before anything else, and let the rest of the doc fill in around it.
- **IDs** are zero-padded and sequential per stage: `SCN-001`, `REQ-001`, `CMP-001`, `SEQ-001`. Continue from the highest existing ID in the target folder.
- **Status** starts `Draft`. Generated docs are drafts for a human to review — do not mark `Reviewed`/`Done` yourself.
- One doc = one unit; produce every doc the upstream demands in a single run, not just the first.

---

## to_scen — Goal -> Scenario

Input: the goal (prose in the invocation, or a goal file the user names).

Split the goal into **vertical slices** — each slice is one thing a user can do end to end, and becomes one SCN. Order the slices by the real situation a user lives through (open app -> browse -> add -> checkout), not by feature grouping.

Interface: the components are Client/User, Program/System, Output/Data; the interface is their interaction, so tag every Flow step with the boundary it crosses.

```
# SCN-001 <title>
- Status: Draft

## User Scenario
As a <role>, I want <capability> so that <outcome>.

## Components
- Client/User: <who>
- Program/System: <what>
- Output/Data: <what is shown/returned>

## Flow (Interface: Client/User <-> Program/System <-> Output/Data)
1. [Client/User -> Program/System] <user action>
2. [Program/System -> Output/Data] <system effect>
3. [Program/System -> Client/User] <response shown>

## Exceptions
- <what can go wrong>
```

Completion: every vertical slice in the goal has one SCN; each SCN has interface-tagged Flow steps and at least the exceptions the goal implies; slices are ordered by real situation.

---

## to_req — Scenario -> Requirement

Input: SCN doc(s).

Decompose each SCN into testable requirements. Every Flow step becomes one or more functional requirements; every Exception becomes a rejection or boundary requirement.

Interface: state the Input -> Output boundary explicitly before writing the Acceptance Criteria — the AC are that boundary spelled out as test cases.

```
# REQ-001
- Status: Draft

## Requirement
The system shall <do what>.

## Interface (Input -> Output)
- Input: <triggering input / condition>
- Output: <guaranteed output>

## Acceptance Criteria
- <concrete, testable condition>
- <concrete, testable condition>
```

Completion: every Flow step and every Exception across the source scenarios maps to at least one REQ; each REQ states its Interface (Input -> Output) and its AC are concrete and testable.

---

## to_cmp — Requirement -> Component

Input: REQ doc(s).

Identify the structural components that realize the requirements. A component is a class/struct/type when the concept holds state or identity; a file/module when it is a stateless function or set of functions.

Interface: the Interfaces section (real method/function/endpoint signatures) IS the contract — design it with the most care. Every REQ's Input -> Output must be realized by some component's interface.

```
# CMP-001 <name>
- Status: Draft

## Responsibility
<single responsibility>

## Interfaces
- <signature, e.g. addProductToCart(productId: string, quantity: number): Cart>
- <endpoint, e.g. POST /cart/items>

## Depends On
- <CMP-id it calls>

## Used By
- <SEQ-id — leave pending; to_seq backfills this>
```

Completion: every REQ's Input -> Output is realized by some CMP interface; each CMP has a Responsibility, Interfaces, and Depends On; every CMP id cited under Depends On exists (no dangling reference).

---

## to_seq — Requirement + Component -> Sequence

Input: REQ + CMP doc(s).

Produce one SEQ per REQ (1:1 unless a requirement genuinely needs more than one collaboration). A SEQ is the collaboration of components that satisfies its requirement.

Interface: every Sequence step that invokes another component MUST cite that component's actual interface signature from its CMP doc — not a prose description. This keeps the sequence traceable to each CMP's Interfaces section and catches drift when a signature changes. After writing, backfill each CMP's `Used By` with the SEQ ids that use it.

```
# SEQ-001 <title>
- Status: Draft

## Requirement
REQ-001

## Components
- <name> (CMP-001)
- <name> (CMP-002)

## Flow
Cart API
    |
    v
Cart Service
  |     |
  |     +--------> Cart Repo
  |
  +--------------> Product Repo

## Sequence
1. <CMP>'s `<signature>` <does what>.
2. <CMP> calls <CMP>'s `<signature>` to <do what>.

## Acceptance Criteria
1. <observable condition for step 1>
2. <observable condition for step 2>
```

Completion: every REQ has a SEQ; every Sequence step that invokes another component cites that component's actual interface signature; each SEQ has a Flow and Acceptance Criteria; every used CMP's `Used By` lists the SEQ.
