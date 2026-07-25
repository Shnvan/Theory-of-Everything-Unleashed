# Exhibit art pipeline

Source geometry for the Omniscience Coliseum's 24 exhibits.

## The rule: scripts are the source, meshes are the build

For any exhibit whose geometry can be described mathematically, **the committed source is a Python script**, not a `.blend` file. `generate.py` runs in Blender headless and writes a glTF.

That buys four things a binary file cannot:

- **Reproducible** — regenerate identical geometry from a clean checkout
- **Reviewable** — a diff, not an opaque blob
- **Parameterised** — change a ring count or an angle by editing a number
- **No Git LFS** — the repository stays text

### What "deterministic" means here, precisely

**Geometrically deterministic: yes.** Every run produces the same triangle count, vertex count, and dimensions. That is what each generator prints, and it is what makes gitignoring the mesh safe — anyone regenerating gets the same object.

**Byte-identical: no, and not chased.** `bpy.ops.object.join()` merges in an order that is not stable across runs, so the exported file differs byte-for-byte while the geometry does not. Sorting mesh elements would not reliably fix it either: these models are highly symmetric, so a distance sort leaves large numbers of ties.

That is an acceptable trade because nothing depends on byte-identity — no mesh is committed, so there is no stored artifact to compare a rebuild against. **Verify the printed geometry figures, not a file hash.**

An earlier version of this document claimed byte-identical output. That was measured and true for the `GLTF_SEPARATE` format, then silently invalidated when the pipeline switched to GLB without re-testing.

`.blend` files and exported meshes are build artifacts and are gitignored. Only hand-sculpted exhibits — statues, ornate facades — need a committed binary, and those get LFS.

## Running a generator

```
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" ^
  --background --factory-startup ^
  --python art/exhibits/<Exhibit>/generate.py ^
  -- --out art/exhibits/<Exhibit>/build/<Exhibit>.gltf
```

`--factory-startup` matters: it ignores local Blender preferences so the output does not depend on whose machine ran it.

## Look at the export before importing it

```
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" ^
  --background --factory-startup ^
  --python art/tools/preview.py ^
  -- --glb art/exhibits/<Exhibit>/build/<Exhibit>.glb ^
     --out <somewhere>/<Exhibit>.png --axis front
```

**This step is not optional, and it is not the same as the asserts.** Asserts check dimensions, triangle counts and envelope fit. Every one of those can pass on an object that is visibly wrong.

Both the beam engine and the black hole passed every assert while carrying defects that a single render made obvious in seconds:

| Exhibit | Passed asserts | Actually wrong |
|---|---|---|
| Beam engine | ✓ | Parallel motion was two bars attached to nothing; governor hidden behind its own frame |
| Black hole | ✓ | Disk was a smooth funnel, not a flat disk with a lensing arc; photon ring lying flat |

The photon-ring bug is the clearest case: a blanket `rotation_euler` assignment silently overwrote the ring's own orientation. Dimensions, triangle count and envelope were all still correct.

`preview.py` renders the **exported GLB**, not the live scene, so it also confirms the export survived the round trip.

The general rule, learned three pilots running: **numbers passing is not evidence the object is right.**

## Units — one Blender unit is one stud

Author geometry 1:1 in studs. Apply no conversion. With the importer's **Scale Unit** set to **Stud** and **Scale Factor** at **1**, one file unit arrives as one stud.

**Verified by import, 2026-07-26.** A generator authored at 45.62 × 52.49 × 45.62 units produced a `MeshPart` measuring exactly `45.62, 52.494, 45.62`.

> This document previously stated the opposite — that Roblox reads a Blender metre as 100 studs, so generators should scale by `0.01`. **That was wrong.** It made the first pilot import 100× too small, needing a manual Scale Factor of 100 to undo. The rule above replaces it, and it is measured rather than sourced.

Still check it per exhibit. Read the imported `MeshPart.Size` and compare against the dimensions the generator printed. It costs one glance and catches the error class that would otherwise reach twenty-four exhibits.

## Import settings

| Setting | Value |
|---|---|
| Scale Unit | **Stud** |
| Scale Factor | **1** |
| Anchored | **On** — every exhibit part is anchored (D-016) |
| Rig Type | No Rig |
| Merge Meshes | Off |
| Collision Fidelity | Box — real collision comes from the exhibit's existing `CollisionShells` |

The importer names the `MeshPart` after the **mesh data block**, not the object, so generators set both. Otherwise the part arrives named after whichever primitive was active during the join.

glTF also wraps output in a `Scene` node, so an import lands as `Scene → <Object> → <MeshPart>`. Take the `MeshPart` and discard the wrappers when placing it.

## Budget

| Constraint | Limit | Source |
|---|---:|---|
| Triangles per mesh | **20,000** | Roblox 3D Importer rejects above this |
| Triangles, whole arena | ≤500,000 | Q-014 budget |
| Texture | ≤1024×1024 | Importer downscales or fails above |
| Draw calls | ≤1,000 | Q-014 budget |

Each generator prints its triangle count. If a mesh exceeds 20,000, split it into several objects rather than decimating blindly — the importer creates one `MeshPart` per object.

**Assert against the collision shell, not the exhibit extents.** An exhibit's visual extents are much larger than its shell, and only the shell is solid — geometry outside it is walked *through* rather than walked around. The beam engine's first build cleared the 70.66-stud extents at 54.66 wide and still overhung its 43.20-stud shell by 11 studs, passing every check. Generators now compare against the shell and print the remaining margin.

**Splitting for physics is different from splitting for budget.** The black hole exports four objects at only 12,016 triangles total — nowhere near the cap. The split is what makes Doppler asymmetry and the black-against-emissive contrast expressible at all, since geometry cannot carry brightness. Record which reason applies in the dossier.

## What must survive replacement (D-017)

An exhibit's Model identity, arena scale, footprint, and **collision shells** are preserved. When a production mesh replaces prototype geometry:

**Remove** — the primitive visual parts, wherever they sit. Note they are *not* all under `VisualDetail`; several exhibits keep geometry directly under the Model root.

**Keep, untouched** — `CollisionShells`, `Plinth`, `LabelAnchor`, `NamePlaque`, the Model's name, and its `ExhibitProxy` / `DisplayName` attributes.

Verify with a before/after bounding-box comparison. The footprint must not move.

## Accuracy and provenance

Every exhibit's `README.md` carries its dossier: what is verified against a real object, and what is stylistic invention. **Be explicit about which is which** — a generator that produces astronomically correct angles but invented proportions must say so, because a factual museum card will later claim accuracy on the player's behalf.

Anything derived from an external source needs a row in [ASSET_PROVENANCE_LEDGER.md](../docs/ASSET_PROVENANCE_LEDGER.md) before it ships, signed by a human per the Q-023 resolution.

## Layout

```
art/
  README.md                        this file
  tools/
    preview.py                     renders an exported GLB for visual check
  exhibits/
    <ExhibitModelName>/
      generate.py                  committed source
      README.md                    dossier: verified vs invented
      build/                       gitignored output
```

Directory names match the Studio Model names exactly, so an exhibit's source is findable from its instance and vice versa.
