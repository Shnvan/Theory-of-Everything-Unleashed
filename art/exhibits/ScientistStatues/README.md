# Scientist Statues — Tesla · Newton · Einstein — dossier

Historical portrayals. Part of the 2026-07-26 final-three batch, **reposed** the same day to a back-to-back hero composition at the user's request.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.Northwest_HallOfMinds.ScientistStatues` |
| Visible name (pending rename) | **NIKOLA TESLA · ISAAC NEWTON · ALBERT EINSTEIN** — left-to-right, matching the statues |
| Class | Historical portrayals — stylised silhouettes, not portrait-quality sculpts |
| Geometry | 5,012 triangles across **3 objects**, 30.60 × 8.60 × 15.20 studs (Einstein pilot at higher fidelity; Newton and Tesla unchanged) |
| Rights | Original geometry, informed by public-domain portraits. Ledger row `REF-EXH-024` |
| Review | **UNSIGNED** |

## Composition — back-to-back hero pose, linear splay

The user supplied a reference image (a caricature of Tesla and Einstein standing back-to-back, each with an outstretched arm holding a glowing object) and asked for that composition with Newton inserted in the middle.

| Figure | Slot X | Yaw | Arm reaches | Prop |
|---|---:|---:|---|---|
| **Nikola Tesla** | −9 | −40° | world **−X** (far left) | Neon lightning orb |
| **Isaac Newton** | 0 | 0° | forward-left, raised | solid brass apple |
| **Albert Einstein** | +9 | +40° | world **+X** (far right) | Neon galaxy orb |

Figures are built facing −Y then yawed about Z. A Z-rotation θ maps the facing vector `(0,−1)` to `(sin θ, −cos θ)`, so −40° turns Tesla left-and-toward-viewer and +40° turns Einstein right-and-toward-viewer. Each outstretched arm is built on a local forward-outward diagonal whose net shoulder→hand direction, after the yaw, lands within 4° of the world X axis — putting both orbs at the outer extremes of the composition, as the reference framing does.

**Mini-plinths stay axis-aligned.** Only the figures rotate. A statue turned on a square pedestal is how real museum statues sit; rotating the pedestal too reads as sloppy.

**Arms are bent at the elbow** (shoulder → elbow → hand). A single straight cylinder reads as a broom handle; the bend makes the pose read as a deliberate gesture, which is the entire point of this composition. Cost is ~400 triangles per figure against a 20,000 cap.

**Chest plates and noses** were added to all three figures. Without them the splay is invisible — the torsos are rotationally symmetric cylinders, so a yaw about Z changes nothing the eye can detect, and only the arms betray that the figures are turned.

## Three-object export — required for the Neon orbs

| Object | Contents | Studio material |
|---|---|---|
| `ScientistStatues` | shared plinth + 3 pedestals + 3 figures + Newton's apple | Metal, brass |
| `Statues_TeslaOrb` | Tesla's lightning orb | **Neon**, pale blue-white |
| `Statues_EinsteinOrb` | Einstein's galaxy orb | **Neon**, warm amber |

Geometry cannot carry emissive material, so material differentiation requires separate meshes — the same principled split the black hole uses. See `art/README.md`: *"splitting for physics is different from splitting for budget."* At 3,656 triangles this is nowhere near the cap; the split is purely about materials.

**The generator asserts on this.** If a future edit joins the orbs into the main mesh they would silently lose the ability to be Neon and the exhibit would ship with two dead brass balls. `GEN_SPLIT_OK` fails the build rather than letting that through.

Placement is therefore a `ProductionMesh` **Model** containing three MeshParts — the black-hole pattern, which the existing placement code already handles.

## Why this trio (user decisions)

**Curie → Tesla.** Marie Curie collides with the Radiant Pioneer character (radiation-and-decay theme), failing the project's five-unprompted-testers identifiability test. Tesla is comparably famous and collides with no character. Note the museum already has a **TESLA COIL APPARATUS** in the Energy sector — this honours Tesla the person *in addition to* his invention, a standard museum pattern.

**Galileo, Lovelace → Einstein, Newton.** User chose maximum public recognition.

**Two concerns the user accepted knowingly:**

1. **The trio is all-male.** Dropping Lovelace removes the accuracy doc's only female-scientist representation. Curie was the only globally-famous female alternative and she is Q-021 blocked. If a reviewer wants representation restored, the next tier is Rosalind Franklin or Jane Goodall.
2. **Einstein and Newton both have weak Gravity Sovereign associations** (general relativity, universal gravitation). Neither is famous *solely* for gravity — Einstein for E=mc², the photoelectric effect, Brownian motion; Newton for calculus, optics, laws of motion — so the risk is far below the Curie/Radiant Pioneer collision that got Curie substituted out.

## Rights — the pose is fine, the style is not

The reference image is a **caricature illustration with unverified rights**. Two separate things:

