# Handoff — B-DNA placed, first exhibit of the Life & Computation sector

**Date:** 2026-07-26
**Scope:** Studio place, `TASKS.md`, and this file.
Follows [2026-07-26-cavendish-and-saturnv-placement.md](2026-07-26-cavendish-and-saturnv-placement.md).

## What's now in the place

**B-DNA double helix** — `TheOmniscienceColiseum.ExhibitSectors.Southwest_LifeAndComputation.DNAHelixStructure.ProductionMesh` — one `MeshPart`, 17.49 × 51.63 × 18.97, brass Metal, anchored, non-colliding. Placed at `(90.10, 33.97, -79.51)`, yaw `131.4°`, on plinth top Y 8.16.

**Coordinates real.** Every C1' atom position in the geometry comes from the PDB 1BNA crystallographic structure (Drew, Wing, Takano, Broka, Tanaka, Itakura, Dickerson, *PNAS* 78 (1981) 2179-2183), which the vendored `art/exhibits/DNAHelixStructure/data/1bna.pdb` carries verbatim. The right-handed twist and correct rise-per-bp emerge from the coordinates themselves — nothing is imposed.

**Stone renamed** in the same recording: `DNA HELIX STRUCTURE` → `B-DNA DOUBLE HELIX — PDB 1BNA`, per the accuracy doc. Both the `Text` label and the `DisplayName` attribute updated.

Replaces 71 hidden prototype parts (`Pair1..10`, `A1..10`, `B1..10` + 41 `VisualDetail` children). One-line restorable via `PrototypeOriginal*` attributes.

Wrapped in one `ChangeHistoryService` recording — Ctrl+Z reverses both the placement and the stone rename together.

## Verified

| Check | Result |
|---|---|
| Explicit axis-aligned AABB delta | 0.0000 on every axis |
| Colliders remaining | 1 (`PrimaryCollisionShell`) |
| Preserved children | `CollisionShells`, `Plinth`, `LabelAnchor`, `NamePlaque` intact |
| Prototypes hidden | 71 parts, `PrototypeOriginal*` attributes stored |
| Visual read at gameplay distance | Twisted double helix, unambiguously DNA. Base pairs visible as rungs across the helix |
| Stone displays correctly | `B-DNA DOUBLE HELIX — PDB 1BNA` (the `1` renders serifed in the current font, easy to misread as `i` at a glance, but the underlying text is correct) |

## Two build-time lessons worth carrying forward

- **Assert canary paid off.** The hard-coded PDB axis swap in the first draft landed the helix horizontally. The shell-overhang assert caught it before the render did. Any future PDB-based exhibit will have the same class of risk — crystal frames are arbitrary — so the "compute helical axis from coordinates" approach is now the pattern.
- **Render step paid off, fifth time on this project.** The NURBS bevel curve produced valid-looking geometry with zero mesh vertices. All the asserts passed. Only the preview render caught it. Would have imported as an invisible ribbon set with only rungs floating.

## What this did not do

- Not signed. Stays `UNSIGNED` under Q-023.
- Not approved.
- Prototype parts hidden, not deleted.
- Factual museum card still to write.
- No factual card typography choice for the stone yet — the current serif `1` reading as `i` is worth noting to whoever picks the final font.
- **M1 still not advanced.** Combat still does not exist.

## Next smallest thing

Continue the Life & Computation sector with the **IUPAC periodic table**. That exhibit introduces a new pipeline capability — Studio-side SurfaceGui generation from an element data set — since text-and-layout is not a Blender-mesh problem. Third exhibit in the sector (AI lab) comes after.

Alternatively: **return to M1 combat** (training dummy + damage + health/respawn) if the exhibit backlog is running too long. That decision belongs to the user.
