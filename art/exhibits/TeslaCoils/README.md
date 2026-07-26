# Tesla Coil Apparatus — dossier

Scientific reconstruction. Part of the 2026-07-26 batch.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.Southeast_EnergyAndMatter.TeslaCoils` |
| Visible name (pending rename) | **TESLA COIL APPARATUS** |
| Class | Scientific reconstruction — generic spark-gap Tesla coil circuit |
| Geometry | 10,360 triangles, 32.00 × 18.70 × 40.10 studs, one `MeshPart` |
| Rights | Original geometry. No external reference (generic circuit). Ledger row `REF-EXH-017` |
| Review | **UNSIGNED** |

## Composition

Standard spark-gap Tesla coil, every element that a working coil has:

- **Wooden base** (rectangular platform)
- **Primary coil**: flat pancake spiral, rendered as 6 concentric toruses
- **Secondary coil**: tall thin cylinder mounted at primary centre, wound with 14 winding ridges hinting at fine wire coils
- **Top terminal**: large toroidal capacitor with breakout spike
- **Spark gap unit** on the base: housing with two electrode balls
- **Capacitor bank** on the base: box with two terminal posts
- **Ground wire** trailing off one edge

## What is accurate

- **Full circuit represented**: primary + secondary + capacitor bank + spark gap + top load + ground — every element the accuracy doc lists.
- **Ratio of secondary to primary height** is roughly right (tall thin secondary, short flat primary).
- **Toroidal top terminal** is the standard capacitance-topping shape.
- **Concentric-ring primary** matches the flat pancake spiral used in most bench and museum coils.
- **Spark gap on the base beside the coils** matches every historical and modern spark-gap Tesla coil arrangement.

## What is interpretation

- **Generic, not a named coil.** No specific Colorado Springs or Wardenclyffe geometry — this is a bench-scale representative apparatus, per the accuracy doc classification.
- **Materials.** Real coils are copper wire, wood formers, and ceramic insulators. Rendered in brass under D-016.
- **Primary is 6 concentric toruses** rather than a true spiral winding — reads as a spiral at gameplay distance.
- **Secondary "windings" are ridges**, not actual wound wire. A true wound secondary would need thousands of triangles.
- **No wiring shown** between components (leads from cap bank to primary, secondary base to ground, etc.).
- **No safety enclosure** or lightning cage.

## Remaining before this can ship

1. Human review signature (Q-023).
2. Rename stone `TESLA COILS` → `TESLA COIL APPARATUS`.
3. Factual card: state this is generic, not a named historical coil. Cite standard spark-gap Tesla coil references.
