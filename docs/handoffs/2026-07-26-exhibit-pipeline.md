## Session handoff — 2026-07-26 (exhibit art pipeline, armillary sphere pilot)

Follows [2026-07-26-movement.md](2026-07-26-movement.md). Format: [templates/SESSION_HANDOFF.md](../templates/SESSION_HANDOFF.md).

### Target

- Task: begin real museum-accurate exhibit production, with proper tooling, at the user's direction and ahead of the M4 gate D-017 required.
- Acceptance condition: a reproducible pipeline proven end to end on one pilot, without breaking D-017's preservation rules.

### Completed

- **`art/` tree and the pipeline convention** — the committed source for an exhibit is a Python generator script, not a binary. `.blend` and exported meshes are build output and gitignored.
- **Armillary sphere generator** — `art/exhibits/GiantArmillarySphere/generate.py`. Parametric, astronomically correct, 8,884 triangles, 45.62 × 52.49 × 45.62 studs.
- **Blender MCP registered** in `.mcp.json`, superseding D-025 for Blender only. `uv 0.11.32` installed to provide `uvx`; the addon downloaded to `tools/blender/addon.py`.
- Decisions **D-033** (production starts now), **D-034** (the pipeline), **D-035** (Q-014 closed).
- Commits: pending at time of writing. Prior session ended at `034719d`.

### The finding that shaped the pipeline

The plan assumed Blender MCP would be the tool. It is not, and should not be.

**Blender runs headless from the CLI**, driven by exactly the committed Python scripts the plan already recommended as the source of truth. That needs no MCP at all, works today, and is reproducible on any machine. MCP is registered for interactive shaping, but it is not in the pipeline — which matters because the honest 2026 read of Blender MCP is that it is strong at repetitive setup and **weak at creative modelling and topology**, and topology is the hard part of a museum object.

**Determinism was verified, not asserted:** two runs produced byte-identical GLB output, SHA256 `60E9D485…`. That is the claim the whole "scripts not binaries" decision rests on, so it is checked rather than trusted, and it is what makes gitignoring the mesh safe.

### Verification

- Generator runs headless: **PASS**, exit 0.
- Triangle budget: **PASS**, 8,884 against a 20,000 per-mesh cap.
- Determinism: **PASS**, identical SHA256 across two runs.
- Arena baseline re-measured: **1,949 BaseParts, 2,455 Workspace instances**, 0 MeshParts, 0 Unions. Shape mix: 1,140 Block, 639 Ball, 146 Cylinder, 24 Wedge.
- **Docs were stale.** The recorded instance count was 2,909; the measured figure is 2,455. Re-measuring rather than trusting the doc was the right call and is now written into Q-014's resolution.
- Studio import: **NOT RUN.** The 3D Importer is Studio UI with no MCP equivalent, so this needs the user.
- Triangle and draw-call counts: **NOT RE-MEASURED.** Not readable from Luau; they come from Studio's Scene Analysis panel, which is UI-only. The 74,238 / 25 figures are inherited from the docs and remain unverified by me.

### Decisions

- **D-033** — production art begins before M4, superseding D-017's deferral. D-017's preservation rules stand untouched.
- **D-034** — Blender headless plus committed generator scripts; GLB; Blender MCP registered but explicitly not the pipeline. Supersedes D-025 for Blender only.
- **D-035** — closes Q-014. ≤500,000 triangles, ≤1,000 draw calls, ≤20,000 per mesh, ≤1024×1024 textures. **D-016's 2,000-BasePart cap retired** as the binding constraint: at 1,949 it was about to block work the GPU budget shows is nowhere near a limit.

### Risks and blockers

- **The dossier is deliberately incomplete and the exhibit must not ship on it.** The astronomy is real — 23.44° obliquity, 66.56° polar circles, correct circle-of-declination geometry, geocentric construction. **Every proportion is invented** and unverified against Science Museum Group object `1878-12`. There is no corroborating source and no human review signature. A factual museum card would currently claim accuracy the dossier cannot support.
- **The import step is manual.** No MCP path exists for the 3D Importer, so every exhibit needs the user for that step.
- **Scale is unverified in Studio.** The 0.01 export factor is documented Roblox behaviour, not something measured here. If it is wrong the exhibit lands 100× off — obvious immediately, but check before assuming.
- Ring geometry sits at the exhibit's **Model root**, not under `VisualDetail`. Replacing it means removing `Meridian_01-08`, `Equator_01-08`, `Ecliptic_01-08`, `Core`, and `Stand` as well. The plan's "replace VisualDetail" was too narrow.
- This does not advance M1. Combat still does not exist, and dash, health, and the training dummy remain unbuilt.
- Q-018 and Q-021 still block the Prague clock and all three Hall of Minds statues.

### Next smallest task

- Task: import `art/exhibits/GiantArmillarySphere/build/GiantArmillarySphere.glb` through Studio's 3D Importer, measure the resulting `MeshPart.Size` against the intended 45.62 × 52.49 × 45.62 studs, and record the true scale factor.
- Acceptance condition: the size matches intent, or the correction factor is recorded in `art/README.md` so every later generator uses it.
