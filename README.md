# Theory of Everything: Unleashed

Design and development context for a Roblox public free-for-all battleground in which science-themed fighters turn discoveries into superpowers.

**Project status:** pre-production / combat prototype  
**Document version:** 0.1  
**Last updated:** 2026-07-23

## Where the game should be made

Use **Roblox Studio and an external IDE together**.

| Tool | Use it for |
|---|---|
| Roblox Studio | The place, arena, parts, models, rigs, animation, VFX, UI layout, audio, device emulation, multiplayer tests, publishing |
| VS Code, Cursor, or another IDE | Luau source files, Markdown plans, Git history, code review, and LLM-assisted coding |
| Script Sync | Keeps selected Studio script folders and local Luau folders synchronized |
| Studio MCP, optional | Lets a trusted compatible AI client inspect and operate the open Studio place |

For the first prototype, use Roblox's built-in **Script Sync**, not Rojo. Script Sync is the lower-setup choice when Studio remains the home of the place and non-code assets. Reconsider Rojo only if the whole data model later needs to be file-system-first.

## Current product

> An eight-player continuous public arena where historical geniuses and original science archetypes fight, fill a Discovery Meter, activate a Breakthrough, earn KOs and assists, and quickly respawn.

The first proof is much smaller:

> Gravity Sovereign versus a training dummy and test players in one graybox arena, with movement, a four-hit basic combo, block, dash, damage states, one gravity ability, KO, and respawn.

## Start here

1. Read [AGENTS.md](AGENTS.md).
2. Read [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) and [docs/MVP_SCOPE.md](docs/MVP_SCOPE.md).
3. Follow [docs/STUDIO_IDE_WORKFLOW.md](docs/STUDIO_IDE_WORKFLOW.md).
4. Work from [TASKS.md](TASKS.md).
5. Before implementing combat, read [docs/COMBAT_SYSTEM.md](docs/COMBAT_SYSTEM.md) and [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md).

The complete document map is in [docs/INDEX.md](docs/INDEX.md).

## Source-of-truth rule

- Product decisions: [docs/DECISION_LOG.md](docs/DECISION_LOG.md)
- Current work: [TASKS.md](TASKS.md)
- Code and networking rules: [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md)
- Unresolved choices: [docs/OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md)

If documents disagree, do not guess. Use the source above or record a decision before implementation.

## Official workflow references

- [Roblox Script Sync](https://create.roblox.com/docs/scripting/sync)
- [Roblox Studio MCP server](https://create.roblox.com/docs/studio/mcp)
- [Studio testing modes](https://create.roblox.com/docs/studio/testing-modes)
- [Luau type checking](https://create.roblox.com/docs/luau/type-checking)
- [Third-party file-based tools](https://create.roblox.com/docs/projects/external-tools)
