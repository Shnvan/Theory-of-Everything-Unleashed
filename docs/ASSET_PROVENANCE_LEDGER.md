# Asset Provenance Ledger

**Status:** operating record; no production exhibit assets approved

**Applies to:** every external or generated model, mesh, texture, image, animation, audio file, font, plugin, extension, code dependency, dataset-derived visual, or commissioned work

**Last reviewed:** 2026-07-25

## Rules

- Create a ledger entry before an external asset enters the production place or repository.
- Separate permission to inspect a reference from permission to copy, modify, redistribute, or ship its media.
- Treat `unclear` as `HOLD`, not as approval.
- A Creator Store or marketplace listing does not prove that its uploader owns the work.
- Record the exact source item and license. A site-wide reputation or general collection policy is insufficient when the item has different terms.
- Inspect downloaded Models and plugins in isolation for scripts, remotes, packages, constraints, hidden objects, dependencies, and unexpected asset references.
- Do not imply endorsement by a museum, university, laboratory, agency, estate, marketplace, or asset creator.

## Cost gate

The user must explicitly approve every cost before purchase, subscription, commission, or paid installation. The request must state:

- exact item, seller, and purpose;
- price and currency;
- taxes or fees if known;
- one-time or recurring terms;
- commercial-use and modification rights;
- key risks; and
- the best free alternative.

Approval of one item does not authorize another purchase or a renewal.

## Status values

| Status | Meaning |
|---|---|
| `REFERENCE ONLY` | May inform research; source media cannot be shipped or copied |
| `RESEARCH` | Rights and technical review are incomplete |
| `HOLD` | A rights, cost, safety, provenance, or quality question blocks use |
| `APPROVED` | Rights, cost, security, quality, and project-fit reviews passed |
| `REPLACE` | Must not ship and needs an approved substitute |
| `REMOVED` | Removed from all production locations; retain the record for audit |

## Asset records

