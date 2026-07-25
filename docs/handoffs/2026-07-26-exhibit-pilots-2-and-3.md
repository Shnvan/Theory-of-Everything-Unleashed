# Handoff — exhibit pilots 2 and 3: beam engine and black hole

**Date:** 2026-07-26
**Scope:** Generator scripts, dossiers, provenance rows, and one new pipeline rule. **Nothing was imported into Studio and nothing is approved.**

## What exists now

| | Beam engine | Black hole |
|---|---|---|
| Path | `art/exhibits/SteamEngine/` | `art/exhibits/BlackHoleGenerator/` |
| Triangles | 3,512 | 12,016 across **4** meshes |
| Size, studs | 41.75 × 18.00 × 56.60 | 35.00 × 34.58 × 20.21 |
| Meshes | 1 | 4 — `Shadow`, `PhotonRing`, `DiskApproaching`, `DiskReceding` |
| Replaces | 50 primitive parts | 68 primitive parts |
| Status | **Unimported, unsigned** | **Unimported, unsigned** |

Both generators fail the build on triangle cap, collision-shell overhang, and their own key proportion.

## The one rule worth carrying forward (D-036)

**Render the export and look at it before importing.** Both pilots passed every assert while carrying defects that a single render exposed in seconds:

- beam engine: parallel motion was two bars attached to nothing; the governor was hidden behind its own frame
- black hole: the accretion disk was a smooth funnel instead of a flat disk with a lensing arc; the photon ring lay flat because a blanket `rotation_euler` assignment silently overwrote its orientation

Dimensions, triangle counts and envelope fit were all correct in every one of those cases. `art/tools/preview.py` renders the exported GLB — the export, not the live scene, so it also checks the round trip.

This is the **fourth** time this project has been bitten by trusting an assumed number over an observable one, after the jump-button overlap, the backwards export scale, and the armillary sphere's proportions. That is why it is now a procedure rather than a lesson.

The related rule: **assert against the collision shell, not the exhibit extents.** The beam engine's first build was 54.66 studs wide, cleared the 70.66-stud extents, and overhung its 43.20-stud shell by 11 studs. Only the shell is solid, so that geometry would have been walked through.

## Three things a human has to decide

**1. The `BLACK-HOLE GENERATOR` stone must be renamed.** `docs/OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md` requires this exhibit to be *"never described as generating a black hole"* and lists as an acceptance condition that *"visible signs contain no fictional machine presented as real."* The current stone fails both. `GRAVITY-CONTROL CHAMBER` has the identical defect against its Cavendish-balance target. Neither was changed here — it is player-visible text. **This blocks release, not just approval.**

**2. The steam engine prototype is a locomotive.** `Boiler`, `Firebox`, `Stack`, `Wheel1`, `Wheel-1`. Object `1861-46` is a stationary rotative beam engine with no boiler, chimney or wheels in its silhouette. The import is a replacement of the wrong object, not a refinement — and the existing footprint was shaped around the wrong thing.

**3. The Lap Engine's dimensions rest on a weak source.** The museum record for `1861-46` gives **no measurements at all**. The bore (18.75 in) and stroke (4 ft) come from Wikipedia, which cites the accession number but no technical document. The plan for this work called them "verified specifics"; that was overstated and is corrected in the dossier and in ledger row `REF-EXH-004`. **The factual card must not present them as measured.**

## Provenance

Three new ledger rows, each licence checked rather than assumed:

- `REF-EXH-003` — Science Museum `1861-46`. Imagery **CC BY-NC-SA 4.0**; the NC clause bars commercial use, so it informs geometry and never ships.
- `REF-EXH-004` — Wikipedia "Lap Engine". Text **CC BY-SA 4.0**; only two numeric facts used, no prose.
- `REF-EXH-005` — NASA SVS. **Public domain**, confirmed from their own terms. Two caveats checked and found not to bite: some visualisations carry licensed music that is *not* public domain, and NASA's guidelines restrict the insignia and forbid implying endorsement. Nothing is copied and no NASA branding appears.

## What is accurate, and what is not

**Beam engine** — real: bore-to-stroke ratio 2.561 (subject to the source warning), sun-and-planet gearing with correct mesh geometry, parallel motion as a closed linkage, separate condenser, centrifugal governor (this engine was the first to carry one). Invented: **all overall dimensions**, flywheel size, spoke count, beam profile, column spacing. Materials are brass per D-016; the real engine is **wood and cast iron**, a larger material gap than the armillary sphere's.

**Black hole** — real: the black sphere is the **shadow** at √27⁄2 ≈ 2.598× the horizon, not the horizon itself; photon ring outside it; lensed disk whose far half arcs above and near half below, emerging from the construction rather than sculpted; Doppler split at the correct azimuth. Invented: the bend profile is tuned to look right, not integrated from geodesics; the photon ring only reads correctly from the front, since a real one always faces the observer.

The four-mesh split is a **physics requirement, not a budget workaround** — geometry cannot carry brightness, so Doppler asymmetry needs separate materials. At 12,016 triangles it is nowhere near the cap.

## Also fixed in passing

`D-034` still contained the backwards `scaled by 0.01` export rule — the last surviving copy, after the correction reached five other places. Corrected in place with the correction marked.

## What this did not do

M1 is not advanced. **Combat still does not exist** — no health, no death, no respawn, no damage. Both exhibits are unimported and unsigned. Also still outstanding from earlier sessions: `REF-ARENA-001` is signed by an AI agent and needs re-signing or explicit downgrade under Q-023, and the CC BY 3.0 credit line for the HUD icons (Q-024) still has to be pasted into the experience description, which blocks release.
