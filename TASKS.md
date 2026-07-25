# Task Board

**Active milestone:** M1 — movement and combat states.

Only check a task after its acceptance condition has been tested. Implementation is not acceptance; see the Definition of Done in [docs/ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md](docs/ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md).

## M0 — Project setup

- [x] Create a private Roblox experience named `Theory of Everything: Unleashed — Prototype`.
- [x] Create the Studio code folders described in `docs/STUDIO_IDE_WORKFLOW.md`.
- [x] Sync the three code folders to `src/shared`, `src/server`, and `src/client`.
- [x] Open this repository root in the external IDE.
- [x] Install a Luau language-server extension.
- [x] Initialize Git and make a documentation baseline commit.
- [x] Optional: connect a trusted AI client through Studio MCP. *Studio-side server enabled. Claude Code CLI was registered separately on 2026-07-25 (D-024); it needs its own `.mcp.json` entry, which the Studio toggles do not provide.*
- [x] Run one solo playtest and one server-with-two-clients playtest.

**M0 exit condition:** editing a test ModuleScript in the IDE updates Studio, and a two-client Studio test starts without errors.

## M0.5 — Foundation repair

Added 2026-07-25 after the audit in [docs/PROJECT_AUDIT_2026-07-25.md](docs/PROJECT_AUDIT_2026-07-25.md).

- [x] Commit the previously untracked client input layer, so the project's only implementation has a recovery point.
- [x] Flatten `src` to the documented Studio mapping, removing the extra `GameClient`/`GameServer`/`GameShared` level.
- [x] Adopt the pinned toolchain: Rokit, Rojo 7, Wally, StyLua, Selene, luau-lsp, CI (D-018). Verified locally — format, lint, type check, and build all pass.
- [x] Move the combat type vocabulary and every tunable into `src/shared` (`CombatTypes`, `CombatConfig`, `InputConfig`).
- [x] Fix the five `InputController` defects found by the audit: duplicated bind names, missing sequence number, blocking startup, permanently latched touch actions, and the ungated global left-click sink.
- [x] Write the design, engineering, HUD, tooling, AI-workflow, and skills doctrine documents, and record D-018 through D-023.
- [x] Register Roblox Studio MCP for Claude Code in a committed `.mcp.json`, with scripts read-only (D-024), and record Blender and the other MCP candidates as OUT (D-025).
- [x] Approve the project-scoped MCP server in a new Claude Code session and confirm Studio's panel stops reporting "No clients connected". *Approved 2026-07-25. Connection proven by successful `list_roblox_studios` plus read calls against the live place; the panel's own text was not visually confirmed.*
- [x] **MCP-VERIFIABLE.** Confirm `ReplicatedStorage/GameShared`, `ServerScriptService/GameServer`, and `StarterPlayer/StarterPlayerScripts/GameClient` exist at the paths `default.project.json` targets — before connecting Rojo, which is the step with real risk to the place. *All three exist, all `Folder`. `GameShared` and `GameServer` are empty; `GameClient` holds stale pre-M0.5 copies of `Bootstrap` and `Controllers/InputController` — see the 2026-07-25 studio-verification handoff.*
- [x] **MCP-VERIFIABLE.** Verify the live `GameHUD` tree against [docs/HUD_AND_UI_SPEC.md](docs/HUD_AND_UI_SPEC.md) and correct whichever side is wrong. The spec was written from what the code expects, not from the place. *Verified 2026-07-25: the place and the spec agree exactly. No correction needed on either side.*
- [x] **MCP-VERIFIABLE.** Read Output for `InputController` warnings about a missing HUD or touch button. *None present. Note this is weak evidence — the place has not been played this session, so no runtime path has executed.*
- [x] **NEEDS STUDIO.** Publish a checkpoint, disable Studio Script Sync for the three folders, then connect the Rojo plugin and confirm the three folders land where Script Sync put them, with no double nesting and no loss of Studio-side instances. *Done 2026-07-25. Checkpoint published; Script Sync disabled and confirmed silent; Rojo 7.7.0 plugin installed via `rojo plugin install` and connected to `localhost:34872`. Sync scope was `ReplicatedStorage` and `StarterPlayer` only — Workspace, StarterGui, and Lighting untouched, and `GameHUD.TouchControls` kept its original `uniqueId`. `Bootstrap` converted `Script` → `LocalScript` with `RunContext = Legacy`, clearing the multiple-run warning. Live two-way sync proven by a probe comment appearing in Studio and disappearing on revert.*

**M0.5 exit condition:** a clean checkout plus `rokit install` reproduces the toolchain, all static gates pass, Rojo syncs into the private place without loss, and the HUD contract matches the place.

## M1 — Movement and combat states

