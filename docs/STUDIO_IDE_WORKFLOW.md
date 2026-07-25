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

## Optional Studio MCP

Roblox Studio includes an MCP server that compatible AI clients can connect to. It can inspect the open data model, read or edit scripts, run Luau, and start tests.

Use it only when:

- The client is trusted.
- The active Studio instance is the intended private prototype.
- Git or a stable Studio checkpoint exists.
- The requested AI action is narrow and reviewable.

In Studio, open **Assistant Settings → MCP Servers → Quick connect**, then enable the installed supported client. If no MCP connection is present, an LLM sees only local files; give it the relevant Explorer tree and Output errors rather than letting it invent Studio Instances.

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
