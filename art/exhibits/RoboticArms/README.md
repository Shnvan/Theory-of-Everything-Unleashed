# Six-Axis and SCARA Robot Arms — dossier

Scientific reconstruction. Part of the 2026-07-26 batch.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.South_Machines.RoboticArms` |
| Visible name (pending rename) | **SIX-AXIS AND SCARA ROBOT ARMS** |
| Class | Scientific reconstruction — generic, non-branded housings |
| Geometry | 796 triangles, 38.88 × 20.00 × 16.65 studs, one `MeshPart` |
| Rights | Original geometry. Ledger row `REF-EXH-020` |
| Review | **UNSIGNED** |

## Composition

Two industrial arm classes side by side on a shared base plate:

- **Six-axis articulated arm (left):** base pedestal + shoulder yoke + angled upper arm + elbow + angled forearm + wrist assembly (3 small joints) + end effector. Six rotational joints, human-arm-like reach. Class of KUKA / ABB / Fanuc / Franka.
- **SCARA (right):** base + tall vertical column + two horizontal shoulder links + vertical Z-axis picker + end effector. Class of Epson / Yamaha assembly arms.

## What is accurate

- **Two distinct kinematic types** — the accuracy doc's requirement.
- **Six-axis has 6 identifiable joints** (base yaw, shoulder pitch, elbow pitch, and 3 wrist joints suggested by the wrist assembly).
- **SCARA has the correct axis set** — vertical prismatic Z, two horizontal rotational shoulders, and a wrist. Fast planar reach with a vertical picker.
- **Generic, non-branded housings** — no manufacturer identity encoded in the silhouettes.
- **Mechanically possible joints** — every joint is a plausible rotational or prismatic axis.

## What is interpretation

- **Materials.** Real arms are painted steel/aluminium in orange/white/grey; brass throughout under D-016.
- **Fixed pose.** Real arms move; each is held in one plausible working pose.
- **No cabling.** Real industrial arms have visible cable bundles running along the links; not modelled.
- **No end effector detail.** Both arms end in generic gripper blocks — no vacuum cups, welding torches, or spray heads that would identify a specific application.
- **Six-axis arm is compact.** Front view mostly shows the arm from the side; the full articulated reach is more visible from above.

## Remaining before this can ship

1. Human review signature (Q-023).
2. Rename stone `ROBOTIC ARMS` → `SIX-AXIS AND SCARA ROBOT ARMS`.
3. Factual card: state this is a generic reconstruction, not any specific commercial arm. Both kinematic types documented in industrial-robotics textbooks; no specific citation required.
