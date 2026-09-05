# CS Fundamentals Study Plan

Source: [jwasham/coding-interview-university](https://github.com/jwasham/coding-interview-university) (CC BY-SA 4.0) — a full self-taught CS curriculum for interview prep. This file is our own condensed paraphrase of its method and topic order, used as *direction* for sequencing sessions, not a checklist bolted onto the end of a session. Open the linked README's matching section for the actual videos/books/exercises on a topic — don't reproduce them here, and don't work through the upstream repo top-to-bottom as separate homework; pull from it exactly when a gap below is live.

## Method (how a topic gets studied)

- **One topic at a time, then build it** — for each topic, learn just enough to understand it, then implement the underlying data structure or algorithm yourself in code. The goal isn't memorizing every algorithm, it's being able to reconstruct one from understanding.
- **Interleave practice with learning, don't sequence them** — once a topic feels workable (e.g. linked lists), immediately solve 2-3 problems on it, move to the next topic, then circle back for a couple more later. Practicing only after finishing "all the learning" is the single biggest mistake this plan warns against — apply this inside our Problem Workflow: a topic that's still shaky doesn't need a full 5-round deep session, a quick round-1/round-2 pass on 2-3 small problems is enough before moving on.
- **Talk and write it out, not just type it** — narrate requirements, approach, and complexity out loud before coding; draft on paper/whiteboard before a keyboard; state time/space complexity and test cases explicitly. This is what an interview actually evaluates, not just a working answer.
- **Retention needs repetition** — a topic seen once is forgotten; recognizing a flashcard's answer once doesn't count as known, it takes several correct passes. This is the same principle already codified in this skill's `curriculum.md` "Repetition" section (a struggling concept gets retested through a different problem later) — treat that as the spaced-repetition mechanism instead of adopting separate flashcard tooling.
- **Explicitly out of scope for this plan**: JavaScript, HTML/CSS/front-end, SQL — don't pull these into the CS-fundamentals track; they belong to a different curriculum if ever needed.

## Topic order

Work top to bottom; a phase's `curriculum.md` problems interleave with whichever topic is current per the interleaving rule above.

1. Algorithmic complexity / Big-O / asymptotic analysis
2. Data structures — arrays, linked lists, stack, queue, hash table
3. Binary search, bitwise operations
4. Trees — intro, BST, heap/priority queue, balanced trees (concept only), traversals (preorder/inorder/postorder/BFS/DFS)
5. Sorting — selection, insertion, heapsort, quicksort, mergesort
6. Graphs — directed/undirected, adjacency matrix/list, BFS/DFS
7. Recursion, dynamic programming
8. Design patterns
9. Combinatorics (n choose k) & probability
10. NP / NP-complete / approximation algorithms
11. How computers process a program, caches, processes & threads
12. Testing
13. String searching & manipulation, tries
14. Floating point, Unicode, endianness, networking
15. Final review — a pass back over everything above, closing whatever's still shaky before moving to interview simulation

## Getting the job (after the topic order is solid)

Resume, hunting for roles, general interview-process prep, questions to have ready for the interviewer, and what to do once an offer lands. Not curriculum content — pull the relevant upstream section in when the user is actually at that stage, not before.

## Optional (only pull in if the role calls for it — 4+ yrs experience, systems-heavy)

System design & scalability, balanced-tree variants (AVL/red-black/B-trees), compilers, parallel programming, messaging/serialization systems, Bloom filter, disjoint sets/union-find, and the rest of the repo's "Optional Extra Topics & Resources" section.

## Using it in this coach

- **"Start." diagnostic** — after the 5 problems, walk the topic order above once, self-rated comfortable/shaky/unknown; seed `progress/mastery.md` from the shaky/unknown ones instead of guessing, and pick the first current topic from the earliest shaky item, not necessarily item 1.
- **Ongoing sessions** — track the current topic in `progress/mastery.md`'s CS Fundamentals row; each session either advances it (learn + interleaved practice) or does a `curriculum.md` deep-dive problem, per the Method's interleaving rule.
- **Curriculum mapping** — a gap found here maps onto `curriculum.md`'s phases when picking the next deep problem (a Trees/Graphs gap → a Phase 1 problem, a Design Patterns gap → Phase 4) rather than running as a fully separate track.
