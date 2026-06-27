# Global Instructions

## Sot Knowledge Base

The sot system is a local RAG knowledge base at `~/sot/` that stores project intent, design rationale, constraints, and preferences.

**When you need context** (ambiguous request, unknown constraints, unfamiliar domain):
1. Run `sot search-cmd "<query>" --k 5` to retrieve relevant chunks.
2. Use the returned chunks to ground your answer. If the index is missing, fall back to reading `~/sot/wiki/` files directly.

**When new knowledge should be persisted** (new decision made, constraint clarified, preference expressed):
1. Write or update `~/sot/wiki/<topic>.md` with the new information.
2. Re-index with `sot index ~/sot` so it becomes searchable.

Use search proactively — don't wait for the user to ask. If a task involves design decisions, project structure, or coding style and you're unsure, search first.
