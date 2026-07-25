# Decision Log

This file records product direction. Newer explicit user decisions supersede older entries.

## Active decisions

| ID | Date | Status | Decision | Rationale |
|---|---|---|---|---|
| D-001 | 2026-07-23 | LOCKED | The game is titled **Theory of Everything: Unleashed** for development. | Strong science-power identity. Public-release title clearance remains required. |
| D-002 | 2026-07-23 | LOCKED | The primary mode is a continuous public free-for-all battleground. | Smaller launch shape than a full 1v1 ranked fighter; immediate play in one server. |
| D-003 | 2026-07-23 | LOCKED | Target maximum is eight players in one compact arena. | Keeps combat readable and performance/test scope manageable. |
| D-004 | 2026-07-23 | LOCKED | Build Gravity Sovereign first; do not begin the other roster members until the foundation passes. | One polished proof is more valuable than several incomplete kits. |
| D-005 | 2026-07-23 | LOCKED | Public-alpha target is three fighters: Gravity Sovereign, Eureka Engineer, and Renaissance Mind. | Gives initial archetype variety without committing to the 12-fighter roadmap. |
| D-006 | 2026-07-23 | LOCKED | Fighters use select-screen titles. Older historical figures may use original stylized portrayals; five modern science themes remain genuinely original characters. | Provides consistent branding while reducing identity and likeness risk. |
| D-007 | 2026-07-23 | LOCKED | Final Proof remains only as a short, stylized 1–2 second KO effect in FFA. | Long finishers are interruptible, frustrating, and expensive in a public arena. |
| D-008 | 2026-07-23 | LOCKED | Combat is non-gory and does not depict realistic death, blood, dismemberment, or torture. | Preserves a broad potential audience and the game's science-fantasy tone. |
| D-009 | 2026-07-23 | LOCKED | Use Roblox Studio plus an external IDE; start with built-in Script Sync. | Studio owns place/assets/testing, while the IDE owns code/docs/history with minimal setup. |
| D-010 | 2026-07-23 | SUPERSEDED | Do not require Rojo for the prototype. | Superseded by D-018 on 2026-07-25. The reasoning held while there was no code; it stopped holding once packages, linting, and CI were needed. |
| D-011 | 2026-07-23 | LOCKED | Server authority covers damage, cooldowns, KOs, assists, meter, and respawn. | Competitive PvP cannot trust client-declared results. |
| D-012 | 2026-07-23 | LOCKED | Monetization is cosmetic-only and begins after combat validation. | Revenue systems cannot rescue an unfun loop; combat power sales damage fairness. |
| D-013 | 2026-07-23 | LOCKED | The first arena is internally named **The Omniscience Coliseum**, a compact Greco-Roman monument to science and invention. Its M1 version uses static graybox proxies for 24 exhibits and original fighter-title monuments. | Establishes a distinct science-fantasy identity while preserving a readable combat disc and avoiding modern-person likeness or endorsement risk. |
| D-014 | 2026-07-23 | LOCKED | Expand The Omniscience Coliseum to a 240-stud combat disc on a 420×420 foundation, distribute the 24 static exhibits across the interior, and hide exhibit-name labels. Keep exhibits non-colliding and preserve clear traversal lanes. | Direct scale review found the former 137-stud playable area too small. The larger layout creates the intended monumental scale while retaining one contained eight-player arena. This refines the size and exhibit-placement aspects of D-003 and D-013. |
| D-015 | 2026-07-23 | LOCKED | Increase The Omniscience Coliseum to ten times D-014's floor area by scaling the arena uniformly by `√10`, scale all 24 exhibits to five times their D-014 dimensions, make visible exhibit geometry collidable, and add visible plus invisible perimeter containment. | The approved monumental scale requires larger architecture and physical landmarks while preventing players from walking or jumping outside. This supersedes D-014's exact dimensions and non-colliding-exhibit rule while preserving its theme, organization, and hidden exhibit-name labels. |
| D-016 | 2026-07-23 | LOCKED | Give The Omniscience Coliseum an arena-specific static realism pass using only Studio-native geometry, aged marble, dark stone, brass, glass, and restrained science-energy accents. Add one readable angled stone inscription to each of the 24 exhibits, use simplified physical collision shells for exhibits, and keep the arena at or below 2,000 BaseParts. | The user approved a more detailed museum identity while keeping every exhibit static and retaining mobile-conscious prototype limits. This supersedes D-015's literal all-visible-parts collision rule and D-014/D-015's hidden exhibit-name rule without resolving the project's broader final-art direction. |
| D-017 | 2026-07-23 | LOCKED | After the M4 prototype gate, replace the Coliseum's invented exhibit visuals with named historical replicas or authoritative scientific reconstructions. Preserve internal Model identities, arena scale, footprints, and collision shells; use monumentally enlarged authentic proportions, real-name stones, and factual museum cards. Verified external assets and custom meshes are allowed, but every asset needs approved provenance and every cost needs separate advance user approval. | The user wants the finished exhibits to be educationally credible rather than decorative inventions. Deferring production until after M4 protects the combat-validation order. This future production decision leaves the accepted D-016 M1 prototype intact and does not resolve Q-008's global character-art direction. |
| D-018 | 2026-07-25 | LOCKED | Adopt a pinned file-based toolchain: Rokit, Rojo 7, Wally, StyLua, Selene, luau-lsp, and GitHub Actions CI. Rojo replaces Script Sync as the primary sync path; Script Sync remains a documented fallback. The project file declares only the three code folders, so the Studio place keeps ownership of the arena, GUI, rigs, and audio. | Supersedes D-010. Two of the five re-evaluation triggers already recorded in `docs/STUDIO_IDE_WORKFLOW.md` had been met: CI needs reproducible place generation, and every combat library the project will want ships on Wally, which requires a project file. The static gates found two real defects on their first run. This changes the code sync mechanism only; it does not change the source-of-truth policy for non-code assets. |
| D-019 | 2026-07-25 | LOCKED | Keep the input layer on `ContextActionService` for now. Migrate to the Input Action System when ability targeting begins or when the Server Authority spike (D-020) starts, whichever comes first. | The Input Action System reached full release after this project's documents were written, and it is the input layer Server Authority expects. It would also remove the hand-wired touch-button dependency. But the existing controller works, and rewriting it mid-M1 trades working code for platform modernity at the wrong moment. Recorded with a trigger so the migration is scheduled rather than forgotten. |
| D-020 | 2026-07-25 | LOCKED | Build M1 and M2 on classic remote validation as already specified. Keep combat simulation in modules that could later move under `BindToSimulation`. Add a timeboxed Server Authority spike as an M2 task with a recorded go/no-go. | Roblox shipped engine-level client prediction and rollback resimulation as a Client Beta in April 2026 — the single most valuable platform feature for a fighting game. It is also beta, with documented gaps that hit this game directly: a maximum of eight active animation tracks per `Animator`, and position quantization causing drift while strafing. Absorbing beta instability during the foundation milestone is the wrong risk; ignoring the feature entirely is the wrong bet. A spike after combat exists resolves it with evidence. |
| D-021 | 2026-07-25 | LOCKED | Sprint is bound to `LeftShift`/`RightShift` as a hold action on keyboard, with a `SprintButton` touch control. Sprint is a movement modifier layered on `Neutral`, not a combat state, so the ten-state model correctly has no `Sprinting` entry. | `docs/COMBAT_SYSTEM.md` listed the keyboard sprint rule as "Movement rule to be selected", but the project's first code had already bound it, unrecorded. That is precisely the silent OPEN-to-requirement conversion the project forbids. This ratifies what the code does and states the state-model consequence explicitly. The binding itself remains DEFAULT and may be retuned. |
| D-022 | 2026-07-25 | LOCKED | The Studio HUD instance tree that client code resolves by name is specified in `docs/HUD_AND_UI_SPEC.md`, and that document is the contract. Any code dependency on a named Studio instance requires a written repository-side spec. | `InputController` resolved ten touch buttons by exact name inside the Studio place, and those names existed nowhere but in the code. Because non-script instances are barred from synced folders, the contract cannot live in git as instances — so it lives as a document or not at all. Without it, renaming one instance silently disables mobile input with no compile-time signal. |
| D-023 | 2026-07-25 | LOCKED | Adopt `docs/DESIGN_PHILOSOPHY.md` as design doctrine and `docs/DEVELOPER_RULES.md` as engineering doctrine. `AGENTS.md` stays the short canonical charter and links to both. | The five product pillars did not settle arguments about specific moves, and the engineering rules were spread across several documents with no single reviewable list. Neither document introduces a new requirement; both make existing ones applicable to one ability or one diff. `AGENTS.md` stays concise per its own rule. |

