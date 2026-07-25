# Project Audit — 2026-07-25

**Scope:** full read of 23 documents (2,678 lines), 9 commits, and the working tree, followed by a systems, design, and production review.

**Reviewer:** AI agent (Claude Opus 5), at the user's request. Per the standing rule in [ASSET_PROVENANCE_LEDGER.md](ASSET_PROVENANCE_LEDGER.md) that rights decisions need a named human reviewer, nothing here is a decision. Findings are proposals until the user accepts them.

**No Studio test was run for this audit.** Every finding is derived from files and git history. Findings that need runtime confirmation are marked **NEEDS STUDIO**.

---

## Headline

The project is **documentation-complete and code-empty**. Every one of the 9 commits contained only Markdown. `src/server` and `src/shared` held nothing but `.gitkeep`. The only gameplay code in existence — a 352-line `InputController` and a 9-line `Bootstrap` — was **untracked**, meaning a single `git clean -fd` would have destroyed the project's entire implementation.

The governance is the strongest part of the repository and the least used. [ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md](ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md) defines a 24-discipline competency map, an 11-condition Definition of Done, a risk-register template, and a playtest-note template. There are **zero instances of any of them**. The templates were written and never filled in.

Four commits are labelled `feat:` and contain no code, because they describe Studio work that `.gitignore` excludes. That is not dishonest, but it means git history overstates progress on the arena and understates it on combat.

---

## Ranked risk register

The playbook's register format, populated for the first time. Probability and impact are 1–5.

| Risk | Category | P | I | Earliest cheap test | Mitigation | Trigger / owner | Status |
|---|---|---:|---:|---|---|---|---|
| Combat never becomes fun, after the arena has already consumed most effort | Product | 3 | 5 | Two-client M2 playtest | Close M1/M2 before any further art or exhibit work | M4 gate / user | OPEN |
| Every combat change costs a manual two-client Studio playtest, so iteration slows permanently | Process | 4 | 4 | Write one unit test over the state table | Jest-Lua on pure logic; frame data as data | Start of M2 / user | MITIGATING |
| Studio place is the only copy of the arena, and `.rbxl` is gitignored | Recoverability | 3 | 5 | Check cloud version history | Publish privately at every checkpoint with version notes | Every work block / user | OPEN |
| Mobile input is unverifiable from the repo; the HUD contract lives only in Studio | Technical | 4 | 3 | Device emulation against the new spec | [HUD_AND_UI_SPEC.md](HUD_AND_UI_SPEC.md) as the written contract | Next Studio session / user | MITIGATING |
| Q-014 unresolved while D-017 and the whole Post-M4 art plan are LOCKED and depend on it | Planning | 5 | 3 | Pick one low-end device, record a budget | Resolve Q-014 before art, not before alpha | Before any art task / user | OPEN |
| Named Curie statue conflicts with the Radiant Pioneer identifiability rule | IP | 3 | 4 | Five-unprompted-testers test on the pairing | Decide via Q-021 before the Hall of Minds is modelled | Post-M4 art start / user | OPEN |
| Server Authority beta gaps (8 animation tracks, strafe quantization) block adoption after the architecture assumes it | Technical | 3 | 3 | Timeboxed M2 spike | Keep combat sim engine-agnostic until the spike reports | M2 / user | MITIGATING |
| Solo capacity: the project needs animation, VFX, technical art, audio, and UX skills it does not have | Capacity | 4 | 4 | Cost one placeholder animation set | [TEAM_AND_SKILLS.md](TEAM_AND_SKILLS.md); buy the narrowest thing that unblocks | Scope B / user | OPEN |
| ~US$100 budget against a paid animation tool plus VFX plus audio | Budget | 4 | 3 | Price the minimum viable set | Free-first pipeline; every cost pre-approved per the ledger | Before first purchase / user | OPEN |
| Scope creep back toward the superseded ranked-1v1 or full-roster shapes | Product | 2 | 4 | Re-read the scope test in AGENTS.md | Existing scope-discipline rules are adequate; keep using them | Any new feature / user | CONTROLLED |