- **The pose is fine to use.** Compositional ideas — a back-to-back stance, an outstretched arm holding a signature object — are not copyrightable. This is original low-poly geometry, not a tracing. No pixel of the reference ships.
- **The caricature style was deliberately not copied.** The reference exaggerates heads and features for comic effect. Museum statues of real historical people should be dignified; caricaturing them would read as mocking and sits badly against the accuracy doc's "historical portrayals" framing. Proportions here stay realistic.

The one exaggeration kept is **Einstein's wild hair**, because that is a real and documented feature of the man rather than a caricature invention.

Portrait references for silhouette guidance (public domain): Newton — Godfrey Kneller, 1689. Tesla — Napoleon Sarony, 1893. Einstein — iconic 1930s–40s photographs, specific image still to be confirmed for rights.

## What is interpretation

- **Materials.** Real bronze busts use bronze; brass here under D-016, with Neon on the two orbs.
- **Silhouettes are stylised** — each figure is 8–12 primitives. Reads as "a scientist statue" at gameplay distance, not "recognisable by face".
- **Fixed pose**, no individual name plaques on the pedestals (the exhibit stone covers naming).
- **Newton's arm angles outward** rather than straight forward. A straight-forward arm at yaw 0 points at the camera and foreshortens to nothing — the first render showed his apple as a sphere apparently stuck to his chest.

## Remaining before this can ship

1. Human review signature (Q-023).
2. Rename stone → `NIKOLA TESLA · ISAAC NEWTON · ALBERT EINSTEIN`. **Note the ordering choice:** this is left-to-right visual order so a visitor can match stone to statue. Chronological order (Newton 1643 · Tesla 1856 · Einstein 1879) would be the more traditional museum convention but would not match what the visitor sees, because the user asked for Newton in the middle. Worth a decision.
3. Confirm which Einstein photograph to cite as reference.
4. Studio materials: Neon on both orb MeshParts, brass Metal on the main mesh.

## Einstein fidelity pilot (2026-07-26)

User asked for the statues to be more realistic — "face, hair, clothes, hands" — after the initial trio shipped. The parametric-generator pipeline cannot produce the painted-anime-Roblox style the initial reference showed (that requires image decals from an artist, not code). The alternative the user chose was to push the pipeline as far as parametric primitives go: **~60-80 primitives per figure instead of ~15, in Blender, no external assets.** Einstein rebuilt as the pilot; Newton and Tesla left at the earlier fidelity so the trio stands side-by-side and the fidelity difference is directly visible.

**What the pilot Einstein has that the other two don't:**

- Real body proportions: separate legs, feet as distinct boxes, hip block, tapered sweater, visible sweater hem, V-neck collar, thin neck
- Face features: nose, moustache, eyebrow ridges, eye sockets as recessed spheres, chin, ears
- **Wild hair as 10 radial spikes** distributed over the top and back of the head, not one big sphere. This is the signature Einstein silhouette; it is the single most important feature for recognition and the reason to do this pass at all.
- Second (non-outstretched) left arm, bent slightly forward with hand near hip — so the figure doesn't look one-armed at the higher fidelity level.
- Right arm + galaxy orb pose unchanged from the earlier repose pass.

**Cost:** current Einstein ~500 tri → pilot ~2,336 tri. Main mesh 4,220 tri total. Still well inside the 20k-per-mesh cap.

**Go/no-go decision:** if the pilot reads as unmistakably Einstein at gameplay distance, the same treatment goes on Newton (long Baroque wig, prism in hand, scholar's robe folds) and Tesla (formal groomed hair, three-piece suit collar, moustache) in a follow-up session. If it reads only as "a low-poly man with spiky hair," we've caught that parametric primitives don't scale to portrait recognisability and the user faces the real-art-assets decision the plan deliberately deferred.

## History

**Built 2026-07-26**, then reposed the same day. Two bugs during the repose, both caught before commit:

**Figures sank through the plinth.** `join()` leaves the merged object's origin wherever `parts[0]` happened to sit — a leg or robe centred at mid-height, around z≈8.2. Setting `location = (slot_x, 0, 0)` then dragged that origin down to zero, sinking every figure ~8 studs while the separately-placed orbs stayed put. Caught by the reported numbers, not the render: the main mesh measured 9.32 tall where ~15 was expected, and total Z didn't reconcile with the parts. Fixed by leaving `location.z` alone.

**Arms pointed 90° wrong and read as detached stubs.** The arm cylinders used `rot=(0, pitch, yaw + π/2)`. Blender's XYZ euler composes as `Rz @ Ry`, so `+Z` maps to `(sin p·cos(yaw+90°), sin p·sin(yaw+90°), cos p)` — the `+π/2` introduced a 90° horizontal error. Hands and props were computed from the direction vector directly and so sat correctly, which is exactly why the figures looked broken rather than merely wrong. Replaced with the axis-angle `cyl_along` construction proven in the B-DNA generator.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/ScientistStatues/generate.py \
  -- --out art/exhibits/ScientistStatues/build/ScientistStatues.glb
```

Fails the build on triangle cap, shell overhang, or if the export is not exactly the three expected objects.
