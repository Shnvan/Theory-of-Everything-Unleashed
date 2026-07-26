# Handoff — placing pilots 2 and 3 into the arena

**Date:** 2026-07-26
**Scope:** Studio place only. No repo changes beyond `TASKS.md` and this file.
Follows [2026-07-26-exhibit-pilots-2-and-3.md](2026-07-26-exhibit-pilots-2-and-3.md), which shipped the generators.

## What is now in the place

**Steam engine** — `TheOmniscienceColiseum.ExhibitSectors.South_Machines.SteamEngine.ProductionMesh` — one `MeshPart`, 41.75 × 56.60 × 18.00, brass metal, anchored, non-colliding. Sits on the plinth (bottom at Y 8.16, centre at Y 36.46). Rotated to shell yaw −157°. Replaces 46 hidden prototype parts (`Boiler`, `Firebox`, `Stack`, `Wheel1`, `Wheel-1`, plus `VisualDetail`).

**Black hole** — `...West_GravityAndSpaceflight.BlackHoleGenerator.ProductionMesh` — a `Model` containing four `MeshPart`s, all sharing origin at (−92.43, 33.16, −66.45), which is the current Singularity position: `BlackHole_Shadow` (SmoothPlastic black), `BlackHole_PhotonRing` (Neon cream), `BlackHole_DiskApproaching` (Neon bright cream), `BlackHole_DiskReceding` (Neon dim orange). Doppler asymmetry expressed through the brightness split. All four anchored and non-colliding. Rotated to shell yaw −125.7°. Replaces 64 hidden prototype parts.

Both wrapped in `ChangeHistoryService` recordings, so one Ctrl+Z reverses either placement.

## Verified per exhibit

| Check | Steam engine | Black hole |
|---|---|---|
| Explicit axis-aligned AABB delta | 0.0000 on every axis | 0.0000 on every axis |
| Colliders remaining | 1 (`PrimaryCollisionShell`) | 1 (`PrimaryCollisionShell`) |
| Preserved children | `CollisionShells`, `Plinth`, `LabelAnchor`, `NamePlaque` intact | Same |
| Prototype originals restorable | 46 parts, each with `PrototypeOriginalTransparency` / `PrototypeOriginalCanCollide` | 64 parts, same attributes |
| Visual read at gameplay distance | Portal frame, beam across top, flywheel with sun-and-planet, cylinder, governor all legible | Cream/orange disk halves with shadow between and photon ring above — the from-below Interstellar view |

## One design decision that cost a round trip

The black hole disk plane is horizontal — the mesh's 34.58-stud axis is Z after glTF import, and Y-yaw rotation preserves that. I tried a 90° pitch to stand it vertical, but the disk-diameter axis ended up pointing straight up-and-down, turning the disk into a plate on its edge. Reverted to horizontal.

Horizontal is correct for the physics. A player at ground level looks *up* at a horizontal disk, so they see the far side arcing over the shadow and the near side dropping below it — the defining gravitational-lensing signature, the Interstellar-from-below shot. The dossier already flags that the photon ring only reads correctly from certain angles, and this reinforces it: the disk face is only fully visible from above (verified with an overhead capture), while ground-level shows the lensed cross-section prominently.

That is genuinely educational, but it is also unusual to eye, and a factual card will need to say what the visitor is looking at.

## The stone still says the wrong thing

`BLACK-HOLE GENERATOR` is visible in one of the gameplay captures. It fails the accuracy doc's acceptance criterion — *"visible signs contain no fictional machine presented as real"* — and the same defect exists on `GRAVITY-CONTROL CHAMBER`. Neither renamed in this session; player-visible text, so a user decision. **Blocks release, not just approval.**

## What this did not do

- Neither exhibit is signed. Both stay `UNSIGNED` under Q-023.
- Neither is approved. Both dossiers stand as written.
- Prototype parts are hidden, not removed. The accuracy doc requires them to survive until an exhibit passes review.
- **M1 is not advanced.** Combat still does not exist. This work does not touch the input-box gate.

## Next smallest thing

If continuing on exhibits: rename the two stones, then pick sector 4. If returning to M1: build the training dummy so damage can be observed.
