# Handoff — 13 batch exhibits placed; 21 of 24 shipped

**Date:** 2026-07-26
**Scope:** Studio place only. `TASKS.md` and this file.
Follows [2026-07-26-batch-generators.md](2026-07-26-batch-generators.md).

## What just landed

All 12 GLBs from the batch were imported by the user at exact generator sizes to three decimals, then placed via MCP in one systematic pass. The equations wall's Luau `setup.luau` was run through MCP in a second pass. Every operation was wrapped in its own `ChangeHistoryService` recording, so any single placement is one Ctrl+Z away from reversal.

**One MCP call placed all 12 mesh exhibits** — sector, exhibit, target position, yaw, brass Metal, non-colliding, hide prototypes, rename stone. A second MCP call built the equations wall + 12 SurfaceGui tiles + hide prototypes + rename stone.

## Post-placement audit — every exhibit in the arena

Ran a single sweep counting `ProductionMesh` presence + collider count + preserved-children integrity across all 24 exhibit models:

```
SUMMARY: 21 OK, 3 MISS

MISS Northeast_ObservationAndTime.AstronomicalClockTower  (Prague clock — Q-018)
MISS Northwest_HallOfMinds.ScientistStatues               (Q-021 — Curie / Radiant Pioneer)
MISS East_CosmicVisualization.HolographicStarCharts       (Gaia — dataset decision deferred)
```

The three misses are exactly the three we deferred coming in. **Everything else has a `ProductionMesh`, exactly one collider (`PrimaryCollisionShell`), and intact preserved children.**

## Sector scoreboard

| Sector | Shipped | Total | Notes |
|---|---:|---:|---|
| West Gravity & Spaceflight | 3 | 3 | ✓ done |
| Southwest Life & Computation | 3 | 3 | ✓ done |
| **North Celestial Hall** | **3** | **3** | **✓ done (sphere + Blaeu + Rowley)** |
| **South Machines** | **3** | **3** | **✓ done (engine + Babbage + arms)** |
| **Southeast Energy & Matter** | **3** | **3** | **✓ done (CP-1 + Tesla + Michelson)** |
| Northeast Observation & Time | 2 | 3 | Astrolabe + telescopes; Prague blocked |
| East Cosmic Visualization | 2 | 3 | JPL + spacetime; Gaia deferred |
| Northwest Hall of Minds | 2 | 3 | Inventions + equations; statues blocked |
| **Total** | **21** | **24** | |

**Five full sectors done today** (West, Life & Computation, North, South, Southeast).

## Renames landed

13 stones now match the accuracy doc's real-object anchors:

| Prototype | → | Accuracy doc name |
|---|---|---|
| CELESTIAL GLOBE | → | BLAEU CELESTIAL GLOBE (1603) |
| MECHANICAL ORRERY | → | ROWLEY ORRERY (1712-1713) |
| ASTROLABE MONUMENTS | → | ARSENIUS PLANISPHERIC ASTROLABE (1607-1618) |
| TELESCOPE TOWERS | → | GALILEAN REFRACTOR AND HOOKER TELESCOPE |
| PLANETARY ORBIT PLATFORMS | → | JPL SOLAR SYSTEM ORBITS |
| SPACE-TIME PORTAL | → | SPACETIME CURVATURE AND GRAVITATIONAL LENSING |
| ATOMIC-ENERGY CORE | → | CHICAGO PILE-1 (1942) |
| TESLA COILS | → | TESLA COIL APPARATUS |
| LASER EXPERIMENT CHAMBER | → | MICHELSON LASER INTERFEROMETER |
| GIANT GEARS & MACHINERY | → | BABBAGE DIFFERENCE ENGINE NO. 2 |
| ROBOTIC ARMS | → | SIX-AXIS AND SCARA ROBOT ARMS |
| INVENTION MUSEUM CASES | → | LANDMARK INVENTIONS COLLECTION |
| FLOATING EQUATIONS & FORMULAS | → | FOUNDATIONAL EQUATIONS OF PHYSICS |

## Verified per exhibit

Systematically, for all 12 mesh placements + equations wall:

| Check | Result |
|---|---|
| Explicit axis-aligned AABB delta | 0.0000 on every exhibit (worst-axis max across all 13) |
| Colliders remaining | 1 per exhibit (`PrimaryCollisionShell`) |
| Preserved children intact | `CollisionShells`, `Plinth`, `LabelAnchor`, `NamePlaque` on every exhibit |
| Prototypes hidden with `PrototypeOriginal*` attributes | 43–69 per exhibit, restorable one-liner |
| SurfaceGuis on hidden prototypes also `Enabled = false` | Applied per periodic-table lesson |

## Visual spot-checks

Two representative captures reviewed:
- **Tesla coil** — iconic silhouette (toroid top, ridged secondary, primary at base) reads unmistakably at gameplay distance.
- **Equations wall** — title + 12 equation tiles + domain colour coding all legible. Adjacent renamed stones visible in the same frame (TESLA COIL APPARATUS, JPL SOLAR SYSTEM ORBITS).

Full arena sweep not screen-captured; 21 exhibits at 5 seconds each is 2 minutes of clicking, deferred to production QA.

## Zero human review signatures

Every one of the 21 shipped exhibits is `UNSIGNED` under Q-023. That's the single largest outstanding item for release. The batch shipped the geometry; a human still has to review each dossier and sign off.

## What this did not do

- **Not signed. Not approved.** 21 unsigned dossiers is a large backlog.
- **Factual museum cards** are not written. Every dossier lists what needs disclosure (display scales, materials, simplifications).
- **Prototype parts hidden, not deleted.** Restoration remains a one-liner via `PrototypeOriginal*` attributes.
- **M1 still not advanced. Combat still does not exist.** This is now the second consecutive session that has scaled exhibit throughput without addressing combat.

## What's left

**Three exhibits and one big gap.**

Exhibits:
- **Prague Astronomical Clock** — Q-018 blocked. Needs restoration-era decision (1866 / 1948 / 2018 look materially different).
- **Scientist Statues** — Q-021 blocked. Curie identifiability vs Radiant Pioneer character. User to decide: substitute figure, drop statue, or retheme character.
- **ESA Gaia Star Map** — dataset decision deferred. Which subset (DR3? nearest 100? constellation set?).

The **M1 combat gap** is the elephant. Every session has ended with the same disclosure. The arena is now a walkable museum with 21 named replicas and one enormous absence: nothing hits anything.

## Next smallest thing

- If continuing exhibits: user resolves one of Q-018, Q-021, or the Gaia dataset choice, and the corresponding exhibit ships.
- Otherwise: **return to M1**. Training dummy + damage + health/death/respawn is one focused session that unblocks the M1 exit condition.