---

## Findings

Severity 1 is act-now. Severity 5 is record-and-move-on. Each finding names its disposition in this session.

### S1 — The only implementation was untracked

`Bootstrap.client.luau` and `Controllers/` were `??` in `git status`. Nine commits of history contained no recovery point for any code.

**Disposition: FIXED.** Committed unchanged as the first action of this session, before any refactor.

### S2 — The first piece of code silently decided an OPEN item

[COMBAT_SYSTEM.md](COMBAT_SYSTEM.md) lists sprint's keyboard binding as "Movement rule to be selected." The controller binds Sprint to `LeftShift`/`RightShift` as a hold action with a `SprintButton` touch control. Neither [DECISION_LOG.md](DECISION_LOG.md) nor [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) records it. It also pre-binds `Ability1-4`, `Mechanic`, and `Breakthrough`, all Scope B.

This breaks the project's own rule — "Never convert a DRAFT or OPEN item into a LOCKED requirement silently" — with its first code. Pre-binding future actions is defensible for an input layer; going unrecorded is not.

**Disposition: RECORDED as D-021.** Sprint is a movement modifier on `Neutral`, not a combat state, which is why the ten-state list correctly has no `Sprinting` entry.

### S3 — An undocumented Studio dependency, enforced by string literals

`InputController` resolves `PlayerGui.GameHUD` (ScreenGui) → `TouchControls` (Frame) → ten exactly-named `GuiButton`s. **No document listed those names.** Because [STUDIO_IDE_WORKFLOW.md](STUDIO_IDE_WORKFLOW.md) bars non-script instances from synced folders, the contract cannot be checked into git as instances — so it has to exist as a spec or not at all. Rename or lose the GUI and mobile input degrades to `warn()` lines with no compile-time signal.

**Disposition: FIXED.** [HUD_AND_UI_SPEC.md](HUD_AND_UI_SPEC.md) is the written contract. **NEEDS STUDIO:** confirm the live tree matches, and correct whichever side is wrong.

### S4 — A named Marie Curie statue conflicts with the Radiant Pioneer rule

[OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md) specifies a Hall of Minds statue set of **GALILEO GALILEI · ADA LOVELACE · MARIE CURIE**. [CHARACTER_ROSTER.md](CHARACTER_ROSTER.md) and [IP_CONTENT_SAFETY.md](IP_CONTENT_SAFETY.md) require Radiant Pioneer — the radiant-fields-and-decay original character — not to read as a disguised Curie.

A named Curie monument standing in the arena where a radiation-themed "original" character fights invites exactly the association the roster rule exists to prevent, and it fails the project's own test: "If five unprompted testers immediately name the same modern person, treat the character as identifiable and redesign." Neither document cross-references the other.

**Disposition: RAISED as Q-021.** Not resolved here; it is a product and rights decision. Options include substituting a different figure, dropping the statue, or redesigning Radiant Pioneer's theme.

### S5 — A LOCKED plan is blocked by a question filed for a later stage

D-017 and the entire Post-M4 art pipeline are LOCKED. Step 2 of that pipeline requires resolving **Q-014** (minimum supported device and performance budget), which sits under "Required before public alpha." The Coliseum has measurements — 2,909 instances, 74,238 triangles, 25 draw calls — and no budget to compare them against, so those numbers currently cannot pass or fail anything.

**Disposition: RAISED.** Q-014 should move to "required before finished art," which is where its dependency actually sits. Cheap to resolve: pick one representative low-end device and write the numbers down.

### S6 — No automated verification existed

No linter, formatter, type check, test runner, or CI. Combined with the standing rule that any change to remotes, hit detection, state transitions, damage, cooldowns, KOs, or respawn requires a manual server-and-two-clients test, every combat change was permanently expensive. This is the single biggest scaling problem in the project.

