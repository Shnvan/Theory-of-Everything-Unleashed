# Black-Hole Accretion-Disk Visualisation — dossier

Third pilot exhibit for the production pipeline. Follows the research-dossier gate in
[OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

**Status: physics researched, geometry built, not imported and not approved.** No human has signed it off.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.West_GravityAndSpaceflight.BlackHoleGenerator` |
| Visible name | **Must change — the current stone violates an acceptance criterion.** See below |
| Classification | **Visualisation of a physical model**, not a replica of an object |
| Primary anchor | NASA Scientific Visualization Studio depictions of a Schwarzschild black hole with a thin accretion disk |
| Geometry | 12,016 triangles across **4 objects**, 35.00 × 34.58 × 20.21 studs |
| Construction | Parametric, `generate.py`, geometrically stable across runs |
| Rights | Geometry original. NASA SVS material is **public domain**, and none is copied regardless |
| Gameplay fit | Replaces 68 primitive parts with 4 `MeshPart`s. Collision shell untouched |
| Performance target | 12,016 tri total, max 4,960 per mesh, against a 20,000 per-mesh cap |
| Review | **UNSIGNED** |

## The visible name violates an acceptance criterion

The stone currently reads **`BLACK-HOLE GENERATOR`**.

[OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md) requires this exhibit to be *"never described as generating a black hole"*, and lists as an acceptance condition that *"visible signs contain no fictional machine presented as real."* The current stone fails both.

`GravityControlChamber` has the identical defect — its target is a Cavendish torsion balance, *"never described as controlling gravity."*

**Neither stone has been renamed here.** Both change player-visible text, so they are surfaced for a decision rather than changed quietly. The internal Studio identity `BlackHoleGenerator` is fine to keep; it is only the sign that makes a claim.

## Why "accurate" means something different here

The armillary sphere and the beam engine are replicas: there is a real object, and fidelity means matching it. This exhibit has no object. It depicts a **physical model**, so accuracy means the *physics reads correctly* — and it is checkable against theory rather than against a catalogue record.

Four features distinguish a black hole from a glowing hoop. All four are present.

## What is accurate

**1. The black sphere is the shadow, not the event horizon.** Light bending makes the horizon appear about **√27 ⁄ 2 ≈ 2.598×** its true radius, so the dark region a distant viewer sees is far larger than the horizon itself. The generator draws the shadow at 6.50 studs and reports the implied horizon at 2.50. This distinction is routinely conflated, and getting it right is exactly the point of an exhibit that exists to teach.

**2. The photon ring hugs the shadow's edge** — light that orbited the hole at least once before escaping, at a radius just outside the shadow.

**3. Gravitational lensing warps the disk.** This is the defining visual, and the reason a torus primitive will not do. The disk is built as a swept annulus in which each radial ring is rotated about the viewing axis by an angle that decays with radius. Because the rotation applies to `y = r·sin(u)`, the far half lifts **above** the shadow and the near half drops **below** it, continuously and with no seam. The arc-over-the-top emerges from the construction rather than being sculpted in.

The generator **asserts that the arc actually clears the shadow** — it peaks at 8.81 studs against a 6.50 shadow. Without that assert, a future tweak to the bend constants could quietly flatten the exhibit back into a tilted annulus that teaches nothing.

**4. Doppler beaming brightens the approaching side.** Geometry cannot express brightness, so the disk exports as **two halves**, split where orbital velocity points at the viewer — `cos(u) < 0`, the `x < 0` half. Studio assigns the brighter material to `BlackHole_DiskApproaching`.

That four-object split is a **physics requirement, not a triangle-budget workaround**: it is what makes Doppler asymmetry and the black-against-emissive contrast expressible at all. The beam engine, by contrast, fits in one mesh comfortably.

## What is interpretation

- **The photon ring only reads correctly from the front.** In reality it is a projection effect and always faces the observer. A fixed ring in a 3D exhibit cannot do that. It is oriented to the primary approach direction, and from the side it will read as an edge-on hoop. A real limitation, recorded rather than hidden.
- **The bend profile is chosen to look right, not integrated from geodesics.** The exponential falloff reproduces the published appearance; it is not a ray-traced solution of the Schwarzschild metric.
- **Absolute scale.** Set by the exhibit envelope. A real black hole's disk extends far beyond what any envelope allows, so the outer radius is a display decision.
- **Disk inner radius.** Placed outside the shadow at a plausible lensed-ISCO position; not computed.
- **Doppler split at exactly half.** The real brightness gradient is smooth around the disk, not a two-step function.
- **No relativistic jet, no photon-ring sub-images, no secondary lensed images.** Omitted for legibility at gameplay distance.

## Rights

Geometry here is **original**, authored from published descriptions of the physics. No NASA media is copied.

**NASA SVS material is public domain** — *"All of our content is in the public domain (unless otherwise noted), meaning that it is free to download, use, and redistribute for whatever purposes you see fit."* Two caveats checked rather than assumed:

- some visualisations carry **licensed music that is not public domain**, though the visuals remain so;
- NASA's media guidelines separately restrict the **NASA insignia** and forbid implying NASA endorsement.

Neither caveat bites here, because nothing is copied and no NASA branding appears. Recorded in [ASSET_PROVENANCE_LEDGER.md](../../../docs/ASSET_PROVENANCE_LEDGER.md) as `REF-EXH-005`.

## Remaining before this can ship

1. **Rename the visible stone** so it stops presenting a fictional machine as real. Blocks release, not just approval.
2. A human review signature (Q-023).
3. The factual museum card, stating the shadow-versus-horizon distinction explicitly — it is the most valuable thing this exhibit can teach.
4. Materials in Studio: Neon for the disk halves and photon ring under D-016's science-energy accent allowance, and a true black non-reflective surface for the shadow.
5. Decide whether `GravityControlChamber` is renamed in the same pass.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/BlackHoleGenerator/generate.py \
  -- --out art/exhibits/BlackHoleGenerator/build/BlackHoleGenerator.glb
```

**Geometrically deterministic:** every run gives 12,016 triangles across 4 objects and identical dimensions. The generator fails the build if any mesh exceeds 20,000 triangles, if the assembly overhangs the collision shell, or if the lensed arc fails to clear the shadow.

## Import settings

Scale Unit **Stud**, Scale Factor **1**, Anchored **on**, Collision Fidelity **Box**, no rig, merge off. The import produces **four** `MeshPart`s, all of which belong to this exhibit.

## History

**Built 2026-07-26.** Two defects, both found by rendering the export rather than by reading the generator's output — the same lesson the beam engine produced an hour earlier.

**The disk came out as a funnel.** The lensing bend decayed over too wide a radial range, so every ring was tilted somewhat and the surface became a smooth bowl. The real appearance is a disk that is **flat almost everywhere** with a **narrow arc** hugging the shadow. Shortening the falloff from 3.6 to 1.25 fixed it, and radial samples were redistributed quadratically toward the inner edge so the arc is not faceted.

**The photon ring was lying flat.** It was built rotated 90° to face the viewer, then a blanket `rotation_euler` assignment applied the disk tilt to every object and **overwrote** that rotation. The ring became a belt around the shadow's waist instead of a circle outlining its edge. Its orientation is now baked into mesh data before the tilt is applied.

Both defects passed every assert the generator had. Neither was visible in the numbers.
