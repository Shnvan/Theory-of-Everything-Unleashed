# Handoff — batch of 13 exhibit generators shipped

**Date:** 2026-07-26
**Scope:** Generators/setup scripts + dossiers + ledger rows for 12 Blender exhibits and 1 Luau exhibit. No placements this session — user does bulk import next.

Follows [2026-07-26-ai-lab-and-sector-complete.md](2026-07-26-ai-lab-and-sector-complete.md).

## What shipped

Twelve Blender-mesh generators + one Luau setup script, one commit per sector for review clarity. Nothing is imported into Studio yet.

| # | Exhibit | Tri | Size (studs) | Anchor |
|---|---|---:|---|---|
| 1 | Blaeu Celestial Globe (1603) | 4,356 | 28.6 × 28.6 × 33.1 | SMG `1980-1913` |
| 2 | Rowley Orrery (1712-13) | 7,608 | 25.6 × 25.6 × 30.0 | SMG `1952-73` |
| 3 | Arsenius Planispheric Astrolabe | 3,724 | 36.0 × 14.9 × 38.6 | SMG `1878-11` |
| 4 | Galilean + Hooker Telescopes | 1,064 | 28.4 × 15.1 × 32.0 | 1610 refractor + 1917 Hooker |
| 5 | JPL Solar System Orbits | 10,424 | 34.0 × 34.0 × 4.0 | NASA JPL mean elements |
| 6 | Spacetime Curvature and Lensing | 7,168 | 36.0 × 30.0 × 30.4 | Standard rubber-sheet analogy |
| 7 | Chicago Pile-1 (1942) | 1,788 | 43.1 × 29.2 × 30.1 | Argonne / historical records |
| 8 | Tesla Coil Apparatus | 10,360 | 32.0 × 18.7 × 40.1 | Generic spark-gap circuit |
| 9 | Michelson Laser Interferometer | 576 | 36.0 × 24.0 × 15.75 | LIGO / laboratory convention |
| 10 | Babbage Difference Engine No. 2 | 5,148 | 39.7 × 16.6 × 28.6 | SMG `1992-556` |
| 11 | Six-Axis + SCARA Robot Arms | 796 | 38.9 × 20.0 × 16.7 | Generic industrial classes |
| 12 | Landmark Inventions Collection | 1,092 | 40.0 × 12.0 × 15.3 | Gutenberg + Pascaline + Faraday + Wright |
| 13 | Foundational Equations of Physics (Luau) | — | 40 × 5 × 30 wall + 12 tiles | Standard physics canon |

All 12 Blender generators pass their asserts (triangle cap, shell fit). Every render was inspected before commit; three exhibits needed a second iteration (Blaeu shell overhang, Babbage triangle cap, CP-1 shell overhang). No third iteration was needed on any.

## Three pipelines exercised

1. **Blender parametric geometry** (10 of the 12): sphere globes, mechanical assemblies, iconic apparatus silhouettes. The workhorse pattern from earlier sessions.
2. **Blender + real data table** (2 of the 12): JPL orbits reads eccentricities and semi-major axes from published mean elements. Simpler than B-DNA's PDB coordinates but same shape.
3. **Luau setup script** (equations wall): second use after periodic table. Setup script pattern is proven.

## What's in the commits

Each sector got one commit for clean history:

- `feat(art): North Celestial sector batch — Blaeu + Rowley`
- `feat(art): Northeast Observation sector batch — Astrolabe + Telescopes`  (Prague clock blocked)
- `feat(art): East Cosmic sector batch — JPL + Spacetime`  (Gaia deferred)
- `feat(art): Southeast Energy sector — Chicago Pile-1 + Tesla + Michelson`
- `feat(art): South Machines sector — Babbage + robot arms`
- `feat(art): Northwest Hall of Minds — inventions + equations`  (statues blocked)

12 new ledger rows `REF-EXH-010` through `REF-EXH-021`, plus `REF-EXH-022` for the equations. `TASKS.md` and this handoff added.

## Deliberate simplifications, per-exhibit

Each dossier states its own; the common threads:

- **Materials** — brass throughout under D-016. Real objects are wood, cast iron, painted steel, painted concrete, coated aluminium — no exhibit matches its real material palette.
- **Overall proportions** either come from published dimensions (Blaeu 34 cm, Babbage 3.35 × 4.65 × 1.83 m, CP-1 7.6 × 7.6 × 6.1 m) or are display choices disclosed as such (JPL logarithmic scaling, telescope side-by-side compression, inventions compression).
- **Detail budget** — triangles are spent on silhouette-defining features, not surface complexity. Babbage has 8 wheels per column not 31; CP-1 has 15 display layers not 57.

## What now

**Next step is a bulk import + placement pass, spanning one session or two.**

Recommended workflow:
1. User opens Studio, publishes a checkpoint.
2. User imports all 12 GLBs at Scale Factor 1 in one Import Queue batch. Confirm each imports at the size the generator reports (dossiers list expected).
3. User tells me it's done.
4. I place all 12 meshes via MCP in one systematic pass, then run the equations setup script. Same pattern as every prior placement: `ChangeHistoryService` recording, `PrototypeOriginal*` attribute hiding (plus SurfaceGui `Enabled = false` on descendants), stone rename per accuracy doc, verify AABB + one collider, screen-capture at gameplay distance.
5. Batch handoff at the end of Phase 3.

After Phase 3: **21 of 24 exhibits shipped**. 3 remain:
- **Prague clock** — Q-018 blocked (era not locked)
- **Scientist statues** — Q-021 blocked (Curie identifiability)
- **Gaia star map** — deferred (dataset decision needed)

## What this did not do

- Not signed. All 13 exhibits stay `UNSIGNED` under Q-023.
- Not approved.
- Not placed. Studio place unchanged in this session (except commits to `docs/` and `art/`).
- No factual museum cards.
- **M1 still not advanced. Combat still does not exist.**

The M1 gap now has 8 exhibits committed since it was last flagged and 12 more waiting to place. That's a lot of exhibit throughput measured against zero combat progress. The user has been picking this direction with eyes open, and today's batch was explicit — but at some point M1 needs to happen or the arena stays a walkable museum.
