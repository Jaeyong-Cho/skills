# Hole TODO Rule

A hole's TODO is written like guidance for a junior developer: clear enough to follow on the first read, using the function's real parameter and return names, naming the general technique, and broken into small numbered steps. The paired test grades whether the human's implementation is correct — the TODO's job is to make sure they know how to get there, not to make them guess the approach.

**Format:**
- No fixed line cap — as many lines as a junior developer needs to follow the steps
- Use the real parameter/return names from the signature — never invented names
- Name the general technique or approach (e.g., "call X then use its result to call Y", "match with a regex", "iterate and accumulate")
- Break the work into small numbered steps
- Include one worked example with concrete values — not abstract placeholders, but different values than the paired test uses, so it clarifies the shape without being a copy-pasteable answer
- Below the TODO comment, write the hole's statement(s) as real code, not omit them — keep the call target, control-flow markers (`?`, `await`, method chaining), statement boundaries, and surrounding structure exactly as they'll be. Blank only the argument list or value that's the actual decision, using the language's inline-comment placeholder (e.g. `/* */` in C-like languages, `...` in Python). This minimizes what the human retypes: they fill in the blanked values using the steps and worked example above, not reconstruct the statement's syntax from scratch.

**Example:**

For the flow-connecting hole inside `execute(self, line: str) -> str:` (paired test uses `"3 + 4"` → `"7"`)
```python
# TODO:
# 1. Call parse_expression(line) to get an Expression.
# 2. Call .evaluate() on that Expression to get the numeric result.
# 3. Convert the result to a string and return it.
# e.g. line="5 - 2" -> parse_expression(line) -> Expression(5, "-", 2)
#      -> .evaluate() -> 3 -> return "3"
return str(parse_expression(/* */).evaluate())
```

A multi-statement hole blanks each statement's decision the same way, one blank per changing value, structure untouched:
```rust
// TODO:
// 1. Call rate(recipe_id, &graph, pack, &mut memo, &mut visiting) to get this
//    node's craft rate.
// 2. Insert (recipe_id.clone(), that rate) into `rates`.
// e.g. recipe_id == "distill" -> rate(..) -> 2.5 -> rates.insert("distill".into(), 2.5)
rate(/* */)?;
rates.insert(/* */);
```
