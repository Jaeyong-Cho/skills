# Bootstrapping a new node

A node with no `AGENTS.md` yet gets one created from this starter, with the accepted edit folded straight into `## Learnings` (never left for a follow-up pass):

```markdown
# {directory name}

Purpose: {one line — what this directory is for}

## Learnings

- {the accepted edit's instruction}

## Maintaining this file

Keep entries short and specific. When an instruction stops mattering, remove it — don't let this file grow forever.
```

Then symlink the pointer so both harnesses see it:

```sh
ln -s AGENTS.md CLAUDE.md
```

Run from inside the node directory, so the symlink target stays a bare relative filename.

If a real (non-symlink) `CLAUDE.md` already exists in that directory, do not overwrite or symlink over it — that's a divergence: two files carrying different content. Flag it to the user and fold the edit into `AGENTS.md` only, leaving `CLAUDE.md` for them to reconcile by hand.
