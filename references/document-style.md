# Document & Communication Style

Basically write document with three phase

**Introduction**: 1-3 sentence short description to explain why, what
**Abstraction**: Abstraction is a model consisted of object and their interactions, relationships, categories
**Detailed**: Detailed description is a representative detailed example for about the model

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
