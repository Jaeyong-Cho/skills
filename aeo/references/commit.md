# Commit Message Format

After each session, show the user a recommended commit message:

```
<type>(aeo): <short description>

Why: <what value or goal this addresses>
What: <what entities or artifacts were created or changed>
How: <what method or approach was applied>
```

`<type>`: `feat` (new design/impl/review/docs), `refact` (refactoring plan), `fix` (correction to existing content).

The subject line should name the specific artifact produced, e.g.:

```
feat(aeo): add design 0001 auth-flow
fix(aeo): correct entity relationships in 0002-payment
refact(aeo): simplify checkout workflow in 0003
```
