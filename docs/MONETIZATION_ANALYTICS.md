# Monetization and Analytics

## Business rule

The game's goal is revenue, but the current milestone proves engagement before building a store. No monetization code belongs in Scope A.

## Monetization principles

- Never sell damage, health, cooldown reduction, meter gain, stun resistance, spawn protection, or stronger exclusive abilities.
- Every fighter needed for competitive fairness must be earnable through play.
- Paid products should express identity, celebration, or support.
- Show price and contents clearly.
- Avoid paid randomness, trading, and manipulative revive prompts in the MVP.
- Do not interrupt a new player's first fights with a purchase screen.

## Future cosmetic candidates

| Offer | Type | Timing | Status |
|---|---|---|---|
| Founder Pack: title, banner, aura, and KO effect | One-time pass | After retention evidence | DRAFT |
| Ability-color themes | Cosmetic | Public alpha or later | DRAFT |
| Entrances and victory emotes | Cosmetic | Later | DRAFT |
| Final Proof variants | Cosmetic KO presentation | After the base effect exists | DRAFT |
| Emote bundles | Cosmetic/social | Later | DRAFT |
| Mastery recolors and titles | Earned through play | Public alpha | DEFAULT |

An earlier working price for the Founder Pack was 149 Robux, but exact pricing remains OPEN and must be checked against current Roblox economics and tester purchase intent.

## Budget

Initial cash budget: approximately US$100.

| Use | Maximum plan | Gate |
|---|---:|---|
| Icon and thumbnail | $60 | Spend only after the graybox loop tests well |
| One reusable animation or VFX improvement | $25 | Spend only where a visible prototype weakness is proven |
| Contingency | $15 | Keep uncommitted |
| Ads | $0 initially | Do not buy traffic before retention evidence |

Free or self-made placeholders are correct during Scope A.

## Analytics phases

### Scope A and B

Use lightweight internal counters and structured playtest notes. Do not build a production analytics wrapper before the combat loop works.

Useful prototype observations:

- Time until first movement.
- Time until first attack.
- Time until first combat with another player.
- First death and whether the player re-engages.
- Uses of attack, block, dash, escape, and Gravity Well.
- Invalid action requests by reason.
- KO/respawn loop failures.
- Frame and server performance with increasing clients.

### Public alpha

Add deliberate analytics events with a stable schema.

Suggested events:

| Event | Important fields |
|---|---|
| `session_started` | version, platform, input type |
| `character_selected` | character ID, first selection |
| `first_combat_entered` | seconds since join |
| `ability_used` | character ID, ability ID, confirmed/rejected |
| `breakthrough_activated` | character ID, seconds since spawn |
| `player_ko` | killer character, defeated character, environmental flag |
| `player_respawned` | seconds dead, spawn ID |
| `final_proof_triggered` | character ID, effect ID |
| `onboarding_completed` | duration, skipped |
| `store_opened` | source |
| `purchase_completed` | product ID, price |
| `session_ended` | duration, KOs, deaths, assists |

Do not send a custom analytics event for every hit in production unless sampling and volume costs are understood.

## Product metrics

Prioritize:

- First-play bounce.
- Tutorial or first-fight completion.
- Time to first combat.
- Immediate re-engagement after death.
- Session length.
- Return rate, including D1 retention when sample size permits.
- Breakthrough use per session.
- Character selection distribution.
- Purchase funnel only after products exist.

Small tests are directional. Do not present five friends' behavior as statistically reliable retention.

## Initial validation targets

Prototype:

- At least three of five sessions show voluntary re-engagement after first death.
- Most testers reach meaningful combat within two minutes.
- Testers ask for another ability, character, or match rather than only visual polish.

Public-alpha targets must be set after closed-test baselines exist. Avoid inventing industry benchmarks without current comparable data.

## Revenue review

Before setting final prices or revenue projections, verify current:

- Pass and developer-product behavior.
- Platform fees and earned-Robux rules.
- DevEx eligibility, threshold, and exchange rate.
- Regional pricing and policy requirements.

Official references:

- [Roblox Analytics](https://create.roblox.com/docs/production/analytics)
- [Passes](https://create.roblox.com/docs/production/monetization/passes)
- [Developer products](https://create.roblox.com/docs/production/monetization/developer-products)
- [Roblox monetization overview](https://create.roblox.com/docs/monetize)
