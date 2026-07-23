# Technical Architecture

The prototype uses Roblox Studio for the place and assets, an external IDE for Luau and documentation, and Script Sync for selected script-only folders.

## Architecture goals

- Responsive local presentation.
- Server-authoritative competitive results.
- Reusable universal combat systems.
- Character behavior defined without copying entire combat stacks.
- Easy cleanup on death, reset, disconnect, and respawn.
- No framework dependency until a demonstrated need appears.

## Planned local source tree

```text
src/
  shared/
    Combat/
    Characters/
    Config/
    Net/
    Types/
  server/
    Services/
    Bootstrap.server.luau
  client/
    Controllers/
    UI/
    Bootstrap.client.luau
```

The `src` tree is created when Script Sync is configured. Exact filenames may evolve, but the layer boundaries must remain.

## Studio mapping

| Studio location | Local folder | Responsibility |
|---|---|---|
| `ReplicatedStorage/GameShared` | `src/shared` | Shared types, configuration, definitions, pure state helpers |
| `ServerScriptService/GameServer` | `src/server` | Authoritative combat, validation, damage, KOs, respawn |
| `StarterPlayer/StarterPlayerScripts/GameClient` | `src/client` | Input, predicted presentation, camera, VFX, sound, HUD |

Keep non-script instances outside these synced code folders. Script Sync ignores most non-script instances and does not preserve script attributes or tags.

## Responsibility boundary

### Client may

- Read local input.
- Select aim direction or a requested ground point.
- Request an action with a monotonically increasing sequence number.
- Immediately play reversible wind-up animation, input feedback, and predicted local presentation.
- Render server-confirmed VFX, SFX, camera shake, cooldown, health, and meter UI.

### Client may not

- Choose or submit the victims of an attack.
- Submit damage, stun duration, knockback result, KO, assist, meter gain, cooldown completion, currency, or respawn.
- Decide that it is invulnerable, blocking, awakened, or spawn-protected.
- replicate arbitrary Instance references for the server to trust.

### Server owns

- Character combat state and legal transitions.
- Action eligibility.
- Cooldown and request-rate validation.
- Hitbox and target eligibility.
- Damage, block result, stun, knockback, ragdoll, and recovery.
- Discovery Meter and Breakthrough.
- KO, assist, streak, death, and respawn.
- Session leaderboard.

## Request flow

```text
Input
  -> client action request
  -> server validation
  -> authoritative state transition
  -> server hit query and result
  -> replicated combat event
  -> client presentation
```

Prediction may make the local wind-up feel immediate. When the server rejects an action, the client must cancel or reconcile presentation without creating gameplay effects.

## Network contract

Prefer a small set of purpose-based remotes rather than one RemoteEvent per move.

Suggested prototype surface:

- `RequestCombatAction`: client to server.
- `CombatEvent`: server to relevant clients.
- `RequestCharacterSelection`: client to server, later.

Illustrative shared type:

```luau
--!strict

export type ActionRequest = {
    sequence: number,
    action: "BasicAttack" | "BlockStart" | "BlockEnd" | "Dash" | "Ability",
    slot: number?,
    direction: Vector3?,
    targetPosition: Vector3?,
}
```

This is a transport shape, not proof that a request is valid.

## Required server validation

For every action:

1. Player and current character exist.
2. Character is alive and belongs to the requesting player.
3. Request shape and values are valid and finite.
4. Sequence is newer than the last accepted request where applicable.
5. Request rate is plausible.
6. Current combat state permits the action.
7. Cooldown or escape charge is available.
8. Aim direction is normalized or safely normalized server-side.
9. Target point is within the allowed cast range.
10. Server performs its own target query.

For hits, also verify target state, team/FFA rules, distance, block direction, spawn protection, and per-attack duplicate-hit rules.

## Suggested modules

### Shared

- `CombatTypes`: typed state and result shapes.
- `CombatConfig`: universal tunables.
- `CombatStateMachine`: legal transition rules.
- `CharacterDefinitions`: data for available fighters and ability slots.
- `AbilityDefinitions`: cooldown, range, tags, and presentation IDs.
- `NetTypes`: remote payload types and validation helpers.

### Server

- `CombatService`: action entry point and player combat lifecycle.
- `HitService`: server-side spatial queries and per-attack hit tracking.
- `DamageService`: block, damage, stun, knockback, and death resolution.
- `AbilityService`: cooldown and character ability execution.
- `MeterService`: Discovery Meter and Breakthrough.
- `KOService`: damage contribution, KO, assist, and streak attribution.
- `RespawnService`: death delay, respawn, and spawn protection.

During Scope A, combine small services when separation would add ceremony without value. Split only when behavior becomes hard to test or reason about.

### Client

- `InputController`: keyboard, mouse, gamepad-ready actions, and touch binding.
- `CombatController`: local prediction and authoritative reconciliation.
- `CharacterController`: local character lifecycle.
- `EffectsController`: animation, VFX, SFX, hit-stop, and camera shake.
- `HUDController`: health, cooldowns, meter, and state feedback.

## State and cleanup

- Store one server combat record per active character.
- Replace or invalidate the record on respawn.
- Use a cleanup owner for connections, delayed tasks, hitboxes, forces, and temporary instances.
- Every delayed callback must confirm that its combat record and character are still current.
- Every ability must define cleanup on normal completion, interruption, death, and target removal.
- Never retain Player or character references after `PlayerRemoving` or character replacement.

## Character definition rule

A character definition may declare:

- Display name and internal ID.
- Ability slots and tunable values.
- Presentation asset references.
- Tags such as blockable, guard break, movement, field, or ragdoll.

It must not bypass server services or implement its own unrelated health, KO, or respawn system.

## Coding conventions

- New gameplay modules begin with `--!strict`.
- Use `PascalCase` for module/type names, `camelCase` for locals/functions, and `UPPER_SNAKE_CASE` only for true constants.
- Use explicit `type` exports for network and service boundaries.
- Keep configuration immutable by convention.
- Use `task.*`, not legacy `wait`, `spawn`, or `delay`.
- Do not use `_G` or hidden cross-module mutation.
- Do not swallow errors that can leave combat state locked.
- Avoid per-frame work when an event or bounded timer is sufficient.
- Keep debug visualization behind a Studio-only flag.

## Prototype data policy

- No persistent player data in Scope A or B.
- Session KOs, assists, and meter live only on the server.
- Add DataStore-backed profiles only after the public-alpha schema is deliberately designed and versioned.

## Test requirement

Any change to remotes, hit detection, state transitions, damage, cooldowns, KOs, or respawn is incomplete until it passes a Studio server-and-two-clients test. Input and HUD changes also require mobile device emulation.
