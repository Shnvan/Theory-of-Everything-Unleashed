# HUD and UI Specification

**Status:** the instance contract is LOCKED because code already depends on it. Layout numbers are DEFAULT and expected to change through device testing.

**Why this document exists.** `src/shared/Config/InputConfig.luau` resolves ten touch buttons by exact name inside the Studio place. Those names were previously written nowhere but in the code. Because [STUDIO_IDE_WORKFLOW.md](STUDIO_IDE_WORKFLOW.md) bars non-script instances from synced folders, the GUI cannot be checked into git as instances — so the only place the contract can live is a document. Rename or delete any instance below and mobile input degrades to `warn()` lines at runtime with no compile-time signal at all. Recorded as D-022.

> **NEEDS STUDIO.** The tree below is the contract the code expects. It has not been verified against the live place in this session. On the next Studio session, compare them and correct whichever side is wrong — then note here that it was verified and on what date.

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
- **Block is the largest and most reachable** combat button. It is held, used reactively, and mispressing it is the most punishing miss.
- Breakthrough is visually distinct and **only interactive at full meter**. It is not hidden when unavailable, because players need to learn it exists.

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
