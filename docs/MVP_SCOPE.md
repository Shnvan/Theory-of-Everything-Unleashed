# MVP Scope

This project has three different scope levels. Do not treat the long-term roster as the first build.

## Scope A — Combat foundation

**Current scope.**

### Included in Scope A

- One graybox arena.
- One player character using placeholder visuals.
- One training dummy.
- Keyboard/mouse and touch input paths.
- Sprint and directional dash.
- Four-hit M1 combo.
- Frontal block.
- Health, damage, hitstun, knockback, ragdoll, death, and respawn.
- One limited ragdoll escape.
- One server-approved gravity test ability.
- Server-authoritative validation.
- Solo, two-client, and multi-client Studio tests.

### Excluded from Scope A

- Full character kit.
- Breakthrough moveset.
- Final art, monetization, saving, mastery, onboarding, or public release.

### Scope A exit gate

Two clients can repeatedly attack, block, escape, KO, and respawn without stuck states, exploitable client-declared damage, or confusing feedback. Testers say the basic interaction itself has potential.

## Scope B — Gravity Sovereign vertical slice

Build only after Scope A passes.

### Included in Scope B

- Gravity Sovereign's approved normal kit.
- Character-specific `R` mechanic.
- Discovery Meter and one Breakthrough.
- KO and assist credit.
- Session leaderboard.
- Short Final Proof KO effect.
- Placeholder but coherent animation, VFX, SFX, HUD, and mobile buttons.
- Up to eight players in a local/private test.
- Limited graybox breakable elements only if combat is already stable.

### Excluded from Scope B

- Other playable fighters.
- Mastery, persistent currency, store, or public launch.
- Large-scale map destruction.

### Scope B exit gate

Three or more external testers understand the controls without live coaching, re-enter combat after dying, and ask to play again. Network and mobile tests remain stable.

## Scope C — Public alpha

This is a future target, not the current build.

### Content budget

- One finished arena based on the approximately 759-stud combat disc, with an estimated clear-lane crossing time of about 53 seconds at default movement speed.
- Maximum eight players per server.
- Three fighters:
  - Gravity Sovereign.
  - Eureka Engineer.
  - Renaissance Mind.
- Universal combat foundation.
- Complete normal kit and Breakthrough for each fighter.
- KOs, assists, streaks, and a server leaderboard.
- Five-second respawn and short spawn protection.
- Practice dummies.
- Keyboard/mouse and mobile controls.
- Lightweight onboarding.
- Minimal mastery and cosmetic rewards.
- Basic analytics and moderation-safe presentation.

### Explicitly outside public alpha

- Ranked ladder or skill rating.
- Private best-of-three 1v1.
- Story campaign or Arcade ladder.
- Trading, clans, tournaments, gear stats, loot boxes, gacha, or battle pass.
- More than one map.
- More than three playable fighters.
- Full destructible city or custom moveset builder.
- Long executions that pause or trap players.
- Pay-to-win damage, cooldown, health, meter, or character advantages.

## Scope-change rule

A feature enters the current scope only when:

1. It is necessary to test the current exit gate.
2. Its cost and failure cases are understood.
3. A lower-cost placeholder cannot answer the same question.
4. The decision is recorded in `DECISION_LOG.md`.

“A competitor has it” is not sufficient.
