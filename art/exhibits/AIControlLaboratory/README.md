# AI Computing and Robotics Laboratory — dossier

Eighth exhibit for the production pipeline. Third and final exhibit from the Life & Computation sector. Follows the research-dossier gate in [OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](../../../docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md).

**Status: geometry built, not imported and not approved.** No human has signed it off.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.Southwest_LifeAndComputation.AIControlLaboratory` (retained) |
| Visible name | **AI COMPUTING AND ROBOTICS LABORATORY** (rename pending, currently `AI CONTROL LABORATORY`) |
| Classification | **Scientific reconstruction** — a truthful, generic workflow, no specific facility |
| Source | Category: *"a truthful, generic inference-server, networking, sensing, and robotics workflow; no fictional sentient core"* — from the accuracy doc |
| Geometry | 3,168 triangles, 1,800 vertices, 40.61 × 28.85 × 28.27 studs, one `MeshPart` |
| Construction | Parametric, `generate.py` |
| Rights | Original design. No external imagery or dataset used, so no ledger row required |
| Gameplay fit | Replaces 45 primitive parts (`GlassLab`, `Core`, `Screen`, `Console` + 41 `VisualDetail` children) with one `MeshPart` |
| Review | **UNSIGNED** |

## This replaces a fictional sentient core

The prototype it supersedes is `GlassLab` (a big turquoise glass box) + `Core` (a neon blue cube inside) + `Screen` + `Console`. That is exactly the "fictional sentient AI core" pattern the accuracy doc explicitly forbids for this exhibit:

> *"A truthful, generic inference-server, networking, sensing, and robotics workflow; no fictional sentient core."*

Wholesale replacement. The internal Studio identity `AIControlLaboratory` is retained because D-017 requires internal Model names to survive, but every visible element of the prototype is replaced.

## What is accurate — what a real lab has

Every element in the composition is real infrastructure that a working AI/robotics lab has, chosen so no single element requires branding to be identifiable:

- **Two 19-inch equipment racks** with visible 1U server chassis stacked. This is what an inference-server rack looks like at any scale — data centres and research labs alike. LED bezel indicators on each unit.
- **Top-of-rack network switch** aggregating the servers. Visible port array on the front — the switch is a real object with real ports.
- **Workbench** — a real flat-topped bench on four legs. Where sensors and robotics are mounted for testing.
- **Flat-panel monitor** on a stand at the back of the bench, angled slightly for legibility.
- **Small collaborative arm** on the bench in a plausible working pose — base, shoulder rotator, upper arm, elbow, forearm, end-effector with two-finger gripper. This is a *cobot*, at the size and shape typical of Universal Robots UR3 / Franka / xArm class arms, deliberately distinct from the dedicated *SIX-AXIS AND SCARA ROBOT ARMS* exhibit that lives in the Machines sector. Reads as an incidental workflow element, not the featured object.
- **Camera-sensor rig** — a tripod-mounted vision sensor at the far end of the bench, representing the "sensing" input of the workflow.

## What is interpretation

- **Materials.** Real racks are usually black steel; real monitors are grey or black; real cobots are grey or orange (Universal Robots). This uses brass under D-016. Larger material gap than most exhibits, and the dossier says so.
- **Rack contents are simplified.** Real 1U servers have complex front panels: drive bays, network ports, USB, VGA, KVM. Rendered here as a single bezel bar with an LED nub to keep the silhouette readable at gameplay distance.
- **Cobot pose is fixed.** Real cobots move; this holds one pose. Chosen to look like the arm is doing something plausible (bent forward with the gripper hovering over the bench).
- **No cables.** Real labs have visible cable runs (power, network, USB). Omitted for triangle budget and visual clarity.
- **Number of racks: 2.** A real inference lab typically has one to many. Two racks reads as "some racks" without over-committing to a specific facility size.
- **Camera as tripod-mounted vision sensor.** Could plausibly be a security camera or a photography setup; the tripod plus the lab context should read as scientific vision sensing.

## Rights

Geometry here is **original**, authored from general knowledge of what data centre and lab infrastructure looks like. No product photography, no vendor imagery, and no specific facility informs the shapes — everything is generic.

Because nothing external is copied or measured against, **no provenance-ledger row is required** for this exhibit. If a reviewer wants a more specific reference (e.g., a real published lab tour used as scale reference), a row can be added at that time.

## Remaining before this can ship

1. A human review signature (Q-023).
2. The factual museum card, stating plainly that this exhibit is a *representative* workflow, not a specific facility.
3. Rename the visible stone `AI CONTROL LABORATORY` → `AI COMPUTING AND ROBOTICS LABORATORY` per the accuracy doc.
4. If a reviewer wants a more grounded reference, cite a public lab photo (e.g., a NASA JPL or MIT CSAIL image released under a permissive licence) and add a ledger row.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/AIControlLaboratory/generate.py \
  -- --out art/exhibits/AIControlLaboratory/build/AIControlLaboratory.glb
```

**Geometrically deterministic:** every run gives 3,168 triangles, 1,800 vertices and identical dimensions. Fails the build on triangle cap, envelope height, or collision-shell overhang.

## Import settings

Scale Unit **Stud**, Scale Factor **1**, Anchored **on**, Collision Fidelity **Box**, no rig, merge off.
