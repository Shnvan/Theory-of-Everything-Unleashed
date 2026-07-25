## Session handoff — 2026-07-25

First handoff record in the project. Format: [templates/SESSION_HANDOFF.md](../templates/SESSION_HANDOFF.md).

### Target

- Task: full project audit, then foundation repair and doctrine documentation. Broader than one task from `TASKS.md` because it was a review session, recorded as M0.5.
- Acceptance condition: the implementation is recoverable, static verification exists and passes, shared types precede any remote, and each documentation gap named in the audit is closed.

### Completed

- Behavior changed: none in gameplay. Input behavior is functionally unchanged apart from five defect fixes.
- Files changed: 5 commits, `5cee20e..d5af658`.

| Commit | What |
|---|---|
| `5cee20e` | Committed the untracked input layer unchanged |
| `9fc5866` | Flattened `src` to the documented Studio mapping |
| `3a05c38` | Pinned toolchain, lint, format, typecheck, CI (D-018) |
| `f7714e4` | Shared types and config; five `InputController` fixes |
| `d5af658` | Seven doctrine documents, three templates, D-018–D-023, Q-016–Q-023 |

### Verification

- Static checks: **PASS.** `stylua --check src`, `selene src` (0 errors, 0 warnings), `luau-lsp analyze` (0 diagnostics), `rojo build`. All run locally at the pinned versions; also wired into `.github/workflows/ci.yml`.
- Link check: **PASS.** All 158 relative Markdown links resolve.
- Toolchain reproducibility: **PASS.** `rokit install` resolved all five tools at pinned versions; `wally install` succeeded.
- Rojo output tree: **PASS.** Builds `ReplicatedStorage/GameShared/{Types,Config}`, `ServerScriptService/GameServer`, `StarterPlayerScripts/GameClient/{Bootstrap,Controllers}` with no double nesting.
- Unit tests: **none exist.** Highest-value remaining gap.
- Studio solo test: **NOT RUN.**
- Server + two clients: **NOT RUN.**
- Device emulation / mobile: **NOT RUN.**
- Eight clients: **NOT RUN.**

The four "not run" lines are why the M1 input-mapping box in `TASKS.md` is still unchecked despite the code being committed.

### Decisions

- New: **D-018** toolchain adoption (supersedes D-010), **D-019** IAS migration deferred with a trigger, **D-020** Server Authority spike at M2, **D-021** sprint on Shift as a movement modifier, **D-022** the HUD instance contract, **D-023** design and engineering doctrine adopted.
- Open questions added: **Q-016** Breakthrough tuning, **Q-017** Gravity Well numbers, **Q-018** Prague clock era, **Q-020** public-alpha metrics, **Q-021** Curie statue conflict, **Q-022** Newton name clearance, **Q-023** whether agent sign-off satisfies "named reviewer". **Q-019** resolved by D-021. **Q-014** relocated to "before finished art".
- Documents updated: 14 existing, 10 new.

### Risks and blockers

- **The Studio place has no repository-side backup.** `*.rbxl` is gitignored, so the cloud version is the only copy of the arena. Publish before connecting Rojo.
- **`rojo build` is not a deployment path.** Its output contains none of the arena. Publishing it over the real place would destroy the arena.
- Touch behavior, the focus-loss latch fix, and the `MouseButton1` gate are all unverified. They are code changes to paths only a device test exercises.
- The `GameHUD` contract in `docs/HUD_AND_UI_SPEC.md` is written from what the code expects, **not** from what the place contains. One of the two may be wrong.
- Q-014 still blocks the LOCKED post-M4 art pipeline. Q-021 blocks the Hall of Minds.
- Assumption needing confirmation: that the Studio place's `GameShared`/`GameServer`/`GameClient` folders are at the locations `default.project.json` targets.

### Next smallest task

- Task: connect the Rojo plugin to the private prototype and confirm the three folders land correctly with no loss of Studio-side instances.
- Acceptance condition: a comment edited locally appears in Studio; Explorer shows no `GameClient/GameClient` nesting; the arena, `GameHUD`, and all other non-code instances are intact; Output shows no project-script errors.
- Publish a checkpoint with a version note first.

Then, in order: verify the HUD tree against the spec → Studio solo test → device emulation including the Block focus-loss check → two-client test → check the M1 input-mapping box. After that, the shared combat state machine, written as pure functions with unit tests.
