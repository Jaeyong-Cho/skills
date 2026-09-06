---
name: to-anki
description: Turn requested content — a topic, a notes file, a document, or an explicit Q&A list — into an Anki-importable flashcard CSV. Triggers on "make anki cards for X", "flashcards for X", "to-anki".
---

# To Anki

1. **Gather the source** — read whatever's pointed at (a file, pasted text, a conversation topic). A bare topic name with no attached source is fine — draw on your own knowledge; ask only if the scope is genuinely ambiguous (e.g. "flashcards for Python" — whole language or the file we were just discussing?). Completion criterion: the material to turn into cards is in hand.

2. **Extract atomic facts** — one fact or concept per card, never a compound ("what is X and how does it relate to Y" is two cards, not one). Skip trivia the source doesn't actually emphasize — overproducing low-value cards is the standard flashcard mistake (see `../coding-interview/references/cs-fundamentals.md`'s retention note). Card count follows scope: roughly 10-30 for a single topic, one per distinct fact for a notes file. Completion criterion: every card is a single fact, count matches scope.

3. **Write each card** — Front: short question/prompt. Back: short answer, doesn't restate the question. Code-recall cards may put a short snippet in Back. Keep both fields single-line; join anything multi-line with `; ` instead of a real newline.

4. **Write the CSV** to `./{slug}.anki.csv` (slug from the topic), UTF-8, this exact header block first so Anki's importer auto-detects the format:
   ```
   #separator:Comma
   #html:false
   #columns:Front,Back
   ```
   Then one `Front,Back` row per card. Standard CSV quoting: wrap a field in double quotes if it contains a comma, quote, or semicolon-joined multi-line content; double up any internal `"` as `""`. Completion criterion: file written, every row has exactly 2 fields, quoting applied wherever a field contains a comma or quote — spot check with `grep -c ',' {file}` against the row count if unsure.

5. **Report** the file path and card count, and that it imports via Anki's File > Import (select the CSV; the header block auto-fills separator/columns in modern Anki, or drag-and-drop for newer versions that auto-detect).

Basic Front/Back cards only — no cloze deletions, no tags, no media. Add those only if explicitly requested.
