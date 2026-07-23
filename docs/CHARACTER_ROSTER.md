# Character Roster

This is a 12-fighter roadmap, not a launch commitment.

## Naming rule

The select screen uses original fighter titles. Internal IDs use lowercase snake case. A title does not make an otherwise uncleared identity safe; character treatment must follow `IP_CONTENT_SAFETY.md`.

## Master roster

| # | Internal ID | Select-screen title | Identity status | Combat archetype | Development wave |
|---:|---|---|---|---|---|
| 1 | `gravity_sovereign` | **Gravity Sovereign** | Isaac Newton; original stylized historical portrayal | Beginner-friendly all-rounder using gravity, motion, and optics | Prototype / alpha |
| 2 | `eureka_engineer` | **Eureka Engineer** | Archimedes; original stylized historical portrayal | Heavy grappler using levers, buoyancy, mirrors, and throws | Alpha |
| 3 | `renaissance_mind` | **Renaissance Mind** | Leonardo da Vinci; original stylized historical portrayal | Gadget zoner using mechanisms, wings, and inventions | Alpha |
| 4 | `star_witness` | **Star Witness** | Galileo Galilei; original stylized historical portrayal | Ranged artillery using observation, falling bodies, and momentum | Update 1 |
| 5 | `code_pioneer` | **Code Pioneer** | Ada Lovelace; original stylized historical portrayal | Technical setup fighter using programmed traps and chained commands | Update 1 |
| 6 | `natural_theorist` | **Natural Theorist** | Charles Darwin; original stylized historical portrayal | Adaptive stance fighter that changes defenses and attacks | Update 2 |
| 7 | `optics_sage` | **Optics Sage** | Ibn al-Haytham; original stylized historical portrayal | Fast mix-up fighter using light, refraction, and visual misdirection | Update 2 |
| 8 | `storm_architect` | **Storm Architect** | Fully original character | Electricity rushdown using coils, charged movement, and chain attacks | Update 1 |
| 9 | `radiant_pioneer` | **Radiant Pioneer** | Fully original character | Area control using radiant fields, zones, and decay effects | Update 2 |
| 10 | `spacetime_savant` | **Spacetime Savant** | Fully original character | Mobility and counterplay using warps and time dilation | Update 3 |
| 11 | `atomic_catalyst` | **Atomic Catalyst** | Fully original character | High-damage bruiser using controlled chain reactions | Update 3 |
| 12 | `cosmic_theorist` | **Cosmic Theorist** | Fully original character | Advanced controller using gravity wells, horizons, and portals | Update 3 |

## Release order

### Prototype

- Gravity Sovereign only.

### Public alpha target

- Gravity Sovereign.
- Eureka Engineer.
- Renaissance Mind.

These give an all-rounder, grappler, and zoner before the roster expands.

### Update 1

- Storm Architect.
- Code Pioneer.
- Star Witness.

### Update 2

- Natural Theorist.
- Optics Sage.
- Radiant Pioneer.

### Update 3

- Spacetime Savant.
- Atomic Catalyst.
- Cosmic Theorist.

The update waves are planning order, not dates.

## Roster production gate

Do not start the next fighter until the previous required content is complete:

- Normal M1 integration.
- Four approved normal abilities.
- Approved `R` mechanic.
- Breakthrough behavior.
- Mobile input and HUD.
- Server validation.
- KO and assist behavior.
- Animation, VFX, sound, and cleanup.
- Short Final Proof effect.
- Two-client and mobile-emulation test pass.

Do not begin fighter four until all three public-alpha fighters pass.

## Original-character boundary

Storm Architect, Radiant Pioneer, Spacetime Savant, Atomic Catalyst, and Cosmic Theorist use broad scientific fields. They must not reproduce the name, face, biography, voice, quotations, clothing, signature equipment, advertising keywords, or recognizable combined identity of Tesla, Curie, Einstein, Oppenheimer, Hawking, or a film portrayal.

## Balance coverage

The full roadmap aims to cover:

- All-rounder.
- Grappler.
- Zoner.
- Rushdown.
- Setup/trap.
- Adaptive stance.
- Mix-up.
- Area control.
- Mobility/counter.
- Bruiser.
- Advanced controller.

Before approving a new kit, compare it with the roster table. If its main combat decision already exists, revise or replace it.
