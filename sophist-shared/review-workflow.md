# Review Workflow: Steps 1–4 (Shared)

Used by sophist-srs, sophist-sad, sophist-sdd. Replace `{LAYER}` and `{dir}` with the layer name and directory path when reading these steps in context.

---

## Step 1: Find all draft items

```bash
grep -rl "^\`draft\`" .sophist/src/{dir}/
```

Read each draft item file.

For each item, determine its status:

- **Answered**: the `### Review needed` section has been removed, or it contains a `#### Answer` subsection added by the human
- **Pending**: the `### Review needed` header is present with only the original question — no `#### Answer` subsection yet

---

## Step 2: Show pending review points

List every pending item so the human knows what still needs their attention. If there are no pending items, note that and move to Step 3.

---

## Step 3: Apply inline answers to answered items

For each answered item:

**If the section contains a `#### Answer` subsection:**
- Read the content under `#### Answer`
- Incorporate it into the relevant content field (see layer-specific notes below)
- Remove the entire `### Review needed` section (including the `#### Answer` subsection)

**If the section has been removed entirely:**
- Accept the current file content as the human's approved version
- No content change needed

The goal is that each item accurately reflects the human's intent. Rewrite clearly — don't just append. If there were multiple questions and only some have `#### Answer` subsections, apply those and leave the unanswered questions in place as a fresh `### Review needed` section.

---

## Step 4: Mark answered items as `reviewed`

For each item where all review points are now resolved:

Change `## State` from `` `draft` `` to `` `reviewed` ``.

---

## Layer-specific notes

### SRS (sophist-srs)
- Step 3: Incorporate the answer by rewriting the sentence or value the review question was about.

### SAD (sophist-sad)
- Step 3: Update Interface, Location, Responsibility, Dependencies, or Diagram section as appropriate.
- Step 3: When the answer changes the component's interface or responsibility, also check whether the component diagram (mermaid) needs updating — keep the diagram in sync with the text.
- Step 3: **Mermaid syntax safety** — Use `<br/>` for line breaks (not `\n`, which renders literally). Quote any label containing `[`, `]`, `(`, `)`, `{`, `}`, or `:` using `["..."]` syntax — bare brackets break the parser.
- Step 3: When an answer reshapes a component's interface, evaluate it against Deep Module principles (Ousterhout, *A Philosophy of Software Design*): does the revised interface hide more complexity than before, or does it leak internal details to callers? If the answer pushes complexity outward (more parameters, more caller knowledge required, narrower purpose), flag a review point asking whether the complexity can be absorbed into the component instead.

### SDD (sophist-sdd)
- Step 3: Incorporate into Signature, Algorithm, Variables, Error cases, or Side effects.
- Step 3: When an answer changes an algorithm step, rewrite that specific step clearly. When it changes an error case or side effect, update those sections. Keep the algorithm numbered and concrete — the SDD must remain implementable without guessing after your edits.
- Step 3: If an answer reveals that the algorithm is more complex than first written, update the algorithm steps, variables, and side effects to reflect that accurately.
