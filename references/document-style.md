# Document Style
Write in a clear, concise, and professional report style. Prefer structured, visual representations over prose — reading structured output is faster than reading paragraphs.

## Priority order (use the highest tier that fits the content)
1. **Structured** (diagram or table) — highest preference
2. **Concise bullets**
3. **Detailed prose**
4. **Free text** — lowest preference, avoid unless nothing else fits

## Which structured form to use
- **Flow, pipeline, dependency, or stage-to-stage content** (e.g. requirement → design → implementation, a data/control flow, a decision sequence) → ASCII tree/flow diagram, plain ASCII characters only (`|`, `v`, `+--`, `->`). No Unicode box-drawing or arrow glyphs — plain ASCII renders correctly everywhere.
- **Comparison content** (options, trade-offs, parallel attributes, before/after) → Markdown table.
- **List-like content with no flow or comparison shape** → bullets (tier 2), per the rules below.
- Short edge/node labels (roughly 4 words or fewer) go inline on the arrow; longer explanations drop to a numbered/bulleted legend below the diagram.

## Bullet rules (when bullets are the right tier)
- Default to bullet + sub-bullet structure over paragraphs. Use paragraphs only for a short lead-in sentence when a section truly needs one.
- One idea per bullet. If a bullet needs "and" to join two claims, split it.
- Push detail, evidence, and caveats into sub-bullets nested under the claim they support, instead of writing them inline.
- Place key information first: lead each bullet with the finding, number, change, risk, or issue, not the context.
- Avoid long or complex sentence structures within a bullet.
- Use transition words (e.g., Therefore, However, In addition, As a result) only where logical flow isn't already clear from bullet nesting.

## Report structure
- Introduction: objective, background, scope, and methodology as bullets.
- Body: facts, analysis, findings, and supporting evidence — diagrams/tables for flow and comparison content, bullets with sub-bullets for everything else.
- Conclusion: key takeaways, insights, recommendations, and next actions, each as its own bullet.

## General
- Prioritize clarity over stylistic or decorative writing.
- Use direct, objective, and business-oriented language.
- Present conclusions and recommendations explicitly as bullets rather than implying them in prose.

## Restricted content
- Never write secrets or credentials into the document: API keys, tokens, passwords, private keys, connection strings.
- Never write personal information: usernames, real names, emails, phone numbers, addresses, or other personally identifiable information.
- If such data appears in source material, redact it (e.g., `[REDACTED]`) or refer to it abstractly (e.g., "the API key") instead of quoting the value.
