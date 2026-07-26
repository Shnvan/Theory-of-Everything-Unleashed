# Prague Astronomical Clock (1865-1866 era) — dossier

Named replica. Part of the 2026-07-26 final-three batch. Q-018 resolved by user: **represent the era most people recognise** — the 1865-1866 restoration.

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.Northeast_ObservationAndTime.AstronomicalClockTower` |
| Visible name (pending rename) | **PRAGUE ASTRONOMICAL CLOCK** |
| Primary anchor | Prague Orloj, south face of Prague's Old Town Hall tower, as it appeared after the 1865-1866 restoration (calendar plaque by Josef Mánes, moralised side statues restored) |
| Real dimensions | Each dial ~2.6 m diameter; overall clock face ~6 m tall |
| Geometry | 9,144 triangles, 30.00 × 13.70 × 45.00 studs, one `MeshPart` |
| Display scale | 5.0 studs/m (2.6 m dial → 13 studs) |
| Rights | Original geometry. Ledger row `REF-EXH-023` |
| Review | **UNSIGNED** |

## Composition

Tall wall-mounted panel carrying every feature of the 1865-1866 face:

- **Astronomical dial (upper)** — 13-stud diameter, with:
  - Outer ring (representing the Schwabacher Czech-time numerals)
  - Middle zodiac ring
  - Sun hand + Sun ball at plausible position (~35° above horizontal)
  - Moon hand + Moon at ~155°
  - Central hub
- **Calendar dial (lower)** — 13-stud diameter, with:
  - Twelve zodiac medallions arranged around the rim (Mánes 1865)
  - Prague coat of arms boss at the centre
- **Twelve apostles procession windows** — two circular openings above the astronomical dial, each with a raised bezel ring + recessed dark cylinder suggesting the apostle behind
- **Rooster** — the crowing cockerel above the apostles windows (Orloj's iconic feature)
- **Eight side statues** on individual mini-plinths:
  - **Astronomical dial flanks (4):** Death (skeleton with hourglass), Vanity (mirror), Miser (money bag), Turk (turban)
  - **Calendar dial flanks (4):** Chronicler, Angel, Astronomer, Philosopher — 1865 additions, rendered with generic scroll props

## What is accurate

- **1865-1866 restoration state** — the "postcard" look with all its defining features present.
- **Two equally-sized dials** stacked vertically — the real Orloj layout.
- **Both dials at real 2.6 m proportion** (13 studs at the disclosed 5 studs/m scale).
- **Twelve zodiac medallions** on the calendar dial — Mánes's specific number.
- **Twelve apostles procession** hinted by the two circular windows.
- **Rooster above** — Orloj's iconic feature.
- **Moralised side statues** on the astronomical dial (Death, Vanity, Miser, Turk) — the four figures the 1865 restoration made canonical.

## What is interpretation

- **Materials.** Real Orloj is stone tower with painted metal dials and gilded ornaments. Rendered entirely in brass under D-016. The gilded parts of the real clock map naturally to brass, so this is a smaller material gap than most exhibits.
- **Statue silhouettes are simple** — body cylinder + sphere head + one identifying prop. Real statues are detailed sculptures; at gameplay distance the silhouettes read as figures.
- **No zodiac paintings on calendar medallions.** Real medallions are Mánes's zodiac artwork. Rendered as plain discs.
- **No engraved numerals on the outer ring.** Real ring has Roman + Arabic + Schwabacher Czech-time markings. Rendered as a plain torus.
- **No motion.** The real Orloj's apostles rotate hourly and the sun hand tracks solar time. This is a static snapshot.
- **Wall-mounted, not tower-integrated.** Real Orloj is part of a tall stone tower. This is just the clock face, rendered as a freestanding panel.

## Remaining before this can ship

1. Human review signature (Q-023).
2. Rename stone `ASTRONOMICAL CLOCK TOWER` → `PRAGUE ASTRONOMICAL CLOCK`.
3. Factual card must state: (a) 1865-1866 era, (b) the ~5 studs/m display scale, (c) that the Orloj is normally viewed as part of a tower rather than a freestanding panel.

## Regenerating

```
blender --background --factory-startup \
  --python art/exhibits/AstronomicalClockTower/generate.py \
  -- --out art/exhibits/AstronomicalClockTower/build/AstronomicalClockTower.glb
```