**Disposition: PARTLY FIXED.** Format, lint, type check, and build now run locally and in CI. On first run they caught two real defects: a deprecated `Enum.KeyCode.Unknown` and an element-type narrowing bug in a config table. **Still open:** no unit tests. Jest-Lua over the state table, cooldown math, meter clamping, and assist attribution is the highest-value remaining addition, because all of it is pure functions.

### S7 — Momentum inversion

Six of nine commits went to the arena. It is now *over-built* relative to combat — 1,949 parts, marble and brass, engraved stones, a 118-cell periodic table — and has already spawned a large deferred art-production plan, while the M1 combat tasks it was meant to unblock were untouched. The arena is genuinely good work; the ordering is the problem.

**Disposition: RECORDED as the top process risk.** The existing rule "Do not begin other fighters or production art while the universal loop remains unproven" already covers it and simply needs to be honored.

### S8 — Two shapes for one wire concept, before any remote existed

The client declared `Block` plus a phase and `Ability1..4`; [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) declared `BlockStart`/`BlockEnd` and `Ability` plus `slot`. Drift had begun with zero remotes written, because the only type contract lived in a *client* module.

**Disposition: FIXED.** Reconciled in `src/shared/Types/CombatTypes.luau`, keeping the client's phase form. Ability slots stay explicit union members so the server validates one union rather than a tag plus a range check. The architecture doc is updated to match.

### S9 — No sequence number, and a client clock used as an ordering hint

The validation list requires sequence freshness. The controller's only ordering hint was `timestamp = os.clock()`, a client-monotonic value with an arbitrary epoch that cannot be compared to server time and is unusable as an authority input.

**Disposition: FIXED.** A monotonic `sequence` is emitted; `timestamp` is retained for local presentation only and documented as never crossing the boundary.

### S10 — Latched touch actions, blocking startup, and a global left-click sink

Three defects in the committed controller: a held touch whose `InputEnded` never arrived latched the action down permanently, so `IsActionDown("Block")` returned `true` for the rest of the session; `Start()` could block ~20 s on two `WaitForChild` calls while reporting itself started; and `ContextActionResult.Sink` on `MouseButton1` swallowed left-click globally whenever the module was started, with `Stop()` as the only escape.

**Disposition: FIXED.** Focus-loss release, threaded touch binding, and a `SetEnabled` gate. **NEEDS STUDIO:** the latch fix and the touch path can only be confirmed by device emulation.

### S11 — Source tree did not match the documented Studio mapping

Files sat at `src/client/GameClient/...` while both the architecture and workflow docs map `StarterPlayerScripts/GameClient` → `src/client`. Under the documented mapping that resolves to `GameClient/GameClient/Bootstrap`. The same extra level existed for server and shared.

**Disposition: FIXED.** Flattened; `rojo build` now produces the documented tree, verified.

### S12 — The only editor configuration was outside the repository

`luau-lsp.studioPlugin.enabled` lived in `.vscode/settings.json` in the **parent** directory of the git root, and `.vscode/` was gitignored — unreproducible and undiscoverable.

**Disposition: FIXED.** Committed as `.vscode/settings.json.example`, with a negated ignore rule so it survives.

### S13 — "graybox" is stale in four documents

D-016 shipped a detailed static realism pass. [OMNISCIENCE_COLISEUM.md](OMNISCIENCE_COLISEUM.md) describes it correctly as "a detailed static prototype, not final production art"; [AGENTS.md](../AGENTS.md), [TASKS.md](../TASKS.md), [MVP_SCOPE.md](MVP_SCOPE.md), and [ROADMAP_AND_TESTING.md](ROADMAP_AND_TESTING.md) still said graybox.

**Disposition: FIXED** by terminology sweep.

### S14 — "Ten-area arena" appears to be a garbling of "ten times the area"

P-008 says "Ten-area arena clear-lane crossing time" and TASKS said "the ten-area graybox arena," but the Coliseum has **eight** sectors plus a central pedestal and gallery. D-015's actual content is *ten times D-014's floor area*. A future reader will go looking for ten areas.

