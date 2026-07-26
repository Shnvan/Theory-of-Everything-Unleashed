# Babbage Difference Engine No. 2 — dossier

Named reconstruction replica. Part of the 2026-07-26 batch.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.South_Machines.GiantGearsAndMachinery` |
| Visible name (pending rename) | **BABBAGE DIFFERENCE ENGINE NO. 2** |
| Primary anchor | Charles Babbage's 1847-1849 design as first constructed by the Science Museum in 1991, SMG object `1992-556` |
| Real dimensions | **3.35 m × 4.65 m × 1.83 m**, ~8,000 parts, ~5 tonnes |
| Geometry | 5,148 triangles, 39.70 × 16.64 × 28.60 studs, one `MeshPart` |
| Display scale | 8.0 studs/m |
| Rights | Original geometry. Ledger row `REF-EXH-019` |
| Review | **UNSIGNED** |

## Composition

- **Seven vertical columns of gear wheels** — the calculating registers, each column a stack of 8 disc-wheels on a shaft
- **Structural frame** — corner posts + top and bottom rails on both sides
- **Printer housing** on the left with a paper roll on top
- **Hand crank** on the right side at operator height
- Base plate under the whole engine

## What is accurate

- **Seven columns of wheels** matches the real DE#2 calculating mechanism.
- **Printer on the left** — the DE#2 printer is a real distinct sub-assembly.
- **Hand crank on the right** — the engine is manually driven.
- **Rectangular frame structure** — the DE#2 is a frame-mounted engine, not a cabinet-enclosed object.
- **Overall proportions** (~4.65 m wide × 3.35 m tall × 1.83 m deep) come from published Science Museum figures.

## What is interpretation

- **8 wheels per column instead of the real 31.** Reduced to stay under the 20,000 triangle cap while keeping the columns visually dense. First attempt at 12 wheels + tooth rings hit ~31k triangles; tooth rings were dropped.
- **No visible gear teeth.** At gameplay distance the disc-stacks read as gear columns; teeth would need a texture or dense geometry.
- **8,000 parts → ~65 parts.** DE#2 has thousands of individually machined bronze components. Simplified to a silhouette-preserving frame.
- **Materials.** Real DE#2 is bronze on cast iron; rendered in brass under D-016.
- **Printing mechanism is a plain box + paper roll.** Real printer has type-setting bars, ink, and paper transport — none of that is modelled.
- **No output tray, no zeroing mechanism, no carry-warning bell.** Simplified.

## Remaining before this can ship

1. Human review signature (Q-023).
2. Rename stone `GIANT GEARS & MACHINERY` → `BABBAGE DIFFERENCE ENGINE NO. 2`.
3. Factual card: state the ~5-tonne, ~8,000-part real scale, cite Science Museum's 1991 construction, and disclose the wheels-per-column simplification.
