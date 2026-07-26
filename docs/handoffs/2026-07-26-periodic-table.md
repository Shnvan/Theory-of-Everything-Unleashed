# Handoff — IUPAC Periodic Table shipped; new pipeline capability proven

**Date:** 2026-07-26
**Scope:** New file `art/exhibits/PeriodicTableWalls/setup.luau` + dossier + ledger + `TASKS.md` + this file. Studio place updated.

Follows [2026-07-26-b-dna-placement.md](2026-07-26-b-dna-placement.md).

## What shipped

**IUPAC Periodic Table of the Elements** — `TheOmniscienceColiseum.ExhibitSectors.Southwest_LifeAndComputation.PeriodicTableWalls.ProductionMesh`. One brass Part wall (60 × 45 × 5, reusing the prototype Wall's exact CFrame per D-017) carrying one `SurfaceGui` with 121 children:

- Title `IUPAC PERIODIC TABLE OF THE ELEMENTS`
- **118 element cells**, each with atomic number, symbol, and standard atomic weight
- 2 f-block placeholder cells (`57-71` and `89-103`) pointing to the lanthanide/actinide strips below

Category-coloured (alkali metals, alkaline earth, transition, post-transition, metalloids, nonmetals, halogens, noble gases, lanthanides, actinides, unknown-superheavies).

Stone renamed: `PERIODIC-TABLE WALLS` → `IUPAC PERIODIC TABLE OF THE ELEMENTS`.

Data source: [iupac.org/what-we-do/periodic-table-of-elements/](https://iupac.org/what-we-do/periodic-table-of-elements/), accessed 2026-07-26 (`REF-EXH-009`). Element data and standard 18-column layout are both facts / scientific conventions and are not copyrightable; nothing is copied from IUPAC's page.

## New pipeline capability: Luau setup scripts

Every earlier production exhibit was Blender → GLB → import → MCP-place. This one is different because **the problem is text-and-data layout, not geometry**. A wall of 118 element cells with atomic weights and colour-coded categories fits Studio's `SurfaceGui` + `TextLabel` model natively: vector-scaled text stays crisp at any distance, colours are runtime properties not baked pixels, no texture asset needs uploading.

**The pattern established here:**

- `art/exhibits/<Exhibit>/setup.luau` — committed source of truth
- Run once via MCP `execute_luau` against the Edit datamodel to build the wall + GUI contents
- Idempotent: the script destroys any prior `ProductionMesh` first, so re-running is safe

This is now available for other data-and-layout exhibits. The AI lab (Exhibit 3 of this sector) may or may not use it — depends on whether it's mostly geometry or mostly screens.

## Two defects worth remembering

**Prototype `SurfaceGui` rendered through the invisible Wall Part.** Setting `Transparency = 1` hides a Part but does nothing to its `SurfaceGui` children — they keep rendering. Two symptoms in this exhibit: a ghost row 8 duplicating period 7, and an overlaid title from the prototype that hid my "IUPAC" prefix. Fix landed in `setup.luau`: when hiding a prototype part, also `Enabled = false` every `SurfaceGui`/`BillboardGui` descendant and store the original `Enabled` state on the GUI itself. Any future exhibit inheriting this pattern gets it for free.

**Missing f-block placeholders.** Standard museum periodic tables show `57-71` and `89-103` cells at row 6 col 3 and row 7 col 3, pointing at the lanthanide/actinide strips below. The prototype's SurfaceGui had happened to include those; disabling it removed them. Added explicit placeholder frames to `setup.luau`.

Both were caught by rendering and looking (D-036), not by any check the setup script performed. Sixth time the render step has surfaced a defect on this project.

## Verified

| Check | Result |
|---|---|
| Element cells present | 118 |
| Explicit axis-aligned AABB delta | 0.0000 on every axis |
| Colliders remaining | 1 (`PrimaryCollisionShell`) |
| Preserved children | `CollisionShells`, `Plinth`, `LabelAnchor`, `NamePlaque` intact |
| Prototypes hidden with attributes stored | 57 parts + prototype SurfaceGui |
| Visual read at gameplay distance | Full IUPAC table with categories, atomic numbers, symbols, weights — legible |
| Stone displays correctly | `IUPAC PERIODIC TABLE OF THE ELEMENTS` |

## What this did not do

- Not signed. `UNSIGNED` under Q-023.
- Not approved.
- Prototype parts hidden, not deleted.
- No factual card yet (needs date-accessed disclosure).
- No trend indicators (electronegativity, atomic radius, etc.) — could be added if reviewer wants richer content.
- **M1 still not advanced.** Combat still does not exist.

## Sector scoreboard

| Sector | Done | Remaining |
|---|---:|---|
| West Gravity & Spaceflight | 3/3 | — |
| Life & Computation | 2/3 | AI lab |
| Everything else | 2/? | ~17 exhibits |

**7 exhibits shipped**, ~17 remaining. Blockers Q-018 (Prague clock era) and Q-021 (Curie / Radiant Pioneer) still hold two of those.

## Next smallest thing

Continue Life & Computation with the **AI Computing and Robotics Laboratory** (third exhibit in the sector). Design-heavy, no single canonical source — the accuracy doc classifies it as a scientific reconstruction of a generic inference-server, networking, sensing, and robotics workflow, no fictional sentient core. Blender pipeline again for that one.

Alternatively: return to M1 combat.
