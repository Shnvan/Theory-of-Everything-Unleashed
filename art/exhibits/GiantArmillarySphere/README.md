# Giant Armillary Sphere — dossier

Pilot exhibit for the production pipeline. Follows the research-dossier gate in
[OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

**Status: structure verified, not yet approved.** Proportions and construction now derive from the real object and a corroborating source. Materials are a deliberate art choice. No human has signed it off.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.North_CelestialHall.GiantArmillarySphere` |
| Visible name | DELLA VOLPAIA ARMILLARY SPHERE (1554) |
| Classification | Named replica — **structure**; materials are interpretation |
| Primary anchor | Science Museum Group object **`1878-12`**, Girolamo della Volpaia, Florence 1554 |
| Corroboration | della Volpaia's **1564** sphere, Museum of the History of Science, Oxford (Epact `18837`) |
| Geometry | 9,520 triangles, 4,780 vertices, 38.12 × 38.12 × 62.95 studs |
| Construction | Parametric, `generate.py`, geometrically stable across runs |
| Scientific content | Ptolemaic ring set — see below |
| Rights | Geometry original. Museum imagery is **reference only** — see Rights below |
| Display conversion | Real 500 × 300 × 300 mm → 62.95 × 38.12 × 38.12 studs, roughly **35× linear**. The factual card must disclose this |
| Gameplay fit | Replaces 71 primitive parts with 1 `MeshPart`. Collision shell untouched |
| Performance target | 9,520 tri against a 20,000 per-mesh cap and a 500,000 arena budget |
| Review | **UNSIGNED** |

## What the sources establish

**Primary — object `1878-12`:**
- **H 500 × W 300 × D 300 mm**, giving the 1.67:1 height-to-width ratio the model is built to
- Stand of **triple claw feet**
- Encloses a **manuscript terrestrial globe**
- Ptolemaic, Earth-centred
- Material **wood**; inscribed *"Hieronymus Carmilli Vulpariae, Florentin, F.1554"*
- Credit line: Myers and Son. On display in Science City

**Corroborating — the 1564 sphere, MHS Oxford:**
- Horizon circle in four 90° quadrants
- Polar caps, equator and tropics divided into degrees
- A **zodiac band** carrying sign names and symbols, **65 mm wide on a 700 mm instrument** — markedly wider than the plain circles
- Central sphere pierced by the inclined axis
- Turned and moulded base terminating in lions' paws

The 1564 object supplies the ring detail `1878-12`'s catalogue record omits, and confirms the ring set is della Volpaia's standard construction rather than a guess.

## What is accurate

**Astronomy** — real values, not decoration:
- Obliquity of the ecliptic **23.44°**
- Polar circles derived at **66.56°** (`90° − obliquity`)
- Tropics at **±23.44°**
- Latitude circles use radius `R·cos(δ)` at height `R·sin(δ)`, so they are genuine circles of declination
- Geocentric construction, correct for a Ptolemaic instrument

**Structure** — from the sources above:
- **1.67:1 proportion**, asserted in the generator so it cannot silently regress
- Triple claw feet
- Zodiac band roughly double the width of the plain circles
- Terrestrial globe at the centre, pierced by the polar axis
- Ring set: meridian, horizon, equator, both tropics, both polar circles, zodiac/ecliptic, two colures

## What is interpretation

Stated plainly, because the factual card must not claim otherwise:

- **Materials.** The real object is **wood**. This is authored for brass, because D-016 locks the arena to marble, dark stone, brass and glass, and wood is not in that palette. A deliberate art choice, agreed with the user, and **not an accuracy claim**.
- **Claw-foot carving.** The silhouette is right; the actual carving is not documented in the object record.
- **Band and ring thicknesses.** Guided by the 1564 zodiac-band ratio, not measured from `1878-12`.
- **Latitude tilt of 45°.** A plausible display angle, not read from the object.
- **Absolute scale.** Set by the exhibit envelope, then disclosed as a scale factor — which is what the accuracy doc requires.

## Rights

Geometry here is **original**, authored from published measurements. No museum media is copied.

**Science Museum Group imagery for `1878-12` is CC BY-NC-SA 4.0.** The NC clause makes it unusable in a commercial game. It may inform geometry; it may never ship. Recorded in [ASSET_PROVENANCE_LEDGER.md](../../../docs/ASSET_PROVENANCE_LEDGER.md) as `REFERENCE ONLY`.

## Remaining before this can ship

1. A human review signature (Q-023).
2. The factual museum card, with real dimensions and the disclosed ~35× scale.
3. The real-name stone replacing the current prototype inscription.
4. Confirm the ring count on `1878-12` specifically — the set used is della Volpaia's standard, evidenced by the 1564 object, not counted from photographs of the 1554 one.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/GiantArmillarySphere/generate.py \
  -- --out art/exhibits/GiantArmillarySphere/build/GiantArmillarySphere.glb
```

**Geometrically deterministic:** every run gives 9,520 triangles, 4,780 vertices, and identical dimensions. The generator fails the build if the ratio drifts more than 0.02 from 1.667 or the mesh exceeds 20,000 triangles.

Not byte-identical between runs — `join()` orders elements unstably — and that is not chased. Verify the printed figures, not a file hash. See [art/README.md](../../README.md).

## Import settings

Scale Unit **Stud**, Scale Factor **1**, Anchored **on**, Collision Fidelity **Box**, no rig, merge off.

## History

**First pilot, 2026-07-26.** Imported at 45.62 × 52.494 × 45.62 and placed. Three problems found and fixed at the source:

- The `0.01` export scale was backwards — with `Scale Unit: Stud`, one file unit is one stud, so the mesh arrived 100× small.
- The `MeshPart` imported named `Torus`; the importer names from mesh *data*, not the object.
- A byte-determinism claim was false. It held under `GLTF_SEPARATE` and was invalidated by the switch to GLB without re-testing.

**Retune, 2026-07-26.** Research produced the real dimensions, exposing a **1.15:1 proportion where the object is 1.67:1** — it read as a ball rather than a tall upright instrument. Rebuilt to the real ratio with claw feet, a differentiated zodiac band, and a proper globe.

The new ratio assert caught a further bug immediately: `join()` merges into `parts[0]`, the meridian ring, which carries a 90° rotation, so the merged object's local axes were swapped and `dimensions` reported height as Y. The geometry was right and the measurement was wrong. The generator now bakes the rotation in before measuring.

### Retune placement, verified

Re-imported at **Scale Factor 1** and measured `38.115, 62.948, 38.115` — an exact match, confirming the 1:1 authoring fix. The part arrived named `GiantArmillarySphere` rather than `Torus`, confirming the mesh-data naming fix. Both first-import bugs are dead.

Placed at 148.12, **39.636**, 164.50 — seated on the plinth top at Y 8.16 rather than centred on the old ring centre, because this object stands on feet.

| Check | Result |
|---|---|
| Axis-aligned footprint | Unchanged, delta 0.0000 on every axis |
| Envelope | Spans Y 8.16–71.11 against a 71.16 limit |
| Colliders in exhibit | Exactly 1, `PrimaryCollisionShell` |
| Preserved children | `CollisionShells`, `Plinth`, `LabelAnchor`, `NamePlaque` intact |
| In-world ratio | 1.652 |

Visually it now reads as a tall upright instrument on claw feet rather than a ball, and the wide zodiac band gives the ring set a legible hierarchy. The upper rings still cross busily; whether that is wrong is a question for reference photography, since real armillary spheres are genuinely dense with rings.
