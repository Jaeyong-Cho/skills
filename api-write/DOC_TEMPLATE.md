# <ApiName>

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

> Rule: may only reference APIs at the **same or inner layer** (Objects→Logics→Usecase→Interfaces). No upward references. See [archi](../references/archi.md).

- `OtherApi.method()` — [layer: objects] used for ...

## Usage Examples

```ts
// example showing typical call
```

## Testing Strategy

- **Unit**: ...
- **Integration**: ...
- **Mocks**: ...
