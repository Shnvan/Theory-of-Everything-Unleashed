# Cavendish Torsion Balance — dossier

Fourth exhibit for the production pipeline. Follows the research-dossier gate in
[OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

**Status: structure researched, geometry built, not imported and not approved.** No human has signed it off.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.West_GravityAndSpaceflight.GravityControlChamber` (retained) |
| Visible name | **CAVENDISH TORSION BALANCE** (already renamed 2026-07-26) |
| Classification | Historical/scientific reconstruction — **structure**; case and proportions are interpretation |
| Primary anchor | Henry Cavendish, *"Experiments to determine the Density of the Earth"*, Philosophical Transactions of the Royal Society vol. 88 pp. 469–526, 1798 |
| Dimension source | Wikipedia's *Cavendish experiment* article, which cites the 1798 paper for every figure below |
| Geometry | 3,152 triangles, 1,620 vertices, 37.66 × 22.00 × 34.84 studs, one `MeshPart` |
| Construction | Parametric, `generate.py`, geometrically stable across runs |
| Display scale | **17× linear.** Real 1.83 m torsion rod → 31.11 studs. Real 1.98 m mahogany case → 33.66 studs. Real 0.30 m large ball → 5.10 studs |
| Small-ball enlargement | Real 51 mm → 0.87 studs at true scale, then **enlarged to 1.60 studs (~1.8× extra)** so they read at gameplay distance. Disclosed |
| Rights | Geometry original. Wikipedia text CC BY-SA 4.0 but only numeric facts are used, not prose |
| Gameplay fit | Replaces 14 primitive parts (`Chamber`, `Core`, `FieldRing_01..08`, plus `VisualDetail` children) with one `MeshPart` |
| Review | **UNSIGNED** |

## This replaces a fictional machine, not a rough one

The prototype it supersedes was built from `Chamber`, `Core`, and `FieldRing_01..08` — a science-fantasy energy chamber, not an apparatus. It also had the visible sign `GRAVITY-CONTROL CHAMBER`, which the accuracy doc lists as an acceptance failure: *"visible signs contain no fictional machine presented as real."* Both the stone and the geometry are wholesale replacements. Studio identity `GravityControlChamber` is kept only because D-017 requires the internal Model name to survive.

## What the primary source establishes

From Cavendish's 1798 paper, per Wikipedia's citation:

- **Torsion rod:** 6 ft / 1.83 m, horizontal, wooden
- **Small balls:** 2 in / 51 mm diameter, 1.61 lb / 0.73 kg lead, one at each rod end
- **Large balls:** 12 in / 300 mm diameter, 348 lb / 158 kg lead
- **Ball separation:** 8.85 in / 225 mm centre-to-centre between a small ball and its adjacent large ball
- **Mahogany case:** 1.98 m × 1.27 m × 0.14 m
- **Wire:** Cavendish switched to a "stiffer wire" after his third experiment; material and length not stated

The purpose: measure the tiny gravitational torque between the lead balls, from which Cavendish computed the density of the Earth — and hence, in modern terms, the gravitational constant *G*.

## What is accurate

- **Six-foot rod, 12-inch large balls, 2-inch small balls, 8.85-inch separation** — all at 17× linear scale, so the ratios between them are correct.
- **Ball geometry: large ball offset perpendicular to the rod** (in Y), not further out along the rod axis. This matters — gravitational torque requires the force to be *tangent* to the small ball's swing path, and the small ball swings in the XY plane about the vertical fibre. An earlier draft put the large balls further along X, which would produce no rotation. The generator asserts the rod-length proportion so this class of error can't regress silently.
- **Rod suspended by a thin fibre from directly above** — the physical mechanism.
- **Small balls at rod tips, large balls at same height** — the near-touching pose Cavendish used to maximise attraction.

## What is interpretation

- **The cabinet has no walls.** Cavendish's real enclosure was a mahogany box shielding the mechanism from air currents. That is a real reason in the lab and a bad reason in a museum exhibit — panels hide the very thing a visitor is here to see. This authors the cabinet as brass corner posts and rails only, with the mechanism exposed inside. The first draft had a solid rear panel and the render showed exactly nothing: the panel dominated the frame and every ball and rod hid behind it. **The exposed-frame version is not what Cavendish built; it is what a visitor needs to see.**
- **Materials:** brass frame and dark-lead balls, not mahogany and lead. D-016 locks the palette to marble, dark stone, brass and glass; wood is not in it.
- **Small balls enlarged ~1.8×.** At true 17× scale they are pinheads (0.87 stud) and unreadable at gameplay distance.
- **Fibre thickness (0.14 stud) is display-only.** The real fibre was fine enough that its thickness was never a display feature; here it is drawn thick enough to be visible from the arena floor.
- **Only one pair of large balls is drawn, both on the +Y side.** Real Cavendish alternated the two large balls to opposite sides of the rod, doubling the torque; this simplification keeps both large balls in a single view.
- **Fixed pose.** The real large balls could be rotated on their swing arm to bring them close to or far from the small balls. This is the "close" pose (the interesting one), held still.
- **Absolute size.** Set by the exhibit envelope, then disclosed as a 17× scale factor.

## Rights

Geometry here is **original**, authored from published measurements.

The numbers used come from **Wikipedia's *Cavendish experiment* article**, which cites the 1798 paper for each. Text is **CC BY-SA 4.0**; only numeric facts are used, not prose. Recorded in [ASSET_PROVENANCE_LEDGER.md](../../../docs/ASSET_PROVENANCE_LEDGER.md) as `REF-EXH-006`.

## Remaining before this can ship

1. A human review signature (Q-023).
2. The factual museum card, disclosing the 17× display scale, the small-ball enlargement, and the single-pair simplification.
3. Ideally, a primary source read for the wire specification, which the secondary source does not carry.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/GravityControlChamber/generate.py \
  -- --out art/exhibits/GravityControlChamber/build/GravityControlChamber.glb
```

**Geometrically deterministic:** every run gives 3,152 triangles, 1,620 vertices and identical dimensions. Fails the build on triangle cap or collision-shell overhang.

## Import settings

Scale Unit **Stud**, Scale Factor **1**, Anchored **on**, Collision Fidelity **Box**, no rig, merge off.

## History

**Built 2026-07-26.** Two rounds of correction, both caught by the render rather than by asserts.

**Round 1 — physics-wrong ball placement.** The first draft put the large balls further along the rod axis (`ROD_LENGTH/2 + BALL_SEP + LARGE_BALL_D/2`), which pushed the assembly 5.76 studs past the collision shell. The width assert caught the overhang; investigating the fix caught the deeper error — a large ball at ±X of the small ball produces no torque at all, since the force is along the rod rather than tangent to the swing. Corrected to the perpendicular-offset geometry.

**Round 2 — the cabinet hid the mechanism.** The first render showed a solid grey rectangle: the "rear panel" was on the negative-Y side, which the preview camera also sits on, so the panel occluded every rod and ball behind it. Rather than fix which side is rear, all panels were dropped — a museum exhibit's cabinet should show the mechanism, not hide it.
