# Hole TODO Rule

A hole's TODO is written like guidance for a junior developer: clear enough to follow on the first read, using the function's real parameter and return names, naming the general technique, and broken into small numbered steps. The paired test grades whether the human's implementation is correct — the TODO's job is to make sure they know how to get there, not to make them guess the approach.

**Format:**
- No fixed line cap — as many lines as a junior developer needs to follow the steps
- Use the real parameter/return names from the signature — never invented names
- Name the general technique or approach (e.g., "call X then use its result to call Y", "match with a regex", "iterate and accumulate")
- Break the work into small numbered steps
- Include one worked example with concrete values — not abstract placeholders, but different values than the paired test uses, so it clarifies the shape without being a copy-pasteable answer

**Example:**

For the flow-connecting hole inside `execute(self, line: str) -> str:` (paired test uses `"3 + 4"` → `"7"`)
```python
# TODO:
# 1. Call parse_expression(line) to get an Expression.
# 2. Call .evaluate() on that Expression to get the numeric result.
# 3. Convert the result to a string and return it.
# e.g. line="5 - 2" -> parse_expression(line) -> Expression(5, "-", 2)
#      -> .evaluate() -> 3 -> return "3"
```
