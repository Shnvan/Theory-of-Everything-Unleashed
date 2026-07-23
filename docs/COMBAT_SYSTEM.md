# Combat System

**Status:** universal rules are LOCKED; exact timing and damage values are DEFAULT and must be tuned.

## Match format

- Continuous public free-for-all.
- Target maximum: eight players.
- No rounds and no mandatory matchmaking queue.
- Players enter combat, earn KOs and assists, die, respawn, and re-engage.
- The prototype supports a training dummy and local multiplayer tests before public servers.

## Input model

| Action | Keyboard/mouse | Mobile | Rule |
|---|---|---|---|
| Basic attack | `M1` | Attack button | Four-hit universal chain |
| Abilities | `1`–`4` | Four ability buttons | Character-specific and cooldown-based |
| Block | `F` | Hold Block | Protects the facing direction |
| Dash / escape | `Q` + movement | Dash button + movement input | Directional dash; limited ragdoll escape |
| Character mechanic | `R` | Mechanic button | Unique to the fighter |
| Breakthrough | `G` | Meter button | Available only when Discovery Meter is full |
| Sprint | Movement rule to be selected | Virtual-stick rule | Must not conflict with mobile combat input |

Mobile is not a later port. Every combat action must have a clear touch equivalent and visible cooldown/state feedback.

## Prototype defaults

| Value | Starting point | Status |
|---|---:|---|
| Maximum health | 100 | DEFAULT |
| M1 chain length | 4 hits | LOCKED |
| Full uninterrupted M1 damage | About 20 total | DEFAULT |
| Combo reset after no follow-up | 1.1 seconds | DEFAULT |
| Respawn delay | 5 seconds | DEFAULT |
| Spawn protection | 2 seconds | DEFAULT |
| Ragdoll-escape cooldown | 20 seconds | DEFAULT |
| Discovery Meter maximum | 100 | DEFAULT |
| Assist lookback window | 10 seconds | DEFAULT |
| Arena crossing time | About 10 seconds | DEFAULT |

All numeric values belong in configuration modules.

## Combat states

Every character has one authoritative primary state:

- `Neutral`
- `Attacking`
- `Blocking`
- `Dashing`
- `UsingAbility`
- `Stunned`
- `Ragdolled`
- `Awakening`
- `Dead`
- `SpawnProtected`

Short flags may supplement the state only when they do not create contradictory combinations.

### State priority

From strongest to weakest:

1. Dead
2. Ragdolled
3. Stunned
4. Awakening
5. UsingAbility
6. Dashing
7. Attacking
8. Blocking
9. SpawnProtected
10. Neutral

An implementation may refine this model, but it must define legal transitions centrally. Do not let each move invent its own stun, lock, or invulnerability flags.

## M1 chain

- The chain has four attacks.
- The first three are quick hit-confirm steps.
- The fourth creates a clearer end state through knockback or knockdown.
- An input buffer may accept the next attack shortly before the current recovery ends.
- Missing, being blocked, being stunned, dashing, or exceeding the combo-reset window ends the chain.
- Air variants and branching finishers are outside Scope A unless the base chain already feels good.

The server decides whether each attack may start and which targets are valid. The client may immediately play a predicted wind-up, but it cannot report who was hit.

## Blocking

- Block is directional, not a full sphere.
- Starting prototype arc: roughly 120 degrees in front of the defender.
- Normal M1 hits from inside the protected arc deal no health damage and apply block feedback.
- Attacks from the side or back bypass block.
- No stamina or guard meter in Scope A.
- Specific future moves may be marked guard-breaking or unblockable, with strong telegraphing.
- A stunned, ragdolled, dead, or actively attacking character cannot begin blocking.

## Dash and ragdoll escape

- Directional input selects forward, backward, or side dash.
- Dash distance and recovery may vary by direction after testing.
- Dash does not automatically grant full invulnerability; any invulnerability window must be explicit and short.
- Pressing Dash while ragdolled may consume the separate escape cooldown and return the player to a recoverable state.
- The escape is defensive counterplay, not a second normal dash.

## Hitstun, knockback, and ragdoll

- Light hits use short hitstun and limited displacement.
- Combo finishers and selected abilities use knockback or ragdoll.
- Repeated crowd control must have an end condition; do not allow permanent stun loops.
- Ragdoll owns movement until recovery or a valid escape.
- Server state determines when a character can act again.
- VFX, camera shake, and hit-stop are presentation and must not be the source of combat timing.

## Spawn protection

- A respawned character begins protected.
- Protection ends when its timer expires or the protected player begins an attack or ability.
- Protected players cannot damage others.
- The UI and character presentation must make protection obvious.
- The system must prevent spawn camping without creating an attack-safe scouting exploit.

## KOs and assists

- The server records valid damage contributions.
- A normal KO goes to the most recent valid attacker within the lookback window.
- An environmental death may credit the last attacker when their knockback or ability plausibly caused it.
- An assist goes to another player who contributed meaningful recent damage; starting threshold is 10% of maximum health.
- Self-reset, disconnect, and void-death rules must be tested explicitly.
- Clients never submit their own KO or assist totals.

## Discovery Meter and Breakthrough

Not required until Scope B.

- Meter is server-owned and clamped from zero to its maximum.
- It may grow from valid damage, assists, and KOs.
- It does not grow from hitting protected targets or repeated invalid requests.
- At full meter, the player may request Breakthrough.
- The server validates state, consumes meter, and starts the timed transformation or empowered moveset.
- The client handles the dramatic presentation after server confirmation.

Exact gain rates, duration, cancel rules, and death behavior remain OPEN.

## Final Proof

In public FFA, Final Proof is a cosmetic KO signature:

- Duration target: 1–2 seconds.
- It is triggered by a server-confirmed KO.
- It does not freeze the server, take over other players' cameras, or hold the defeated player beyond the normal death flow.
- It uses energy, portals, transformations, launches, or scientific phenomena.
- It contains no blood, dismemberment, torture, realistic corpse damage, or copied franchise presentation.

## Combat-feel gate

Before more abilities or characters:

- Inputs feel immediate under normal test latency.
- Hits and blocks are visually and audibly distinguishable.
- The defender understands why an attack landed.
- A successful opening does not guarantee an unavoidable full-health KO.
- Death returns the player to meaningful action quickly.
- The system remains readable with at least four test players.
