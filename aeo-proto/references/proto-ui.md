# UI Prototype

Use when the question is about **layout, interaction, or visual design direction**.

Generate several radically different UI variations switchable via a floating bottom bar — compare approaches and steal the best bits before discarding the rest.

## Two paths

**Preferred — existing route:** Render variants on an existing route using `?variant=` URL params. Preserves real data, auth, and context. Surfaces genuine design constraints.

**Fallback — new route:** For entirely new surfaces without a natural host page, create a throwaway route clearly marked as a prototype, following the project's routing conventions.

## Steps

1. **Define scope** — default to three variants max; document the plan in one line
2. **Draft structurally distinct variants** — each must differ fundamentally (layout, hierarchy, affordances), not cosmetically
3. **Create a switcher component** — conditionally render variants based on search params
4. **Build a floating control bar** — fixed bottom-center, arrow navigation, variant label, keyboard support, gated from production builds
5. **Let the user evaluate** — share the URL for comparison and feedback
6. **Consolidate** — after selection, promote the winner and delete all prototype scaffolding

## Rules

- Each variant must stand independently
- No mutations wired into read-only prototypes
- Never ship prototype scaffolding to production
- Variants must be structurally distinct — cosmetic-only variants waste time
