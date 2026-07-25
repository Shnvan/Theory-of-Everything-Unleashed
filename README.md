# Theory of Everything: Unleashed

Design and development context for a Roblox public free-for-all battleground in which science-themed fighters turn discoveries into superpowers.

**Project status:** pre-production / combat prototype  
**Document version:** 0.2  
**Last updated:** 2026-07-25

## Where the game should be made

Use **Roblox Studio and an external IDE together**.

| Tool | Use it for |
|---|---|
| Roblox Studio | The place, arena, parts, models, rigs, animation, VFX, UI layout, audio, device emulation, multiplayer tests, publishing |
| VS Code, Cursor, or another IDE | Luau source files, Markdown plans, Git history, code review, and LLM-assisted coding |
| Rojo | Syncs the three Studio script folders with `src/shared`, `src/server`, and `src/client` |
| StyLua, Selene, luau-lsp | Format, lint, and type check — enforced in CI |
| Studio MCP, optional | Lets a trusted compatible AI client inspect and operate the open Studio place |

Run `rokit install` from the repository root to get every tool at its pinned version, then copy `.vscode/settings.json.example` to `.vscode/settings.json`.

Rojo syncs **code only**. Studio remains the home of the place, arena, GUI, rigs, animation, VFX instances, and audio. `rojo build` output is a syntax check, not the game — never publish it over the real place. Full rationale in [docs/TOOLING_AND_PIPELINE.md](docs/TOOLING_AND_PIPELINE.md); this supersedes the earlier Script-Sync-only guidance (D-018).

## Current product

> An eight-player continuous public arena where historical geniuses and original science archetypes fight, fill a Discovery Meter, activate a Breakthrough, earn KOs and assists, and quickly respawn.

The first proof is much smaller:

> Gravity Sovereign versus a training dummy and test players in The Omniscience Coliseum, with movement, a four-hit basic combo, block, dash, damage states, one gravity ability, KO, and respawn.

The arena is built and validated. Combat is not. See [docs/PROJECT_AUDIT_2026-07-25.md](docs/PROJECT_AUDIT_2026-07-25.md) for where the project actually stands.

## Start here

1. Read [AGENTS.md](AGENTS.md).
2. Read [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) and [docs/MVP_SCOPE.md](docs/MVP_SCOPE.md).
3. Follow [docs/STUDIO_IDE_WORKFLOW.md](docs/STUDIO_IDE_WORKFLOW.md).
4. Work from [TASKS.md](TASKS.md).
5. Before writing code, read [docs/DEVELOPER_RULES.md](docs/DEVELOPER_RULES.md) and [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md).
6. Before designing anything, read [docs/DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md) and [docs/COMBAT_SYSTEM.md](docs/COMBAT_SYSTEM.md).

The complete document map is in [docs/INDEX.md](docs/INDEX.md).

## Source-of-truth rule

- Product decisions: [docs/DECISION_LOG.md](docs/DECISION_LOG.md)
- Current work: [TASKS.md](TASKS.md)
- Code and networking rules: [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md), with habits in [docs/DEVELOPER_RULES.md](docs/DEVELOPER_RULES.md)
- Design consistency: [docs/DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md)
- Unresolved choices: [docs/OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md)
- Tunable numbers: `src/shared/Config/CombatConfig.luau`
- Studio instances code depends on by name: [docs/HUD_AND_UI_SPEC.md](docs/HUD_AND_UI_SPEC.md)

If documents disagree, do not guess. Use the source above or record a decision before implementation.

## Official workflow references

- [Rojo](https://rojo.space/docs/v7/)
- [Roblox Script Sync](https://create.roblox.com/docs/scripting/sync), the fallback sync path
- [Roblox Studio MCP server](https://create.roblox.com/docs/studio/mcp)
- [Studio testing modes](https://create.roblox.com/docs/studio/testing-modes)
- [Luau type checking](https://create.roblox.com/docs/luau/type-checking)
- [Third-party file-based tools](https://create.roblox.com/docs/projects/external-tools)