| ID | Asset and type | Purpose | Creator/source | Source URL or file | License/permission | Commercial use | Modification | Attribution | Cost/approval | Receipt | Local source/hash | Roblox asset ID | Obtained | Reviewer/status | Shipped |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `REF-ARENA-001` | `ChatGPT Image Jul 23, 2026, 07_15_55 PM (1).png`; image | Coliseum composition and mood reference | User-provided generated image | `C:\Users\Ivan\Downloads\ChatGPT Image Jul 23, 2026, 07_15_55 PM (1).png` | Source rights not verified; reference use only | No | Unclear | N/A while unshipped | None | N/A | Not copied into repository; hash not recorded | N/A | 2026-07-23 | Codex (an AI agent — see Q-023) / `REFERENCE ONLY` | No |
| `TOOL-001` | Moon Animator 2; Studio plugin | Primary combat animation authoring | xSIXx / Team Moon | Creator Store asset `4725618216` | Paid plugin licence; terms not yet read | Unreviewed | Unreviewed | Unreviewed | **Not approved.** Reported ~1,700 Robux, price unverified. Needs the full cost gate before purchase | None | N/A | N/A | Not obtained | Unassigned / `HOLD` | No |
| `TOOL-002` | Roblox Animations Importer/Exporter; Blender add-on plus Studio plugin | Free animation bridge and fallback to Moon Animator | Cautioned | `github.com/Cautioned/Blender-Animations-Plugin` | GPL-3.0 | Stated yes; terms not yet read in full | Yes under GPL-3.0 | Per GPL-3.0; requirement not yet confirmed | Free | N/A | N/A | N/A | Not obtained | Unassigned / `RESEARCH` | No |
| `TOOL-003` | Beziers; VFX plugin and asset library | Modular VFX authoring | coroutine_yieId | DevForum thread `4180222` | Paid | Unreviewed | Unreviewed | Unreviewed | **Not approved.** Deferred past M4 | None | N/A | N/A | Not obtained | Unassigned / `HOLD` | No |
| `TOOL-004` | `StudioMCP.exe`; Roblox Studio MCP proxy | Lets Claude Code read the open place's data model and Output | Roblox, first party | Ships with Studio at `%LOCALAPPDATA%\Roblox\Versions\version-14d8b191232f4ddd\`; launcher at `%LOCALAPPDATA%\Roblox\mcp.bat` | Roblox Studio terms; first-party component, not a third-party download | N/A — a development tool, nothing ships to players | No | None | Free | N/A | Installed by Studio; not copied into the repository | N/A | 2026-07-23 (file date) | Connected 2026-07-25 under D-024 / `APPROVED` for development use | No |
| `REF-EXH-001` | Object record and imagery for **`1878-12`**, della Volpaia armillary sphere, 1554; web page | Dimensions and construction reference for the `GiantArmillarySphere` exhibit | Science Museum Group | `collection.sciencemuseumgroup.org.uk/objects/co56284` | Imagery **CC BY-NC-SA 4.0** | **No — the NC clause bars commercial use** | Share-alike would apply | Required if ever used, which it is not | Free | N/A | Not copied into the repository. Published measurements only: H 500 × W 300 × D 300 mm, triple claw feet, encloses a manuscript terrestrial globe | N/A | 2026-07-26 | Unassigned / `REFERENCE ONLY` | No — informs original geometry; no museum media ships |
| `REF-EXH-002` | Object record for della Volpaia's **1564** armillary sphere, Epact `18837`; web page | Corroborating source for della Volpaia's ring construction, which `1878-12`'s record omits | Museum of the History of Science, Oxford | `mhs.ox.ac.uk/epact/catalogue.php?ENumber=18837` | Not reviewed — descriptive text used, no media | N/A | N/A | N/A | Free | N/A | Not copied. Used for: zodiac band 65 mm on a 700 mm instrument, horizon in four 90° quadrants, polar caps/equator/tropics divided, central sphere pierced by the inclined axis | N/A | 2026-07-26 | Unassigned / `REFERENCE ONLY` | No |
| `REF-EXH-003` | Object record and imagery for **`1861-46`**, Boulton and Watt rotative beam engine (the *Lap Engine*), 1788; web page | Structure reference for the `SteamEngine` exhibit | Science Museum Group | `collection.sciencemuseumgroup.org.uk/objects/co50948` | Imagery **CC BY-NC-SA 4.0** | **No — the NC clause bars commercial use** | Share-alike would apply | Required if ever used, which it is not | Free | N/A | Not copied into the repository. **The record gives no measurements at all.** Used for: 1788, Boulton Watt & Co Birmingham, materials wood and cast iron, sun-and-planet gear, first engine fitted with a centrifugal governor, drove 43 lapping machines for 70 years | N/A | 2026-07-26 | Unassigned / `REFERENCE ONLY` | No — informs original geometry; no museum media ships |
| `REF-EXH-004` | Wikipedia article **"Lap Engine"**; web page | **Sole source** for the only two dimensions in the `SteamEngine` model | Wikipedia contributors | `en.wikipedia.org/wiki/Lap_Engine` | Text **CC BY-SA 4.0** | Yes | Yes, under share-alike | Required if text were reused, which it is not — only two numeric facts are used | Free | N/A | Not copied. Bore **18.75 in (47.6 cm)**, stroke **4 ft (1.2 m)**. **Secondary source, unconfirmed against any primary record** — the article cites the museum accession number but no technical document for these figures. The dossier's provenance warning turns on this row | N/A | 2026-07-26 | Unassigned / `REFERENCE ONLY` | No |
| `REF-EXH-005` | NASA Scientific Visualization Studio black-hole visualisations and accompanying descriptions; web pages | Physics reference for the `BlackHoleGenerator` exhibit | NASA Goddard Space Flight Center / SVS | `svs.gsfc.nasa.gov` | **Public domain** — "All of our content is in the public domain (unless otherwise noted)". Checked, not assumed. Two caveats verified: some visualisations carry **licensed music that is not public domain**, and NASA's media guidelines restrict the **NASA insignia** and forbid implying endorsement | Yes | Yes | Not required; none claimed | Free | N/A | Not copied. Used for: shadow radius √27⁄2 ≈ 2.598× the horizon, photon ring just outside the shadow, lensed disk arcing over and under, Doppler brightening of the approaching side | N/A | 2026-07-26 | Unassigned / `REFERENCE ONLY` | No — neither caveat bites; nothing is copied and no NASA branding appears |
| `REF-EXH-006` | Wikipedia article **"Cavendish experiment"**; web page | **Sole source** for every dimension in the `GravityControlChamber` model | Wikipedia contributors | `en.wikipedia.org/wiki/Cavendish_experiment` | Text **CC BY-SA 4.0** | Yes | Yes, under share-alike | Required if text were reused, which it is not — only numeric facts are used | Free | N/A | Not copied. Rod 1.83 m, small balls 51 mm / 0.73 kg, large balls 300 mm / 158 kg, separation 225 mm, mahogany case 1.98 × 1.27 × 0.14 m. Article cites Cavendish, *Philosophical Transactions of the Royal Society* vol. 88 pp. 469–526, 1798, as the primary source; the wire specification is not given in either | N/A | 2026-07-26 | Unassigned / `REFERENCE ONLY` | No |
| `REF-EXH-007` | Wikipedia articles **"Saturn V"** and **"Kennedy Space Center Launch Complex 39"**; web pages | **Sole source** for every dimension in the `RocketLaunchDisplay` model | Wikipedia contributors | `en.wikipedia.org/wiki/Saturn_V`, `en.wikipedia.org/wiki/Kennedy_Space_Center_Launch_Complex_39` | Text **CC BY-SA 4.0** | Yes | Yes, under share-alike | Required if text were reused, which it is not — only numeric facts are used | Free | N/A | Not copied. Saturn V total 363 ft x 33 ft dia; S-IC 138 ft, S-II 81.6 ft, S-IVB 58.6 ft x 21.7 ft dia, IU 3 ft, spacecraft ~82 ft. LUT 446 ft with 9 swing arms. Mobile Launcher 161 x 135 ft, two-story, four hold-down arms. Saturn V article cites NASA technical documentation | N/A | 2026-07-26 | Unassigned / `REFERENCE ONLY` | No |
| `REF-EXH-008` | **PDB entry `1BNA`** — B-DNA dodecamer crystal structure; text file of atom coordinates | Coordinate source for the `DNAHelixStructure` exhibit | Drew, Wing, Takano, Broka, Tanaka, Itakura, Dickerson (deposit 26 Jan 1981) | `files.rcsb.org/download/1BNA.pdb`, primary paper DOI [10.1073/pnas.78.4.2179](https://doi.org/10.1073/pnas.78.4.2179) | RCSB PDB terms — data is freely reusable including for commercial purposes; standard courtesy citation of primary paper | Yes | Yes | **Required:** Drew et al., *Structure of a B-DNA dodecamer: conformation and dynamics*, Proc. Natl. Acad. Sci. USA **78** (1981) 2179–2183 | Free | N/A | Vendored to `art/exhibits/DNAHelixStructure/data/1bna.pdb`, 76 KB, downloaded 2026-07-26. Used for: C1' atom positions per residue for backbone ribbons and base-pair rungs. 486 non-hydrogen atoms in file; ribbon rendering uses 24 (one C1' per residue × 2 chains) | N/A | 2026-07-26 | Unassigned / `RESEARCH` | Yes — vendored file ships; content is coordinates only, no imagery |
| `REF-EXH-009` | **IUPAC Periodic Table of the Elements** — web page listing element data | Source of atomic numbers, symbols, names, standard atomic weights, and category assignments for the `PeriodicTableWalls` exhibit | International Union of Pure and Applied Chemistry (IUPAC) | `iupac.org/what-we-do/periodic-table-of-elements/`, accessed 2026-07-26 | Element data is factual (not copyrightable). Standard 18-column layout is a scientific convention (not copyrightable). IUPAC page itself is not copied | Yes (facts only) | Yes (facts only) | Not required for facts; IUPAC named as data source on factual card | Free | N/A | Not copied. Element data transcribed into `art/exhibits/PeriodicTableWalls/setup.luau` as a Luau table. Accessed date must appear on the factual card, since atomic weights and category assignments have been revised historically | N/A | 2026-07-26 | Unassigned / `REFERENCE ONLY` | No — data used but not the page itself; source cited as fact |
| `TOOL-005` | `addon.py`; Blender addon, plus the `blender-mcp` Python package | Optional interactive control of Blender from an MCP client. **Not part of the art pipeline** — generators run through Blender headless with no MCP involved (D-034) | ahujasid | `github.com/ahujasid/blender-mcp`, addon from `raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py` | **Licence not yet reviewed** | Unreviewed | Unreviewed | Unreviewed | Free | N/A | SHA256 `CA6955BB584D78E229F020A8B9D7011440ADC6E94DAB0AC8E01AB2794DB19DC0`. Fetched to `tools/blender/`, which is gitignored — pinned by hash rather than vendored | N/A | 2026-07-26 | Unassigned / `RESEARCH` | No — development tool, nothing ships to players |
| `UI-ICON-001` | `punch.png`; image | `BasicAttackButton` glyph — a fist | Lorc | `game-icons.net/icons/ffffff/transparent/1x1/lorc/punch.png` | CC BY 3.0 | Yes | Yes | **Required.** See the attribution block below | Free | N/A | SHA256 `6D03B59C8968030F…`; re-fetchable from the URL | `85239036663948` | 2026-07-26 | **Shnvan** (human), 2026-07-26 / `APPROVED` | In place, not released |
| `UI-ICON-002` | `shield.png`; image | `BlockButton` glyph — a shield | sbed | `game-icons.net/icons/ffffff/transparent/1x1/sbed/shield.png` | CC BY 3.0 | Yes | Yes | **Required.** See the attribution block below | Free | N/A | SHA256 `2845A27016087399…`; re-fetchable from the URL | `94413571867350` | 2026-07-26 | **Shnvan** (human), 2026-07-26 / `APPROVED` | In place, not released |
| `UI-ICON-003` | `move.png`; image | *(was `DashButton` — a four-way arrow. Replaced by `UI-ICON-007` under D-028: the button never chose a direction, so the arrow misdescribed it.)* | Delapouite | `game-icons.net/icons/ffffff/transparent/1x1/delapouite/move.png` | CC BY 3.0 | Yes | Yes | Not required while unused | Free | N/A | SHA256 `6358524C91F97F49…`; re-fetchable from the URL | `89977891032744` | 2026-07-26 | **Shnvan** (human), 2026-07-26 / `REMOVED` | No — removed before release |
| `UI-ICON-004` | `sprint.png`; image | `DashButton` glyph — a running figure. Originally the sprint button (removed by D-028), **reinstated for Dash by D-030** because it promises speed without asserting a direction and matches the metaphor reference layouts use for that slot | Lorc | `game-icons.net/icons/ffffff/transparent/1x1/lorc/sprint.png` | CC BY 3.0 | Yes | Yes | **Required.** See the attribution block below | Free | N/A | SHA256 `99E9449A49398651…`; re-fetchable from the URL | `87301382738025` | 2026-07-26 | **Shnvan** (human), 2026-07-26 / `APPROVED` | In place, not released |
| `UI-ICON-005` | `vortex.png`; image | `MechanicButton` glyph — a vortex; the source describes it as "a hungry black hole", which suits the Gravity Sovereign prototype | Lorc | `game-icons.net/icons/ffffff/transparent/1x1/lorc/vortex.png` | CC BY 3.0 | Yes | Yes | **Required.** See the attribution block below | Free | N/A | SHA256 `7F9594786AD63451…`; re-fetchable from the URL | `133264139799883` | 2026-07-26 | **Shnvan** (human), 2026-07-26 / `APPROVED` | In place, not released |
| `UI-ICON-006` | `light-bulb.png`; image | `BreakthroughButton` glyph — a light bulb, reading as idea/discovery to match the Discovery Meter | Lorc | `game-icons.net/icons/ffffff/transparent/1x1/lorc/light-bulb.png` | CC BY 3.0 | Yes | Yes | **Required.** See the attribution block below | Free | N/A | SHA256 `96FFA2E672AC7D19…`; re-fetchable from the URL | `105324694393567` | 2026-07-26 | **Shnvan** (human), 2026-07-26 / `APPROVED` | In place, not released |
| `UI-ICON-007` | `fast-forward-button.png`; image | *(was `DashButton` — a forward burst. Replaced by `UI-ICON-004` under D-030: it read as a media control rather than a movement action.)* | Delapouite | `game-icons.net/icons/ffffff/transparent/1x1/delapouite/fast-forward-button.png` | CC BY 3.0 | Yes | Yes | Not required while unused | Free | N/A | SHA256 `B8F786AC2F40314C…`; re-fetchable from the URL | `80510587140014` | 2026-07-26 | **Shnvan** (human), 2026-07-26 / `REMOVED` | No — removed before release |

Add one row per asset. Do not combine a model, its third-party textures, and its embedded audio into one entry when their creators or licenses differ.

## Required attribution — HUD icons

The `UI-ICON-*` rows are **CC BY 3.0**, which makes attribution a licence condition, not a courtesy. **Five are in the place today** — `001`, `002`, `004`, `005`, `006` — so this obligation is live now and blocks release, not merely publication of art. (`003` and `007` are `REMOVED` and need no credit while unused.)

> Icons by **Lorc**, **sbed**, and **Delapouite** — [game-icons.net](https://game-icons.net) — licensed under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0/).

The game-icons.net FAQ states that for a video game the mention may be reachable from a menu. **The game currently has no credits or settings menu to put it in** — tracked as **Q-024**. Recorded as D-027.

Two rules from the top of this document apply directly and were followed: the per-icon licence was checked on each icon's own page rather than assumed from the site (the set is mixed CC BY 3.0 and Public Domain), and each icon is its own row because the three authors differ.

The `TOOL-*` rows above are recorded as `HOLD` and `RESEARCH` so the research in [TOOLING_AND_PIPELINE.md](TOOLING_AND_PIPELINE.md) cannot be mistaken for approval. Per the rule above, `unclear` is `HOLD`.

**Warning on Moon Animator.** Several Creator Store listings named "Free Moon Animator 2", and several GitHub mirrors, are reuploads or cracks. Using one on a commercial project is both a licensing and a supply-chain risk, and would fail the "a marketplace listing does not prove its uploader owns the work" rule above.

The pinned code toolchain in `rokit.toml` (Rojo, Wally, StyLua, Selene, luau-lsp) is free and open source and installs outside the Roblox place, so it is recorded in D-018 rather than here. Any **Wally package** that ships inside the place does need a row.

## Per-asset review checklist

- [ ] Exact creator and recoverable source identified.
- [ ] Exact license or written permission archived.
- [ ] Commercial Roblox use permitted.
- [ ] Modification and redistribution terms understood.
- [ ] Attribution text and placement recorded.
- [ ] Trademark, likeness, privacy, cultural-property, and endorsement risks reviewed.
- [ ] Cost received explicit user approval when non-zero.
- [ ] Original file and cryptographic hash recorded.
- [ ] Mesh topology, textures, LODs, scale, pivots, and naming reviewed.
- [ ] Scripts, remotes, packages, hidden objects, and external dependencies inspected.
- [ ] Roblox moderation and permissions passed.
- [ ] Internal owner, Roblox asset ID, source file, and reimport path recorded.
- [ ] Performance and visual-quality acceptance passed.
- [ ] Final status set by a named reviewer.

**Q-023 is RESOLVED (2026-07-26): a human must name themselves.** An agent may research a row, identify the creator, verify the licence, record hashes and asset IDs, and prepare everything — but the final status is set by a person, because this field exists to record accountability for a rights decision and an agent cannot carry that. The `UI-ICON-*` rows were prepared by an agent and signed by **Shnvan**, which is the pattern to follow.

**One consequence to action:** `REF-ARENA-001` is still signed by "Codex", an AI agent. Under this resolution it is **not** reviewed, and should be re-signed by a human or left explicitly at `REFERENCE ONLY` with no human approval claimed. It has not been changed here, because re-signing someone else's row is exactly the thing this rule forbids.

## Related documents

- [IP, Identity, and Content Safety](IP_CONTENT_SAFETY.md)
- [Omniscience Coliseum Exhibit Accuracy](OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md)
- [Roblox Game Development Playbook](ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md)
