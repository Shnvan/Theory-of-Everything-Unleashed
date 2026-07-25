# Exhibit art pipeline

Source geometry for the Omniscience Coliseum's 24 exhibits.

## The rule: scripts are the source, meshes are the build

For any exhibit whose geometry can be described mathematically, **the committed source is a Python script**, not a `.blend` file. `generate.py` runs in Blender headless and writes a glTF.

That buys four things a binary file cannot:

- **Reproducible** — regenerate identical geometry from a clean checkout
- **Reviewable** — a diff, not an opaque blob
- **Parameterised** — change a ring count or an angle by editing a number
- **No Git LFS** — the repository stays text

`.blend` files and exported meshes are build artifacts and are gitignored. Only hand-sculpted exhibits — statues, ornate facades — need a committed binary, and those get LFS.

## Running a generator

```
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" ^
  --background --factory-startup ^
  --python art/exhibits/<Exhibit>/generate.py ^
  -- --out art/exhibits/<Exhibit>/build/<Exhibit>.gltf
```

`--factory-startup` matters: it ignores local Blender preferences so the output does not depend on whose machine ran it.

## Units

Roblox's importer treats **1 Blender metre as 100 studs**. Generators therefore author in studs for readability and scale by `0.01` on export, via `STUDS_TO_BLENDER` in each script.

**This is verified empirically per exhibit, not trusted.** Import, measure the resulting `MeshPart.Size` in Studio, and compare against the intended stud dimensions. Get this wrong and an exhibit is out by 100×.

## Budget

| Constraint | Limit | Source |
|---|---:|---|
| Triangles per mesh | **20,000** | Roblox 3D Importer rejects above this |
| Triangles, whole arena | ≤500,000 | Q-014 budget |
| Texture | ≤1024×1024 | Importer downscales or fails above |
| Draw calls | ≤1,000 | Q-014 budget |

Each generator prints its triangle count. If a mesh exceeds 20,000, split it into several objects rather than decimating blindly — the importer creates one `MeshPart` per object.

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
  exhibits/
    <ExhibitModelName>/
      generate.py                  committed source
      README.md                    dossier: verified vs invented
      build/                       gitignored output
```

Directory names match the Studio Model names exactly, so an exhibit's source is findable from its instance and vice versa.
