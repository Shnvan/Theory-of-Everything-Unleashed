# HUD and UI Specification

**Status:** the instance contract is LOCKED because code already depends on it. Layout numbers are DEFAULT and expected to change through device testing.

**Why this document exists.** `src/shared/Config/InputConfig.luau` resolves ten touch buttons by exact name inside the Studio place. Those names were previously written nowhere but in the code. Because [STUDIO_IDE_WORKFLOW.md](STUDIO_IDE_WORKFLOW.md) bars non-script instances from synced folders, the GUI cannot be checked into git as instances — so the only place the contract can live is a document. Rename or delete any instance below and mobile input degrades to `warn()` lines at runtime with no compile-time signal at all. Recorded as D-022.

> **VERIFIED 2026-07-25.** The tree below was compared against the live private prototype place over Studio MCP and matches exactly: `GameHUD` is a `ScreenGui` under `StarterGui`, `TouchControls` is a `Frame` under it, and all ten buttons are `TextButton` direct children with the exact names below. Neither side needed correction. The place additionally carries per-button `UICorner`/`UIStroke`/`UITextSizeConstraint` styling children and two `GameHUD` attributes (`TouchButtonCount = 10`, `InputLayoutRevision = "M1InputMappingV1"`); none participate in the lookup, and this document does not govern them.
>
> Re-verify if the HUD is rebuilt. What this check does **not** cover is runtime: the place has not been played since the M0.5 input fixes, so no `InputController` warning path has actually executed.

---

## Required instance tree

Exact names. Exact classes. Anything else breaks the lookup.

```text
StarterGui
  GameHUD                      ScreenGui
    TouchControls              Frame        -- visibility driven by UserInputService.TouchEnabled
      BasicAttackButton        GuiButton    -- ImageButton or TextButton
      Ability1Button           GuiButton
      Ability2Button           GuiButton
      Ability3Button           GuiButton
      Ability4Button           GuiButton
      BlockButton              GuiButton    -- hold
      DashButton               GuiButton
      MechanicButton           GuiButton
      BreakthroughButton       GuiButton
```

**Nine buttons, not ten.** `SprintButton` was removed by **D-028**: sprinting is automatic at full movement input, so there is nothing for a sprint button to request. `Walk` replaced `Sprint` in the action set and deliberately has **no** touch button — an analogue thumbstick pushed part-way already walks, while a keyboard needs `Shift` because `W` is binary.

That is why `touchButtonName` is **optional** in `InputConfig.ActionDefinition`. An action without one never enters `DEFINITION_BY_TOUCH_BUTTON`, so the input layer never hunts for a GuiButton this document does not list — which is what would otherwise produce a `warn()` every session.

Contract rules:

- `GameHUD` must be a **ScreenGui** and a direct child of `PlayerGui` at runtime. The code type-checks this and bails if it is wrong.
- `TouchControls` must be a **Frame** and a direct child of `GameHUD`.
- Each button must be a **GuiButton** subclass and a direct child of `TouchControls`. Nesting a button inside a container frame breaks `FindFirstChild`.
- Missing buttons degrade individually: the code warns for that one button and continues. Missing `GameHUD` or `TouchControls` disables touch entirely and leaves desktop input working.
- `TouchControls.Visible` is owned by `InputController`. Do not drive it from anywhere else.

**To add an action:** add it to `ACTION_DEFINITIONS` in `src/shared/Config/InputConfig.luau`, add its button here, and create the instance in Studio. All three, or it is broken in one of three ways.

---

## Visual language

**Status:** the achromatic-and-wordless rule is LOCKED by **D-026**. The specific glyph shapes below are DEFAULT and expected to change through device testing.

The control layer is black-and-white with **one** exception. Colour in this project means something — [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md) assigns it to the character, ability VFX, and world feedback — so the HUD stays out of that channel and never competes with the reserved warning treatment for incoming danger, which the feedback hierarchy ranks above the player's own resources.

| Element | Treatment |
|---|---|
| Button fill | Near-black, `BackgroundTransparency ≈ 0.3` so the arena reads through |
| Ring | White `UIStroke`, thin, `Transparency ≈ 0.15` |
| Icon | White source art, tinted through `ImageColor3` |
| Silhouette | Circle for all ten (`UICorner` 0.5) |

