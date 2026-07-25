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

Add one row per asset. Do not combine a model, its third-party textures, and its embedded audio into one entry when their creators or licenses differ.

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

**Q-023 is open on what "named reviewer" means.** The only pre-existing row records "Codex", an AI agent, as its reviewer. The recommended answer is that an agent may prepare and research a row but a human names themselves on the final status, because the reviewer field exists to record accountability for a rights decision. Until Q-023 is resolved, treat any agent-signed row as `RESEARCH` rather than reviewed.

## Related documents

- [IP, Identity, and Content Safety](IP_CONTENT_SAFETY.md)
- [Omniscience Coliseum Exhibit Accuracy](OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md)
- [Roblox Game Development Playbook](ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md)
