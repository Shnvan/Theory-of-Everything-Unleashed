# The Omniscience Coliseum

**Status:** approved arena direction; ten-area M1 graybox implemented and validated

**Decision:** D-013, refined by D-014 and D-015

**Purpose:** monumental contained eight-player combat arena and monument to science, polymaths, and invention

## Direction

The Omniscience Coliseum combines a Greco-Roman circular arena with a surrounding science museum. The monumental combat floor distributes five-times-scale scientific landmarks throughout the interior as physical obstacles while preserving at least one verified clear movement lane and a contained perimeter.

The M1 build is a primitive-part blockout, not finished art. Marble-gray architecture, brass accents, and limited cyan, blue, purple, red, and green category colors establish the silhouette without committing to production assets.

## Layout

- A 1328.16×1328.16-stud foundation with a 758.95-stud-diameter circular combat disc.
- Arena architecture scaled uniformly by `√10` from D-014, producing exactly ten times its former floor area.
- Eight spawn pads at approximately radius 329, facing the center.
- Low central pedestal with a static mechanical orrery proxy.
- All 24 exhibit proxies scaled to five times their D-014 linear dimensions and distributed across the central, middle, and outer interior rings.
- Elevated surrounding gallery behind a continuous collision barrier.
- Eighteen-segment colonnade, open oculus, and north-facing arena title.
- A 48-segment transparent fail-safe collision ring at radius 373.97 and height 160, inside the visible perimeter barrier.
- Exhibit-name labels are hidden; formula visuals, original fighter-title plaques, and the arena title remain.
- 472 anchored BaseParts total; all 282 visible exhibit BaseParts are collidable while invisible anchors are not.

The D-014 arena used a 240-stud combat disc and a 16.77-second tested route. D-015 increases its floor area tenfold, producing an estimated full clear-lane crossing time of about 53 seconds. A tested 100-stud segment along the required `Z=70` lane took 6.15 seconds at `WalkSpeed=16`.

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

- All 24 exhibits are static, anchored, unlabeled graybox proxies at five-times scale.
- Exhibits do not damage, move, launch, teleport, stun, or otherwise affect players.
- Visible exhibit geometry is collidable and acts as deliberate physical cover or obstacles; invisible UI anchors remain non-colliding.
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
- All 24 exhibits are distributed inside the combat disc with zero exhibit/exhibit and exhibit/spawn overlaps.
- Zero exhibit-name BillboardGuis remain; six content BillboardGuis remain for formulas and fighter-title plaques.
- Exactly eight enabled neutral SpawnLocations at approximately radius 329.
- 472 anchored BaseParts and zero unanchored parts.
- All 282 visible exhibit BaseParts are collidable; zero invisible exhibit anchors are collidable.
- Exactly 48 continuous invisible containment segments.
- Solo spawn occurred safely inside the combat boundary at radius 329.5 with no exhibit conflict.
- Ray tests hit `CombatDisc`, `InnerBalustrade`, and the invisible `ArenaBoundary`.
- A player-sized full-width blockcast confirmed the required `Z=70` interior lane is clear.
- A 100-stud walk segment on that lane completed in 6.15 seconds.
- Eight seconds of repeated outward walking and jumping reached a maximum radius of 368.55 and could not cross the 373.97-stud containment ring.
- Solo Studio Output contained no project-script errors.
