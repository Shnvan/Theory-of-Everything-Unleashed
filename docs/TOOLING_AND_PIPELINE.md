# Tooling and Pipeline

**Status:** the code toolchain is LOCKED and installed (D-018). The animation, VFX, and audio pipelines are RESEARCH — recommendations with no adoption decision and no spend approved.

**Research date:** 2026-07-25. Roblox ships fast; recheck anything platform-related before building on it.

**Cost rule:** every non-zero cost needs separate advance approval per [ASSET_PROVENANCE_LEDGER.md](ASSET_PROVENANCE_LEDGER.md). Nothing in this document is authorization to buy anything.

---

## Read this first: the platform moved

Every document in this repository is dated 2026-07-23. Between then and now, four first-party systems reached beta or full release, and they target precisely the problems a fighting game has. Much of the 2024–2025 DevForum advice you will find is now partly obsolete.

| System | Status | Why it matters here |
|---|---|---|
| [Server Authority](https://create.roblox.com/docs/projects/server-authority) | Client Beta, Apr 2026 | Engine-level client prediction and rollback resimulation. This is the thing fighting games need most, and it removes the main reason people adopted Chickynoid. |
| [Input Action System](https://create.roblox.com/docs/input/input-action-system) | Full release | Cross-platform rebindable input; also the input layer Server Authority expects. Replaces hand-wiring `ContextActionService` plus touch buttons. |
| [Animation Graphs](https://devforum.roblox.com/t/full-release-animation-graphs-create-complex-character-motion-visually/4739840) | Full release, Jul 15 2026 | Node-based blend trees with parameters that replicate automatically. |
| [Adaptive Animation](https://devforum.roblox.com/t/full-release-adaptive-animation-use-one-animation-across-any-rig/4605672) | Full release, Apr 2026 | One animation set across R6, R15, and custom rigs. Directly relevant to a 12-fighter roadmap. |

### How this project is responding

| System | Decision | Trigger |
|---|---|---|
| Server Authority | Do **not** adopt yet. Build M1/M2 on classic remote validation, keep combat simulation in modules that could move under `BindToSimulation` later. Timeboxed spike at M2 with a recorded go/no-go. | D-020 |
| Input Action System | Stay on `ContextActionService` through M1. Migrate before ability targeting or at the Server Authority spike, whichever comes first. | D-019 |
| Animation Graphs | Use for locomotion and stance blending **only**. Not for the move list — see the caveats below. | Not yet decided |
| Adaptive Animation | Adopt when the second fighter begins. No value with one fighter. | Not yet decided |

### Caveats worth knowing before you architect around any of it

- Server Authority is **beta**, and its documented gaps hit this game: a **maximum of 8 active animation tracks per `Animator`** (budget for it if you planned layered additive hit reactions), position quantization causing drift during strafing, and unavailable custom emotes. Verify each yourself before committing.
- Animation Graphs are **movement-first, not combat-first**. There are no cancellation windows, no hit-reaction interrupt priority, and **no animation-marker-to-graph hookup**. Your combo and cancel state machine still has to be Luau.
- There are **no IK nodes** in Animation Graphs. Drive `IKControl` from script alongside the graph.
- The Apr 2026 Server Authority beta thread says Animation Graphs are "not yet supported" under Server Authority, while the Jul 2026 Animation Graphs release says parameters replicate in both modes. **These two statements conflict and this is the single biggest uncertainty in this research.** Check current docs before relying on the combination.

---

## Code toolchain — LOCKED and installed

Pinned in `rokit.toml`. One `rokit install` reproduces it. All five were installed and run against this repository on 2026-07-25; results are in the D-018 commit.

| Tool | Version | For | Verified |
|---|---|---|---|
| [Rojo](https://rojo.space/docs/v7/) | 7.7.0 | Studio sync and place generation from `default.project.json` | Builds the documented tree |
| [Wally](https://wally.run/) | 0.3.2 | Packages. Capability only; nothing installed yet | `wally install` succeeds |
| [StyLua](https://github.com/JohnnyMorganz/StyLua) | 2.5.2 | Formatting | `--check` clean |
| [Selene](https://kampfkarren.github.io/selene/) | 0.31.0 | Linting | 0 errors, 0 warnings |
| [luau-lsp](https://github.com/JohnnyMorganz/luau-lsp) | 1.69.0 | Type checking, headless and in the editor | 0 diagnostics |
| Rokit | 1.2.0 | Pins the above | Resolves all five |

**They paid for themselves on first run.** Selene caught a deprecated `Enum.KeyCode.Unknown`, and luau-lsp caught a genuine element-type narrowing bug in a config table. Neither would have surfaced in a Studio playtest until it misbehaved.

Not adopted, and why: **roblox-ts** (you would debug compiled Luau in the Studio debugger, which is the wrong trade for frame-by-frame combat work), **Matter/ECS** (a large paradigm commitment before the loop is proven), **Flamework** (roblox-ts only), **Argon** (Rojo is sufficient while Studio owns non-code assets), **pesde** (Wally is still where the combat libraries publish).

---

## Animation pipeline — RESEARCH

The most important unpriced dependency in the project. Nothing here is adopted.

| Tool | For | Cost | Note |
|---|---|---|---|
| [Moon Animator 2](https://create.roblox.com/store/asset/4725618216/Moon-Animator-2) | Primary hand-keyed combat animation | **Paid, reported ~1,700 Robux — UNVERIFIED, confirm on the Creator Store** | Still the de-facto standard for this genre. IK/FK toggle, multi-rig in one scene (needed for grabs and throws), camera tracks, sub-frame timeline. |
| [Blender + Cautioned's Roblox Animations Importer/Exporter](https://github.com/Cautioned/Blender-Animations-Plugin) | Complex animation, cinematics, VFX meshes; free fallback | Free, GPL-3.0 | The current maintained bridge. Live sync between a Blender add-on and a Studio plugin. Blender 4.2+. |
| Animation Clip Editor + Curve Editor | Cleanup, curve polish, glTF/FBX import | Free, built in | The importer gained glTF support and multiple clips per file in Mar 2026. Still **no IK**, which is why Moon Animator persists. |
| [Rig Edit Lite](https://devforum.roblox.com/t/rigedit-create-and-edit-animation-rigs/70840) | Motor6D joint placement | Free | Visual handles instead of hand-computing `C0`/`C1`. |
| [`IKControl`](https://create.roblox.com/docs/reference/engine/classes/IKControl) | Hit reactions, foot planting, look-at | Free, built in | How a punch lands *on* the opponent instead of near them. Blend `Weight` in and out to avoid pops. |
| [Animation markers](https://create.roblox.com/docs/animation/events) | **Frame data** | Free, built in | See below. This is the most important item in the table. |

### Animation markers are the frame-data source of truth

Place named markers in the animation — `HitStart`, `HitEnd`, `CancelOpen` — and subscribe with `GetMarkerReachedSignal`. Prefer it over `KeyframeReached`, which fires for every keyframe.

This is what makes hitboxes match what the player sees, and it is the mechanism the whole recommended combat pipeline hangs off. **But** the timing values themselves still belong in shared config: an animation may express them, and must not be the only place they exist. Per [DEVELOPER_RULES.md](DEVELOPER_RULES.md), never derive a gameplay duration from an animation length.

### Licensing warning

Multiple Creator Store listings called "Free Moon Animator 2", and several GitHub mirrors, are reuploads or cracks. Using them on a commercial project is both a licensing and a supply-chain risk. Budget for the real one or use the free Blender path.

---

## Combat systems — RESEARCH

| Library | For | Cost | Note |
|---|---|---|---|
| [ShapecastHitbox](https://github.com/TeamSwordphin/ShapecastHitbox) | Melee hitboxes | Free, Wally | **Use this, not RaycastHitbox.** Blockcast/Spherecast/Raycast, mesh-deformation and bone detection, better performance with many simultaneous hitboxes. |
| [Rewind](https://devforum.roblox.com/t/rewind-server-authoritative-lag-compensated-hit-validation/4160622) | Lag-compensated server-side hit validation | Free | The one lag-comp library with a **melee Cone mode**. Snapshot ring buffer, Hermite interpolation to the client's claimed time, rate limiting, duplicate detection. |
| [Trove](https://github.com/Sleitnick/RbxUtil) | Lifetime cleanup | Free, Wally | Effectively mandatory. This game creates and destroys hitboxes, forces, and VFX constantly, and cleanup is a stated project rule. |
| [Blink](https://github.com/1Axen/blink) | Buffer network serialization | Free | Faster and lower-bandwidth than Zap or ByteNet in Apr 2025 benchmarks. **Only if the plain-remote surface proves too costly** — do not pre-optimize. |
| [Chickynoid](https://github.com/easy-games/chickynoid) | Custom server-authoritative character controller | Free | **Read it, do not adopt it.** Official Server Authority covers the same ground with engine support. Its own authors warn it needs "serious engineering." Keep as a fallback if the M2 spike fails. |

Community consensus on where hitboxes run: **client-side, marker-gated, then validated server-side.** Server-side hitboxes lag behind the animation and produce ghost misses. This does not weaken D-011 — the client detects a *candidate*, the server decides the *result*.

---

## VFX and audio — RESEARCH

| Tool | For | Cost |
|---|---|---|
| Flipbook particles (`ParticleEmitter` + `FlipbookLayout`) | Impacts, explosions, hit sparks | Free, built in. 2×2 / 4×4 / 8×8 grids; leave spacing between frames or you get bleed |
| [Beziers](https://devforum.roblox.com/t/beziers-advanced-modular-vfx-plugin-10000-assets-add-ons/4180222) | Modular VFX authoring, large asset library | Paid. Add-ons include ImpactFrames and CameraShake, which are exactly this genre's needs |
| Blender | VFX meshes: slash arcs, shockwave rings, mesh trails | Free; same install as the animation bridge |
| [EmberGen](https://jangafx.com/software/embergen) | Generating flipbook sheets from volumetric sim | Paid. The pro path for smoke and fire; overkill at prototype stage |

Audio has **no** tooling recommendation yet and no rights review. Every sound needs a provenance row before it ships. The design constraint is in [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md): critical cues must be identifiable with the music muted.

---

## Do not use — dated advice you will still find recommended

| Avoid | Use instead | Why |
|---|---|---|
| RaycastHitbox 4.01 | ShapecastHitbox | Explicitly unsupported; known bugs and performance issues the original team is not addressing |
| ProfileService | ProfileStore | Stable but no longer supported |
| Knit | Plain services and modules | Reported archived |
| Aftman / Foreman | Rokit | Superseded |
| The 2016-era "Blender rig exporter" thread | Cautioned's add-on | Long superseded |
| SecureCast | Rewind or RollbackHitbox | Archived |
| Hoarcekat | UI Labs | Older generation; UI Labs hot-reloads without running the game |

---

## How the top games actually do it

**Label this inference, not fact.** None of The Strongest Battlegrounds, Untitled Boxing Game, Jujutsu Shenanigans, or Deepwoken publishes a technical devlog. What follows is community reverse-engineering plus a few verified facts.

**The cinematic-move technique**, which DevForum practitioners converge on and which is not what most people guess:

1. Animate the move **with** world displacement, so it reads well while authoring.
2. Strip the displacement so the animation plays **in place**.
3. Drive world-space movement from script, triggered by animation markers, using physics (`BodyVelocity`-style) rather than tweens — tweens look choppy and fight replication.
4. Play the animation on server and client to hide latency.

Do **not** try to read Moon Animator CFrame tracks at runtime.

**Grabs and throws:** Motor6D-weld the victim into the attacker's rig, or use a middle-man assembly part between them. Common gotcha — the second character will not animate unless you handle or remove its `Humanoid`. Animate both rigs in one Moon Animator scene.

**Verified facts worth weighing:**

- TSB's animations are done in Moon Animator; the team publishes an official animation set on the Creator Store.
- TSB's combat model applies **ragdoll as a status effect** at the end of most attacks and the basic chain, with a dash-based Ragdoll Cancel and brief stun immunity on getup. That is hitstun, wakeup, and cancel windows by another name — and it closely resembles what [COMBAT_SYSTEM.md](COMBAT_SYSTEM.md) already specifies.
- **Untitled Boxing Game is a solo-dev project.** A top-tier fighter shipped on a lean stack, not an exotic one. That is the most encouraging data point available to this project.
- Rivals ships per-platform control profiles and full hotkey rebinding across desktop, mobile, and console. The Input Action System now gives that for free.

---

## Budget

Founder constraint is roughly **US$100** cash. Against that:

| Item | Cost | Verdict |
|---|---|---|
| Whole code toolchain | Free | Installed |
| Blender + animation bridge | Free | Free path exists for everything below |
| Studio built-ins: ACE, Curve Editor, `IKControl`, flipbooks, Adaptive Animation, Animation Graphs | Free | Use these first |
| ShapecastHitbox, Rewind, Trove, Blink, UI Labs, Jest-Lua | Free | Adopt when a concrete need appears |
| Moon Animator 2 | ~1,700 Robux (**unverified**) | The one purchase with a strong case. Needs approval and a price check. |
| Beziers | Paid | Defer. Flipbooks plus Blender cover prototype needs. |
| EmberGen | Paid | Defer past public alpha. |
| Audio | Unpriced | Unassessed. Biggest unknown in the budget. |

The honest read: **a free pipeline can carry this project to the M4 gate.** Moon Animator is the first purchase worth making, and only once combat is proven enough to be worth animating.

---

## Adoption order

Nothing here is started before the milestone that needs it. This is a shopping list, not a to-do list.

1. **Now** — code toolchain (done). Add Jest-Lua when the first pure module exists.
2. **M2** — ShapecastHitbox and Trove with hit detection. Server Authority spike (D-020).
3. **M2/M3** — animation tool decision, once there is a move worth animating. Markers as frame data from the first move.
4. **M3** — flipbook VFX and placeholder audio. UI Labs if the HUD gets complex.
5. **Post-M4** — Adaptive Animation with fighter two. Blink only if profiling shows remotes cost too much. Paid VFX only with retention evidence.
