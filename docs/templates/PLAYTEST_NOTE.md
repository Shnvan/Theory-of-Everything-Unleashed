# Playtest Note — template

**Canonical.** [ROADMAP_AND_TESTING.md](../ROADMAP_AND_TESTING.md) and [ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md](../ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md) previously carried two different versions of this template with no statement of which to use. This file is the merged one; both now point here.

Copy the block below into a new file under `docs/playtests/` named `YYYY-MM-DD-short-topic.md`.

**Ask players to demonstrate and explain.** Do not ask whether the concept "could be good" — that question has no useful answer. The observation that matters most is what they did without being told to.

---

```markdown
## Playtest YYYY-MM-DD

### Setup

- Build, place version, and commit:
- Hypothesis:
- Acceptance threshold (state it before playing):
- Players, devices, input types, and client count:
- Instructions given (ideally: none):

### Observed

- What players actually did, in order:
- Time to first meaningful action:
- Did they re-engage voluntarily after a KO?
- Could they explain why they lost?
- Confusion and failure points:
- Best moment:
- Worst moment:

### Technical

- Errors in Output:
- Performance (frame time, and on which device):
- P0/P1 issues:

### Decision

- Did the acceptance threshold pass?
- Evidence-supported decision:
- DEFAULT values this changes (and their new numbers):
- Next smallest change:
```

---

## Which acceptance threshold applies

| Milestone | The threshold |
|---|---|
| M1 | A player can move, dash, damage the dummy through a server-approved action, die, and respawn with no stuck states. |
| M2 | Two clients attack, block, escape once, and complete repeated KO/respawn loops without desynchronizing. |
| M3 | Three uninstructed testers enter, fight, understand the main controls, and **voluntarily re-engage after a KO**. |
| M4 | The full gate in [TASKS.md](../../TASKS.md), including adversarial tests. |

The M3 threshold is the one that decides the project. Per [PROJECT_BRIEF.md](../PROJECT_BRIEF.md), the product test is whether the prototype creates *"Let me fight again"* — not *"This could look cool after it has art."*
