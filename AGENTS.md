# Instructions for AI Coding Agents

This file is the canonical operating context for any LLM or coding agent working on **Theory of Everything: Unleashed**.

## Required reading

Before changing code or design:

1. Read `README.md`.
2. Read `docs/PROJECT_BRIEF.md`.
3. Read `docs/MVP_SCOPE.md`.
4. Read `docs/DECISION_LOG.md`.
5. Read the task-specific document linked from `docs/INDEX.md`.
6. Read `TASKS.md` and work only on the active milestone unless the user changes scope.

For milestone planning, new systems, production decisions, or large cross-discipline features, also read `docs/ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md`. Tiny isolated fixes do not require it.

Then, by kind of work:

- Writing code: `docs/DEVELOPER_RULES.md`.
- Designing a move, ability, or character: `docs/DESIGN_PHILOSOPHY.md`, and fill in `docs/templates/MOVE_SPEC.md` first.
- Touching input or HUD: `docs/HUD_AND_UI_SPEC.md`.
- Choosing a tool, library, or pipeline: `docs/TOOLING_AND_PIPELINE.md`.
- Working with an AI agent: `docs/AI_ASSISTED_WORKFLOW.md`.
- Understanding current project state and known problems: `docs/PROJECT_AUDIT_2026-07-25.md`.

## Current milestone

Build the universal combat foundation and a small **Gravity Sovereign** vertical slice. The game is not yet at public-alpha content production.

## Locked product constraints

- Platform: Roblox.
- Primary mode: continuous public free-for-all battleground.
- Target server size: eight players.
- Prototype character: Gravity Sovereign, inspired by Isaac Newton.
- Prototype environment: The Omniscience Coliseum, one contained arena with an approximately 759-stud combat disc, eight thematic sectors, 24 static exhibits, and physical plus fail-safe perimeter containment. It is a detailed static prototype, not final production art.
- Controls: four-hit basic combo, block, dash/limited escape, four future ability slots, character mechanic, and Breakthrough meter.
- Final Proof is a short stylized KO effect, not a long execution cinematic.
- Combat uses no blood, dismemberment, torture, or realistic death.
- PvP ranking, private 1v1 rounds, story mode, trading, gacha, battle passes, and large destructible cities are outside the prototype.
- The project must remain understandable and usable on mobile as well as keyboard/mouse.

Do not reopen a locked decision merely because another popular battleground uses a different design. If a change is necessary, explain the evidence, update `docs/DECISION_LOG.md`, and obtain user approval.

## Engineering rules

- Use Luau and place `--!strict` at the top of new gameplay modules unless a documented engine limitation prevents it.
- Treat the server as authoritative for damage, cooldowns, hit eligibility, KOs, meter gain, and respawning.
- Clients may request an action and predict presentation. They may never declare damage, a KO, currency, or meter gain.
- Validate remote requests for action type, character state, cooldown, rate, range, and plausible target.
- Keep tunable values in shared configuration modules instead of scattering numbers through scripts. They live in `src/shared/Config/`.
- Keep shared modules pure — no services, no instances, no side effects — so they can be unit tested without the engine.
- Prefer small ModuleScripts with explicit responsibilities. The toolchain in `rokit.toml` is settled (D-018); do not add a framework, or a Wally package, without a concrete need.
- Run the static gates before calling a change complete: `stylua --check src`, `selene src`, `luau-lsp analyze`, `rojo build`.
- Avoid `_G`, shared mutable globals, unbounded loops, and one RemoteEvent per move.
- Separate simulation/gameplay state from VFX, sound, camera shake, and UI.
- Never let a cosmetic failure block combat simulation.
- Add cleanup for connections, tasks, temporary instances, hitboxes, and character lifecycle state.
- Comment intent and non-obvious constraints; do not narrate obvious syntax.

## Scope discipline

Before implementing a requested feature, ask:

1. Does it help prove that moving, attacking, defending, and getting hit feel good?
2. Is it required for a two-client network test?
3. Is it in the current milestone in `TASKS.md`?

If all answers are no, record it as a future task instead of building it.

Do not create the other eleven fighters until the Gravity Sovereign foundation passes the prototype gate. Do not implement saving, shops, mastery, full map destruction, matchmaking, or public release systems during the combat-foundation milestone.

## Change completion

For every code change:

- State the behavior being changed.
- Keep the patch focused.
- Test in the smallest relevant Studio mode.
- For combat or remotes, run at least a server-and-two-clients test before calling it complete.
- Test a mobile viewport when input or HUD changes.
- Report files changed, tests run, remaining risks, and the next task.
- Update `TASKS.md` and any affected design document when behavior or a decision changes.

## Decision labels

Documents use these labels:

- **LOCKED:** approved project direction; requires an explicit decision to change.
- **DEFAULT:** starting value for a prototype; expected to change through testing.
- **DRAFT:** design candidate; do not implement the entire item without approval.
- **OPEN:** unresolved decision.
- **OUT:** outside current scope.

Never convert a DRAFT or OPEN item into a LOCKED requirement silently. This project has already broken that rule once, in code — see D-021 — so treat it as a live risk rather than a formality. If implementation forces a choice a document leaves OPEN, stop and record the decision.

## Source-of-truth priority

1. The user's latest explicit instruction.
2. `docs/DECISION_LOG.md`.
3. The domain document for the system.
4. `TASKS.md`.
5. Older notes and LLM output.

When the first four disagree, stop and surface the conflict.

Two sources of truth live outside Markdown and rank with the domain document for their subject: `src/shared/Config/` for tunable numbers, and the Studio place for the arena, GUI, rigs, and audio. A number in a document that disagrees with `CombatConfig` means one of them needs fixing — say which.
