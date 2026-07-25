# Boulton and Watt Rotative Beam Engine — dossier

Second pilot exhibit for the production pipeline. Follows the research-dossier gate in
[OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

**Status: structure researched, geometry built, not imported and not approved.** No human has signed it off.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.South_Machines.SteamEngine` |
| Visible name | To be set — see "Remaining before this can ship" |
| Classification | Named replica — **structure**; proportions largely interpretation |
| Primary anchor | Science Museum Group object **`1861-46`**, Boulton and Watt, Birmingham 1788 — the *Lap Engine* |
| Dimension source | **Wikipedia, not the museum record** — see the provenance warning below |
| Geometry | 3,512 triangles, 1,848 vertices, 41.75 × 18.00 × 56.60 studs, 1 `MeshPart` |
| Construction | Parametric, `generate.py`, geometrically stable across runs |
| Rights | Geometry original. Museum imagery is **reference only** — CC BY-NC-SA 4.0, NC bars commercial use |
| Gameplay fit | Replaces 50 primitive parts with 1 `MeshPart`. Collision shell untouched |
| Performance target | 3,512 tri against a 20,000 per-mesh cap and a 500,000 arena budget |
| Review | **UNSIGNED** |

## This replaces a locomotive, not a rough beam engine

The prototype in the place was built from `Boiler`, `Firebox`, `Stack`, `Wheel1` and `Wheel-1`. That is a **locomotive**. Object `1861-46` is a **stationary rotative beam engine** — a rocking beam on a raised pivot, a vertical cylinder at one end, a sun-and-planet gear and flywheel at the other. There is no boiler, no chimney and no wheels in its silhouette.

So this is a replacement rather than a refinement, and the old footprint was shaped for the wrong class of object.

## Provenance warning — read before citing any number

The museum object record for `1861-46` **gives no measurements at all**. It has no overall size, no bore, no stroke, no flywheel diameter and no power output.

The **bore of 18.75 in (47.6 cm) and stroke of 4 ft (1.2 m)** used here come from the **Wikipedia article "Lap Engine"**, which cites the museum accession number but does not cite a technical document for those two figures. They are therefore **secondary-source figures that have not been confirmed against a primary record**, and they are weaker evidence than the armillary sphere's dimensions, which came directly from the museum's own record.

The plan for this pilot originally called them "verified specifics". That was overstated, and correcting it is the point of this section. **The factual museum card must not present these as measured.**

## What the sources establish

**Primary — object `1861-46`** (Science Museum Group record):
- Boulton, Watt & Company, Birmingham, **1788**
- Materials **wood (unidentified) and cast iron** — note, *not* brass
- **"The oldest essentially unaltered rotative engine in the world"**
- Carries the **sun-and-planet gear**
- The **first engine fitted with a centrifugal governor**
- Drove **43 metal-polishing ("lapping") machines** at Matthew Boulton's Soho Manufactory for **70 years**
- By 1800 Boulton and Watt had built 451 engines, 268 of them rotative
- On display in the Science Museum's Energy Hall

**Secondary — Wikipedia, "Lap Engine":**
- One cylinder, **bore 18.75 in**, **stroke 4 ft**
- Parallel motion, rotative drive via sun-and-planet, centrifugal governor

## What is accurate

- **Bore-to-stroke ratio 2.561**, asserted in the generator so it cannot silently regress. This is the only real dimensional relationship in the model — subject to the provenance warning above.
- **Sun-and-planet gear**, with the planet wheel fixed to the connecting rod and meshing with a sun wheel on the flywheel shaft at a centre distance equal to the sum of their radii. Invented by William Murdoch and patented by Watt in 1781 to avoid the crank patent; the feature that makes this engine historically significant.
- **Parallel motion** as a closed linkage under the beam end, which is what keeps the piston rod travelling straight while the beam end swings on an arc.
- **Separate condenser** — Watt's founding invention — present as a distinct vessel beside the cylinder rather than merged into it.
- **Centrifugal governor**, correct for this engine specifically, since it was the first to carry one.
- Structural order: bedplate, entablature columns, beam pivoted centrally, cylinder under one end, flywheel under the other.

## What is interpretation

Stated plainly, because the factual card must not claim otherwise:

- **Overall dimensions.** Not documented anywhere found. Everything except the cylinder's proportions is scaled from the exhibit envelope. **The whole object's size is invented**, and the card must disclose it as a display scale rather than a measurement.
- **Materials.** The real engine is **wood and cast iron**. This is authored for the arena's brass-and-dark-stone palette under D-016. A deliberate art choice, **not an accuracy claim**. Early Watt beams were commonly *wooden*, so the material gap here is larger than it was on the armillary sphere.
- **Flywheel diameter, spoke count, beam profile, column count and spacing.** All plausible for the type, none measured.
- **Beam held level.** The real beam rocks. D-016 keeps exhibits static, and a frozen mid-stroke pose reads as broken rather than paused.
- **Condenser and air-pump sizing and placement.** Kept inboard of the cylinder, which is both typical of the type and required by the collision shell.

## Rights

Geometry here is **original**, authored from published descriptions. No museum media is copied.

**Science Museum Group imagery for `1861-46` is CC BY-NC-SA 4.0.** The NC clause makes it unusable in a commercial game. It may inform geometry; it may never ship. Recorded in [ASSET_PROVENANCE_LEDGER.md](../../../docs/ASSET_PROVENANCE_LEDGER.md) as `REF-EXH-003`. The Wikipedia article supplying the bore and stroke is `REF-EXH-004`; its text is CC BY-SA 4.0, but only two numeric facts are used, not prose.

## Remaining before this can ship

1. A human review signature (Q-023).
2. The factual museum card, disclosing the display scale and **not** presenting the bore and stroke as measured.
3. The real-name stone replacing the prototype inscription.
4. Ideally, a primary source for the bore and stroke, to retire the provenance warning above.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/SteamEngine/generate.py \
  -- --out art/exhibits/SteamEngine/build/SteamEngine.glb
```

**Geometrically deterministic:** every run gives 3,512 triangles, 1,848 vertices and identical dimensions. The generator fails the build if the mesh exceeds 20,000 triangles or overhangs the collision shell.

Not byte-identical between runs — `join()` orders elements unstably. Verify the printed figures, not a file hash. See [art/README.md](../../README.md).

## Import settings

Scale Unit **Stud**, Scale Factor **1**, Anchored **on**, Collision Fidelity **Box**, no rig, merge off.

## History

**Built 2026-07-26.** Two rounds of correction, both caught by rendering the mesh rather than by reading the generator's numbers.

**Round 1 — the asserts were checking the wrong envelope.** The first mesh measured 54.66 studs wide and passed, because the check compared against the *exhibit extents* (70.66). The binding constraint is the **collision shell** at 43.20, since only the shell is solid — geometry outside it is walked through rather than walked around. Overhang was 11 studs. The asserts now check the shell, and print the remaining margin.

**Round 2 — three defects visible only in a render.** An orthographic preview of the exported GLB showed:

- the **parallel motion** was two angled bars touching nothing, reading as damage rather than a linkage. Rebuilt as a closed parallelogram hung from the beam end and meeting the piston rod.
- the **beam was a thin slab**. It is the feature the engine is named for, so it was deepened into a lozenge profile.
- the **governor was hidden behind the columns**, its balls reading as two beads floating inside the frame. Moved in front of the frame at belt height from the flywheel shaft, which is where it was actually driven from. It then landed directly over the flywheel centre and was moved again into the gap between cylinder and flywheel.

The lesson matches the armillary sphere's: **the numbers passing is not evidence the object is right.** Rendering the export is cheap and catches a class of error no assert expresses.