**The one permitted accent** means exactly one thing: *ready / available* — Breakthrough at full meter, an ability off cooldown. It is applied by tinting an icon's `ImageColor3`, which is why the source art is white: a white image can be tinted to any colour, a coloured one cannot. It must never be used decoratively, and never in the danger channel's hue.

> **Not yet driven.** All icons currently render white because no server-side meter or cooldown state exists to drive readiness. The channel is built; the signal is M3.

Icon, size tier, and screen position carry every remaining distinction, so nothing critical rides on colour alone — which satisfies the accessibility rule below rather than straining it.

### Icon set

Conventional pictograms, not invented shapes. The metaphors below were chosen because research across TSB, Jujutsu Shenanigans, Untitled Boxing Game, Blox Fruits, Deepwoken, Rivals, Genshin, Honkai Star Rail, Diablo Immortal, and COD Mobile found them shared across *many* games. Adopting shared vocabulary is safe; reproducing one game's layout or artwork is not, and [PROJECT_BRIEF.md](PROJECT_BRIEF.md) forbids it by name.

Each icon lives in an `ImageLabel` named `Icon`, a child of its button. Ledger rows `UI-ICON-001`…`006` in [ASSET_PROVENANCE_LEDGER.md](ASSET_PROVENANCE_LEDGER.md); recorded as D-027.

| Button | Icon | Source | Asset ID |
|---|---|---|---|
| `BasicAttackButton` | Fist | `lorc/punch` | `85239036663948` |
| `BlockButton` | Shield | `sbed/shield` | `94413571867350` |
| `DashButton` | Running figure | `lorc/sprint` | `87301382738025` |
| `MechanicButton` | Vortex | `lorc/vortex` | `133264139799883` |
| `BreakthroughButton` | Light bulb | `lorc/light-bulb` | `105324694393567` |
| `Ability1–4Button` | Numerals `1` `2` `3` `4`, the button's own `Text` | — | — |

Why a running figure for Dash: it promises speed without asserting a direction, which is correct because the button does **not** choose one — [COMBAT_SYSTEM.md](COMBAT_SYSTEM.md) defines dash as button *plus movement input*, so the stick supplies direction. It also matches the metaphor genre reference layouts use for the same slot. Two earlier icons were rejected: a four-way arrow (`delapouite/move`) implied the button picked a compass direction, and a forward burst (`delapouite/fast-forward-button`) read as a media control.

Why a bulb for Breakthrough: every available lightning icon was a busy shard cluster unreadable at 64px, and the meter that gates it is literally called Discovery. That is the one place theme-fit beat strict convention.

Numerals are permitted; **word labels are not**. A numeral carries information an icon cannot — which slot, how many seconds remain. `ATK`, `BLOCK`, `RUN`, `DASH`, `BREAK`, and `R` carried none the icon does not.

> **Every icon child must have `Active = false` and `Selectable = false`.** An active child GuiObject sinks the pointer input that `button.InputBegan` depends on, and the button silently stops responding to touch. Verify this after any HUD edit.

### Size tiers

| Tier | Buttons | Size (scale of X) |
|---|---|---|
| Primary | `BasicAttack`, `Block` — equal | ~0.115 |
| Secondary | `Dash`, `Mechanic`, `Breakthrough` | ~0.085 |
| Ability | `Ability1–4` | ~0.075 |

---

## Layout

Target viewport for the prototype is the one already recorded in [OMNISCIENCE_COLISEUM.md](OMNISCIENCE_COLISEUM.md): **750 × 361**, iPhone 17 Pro landscape. That is the smallest supported case until Q-014 sets a real device floor.

### Reserved zones

Roblox owns parts of the screen. Placing anything here guarantees a conflict:

| Zone | Owner | Rule |
|---|---|---|
| Bottom-left | Roblox thumbstick | Never place a combat button here |
| Bottom-right corner | Roblox jump button | Never place a combat button here |
| Top-left | Roblox menu button | Keep clear |
| Top-right | Chat and player list | Keep clear |
| Left edge inset | Notch / Dynamic Island in landscape | Keep critical UI out of the inset |
| Bottom edge inset | Home indicator | Keep tappable targets above it |

