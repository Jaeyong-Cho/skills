---
name: psos
description: Tag a day's markdown journal with the PSOS operator that ran and the state it updated. Use when invoked as /psos.
disable-model-invocation: true
---

# PSOS

Annotates a journal entry in place, sentence by sentence, with which of the
four core-loop operators fired and which state it produced — turning a day's
writing into a traceable state history. Full model:
`~/workspace/5-cubed/psos/framework.md` (§5–6 for the core loop, §12.5 open
question on Requirement).

## The core loop

| Operator | Signature | Marks a clause where... |
|---|---|---|
| **Sense** | World → Understanding | you noticed, read, measured, or learned some fact |
| **Feel** | Understanding → Goal | a discrepancy turned into something you now want |
| **Plan** | Understanding + Goal → Solution | you decided or wrote down what to do |
| **Execute** | Solution → World′ | you actually did it, changing reality |

A checklist item (`- [ ]` / `- [O]` / `- [x]`) is already a Solution by
construction — its creation was a past Plan, not this run's event. Only a
checked item marks a new event: Execute.

## Steps

1. Resolve the target file: an explicit path if given; otherwise a bare date
   resolves to `~/wiki/journal/{year}/{date}.md`; no argument at all means
   today's file at that path. Read it.
2. Walk the file top to bottom. Each list item and each clause of paragraph
   text is a candidate event — judge by meaning, not punctuation, since
   entries mix languages and run clauses together on commas.
3. Skip any clause whose line already contains a `` `[Operator → State: ...]` ``
   tag — it was classified on a previous run.
4. For every remaining clause that depicts a discrete event (per the table
   above, or a checked checklist item), append a tag to the end of its line:
   `` `[Operator → State: gloss]` ``, gloss being a 2–6 word summary of the
   state's new content. Pure context, color, or an unchecked checklist item
   gets no tag.
5. Write the file back with only these tags inserted — no other text changes.

Completion criterion: every list item and every clause in the file has been
judged event-or-not, with no line skipped except those already tagged.

Report the file path and a per-operator count of newly added tags.
