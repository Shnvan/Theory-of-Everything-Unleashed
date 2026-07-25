## Session handoff — 2026-07-26 (jump overlap fix, reference layout)

Follows [2026-07-26-standard-layout.md](2026-07-26-standard-layout.md). Format: [templates/SESSION_HANDOFF.md](../templates/SESSION_HANDOFF.md).

### Target

- Task: fix the Block/jump-button overlap the user spotted on a real screen, swap Block and Dash, and match the supplied reference arrangement.
- Acceptance condition: no button overlaps Roblox's actual jump button, verified by measurement rather than by a guessed zone.

### Completed

- Behavior changed: none. Presentation only, zero Luau.
- Studio place: all nine buttons repositioned and resized; Block and Dash swapped; `DashButton` icon changed to a running figure; `InputLayoutRevision` → `M1ReferenceArcV1`. Wrapped in a `ChangeHistoryService` recording.
- Docs: [DECISION_LOG.md](../DECISION_LOG.md) (D-030), [HUD_AND_UI_SPEC.md](../HUD_AND_UI_SPEC.md), [ASSET_PROVENANCE_LEDGER.md](../ASSET_PROVENANCE_LEDGER.md).
- Commits: none yet. Last commit `68f70fe`.

### The defect, and why it shipped

The user photographed a real screen showing `BlockButton` overlapping the jump button. Measurement confirmed it: Block occupied **y 134–213**, and Roblox's `JumpButton` occupies **x 590–660, y 190–260** at a 685×338 viewport.

**Root cause: I validated against a guessed reserved zone (`x>0.82, y>0.75`) rather than measuring the real control.** That guess put the jump button's top edge 63px lower than it actually is, so the checker reported clean while the buttons genuinely overlapped.

Roblox's touch controls are ordinary instances at `PlayerGui.TouchGui.TouchControlFrame` with readable `AbsolutePosition` and `AbsoluteSize`. There was never a reason to guess. **This is the third defect in this HUD work traceable to trusting an assumed number over an observable one** — after the aspect-ratio collapse and the viewport-vs-frame height error. The rule is now written into the spec and D-030: measure the instance, and if `TouchGui` is absent (it initialises lazily) report the check as *not run* rather than as a pass.

### Verification

- Jump-button clearance: **PASS** at validation time, 37px horizontal clearance for Attack, no button within 8px of the measured jump box.
- Pair gaps: **PASS**, 0 failures; tightest 8.3px (Breakthrough/Block).
- Tappable floor, screen bounds: **PASS**.
- Contract: **PASS**, nine buttons, 0 unresolved through `InputConfig.DEFINITION_BY_TOUCH_BUTTON`.
- Screen capture with emulation on: **RUN**, arrangement matches the reference.
- Static gates: **not re-run** — no source file was touched since the last green run.
- Jump check on the final applied state: **PASS, 0 overlaps.** Re-run after `TouchGui` was confirmed present. `JumpButton` measured at x 590–660, y 190–260; nearest button is `DashButton` at **14.0px** clearance. (An earlier attempt reported nothing because `TouchGui` had not yet initialised — the check now waits for it and reports NOT RUN rather than passing if it never appears.)
- Device acceptance walk, focus-loss latch, two clients: **NOT RUN.**

### Decisions

- **D-030**, superseding D-029's positions: reference arrangement, Block and Dash swapped, running-figure dash icon, and reserved-zone guesses replaced by measuring `TouchGui`.
- D-029's argument for moving Block away from the reference position was mine, applied to values the spec marks DEFAULT. The user overrode it, which is theirs to do.
- Ledger: `UI-ICON-004` (running figure) reinstated for Dash; `UI-ICON-007` (forward burst) marked `REMOVED`.

### Risks and blockers

- `DashButton` clears the jump button by only **14px**. It is the nearest button and the one to re-check after any retune.
- `Ability1Button` clips the dynamic thumbstick area by ~32px. Accepted deliberately — the frame describes where the stick *may* appear and is generously sized, and the reference layout does the same — but it means the leftmost ability button sits in movement space.
- `MechanicButton` keeps the vortex rather than a four-point star. No clean sparkle exists in the licensed icon set; every candidate was too busy at button size. The mechanic icon is character-specific anyway, and a black hole suits Gravity Sovereign.
- Tightest pair is 8.3px against an 8px minimum — very little margin if positions are retuned.
- `Shift` still walks rather than sprints (D-028). Unverified with testers.
- Attribution (Q-024) unmet, blocks release. Ledger rows unsigned pending Q-023.

### Next smallest task

- Task: walk the device-emulation acceptance list in [HUD_AND_UI_SPEC.md](../HUD_AND_UI_SPEC.md). It is now the only thing between the input layer and a checked M1 box — every other acceptance item has passed.
- Acceptance condition: every box passes, or failures are recorded with the specific position or icon that needs changing.
