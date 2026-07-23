# Asset Provenance Ledger

**Status:** operating record; no production exhibit assets approved

**Applies to:** every external or generated model, mesh, texture, image, animation, audio file, font, plugin, extension, code dependency, dataset-derived visual, or commissioned work

**Last reviewed:** 2026-07-23

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
| `REF-ARENA-001` | `ChatGPT Image Jul 23, 2026, 07_15_55 PM (1).png`; image | Coliseum composition and mood reference | User-provided generated image | `C:\Users\Ivan\Downloads\ChatGPT Image Jul 23, 2026, 07_15_55 PM (1).png` | Source rights not verified; reference use only | No | Unclear | N/A while unshipped | None | N/A | Not copied into repository; hash not recorded | N/A | 2026-07-23 | Codex / `REFERENCE ONLY` | No |

Add one row per asset. Do not combine a model, its third-party textures, and its embedded audio into one entry when their creators or licenses differ.

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

## Related documents

- [IP, Identity, and Content Safety](IP_CONTENT_SAFETY.md)
- [Omniscience Coliseum Exhibit Accuracy](OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md)
- [Roblox Game Development Playbook](ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md)
