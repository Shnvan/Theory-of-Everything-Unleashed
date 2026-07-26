# Handoff — Cavendish and Saturn V placed, West Gravity sector complete

**Date:** 2026-07-26
**Scope:** Studio place only. Two `TASKS.md` rows and this file are the only repo changes.

Follows [2026-07-26-pilots-2-and-3-placement.md](2026-07-26-pilots-2-and-3-placement.md).

## West Gravity sector: all three exhibits now production-mesh

| Exhibit | Studio path | Real anchor | Status |
|---|---|---|---|
| BlackHoleGenerator | `.West_GravityAndSpaceflight.BlackHoleGenerator.ProductionMesh` | NASA SVS visualization | Placed 2026-07-26 |
| GravityControlChamber (Cavendish) | `.West_GravityAndSpaceflight.GravityControlChamber.ProductionMesh` | Cavendish 1798 apparatus | **Placed today** |
| RocketLaunchDisplay (Saturn V + LUT) | `.West_GravityAndSpaceflight.RocketLaunchDisplay.ProductionMesh` | SA-501 + Mobile Launcher + LUT | **Placed today** |

All three exhibits also had their visible stones corrected earlier today:
- `GRAVITY-CONTROL CHAMBER` → **CAVENDISH TORSION BALANCE**
- `BLACK-HOLE GENERATOR` → **BLACK-HOLE ACCRETION-DISK VISUALIZATION**

The Saturn V stone still reads a placeholder; the accuracy doc's target is `APOLLO 4 SATURN V AND LAUNCH UMBILICAL TOWER`. Since the current placeholder does not violate the "fictional machine presented as real" rule that blocked the other two, this can be batched with a later production pass rather than fixed as a release blocker.

## Placed today

**Cavendish** — one `MeshPart` at `(-169.20, 25.58, 152.35)`, yaw `-48°` to match the shell. Brass Metal, anchored, non-colliding. Sits on plinth (top Y 8.16, mesh centre Y 25.58, half-height 17.42). Reads as a torsion balance: two prominent lead balls (rendered brass under D-016) hanging on either side of a thin horizontal rod, brass cabinet frame open on all sides, gantry above. Replaces 51 hidden prototype parts (`Core`, `Chamber`, `FieldRing_01..08`, plus 41 `VisualDetail` children — the fictional energy-chamber prototype).

**Saturn V + LUT** — one `MeshPart` at `(-110.17, 42.16, 272.68)`, yaw `-22°`. Brass Metal, anchored, non-colliding. Sits on plinth (top Y 10.66, mesh 63 studs tall, centre Y 42.16, fills envelope exactly). LES spike, rocket stages, LUT lattice with 9 swing arms, and mobile launcher platform all legible at gameplay distance. LUT correctly taller than rocket, matching the real 446 ft vs 363 ft. Replaces 46 hidden prototype parts (`Body`, `Nose`, `Fin1`, `Fin-1`, `Flame` + 41 `VisualDetail` children).

Both wrapped in `ChangeHistoryService` recordings — one Ctrl+Z reverses either placement.

## Verified per exhibit

| Check | Cavendish | Saturn V |
|---|---|---|
| Explicit axis-aligned AABB delta | 0.0000 on every axis | 0.0000 on every axis |
| Colliders remaining | 1 (`PrimaryCollisionShell`) | 1 (`PrimaryCollisionShell`) |
| Preserved children intact | `CollisionShells`, `Plinth`, `LabelAnchor`, `NamePlaque` | Same |
| Prototype originals restorable | 51 parts, `PrototypeOriginal*` attributes | 46 parts, same |
| Visual read at gameplay distance | Cabinet frame, rod with balls, gantry — reads as balance | Rocket + LUT tower, LES spike, swing arms — reads as Saturn V |

## Notes worth carrying forward

- **Both imports arrived anchored this time.** The `SteamEngine` was the outlier that came unanchored — presumably a one-off importer state, not a per-file thing. Still worth checking on future imports (D-016 requires every exhibit part anchored).
- **The render-the-export rule earned its keep during the generator pass** (both exhibits had defects that passed asserts and were caught by preview renders). At the placement stage the numbers are what they are, but the screen-capture still catches orientation and material problems — same principle, different failure surface.

## What this did not do

- Neither exhibit is signed. Both stay `UNSIGNED` under Q-023.
- Neither is approved.
- Prototype parts are hidden, not removed.
- Saturn V stone still on placeholder, not release-blocking.
- **M1 still not advanced.** Combat still does not exist. Five exhibits now shipped, roughly 19 remaining across four sectors plus Hall of Minds (Q-018 and Q-021 still block two of those).

## Next smallest thing

If continuing on exhibits: pick a sector. If returning to M1: build the training dummy so damage becomes observable.
