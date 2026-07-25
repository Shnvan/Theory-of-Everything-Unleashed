## Session handoff — 2026-07-25 (studio verification)

Second handoff of the day; follows [2026-07-25-foundation-repair.md](2026-07-25-foundation-repair.md). Format: [templates/SESSION_HANDOFF.md](../templates/SESSION_HANDOFF.md).

### Target

- Task: pre-Rojo verification of the private prototype place against the repo, using the Roblox Studio MCP server registered in [.mcp.json](../../.mcp.json) (D-024). Precondition for the "connect the Rojo plugin" task named as the next smallest task in the prior handoff.
- Acceptance condition: know, from live Studio reads rather than assumption, whether the three sync roots exist at the paths `default.project.json` targets, whether `StarterGui.GameHUD` matches [HUD_AND_UI_SPEC.md](../HUD_AND_UI_SPEC.md), and whether any `InputController` warning is present in Output.

### Completed

- Behavior changed: none. Read-only session.
- Files changed: this handoff only.
- Commits: none.

### Verification

- Static checks: **PASS**, all four re-run this session at the pinned versions from `~/.rokit/bin` (they are not on the shell `PATH` by default). `stylua --check src` exit 0; `selene src` 0 errors / 0 warnings / 0 parse errors; `rojo build` exit 0; `luau-lsp analyze --definitions=globalTypes.d.luau --sourcemap=sourcemap.json src` exit 0, no diagnostics.
- Build tree: **PASS.** The built place contains `ReplicatedStorage.GameShared.{Types,Config}`, `ServerScriptService.GameServer`, and `StarterPlayer.StarterPlayerScripts.GameClient.{Bootstrap,Controllers}` with no double nesting. `GameServer` is absent from `sourcemap.json` only because `src/server/` holds nothing but `.gitkeep`; it is present in the built `.rbxlx`.
- Unit tests: none exist.
- Studio solo test: NOT RUN. Studio was in edit mode throughout; no play session started.
- Server + two clients: NOT RUN.
- Device emulation / mobile: NOT RUN.
- Eight clients: NOT RUN.

Studio MCP reads performed (all read-only):

- `list_roblox_studios` → single instance found and set active: "Theory of Everything: Unleashed — Prototype" (`70bc8bc0-…`).
- `inspect_instance` on the three sync roots and on `StarterGui.GameHUD` / `.TouchControls`.
- `search_game_tree` on `StarterGui.GameHUD.TouchControls` (depth 4) to enumerate button children.
- `get_console_output`.

Findings:

1. **Three sync roots exist at the exact paths in `default.project.json`.** Classes are all `Folder`. `ReplicatedStorage.GameShared` and `ServerScriptService.GameServer` are empty. **`StarterPlayer.StarterPlayerScripts.GameClient` is not empty** — it already contains a `Bootstrap` (Script) and a `Controllers` (Folder), 3 descendants total, provenance unknown. This is not in this session's git history.
2. **`StarterGui.GameHUD` matches the spec exactly.** ScreenGui → TouchControls Frame → ten TextButtons with the exact names required by [`InputConfig.luau`](../../src/shared/Config/InputConfig.luau). Buttons carry `UICorner`/`UIStroke`/`UITextSizeConstraint` styling children (not lookup-relevant, not forbidden). `TouchControls.Visible = false` at author time, consistent with the spec's rule that `InputController` owns visibility. `GameHUD` has attributes `TouchButtonCount=10` and `InputLayoutRevision="M1InputMappingV1"` (extras; spec is silent on these).
3. **Zero `InputController` warnings** in Output — but nothing has been played, so this is not a real signal. What Output *does* show, unrelated to the three checks but important:
   - `Warning: The script 'Bootstrap' with a non-legacy RunContext is parented to a container 'StarterPlayerScripts', which will cause it to run multiple times.` — from the pre-existing Studio-side `GameClient.Bootstrap`.
   - Repeated `Can't sync <GameShared|GameServer|GameClient> to disk: Root file or folder is missing`. **Corrected reading** (an earlier draft of this handoff guessed "another Rojo session"; that was a guess and the evidence points elsewhere): this is Studio's built-in **Script Sync**, which [TASKS.md](../../TASKS.md) M0 records as the mechanism originally used to put code into the place, and which M0.5 still refers to by name. It was configured against the pre-flattening layout; commit `9fc5866` moved those disk paths, so its roots no longer resolve. Consistent with the Studio-side scripts being exactly the pre-flattening set. Not confirmed directly — Script Sync's configuration is not readable over MCP, so **check the Script Sync panel in Studio to confirm**.

