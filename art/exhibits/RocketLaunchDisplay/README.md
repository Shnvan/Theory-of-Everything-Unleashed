# Apollo 4 Saturn V + Launch Umbilical Tower — dossier

Fifth exhibit for the production pipeline. Follows the research-dossier gate in
[OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

**Status: structure researched, geometry built, not imported and not approved.** No human has signed it off.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.West_GravityAndSpaceflight.RocketLaunchDisplay` |
| Visible name | To be set — currently placeholder |
| Classification | Named replica — **three real objects at one disclosed display scale** |
| Primary anchor | Saturn V vehicle **SA-501** (Apollo 4, launched 9 November 1967), its Mobile Launcher, and Launch Umbilical Tower at Kennedy Space Center Launch Complex 39A |
| Dimension source | Wikipedia's *Saturn V* article for the vehicle (cites NASA technical documentation), *Kennedy Space Center Launch Complex 39* article for the LUT |
| Geometry | 2,664 triangles across **4 MeshParts** (polychrome pilot under D-037), 22.74 × 19.07 × 63.00 studs |
| Construction | Parametric, `generate.py`, geometrically stable across runs |
| **Display scale** | **1 stud = 7.08 ft = 2.16 m**, fixed by the LUT height (446 ft) fitting the 63-stud vertical envelope. Uniform across all three objects, as the accuracy doc requires |
| Rights | Geometry original. Wikipedia text CC BY-SA 4.0 but only numeric facts used |
| Gameplay fit | Replaces 50 primitive parts (`Body`, `Nose`, `Fin1`, `Fin-1`, `Flame`, plus `VisualDetail` children) with one `MeshPart` |
| Review | **UNSIGNED** |

## Why the scale is what it is

The exhibit's vertical envelope is 63 studs. Three real objects have to fit inside it at one scale:

- Saturn V total height (with LES): **363 ft**
- Mobile Launcher: **25 ft**
- Launch Umbilical Tower: **446 ft** — the tallest, and therefore the sizing driver

446 ft / 63 studs = **7.08 ft per stud**. At this scale the rocket becomes 51.30 studs tall (leaving the LUT visibly taller — the correct real relationship), and the whole assembly is 22.74 × 19.07 studs in plan, well inside the shell's 43.20 × 31.50 footprint. The generator asserts the LUT-taller-than-rocket relationship so it can't drift.

## What the primary sources establish

**Saturn V**, from Wikipedia's *Saturn V* article (cites NASA technical documentation):

- **Total height with spacecraft:** 363 ft / 111 m
- **Base diameter:** 33 ft / 10 m (S-IC and S-II)
- **S-IC first stage:** 138 ft × 33 ft dia
- **S-II second stage:** 81.6 ft × 33 ft dia
- **S-IVB third stage:** 58.6 ft × 21.7 ft dia
- **Instrument Unit:** 3 ft × 21.7 ft dia
- **Apollo spacecraft + LES:** ~82 ft (LM adapter + SM + CM + LES tower)
- SA-501 (Apollo 4) used the standard configuration; no dimensional deltas

**LUT and Mobile Launcher**, from Wikipedia's *Kennedy Space Center Launch Complex 39* article:

- **LUT height:** 446 ft / 136 m
- **Nine retractable swing arms**
- **Mobile Launcher Platform:** 161 × 135 ft, two-story, ~25 ft tall, four hold-down arms

## What is accurate

- **Uniform 1 stud = 7.08 ft scale for all three objects** — the accuracy doc's own requirement.
- **Five stages with correct diameter transitions:** S-IC and S-II at base diameter, taper down to S-IVB and Instrument Unit at upper diameter, LM adapter tapers again to spacecraft width. Interstages at the correct heights.
- **Silhouette-defining features:** four S-IC base fins, five F-1 engine bells at the bottom, the LES spike at the tip. Any one of these is enough to identify the vehicle as Saturn V rather than any other rocket.
- **LUT taller than rocket** — 63 vs 51.3 studs, matching the real 446 vs 363 ft.
- **Nine swing arms** at spaced heights, each reaching from the LUT to the rocket surface at the rocket's local radius at that height.
- **Mobile launcher underneath**, two-story rectangle with four hold-down arms clustered around the rocket base.

## What is interpretation

Stated plainly, because the factual card must not claim otherwise:

- **Materials.** Real Saturn V was white with black roll-pattern stripes; real LUT was painted red; real Mobile Launcher was industrial grey. All authored in brass because D-016 locks the palette to marble, dark stone, brass and glass. A larger palette gap than the sphere's brass-for-wood, and a real accuracy debt against a very recognisable colour scheme.
- **Structural detail on the LUT.** Real LUT was a dense trussed-steel lattice with hundreds of diagonal braces per storey. This authors it as four corner posts, horizontal rails at every 5 studs of height, and the swing arms — enough to read as "a scaffold tower", nothing more. Not a lattice at gameplay distance.
- **Swing arm shape.** Real arms had specific geometries and connections tuned to each stage's umbilical panel. These are straight rectangular beams to the rocket surface, no umbilical details.
- **F-1 engine bells at the base.** Simplified cones, not the ribbed bell-nozzle geometry the real engines carried.
- **No lightning rod on the LUT.** Real LUT had a lightning rod extending to 490.6 ft; that would exceed the envelope at the fixed scale, so it is omitted. The dossier says so.
- **No crawler-transporter.** The real Mobile Launcher was moved by a separate treaded crawler; not depicted.
- **Pose:** stacked-and-ready, not launch or roll-out.

## Rights

Geometry here is **original**. Numeric facts from **Wikipedia** — text **CC BY-SA 4.0**, prose not reused. Recorded in [ASSET_PROVENANCE_LEDGER.md](../../../docs/ASSET_PROVENANCE_LEDGER.md) as `REF-EXH-007`.

No NASA imagery is copied. NASA's own media is largely public domain (see `REF-EXH-005` for the SVS terms), but this exhibit uses none of it — only published measurements.

## Polychrome pilot (2026-07-26, D-037)

This exhibit is the pilot for D-037 — the amendment allowing real-object colours on production exhibit meshes while retaining the palette lock for arena architecture.

**Four MeshParts, one per material group** (splitting-for-physics/material reasons, not budget — same principled split the black hole, statues+orbs, and equations wall use):

| MeshPart | Contents | Studio material | Colour |
|---|---|---|---|
| `SaturnV_Body` | S-IC + S-II + S-IVB + IU + LM adapter + SM + LES tower + fins | `SmoothPlastic` | Institutional white |
| `SaturnV_Engines` | Five F-1 bells + Command Module heat-shield + LES motor tip | `Metal` | Dark grey / near-black |
| `SaturnV_LUT` | LUT tower structure + crane platform + crane jib | `SmoothPlastic` | LC-39A red-orange (Rocketdyne / lead-red primer visible in Apollo 4 launch photos) |
| `SaturnV_ML` | Mobile Launcher (both stories) + hold-down arms + 9 swing arms + arm tips | `Metal` | Industrial grey |

**What the polychrome captures that the all-brass version didn't:**

- **White + dark-grey engines** is Saturn V's actual iconic look. All-brass is not honest about any rocket in history.
- **Red LUT vs grey ML** matches Apollo-4 launch photography and lets a viewer read tower-vs-platform at a glance.
- **Neon accents not used here** — this exhibit's real colour scheme has no glow; kept for the science-visualisation exhibits under D-016's science-energy accent allowance.

**Simplifications kept from the earlier pass:**

- Black roll-pattern stripes on the S-IC body are NOT modelled. Adding them would need a handful of new torus segments and their own bucket. Recorded as a future refinement — probably worth doing if the pilot is judged a success and the full 23-exhibit polychrome pass goes ahead.
- Command Module coloured dark-grey (in the engine bucket) rather than silver — Roblox has no true silver material outside Neon and this is close enough at gameplay distance.

**Assert added:** the generator fails the build if the export is not exactly the four expected object names — same protection the statue orbs have. If a future edit collapses the buckets back into one mesh, the polychrome pilot silently loses its point.

## Remaining before this can ship

1. A human review signature (Q-023).
2. The factual museum card, disclosing the 1 stud = 7.08 ft scale and the material gap.
3. Set the visible stone name — the accuracy doc calls this **APOLLO 4 SATURN V AND LAUNCH UMBILICAL TOWER**.
4. Ideally, a primary source for LUT specifications (the Wikipedia article's LUT figures cite mixed sources).

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/RocketLaunchDisplay/generate.py \
  -- --out art/exhibits/RocketLaunchDisplay/build/RocketLaunchDisplay.glb
```

**Geometrically deterministic:** every run gives 2,664 triangles, 1,512 vertices and identical dimensions. Fails the build on triangle cap, collision-shell overhang, or if LUT is not taller than rocket.

## Import settings

Scale Unit **Stud**, Scale Factor **1**, Anchored **on**, Collision Fidelity **Box**, no rig, merge off.

## History

**Built 2026-07-26.** One assert-caught defect and one design decision.

**Assert caught: crane pushed the assembly past envelope.** The first draft placed the crane on top of the 63-stud LUT (`top_z + 0.9`, `top_z + 1.4`), which took the assembly to 65.4 studs — 2.4 past the envelope. Reworked so the crane operates from inside the tower's top platform rather than above it, which is closer to how the real LUT's crane was positioned anyway.

**Design decision: five real objects into one shape.** Rocket, LES tower, Instrument Unit, Mobile Launcher, and LUT are all distinct real objects, and this exports as one `MeshPart` because at gameplay distance they read as a single silhouette. The join is legitimate because nothing has to move independently — no swing arm animation, no launch pose, no crawler transport. If any of that ever ships, the split becomes a physics requirement rather than a budget one, and the four-mesh black-hole split is the precedent.
