---
name: spec
description: Create, update, or remove spec-pipeline docs from the stage above them — scenarios, requirements, components, sequences, and the requirement/architecture decision records — each transformed from its upstream artifact in the workflow.md format, reconciled against whatever already exists in that stage's folder. Use when invoked as /spec with to_scen | to_req | to_cmp | to_seq | to_rdr | to_adr.
disable-model-invocation: true
---

# Spec

Advance one spec stage, or record a decision. The arg picks which; each reads the artifact above it and writes filled-in docs below.

```
Goal --to_scen--> SCN --to_req--> REQ --to_cmp--> CMP --to_seq--> SEQ
                                   |                |     ^_________|
                                   |                |   (to_seq reads REQ + CMP)
                            to_rdr |         to_adr |
                                   v                v
                                  RDR              ADR
```

The four linear stages transform each artifact into the next, reconciling against whatever already exists in the target folder rather than always creating fresh docs (see Conventions below). `to_rdr` and `to_adr` are also run standalone as needed, to record decisions beyond the ones `to_req`/`to_cmp`/`to_seq` already pair in when they update a doc.

| arg       | reads         | writes             |
|-----------|---------------|--------------------|
| `to_scen` | a goal + existing SCN docs | `spec/scen/SCN-*.md` |
| `to_req`  | SCN docs + existing REQ docs | `spec/req/REQ-*.md` (+ `spec/rdr/RDR-*.md` on update) |
| `to_cmp`  | REQ docs + existing CMP docs | `spec/cmp/CMP-*.md` (+ `spec/adr/ADR-*.md` on update) |
| `to_seq`  | REQ + CMP docs + existing SEQ docs | `spec/seq/SEQ-*.md` (+ `spec/adr/ADR-*.md` on update) |
| `to_rdr`  | REQ docs      | `spec/rdr/RDR-*.md`  |
| `to_adr`  | CMP + SEQ docs| `spec/adr/ADR-*.md`  |

Read the upstream from `spec/<stage>/` by default; if the user named a file or path in the invocation, use that instead. Write the new docs to `spec/<stage>/{ID}.md`, one file per doc, `mkdir -p` the folder first.

## Conventions (every stage)

- **Interface first.** At each stage the interface is the contract between the stage's parts — get it wrong and every dependent breaks; internal detail can be revised freely as long as the interface holds. Nail the interface before anything else, and let the rest of the doc fill in around it.
- **IDs** are zero-padded and sequential per stage: `SCN-001`, `REQ-001`, `CMP-001`, `SEQ-001`, `RDR-001`, `ADR-001`. Continue from the highest existing ID in the target folder.
- **Status** starts `Draft`. Generated docs are drafts for a human to review — do not mark `Reviewed`/`Done` yourself. The only status you set beyond `Draft` is `Removed`, for a doc whose upstream source disappeared.
- One doc = one unit; produce every doc the upstream demands in a single run, not just the first.
- **Every stage is CRUD against its own folder, not create-only.** Before writing, read what's already in `spec/<stage>/`. For each piece of upstream content, decide:
  - **Create** — no existing doc covers it: mint the next ID as usual.
  - **Update** — an existing doc covers the same thing but upstream changed it: edit that doc in place (same ID, revised body), don't duplicate it. Pair the edit with a decision record where the stage has one — `to_req` writes an RDR, `to_cmp` and `to_seq` write an ADR — capturing what the doc said before, what changed, why, and what alternative was rejected. `to_scen` has no paired decision-record type; update it in place with no companion doc.
  - **Delete** — an existing doc's upstream source is gone (its SCN/REQ/CMP was removed or superseded): don't silently delete the file — set its `Status` to `Removed` and add one line saying why, so the trail stays intact.
  - **Read** — this scan happens every run, even when the result is "everything is a Create."

---

## to_scen — Goal -> Scenario

Input: the goal (prose in the invocation, or a goal file the user names), plus existing SCN docs in `spec/scen/`.

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

Completion: every vertical slice in the goal has one SCN; each SCN has interface-tagged Flow steps and at least the exceptions the goal implies; slices are ordered by real situation; slices matching an existing SCN updated that doc in place instead of duplicating it, and any SCN whose slice dropped out of the goal is marked `Removed`.

