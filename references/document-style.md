# Document & Communication Style

Basically write document with three phase (Introduction -> Abstraction -> Detailed)

**Introduction**: 1-3 sentence short description to explain why, what
**Abstraction**: Abstraction is a model consisted of object and their interactions, relationships, categories
**Detailed**: Detailed description is a representative detailed example for about the model

applies_to: chat responses, explanations, plans, `AskUserQuestion` text, standalone docs (README, design docs, reports)
narrowed: commit messages & PR descriptions -> bullets only, no diagrams (shared history, collaborators' own conventions)
excludes: code comments (see minimal-comment rule)

## priority
1. key-value — attributes, config, or facts about a single subject
2. table — comparison across options/subjects
3. bullets — concise, one idea each
4. prose — detailed, only when needed
5. free text — avoid unless nothing else fits

ascii_diagram: not part of the ranked priority — use only if needed, i.e. content is genuinely a flow/pipeline/hierarchy that a diagram reads faster than any tier above.

floor: a single fact, yes/no answer, or one-item confirmation stays plain text — don't force structure on it.

## ascii_diagram
- chars: only `|` `v` `+--` `->`
- avoid: arrows (`→` `⇒` `➜`), box-drawing (`─` `│` `┌` `└` `├` `┬`), bullet glyphs (`•` `▪`)
- fence: always ` ```text ` (never bare ` ``` `) — stops renderers from syntax-highlighting or reflowing the layout
- caption: one sentence stating what the diagram depicts, placed directly above or below it
- labels: inline on the arrow if <=4 words; longer explanations go to a numbered/bulleted legend below

**MUST NOT** make the document size over then below
- Sentence: 15 word
- Paragraph: 50 word
- Key message: 1-3 sentence
- Section: 200 word (almost)
- File: 500 word (almost)

**MUST** Split the file if the size over then below
