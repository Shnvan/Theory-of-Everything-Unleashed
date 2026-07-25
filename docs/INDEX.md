# Documentation Index

Read only the documents needed for the current task, but always read the four marked **core**.

| Document | Purpose | Read when |
|---|---|---|
| [../README.md](../README.md) | Entry point and tool choice | **Core** |
| [../AGENTS.md](../AGENTS.md) | Canonical instructions for LLMs and coding agents | **Core** |
| [PROJECT_BRIEF.md](PROJECT_BRIEF.md) | Product vision, player promise, constraints, pillars | **Core** |
| [MVP_SCOPE.md](MVP_SCOPE.md) | What is in and out of the prototype | **Core** |
| [PROJECT_AUDIT_2026-07-25.md](PROJECT_AUDIT_2026-07-25.md) | Where the project actually stands: findings, ranked risk register, recommendations | Orienting, or planning the next milestone |
| [DECISION_LOG.md](DECISION_LOG.md) | Locked, superseded, and pending decisions | Before changing direction |
| [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) | Choices that are intentionally unresolved | Before making assumptions |
| [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md) | Pillars as per-move rules, counterplay contract, telegraphs, feedback hierarchy, consistency checklist | Designing any move, ability, VFX, or UI |
| [DEVELOPER_RULES.md](DEVELOPER_RULES.md) | Engineering do/do-not rules, lifecycle, verification ladder, commit and pre-commit checklists | Writing any code |
| [COMBAT_SYSTEM.md](COMBAT_SYSTEM.md) | Universal controls, rules, states, and tunables | Combat work |
| [HUD_AND_UI_SPEC.md](HUD_AND_UI_SPEC.md) | The Studio HUD instance contract, mobile layout, safe areas, information display | Input, HUD, or mobile work |
| [CHARACTER_ROSTER.md](CHARACTER_ROSTER.md) | Master roster and release order | Character planning |
| [GRAVITY_SOVEREIGN.md](GRAVITY_SOVEREIGN.md) | First fighter's approved slice and draft full kit | Gravity Sovereign work |
| [OMNISCIENCE_COLISEUM.md](OMNISCIENCE_COLISEUM.md) | First arena layout, exhibit map, prototype limits, and recorded validation | Arena work |
| [OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md) | Deferred real-artifact references, factual cards, asset pipeline, and post-M4 exhibit acceptance | Coliseum production art |
| [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) | Client/server boundaries, modules, remotes, coding rules | Any implementation |
| [STUDIO_IDE_WORKFLOW.md](STUDIO_IDE_WORKFLOW.md) | Studio, external IDE, Rojo, Git, and testing setup | Initial setup or sync problems |
| [TOOLING_AND_PIPELINE.md](TOOLING_AND_PIPELINE.md) | Toolchain, the 2026 platform shift, animation/VFX/audio pipelines, what not to use, budget | Choosing a tool, library, or pipeline |
| [ROADMAP_AND_TESTING.md](ROADMAP_AND_TESTING.md) | Milestones, acceptance tests, test matrix, validation gate | Planning and QA |
| [ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md](ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md) | Development disciplines, evidence-gated production flow, agent process, and genre risks | Milestone planning, new systems, or cross-discipline work |
| [TEAM_AND_SKILLS.md](TEAM_AND_SKILLS.md) | Which disciplines a solo developer must hold, defer, or buy on this project | Capacity, hiring, or commissioning decisions |
| [MONETIZATION_ANALYTICS.md](MONETIZATION_ANALYTICS.md) | Revenue boundaries, budget, metrics, events | Product or business work |
| [IP_CONTENT_SAFETY.md](IP_CONTENT_SAFETY.md) | Historical-person, asset, title, and violence guardrails | Character, art, audio, marketing |
| [ASSET_PROVENANCE_LEDGER.md](ASSET_PROVENANCE_LEDGER.md) | Per-asset rights, cost approval, security review, source IDs, and ship status | Any external or generated asset |
| [LLM_HANDOFF.md](LLM_HANDOFF.md) | Reusable session prompts | Starting or ending an LLM session |
| [AI_ASSISTED_WORKFLOW.md](AI_ASSISTED_WORKFLOW.md) | The working method behind those prompts: explore/plan/implement/verify, what an agent cannot verify, review checklist | Working with a coding agent |
| [templates/](templates/) | [MOVE_SPEC](templates/MOVE_SPEC.md), [PLAYTEST_NOTE](templates/PLAYTEST_NOTE.md), [SESSION_HANDOFF](templates/SESSION_HANDOFF.md) | Before a move, after a playtest, at the end of a session |
| [../TASKS.md](../TASKS.md) | Active execution checklist | Every work session |

## Fast reading paths

### Orienting on a project you have not seen in a while

`PROJECT_AUDIT_2026-07-25` → `DECISION_LOG` → `TASKS`

### First coding session

`README` → `AGENTS` → `PROJECT_BRIEF` → `MVP_SCOPE` → `STUDIO_IDE_WORKFLOW` → `DEVELOPER_RULES` → `TECHNICAL_ARCHITECTURE` → `TASKS`

### Combat implementation

`AGENTS` → `MVP_SCOPE` → `COMBAT_SYSTEM` → `DEVELOPER_RULES` → `TECHNICAL_ARCHITECTURE` → `GRAVITY_SOVEREIGN` → `TASKS`

### Designing a move or ability

`DESIGN_PHILOSOPHY` → `COMBAT_SYSTEM` → character document → `templates/MOVE_SPEC` → `OPEN_QUESTIONS`

### Input, HUD, or mobile work

`HUD_AND_UI_SPEC` → `DESIGN_PHILOSOPHY` → `src/shared/Config/InputConfig.luau` → device emulation

### Character or visual design

`PROJECT_BRIEF` → `DESIGN_PHILOSOPHY` → `CHARACTER_ROSTER` → `IP_CONTENT_SAFETY` → `ASSET_PROVENANCE_LEDGER` → character-specific document

### Choosing a tool or pipeline

`TOOLING_AND_PIPELINE` → `ASSET_PROVENANCE_LEDGER` (for anything with a cost) → `DECISION_LOG`

### Coliseum production art

`OMNISCIENCE_COLISEUM` → `OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY` → `IP_CONTENT_SAFETY` → `ASSET_PROVENANCE_LEDGER` → `TASKS`

### Product decision

`PROJECT_BRIEF` → `MVP_SCOPE` → `DECISION_LOG` → `OPEN_QUESTIONS` → update `DECISION_LOG`

### Milestone or system planning

`AGENTS` → `PROJECT_BRIEF` → `MVP_SCOPE` → `ROBLOX_GAME_DEVELOPMENT_PLAYBOOK` → relevant domain document → `TASKS`
