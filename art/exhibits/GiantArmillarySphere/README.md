# Giant Armillary Sphere — dossier

Pilot exhibit for the production pipeline. Follows the research-dossier gate in
[OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

**Dossier status: INCOMPLETE.** Enough to validate the pipeline, not enough to ship. See the gaps below.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.North_CelestialHall.GiantArmillarySphere` |
| Visible name | DELLA VOLPAIA ARMILLARY SPHERE (1554) |
| Classification | Named replica |
| Primary anchor | Girolamo Della Volpaia's Ptolemaic armillary sphere, Science Museum Group object `1878-12` |
| Corroboration | **MISSING.** No second independent source consulted |
| Geometry | Generated: 8,884 triangles, 4,450 vertices, 45.62 × 52.49 × 45.62 studs |
| Construction | Parametric, `generate.py`, deterministic |
| Scientific content | Standard Ptolemaic ring set — see below |
| Rights | Original geometry, authored here. No external asset, so no ledger row needed *yet* — one becomes required if reference photography or a scan is used |
| Display conversion | Authored in studs, exported at 0.01 scale. **Not yet verified in Studio** |
| Gameplay fit | Replaces 71 primitive parts with 1 `MeshPart`. Collision shell untouched |
| Performance target | 8,884 tri against a 20,000 per-mesh cap and a 500,000 arena budget |
| Review | **UNSIGNED** |

## What is accurate

The astronomy is real, not decorative:

- **Obliquity of the ecliptic: 23.44°** — the actual tilt of the sun's apparent yearly path against the celestial equator.
- **Polar circles at 66.56°**, derived as `90° − obliquity`, which is what makes them the latitudes where the sun does not set at solstice.
- **Tropics at ±23.44°**, the declinations the sun reaches at the solstices.
- **Small-circle geometry**: each latitude circle has radius `R·cos(δ)` and sits at height `R·sin(δ)`. They are genuine circles of declination rather than evenly spaced hoops.
- **Geocentric construction** — Earth at the centre. Correct for a Ptolemaic instrument, and the reason this object is what it is.
- **Ring set**: meridian, horizon, equator, ecliptic, both tropics, both polar circles, and two colures at right angles through the poles. This is the standard armillary construction.

## What is invented

Stated plainly, because the factual card must not claim otherwise:

- **Every proportion.** Ring width, band thickness, and the ratio of meridian to equator are stylistic. They have **not** been checked against object `1878-12`.
- **The stand.** A stepped cylinder. The real instrument's mount has not been examined.
- **The 45° latitude tilt.** A plausible display angle, not read from the object.
- **Materials and colour.** None authored yet; Studio-side for now.
- **Overall scale.** Driven by the existing exhibit footprint, not by the real object's dimensions with a disclosed scale factor — which is what the accuracy doc actually requires.

## Gaps before this can ship

1. Consult Science Museum Group object `1878-12` for real dimensions and ring proportions, and record the scale factor.
2. Find a second independent source.
3. Confirm the number and arrangement of rings on the actual instrument — the standard set is used here, but Della Volpaia's may differ.
4. Verify imported size in Studio against the intended studs.
5. Write the factual museum card with the real dimensions and disclosed display scale.
6. Get a human review signature.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/GiantArmillarySphere/generate.py \
  -- --out art/exhibits/GiantArmillarySphere/build/GiantArmillarySphere.glb
```

Deterministic: two runs produced byte-identical output (SHA256 `60E9D485…`). If that stops being true, the script has stopped being the source of truth.
