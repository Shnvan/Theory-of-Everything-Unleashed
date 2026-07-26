# Blaeu Celestial Globe (1603) — dossier

Named replica. Part of the 2026-07-26 batch of 13 exhibits.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.North_CelestialHall.CelestialGlobe` |
| Visible name (pending rename) | **BLAEU CELESTIAL GLOBE (1603)** |
| Primary anchor | Willem Janszoon Blaeu's 1603 celestial globe, Amsterdam. Science Museum Group object `1980-1913`; corroborated by extant pairs at MHS Oxford, Met Museum, Vatican, and others |
| Real diameter | **34 cm** (Blaeu's 1603 pair standard) |
| Geometry | 4,356 triangles, 28.60 × 28.60 × 33.10 studs, one `MeshPart` |
| Display scale | 1 stud = 15.45 mm (globe 34 cm → 22 studs) |
| Rights | Geometry original. See ledger row `REF-EXH-010` |
| Review | **UNSIGNED** |

## What the sources establish

- **34 cm sphere diameter**, first published globe pair by Blaeu (celestial + terrestrial).
- **Papier-mâché over plaster** internal construction; 12 printed gores + 2 polar caps.
- **Wooden stand** with a horizon ring at globe-centre height, meridian ring, four turned columns and feet with cross-stretchers.
- Based on **Tycho Brahe's star catalogue**; first celestial globe to include the newly-mapped southern constellations from Dutch voyages.

## What is accurate

- **Sphere-plus-meridian-plus-horizon-ring construction** matches every surviving Blaeu library globe.
- **Four-column stand with splayed feet and cross-stretchers** — the standard 17th-century library-globe silhouette.
- **Polar axis** passes through the globe from top to bottom of the meridian ring.

## What is interpretation

- **Materials.** Real globe is coloured paper on plaster; stand is turned wood. Rendered in brass under D-016.
- **Stand ornament.** Real 1603 stands were more ornate (turned finials, decorative fluting). Rendered here as clean cylindrical columns with spherical finials.
- **Constellation surface.** Real globe has hand-coloured gores showing constellations, star magnitudes, and the ecliptic. Rendered as a plain sphere — texture and content are a later production pass.
- **Absolute scale.** Set by the exhibit envelope, disclosed as ~15.5 mm per stud.

## Remaining before this can ship

1. Human review signature (Q-023).
2. Rename stone `CELESTIAL GLOBE` → `BLAEU CELESTIAL GLOBE (1603)`.
3. Consider adding constellation surface content (texture or engraved lines) in a follow-up.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/CelestialGlobe/generate.py \
  -- --out art/exhibits/CelestialGlobe/build/CelestialGlobe.glb
```
