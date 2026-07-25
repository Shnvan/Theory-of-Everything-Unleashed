# Design Philosophy

**Status:** the principles are LOCKED as design doctrine. The open art and feel questions this document frames stay OPEN.

**Purpose:** [PROJECT_BRIEF.md](PROJECT_BRIEF.md) states five pillars. Pillars alone do not settle arguments about a specific move. This document turns them into rules a designer can apply to one ability and get the same answer twice.

Use it when designing any move, ability, character mechanic, Breakthrough, VFX, HUD element, or sound. Combat behavior lives in [COMBAT_SYSTEM.md](COMBAT_SYSTEM.md); this is the reasoning behind it.

---

## The one-line design test

> Can the player who lost explain why they lost, and name the thing they would do differently?

If no, the design is not finished, however good it looks. Every rule below is a way of making that answer reachable.

---

## From pillars to rules

### 1. Science becomes spectacle

An ability must read as a *specific* scientific idea, not as generic energy. A player should be able to name what it is doing — pulling, refracting, chaining, bending — from watching it once.

- Every ability answers: **what phenomenon is this, and what does it do to bodies in space?**
- Prefer forces the player already intuits: pull, push, redirect, slow, reflect.
- Reject any effect whose only description is "damage in an area." That is a placeholder, not a design.

### 2. Responsive combat with dramatic payoff

Basics are fast and interruptible. Big abilities may be committed and cinematic. Neither may take control away from anyone who did not choose to be there.

- Basic attacks and defensive options must feel immediate under normal test latency.
- A committed ability may lock its *user*. It may never freeze the server, seize another player's camera, or hold a defeated player beyond the normal death flow.
- **Presentation never carries gameplay timing.** VFX, camera shake, and hit-stop decorate a decision the server already made. If removing an effect changes what happens, the effect is load-bearing and must be fixed.

### 3. Social chaos

Interruptions, knockback, ragdolls, and near-escapes are the product, not noise to be smoothed away.

- Design for third-party interference. Two players fighting should be interruptible by a third; that is a feature.
- Chaos must stay *readable*. Eight players in one arena is the target, so every effect is judged at eight-player density, never in isolation.
- Every crowd-control effect has an end condition. No permanent stun loops.

### 4. Fair competition

- **Monetization never sells combat power.** No stat, cooldown, range, or damage difference is ever purchasable.
- Cosmetics may not confer information or concealment advantages: no smaller silhouette, no harder-to-read telegraph, no quieter attack.
- Spawn protection prevents camping without becoming an attack-safe scouting window.

### 5. Small systems, reusable content

- A fighter supplies **data**, not systems. If a new character needs its own health, KO, stun, or respawn logic, the universal system is wrong and gets fixed instead.
- No move invents its own invulnerability, stun, or lock flag. State lives in one place with one priority order.

---

## The counterplay contract

Every offensive option must have at least one of these, and the designer must name which:

| Counter | Meaning |
|---|---|
| **Avoidable** | Movement, dash, or spacing can beat it. |
| **Blockable** | The frontal block arc stops or reduces it. |
| **Interruptible** | A third party or a faster option can stop it during startup. |
| **Punishable** | Whiffing or being blocked leaves the user exposed. |

An ability with none of these is not shipped. An ability with only one is a balance risk and gets flagged in its move spec.

Corollary, from the combat-feel gate: **a successful opening must not guarantee an unavoidable full-health KO.**

---

## Telegraphs and readability

The defender's information must arrive in time to matter.

- **Startup is visible before the hit is committed.** Longer, stronger, and less avoidable means a longer and clearer telegraph.
- Telegraph the *danger area*, not just the caster. A ground field shows its edge; a line attack shows its line.
- A telegraph reads from gameplay camera distance, at eight-player density, on the smallest supported viewport.
- Guard-breaking and unblockable moves need the strongest telegraphs in the game, because they remove the defender's default answer.
- Readability outranks mood. If lighting, post-processing, or effect density hides an incoming attack, the presentation loses.