Use `GuiService:GetGuiInset()` and a `ScreenInsets` setting of `DeviceSafeInsets` rather than hardcoding offsets.

### Placement

- **Combat buttons form a staggered two-column arc on the right**, above and inboard of the jump button, reachable by the right thumb without covering the character. This is the genre-standard arrangement and derives from Roblox's own default jump-button placement, so players arrive with the muscle memory already built.
- **Abilities sit as a numbered row across the bottom-centre**, below the character rather than over it. They are deliberate choices, not reflexes, so they do not need the thumb-rest positions.
- **No combat control sits on the left.** The left thumb steers and does nothing else. Sprint used to live there; D-028 removed it by deriving speed from movement input instead.
- **Block and Basic Attack are the joint-largest and most reachable.** Block is held, used reactively, and mispressing it is the most punishing miss. *(This previously read "Block is the largest" while the Sizes table below said "equal to basic attack" — the two contradicted each other. Joint-largest is the reconciled rule.)*
- Breakthrough is visually distinct and **only interactive at full meter**. It is not hidden when unavailable, because players need to learn it exists.

The arrangement follows the genre standard: **a numbered ability row across the bottom-centre, and the combat actions in a staggered two-column arc on the right.** Positions as `Scale` within `TouchControls`.

| Button | x | y | Column | Size |
|---|---:|---:|---|---:|
| `BreakthroughButton` | 0.750 | 0.280 | inner | 0.070 |
| `BlockButton` | 0.750 | 0.536 | inner | 0.115 |
| `BasicAttackButton` | 0.750 | 0.850 | inner — nearest the thumb rest | 0.115 |
| `MechanicButton` | 0.900 | 0.307 | outer | 0.070 |
| `DashButton` | 0.900 | 0.543 | outer | 0.070 |
| `Ability1Button` | 0.389 | 0.893 | bottom-centre row | 0.070 |
| `Ability2Button` | 0.474 | 0.893 | " | 0.070 |
| `Ability3Button` | 0.558 | 0.893 | " | 0.070 |
| `Ability4Button` | 0.643 | 0.893 | " | 0.070 |

**Attack and Block are the two large buttons and both sit inner**, where the thumb rests; the smaller utilities sit outer, above the jump button. Sizes are `Scale` of `TouchControls` width.

**The entire left half is free of combat controls** (D-028). The left thumb steers and does nothing else.

### Geometry check

**Validate against live rendered geometry and measured obstacles — never against arithmetic or guessed zones.** Three separate rounds produced measured defects, each time because a number was assumed rather than observed. Read `AbsolutePosition` and `AbsoluteSize` from a running client with device emulation on, then check:

- every button pair for an edge gap `< 8px`
- every box against **Roblox's real touch controls**, read from `PlayerGui.TouchGui.TouchControlFrame`:
  - `JumpButton` — a hard failure. At a 685×338 viewport it measured **x 590–660, y 190–260**
  - `DynamicThumbstickFrame` — a soft warning; it is the *potential* stick area and is generously sized (**x −100–274**), so the ability row unavoidably clips it, as reference layouts also do
- every button against the 44pt tappable floor
- anything outside the screen

`TouchGui` is created lazily and may be absent early in a play session. If it is missing, the jump check has **not run** — say so rather than reporting a pass.

Three traps this has already caught, all invisible to inspection:

0. **The jump button is not where a guessed "bottom-right corner" zone puts it.** A guessed reserve of `x>0.82, y>0.75` put its top edge 63px below the real one, and Block overlapped the jump button in shipped layout as a result. Measure the instance.

1. **`TouchControls` is shorter than the viewport.** At a 685×338 viewport it is 685×**280** — `ScreenInsets = CoreUISafeInsets` takes the difference. Y positions are scale of *that*, so validating vertical gaps against viewport height overstates every one of them by around 20%.
2. **`UIAspectRatioConstraint.AspectType` must be `ScaleWithParentSize`.** The default, `FitWithinMaxSize`, fits the square inside the element's own `Size` box — and since `Size.Y` is `{0,0}` that box has no height, so the button collapses and `UISizeConstraint.MinSize` becomes the only thing giving it a size. Every button silently rendered at its floor, and would never have grown on a larger screen.

