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
| [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) | Client/server boundaries, modules, remotes, coding rules | Any implementation |
| [STUDIO_IDE_WORKFLOW.md](STUDIO_IDE_WORKFLOW.md) | Studio, external IDE, Script Sync, Git, and testing setup | Initial setup or sync problems |
| [ROADMAP_AND_TESTING.md](ROADMAP_AND_TESTING.md) | Milestones, acceptance tests, test matrix, validation gate | Planning and QA |
| [MONETIZATION_ANALYTICS.md](MONETIZATION_ANALYTICS.md) | Revenue boundaries, budget, metrics, events | Product or business work |
| [IP_CONTENT_SAFETY.md](IP_CONTENT_SAFETY.md) | Historical-person, asset, title, and violence guardrails | Character, art, audio, marketing |
| [LLM_HANDOFF.md](LLM_HANDOFF.md) | Reusable session prompt and end-of-session handoff | Starting or ending an LLM session |
| [../TASKS.md](../TASKS.md) | Active execution checklist | Every work session |

## Fast reading paths

### First coding session

`README` → `AGENTS` → `PROJECT_BRIEF` → `MVP_SCOPE` → `STUDIO_IDE_WORKFLOW` → `TECHNICAL_ARCHITECTURE` → `TASKS`

### Combat implementation

`AGENTS` → `MVP_SCOPE` → `COMBAT_SYSTEM` → `TECHNICAL_ARCHITECTURE` → `GRAVITY_SOVEREIGN` → `TASKS`

### Character or visual design

`PROJECT_BRIEF` → `CHARACTER_ROSTER` → `IP_CONTENT_SAFETY` → character-specific document

### Product decision

`PROJECT_BRIEF` → `MVP_SCOPE` → `DECISION_LOG` → `OPEN_QUESTIONS` → update `DECISION_LOG`
