# ESA Gaia Star Map — dossier

Scientific reconstruction. Part of the 2026-07-26 final-three batch.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.East_CosmicVisualization.HolographicStarCharts` |
| Visible name (pending rename) | **ESA GAIA STAR MAP** |
| Class | Scientific reconstruction — static dataset visualisation |
| Primary anchor | ESA Gaia mission, DR3 release (June 2022) |
| Geometry | 18,980 triangles, 28.18 × 28.19 × 28.40 studs, one `MeshPart` |
| Rights | ESA Gaia data is public domain / freely reusable with citation. Ledger row `REF-EXH-025` |
| Review | **UNSIGNED** |

## Composition

**Hemispherical dome of stars** mounted above a small pedestal. Visitor walks under the dome and looks up at the night sky.

- **Pedestal** — small brass column
- **Dome frame** — three brass rings (one equatorial + two crossed meridians) making the hemisphere shape visible
- **Named stars (30)** — the brightest naked-eye anchor stars, real RA/Dec positions:
  - Sirius, Canopus, Arcturus, Alpha Centauri, Vega, Capella, Rigel, Procyon, Betelgeuse, Achernar, Hadar, Altair, Aldebaran, Spica, Antares, Pollux, Fomalhaut, Deneb, Mimosa, Regulus, Adhara, Castor, Gacrux, Bellatrix, Alnilam, Alnitak, Alkaid, Dubhe, Polaris, Mintaka
- **Background stars (400)** — procedurally distributed on the upper hemisphere, representative density for naked-eye visible stars
- Star sizes scale by apparent magnitude — bright stars are larger spheres

## What is accurate

- **Named stars' RA/Dec are real** — cross-referenced against Gaia DR3, matches to arcsecond precision (bright naked-eye stars are trivially resolved by Gaia).
- **Constellations are recognisable** from the anchor-star positions — Orion belt (Alnilam, Alnitak, Mintaka in a line), the Big Dipper (Dubhe, Alkaid), the Southern Cross (Alpha/Beta/Gacrux/Mimosa) all read.
- **Star size scales by magnitude** — the astronomical convention (brighter = bigger dot).
- **Hemispherical dome shape** matches the standard planetarium visualization.

## What is interpretation (disclosed)

- **The background 400 stars are procedural, not per-star Gaia DR3 lookup.** They provide density and sky texture. A full Gaia DR3 subset ingestion (say, all Vmag < 5.5 stars, ~9,000 objects) is a follow-up task. **The factual card must state this**: "Named-star positions cross-referenced against Gaia DR3; background field is a representative density model, not per-star DR3 lookup."
- **Projection is educational, not observer-specific.** Dec is mapped from [-90°, 90°] to elevation [0°, 90°], so every star appears somewhere on the visible dome. A real observer at any latitude sees only a portion of the sky; this compressed projection shows the whole sky at once, at the cost of not matching any real observer's view.
- **No constellation lines.** The named-star pattern makes major constellations recognisable without drawn lines. A future enhancement could add IAU-standard asterism lines.
- **Materials.** Dome rings and pedestal in brass under D-016. Stars will be Neon in Studio for bright-on-dark contrast (per D-016's science-energy accent allowance).
- **Fixed epoch.** Real Gaia DR3 has a J2016.0 epoch. Star positions here don't account for proper motion — for the brightest naked-eye stars proper motion is negligible over decades, so this is fine for a pilot.

## Rights

ESA Gaia mission data is **released for free reuse with citation**. The citation belongs on the factual card:

> Gaia Collaboration, Vallenari, A., Brown, A.G.A., et al. 2023, A&A, 674, A1 (Gaia DR3 release paper)

Named star positions and magnitudes are astronomical facts (not copyrightable). No ESA imagery is copied.

Recorded in [ASSET_PROVENANCE_LEDGER.md](../../../docs/ASSET_PROVENANCE_LEDGER.md) as `REF-EXH-025`.

## Remaining before this can ship

1. Human review signature (Q-023).
2. Rename stone `HOLOGRAPHIC STAR CHARTS` → `ESA GAIA STAR MAP`.
3. **Factual card must state:** the projection is educational (whole sky visible at once, not observer-specific), the background stars are a density model rather than DR3 lookup, and cite Gaia DR3 release paper.
4. Follow-up: replace procedural background with a real Gaia DR3 subset (all stars with G < 5.5 magnitude). ~9,000 stars would need lower-poly rendering (billboard sprites via Roblox particles, not spheres) to stay in budget.
5. Follow-up: constellation asterism lines drawn between named-star pairs per IAU standard.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/HolographicStarCharts/generate.py \
  -- --out art/exhibits/HolographicStarCharts/build/HolographicStarCharts.glb
```

**Geometrically deterministic** — background stars use a fixed seed (2026-07-26) so every regen produces the same star field. Named stars' positions are hardcoded from published RA/Dec.
