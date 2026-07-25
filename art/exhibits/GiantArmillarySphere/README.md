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

## Placement result — 2026-07-26

Placed into `North_CelestialHall.GiantArmillarySphere` as `ProductionMesh` at 148.12, 33.16, 164.50 — the prototype ring centre, not the Model bounding-box centre, which sits low because it includes the plinth and plaque.

The 67 prototype parts (26 ring parts at the Model root, 41 under `VisualDetail`) are **hidden, not deleted**. Each stores its original `Transparency` and `CanCollide` in attributes, so restoring them is a one-line script. They stay until this exhibit passes review, which it has not.

| Check | Result |
|---|---|
| Axis-aligned footprint | Unchanged, delta 0.0000 on every axis |
| Preserved children | `CollisionShells`, `Plinth`, `LabelAnchor`, `NamePlaque` all intact |
| Colliding parts in exhibit | Exactly 1 — `PrimaryCollisionShell` |
| Raycast through exhibit | Hits the shell, not the mesh |
| Reversibility | 67 hidden, 67 with stored originals |

Mesh set to `CanCollide = false`, `CanQuery = false`, `CollisionFidelity = Box`, `Material = Metal` in brass.

### A verification method that was wrong

The first check used `Model:GetBoundingBox()` and reported the footprint growing 4.43 studs in X and 7.99 in Z. That was **an artifact of the instrument, not a real change**: `GetBoundingBox` returns an *oriented* box, so adding any part can rotate the fit and produce a delta with nothing moving.

Recomputing an explicit axis-aligned box showed zero change on every axis. The exhibit's real extents are set by `TrimBack`, `TrimLeft`, and `InscriptionStone` — all pre-existing — and the mesh sits entirely inside them.

**Use an explicit AABB for footprint checks.** `GetBoundingBox` is not a stable measure across structural edits.

### Honest visual assessment

It reads as a real instrument rather than the 48 spheres it replaces. But at gameplay distance the ring set looks **busy** — the colures and tropics overlap into something closer to a ball of wire than a precise brass instrument.

That is a parameter problem, not a pipeline one: fewer rings, thinner bands, or a smaller `BAND_WIDTH_RATIO`. Worth tuning against real reference photography of object `1878-12` at the same time the proportions get verified, rather than guessing twice.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/GiantArmillarySphere/generate.py \
  -- --out art/exhibits/GiantArmillarySphere/build/GiantArmillarySphere.glb
```

**Geometrically deterministic:** three runs each produced 8,884 triangles, 4,450 vertices, and 45.62 × 52.49 × 45.62 studs. Check those printed figures, not a file hash — the GLB is not byte-identical between runs because `join()` ordering is unstable, and nothing depends on it being so. See [art/README.md](../../README.md).

## Import result — verified 2026-07-26

Imported through Studio's 3D Importer. `MeshPart.Size` measured **45.62, 52.494, 45.62** — an exact match for the generator's stated output.

Two corrections came out of that first import, both now fixed at the source:

- **Scale.** The generator had scaled by 0.01 on the documented belief that Roblox reads a Blender metre as 100 studs. It does not — with `Scale Unit: Stud`, one file unit is one stud. The pilot arrived 100× too small and needed a manual Scale Factor of 100. The generator now authors 1:1 and imports correctly at Scale Factor 1.
- **Naming.** The `MeshPart` arrived called `Torus`, because the importer names from the mesh *data* block rather than the object. The generator now sets both.
