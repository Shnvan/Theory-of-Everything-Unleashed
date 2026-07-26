# Handoff — AI Lab placed; Life & Computation sector complete (3/3)

**Date:** 2026-07-26
**Scope:** Studio place, `TASKS.md`, and this file.
Follows [2026-07-26-periodic-table.md](2026-07-26-periodic-table.md).

## Life & Computation sector: all three exhibits now production-mesh

| Exhibit | Type | Anchor |
|---|---|---|
| DNAHelixStructure | Blender mesh | PDB 1BNA (Drew et al. 1981) |
| PeriodicTableWalls | Luau SurfaceGui | Current IUPAC list |
| AIControlLaboratory | Blender mesh | *Generic — scientific reconstruction, no source* |

All three stones now match the accuracy doc's real names:
- `DNA HELIX STRUCTURE` → **B-DNA DOUBLE HELIX — PDB 1BNA**
- `PERIODIC-TABLE WALLS` → **IUPAC PERIODIC TABLE OF THE ELEMENTS**
- `AI CONTROL LABORATORY` → **AI COMPUTING AND ROBOTICS LABORATORY**

The two West Gravity stones (BLACK-HOLE / GRAVITY-CONTROL) were renamed earlier today; between the two sectors, no visible sign now presents a fictional machine as real. **Two release blockers cleared.**

## Placed today

**AI Computing and Robotics Laboratory** — `TheOmniscienceColiseum.ExhibitSectors.Southwest_LifeAndComputation.AIControlLaboratory.ProductionMesh`. One `MeshPart`, 40.61 × 28.85 × 28.27, brass Metal, anchored, non-colliding. Placed at `(115.23, 22.59, 20.32)`, yaw `80°`, on plinth top Y 8.16.

Composition: two 19-inch server racks with visible 1U chassis + network switch on top, workbench with a monitor stand, small collaborative arm reaching over the bench, tripod-mounted camera-sensor rig at the free end.

**Wholesale replacement of a fictional AI core.** The prototype was `GlassLab` (turquoise glass box) + `Core` (neon blue cube inside) + `Screen` + `Console` — exactly the "fictional sentient core" pattern the accuracy doc explicitly forbids. Every visible element replaced. 45 prototype parts hidden with `PrototypeOriginal*` attributes for one-line restoration.

Wrapped in one `ChangeHistoryService` recording covering placement + stone rename together.

## Verified

| Check | Result |
|---|---|
| Explicit axis-aligned AABB delta | 0.0000 on every axis |
| Colliders remaining | 1 (`PrimaryCollisionShell`) |
| Preserved children | `CollisionShells`, `Plinth`, `LabelAnchor`, `NamePlaque` intact |
| Prototypes hidden with attributes stored | 45 parts, including their child GUIs |
| Visual read at gameplay distance | Server rack farm + workbench with instruments — reads as an infrastructure lab |
| Stone displays correctly | `AI COMPUTING AND ROBOTICS LABORATORY` |

The lesson from the periodic table (also disable child SurfaceGuis/BillboardGuis on hidden prototype parts) was applied here too — no ghost renders.

## Sector scoreboard

| Sector | Done | Remaining |
|---|---:|---|
| West Gravity & Spaceflight | 3/3 ✓ | — |
| **Southwest Life & Computation** | **3/3 ✓** | — |
| North CelestialHall | 1/3 | Blaeu globe, Rowley orrery |
| Northeast Observation & Time | 0/3 | Arsenius astrolabe, Prague clock (Q-018 BLOCKED), telescopes |
| South Machines | 1/3 | Babbage difference engine, robot arms |
| East Cosmic Visualization | 0/3 | Gaia star map, JPL orbits, spacetime lensing |
| Southeast Energy & Matter | 0/3 | Chicago Pile-1, Tesla coil, Michelson interferometer |
| Northwest Hall of Minds | 0/3 | Scientist statues (Curie Q-021 BLOCKED), equations, inventions |

**8 exhibits shipped, ~16 remaining.** Two hard blockers (Q-018 Prague clock era, Q-021 Curie / Radiant Pioneer conflict) still hold two of those.

## What this did not do

- Not signed. All exhibits stay `UNSIGNED` under Q-023.
- Not approved.
- Prototype parts hidden, not deleted.
- No factual museum cards written.
- **M1 still not advanced. Combat still does not exist.**

## Two full sectors done. Three pipelines now proven:

1. **Blender headless + generator.py** → GLB → import → MCP place. Six exhibits: sphere, beam engine, black hole (4-mesh split), Cavendish, Saturn V + LUT, B-DNA, AI lab.
2. **Data-derived Blender**: DNA structure from vendored `1bna.pdb` coordinates. Same pipeline shape, but the geometry is computed from real experimental data rather than parametric shape functions.
3. **Luau setup script** → MCP `execute_luau` → Studio Part + SurfaceGui. Periodic table only. Available for any future text/data exhibit.

Each pipeline has documented pitfalls (D-036 covers the shared one: numbers can pass while the render is wrong) and each has an "assert canary" that catches its own class of regression. Any of the 16 remaining exhibits should fit one of these three shapes without new machinery.

## Next smallest thing

**Pick a sector, or return to M1 combat.** The exhibit backlog is genuinely long, and the "combat does not exist" gap is genuinely wide. Either is defensible; only one is a decision the project can defer forever.
