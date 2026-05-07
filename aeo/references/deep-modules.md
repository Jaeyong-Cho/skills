# Deep Modules

From "A Philosophy of Software Design":

**Deep module** = small interface + lots of implementation

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid)

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing interfaces, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Design Smells (shallow module signs)

| Smell | What to look for |
|---|---|
| **Shallow module** | Interface nearly as wide as the implementation — many tiny methods |
| **Duplicated logic** | Same rule or algorithm in more than one place |
| **Information leakage** | Same knowledge scattered across call sites instead of owned by one module |
| **Temporal decomposition** | Split by execution order rather than responsibility |
| **Pass-through method** | A function that just calls another with the same arguments |
| **Leaky interface** | Callers must know internal details to use the module correctly |
| **Conjoined twins** | Two modules always edited together — should probably be one |