---

## Feedback hierarchy

When several things happen at once, this is the priority order for the player's attention. Higher entries must never be obscured by lower ones.

1. **My state** — am I stunned, blocking, ragdolled, protected, dead?
2. **Incoming danger** — what is about to hit me, and from where?
3. **My action's result** — did it hit, get blocked, or miss?
4. **My resources** — health, cooldowns, Discovery Meter.
5. **Ambience and spectacle** — everything else.

Rules that follow from it:

- Hit, block, and miss must be distinguishable **both** visually and audibly. Neither channel alone is sufficient.
- Invalid actions get explicit feedback. Silence reads as a bug and teaches players nothing.
- A cosmetic failure must never block combat simulation.

---

## Colour and audio language

Colour carries meaning, so it is assigned once and reused, never chosen per effect.

| Meaning | Channel |
|---|---|
| The player's own abilities | The fighter's identity colour |
| Incoming danger to me | A single reserved warning treatment, consistent across all fighters |
| Blocked | One shared block treatment, character-independent |
| Protected or invulnerable | One shared, obvious treatment |
| Environment and ambience | Desaturated relative to all of the above |

Colour is never the *only* carrier of a critical distinction — shape, motion, and sound must also differ, so the game stays readable for colour-blind players and on low-quality graphics settings.

Audio priority mirrors the feedback hierarchy: state changes over incoming attacks over own-action results over resources over ambience. A critical cue must be identifiable with the music muted.

---

## The consistency checklist

Apply to every new move, ability, mechanic, Breakthrough, and character. A "no" is a blocker, not a note.

- [ ] The phenomenon is nameable, and the ability does what its name implies.
- [ ] At least one counter from the counterplay contract is named.
- [ ] Startup is telegraphed proportionally to its power and unavoidability.
- [ ] It reads at eight-player density on the smallest supported viewport.
- [ ] Hit, block, and miss are distinguishable visually **and** audibly.
- [ ] It has a clear mobile input, not a keyboard-first design with a touch afterthought.
- [ ] No new stun, lock, or invulnerability flag; it uses the shared state model.
- [ ] Every crowd-control effect has an end condition.
- [ ] All tunable numbers live in shared config, not in the move's code.
- [ ] Cleanup is defined for normal completion, interruption, death, and target removal.
- [ ] Presentation carries no gameplay timing.
- [ ] It sells no combat power and confers no cosmetic advantage.
- [ ] It contains no blood, dismemberment, torture, or realistic death (D-008).
- [ ] It does not reproduce another game's move, name, presentation, or terminology.

---

## Open questions this document frames but does not decide

These stay OPEN in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). What follows is the decidable form of each, so the choice can be made quickly when its deadline arrives.

**Q-001, combat feel.** The pillars already constrain this to a hybrid: pillar 2 requires responsive basics, pillar 1 requires spectacle in the big moments. The remaining choice is only *how heavy* the abilities are — specifically, the longest acceptable commitment on a normal ability. Decide it as a number of seconds, then tune.

**Q-002, camera.** The hard part is not distance or FOV, it is whether FFA gets target lock. The counterplay contract argues against hard lock: lock removes spacing as a skill, and in a three-way fight it picks the wrong target. Soft directional assist preserves spacing while keeping mobile viable. Decide lock behavior first; distance and FOV are then tuning.

**Q-007, rig style.** Constrained by the readability rules above more than by aesthetics — silhouettes must stay distinguishable at gameplay distance with eight fighters on screen. R15-compatible proportions also make the animation pipeline cheaper (see [TOOLING_AND_PIPELINE.md](TOOLING_AND_PIPELINE.md)).

**Q-008, art direction.** Note that the arena has already answered this by precedent: D-016 committed to aged marble, dark stone, brass, glass, and restrained energy accents, while D-016 itself states it does not resolve the project's broader art direction. The real decision is whether characters match that restrained palette or contrast against it. Either is defensible; leaving it undecided while more art is made is not.
