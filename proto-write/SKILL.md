---
name: proto-write
description: Write a skeleton prototype of code — stubs, scaffolding, and structure only, no implementation detail. Use when user wants to sketch the shape of a feature first, mentions "proto-write", "write a skeleton", "scaffold this", or "prototype this".
---

# Proto Write (Skeleton First)

Write the structural skeleton of a feature — file layout, types, function stubs, and wiring — without filling in logic. Goal is to get the shape right fast so implementation can follow.

Read [archi](../references/archi.md) before starting.

## Step 1: Understand the scope

Read the goal or IF doc the user provides. Identify which layers are involved (Objects / Logics / Usecase / External) and what files need to be created or modified.

## Step 2: Write the skeleton

For each file, write stubs only:
- Types and structs with field names but no logic
- Function signatures with `todo!()` / `unimplemented()` / `pass` bodies
- Module structure and imports wired up
- No business logic, no algorithms

Order: inner layers first (Objects → Logics → Usecase → External) so imports resolve top-down.

## Step 3: Verify it compiles

Run the compiler / type checker. The skeleton must compile (or pass type checking) with stubs in place. Fix any structural errors before handing off.

## Step 4: Done

List created/modified files. Tell the user the skeleton is ready for `if-impl` to fill in.
