# JPL Solar System Orbits — dossier

Data-derived scientific reconstruction. Part of the 2026-07-26 batch.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.East_CosmicVisualization.PlanetaryOrbitPlatforms` |
| Visible name (pending rename) | **JPL SOLAR SYSTEM ORBITS** |
| Primary anchor | NASA / JPL published mean orbital elements ([ssd.jpl.nasa.gov/planets/approx_pos.html](https://ssd.jpl.nasa.gov/planets/approx_pos.html)) |
| Geometry | 10,424 triangles, 34.00 × 34.00 × 4.00 studs, one `MeshPart` |
| Rights | Original geometry. Ledger row `REF-EXH-014`. NASA JPL data is public domain |
| Review | **UNSIGNED** |

## Composition

A **flat brass platform** with 8 concentric Keplerian ellipses drawn as thin segmented cylinder rings — one per planet. Sun at the shared focus, raised slightly above the platform. A planet marker on each orbit.

## What is accurate

- **Real orbital elements** from JPL published mean values:

  | Planet | a (AU) | e |
  |---|---:|---:|
  | Mercury | 0.387 | 0.206 |
  | Venus | 0.723 | 0.007 |
  | Earth | 1.000 | 0.017 |
  | Mars | 1.524 | 0.093 |
  | Jupiter | 5.203 | 0.048 |
  | Saturn | 9.539 | 0.056 |
  | Uranus | 19.19 | 0.046 |
  | Neptune | 30.07 | 0.010 |

- **Ellipses are drawn with real eccentricity** applied to their radial scale. Mercury's visibly-non-circular ellipse and Neptune's near-circular one both come from the JPL values.
- **Kepler order** and inclusion of all 8 major planets.

## What is interpretation (disclosed)

- **Base-10 logarithmic radial scaling.** Real Neptune orbits at 78× Mercury's semi-major axis; at linear scale Mercury would vanish. Display uses `r_display = R_MIN + (R_MAX - R_MIN) * log10(a / a_Mercury) / log10(a_Neptune / a_Mercury)`. **Factual card must state this**, per the accuracy doc's requirement to "disclose any logarithmic or educational display scaling".
- **Planet sizes are not to scale** — chosen to be visible on the display without dominating the orbit lines.
- **Sun is not at the ellipse focus in this display.** Ellipses are centred at the geometric origin for simplicity, and the Sun sphere sits at that origin. Real Kepler orbits have the Sun at one focus, offset from geometric centre by `a·e`. Fixing this would help legibility for high-e Mercury; noted as a follow-up.
- **Planet positions are static and chosen for visual clarity** — a real ephemeris pose at a specific UTC epoch would place planets in specific angular positions; this generic pose is not an ephemeris snapshot. If a reviewer wants a specific epoch, the generator can trivially compute mean anomalies from JPL J2000 elements.
- **Materials.** Brass throughout under D-016.

## Remaining before this can ship

1. Human review signature (Q-023).
2. Rename stone `PLANETARY ORBIT PLATFORMS` → `JPL SOLAR SYSTEM ORBITS`.
3. Factual card must disclose the logarithmic scaling and cite JPL Horizons.
4. Consider fixing Sun-at-focus placement.
5. Consider computing planet positions at a specific UTC epoch, recorded on the card.
