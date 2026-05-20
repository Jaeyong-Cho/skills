# Commit Message Format

After each session, show user recommended commit message:

```
<type>(pf): <short description>

Why: <what value or goal this addresses>
What: <what entities or artifacts were created or changed>
How: <what method or approach was applied>
```

`<type>`: `feat` (new design/impl/review/docs), `refact` (refactoring plan), `fix` (correction to existing content).

Subject line should name specific artifact produced, e.g.:

```
feat(pf): add design 0001 auth-flow
fix(pf): correct entity relationships in 0002-payment
refact(pf): simplify checkout workflow in 0003
```
