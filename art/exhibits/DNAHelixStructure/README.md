# B-DNA Double Helix (PDB 1BNA) — dossier

Sixth exhibit for the production pipeline. First from the Life & Computation
sector. Follows the research-dossier gate in
[OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

**Status: structure researched, geometry built, not imported and not approved.** No human has signed it off.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.Southwest_LifeAndComputation.DNAHelixStructure` |
| Visible name | **B-DNA DOUBLE HELIX — PDB 1BNA** (rename pending, currently `DNA HELIX STRUCTURE`) |
| Classification | Data-derived reconstruction — atom coordinates from a crystallographic structure |
| Primary anchor | **RCSB PDB entry `1BNA`** — Drew, Wing, Takano, Broka, Tanaka, Itakura, Dickerson, *Structure of a B-DNA dodecamer: conformation and dynamics*, Proc. Natl. Acad. Sci. USA **78** (1981) 2179–2183. DOI [10.1073/pnas.78.4.2179](https://doi.org/10.1073/pnas.78.4.2179) |
| Coordinates used | `data/1bna.pdb` — full ATOM record set (486 non-hydrogen atoms), fetched from `files.rcsb.org/download/1BNA.pdb` 2026-07-26 |
| Resolution of source | 1.90 Å |
| Sequence | `d(CGCGAATTCGCG)` — palindromic 12-mer, both chains |
| Geometry | 4,584 triangles, 2,408 vertices, 17.49 × 18.97 × 51.63 studs, one `MeshPart` |
| Construction | Parametric, `generate.py`, driven by the vendored PDB coordinates |
| Display scale | **1 stud = 0.75 Å** (1.329 studs per Å). Real helix ~40.8 Å tall → 51.6 studs, fills envelope |
| Rights | Geometry original. PDB data is freely reusable; primary citation carried in dossier and factual card |
| Gameplay fit | Replaces 71 primitive parts (Pair1..10, A1..10, B1..10 plus 41 `VisualDetail` children) with one `MeshPart` |
| Review | **UNSIGNED** |

## What the source establishes

PDB 1BNA was the **first high-resolution crystal structure of B-form DNA**, published in 1981 and still one of the most-referenced structures in molecular biology. The structure was solved by X-ray diffraction at 1.90 Å resolution.

Key features from the deposited coordinates and the primary paper:

- **12 base pairs** in each chain (both 5'→3' `CGCGAATTCGCG`)
- **Palindromic sequence**: chain B is the reverse complement of chain A, so chain A residue *i* pairs with chain B residue (13 − *i*)
- **Right-handed double helix** — the standard B-form
- Approximately **10 bp per helical turn**, so ~36° twist per base
- Approximately **3.4 Å rise per base pair**, so the 12-bp helix is ~40.8 Å long from first to last base
- Approximately **20 Å diameter**

## Render style — ribbon + rungs

Two "ribbons" trace the sugar-phosphate backbones through the C1' atoms of each residue; twelve "rungs" join paired C1' atoms across the helix. This is the standard biology-textbook rendering of DNA (schoolbook diagrams, protein-database cartoons) and it gives an unambiguous double-helix silhouette at gameplay distance.

The C1' atom was chosen as the backbone control point because:

- It exists in every residue (unlike the phosphate P, which is missing on the 5' terminal residue of each chain).
- It sits at the sugar-base junction, so joining paired C1' atoms across the helix produces rungs of realistic length.

Two alternatives were considered and rejected in the plan (approved by the user):

- **Per-atom ball-and-stick.** 486 non-hydrogen atoms × ~72 tri per low-poly sphere = ~35k triangles, over the 20k cap unless split across multiple meshes. Reads as noise from the arena floor even with splitting.
- **Van der Waals space-filling.** Every atom at its VdW radius. Reads as a solid twisted cylinder, obscures the double-helix shape entirely.

## What is accurate

- **Real coordinates from a published crystal structure**, not idealised parameters.
- **Right-handedness** and **twist rate** emerge from the coordinates themselves — nothing is imposed.
- **Palindromic pairing** — chain A residue *i* pairs with chain B residue (13 − *i*), matching the natural pairing of the CGCGAATTCGCG dodecamer.
- **12 base pairs at the correct spacing** — the 51.6-stud helical height corresponds to ~38.8 Å (12 rungs × 3.23 Å average rise) at the 1.329-stud-per-Å scale, close to the textbook 3.4 Å/bp.
- **Helical axis aligned to vertical** — computed from the coordinates (first C1' of chain A to last C1' of chain A), not hard-coded. The first draft of the generator hard-coded a PDB axis swap and produced a horizontally oriented helix; that was fixed.

## What is interpretation

- **Materials.** Real DNA has no colour. This uses brass for backbones under D-016. Base pairs will be coloured in Studio to visually distinguish A-T (2 hydrogen bonds) from G-C (3 hydrogen bonds), but the colour choice is a display convention.
- **Backbone smoothness.** Real backbones are curves through many atoms per residue; this uses one C1' per residue, so the backbone is 12-segment polyline, not smooth. Visible at close range as slight kinks at each residue.
- **Base geometry.** The rungs are simple cylinders with no representation of the aromatic base rings themselves. A ball-and-stick or ribbon-with-bases approach would show more of the base structure at the cost of triangle budget.
- **Absolute scale.** Set by the exhibit envelope, then disclosed as ~0.75 Å per stud.

## Rights

Geometry here is **original**, generated from freely reusable PDB coordinates. The primary citation (Drew et al. 1981) is carried in this dossier and must appear on the factual museum card.

Recorded in [ASSET_PROVENANCE_LEDGER.md](../../../docs/ASSET_PROVENANCE_LEDGER.md) as `REF-EXH-008`.

The vendored `data/1bna.pdb` is checked into the repository so the build is fully reproducible without network access, and so a diff of the source file would be visible if the coordinates ever change (they will not — the PDB entry is stable).

## Remaining before this can ship

1. A human review signature (Q-023).
2. The factual museum card, disclosing the 0.75 Å-per-stud scale and citing Drew et al. 1981.
3. Rename the visible stone `DNA HELIX STRUCTURE` → `B-DNA DOUBLE HELIX — PDB 1BNA` per the accuracy doc.
4. Consider a "base rings" pass — thin discs perpendicular to the rungs at each C1' — if the ribbon-only look is judged too abstract by a reviewer.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/DNAHelixStructure/generate.py \
  -- --out art/exhibits/DNAHelixStructure/build/DNAHelixStructure.glb
```

**Geometrically deterministic:** every run gives 4,584 triangles, 2,408 vertices and identical dimensions, driven by the vendored PDB coordinates. Fails the build on triangle cap, shell-overhang, or if the helix height deviates >20% from expected (a canary for axis-alignment regressions).

## Import settings

Scale Unit **Stud**, Scale Factor **1**, Anchored **on**, Collision Fidelity **Box**, no rig, merge off.

## History

**Built 2026-07-26.** Two rounds of correction:

**Round 1 — axis misalignment.** The first draft hard-coded a PDB Y → Blender Z swap. The 1BNA crystal frame doesn't cleanly align the helical axis with any of PDB X/Y/Z, so the helix landed horizontally and the depth assert caught it (51.76 studs overhanging the 31.50 shell). The fix computes the helical axis directly from the coordinates (first C1' of chain A to last) and rotates to align with Z — robust to whatever crystal-frame orientation any future PDB entry happens to use.

**Round 2 — invisible ribbons.** The first backbone approach used Blender NURBS curves with a bevel curve for tube geometry. After convert-to-mesh, the ribbon meshes had zero vertices — the bevel geometry didn't materialise. Replaced with segmented cylinders between consecutive C1' atoms plus a small sphere at each junction. Same approach as the rungs use, robust and readable at gameplay distance.

Both defects would have shipped without the render-the-export step. The first was caught by an assert (the height check); the second wasn't — it produced a valid mesh under the triangle cap that would have imported cleanly and looked wrong in the arena.
