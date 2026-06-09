---
name: pf-impl
description: |
  Design and implement a feature in one session using VAO — no ADR written.
  Grills the user to reach a clear VAO design, extracts behaviors, then implements one at a time: write code, assert known unknowns, log unexpected states, run and observe.
  Use when the user wants to think through a design and implement immediately without writing a formal ADR.
  Triggers: "pf-impl", "design and implement", "think through and build", "quick impl", "no ADR just implement", "implement this".
---

For layer definitions read `../pf/references/layers.md`.

# VAO Design + Implement (No ADR)

Design direction: **Value → Aspect → Object** (iterative in practice).

## Step 1: Grill the design

Read `../pf/references/deep-modules.md`, `../pf/references/layers.md`.

Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: reach a clear VAO design before implementing. Starting context: the user's scenario.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead. When referencing source code, show the relevant snippet inline with `file:line` header before asking.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

## Step 2: Extract behavior list

From grill conclusions derive and show:

```
Behavior list:
1. <tracer bullet behavior>    [value]
2. <next behavior>             [aspect]
3. <next behavior>             [object]
```

Ask via `AskUserQuestion`: "Ready to implement?" — adjust list if needed.

## Step 3: Implement — one behavior at a time

Read `../pf-observe/REFERENCE.md` for logging rules before implementing. Follow its conventions for log levels, CLI flags, and output format.

For each behavior:
1. **Write the implementation** — minimal code that satisfies the behavior
2. **Assert known unknowns** — for every invariant that must hold, add an assertion inline. If it fires, something is wrong.
3. **Log unexpected states** — for states that shouldn't happen but aren't fatal, add an error log with enough context (inputs, state) to diagnose without a debugger
4. **Dump useful data** — log key inputs, outputs, and state changes per pf-observe conventions
5. **Run and observe** — execute the code, confirm assertions don't fire, confirm logs show expected data

Do not move to the next behavior until the current one runs cleanly.

## Step 4: Refactor (after all behaviors run cleanly)

Read `../pf/references/deep-modules.md`.

- [ ] Interface narrowable?
- [ ] Complexity hidden or exposed?
- [ ] Duplication to extract?

**Observability checklist** (see `../pf-observe/REFERENCE.md` for patterns and CLI flag conventions):
- [ ] Logs key inputs, outputs, and state changes at appropriate level?
- [ ] Logs environment info (runtime version, env name, config values) on startup or entry?
- [ ] Logs dependency versions where relevant?
- [ ] Writes important runtime state to a file (structured log, snapshot, or output file) for later inspection?
- [ ] Errors include enough context (input values, state) to diagnose without a debugger?
- [ ] Existing `observe/` scripts still compatible? (`ls observe/ 2>/dev/null` — check each script still targets valid paths, interfaces, and output formats)

Run the code after each refactor step and confirm assertions still pass and logs still look correct.

## Step 5: Done

Show summary of what was built. Suggest commit message using `../pf/references/commit.md`.
