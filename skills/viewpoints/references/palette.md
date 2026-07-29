# Palette — token-light theme

Derived from the [`token`](https://github.com/ThorstenRhau/token) Neovim colorscheme's light variant, for styling every chart `viewpoints` renders.

## How to use these values

Everything below is plain hex. In an HTML chart, define the slots you use as CSS custom properties in a local `<style>` block, then reference them by role throughout, so the chart body is written against roles rather than raw hex:

```css
.viz-root {
  --surface:        #faf9f5;
  --text-primary:   #2a2920;
  --text-secondary: #6c675f;
  --series-1:       #856c02;   /* categorical slot 1 */
  /* …only the roles this chart uses */
}
```

For non-HTML plotting libraries, set the equivalent theme/rcParams (figure background, text color, color cycle) to the same hex values.

**Scope: light mode only.** token's dark-theme syntax hues sit at OKLCH lightness 0.65–0.75, too light to give the same separation between colors that the light set achieves — so they aren't used here as dark-mode data-mark colors. Dark **chrome** (surface/ink/gridlines below) is included and safe to use; for dark-mode data marks, fall back to any sensible default dark categorical set until token-dark is derived.

## Derivation

token's 8 syntax hues (blue, green, red, yellow, purple, cyan, orange, olive) are built for code-comment legibility on a specific background, not for standing apart from each other as chart marks — most were too desaturated to stay distinguishable once colorblind vision is simulated (protanopia/deuteranopia), especially side by side in a legend. Each was re-saturated at the same hue angle — and, for yellow and cyan, at a lightness where that extra saturation is reachable in sRGB — checked in OKLab against simulated colorblind vision and normal vision to confirm neighbors stay tellable apart, and checked for contrast against the chart surface. Slot order and the all-pairs cap below were chosen by comparing every ordering of the 8 hues against those checks and keeping the best.

## Categorical palette (light)

| Slot | Name | Hex |
|------|------|-----|
| 1 | yellow | `#856c02` |
| 2 | blue | `#2876b2` |
| 3 | orange | `#9f5c0b` |
| 4 | cyan | `#00a2a3` |
| 5 | red | `#b05555` |
| 6 | green | `#296926` |
| 7 | purple | `#805ba7` |
| 8 | olive | `#617613` |

For white vs. dark-ink (`#2a2920`) text set *on* one of these slots as a fill (legend chips, tags) rather than the slot used as a mark on the surface: white wins on every slot except 4 (cyan), where dark ink wins.

This order clears the hard gates for **adjacent** use (stacks/bars/lines): worst adjacent CVD ΔE 6.1 (protan/deutan — floor band, 6–8, ship secondary encoding: direct labels, gaps, or texture) — worst adjacent normal-vision ΔE 22.4 (≥15 floor, pass). Slot 4 (cyan `#00a2a3`) sits at 2.98:1 on the light surface, just under the 3:1 relief threshold — ship a visible label or the table view whenever it's used, per the relief rule.

**All-pairs cap (scatter, bubble, choropleth, small multiples):** the full 8 do not clear all-pairs CVD separation at any 4-color subset — token's hues crowd into the warm range (red/orange/yellow/olive), leaving too little distance between any four once every pair, not just neighbors, can land side by side. The one 3-color subset that clears every gate cleanly is **green `#296926`, purple `#805ba7`, cyan `#00a2a3`** (all-pairs CVD ΔE 12.1, normal ΔE 20.9 — both pass, no relief needed). Use this triad, in this order, for all-pairs contexts; past 3 series, fold to "Other," facet, or label directly.

## Sequential hue

Base hue: slot 1 (yellow). 13-step ramp, light→dark, lightness stepping roughly evenly from near-white to near-black while chroma rises through the mid steps and eases off at both ends — the shape that keeps every step visually distinct without any reading as pure gray:

| step | hex | step | hex | step | hex | step | hex |
|---|---|---|---|---|---|---|---|
| 100 | `#e9e0c2` | 250 | `#c8b168` | 400 | `#a18409` | 550 | `#715b05` |
| 150 | `#ddd0a6` | 300 | `#bda142` | 450 | `#917607` | 600 | `#614f04` |
| 200 | `#d3c186` | 350 | `#b3920a` | 500 | `#806806` | 650 | `#524203` |
| | | | | | | 700 | `#443602` |

For a second simultaneous sequential context, use slot 2's hue (blue `#2876b2`) as its own one-hue ramp, built the same way.

## Diverging pair

**blue ↔ red** (slots 2 and 5), 3 steps per arm plus a neutral midpoint:

| | 3 (outer) | 2 | 1 (inner) | neutral | 1 (inner) | 2 | 3 (outer) |
|---|---|---|---|---|---|---|---|
| hex | `#035183` | `#378ccf` | `#98bcdc` | `#ecebe7` | `#dba9a6` | `#c86363` | `#822b2e` |

Neutral midpoint is token's `bg1` (light `#ecebe7`); the dark-mode neutral, if needed for chrome, is token's `bg5` dark (`#383835`).

## Status palette (fixed — never themed)

good `#0ca30c`, warning `#fab219`, serious `#ec835a`, critical `#d03b3b`. Keep these fixed regardless of theme, so a status color never collides with, or gets mistaken for, one of the eight categorical slots above.

## Chart chrome & ink

| Role | Light | Dark |
|---|---|---|
| Chart surface | `#faf9f5` (bg3) | `#262624` (bg3) |
| Page plane | `#f6f5f1` (bg2) | `#191918` (bg0) |
| Primary ink | `#2a2920` (fg0) | `#e8e4dc` (fg0) |
| Secondary ink | `#6c675f` (fg2) | `#938e87` (fg2) |
| Muted (axis/labels) | `#858179` (fg3) | `#5a5955` (fg3) |
| Gridline (hairline) | `#e0ddd8` (indent) | `#333330` (indent) |
| Baseline / axis | `#a8a49c` (indent_active) | `#636360` (indent_active) |
| Delta ↑ good (success text) | `#24831f` (gsign_add) | `#7da47a` (gsign_add) |
| Border (hairline ring) | `rgba(42,41,32,0.10)` | `rgba(232,228,220,0.10)` |

## Surfaces

- Light chart surface: `#faf9f5`
- Dark chart surface: `#262624`

If the categorical set above is ever re-derived or extended, re-check contrast against these surfaces, and re-check CVD/normal-vision separation between every pair that can appear together.
