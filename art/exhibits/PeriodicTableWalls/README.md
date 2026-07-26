# IUPAC Periodic Table of the Elements — dossier

Seventh exhibit for the production pipeline. Second from the Life & Computation sector. Follows the research-dossier gate in [OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

**Status: content built, stone renamed, not signed.** No human has approved it.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.Southwest_LifeAndComputation.PeriodicTableWalls` |
| Visible name | **IUPAC PERIODIC TABLE OF THE ELEMENTS** (renamed 2026-07-26) |
| Classification | Data-derived display |
| Primary anchor | Current IUPAC list — `iupac.org/what-we-do/periodic-table-of-elements/` (accessed 2026-07-26) |
| Pipeline | **Not a Blender exhibit.** Committed source is `setup.luau`, run once via MCP `execute_luau` against the Edit datamodel |
| Content | One brass `Part` wall (60 × 45 × 5) + one `SurfaceGui` with 121 children (title + 118 element cells + 2 f-block placeholders) |
| Wall CFrame | Reuses the prototype `Wall` position/size/rotation exactly, so the exhibit footprint doesn't change (D-017) |
| Rights | Element data is factual (not copyrightable). IUPAC layout is a scientific convention (not copyrightable). No text or imagery copied |
| Gameplay fit | Replaces 16 prototype visual parts (Wall + 15 sample element cells) + 41 `VisualDetail` children with one `Part` and one `SurfaceGui` |
| Review | **UNSIGNED** |

## This is a new pipeline case, deliberately

The five earlier production exhibits (sphere, engine, black hole, Cavendish, Saturn V, B-DNA) are all mesh exhibits: `art/exhibits/<Exhibit>/generate.py` in Blender headless → GLB → user imports through Studio → I place via MCP. The periodic table doesn't fit that shape.

**The problem is text-and-data layout, not modelling.** A wall of 118 element cells with symbols, atomic numbers, atomic weights and category colours is a data-visualisation, not a geometry. Baking it as a texture in Blender would work but locks the typography in at a fixed pixel resolution and pushes text-rendering choices into the mesh pipeline. Studio's `SurfaceGui` with `TextLabel` children solves it natively: vector-scaled text stays crisp at any distance, colours are properties not baked pixels, and no texture asset needs uploading.

So this exhibit's "generator" is `setup.luau` — a committed Luau script that, run once through `execute_luau`, builds the wall and all its children. Idempotent: re-running it destroys any prior `ProductionMesh` first.

## What the source establishes

Element data below is transcribed from the current IUPAC list at [iupac.org/what-we-do/periodic-table-of-elements/](https://iupac.org/what-we-do/periodic-table-of-elements/), accessed 2026-07-26.

- **118 elements**, Z = 1 to 118
- Symbols, names, standard atomic weights, and IUPAC categorisation
- Standard 18-column layout: seven main rows plus lanthanide (57-71) and actinide (89-103) strips beneath
- Standard convention for elements with no stable isotope: mass number of the longest-lived isotope shown in brackets, e.g., `[98]` for Tc

## What is accurate

- **All 118 elements present**, correctly positioned in the standard IUPAC 18-column layout.
- **Category colouring:** alkali metals, alkaline earth metals, transition metals, post-transition metals, metalloids, nonmetals, halogens, noble gases, lanthanides, actinides, and "unknown" (for the recently synthesised superheavies whose chemistry hasn't been experimentally established).
- **F-block indicators** at row 6 col 3 and row 7 col 3, pointing to the lanthanide/actinide strips below — standard museum convention.
- **Atomic weights** taken directly from the current IUPAC values.
- **Bracketed mass numbers** for elements with no stable isotope, following the IUPAC convention.

## What is interpretation

- **Category colour palette.** Chosen for legibility on brass (pastel palette so black text stays readable). Any museum's specific palette is design choice, not data; IUPAC does not mandate a colour scheme.
- **Wall material and colour.** Brass, matching D-016. Real museum periodic tables are typically light-coloured backing panels or backlit acrylic; the arena palette overrides this.
- **Text on brass legibility.** Title is dark brown text on brass — adequate at gameplay distance but not crisp. Cell backgrounds are pastel so cell contents are always dark-on-light.
- **Font.** Roblox's built-in `SourceSans`/`SourceSansBold`. The default `1` glyph is unambiguous, and no custom typography is baked in.
- **No trend indicators.** Real museum periodic tables often include arrows and axes showing periodic trends (electronegativity, atomic radius, etc.). Omitted for the pilot.

## Rights

Element data and the IUPAC 18-column layout are both facts and are not copyrightable. No IUPAC text or imagery is copied — the atomic weights and category assignments come from the IUPAC page as facts, and the layout is a scientific convention that predates any single publication.

Recorded in [ASSET_PROVENANCE_LEDGER.md](../../../docs/ASSET_PROVENANCE_LEDGER.md) as `REF-EXH-009`.

## Remaining before this can ship

1. A human review signature (Q-023).
2. The factual museum card, disclosing:
   - IUPAC as the data source
   - The **date the data was accessed** (atomic weights and category assignments have been revised historically)
   - The colour palette as a display choice
3. Consider adding trend indicators (electronegativity gradient, atomic radius, etc.) if the flat 118-cell display is judged too plain by a reviewer.

## Regenerating

There is no `.glb` here. The source is Luau; re-run it against the Edit datamodel through the Roblox Studio MCP `execute_luau` tool, or paste the file contents into Studio's command bar. Running twice is safe (`existing ProductionMesh` is destroyed first).

Verification is self-reporting: the script returns triangle count, prototype-hidden count (57 parts), element cell count (should be 118), AABB delta (should be 0.0000 on every axis), collider count (should be 1: `PrimaryCollisionShell`), and the before/after stone text.

## History

**Built 2026-07-26.** Two defects fixed, both surfaced by the render step (D-036):

**The prototype `Wall` still had a `PeriodicTableDisplay` SurfaceGui rendering through the invisible Part.** Setting `Transparency = 1` on the Wall hid the Part itself but did nothing to its `SurfaceGui` child, which kept rendering over the top of my new content. Symptoms: a ghost row 8 duplicating period 7, and an overlaid title from the prototype that hid my "IUPAC" prefix. Fix: also set `Enabled = false` on every `SurfaceGui`/`BillboardGui` descendant of hidden prototype parts, and store the original `Enabled` state on the GUI itself as an attribute so restoration remains a one-liner. Committed to `setup.luau` so any future exhibit hiding this class of part gets the same treatment automatically.

**Missing f-block placeholders.** The prototype's SurfaceGui had happened to render `57-71` and `89-103` placeholders at row 6 col 3 and row 7 col 3; when I disabled the prototype's SurfaceGui the placeholders disappeared and the main table looked like it had two empty cells. Added explicit placeholder frames in the setup script so a re-run reproduces them.
