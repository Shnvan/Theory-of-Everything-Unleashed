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
      SprintButton             GuiButton    -- hold
```

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
| `DashButton` | Four-way directional arrow | `delapouite/move` | `89977891032744` |
| `SprintButton` | Running figure | `lorc/sprint` | `87301382738025` |
| `MechanicButton` | Vortex | `lorc/vortex` | `133264139799883` |
| `BreakthroughButton` | Light bulb | `lorc/light-bulb` | `105324694393567` |
| `Ability1–4Button` | Numerals `1` `2` `3` `4`, the button's own `Text` | — | — |

Why a four-way arrow for Dash: [COMBAT_SYSTEM.md](COMBAT_SYSTEM.md) defines dash as **directional** — button plus movement input — so the metaphor is literal rather than decorative. Why a bulb for Breakthrough: every available lightning icon was a busy shard cluster unreadable at 64px, and the meter that gates it is literally called Discovery. That is the one place theme-fit beat strict convention.

Numerals are permitted; **word labels are not**. A numeral carries information an icon cannot — which slot, how many seconds remain. `ATK`, `BLOCK`, `RUN`, `DASH`, `BREAK`, and `R` carried none the icon does not.

> **Every icon child must have `Active = false` and `Selectable = false`.** An active child GuiObject sinks the pointer input that `button.InputBegan` depends on, and the button silently stops responding to touch. Verify this after any HUD edit.

### Size tiers

| Tier | Buttons | Size (scale of X) |
|---|---|---|
| Primary | `BasicAttack`, `Block` — equal | ~0.115 |
| Secondary | `Dash`, `Mechanic`, `Breakthrough`, `Sprint` | ~0.085 |
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

- **Combat buttons cluster on the right**, above and inboard of the jump button, reachable by the right thumb without covering the character.
- **Sprint sits near the left thumb**, because it is a movement modifier used while steering — not with the combat cluster.
- **Block and Basic Attack are the joint-largest and most reachable.** Block is held, used reactively, and mispressing it is the most punishing miss. *(This previously read "Block is the largest" while the Sizes table below said "equal to basic attack" — the two contradicted each other. Joint-largest is the reconciled rule.)*
- Breakthrough is visually distinct and **only interactive at full meter**. It is not hidden when unavailable, because players need to learn it exists.

Positions as `Scale` within `TouchControls`. DEFAULT — retune from device testing, but **re-run the geometry check afterwards**; these values were computed and machine-validated, not eyeballed.

| Button | x | y | Shares column with |
|---|---:|---:|---|
| `Ability1Button` | 0.545 | 0.270 | — |
| `Ability2Button` | 0.635 | 0.270 | `BreakthroughButton` |
| `Ability3Button` | 0.725 | 0.270 | — |
| `Ability4Button` | 0.815 | 0.270 | — |
| `BreakthroughButton` | 0.635 | 0.560 | `Ability2Button` |
| `MechanicButton` | 0.755 | 0.470 | `BlockButton` |
| `BlockButton` | 0.755 | 0.710 | `MechanicButton` |
| `DashButton` | 0.900 | 0.360 | `BasicAttackButton` |
| `BasicAttackButton` | 0.900 | 0.600 | `DashButton` |
| `SprintButton` | **0.115** | 0.430 | — |

Buttons snap onto **shared columns** (0.900, 0.755, 0.635) rather than sitting a hundredth apart. A near-miss reads as sloppiness, and the previous layout had two.

`SprintButton` sits on the **left**, above the thumbstick zone. It was previously at x = 0.79 among the combat cluster, contradicting the placement rule above.

### Geometry check

Hand-placing this layout produced three real defects — a 0.09px Block/Breakthrough gap, Basic Attack 10.6px inside the jump reserve, Ability4 13.7px inside the chat reserve. **Validate, do not eyeball.** At 750×361, check:

- all 45 button pairs for an edge gap `< 8px`
- every button box against the four reserved zones
- any two buttons within 0.02 scale of an axis without exactly sharing it
- anything outside the screen

The current values pass all four with **zero failures**; the tightest pair is 11.25px.

### Sizes

DEFAULT, from mobile touch-target guidance. Tune from device testing, never below the minimum.

| Element | Minimum tappable | Default |
|---|---|---|
| Basic attack | 44 × 44 pt | Largest in the cluster |
| Block | 44 × 44 pt | Equal to basic attack |
| Ability 1–4 | 44 × 44 pt | Uniform, smaller than block |
| Dash, Mechanic, Breakthrough, Sprint | 44 × 44 pt | Uniform |
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

- [ ] Every one of the ten buttons exists with the exact name and class above, and no `InputController` warning appears in Output.
- [ ] All ten are reachable by thumb without covering the player's own character.
- [ ] No two buttons overlap, and none collides with a reserved zone.
- [ ] Health, active cooldowns, and meter are readable at a glance during combat.
- [ ] Spawn protection is obvious both on the HUD and on the character.
- [ ] Hit, block, and miss are distinguishable with sound off, and again with the screen ignored.
- [ ] Holding Block then losing window focus releases the block rather than latching it. This is the regression fixed in S10 of [PROJECT_AUDIT_2026-07-25.md](PROJECT_AUDIT_2026-07-25.md) and only a device test proves it.
- [ ] `TouchControls` is hidden on desktop and visible on touch, and switching input mid-session updates it.

Record results in a [playtest note](templates/PLAYTEST_NOTE.md).
