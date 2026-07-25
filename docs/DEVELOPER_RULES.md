# Developer Rules

**Status:** LOCKED as engineering doctrine.

**Audience:** anyone writing code in this repository, human or agent.

**Relationship to other documents.** [AGENTS.md](../AGENTS.md) is the short canonical charter and stays that way by its own rule ("Keep `AGENTS.md` concise and stable"). This is the long-form rulebook behind it. [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) defines the boundaries; this document defines the habits. Where they disagree, the architecture document wins and this one gets fixed.

---

## The three rules that matter most

If you remember nothing else:

1. **The server decides consequential results.** Always. No exceptions for convenience, prototyping, or "it's only a test."
2. **Never mark a task done when only the implementation is done.** Acceptance evidence, not code, closes a task.
3. **Never claim a test you did not run.** Especially a Studio, device, or multiplayer test.

---

## Client and server boundary

Restated as checks a reviewer can apply. Every one of these is a rejection, not a suggestion.

### The client may never

- Choose or submit who was hit.
- Submit damage, stun duration, knockback, a KO, an assist, meter gain, cooldown completion, currency, or a respawn.
- Assert that it is invulnerable, blocking, awakened, or spawn-protected.
- Send an `Instance` reference the server then trusts.
- Send a value the server does not re-validate.

### The client may

- Read input, pick an aim direction or requested ground point, and send a request with a sequence number.
- Play reversible wind-up and local feedback immediately.
- Render results the server confirmed.

### Every server-side action handler validates, in order

1. The player and their current character exist.
2. The character is alive and belongs to the requester.
3. Values are present, correctly typed, and **finite** — reject `NaN` and `inf`.
4. The sequence is newer than the last accepted one.
5. The request rate is plausible.
6. The current combat state permits this action.
7. The cooldown or charge is available.
8. The aim direction is normalized server-side; do not trust the client's magnitude.
9. Any target point is within the allowed cast range.
10. The server runs its **own** target query.

For hits, additionally: target state, FFA rules, distance, block direction, spawn protection, and per-attack duplicate-hit rules.

**Do not** write the validation as a comment saying it happens elsewhere. It happens in the handler.

---

## Luau rules

### Always

- `--!strict` at the top of every gameplay module.
- `PascalCase` for modules and types, `camelCase` for locals and functions, `UPPER_SNAKE_CASE` only for genuine constants.
- Export types at every boundary another layer consumes.
- `task.spawn`, `task.delay`, `task.wait`.
- Return `table.freeze(Module)` from configuration modules.
- Put every tunable number in a shared config module. A magic number in a gameplay file is a defect.

### Never

- `_G`, or hidden cross-module mutation.
- Legacy `wait`, `spawn`, or `delay`. Selene rejects these.
- One `RemoteEvent` per move. Use the small purpose-based surface.
- A per-frame loop where an event or a bounded timer would do.
- Swallowing an error that can leave combat state locked.
- Debug visualization that is not behind a Studio-only flag.

### Types shared between client and server go in `src/shared`

Not in whichever layer needed them first. The project already produced two incompatible shapes for one wire concept this way; see S8 in [PROJECT_AUDIT_2026-07-25.md](PROJECT_AUDIT_2026-07-25.md).

---

## Lifecycle and cleanup

The most common source of real bugs in a combat game. Treat these as mandatory.

- One server combat record per active character. Replace or invalidate it on respawn.
- **Every delayed callback re-checks that its combat record and character are still current** before acting. A 2-second ability that resolves after the player died must do nothing.
- Every ability defines cleanup for four cases: normal completion, interruption, death, and target removal. Not three.
- Every connection, task, temporary instance, hitbox, and force has an owner that disposes of it.
- Never retain a `Player` or character reference past `PlayerRemoving` or character replacement.
- A held input can latch. Any state driven by a hold must have a release path that fires even when the release event never arrives — window focus loss, GUI destruction, disconnect. This project already shipped that bug once (S10).

---

## Simulation versus presentation

- Combat state, damage, and timing are simulation. Animation, VFX, sound, camera shake, hit-stop, and UI are presentation.
- Presentation reads simulation. Simulation never reads presentation.
- A cosmetic failure must never block combat. If a missing asset can stop a hit registering, the code is wrong.
- Do not derive a gameplay duration from an animation length. Configure the duration; drive the animation from it.

---

## Studio and repository boundary

- Code is the repository's truth. The place, parts, GUI, rigs, animation, VFX instances, and audio are Studio's truth.
- `*.rbxl` is gitignored, so **the Studio place has no repo-side backup.** Publish privately at every checkpoint with a version note. This is the only recovery path that exists.
- `rojo build` output is a syntax check, not the game. **Never publish it over the real place** — it contains none of the arena.
- Anything code depends on by name inside Studio needs a written contract in the repository. See [HUD_AND_UI_SPEC.md](HUD_AND_UI_SPEC.md) for the pattern and for why.

---

## Verification ladder

Cheapest first. An earlier failure blocks later confidence; a later pass does not excuse a skipped earlier one.

1. `stylua --check src`, `selene src`, `luau-lsp analyze`. Free, fast, run every time.
2. Unit tests over pure logic.
3. Studio solo play.
4. Server with two clients. **Required** for any change to remotes, hit detection, state transitions, damage, cooldowns, KOs, or respawn.
5. Device emulation. **Required** for any input or HUD change.
6. Network simulation with latency, jitter, loss, and duplicated or reordered requests.
7. Eight-client test at target scale.
8. A physical lower-end device.
9. A small uncoached playtest.

---

## Commits

- One coherent change per commit. A refactor and a behavior change are two commits.
- Prefix: `feat:`, `fix:`, `refactor:`, `docs:`, `build:`, `chore:`, `test:`.
- If the change is Studio-side, say so in the body, because the diff will not show it. Four commits in this project's history are labelled `feat:` and contain no code for exactly this reason.
- State what was verified and what was not. "No Studio test was run" is a valid and useful line.
- Never commit credentials, cookies, `.env` files, or local Studio settings.
- Never use `--no-verify` or skip hooks. Fix the cause.

---

## Pre-commit checklist

- [ ] The behavior I changed is the behavior I intended to change, and nothing else moved.
- [ ] Static checks pass: format, lint, type check, build.
- [ ] The cheapest relevant runtime test ran, and I can say which.
- [ ] Multiplayer or device tests ran if the change touches remotes, combat, input, or HUD — or I have said explicitly that they did not.
- [ ] Failure, interruption, death, respawn, and rejoin paths clean up.
- [ ] No new magic numbers; new tunables went to shared config.
- [ ] No new client authority over a consequential result.
- [ ] Docs, decision records, and `TASKS.md` match reality.
- [ ] The Studio place is saved with a version note if Studio changed.
- [ ] The commit message names what was verified and what remains at risk.

---

## Things this project has already got wrong once

Kept here so they are not repeated. Full detail in [PROJECT_AUDIT_2026-07-25.md](PROJECT_AUDIT_2026-07-25.md).

| Mistake | Rule it violated |
|---|---|
| The only implementation sat untracked for a whole session's worth of work | Keep work recoverable; commit checkpoints |
| A keybind decision was made in code while the docs said "to be selected" | Never silently convert an OPEN item into a requirement |
| Ten GUI instance names were asserted by string with no written contract | Studio dependencies need a repo-side spec |
| A binding name was typed three times in three places | One source of truth for every value |
| A held touch latched an action down permanently | Every hold needs a release path that always fires |
| `Sink` on left-click swallowed it globally with no gate | Do not take a global input without a way to give it back |
| A client clock was used where a sequence number was required | Read the validation list before writing the request |
