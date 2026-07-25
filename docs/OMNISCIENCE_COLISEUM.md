# The Omniscience Coliseum

**Status:** approved arena direction; detailed static M1 prototype implemented and validated

**Decision:** D-013, refined by D-014, D-015, and D-016; D-017 governs deferred post-M4 production exhibits

**Purpose:** monumental contained eight-player combat arena and monument to science, polymaths, and invention

## Direction

The Omniscience Coliseum combines a Greco-Roman circular arena with a surrounding science museum. The monumental combat floor distributes five-times-scale scientific landmarks throughout the interior as physical obstacles while preserving at least one verified clear movement lane and a contained perimeter.

The D-016 build is a detailed static prototype, not final production art. Studio-native parts, aged pale marble, dark stone, brass and bronze mechanisms, glass, and restrained cyan, blue, purple, red, and green energy accents establish believable museum construction without external assets.

D-017 does not alter that accepted prototype. If the project passes M4, the future production pass will replace invented exhibit visuals with named historical replicas or authoritative scientific reconstructions while preserving the arena's scale, internal Model identities, footprints, collision shells, spawns, containment, and clear lane. See [Omniscience Coliseum Exhibit Accuracy](OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

## Layout

- A 1328.16×1328.16-stud foundation with a 758.95-stud-diameter circular combat disc.
- Arena architecture scaled uniformly by `√10` from D-014, producing exactly ten times its former floor area.
- Eight spawn pads at approximately radius 329, facing the center.
- Low central pedestal with a static mechanical orrery proxy.
- All 24 exhibit proxies scaled to five times their D-014 linear dimensions and distributed across the central, middle, and outer interior rings.
- Elevated surrounding gallery behind a continuous collision barrier.
- Eighteen-segment colonnade, open oculus, and north-facing arena title.
- A 48-segment transparent fail-safe collision ring at radius 373.97 and height 160, inside the visible perimeter barrier.
- Segmented marble floor panels, radial brass inlays, a compass mosaic, detailed gallery trim, upgraded column bases and capitals, spawn medallions, and a dark-stone title backing.
- Exactly one angled dark-stone inscription at the center-facing base of every exhibit; formula visuals, original fighter-title plaques, and the arena title remain.
- 1,949 anchored BaseParts total, including 445 architectural-detail parts, 984 exhibit visual-detail parts, and 24 simplified exhibit collision shells.

The D-014 arena used a 240-stud combat disc and a 16.77-second tested route. D-015 increases its floor area tenfold. A tested 100-stud segment along the required `Z=70` lane took **6.15 seconds at `WalkSpeed = 16`**, giving a full clear-lane crossing of about 53 seconds.

Movement speed has since risen to 24 (P-010), so the same lane is now about **4.1 seconds per 100 studs and roughly 35 seconds end to end**. Those two numbers are **derived by rescaling, not re-measured** — valid because speed is linear along a clear lane, but re-measure if the lane gains obstacles or slopes.

Do not be surprised that 759 ÷ 24 gives 31 seconds rather than 35. The original figure was a walked route, not a straight diameter, and carried roughly 12% overhead from acceleration and the lane's actual path. The 35-second number preserves that overhead and is the like-for-like comparison; 31 seconds is the frictionless ideal.

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

In the deferred D-017 pass, those fighter-title monuments remain separate. The `Scientist Statues` exhibit is planned to receive historically grounded portrayals with real-name stones and factual cards after its likeness references and rights pass review.

## Static-detail boundaries

- All 24 exhibits remain static and anchored at five-times scale.
- Exhibits do not damage, move, launch, teleport, stun, or otherwise affect players.
- Broad transparent collision shells preserve physical exhibit obstacles. Fine visual geometry, invisible UI anchors, and inscription stones are non-colliding and cannot snag players.
- Each exhibit has a `VisualDetail` Folder, a `CollisionShells` Folder, and one `NamePlaque` Model with an uppercase SurfaceGui inscription.
- The periodic-table exhibit displays all 118 element symbols in a static SurfaceGui.
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
- Exactly 24 non-Billboard stone inscriptions with the approved exhibit names; each is readable at approximately 20–30 studs.
- Zero exhibit-name BillboardGuis remain; six content BillboardGuis remain for formulas and fighter-title plaques.
- Exactly eight enabled neutral SpawnLocations at approximately radius 329.
- 1,949 anchored BaseParts and zero unanchored parts, below the 2,000-part ceiling.
- Exactly 984 fine exhibit-detail parts are non-colliding, non-touching, and non-queryable.
- Exactly 24 broad exhibit collision shells are collidable, non-touching, and queryable.
- Exactly 118 element-symbol cells exist on the periodic-table display.
- Exactly 48 continuous invisible containment segments.
- Solo spawn occurred safely inside the combat boundary at radius 334.59.
- Ray tests hit `CombatDisc`, `InnerBalustrade`, and the invisible `ArenaBoundary`.
- A player-sized full-width blockcast confirmed the required `Z=70` interior lane is clear.
- A 100-stud walk segment on that lane completed in 6.15 seconds, measured at `WalkSpeed = 16`. At the current `SPRINT_SPEED` of 24 that rescales to about 4.1 seconds.
- Eight representative exhibit-approach walks, one per sector, completed without collision snags.
- Eight seconds of repeated outward walking and jumping reached a maximum radius of 368.52 and could not cross the 373.97-stud containment ring.
- Solo Studio Output contained no project-script errors.
- An iPhone 17 Pro landscape simulation rendered at a 750×361 Studio viewport without severe camera or composition loss; Studio was reset to its default viewport afterward.
- A local server log recorded exactly two connected test players, and both PlayClient contexts launched without project-script errors.
- Runtime Scene Analysis recorded 2,909 instances, 74,238 triangles, and 25 draw calls from the tested boundary view. Its 12 unparented instances belonged only to Roblox PlayerModule and character runtime code.
