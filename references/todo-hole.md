# Hole TODO Rule

A hole's TODO is written like guidance for a junior developer: clear enough to follow on the first read, using the function's real parameter and return names. The paired test grades whether the human's implementation is correct — the TODO's job is to make sure they know how to get there, not to make them guess the approach.

What matters most is the input → output contract: given these values, what should come out. For most holes — especially the flow-connecting kind — that's really an interaction: how one call's output becomes the next call's input. The worked example should trace that chain (this input → this call → its result → the next call → the final output), not just state the hole's overall input and final output as a black box. Naming the technique and numbering the steps are secondary — a hint at how, for whoever wants it — not a substitute for tracing the chain.

Aim to keep the target language's grammar off the human's plate — syntax is already working code around the blank, and what's left to supply is meaning: which values, which call, what result. This is a guideline for where to put the blank, not a strict rule; some holes (e.g. the in-stage key-change kind) are naturally more about the shape of the code than a single value, and that's fine.

**Format:**
- Include one worked example with concrete values — not abstract placeholders, but different values than the paired test uses, so it clarifies the shape without being a copy-pasteable answer. Trace it as a chain, each call's result feeding the next (`input -> call -> result -> next call -> final output`), not just the hole's start and end values. This is the core of the TODO; get this right first.
- Use the real parameter/return names from the signature — never invented names
- Name the general technique or approach and break the work into small numbered steps (e.g., "call X then use its result to call Y", "match with a regex", "iterate and accumulate") — secondary support for the worked example above, not a replacement for it. No fixed line cap, but keep it as short as the input → output already makes clear.
- Below the TODO comment, write the hole's statement(s) as real code, not omit them — keep the call target, control-flow markers (`?`, `await`, method chaining), statement boundaries, and surrounding structure exactly as they'll be where it's natural to do so. Blank the argument list or value that's the actual decision, using the language's inline-comment placeholder (e.g. `/* */` in C-like languages, `...` in Python). Prefer a blank fillable by meaning alone (a value or name from the worked example above) over one that also asks the human to work out syntax — but use judgment: widen the blank to cover more of the statement when the hole is more about shape than a single value.

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
