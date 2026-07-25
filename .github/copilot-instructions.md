# Copilot Instructions

Use `AGENTS.md` as the canonical project instructions and `TASKS.md` as the active scope.

This is a Roblox Luau public-FFA combat prototype. Generate small, `--!strict`, server-authoritative modules. A client may request an action and play predicted presentation, but it may not choose victims or award damage, KOs, assists, meter, cooldown completion, currency, or respawns.

Tunable numbers go in `src/shared/Config/`, never inline. Shared types go in `src/shared/Types/`, never in a client or server module — the project has already produced two incompatible shapes for one wire concept that way. Keep shared modules pure so they can be unit tested without the engine.

Before suggesting a new system, check `docs/MVP_SCOPE.md`. Do not add ranked 1v1, story, trading, gacha, a battle pass, a large city, or additional fighters during the combat-foundation milestone. Do not add a framework or a Wally package without a concrete need; the toolchain in `rokit.toml` is settled.

Treat values marked DEFAULT as tunable, DRAFT as unapproved, OPEN as unresolved, LOCKED as product direction, and OUT as outside current scope. Never resolve an OPEN item by writing code that assumes an answer.

Code must pass `stylua --check src`, `selene src`, and `luau-lsp analyze`. Never claim a Studio, device, or multiplayer test that was not run.

Longer form: `docs/DEVELOPER_RULES.md` for engineering, `docs/DESIGN_PHILOSOPHY.md` for design, `docs/HUD_AND_UI_SPEC.md` for input and HUD.
