# Roblox Studio and IDE Workflow

## Decision

Build the experience in **Roblox Studio**, while editing synchronized Luau and project documents in an external IDE.

The external IDE does not replace Studio. Roblox Studio is still required to create the place, arrange Instances, animate, test Roblox engine behavior, emulate devices, run clients and servers, upload assets, and publish.

## Required tools

Versions are pinned in `rokit.toml`. Run `rokit install` from the repository root; see [TOOLING_AND_PIPELINE.md](TOOLING_AND_PIPELINE.md) for what each one is for.

- Latest Roblox Studio, plus the **Rojo Studio plugin**.
- VS Code, Cursor, or another editor that can open a folder.
- The `luau-lsp` extension, plus its Studio companion plugin — without the plugin, Studio-owned instances are untyped.
- Git.
- [Rokit](https://github.com/rojo-rbx/rokit), which installs Rojo, Wally, StyLua, Selene, and luau-lsp at pinned versions.
- Optional: Roblox Studio MCP for a trusted compatible AI client.

Copy `.vscode/settings.json.example` to `.vscode/settings.json`. The real file is gitignored, so the example is the committed record; previously the only editor configuration in existence sat in an untracked file **outside** the repository root and was unreproducible.

D-018 supersedes the earlier instruction not to add Rojo or Wally. Frameworks and build automation beyond the static gates are still out of scope without a concrete need.

## One-time Studio setup

1. Open Roblox Studio.
1. Create a private Baseplate experience named `Theory of Everything: Unleashed — Prototype`.
1. Publish it privately once so the prototype has a recoverable cloud place.
1. In Explorer, create these script-only folders:

```text
ReplicatedStorage
  GameShared

ServerScriptService
  GameServer

StarterPlayer
  StarterPlayerScripts
    GameClient
```

1. Do not place parts, models, remotes with attributes, UI Instances, sounds, or other non-script assets inside the three synced folders.
1. Save or publish the private place.

## Configure Rojo

`default.project.json` already declares the mapping, so there is nothing to configure per folder:

| Studio location | Local folder |
|---|---|
| `ReplicatedStorage/GameShared` | `src/shared` |
| `ServerScriptService/GameServer` | `src/server` |
| `StarterPlayer/StarterPlayerScripts/GameClient` | `src/client` |

Note that the `GameShared`, `GameServer`, and `GameClient` names come from the mapping, not from folders on disk. Files live directly at `src/client/...`.

Steps:

1. **Publish the private place first.** The arena exists only in Studio and `*.rbxl` is gitignored, so the cloud version is the sole backup.
2. Open the repository root, not only `src`, in the IDE. This makes the Markdown context visible to LLM tools.
3. Run `rojo serve` from the repository root.
4. In Studio, open the Rojo plugin and connect.
5. Confirm the three folders appear where Script Sync previously put them, with **no** double nesting such as `GameClient/GameClient`, and with no Studio-side instances lost.
6. Edit a comment in one file and confirm it reaches Studio.

**`rojo build` is not a deployment path.** The project file declares only the three code folders, so its output contains none of the arena. It exists to prove the project file resolves and every file parses. Never publish it over the real place.

### Script Sync as fallback

Script Sync still works and the folder mapping is identical, via right-click → **Sync to…** on each folder. It does not preserve script attributes or tags. Use it if the Rojo plugin is unavailable; do not run both at once.

## Source-of-truth policy

| Content | Primary home |
|---|---|
| Synced Luau source | Local `src` files |
| Markdown plans and LLM context | This repository |
| Parts, terrain, models, rigs, animation objects, VFX Instances, UI layout, audio, lighting | Roblox Studio place |
| Product decisions | `docs/DECISION_LOG.md` |
| Current work | `TASKS.md` |

Avoid editing the same synced script in Studio and the IDE at the same time.

If Studio shows a sync conflict:

1. Stop.
2. Inspect the listed additions, modifications, and deletions.
3. Preserve the side containing the intentional latest change.
4. Confirm no script attributes, tags, or unrelated Instances will be lost.
5. Commit the resolved local files before continuing.

Never choose “Keep Disk” or “Keep Studio” reflexively for a large conflict.

## Daily development loop

1. Run `git status`. **Untracked work is not saved work** — this project nearly lost its only implementation that way.
2. Open the private prototype in Studio and start `rojo serve`.
3. Confirm the Rojo plugin is connected.
4. Read `TASKS.md` and choose one acceptance condition.
5. Edit Luau in the IDE.
6. Run the static gates: `stylua --check src`, `selene src`, `luau-lsp analyze`.
7. Observe Output and Script Analysis in Studio.
8. Run the smallest relevant test.
9. Run server and two clients for any networked combat change.
10. Run device emulation for any input or HUD change.
11. Update the task and affected document — the task only if acceptance passed.
12. Commit a focused working change.
13. Publish the private prototype at a stable checkpoint, with a version note.
14. Write a [session handoff](templates/SESSION_HANDOFF.md).

## Testing modes

### Solo play

Use for:

- Camera and local input.
- Graybox traversal.
- UI layout.
- Dummy interactions.
- Fast iteration on presentation.

Solo play is not proof that remotes, ownership, KOs, assists, or combat replication work.

### Server and clients

Use at least two clients for:

- Player-versus-player hit validation.
- Blocking direction.
- Knockback and ragdoll.
- Death and respawn.
- Duplicate-request and cooldown tests.
- KO and assist attribution.

Use up to eight local clients for the prototype load/readability test.

### Device emulation

Use for:

- Touch-button reach and overlap.
- Camera and aim behavior.
- Text size and cooldown readability.
- Lower-end device simulation and performance.

## Studio MCP

Roblox Studio can act as an MCP server, letting a compatible AI client inspect the open data model, read Output, run Luau, and start tests. Connected and configured on 2026-07-25 (D-024).

### How the pieces fit

Studio does **not** connect out to anything. Enabling **Assistant Settings → MCP Servers → Enable Studio as MCP server** only starts the listener inside Studio — the panel will keep saying **"No clients connected"** until a client launches the `StudioMCP.exe` proxy, which then connects back to Studio. The client spawns the proxy, not Studio.

For Claude Desktop, Cursor, and Codex, Studio can write that client's config itself via its toggles. **Claude Code CLI is different** — its row shows a command you must run yourself. Turning on the other toggles does nothing for Claude Code.

### Registration

Committed at the repository root in `.mcp.json`, so the setup is reproducible:

```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "type": "stdio",
      "command": "cmd.exe",
      "args": ["/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"],
      "env": {}
    }
  }
}
```

`%LOCALAPPDATA%` is expanded by `cmd.exe`, which keeps the file portable across machines and user names.

Two things to expect:

1. **MCP servers load when a session starts.** Registering the server does nothing for a session already running. Start a new Claude Code session.
2. **A project-scoped server needs explicit approval on first use.** `claude mcp get Roblox_Studio` will report `Pending approval` until you accept the prompt. That gate exists because `.mcp.json` is checked into git and could otherwise let a repository launch a process on your machine.

Do not use `claude mcp add` from Git Bash. MSYS path translation rewrites the `/c` flag to `C:/`, which produces a registration that silently cannot start. Edit `.mcp.json` directly, or run the command from PowerShell.

### Known bug in Roblox's launcher

`%LOCALAPPDATA%\Roblox\mcp.bat` has a batch-syntax error. Its `else` sits on its own line, which is invalid — `else` must follow the closing parenthesis on the same line. Running it produces:

```text
'else' is not recognized as an internal or external command,
'"%B/..\StudioMCP.exe"' is not recognized as an internal or external command,
```

Consequence: the `if exist` branch works, so the proxy launches correctly while the version path the file names still exists. The registry-lookup **fallback is dead**. Studio normally rewrites `mcp.bat` when it updates, so this should self-heal — but if MCP stops working right after a Studio update, this is the first thing to check. Re-copy the command from Studio's Quick connect panel and reconcile `.mcp.json` with it.

### Use it only when

- The client is trusted.
- The active Studio instance is the intended private prototype.
- **The place has been published**, not merely saved. `*.rbxl` is gitignored, so the cloud version is the only backup of the arena that exists, and MCP can modify and delete instances.
- The requested AI action is narrow and reviewable.

### Scripts are read-only over MCP

Rojo syncs disk to Studio. MCP can edit scripts inside Studio. Those are two writers to the same scripts, and **Rojo wins silently** — an MCP script edit is overwritten on the next sync with no conflict prompt and no error.

| MCP may | MCP may not |
|---|---|
| Read the data model, instance names, classes, properties | Create or edit `.luau` scripts |
| Read Output and Script Analysis | |
| Create and edit non-script instances: GUI, parts, attributes | |
| Run Luau for inspection, and start tests | |

Luau authoring stays on disk, under git, synced by Rojo. Recorded as D-024.

### What MCP does and does not remove

It removes the need to *guess* what is in the place — which is worth a lot here, since this project already shipped a bug caused by asserting ten GUI instance names that were written down nowhere (see [HUD_AND_UI_SPEC.md](HUD_AND_UI_SPEC.md)).

It does **not** remove any test. Feel, thumb reach, readability, and whether combat is fun are not inspectable. The two-client test and the mobile device test are unchanged.

If MCP is not connected, an agent sees only local files. Give it the relevant Explorer tree, property values, and Output errors rather than letting it invent Studio instances.

## Why Rojo, and what did not change

D-018 adopted Rojo on 2026-07-25, superseding D-010. Two of the five re-evaluation triggers this document already listed had been met: **CI needs reproducible place generation**, and every combat library the project will want — ShapecastHitbox, Trove, Blink — ships on Wally, which requires a project file.

What deliberately did **not** change: the project file declares only the three code folders, so Studio keeps ownership of the place, arena, GUI, rigs, animation, VFX instances, and audio. The source-of-truth table above is unchanged. This was a change of sync mechanism, not of the data-model philosophy.

The remaining triggers from the original list are still worth watching, since they would push toward representing more of the data model as files:

- More than one developer needs reviewable full data-model changes.
- Most Instances should be represented as files.

That would be a further decision, not an extension of D-018.

## Git

Never commit credentials, cookies, local Studio settings, or secret keys. Commit rules are in [DEVELOPER_RULES.md](DEVELOPER_RULES.md).

Use small commits such as:

- `docs: establish prototype scope`
- `feat: add combat state machine`
- `feat: validate basic attack requests`
- `fix: clear ragdoll force on respawn`

If the change is Studio-side, say so in the commit body — the diff will not show it. Four commits in this project's history are labelled `feat:` and contain no code for exactly that reason.

## Official references

- [Rojo](https://rojo.space/docs/v7/) and [Rokit](https://github.com/rojo-rbx/rokit)
- [Script Sync](https://create.roblox.com/docs/scripting/sync), the fallback path
- [Studio MCP server](https://create.roblox.com/docs/studio/mcp)
- [Studio testing modes](https://create.roblox.com/docs/studio/testing-modes)
- [Luau type checking](https://create.roblox.com/docs/luau/type-checking)
- [Third-party tools and Rojo overview](https://create.roblox.com/docs/projects/external-tools)
