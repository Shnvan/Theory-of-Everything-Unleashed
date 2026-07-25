# Technical Architecture

The prototype uses Roblox Studio for the place and assets, an external IDE for Luau and documentation, and **Rojo** to sync the three script-only folders (D-018; Script Sync remains a documented fallback).

Engineering habits and reviewable checks derived from this document are in [DEVELOPER_RULES.md](DEVELOPER_RULES.md). Where the two disagree, this document wins.

## Architecture goals

- Responsive local presentation.
- Server-authoritative competitive results.
- Reusable universal combat systems.
- Character behavior defined without copying entire combat stacks.
- Easy cleanup on death, reset, disconnect, and respawn.
- No framework dependency until a demonstrated need appears.

## Local source tree

Present state marked, planned entries unmarked.

```text
src/
  shared/                            -> ReplicatedStorage/GameShared
    Combat/
    Characters/
    Config/
      CombatConfig.luau              exists
      InputConfig.luau               exists
    Net/
    Types/
      CombatTypes.luau               exists
  server/                            -> ServerScriptService/GameServer
    Services/
    Bootstrap.server.luau
  client/                            -> StarterPlayerScripts/GameClient
    Controllers/
      InputController.luau           exists
    UI/
    Bootstrap.client.luau            exists
```

Exact filenames may evolve, but the layer boundaries must remain. `default.project.json` encodes the three mappings; `rojo build` output is a syntax check, not the game place, and must never be published over it.

Note that the folder name inside each mapped Studio location is supplied by the mapping, not by a folder on disk. Files live directly at `src/client/...`, not `src/client/GameClient/...` — the extra level was a real bug, corrected on 2026-07-25.

## Studio mapping

| Studio location | Local folder | Responsibility |
|---|---|---|
| `ReplicatedStorage/GameShared` | `src/shared` | Shared types, configuration, definitions, pure state helpers |
| `ServerScriptService/GameServer` | `src/server` | Authoritative combat, validation, damage, KOs, respawn |
| `StarterPlayer/StarterPlayerScripts/GameClient` | `src/client` | Input, predicted presentation, camera, VFX, sound, HUD |

Keep non-script instances outside these synced code folders. Rojo would overwrite them on sync, and the fallback Script Sync path ignores most non-script instances and does not preserve script attributes or tags. Anything code resolves by name inside Studio needs a written contract instead — see [HUD_AND_UI_SPEC.md](HUD_AND_UI_SPEC.md).

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

The shared type is now real code, in `src/shared/Types/CombatTypes.luau`:

```luau
export type ActionRequest = {
    sequence: number,
    action: ActionName,          -- BasicAttack | Ability1..4 | Block | Dash | Mechanic | Breakthrough | Sprint
    phase: InputPhase,           -- Begin | End | Cancel
    direction: Vector3?,
    targetPosition: Vector3?,
}
```

This reconciles an earlier conflict. This document previously specified `BlockStart`/`BlockEnd` and `Ability` plus a numeric `slot`, while the client emitted `Block` plus a phase and explicit `Ability1..4`. Two shapes existed for one concept before a single remote was written, because the only type contract lived in a client module.

The resolution keeps the client's form, for two reasons. A phase generalizes: every future hold action gets release semantics for free, where `XStart`/`XEnd` needs a new pair of names each time. And explicit ability actions let the server check **one** union exhaustively instead of validating a tag and then range-checking a slot — one validation path rather than two. Use `CombatTypes.getAbilitySlot` where a slot number is genuinely needed.

`ActionRequest` deliberately carries less than the client's own `ActionInput`. Device identity (`inputType`, `keyCode`) is useless to the server, and `timestamp` comes from `os.clock()` — a client-monotonic value with an arbitrary epoch that cannot be compared against server time and is not a substitute for `sequence`.

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

- `CombatTypes` **(exists)**: typed state and result shapes, the state-priority table, and the reconciled `ActionRequest`.
- `CombatConfig` **(exists)**: universal tunables, each labelled LOCKED or DEFAULT.
- `InputConfig` **(exists)**: action, bind name, touch-button name, hold flag, and keybinds in one table.
- `CombatStateMachine`: legal transition rules. Consumes `CombatTypes.STATE_PRIORITY`.
- `CharacterDefinitions`: data for available fighters and ability slots.
- `AbilityDefinitions`: cooldown, range, tags, and presentation IDs.
- `NetTypes`: remote payload types and validation helpers.

Keep shared modules **pure** — no services, no instances, no side effects. That is what makes transition legality, cooldown math, meter clamping, assist attribution, and block-arc geometry unit testable without the engine, which is the only way to stop every combat change costing a manual two-client playtest.

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

## Keeping the door open to Server Authority

Roblox shipped engine-level client prediction and rollback resimulation as a Client Beta in April 2026 — after this document was first written. D-020 defers adoption to a timeboxed M2 spike, because the beta's documented gaps hit this game directly. See [TOOLING_AND_PIPELINE.md](TOOLING_AND_PIPELINE.md) for the specifics.

Until that spike reports, keep the option cheap:

- Put combat simulation in modules that take state and inputs and return results. Do not entangle it with remote plumbing, so it could later run under `BindToSimulation` without a rewrite.
- Keep presentation strictly downstream of simulation. Rollback resimulation replays simulation, and anything with a side effect baked into it will replay that side effect.
- Do not build a hand-rolled prediction or reconciliation framework in the meantime. The current plan — immediate reversible wind-up, server-confirmed results — is sufficient for M1 and M2 and is not wasted either way.

## Studio dependencies

Any code that resolves a Studio instance by name needs a written repository-side contract, because non-script instances stay out of the synced folders and therefore cannot be versioned as instances. See [HUD_AND_UI_SPEC.md](HUD_AND_UI_SPEC.md) and D-022. Without one, renaming a single instance silently disables a feature with no compile-time signal.

## Test requirement

Any change to remotes, hit detection, state transitions, damage, cooldowns, KOs, or respawn is incomplete until it passes a Studio server-and-two-clients test. Input and HUD changes also require mobile device emulation.

Static gates run first and are not a substitute: `stylua --check src`, `selene src`, `luau-lsp analyze`, `rojo build`. They are enforced in CI.
