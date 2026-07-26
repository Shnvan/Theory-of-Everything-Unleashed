# Michelson Laser Interferometer — dossier

Scientific reconstruction. Part of the 2026-07-26 batch.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.Southeast_EnergyAndMatter.LaserExperimentChamber` |
| Visible name (pending rename) | **MICHELSON LASER INTERFEROMETER** |
| Class | Scientific reconstruction — laboratory Michelson-interferometer configuration |
| Geometry | 576 triangles, 36.00 × 24.00 × 15.75 studs, one `MeshPart` |
| Rights | Original geometry. Ledger row `REF-EXH-018` |
| Review | **UNSIGNED** |

## Composition

Standard Michelson interferometer on an optical bench:

- **Optical bench** (rectangular table on four legs)
- **Laser source** on a mount, aligned to the beam-splitter arm
- **Beam splitter** (cube at 45°) at the intersection of the two perpendicular arms
- **Two end mirrors** on mounts, one at the end of each arm, at right angles to each other
- **Detector** at the free end of the recombine arm
- **Beam paths** drawn as thin cylinders showing: laser→BS, BS→mirror A, BS→mirror B, BS→detector

## What is accurate

- **All five canonical elements present** (laser, beam splitter, two end mirrors, detector) — the accuracy doc's requirement.
- **Perpendicular arms** — the defining Michelson geometry.
- **Beam splitter at 45°** to both arms — correct orientation for splitting one input into two equal orthogonal beams.
- **Detector on the fourth port** — the recombine arm 90° from the input.
- **Beam paths shown** — helps the viewer trace the two interfering paths.

## What is interpretation

- **Table-top scale.** Real laboratory Michelsons range from ~30 cm arms (bench class) to ~4 km (LIGO). This is a bench-class layout with ~11-stud arms.
- **Materials.** Real optical benches are aluminium honeycomb tables; mirrors are silvered glass; laser is aluminium tube. Brass throughout under D-016. Beam paths will be Neon in Studio.
- **No vacuum chamber.** Real Michelsons in precision applications sit in a vacuum enclosure; not modelled.
- **No vibration isolation.** Real optical benches have air-legs or granite; here the legs are plain wooden columns.
- **No fringe pattern.** Real Michelsons produce circular or straight interference fringes at the detector; not modelled.
- **Beam splitter simplified.** Real broadband beam splitters have specific coatings and thicknesses; rendered as a plain cube.

## Remaining before this can ship

1. Human review signature (Q-023).
2. Rename stone `LASER EXPERIMENT CHAMBER` → `MICHELSON LASER INTERFEROMETER`.
3. Factual card: acknowledge this is a bench-class illustrative arrangement; reference LIGO for the industrial-scale application.
