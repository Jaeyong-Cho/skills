# UI Prototype

Six rules in `SKILL.md` Step 2 apply to all prototypes. This file adds UI-specific guidance.

Use when question is about **layout, interaction, or visual design direction**.

Generate several radically different UI variations switchable via floating bottom bar — compare approaches and steal best bits before discarding rest.

## Two paths

**Preferred — existing route:** Render variants on existing route using `?variant=` URL params. Preserves real data, auth, and context. Surfaces genuine design constraints.

**Fallback — new route:** For entirely new surfaces without natural host page, create throwaway route clearly marked as prototype, following project's routing conventions.

## Steps

1. **Define scope** — default to three variants max; document plan in one line
2. **Draft structurally distinct variants** — each must differ fundamentally (layout, hierarchy, affordances), not cosmetically
3. **Create switcher component** — conditionally render variants based on search params
4. **Build floating control bar** — fixed bottom-center, arrow navigation, variant label, keyboard support, gated from production builds
5. **Let user evaluate** — share URL for comparison and feedback
6. **Consolidate** — after selection, promote winner and delete all prototype scaffolding

## Rules

- Each variant must stand independently
- No mutations wired into read-only prototypes
- Never ship prototype scaffolding to production
- Variants must be structurally distinct — cosmetic-only variants waste time
