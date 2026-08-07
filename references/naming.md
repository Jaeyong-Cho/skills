# Naming

A name is intention-revealing when the reader needs nothing but the name to know why it exists, what it does, and how it's used.

## Smells

| Smell | What to look for |
|---|---|
| Disinformative name | Name implies something the thing isn't (`accountList` that's actually a `Set`) |
| Noise word | Suffix/prefix adds no meaning (`data`, `info`, `obj`, `Impl`, a `Manager` with no distinct role) |
| Un-searchable name | Single letter or number outside a tiny loop scope |
| Encoded name | Hungarian/type/scope prefix the language already tracks (`strName`, `m_count`) |
| Mismatched part of speech | A class named as a verb, a method named as a noun |
| Synonym drift | The same operation called `get`/`fetch`/`retrieve` in different places |
| Mental-mapping name | Reader must remember what `x` "really" means; no name says it directly |
