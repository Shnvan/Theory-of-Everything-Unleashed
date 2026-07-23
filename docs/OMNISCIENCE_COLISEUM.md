# The Omniscience Coliseum

**Status:** approved arena direction; M1 graybox implemented  
**Decision:** D-013  
**Purpose:** compact eight-player combat arena and monument to science, polymaths, and invention

## Direction

The Omniscience Coliseum combines a Greco-Roman circular arena with a surrounding science museum. The playable center remains open and readable, while an elevated gallery presents monumental scientific instruments and invention displays.

The M1 build is a primitive-part blockout, not finished art. Marble-gray architecture, brass accents, and limited cyan, blue, purple, red, and green category colors establish the silhouette without committing to production assets.

## Layout

- Circular combat disc with an effective playable diameter of about 137 studs.
- Eight spawn pads at the perimeter of the combat space, facing the center.
- Low central pedestal with a static mechanical orrery proxy.
- Elevated, non-playable exhibit gallery behind a continuous collision barrier.
- Eighteen-segment colonnade, open oculus, and north-facing arena title.
- 424 anchored BaseParts total; decorative exhibit parts are non-collidable.

The original 160-stud estimate was tuned after an in-engine movement test measured sustained default character movement below the theoretical `WalkSpeed` value. The accepted route from `X=-64` to `X=64` took 9.85 seconds at `WalkSpeed=16`.

## Exhibit sectors

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

- All 24 exhibits are static, anchored, labeled graybox proxies.
- Exhibits do not damage, move, launch, teleport, stun, or otherwise affect players.
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

- Exactly 24 uniquely named exhibit Models across eight sectors.
- Exactly eight enabled neutral SpawnLocations.
- 424 anchored BaseParts; zero unanchored parts and zero collidable decorative exhibit parts.
- Solo spawn occurred inside the combat boundary.
- Downward and outward ray tests hit the combat floor and perimeter barrier.
- Default-speed traversal completed in 9.85 seconds.
- Solo Studio Output contained no project-script errors.
- A local server accepted two clients and recorded two connected players.