Current values pass with **zero failures** at a 685×338 emulated viewport; tightest pair 9.9px, Attack and Block render at 78px.

### Sizes

DEFAULT, from mobile touch-target guidance. Tune from device testing, never below the minimum.

| Element | Minimum tappable | Default |
|---|---|---|
| Basic attack | 44 × 44 pt | Largest in the cluster |
| Block | 44 × 44 pt | Equal to basic attack |
| Ability 1–4 | 44 × 44 pt | Uniform, smaller than block |
| Dash, Mechanic, Breakthrough | 44 × 44 pt | Uniform |
| Gap between adjacent buttons | 8 pt | 8–12 pt |

Use `UIAspectRatioConstraint` plus `Scale`-based sizing so buttons hold proportion across aspect ratios. **No button may overlap another**, including its transparent padding, at any supported viewport.

---

## Information display

Applies the feedback hierarchy in [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md). Higher priority must never be obscured by lower.

| Element | Shows | Rules |
|---|---|---|
| Health | Own current health out of `CombatConfig.MAX_HEALTH` | Always visible. Readable without counting pixels. Never the only signal that a hit landed. |
| Combat state | Stunned, blocking, ragdolled, spawn-protected, awakening | Only when not `Neutral`. Spawn protection must be unmistakable, on the HUD **and** on the character, since protected players cannot deal damage. |
| Cooldowns | Per-ability remaining time | On the button itself, not in a separate list. Radial or fill, plus a readable number. |
| Discovery Meter | Fill from 0 to `DISCOVERY_METER_MAX` | Distinct treatment at full, because that is when Breakthrough unlocks. |
| Combo state | Current position in the four-hit chain | Optional in Scope A. Must not be confusable with health. |
| Hit / block / miss | Result of my last action | Visual **and** audible. Blocked must not read as a hit. |
| Invalid action | A request the server rejected | Explicit. Silence reads as a bug and teaches nothing. |
| Session leaderboard | KOs and assists | Scope B. Dismissible. Never covers combat buttons or incoming-danger space. |

Numbers displayed here are presentation only. The server owns every value; the HUD renders what it is told and computes nothing consequential.

---

## Accessibility

- No critical distinction is carried by colour alone. Shape, motion, or sound must also differ.
- Every critical cue is identifiable with music muted.
- Text is legible at 750 × 361 without zooming.
- No interaction requires precise tapping, rapid reading, or a gesture with no button equivalent.
- Every keyboard action has a touch equivalent. Mobile is not a later port — that is a pillar-level constraint in [PROJECT_BRIEF.md](PROJECT_BRIEF.md).

---

## Acceptance

The HUD is acceptable when, on the target viewport in device emulation:

- [ ] Every one of the nine buttons exists with the exact name and class above, and no `InputController` warning appears in Output.
- [ ] Sprinting engages on its own at full stick deflection, and easing off the stick walks — with no button involved.
- [ ] All ten are reachable by thumb without covering the player's own character.
- [ ] No two buttons overlap, and none collides with a reserved zone.
- [ ] Health, active cooldowns, and meter are readable at a glance during combat.
- [ ] Spawn protection is obvious both on the HUD and on the character.
- [ ] Hit, block, and miss are distinguishable with sound off, and again with the screen ignored.
- [ ] Holding Block then losing window focus releases the block rather than latching it. This is the regression fixed in S10 of [PROJECT_AUDIT_2026-07-25.md](PROJECT_AUDIT_2026-07-25.md). **A human cannot check this by feel** — nothing on screen indicates whether Block is held, so playing the game proves nothing either way. It needs a debug readout of `IsActionDown("Block")`, or a unit test over the release path. Do not mark it passed on the strength of the button feeling fine.
- [ ] `TouchControls` is hidden on desktop and visible on touch, and switching input mid-session updates it.

Record results in a [playtest note](templates/PLAYTEST_NOTE.md).
