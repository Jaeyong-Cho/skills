# Hole TODO Rule

A hole's TODO is a transformation spec, not an explanation. State only what goes in and what comes out, using the function's real parameter and return names — no rationale, no hint at the operation category or technique. The human should have to think to fill it; the paired test grades whether they got it right.

**Format:**
- ≤2 lines
- Use the real parameter/return names from the signature — never invented names
- Include one worked example with concrete values — not abstract placeholders, but different values than the paired test uses, so it clarifies the shape without being a copy-pasteable answer
- No "why this matters" reasoning
- No operation-category or technique hint (not "split", not "use regex", not "orchestrate")

**Examples:**

For `def parse_expression(line: str) -> Expression:` (paired test uses `"3 + 4"`)
```python
# TODO: Turn `line` (e.g. "5 - 2") into
# Expression(5, "-", 2).
```

For an orchestration hole inside `execute(self, line: str) -> str:` (paired test uses `"3 + 4"` → `"7"`)
```python
# TODO: Turn `line` (e.g. "5 - 2") into the value this method
# returns (e.g. "3").
```
