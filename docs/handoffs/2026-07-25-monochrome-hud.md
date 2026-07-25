## Session handoff — 2026-07-25 (monochrome HUD)

Third handoff of the day; follows [2026-07-25-studio-verification.md](2026-07-25-studio-verification.md). Format: [templates/SESSION_HANDOFF.md](../templates/SESSION_HANDOFF.md).

### Target

- Task: restyle the ten touch buttons to an achromatic, wordless control layer, and correct the layout drifts found while inspecting the live place. Sits under M1's input-mapping task.
- Acceptance condition: every button wordless and achromatic, the D-022 instance contract intact, `InputController` resolving all ten at runtime, and no source file changed.

### Completed

- Behavior changed: **none in gameplay.** Presentation only. No Luau was modified — the ten buttons keep their names, `TextButton` class, and parenting, so `InputController` and `InputConfig` were untouched.
- Files changed: [DECISION_LOG.md](../DECISION_LOG.md) (D-026), [HUD_AND_UI_SPEC.md](../HUD_AND_UI_SPEC.md) (Visual language section, layout positions), [TASKS.md](../../TASKS.md), this handoff.
- Studio place: all ten buttons restyled in one `execute_luau` pass wrapped in a `ChangeHistoryService` recording, so the whole change is a single Ctrl+Z in Studio.
- Commits: none yet at time of writing.

### Verification

- Static checks: **PASS**, all four. `stylua --check src` exit 0; `selene src` 0/0/0; `rojo build` exit 0; `luau-lsp analyze` exit 0. Expected, since no source file was touched — run anyway to prove it.
- Instance contract: **PASS, 0 problems.** All ten resolve, all `IsA("GuiButton")`, all direct children of `TouchControls`, and every `GetDebugId` matches the pre-change value — proving the buttons were *edited*, not recreated. Word labels cleared; numerals `1`–`4` retained.
- Input-sink check: **PASS.** Zero `Active` GuiObject descendants across all ten buttons. This was the main way the change could have silently broken touch, since an active child sinks the pointer input `button.InputBegan` needs.
- Studio solo test: **RUN.** Play mode entered and exited. At runtime `PlayerGui.GameHUD.TouchControls` existed, and resolving every name through `InputConfig.DEFINITION_BY_TOUCH_BUTTON` gave **0 unresolved buttons**. Console output was clean — no `InputController` warnings.
- Unit tests: none exist.
- Device emulation / mobile: **PARTIAL.** A screen capture during play confirmed every glyph renders and that `TouchControls.Visible` flipped to `true` under `TouchEnabled`. **Reachability, overlap at the 750×361 target, and reserved-zone collision were NOT formally checked.**
- Block focus-loss latch: **NOT RUN.**
- Server + two clients: **NOT RUN.**
- Eight clients: **NOT RUN.**

**One reading to not misinterpret.** `InputController.IsStarted()` returned `false` when queried from the command bar. That is **not** evidence the controller failed — Studio's command bar keeps a module cache separate from game scripts, so `require` there returns a fresh module instance rather than the one `Bootstrap` started. The positive evidence that the real controller ran is that `TouchControls.Visible` was `true` at runtime while the `StarterGui` template has it `false`, and `InputController.bindTouchControls` is the only code that sets it.

### Decisions

- New: **D-026** — the touch HUD is achromatic and wordless; the `DESIGN_PHILOSOPHY.md` colour language governs the character, ability VFX, and world feedback, **not** HUD button chrome. This resolves a real tension rather than overriding doctrine silently: read literally, that table assigns "the player's own abilities" to the fighter's identity colour, which would put hue on the ability buttons.
- Documents updated: `DECISION_LOG.md`, `HUD_AND_UI_SPEC.md`, `TASKS.md`.
- Two pre-existing spec contradictions were reconciled while editing: `HUD_AND_UI_SPEC.md` said both "Block is the largest" (Placement) and "equal to basic attack" (Sizes). Now joint-largest. Sprint's documented left-thumb placement disagreed with the place, where it sat at x = 0.79 among the combat cluster; the place now matches the document.

### Risks and blockers

- **The Block glyph is a single thick horizontal bar and may read as a "minus" or a disabled state rather than a barrier.** It is the weakest glyph in the set and the most likely to need a second pass. Worth deciding before any playtest with uninstructed testers.
- Press feedback is `AutoButtonColor` on a near-black fill, which may be too subtle to perceive. Deliberately not addressed in this pass, because a stronger press state needs code and this change was scoped to contain zero Luau.
- Layout positions are DEFAULT and were placed analytically, not tuned on a device. The lower-right cluster (Block, Breakthrough, Mechanic, Dash, Attack) is the densest region and the most likely to need spacing.
- Breakthrough's inner ring is built but **nothing hides it when the meter is not full** — the meter does not exist server-side. The distinct-at-full-meter rule is therefore prepared, not implemented. M3.
- GUI still cannot be version-controlled. The pre-change property table lives in the plan file and in the studio-verification handoff; the published checkpoint taken before this change is the real rollback.

### Next smallest task

- Task: run the full device-emulation pass at 750×361 against the acceptance list in [HUD_AND_UI_SPEC.md](../HUD_AND_UI_SPEC.md) — all ten thumb-reachable, no two overlapping, nothing colliding with thumbstick/jump/menu/chat, every glyph identifiable without its old label, and the Block hold → focus-loss release check.
- Acceptance condition: every box in that list passes, or the failures are recorded with the layout numbers that need changing.

After that: the two-client test, then check M1's input-mapping box, then the shared combat state machine as pure functions with unit tests.
