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
- [x] Remove `SprintButton`, replace `Sprint` with `Walk` in the shared action set, and give Dash a non-directional icon (D-028). *Done 2026-07-26. Ten touch buttons become nine. First source change of the HUD work: `touchButtonName` is now optional so an action can exist without a button. All four static gates pass; runtime shows 9 touch-mapped actions, 0 unresolved, clean Output.*
- [x] Adopt the genre-standard HUD arrangement — bottom-centre ability row, staggered right-hand combat arc (D-029). *Done 2026-07-26. Also fixed a latent defect: `UIAspectRatioConstraint.AspectType` defaulted to `FitWithinMaxSize`, which had been collapsing every button to its `MinSize`, so scale-based sizing had never worked. Geometry now validated against live rendered values; zero failures at a 685×338 emulated viewport.*
- [x] Sign the `UI-ICON-*` provenance rows and resolve Q-023. *Done 2026-07-26. All seven rows reviewed by **Shnvan** — five `APPROVED`, two `REMOVED`. Q-023 resolved: an agent may prepare a provenance row, a human sets the final status.*
- [ ] Re-sign or annotate `REF-ARENA-001`, which is still signed by an AI agent and is therefore not reviewed under the Q-023 resolution.
- [ ] **NEEDS ROBLOX.** Paste the CC BY 3.0 credit line into the experience description (Q-024). One minute, no code, and it discharges the licence condition that currently blocks release.
- [ ] Build a Credits panel in the settings/pause menu for the same attribution, once a settings UI exists (Q-024, proper fix).
- [x] Implement the shared combat state machine. *Done 2026-07-26 as `src/shared/Combat/CombatStateMachine.luau` (D-031). Pure functions: `canEnter`, `isActionPermitted`, `releaseHold`, `getRespawnState`. Verified by 36 unit tests plus a require in a live play session. Consumed by nothing yet — it is rules, not wiring.*
- [x] Implement automatic sprint and the `Walk` modifier (D-028). *Done 2026-07-26. `MovementController` plus `SPRINT_SPEED`/`WALK_SPEED` (P-010/P-011) and `getMoveSpeed`. No threshold constant was needed — the engine already scales speed by input magnitude, measured rather than assumed. Verified live: Shift drops 16→8 and releasing restores it, and respawning mid-hold comes back walking rather than latching.*
- [ ] Implement directional dash. Split out of the line above because dash is a combat state: it needs the first `RemoteEvent`, the first server module (`src/server/` is empty), the full server validation list, and four numbers nothing documents — distance, cooldown, duration, and any invulnerability window. `ROADMAP_AND_TESTING.md` requires it to degrade sanely with no directional input.
- [ ] Implement 100 health, death, five-second respawn, and brief spawn protection.
- [ ] Add a training dummy with resettable health.
- [x] Add unit tests over the pure shared logic: transition legality, priority comparison, and assist threshold. *Done 2026-07-26 (D-032). Lune runner, 36 tests in `tests/`, wired into CI. The suite was verified to fail correctly, not just to pass.*
- [ ] Add block-arc geometry tests. Deferred from the line above: no geometry function exists yet, and it needs `Vector3`, which the Lune harness deliberately does not provide. Belongs with M2 hit detection.

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

## Museum-Accurate Coliseum Production

**Started 2026-07-26 by user direction (D-033), ahead of the M4 gate D-017 originally required.** The combat foundation is still unfinished; this section runs alongside M1 rather than after M4.

- [x] Establish the art pipeline: Blender headless driven by committed Python generator scripts, GLB export, `art/` tree (D-034). *Verified deterministic — two runs produce byte-identical output.*
- [x] Resolve Q-014 and record target-device budgets (D-035). *≤500,000 triangles and ≤1,000 draw calls arena-wide, ≤20,000 per mesh, ≤1024×1024 textures. Baseline measured: 1,949 parts, 2,455 instances, 74,238 triangles, 25 draw calls.*
- [x] Build the armillary sphere pilot generator. *8,884 triangles, 45.62 × 52.49 × 45.62 studs, replaces 71 primitive parts with one mesh.*
- [x] Import the armillary sphere GLB and verify scale. *Done 2026-07-26. `MeshPart.Size` measured 45.620, 52.494, 45.620 — exact match. Found and fixed two source bugs: the 0.01 export conversion was backwards (arrived 100× small), and the part imported named `Torus` because the importer names from mesh data rather than the object. Also corrected a false byte-determinism claim — generators are geometrically deterministic, not byte-identical.*
- [x] Place the pilot mesh into its exhibit and hide (not delete) the 67 prototype parts. *Done 2026-07-26. Axis-aligned footprint unchanged, exactly one collider remains, reversal is a one-line script. Prototype visuals stay until the exhibit passes review, per `docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md`.*
- [ ] Verify the armillary sphere's proportions against Science Museum Group object `1878-12` and retune. The ring set currently reads busy at gameplay distance, and every proportion is invention — see the dossier. Do this before the second pilot, so the lesson applies to all 24.
- [ ] Complete and approve research dossiers for all 24 exhibits using the real names and accuracy classes in `docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md`. *Armillary sphere dossier started and explicitly marked INCOMPLETE — no corroborating source, proportions unverified against object `1878-12`.*
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
