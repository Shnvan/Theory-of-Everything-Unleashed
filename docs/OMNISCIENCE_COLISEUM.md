# The Omniscience Coliseum

**Status:** approved arena direction; expanded M1 graybox implemented and validated

**Decision:** D-013, refined by D-014

**Purpose:** expanded eight-player combat arena and monument to science, polymaths, and invention

## Direction

The Omniscience Coliseum combines a Greco-Roman circular arena with a surrounding science museum. The enlarged combat floor distributes scientific landmarks throughout the interior while keeping every exhibit non-colliding and maintaining clear movement lanes.

The M1 build is a primitive-part blockout, not finished art. Marble-gray architecture, brass accents, and limited cyan, blue, purple, red, and green category colors establish the silhouette without committing to production assets.

## Layout

- A 420×420-stud foundation with a 240-stud-diameter circular combat disc.
- Eight spawn pads at radius 104, facing the center.
- Low central pedestal with a static mechanical orrery proxy.
- All 24 exhibit proxies distributed across the central, middle, and outer interior rings.
- Elevated surrounding gallery behind a continuous collision barrier.
- Eighteen-segment colonnade, open oculus, and north-facing arena title.
- Exhibit-name labels are hidden; formula visuals, original fighter-title plaques, and the arena title remain.
- 424 anchored BaseParts total; decorative exhibit parts are non-collidable.

The original 137-stud playable area passed its ten-second target but felt too small during direct scale review. The approved revision expands the combat disc to 240 studs. An unobstructed 216-stud lane from `X=-108` to `X=108` at `Z=18` took 16.77 seconds at `WalkSpeed=16`.

## Exhibit organization

The sector Models remain as Explorer organization and thematic ownership. Their children are deliberately mixed across the playable interior rather than placed only in the corresponding outer gallery.

| Sector | Static M1 proxies |
|---|---|
| North — Celestial Hall | Giant armillary sphere, celestial globe, mechanical orrery |
| Northeast — Observation & Time | Astrolabe monuments, astronomical clock tower, telescope towers |
| East — Cosmic Visualization | Holographic star charts, planetary-orbit platforms, space-time portal |
| Southeast — Energy & Matter | Atomic-energy core, Tesla coils, laser experiment chamber |
| South — Machines | Giant gears and machinery, steam engine, robotic arms |
| Southwest — Life & Computation | DNA helix, AI control laboratory, periodic-table walls |
| West — Gravity & Spaceflight | Gravity-control chamber, rocket launch display, black-hole generator |
| Northwest — Hall of Minds | Scientist statues, floating equations, invention museum cases |

Scientist monuments use original fighter titles such as **Gravity Sovereign**, **Eureka Engineer**, and **Renaissance Mind**. They do not reproduce the modern-person names or likenesses shown in the visual reference.

## M1 boundaries

- All 24 exhibits are static, anchored, unlabeled graybox proxies.
- Exhibits do not damage, move, launch, teleport, stun, or otherwise affect players.
- Decorative exhibit parts remain non-colliding so the scattered layout cannot create accidental combat traps.
- Rotation, moving machinery, animated holograms, functional portals, lasers, hazards, breakage, and final art are deferred until core combat is stable.
- No external models, meshes, packages, textures, or persistent arena scripts are included.

## Reference provenance

| Field | Record |
|---|---|
| Asset | `ChatGPT Image Jul 23, 2026, 07_15_55 PM (1).png` |
| Source | User-provided local visual reference |
| Local path | `C:\Users\Ivan\Downloads\ChatGPT Image Jul 23, 2026, 07_15_55 PM (1).png` |
| Date received | 2026-07-23 |
| Usage | Composition and mood reference only; not imported into the Roblox place |
| License/permission | Not verified for shipped use; no source pixels or geometry reproduced |

## Acceptance evidence

- Exactly 24 uniquely named exhibit Models across eight organizational sectors.
- All 24 exhibits are distributed inside the combat disc with zero bounding-box overlaps.
- Zero exhibit-name BillboardGuis remain; six content BillboardGuis remain for formulas and fighter-title plaques.
- Exactly eight enabled neutral SpawnLocations at radius 104.
- 424 anchored BaseParts; zero unanchored parts and zero collidable decorative exhibit parts.
- Solo spawn occurred safely inside the combat boundary at radius 103.6.
- Downward and outward ray tests hit `CombatDisc` and `InnerBalustrade`.
- The clear 216-stud lane completed in 16.77 seconds at default speed.
- Solo Studio Output contained no project-script errors.
- A local server accepted exactly two clients and recorded two connected players after the revision.