---

## to_req — Scenario -> Requirement

Input: SCN doc(s), plus existing REQ docs in `spec/req/`.

Decompose each SCN into testable requirements. Every Flow step becomes one or more functional requirements; every Exception becomes a rejection or boundary requirement. If a Flow step or Exception maps onto a REQ that already exists, update that REQ in place and write a paired RDR recording the change; only mint a new REQ when nothing existing covers it. If an existing REQ's source Flow step/Exception is gone from the SCN, mark that REQ `Removed`.

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

Completion: every Flow step and every Exception across the source scenarios maps to at least one REQ; each REQ states its Interface (Input -> Output) and its AC are concrete and testable; every updated REQ has a paired RDR explaining the change; every removed REQ is marked `Removed`, not deleted.

---

## to_cmp — Requirement -> Component

Input: REQ doc(s), plus existing CMP docs in `spec/cmp/`.

Identify the structural components that realize the requirements. A component is a class/struct/type when the concept holds state or identity; a file/module when it is a stateless function or set of functions. If a REQ's Input -> Output is already realized by an existing component, extend that CMP in place (Responsibility/Interfaces/Depends On) and write a paired ADR recording the change; only mint a new CMP when no existing component covers it. If an existing CMP's source REQ is gone, mark that CMP `Removed`.

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

Completion: every REQ's Input -> Output is realized by some CMP interface; each CMP has a Responsibility, Interfaces, and Depends On; every CMP id cited under Depends On exists (no dangling reference); every updated CMP has a paired ADR explaining the change; every removed CMP is marked `Removed`, not deleted.

---

## to_seq — Requirement + Component -> Sequence

Input: REQ + CMP doc(s), plus existing SEQ docs in `spec/seq/`.

Produce one SEQ per REQ (1:1 unless a requirement genuinely needs more than one collaboration). A SEQ is the collaboration of components that satisfies its requirement. If a REQ already has a SEQ and the CMP collaboration changed, update that SEQ in place and write a paired ADR recording the change; only mint a new SEQ for a REQ that doesn't have one yet. If an existing SEQ's source REQ is gone, mark that SEQ `Removed`.

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

Completion: every REQ has a SEQ; every Sequence step that invokes another component cites that component's actual interface signature; each SEQ has a Flow and Acceptance Criteria; every used CMP's `Used By` lists the SEQ; every updated SEQ has a paired ADR explaining the change; every removed SEQ is marked `Removed`, not deleted.

---

## to_rdr — Requirement -> Requirement Decision Record

Input: REQ doc(s), plus their source SCN for context.

Scan the requirements for points that are underspecified or admit more than one valid implementation — the places a reader would otherwise have to guess. For each, draft one RDR that records the **choice made among alternatives**, not the requirement itself.

```
# RDR-001
- Status: Draft

## Requirement
- REQ-001 <requirement title>

## Context
<what is unspecified or in tension>

## Decision
<the choice made>

## Rationale
- <why this choice>

## Alternatives
- <option not taken>

## Consequences
- <trade-off accepted>
```

Completion: every underspecified or multi-option point in the source requirements has an RDR; each RDR links its REQ and states Context, Decision, Rationale, Alternatives, and Consequences.

---

## to_adr — Component -> Architectural Decision Record

Input: CMP doc(s), plus SEQ for how the components collaborate.

Scan the architecture for decisions a reader would question — why a responsibility became its own component, why a dependency points the way it does, why an abstraction was introduced. For each, draft one ADR that records the choice among alternatives.

```
# ADR-001
- Status: Draft

## Architecture
- <affected component(s), e.g. CMP-003 Cart Repo>

## Context
<the architectural force or constraint>

## Decision
<the choice made>

## Rationale
- <why this choice>

## Alternatives
- <option not taken>

## Consequences
- <trade-off accepted>
```

Completion: every non-obvious architecture decision in the source components has an ADR; each ADR names the affected component(s) and states Context, Decision, Rationale, Alternatives, and Consequences.
