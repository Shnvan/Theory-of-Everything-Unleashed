# Roblox Studio and IDE Workflow

## Decision

Build the experience in **Roblox Studio**, while editing synchronized Luau and project documents in an external IDE.

The external IDE does not replace Studio. Roblox Studio is still required to create the place, arrange Instances, animate, test Roblox engine behavior, emulate devices, run clients and servers, upload assets, and publish.

## Recommended initial tools

- Latest Roblox Studio.
- VS Code, Cursor, or another editor that can open a folder.
- Luau language-server extension.
- Git.
- Roblox Script Sync.
- Optional: Roblox Studio MCP for a trusted compatible AI client.

Do not add Rojo, Wally, a large framework, or build automation during M0 unless a specific blocker requires it.

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

## Configure Script Sync

For each code folder:

1. Right-click the folder in Studio.
1. Select **Sync to…**.
1. Map it to:

| Studio folder | Local folder |
|---|---|
| `ReplicatedStorage/GameShared` | `src/shared` |
| `ServerScriptService/GameServer` | `src/server` |
| `StarterPlayer/StarterPlayerScripts/GameClient` | `src/client` |

1. Open the repository root, not only `src`, in the IDE. This makes the Markdown context visible to LLM tools.
1. Create a small test ModuleScript in one synced folder and verify a harmless edit moves both directions.
1. Remove the test script after the sync check.

Script Sync supports scripts, ModuleScripts, LocalScripts, and folders. It does not preserve script attributes or tags. Keep those out of synced scripts during this workflow.

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

1. Pull or inspect the current Git state.
2. Open the private prototype in Studio.
3. Confirm Script Sync is active.
4. Read `TASKS.md` and choose one acceptance condition.
5. Edit Luau in the IDE.
6. Observe Output and Script Analysis in Studio.
7. Run the smallest relevant test.
8. Run server and two clients for any networked combat change.
9. Run device emulation for any input or HUD change.
10. Update the task and affected document.
11. Commit a focused working change.
12. Publish the private prototype at a stable checkpoint.

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

## When to consider Rojo

Re-evaluate a file-system-first workflow only if at least one becomes true:

- More than one developer needs reviewable full data-model changes.
- The team wants most Instances represented as files.
- Automated place builds are required.
- Script Sync limitations repeatedly block necessary organization.
- CI needs reproducible place generation.

Do not migrate merely because Rojo is common. A migration changes the source-of-truth model and deserves its own decision.

## Git baseline

After Script Sync creates `src`, make a first baseline commit containing:

- This documentation pack.
- The three synced source trees.
- No credentials, cookies, local Studio settings, or secret keys.

Use small commits such as:

- `docs: establish prototype scope`
- `feat: add combat state machine`
- `feat: validate basic attack requests`
- `fix: clear ragdoll force on respawn`

## Official references

- [Script Sync](https://create.roblox.com/docs/scripting/sync)
- [Studio MCP server](https://create.roblox.com/docs/studio/mcp)
- [Studio testing modes](https://create.roblox.com/docs/studio/testing-modes)
- [Luau type checking](https://create.roblox.com/docs/luau/type-checking)
- [Third-party tools and Rojo overview](https://create.roblox.com/docs/projects/external-tools)
