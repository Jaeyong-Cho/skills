# <IfName>

**Purpose**: [one-line description]

## Public Methods

### `methodName(param: Type, ...): ReturnType`

**Description**: ...
**Parameters**:
- `param` — ...

**Returns**: ...
**Errors**: ...
**Algorithm**: ...

## CLI Interface

### `<command> <subcommand> [flags]`

**Description**: ...
**Flags**:
- `--flag` — ...

## UI Entry Points

### `<ComponentName>`

**Description**: ...
**Props / Handlers**: ...

## Dependencies

> Rule: may only reference IFs at the **same or inner layer** (Objects→Logics→Usecase→External). No upward references. See [archi](../references/archi.md).

- `OtherIf.method()` — [layer: objects] used for ...

## Usage Examples

```ts
// example showing typical call
```

## Testing Strategy

- **Unit**: ...
- **Integration**: ...
- **Mocks**: ...