## Prototype defaults

These are starting values, not promises.

| ID | Status | Default |
|---|---|---|
| P-001 | DEFAULT | 100 maximum health |
| P-002 | DEFAULT | Five-second respawn |
| P-003 | DEFAULT | Two seconds of spawn protection, canceled by attacking |
| P-004 | SUPERSEDED | Arena crossing time of about ten seconds; replaced after the approved scale revision |
| P-005 | DEFAULT | Responsive basic attacks with heavier cinematic abilities |
| P-006 | DEFAULT | Third-person camera and hybrid directional targeting |
| P-007 | SUPERSEDED | Expanded arena clear-lane crossing time of about seventeen seconds; replaced by D-015 |
| P-008 | DEFAULT | Clear-lane crossing time across the current arena, estimated at about 53 seconds. The arena has eight thematic sectors; "ten" in the superseded P-004 and P-007 lineage referred to ten times D-014's floor area, not ten areas. |
| P-009 | DEFAULT | Sprint bound to `LeftShift`/`RightShift` as a hold action; see D-021 |

Change defaults through documented playtest evidence without treating the change as a project pivot.

Numeric defaults live in `src/shared/Config/CombatConfig.luau`, each labelled with its status. Changing a value labelled LOCKED there requires a decision in this log, not a playtest observation.

## Superseded directions

| Direction | Status | Why it is not current |
|---|---|---|
| PvE-first arena roguelite | SUPERSEDED | The project pivoted to player-versus-player public combat. |
| Tekken/Mortal Kombat-style ranked 1v1 | SUPERSEDED | Matchmaking, rounds, bots, strict roster balance, and duel presentation expanded the solo scope too far. |
| Ranked Nobel-themed ladder | SUPERSEDED | Ranked 1v1 is not in the current game shape; specific protected terms also need clearance. |
| Long “Finish Him”-style cinematic | SUPERSEDED | It does not fit interruptible continuous FFA and must not copy another franchise. |
| Full public battleground clone | REJECTED | The project adapts broad genre lessons but must have original science identity and a smaller scope. |

## How to add a decision

1. Describe the problem and alternatives.
2. State whether the change affects a LOCKED direction or a DEFAULT.
3. Record the user's choice, date, and rationale.
4. Update affected documents and `TASKS.md`.
5. Mark the old choice SUPERSEDED instead of deleting its history.