- [x] Build and validate the arena with eight thematic sectors, eight safe spawns, 5× physical exhibits, a clear traversal lane, and tested perimeter containment.
- [x] Complete and validate the Studio-native static realism pass with 24 engraved exhibit stones, simplified collision shells, mobile-landscape readability, and a sub-2,000-part budget.
- [ ] Implement input mapping for keyboard/mouse and touch. *Implemented and committed. Studio solo test **passed** 2026-07-25 — all ten touch buttons resolved at runtime with zero `InputController` warnings. Still pending: full device emulation against the HUD spec, the Block focus-loss latch check, and a two-client test before this box may be checked.*
- [x] Restyle the touch HUD to an achromatic, wordless control layer (D-026), and correct the Sprint placement, Block sizing, and missing `UIAspectRatioConstraint` drifts from [docs/HUD_AND_UI_SPEC.md](docs/HUD_AND_UI_SPEC.md). *Done 2026-07-25. Zero Luau changed; the D-022 instance contract verified intact by matching debug IDs.*
- [x] Replace the abstract glyphs with conventional pictogram icons and a machine-validated thumb-arc layout (D-027). *Done 2026-07-26. Six CC BY 3.0 icons from game-icons.net uploaded and applied; layout recomputed to zero geometry failures from three measured violations. Zero Luau changed; contract re-verified by matching debug IDs.*
- [ ] Surface the CC BY 3.0 icon attribution in-game (Q-024). **Blocks release.** The obligation is live now — the icons are already in the place — but there is no credits or settings menu to put the credit in.
- [ ] Implement the shared combat state machine. *`CombatTypes.CombatState` and the priority table exist; the transition rules do not.*
- [ ] Implement sprint and directional dash.
- [ ] Implement 100 health, death, five-second respawn, and brief spawn protection.
- [ ] Add a training dummy with resettable health.
- [ ] Add unit tests over the pure shared logic: transition legality, priority comparison, assist threshold, and block-arc geometry. Retires the "every combat change costs a two-client playtest" risk.

**M1 exit condition:** a player can move, dash, damage the dummy through a server-approved test action, die, and respawn without stuck states.

## M2 — Universal close combat

- [ ] Implement the four-hit M1 chain.
- [ ] Implement hit detection and server validation.
- [ ] Implement frontal block.
- [ ] Implement hitstun, knockback, and ragdoll.
- [ ] Implement one limited ragdoll escape using the dash input.
- [ ] Add clear hit, block, and invalid-action feedback.
- [ ] Run the timeboxed Server Authority spike and record a go/no-go decision (D-020). Measure feel against the documented beta gaps: the eight-active-animation-track ceiling and strafe position quantization.
- [ ] Migrate the input layer to the Input Action System, or restate the trigger if the spike defers it (D-019).

**M2 exit condition:** two local clients can attack, block, escape once, and complete repeated KO/respawn loops without desynchronizing.

## M3 — Gravity Sovereign vertical slice

- [ ] Implement the first approved gravity ability.
- [ ] Add cooldown and Discovery Meter handling.
- [ ] Add placeholder animation, VFX, sound, and mobile button feedback.
- [ ] Add KO and assist credit.
- [ ] Add a server leaderboard for the current session.
- [ ] Add the short prototype Final Proof KO effect only if core combat already passes.

**M3 exit condition:** three uninstructed testers can enter, fight, understand the main controls, and voluntarily re-engage after a KO.

## M4 — Prototype gate

- [ ] Run keyboard/mouse and mobile-emulation tests.
- [ ] Run one-, two-, and eight-client tests.
- [ ] Test duplicate requests, impossible range, cooldown spam, reset, disconnect, and death during an ability.
- [ ] Record tester observations and metrics from `docs/ROADMAP_AND_TESTING.md`.
- [ ] Decide: iterate combat, continue to the full Gravity Sovereign kit, or stop/pivot.

## Post-M4 — Museum-Accurate Coliseum Production

**Deferred:** do not begin this section unless M4 passes and the continuation decision authorizes production art.

- [ ] Complete and approve research dossiers for all 24 exhibits using the real names and accuracy classes in `docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md`.
- [ ] Resolve Q-014 and record target-device geometry, texture, draw, memory, streaming, and frame-time budgets. **This blocks the rest of this section and is cheap to close; do it early rather than in sequence.**
- [ ] Resolve Q-021 before modelling the Hall of Minds: decide whether a named Marie Curie statue can coexist with the Radiant Pioneer identifiability rule.
- [ ] Resolve Q-018: lock the Prague Astronomical Clock restoration era before modelling it.
- [ ] Approve provenance for every external reference and asset; obtain separate advance approval for every non-zero cost.
- [ ] Establish the Git LFS `art/` source tree, naming rules, export presets, reimport workflow, and rollback procedure.
- [ ] Build and validate the Della Volpaia armillary-sphere, Boulton and Watt beam-engine, and NASA-grounded black-hole pilots.
- [ ] Produce the remaining exhibits one sector at a time without changing internal Model identities, footprints, or collision shells.
- [ ] Add exactly 24 real-name stones and 24 factual museum cards with verified text, scale disclosures, and source identifiers.
- [ ] Confirm imported assets contain no scripts, remotes, packages, hidden executable content, or undocumented dependencies.
- [ ] Re-run arena collision, spawn, containment, `Z=70` lane, desktop, mobile, solo, two-client, and eight-client acceptance.
- [ ] Complete the provenance, factual-accuracy, Scene Analysis, and target-device performance reviews before replacing the final prototype visual.

**Post-M4 Coliseum exit condition:** all 24 exhibits have approved evidence and rights, real-name stones and factual cards are correct, arena gameplay constraints still pass, and the target device meets its recorded performance budgets.

## Parking lot

- Full Gravity Sovereign normal kit
- Character-specific `R` mechanic
- Breakthrough transformation and awakened moveset
- Breakable walls and throwable science props
- Eureka Engineer and Renaissance Mind
- Mastery and cosmetics
- Public alpha, onboarding, saving, and store
