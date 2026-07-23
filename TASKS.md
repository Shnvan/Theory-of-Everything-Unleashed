# Task Board

**Active milestone:** M1 — movement and combat states.

Only check a task after its acceptance condition has been tested.

## M0 — Project setup

- [x] Create a private Roblox experience named `Theory of Everything: Unleashed — Prototype`.
- [x] Create the Studio code folders described in `docs/STUDIO_IDE_WORKFLOW.md`.
- [x] Sync the three code folders to `src/shared`, `src/server`, and `src/client`.
- [x] Open this repository root in the external IDE.
- [x] Install a Luau language-server extension.
- [x] Initialize Git and make a documentation baseline commit.
- [x] Optional: connect a trusted AI client through Studio MCP.
- [x] Run one solo playtest and one server-with-two-clients playtest.

**M0 exit condition:** editing a test ModuleScript in the IDE updates Studio, and a two-client Studio test starts without errors.

## M1 — Movement and combat states

- [x] Build and validate the ten-area graybox arena with eight safe spawns, 5× physical exhibits, a clear traversal lane, and tested perimeter containment.
- [x] Complete and validate the Studio-native static realism pass with 24 engraved exhibit stones, simplified collision shells, mobile-landscape readability, and a sub-2,000-part budget.
- [ ] Implement input mapping for keyboard/mouse and touch.
- [ ] Implement the shared combat state machine.
- [ ] Implement sprint and directional dash.
- [ ] Implement 100 health, death, five-second respawn, and brief spawn protection.
- [ ] Add a training dummy with resettable health.

**M1 exit condition:** a player can move, dash, damage the dummy through a server-approved test action, die, and respawn without stuck states.

## M2 — Universal close combat

- [ ] Implement the four-hit M1 chain.
- [ ] Implement hit detection and server validation.
- [ ] Implement frontal block.
- [ ] Implement hitstun, knockback, and ragdoll.
- [ ] Implement one limited ragdoll escape using the dash input.
- [ ] Add clear hit, block, and invalid-action feedback.

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
- [ ] Resolve Q-014 and record target-device geometry, texture, draw, memory, streaming, and frame-time budgets.
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
