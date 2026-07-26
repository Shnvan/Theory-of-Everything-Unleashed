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
- [x] Verify the armillary sphere's proportions against Science Museum Group object `1878-12` and retune. *Done 2026-07-26. The real object is 500 × 300 × 300 mm — a 1.67:1 ratio against the model's 1.15:1, so it read as a ball rather than a tall instrument. Rebuilt with claw feet, a differentiated zodiac band, and a central globe. Corroborating source found (della Volpaia 1564, Epact `18837`), closing the dossier's biggest gap. The generator now asserts the ratio so it cannot regress silently.*
- [x] Re-import the retuned GLB and swap `ProductionMesh`. *Done 2026-07-26. Imported at Scale Factor 1 measuring 38.115 × 62.948 × 38.115 — exact match, and named correctly, confirming both first-import bugs are fixed. Seated on the plinth at Y 39.636. Footprint delta 0.0000, envelope 8.16–71.11 against a 71.16 limit, exactly one collider.*
- [x] Build the second and third pilot **generators** — Boulton and Watt beam engine, and the NASA-grounded black hole. *Done 2026-07-26. Engine: 3,512 tri, 41.75 × 18.00 × 56.60, one mesh. Black hole: 12,016 tri across four meshes, 35.00 × 34.58 × 20.21. Both rendered and visually checked before export was accepted; four defects found that every assert had passed (D-036). Neither is imported and neither is approved.*
- [x] Import both pilot GLBs, replace the prototype geometry, and verify footprints. *Done 2026-07-26. All five MeshParts arrived at exact generator dimensions to three decimals, and mesh-data naming held. Engine placed as one `ProductionMesh` at plinth top; black hole placed as a four-mesh `ProductionMesh` Model matching the prototype's Singularity position. Both exhibits: axis-aligned footprint delta 0.0000, exactly one collider (`PrimaryCollisionShell`), all preserved children intact. 46 engine and 64 black-hole prototype parts hidden with originals stored in attributes for one-line restoration. Screen-captured from a gameplay-distance angle for each; the engine reads as a rotative beam engine and the black hole reads as a shadow-plus-lensed-disk with Doppler asymmetry. Neither is signed and neither is approved.*
- [x] Rename the `BLACK-HOLE GENERATOR` and `GRAVITY-CONTROL CHAMBER` stones. *Done 2026-07-26. Now `BLACK-HOLE ACCRETION-DISK VISUALIZATION` and `CAVENDISH TORSION BALANCE` per the accuracy doc's real-object anchors. Both the `Text` label and the `DisplayName` attribute were updated on each exhibit.*
- [x] Build the Cavendish torsion balance generator (`GravityControlChamber` renamed). *Generator + placement done 2026-07-26: 3,152 tri, 37.66 × 34.84 × 22.00, one mesh, 17× linear scale. Imported at Scale Factor 1 to exact dimensions; placed as `ProductionMesh` at plinth top. Footprint delta 0.0000, exactly one collider, all preserved children intact. 51 prototype parts hidden.*
- [x] Build the Apollo 4 Saturn V + LUT generator (`RocketLaunchDisplay`). *Generator + placement done 2026-07-26: 2,664 tri, 22.74 × 63.00 × 19.07, one mesh, uniform 1 stud = 7.08 ft scale set by LUT height fitting the envelope. Imported exact; placed at plinth centre (Y 42.16). Footprint delta 0.0000, one collider, preserved children intact. 46 prototype parts hidden. Silhouette reads unmistakably as Saturn V + LUT at gameplay distance.*
- [x] Build the B-DNA double-helix generator (`DNAHelixStructure`). *Generator + placement done 2026-07-26: 4,584 tri, 17.49 × 51.63 × 18.97, one mesh, data-derived from PDB entry 1BNA (Drew et al. 1981) via vendored `data/1bna.pdb`. Ribbon-and-rungs style; two defects fixed during build — a hard-coded axis swap that landed the helix horizontally (caught by shell-overhang assert), and NURBS bevel curves that produced zero-vertex meshes (caught by render). Imported exact to three decimals; placed as `ProductionMesh` at plinth centre (Y 33.97), yaw 131.4°. Footprint delta 0.0000, one collider, all preserved children intact. 71 prototype parts hidden. Stone renamed to `B-DNA DOUBLE HELIX — PDB 1BNA` per the accuracy doc.*
- [x] Build the IUPAC periodic table (`PeriodicTableWalls`). *Content built 2026-07-26. First non-Blender exhibit — pipeline is a committed Luau setup script (`art/exhibits/PeriodicTableWalls/setup.luau`) run once through MCP `execute_luau`. Wall is a Studio Part reusing the prototype Wall's exact CFrame; content is one SurfaceGui with 121 children (title + 118 element cells + 2 f-block placeholders). Two defects fixed: prototype SurfaceGui rendered through the invisible Wall Part (ghost row + overlaid title), and missing 57-71/89-103 placeholders after the prototype GUI was disabled. Stone renamed to `IUPAC PERIODIC TABLE OF THE ELEMENTS`. Footprint delta 0.0000, one collider, all preserved children intact. 57 prototype parts hidden.*
- [x] Build the AI computing and robotics laboratory (`AIControlLaboratory`). *Generator + placement done 2026-07-26: 3,168 tri, 40.61 × 28.85 × 28.27, one mesh. Two server racks with 1U chassis + network switch on top; workbench with monitor, small collaborative arm, and tripod-mounted camera-sensor rig. Wholesale replacement of the fictional `GlassLab`/`Core` prototype the accuracy doc forbids. Imported exact; placed at plinth centre (Y 22.59), yaw 80°. Footprint delta 0.0000, one collider, all preserved children intact. 45 prototype parts hidden. Stone renamed to `AI COMPUTING AND ROBOTICS LABORATORY`. **Southwest_LifeAndComputation sector now 3/3 complete.***
- [x] **BATCH GENERATORS: 12 Blender exhibits + 1 Luau (equations wall).** *Done 2026-07-26 in one push. Generators only — not imported, not placed. Blaeu Celestial Globe (4,356 tri), Rowley Orrery (7,608 tri), Arsenius Astrolabe (3,724 tri), Galilean+Hooker Telescopes (1,064 tri), JPL Solar System Orbits (10,424 tri, log-scaled disclosed), Spacetime Curvature and Lensing (7,168 tri), Chicago Pile-1 (1,788 tri), Tesla Coil Apparatus (10,360 tri), Michelson Laser Interferometer (576 tri), Babbage Difference Engine No. 2 (5,148 tri), Six-Axis + SCARA Robot Arms (796 tri), Landmark Inventions Collection (1,092 tri, Gutenberg + Pascaline + Faraday + Wright Flyer). Plus Foundational Equations of Physics as Luau `setup.luau` with 12 equation tiles across 6 domains. Every generator has assert guards; every render was inspected before commit. Dossiers, ledger rows `REF-EXH-010` through `REF-EXH-022`. Stones NOT yet renamed (batched with placements).*
- [ ] Import the 12 batch GLBs + run equations `setup.luau` via MCP; place all 12 meshes + rename all 13 stones per accuracy doc. Envelope, yaw, and placement targets already known per the exhibit models. Once done: **21 of 24 exhibits shipped**. Remaining: Prague clock (Q-018 blocked), Curie statues (Q-021 blocked), Gaia star map (dataset decision deferred).
- [ ] Find a primary source for the Lap Engine's bore and stroke. The museum record for `1861-46` carries **no measurements at all**; the two figures used come from Wikipedia (`REF-EXH-004`) and are unconfirmed. Until then the factual card must not present them as measured.
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
