## Session handoff — 2026-07-26 (genre-standard layout)

Follows [2026-07-26-sprint-removal.md](2026-07-26-sprint-removal.md). Format: [templates/SESSION_HANDOFF.md](../templates/SESSION_HANDOFF.md).

### Target

- Task: adopt the standard Roblox fighting-game HUD arrangement — numbered ability row bottom-centre, combat actions in a staggered right-hand arc.
- Acceptance condition: the arrangement matches the genre convention, geometry validates clean against real rendered values, and the D-022 contract is intact.

### Completed

- Behavior changed: **none.** Presentation only. Zero Luau modified.
- Studio place: all nine buttons repositioned; `UIAspectRatioConstraint.AspectType` corrected on all nine; `InputLayoutRevision` → `M1StandardArcV2`. Three `execute_luau` passes, each inside a `ChangeHistoryService` recording.
- Docs: [DECISION_LOG.md](../DECISION_LOG.md) (D-027 amended, D-029 added), [HUD_AND_UI_SPEC.md](../HUD_AND_UI_SPEC.md), [TASKS.md](../../TASKS.md).
- Commits: none yet. Last commit is `9b583de`; the sprint-removal work from the previous handoff is also still uncommitted.

### Verification

- Geometry: **PASS, 0 failures** — validated against **live rendered** `AbsolutePosition`/`AbsoluteSize` at a 685×338 emulated viewport with `TouchEnabled = true`. Tightest pair 9.9px against an 8px minimum; no reserved-zone intrusion; every button above the 44pt floor.
- Contract: **PASS, 0 problems.** Nine names, all `IsA("GuiButton")`, all direct children, every `GetDebugId` matching pre-change — positions moved, instances did not.
- Input-sink: **PASS.** Zero `Active` GuiObject descendants.
- Static gates: **PASS**, all four. Expected, since no source file was touched.
- Runtime: **PASS.** 0 unresolved touch buttons, Output clean.
- Screen capture: **RUN, with device emulation on** — the previous session's capture was taken on desktop and showed nothing, since `TouchControls` correctly hides there. This one shows the arrangement and the restored size hierarchy.
- Unit tests: none exist.
- Full device acceptance walk: **NOT RUN.** Reach and one-handed use are still unverified by a human.
- Block focus-loss latch: **NOT RUN.**
- Server + two clients: **NOT RUN.**

### Two defects found, both invisible to inspection

1. **`UIAspectRatioConstraint.AspectType` was wrong on every button since the icon pass.** The default, `FitWithinMaxSize`, fits the square inside the element's own `Size` box; `Size.Y` is `{0,0}`, so that box had no height, the square collapsed, and `UISizeConstraint.MinSize` was the only thing giving each button a size. **Scale-based sizing had never once taken effect** — Attack rendered at 56px instead of 79px, and no button would ever have grown on a larger screen. Fixed by setting `ScaleWithParentSize`.
2. **Vertical gaps had been validated against the wrong height.** `TouchControls` is 280px tall inside a 338px viewport, because `ScreenInsets = CoreUISafeInsets` takes the difference. Y positions are scale of the frame, not the viewport, so validating against viewport height overstated every vertical gap by roughly 20%.

Together these mean the previous pass's "zero failures" was **arithmetically correct on wrong inputs**. Once real sizes and the real parent height were used, three pairs failed — Breakthrough/Dash at 0.6px. Corrected before anything shipped, but the lesson is recorded in D-029 and the spec: **validate against live rendered geometry, never against computed intent.**

### Decisions

- **D-029**, amending D-027's arrangement: genre-standard bottom-centre ability row plus staggered right arc; arc ordered by reachability rather than the reference's order; live-rendered validation and `ScaleWithParentSize` both made binding rules.
- The layout question that prompted this was settled on the merits: adopting a shared ergonomic arrangement is convention, not copying. What is deliberately not taken is the reference's ability names, title treatment, and artwork.

### Risks and blockers

- **Uncommitted work is accumulating again** — two sessions' worth now: the sprint/walk change and this layout pass.
- The bottom-centre ability row sits below the character in the capture, but **whether it covers the character during actual movement is unverified**. The spec forbids covering the player's own character.
- `Shift` still means walk, not sprint — the inverted convention flagged in the previous handoff, still the most likely thing to confuse a tester.
- Attribution (Q-024) unmet, blocks release. Ledger rows unsigned pending Q-023.
- Every remaining M1 acceptance item — device walk, focus-loss latch, two clients — is still unrun.

### Next smallest task

- Task: the full device-emulation acceptance walk in [HUD_AND_UI_SPEC.md](../HUD_AND_UI_SPEC.md), which is now the only thing standing between the input layer and a checked M1 box.
- Acceptance condition: every box passes, or failures are recorded with the specific positions that need changing.

Then: two-client test → check M1's input-mapping box → the shared combat state machine as pure functions with unit tests.
