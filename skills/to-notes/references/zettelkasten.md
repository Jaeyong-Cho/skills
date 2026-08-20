# Zettelkasten Theory

Background for `to-notes`' design — why three note types, why linking instead of categories, why own-words is non-negotiable. Read this when a judgment call isn't spelled out in `SKILL.md` itself; the day-to-day steps don't need it.

## Origin

The method comes from sociologist Niklas Luhmann, who kept a paper slip-box (*Zettelkasten*, German for "slip box") of roughly 90,000 index cards over his career and credited it, not raw output, for his unusual productivity — he described it as a conversation partner, not an archive. Luhmann numbered each card with an addressable, branching ID (`21`, `21a`, `21a1`...) so a new card could be inserted physically next to a related one without renumbering everything else. Sönke Ahrens' *How to Take Smart Notes* later distilled the method into the three-note-type workflow most digital tools (and this skill) now follow.

`to-notes` keeps the three-type workflow and the linking discipline, and drops the numeric addressing — a filesystem plus `grep`/relative links gives free-form addressing (any note can link any other) without needing an insertion scheme designed for paper.

## The three note types, and why they're separate

- **Fleeting notes** are a rough jot of a sudden thought or something learned — they exist because that thought or fact loses value if capturing it takes any real effort, so fleeting notes have no format requirements at all. They are explicitly disposable: reviewed within a day or two and either promoted into something durable or discarded. A fleeting-notes pile that keeps growing has failed at its one job.
- **Literature notes** exist because a source's ideas need to be translated into your own understanding before they're reusable — copying a passage verbatim preserves the source's words, not your comprehension of it. One note per source keeps that translation anchored to what it came from.
- **Permanent notes** are not freestanding — each one is a fleeting or literature note *refined*: reworked until it's atomic, until it stands alone with zero context, and until it's linked to what else it relates to. An idea only compounds in value once it's gone through that refining and reconnection; that's what "atomic," "own words," and the mandatory `## Links` are each enforcing a piece of.

Skipping straight to permanent notes without the first two stages tends to produce notes that are really just relocated fleeting thoughts or paraphrased source material — atomic in form but not actually distilled. The friction of passing through fleeting/literature first is what does the distilling.

## Why linking beats categorizing

A category tree forces every note into exactly one place, decided at write time, before you know what else will eventually relate to it. A link-only structure lets a note belong to as many contexts as turn out to matter, decided incrementally as each new note is written. Structure *emerges* from the accumulated links rather than being imposed upfront — this is why `to-notes`' permanent notes stay flat (`~/wiki/notes/permanent/*.md`) until sheer volume makes flat browsing impractical, and even then, categories are a browsing aid layered on top of the link graph, not a replacement for it. The links keep working across a category split; the categories don't do the connecting.

## Where new ideas actually come from

The often-cited payoff of a working slip-box isn't storage, it's collision: browsing from one permanent note to its links surfaces a second note you weren't looking for, and holding both in view at once suggests a third idea neither one stated alone. This only works if notes are densely and honestly linked — a permanent note with no links can't participate in this at all, which is why `to-notes` treats a link-less permanent note as a smell rather than a style nit. `to-notes`' Promote step is a deliberate version of this: reading fleeting/literature notes together, on purpose, looking for exactly this kind of unplanned connection.

## What's deliberately not adopted here

- **Luhmann's numeric addressing** — superseded by filesystem links; nothing is gained by re-deriving it digitally.
- **A fixed top-level taxonomy** — the whole point of the method is that structure isn't decided upfront; `to-notes`' category split is a threshold-triggered browsing aid, not a taxonomy design step.
- **Tool-specific features** (backlink panels, graph views, spaced repetition) — genuinely useful in a dedicated app, out of scope for a set of markdown files and an agent.
