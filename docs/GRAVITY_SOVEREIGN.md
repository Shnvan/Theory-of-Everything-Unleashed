# Gravity Sovereign

**Internal ID:** `gravity_sovereign`  
**Historical inspiration:** Isaac Newton  
**Role:** approachable all-rounder  
**Prototype status:** first fighter  
**Design status:** identity and first ability are approved; full kit is DRAFT

## Player fantasy

> Control force, motion, gravity, and light so every enemy position becomes a physics problem.

Gravity Sovereign should teach the universal combat system without being weak at higher skill. The kit should reward spacing, pulling a target into danger, and redirecting momentum.

## Identity rules

- Use an original stylized model, outfit, face, proportions, color language, animation, and voice treatment.
- Draw from public-domain historical facts and scientific concepts.
- Do not copy a living actor, a specific film, a copyrighted portrait treatment, or another game's Newton design.
- The select screen leads with `Gravity Sovereign`; historical context may identify Isaac Newton only after the project completes its clearance record.

## Visual language

- Gravity: dark indigo fields, orbit lines, bent particles, and clean force arrows.
- Motion: white or cyan vector trails.
- Optics: prismatic spectral accents.
- Silhouette: readable scholar-superhero, not a photorealistic historical reconstruction.
- Effects must remain legible on a phone screen and against the graybox arena.

## Scope A implementation

Only implement:

- Universal four-hit M1.
- Universal block and dash.
- Universal damage states.
- **Gravity Well** as the first character ability.

### Gravity Well — approved prototype ability

**Purpose:** test an area ability, server hit validation, controlled pull, cooldown, and combo setup.

**Behavior draft:**

1. Player aims at a bounded ground position.
2. Server validates the action, range, state, and cooldown.
3. A short telegraph appears.
4. The well pulls valid opponents toward its center over a brief duration.
5. It applies modest damage or a final pulse, not a long unavoidable stun.

**Prototype constraints:**

- No client-provided victim list.
- Clear maximum cast range and radius.
- Spawn-protected, dead, or otherwise invalid targets are ignored.
- Pull force must clean up on death, reset, target removal, and ability end.
- It must not pull players permanently into geometry.
- The effect must have an obvious edge and warning.

Exact radius, duration, damage, pull strength, and cooldown are DEFAULT values to tune in a shared definition.

## Draft full normal kit

Do not implement this table as a complete requirement until the user approves it.

| Slot | Working name | Function | Design risk |
|---|---|---|---|
| `1` | Vector Impulse | Quick directed force blast for neutral and knockback | Could become a generic projectile |
| `2` | Gravity Well | Telegraphed pull and setup field | Crowd-control loops and geometry issues |
| `3` | Prism Divide | Optics-based line attack or refracted follow-up | Visual clutter and overlap with zoners |
| `4` | Inertial Crash | Committed movement or slam that converts momentum into impact | May overlap the universal dash |
| `R` | Revector | Short character mechanic that redirects force or changes the next physics interaction | Must remain understandable on mobile |

The final kit must include:

- One reliable neutral tool.
- One setup or control tool.
- One defensive or repositioning decision.
- One committed payoff.
- Counterplay through telegraphs, flanking, cooldowns, or recovery.

## Draft Breakthrough

**Working name:** Laws Unbound  
**Status:** DRAFT

Breakthrough should make gravity visibly unstable for a limited time. It may replace the four ability slots with a stronger, coherent moveset. It must not grant endless invulnerability, permanent flight, or a server-wide cutscene.

Possible themes:

- Orbital motion.
- Extreme gravity.
- Reversal of vectors.
- Prismatic singularity.

Exact moves, duration, meter gain, death behavior, and cancellation rules remain OPEN.

## Final Proof concept

**Status:** DRAFT presentation built only after combat passes.

A defeated target compresses into a harmless geometric gravity field, flashes through a prism, and exits through a small rift. Target duration is 1–2 seconds. There is no blood, body damage, copied sound cue, forced victim camera, or server pause.

## Strengths and weaknesses

### Intended strengths

- Flexible range.
- Strong positional control.
- Clear combo setup.
- Good teaching character.

### Intended weaknesses

- Control effects are telegraphed.
- Strong payoff requires positioning.
- Missed fields create punishable cooldown windows.
- Should not match dedicated grapplers at close-range control or dedicated zoners at long range.

## Implementation order

1. Universal combat foundation.
2. Placeholder character definition.
3. Gravity Well with server validation.
4. Two-client and geometry-edge-case testing.
5. Combat-feel review.
6. Approve the full normal kit.
7. Build one move at a time.
8. Approve and build `R`.
9. Approve and build Breakthrough.
10. Add Final Proof and production presentation.