**Disposition: FIXED.** Normalized to eight sectors and "ten times the D-014 floor area."

### S15 — Six live unknowns had no Q-ID

Sprint rule, Breakthrough tuning, Gravity Well numbers, the Prague clock's restoration era, public-alpha metric targets, and the Newton-name clearance were all live and untracked, so none could be closed.

**Disposition: FIXED.** Assigned Q-016 through Q-021.

### S16 — An AI agent is the named reviewer of a rights decision

The single row in [ASSET_PROVENANCE_LEDGER.md](ASSET_PROVENANCE_LEDGER.md), `REF-ARENA-001`, records its reviewer as **"Codex."** The ledger elsewhere requires "a named reviewer" for rights decisions.

**Disposition: RAISED.** Whether agent sign-off counts is the user's call. This audit takes the conservative position and does not sign anything.

### S17 — Lower-severity drift

Recorded, not individually fixed:

- Four phrasings of one disc diameter: "approximately 759-stud," "758.95-stud," and "240 × √10." Numerically consistent; no single doc gives the canonical figure with its derivation.
- **Every document shares one date**, 2026-07-23, so dates currently carry zero signal about staleness.
- The `OUT` label is defined in AGENTS.md and never used anywhere; exclusions are prose lists instead. **First applied later the same day by D-025**, which records the rejected MCP servers as OUT with a revisit trigger.
- Two status vocabularies coexist: product decisions use `LOCKED`, the ledger uses `APPROVED`. Asking "what's approved?" gets different answers in different documents.
- Two competing playtest-note templates with different fields and no statement of which is canonical. **FIXED** by a single canonical template.
- README's "Document version: 0.1" did not move across five subsequent commits that changed the arena spec materially. **FIXED.**
- Provenance for the arena reference image is recorded in two places with different field names.

---

## What is genuinely strong

Worth stating, because an audit that only lists problems misrepresents the project.

- **Server-authority rules are stated identically** across AGENTS.md, CLAUDE.md, copilot-instructions.md, TECHNICAL_ARCHITECTURE.md, COMBAT_SYSTEM.md, LLM_HANDOFF.md, and the playbook. Seven documents, zero contradictions. That is unusual.
- **The Coliseum acceptance evidence is exemplary** — exact radii, part counts, walk times, blockcast results, viewport dimensions, Scene Analysis figures. This is the standard the rest of the project should be held to.
- **Scope exclusions are repeated consistently** across four documents. The project knows what it is not.
- **The 352 lines of input code were disciplined**: `--!strict`, data-driven definitions, real exported types, idempotent start/stop, full connection teardown, a focused-text-box guard most prototypes miss. The defects found were subtle, not sloppy.
- **The IP and provenance framework is more rigorous than most commercial projects'**, including the five-unprompted-testers test and a cost gate requiring approval per purchase.

---

## Recommendations not acted on in this session

Ordered by value per unit of effort.

1. **Jest-Lua over pure logic.** State-transition legality, cooldown math, meter clamping, assist attribution, and block-arc geometry are all pure. Today each costs a two-client playtest.
2. **Frame data as data.** Every move as a table — startup, active, recovery, cancel window, damage, knockback, block behavior — with hitboxes driven from animation markers rather than per-move code. Makes balance a data edit and unit-testable.
3. **A debug overlay.** Live state, active hitbox, cooldowns, and the last rejected request with its reason. Turns "it felt wrong" into a reading.
4. **A rejection counter.** Count every validation failure by reason. Free anticheat signal and free bug detector.
5. **Resolve Q-014 now.** One device, one set of numbers. It gates a LOCKED plan.
6. **A training-mode toggle.** Infinite meter, no cooldowns, hitbox visualization, instant reset. Pays for itself within days of combat work.
7. **Actually use the handoff and playtest templates.** Zero instances exist. This is what makes work compound across sessions instead of restarting.
