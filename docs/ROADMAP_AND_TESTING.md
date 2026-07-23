# Roadmap and Testing

The schedule is gate-based. Available hours do not justify advancing when the current interaction is not yet fun or stable.

## Four-week prototype plan

| Week | Goal | Required evidence |
|---|---|---|
| 1 | Tool setup, graybox, input, combat state, dummy, health, death, respawn | IDE-to-Studio sync works; no stuck lifecycle states in repeated solo tests |
| 2 | Four-hit M1, hit validation, block, dash, hitstun, knockback, ragdoll, escape | Two clients can complete repeated attack/block/KO loops |
| 3 | Gravity Well, cooldown, meter foundation, KO/assist, session leaderboard, touch UI | Ability is server-validated and stable under two and eight clients |
| 4 | External playtests, mobile and performance pass, iteration, go/no-go review | Testers understand, re-engage, and identify combat—not art—as the reason to continue |

Do not use unused week time to begin another fighter. Use it to test, simplify, tune, or improve feedback.

## Test ladder

Run tests from cheapest to most representative:

1. Pure shared-module checks where possible.
2. Studio solo play.
3. Server and two clients.
4. Device emulation.
5. Server and eight clients.
6. Small external private-server playtest.

Failure at an earlier level blocks the later level.

## Required test matrix

| Area | Test cases |
|---|---|
| Character lifecycle | Spawn, reset, die during attack, die during ability, respawn repeatedly, player leaves |
| Input | Rapid M1, held input, simultaneous block/attack, dash with no direction, mobile button overlap |
| State machine | Stun during wind-up, ragdoll during ability, block released during latency, escape on and off cooldown |
| Networking | Duplicate request, reordered sequence, invalid payload, `NaN`/infinite vector defense, spam rate |
| Hit validation | Out-of-range target, target behind wall, target behind attacker, same target hit twice, protected target |
| Block | Front, edge of arc, side, back, block during stun, guard-breaking tag later |
| Gravity Well | Cast too far, inside geometry, target dies, caster dies, target resets, overlapping wells |
| KO/assist | Normal KO, two attackers, environmental fall, reset, void death, disconnect |
| Respawn | Spawn protection expires, cancels on attack, prevents outgoing damage, no spawn trap |
| Scale | One, two, four, and eight clients; VFX readability and server/frame performance |

## Severity

- **P0:** data/security issue, remote exploit, server crash, or combat cannot continue.
- **P1:** common stuck state, wrong KO, invulnerability, cooldown bypass, or broken mobile control.
- **P2:** inconsistent timing, unclear feedback, visual desync, or recoverable edge case.
- **P3:** polish issue.

No P0 or P1 issue may be knowingly carried through the prototype gate.

## External playtest protocol

Use at least three people who did not watch development.

1. Do not explain controls verbally at first.
2. Observe whether they move, attack, block, dash, and re-enter combat.
3. Record where they stop or ask questions.
4. After play, ask:
   - What did you think your goal was?
   - Why did attacks land or fail?
   - Which action felt best?
   - Which moment felt unfair or confusing?
   - Would you immediately play another five minutes? Why?
5. Ask what they want more of only after recording first impressions.

Do not lead with “Would this be good with better art?”

## Prototype success gate

Continue to the full Gravity Sovereign kit when:

- At least three external testers can begin fighting without live coaching.
- Most testers use attack and dash; block discovery is visible or clearly fixable through UI.
- At least three out of five test sessions show voluntary re-engagement after the first death.
- Players can explain at least one cause of a successful or failed hit.
- No P0 or P1 issue remains.
- The two-client loop survives at least 20 repeated KOs and respawns.
- The eight-client test remains playable and readable on the target development machine.
- Mobile controls fit and all required actions are reachable in landscape orientation.

These are prototype gates, not public-retention claims.

## Stop or redesign signals

- Players avoid combat after one death.
- Basic attacks feel delayed even before art/VFX load.
- Defenders cannot understand or escape damage sequences.
- Server validation produces unacceptable latency and no bounded design adjustment helps.
- The arena is readable only with two players.
- Testers praise only the concept or character, not an interaction.

## Playtest note template

```markdown
### Playtest YYYY-MM-DD

- Build/commit:
- Studio mode and client count:
- Devices:
- Testers:
- Task being tested:
- What happened:
- Repeated confusion:
- Best moment:
- Unfair moment:
- P0/P1 issues:
- Metrics:
- Decision:
- Next change:
```

## Public-alpha gate

Do not schedule public alpha until:

- Scope B passes.
- Three fighters pass their production gates.
- Onboarding, saving, moderation-safe content, analytics, and rollback plans exist.
- The title and assets pass the release checklist in `IP_CONTENT_SAFETY.md`.
