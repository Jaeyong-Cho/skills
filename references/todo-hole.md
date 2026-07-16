# Hole TODO Rule

A hole's TODO is a transformation spec, not an explanation. State only what goes in and what comes out, using the function's real parameter and return names — no rationale, no hint at the operation category or technique. The human should have to think to fill it; the paired test grades whether they got it right.

**Format:**
- ≤2 lines
- Use the real parameter/return names from the signature — never invented names
- Include one abstracted example: the *shape* of the transformation, not a worked concrete value
- No "why this matters" reasoning
- No operation-category or technique hint (not "split", not "use regex", not "orchestrate")

**Examples:**

For `def parse_expression(line: str) -> Expression:`
```python
# TODO: Turn `line` (shape: "<left> <operator> <right>") into
# Expression(left, operator, right).
```

For an orchestration hole inside `execute(self, line: str) -> str:`
```python
# TODO: Turn `line` into the value this method returns.
```
