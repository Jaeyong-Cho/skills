# Verification Design

Choose the narrowest executable check that can falsify the cycle's current assumption.

## Cost order

Use only the needed prefix of this ladder:

```text
static/deterministic
→ targeted unit
→ targeted component
→ targeted integration
→ representative path
→ broader regression
→ E2E/full test
```

A cycle stops when its question is answered with sufficient evidence. E2E and full tests are final confidence gates, never ordinary first feedback.

## Useful checks

- **Behavior:** valid and invalid input, focused regression, integration result, or representative path.
- **API / CLI:** required or forbidden entry point, signature, option, default, exit status, or compatibility.
- **Structure:** required class/module placement, interface, ownership, visibility, or dependency direction.
- **Architecture:** only the few boundaries whose violation would materially damage the design.

Every check exposes its expected state, actual state, and useful evidence on failure. Prefer deterministic inputs and outputs.

## Final confidence

Only use E2E or a full test after cheaper required evidence passes. If it is part of a cycle, it must be the last numbered script. A long full test also needs the cycle README's budget and both required justifications; being broad is not a justification.
