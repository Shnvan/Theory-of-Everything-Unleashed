# Documentation Index

Read only the documents needed for the current task, but always read the four marked **core**.

| Document | Purpose | Read when |
|---|---|---|
| [../README.md](../README.md) | Entry point and tool choice | **Core** |
| [../AGENTS.md](../AGENTS.md) | Canonical instructions for LLMs and coding agents | **Core** |
| [PROJECT_BRIEF.md](PROJECT_BRIEF.md) | Product vision, player promise, constraints, pillars | **Core** |
| [MVP_SCOPE.md](MVP_SCOPE.md) | What is in and out of the prototype | **Core** |
| [DECISION_LOG.md](DECISION_LOG.md) | Locked, superseded, and pending decisions | Before changing direction |
| [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) | Choices that are intentionally unresolved | Before making assumptions |
| [COMBAT_SYSTEM.md](COMBAT_SYSTEM.md) | Universal controls, rules, states, and tunables | Combat work |
| [CHARACTER_ROSTER.md](CHARACTER_ROSTER.md) | Master roster and release order | Character planning |
| [GRAVITY_SOVEREIGN.md](GRAVITY_SOVEREIGN.md) | First fighter's approved slice and draft full kit | Gravity Sovereign work |
| [OMNISCIENCE_COLISEUM.md](OMNISCIENCE_COLISEUM.md) | First arena layout, exhibit map, graybox limits, and validation | Arena work |
| [OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md](OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md) | Deferred real-artifact references, factual cards, asset pipeline, and post-M4 exhibit acceptance | Coliseum production art |
| [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) | Client/server boundaries, modules, remotes, coding rules | Any implementation |
| [STUDIO_IDE_WORKFLOW.md](STUDIO_IDE_WORKFLOW.md) | Studio, external IDE, Script Sync, Git, and testing setup | Initial setup or sync problems |
| [ROADMAP_AND_TESTING.md](ROADMAP_AND_TESTING.md) | Milestones, acceptance tests, test matrix, validation gate | Planning and QA |
| [ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md](ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md) | Development disciplines, evidence-gated production flow, agent process, and genre risks | Milestone planning, new systems, or cross-discipline work |
| [MONETIZATION_ANALYTICS.md](MONETIZATION_ANALYTICS.md) | Revenue boundaries, budget, metrics, events | Product or business work |
| [IP_CONTENT_SAFETY.md](IP_CONTENT_SAFETY.md) | Historical-person, asset, title, and violence guardrails | Character, art, audio, marketing |
| [ASSET_PROVENANCE_LEDGER.md](ASSET_PROVENANCE_LEDGER.md) | Per-asset rights, cost approval, security review, source IDs, and ship status | Any external or generated asset |
| [LLM_HANDOFF.md](LLM_HANDOFF.md) | Reusable session prompt and end-of-session handoff | Starting or ending an LLM session |
| [../TASKS.md](../TASKS.md) | Active execution checklist | Every work session |

## Fast reading paths

### First coding session

`README` → `AGENTS` → `PROJECT_BRIEF` → `MVP_SCOPE` → `STUDIO_IDE_WORKFLOW` → `TECHNICAL_ARCHITECTURE` → `TASKS`

### Combat implementation

`AGENTS` → `MVP_SCOPE` → `COMBAT_SYSTEM` → `TECHNICAL_ARCHITECTURE` → `GRAVITY_SOVEREIGN` → `TASKS`

### Character or visual design

`PROJECT_BRIEF` → `CHARACTER_ROSTER` → `IP_CONTENT_SAFETY` → `ASSET_PROVENANCE_LEDGER` → character-specific document

### Coliseum production art

`OMNISCIENCE_COLISEUM` → `OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY` → `IP_CONTENT_SAFETY` → `ASSET_PROVENANCE_LEDGER` → `TASKS`

### Product decision

`PROJECT_BRIEF` → `MVP_SCOPE` → `DECISION_LOG` → `OPEN_QUESTIONS` → update `DECISION_LOG`

### Milestone or system planning

`AGENTS` → `PROJECT_BRIEF` → `MVP_SCOPE` → `ROBLOX_GAME_DEVELOPMENT_PLAYBOOK` → relevant domain document → `TASKS`