4. **The Studio-side scripts are stale, and overwriting them loses nothing.** This was the open assumption from the prior handoff; it is now closed by reading both sides. `script_read` on the two Studio scripts, compared against [`src/client/Bootstrap.client.luau`](../../src/client/Bootstrap.client.luau) and [`src/client/Controllers/InputController.luau`](../../src/client/Controllers/InputController.luau):

   | | Studio copy | Repo copy |
   |---|---|---|
   | `Bootstrap` class | `Script` (non-Legacy `RunContext`) | builds as `LocalScript` |
   | `Bootstrap` teardown | has `script.Destroying → Stop()` | deliberately **removed**, with a comment explaining it never fires |
   | `ACTION_DEFINITIONS` | inlined in the controller | moved to shared [`InputConfig.luau`](../../src/shared/Config/InputConfig.luau) |
   | Fix 1 — duplicated bind names | absent; names re-typed at bind time | binds by loop over one table |
   | Fix 2 — sequence number | absent; `ActionInput` has no `sequence` | `nextSequence`, monotonic |
   | Fix 3 — blocking startup | absent; `bindTouchControls()` called inline | `task.spawn(bindTouchControls)` |
   | Fix 4 — latched touch actions | absent; no focus-loss release | `releaseAllHeldActions` + `WindowFocusReleased` |
   | Fix 5 — ungated left-click sink | absent; always `Sink` | `enabled` gate, `SetEnabled`, `Pass` when disabled |

   The Studio copies are the pre-M0.5 versions and are strictly superseded. Rojo overwriting them is the intended outcome, not a loss.

5. **Static gates re-run this session and all pass** (see Verification).

### Decisions

- New or changed decisions: none.
- Open questions resolved: none.
- Documents updated: [HUD_AND_UI_SPEC.md](../HUD_AND_UI_SPEC.md) — the `NEEDS STUDIO` banner is discharged and replaced with a dated VERIFIED note, per that banner's own instruction. [TASKS.md](../../TASKS.md) — the three MCP-VERIFIABLE M0.5 boxes and the MCP-approval box checked, each with a note on what was and was not covered; the remaining Rojo box reworded to include disabling Script Sync first.

### Risks and blockers

- **Script Sync and Rojo would both manage the same three folders.** Studio's Script Sync is still configured against the pre-flattening paths and is erroring every few seconds. Leaving it active while connecting Rojo means two writers on one tree. **Disable Script Sync for these folders before connecting Rojo.** The Script Sync panel is not readable over MCP, so this is a manual check.
- **`GameShared` is empty in the place, and the new `InputController` hard-depends on it.** [`InputController.luau:27-30`](../../src/client/Controllers/InputController.luau#L27-L30) calls `ReplicatedStorage:WaitForChild("GameShared")` and then `WaitForChild("Types")` / `WaitForChild("Config")` **with no timeout**. If Rojo syncs the client folder but `GameShared` does not populate, the controller yields forever — the symptom is an "Infinite yield possible" warning and input never starting, not a clean error. Confirm all three roots populate in the same sync.
- `Bootstrap` changes class on sync: `Script` in the place → `LocalScript` from the build. This should clear the existing non-Legacy `RunContext` warning; confirm at the next play test rather than assume.
- Everything unverified in the prior handoff (touch behavior, focus-loss latch, `MouseButton1` gate, two-client) is still unverified. No play session has been run.
- **The checkpoint is still unpublished.** No write to the place has been made or should be made until it is.

### Next smallest task

- Task: publish the pre-Rojo checkpoint, disable Studio Script Sync for the three folders, then connect the Rojo plugin from this repo.
- Acceptance condition: a place version is saved to the cloud with a note identifying it as the pre-Rojo checkpoint; Output stops emitting "Root file or folder is missing"; after connecting, `GameShared` contains `Types/CombatTypes` + `Config/{CombatConfig,InputConfig}`, `GameClient` contains `Bootstrap` (as a `LocalScript`) + `Controllers/InputController`, there is no `GameClient/GameClient` nesting, and the arena, `GameHUD`, and all other non-code instances are intact.
