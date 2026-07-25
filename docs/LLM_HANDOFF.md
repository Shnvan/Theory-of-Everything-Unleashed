# LLM Handoff

Use this document when starting or ending work with an LLM.

## Pasteable session-start prompt

```text
You are helping build a Roblox game called Theory of Everything: Unleashed.

First read AGENTS.md, README.md, docs/PROJECT_BRIEF.md, docs/MVP_SCOPE.md,
docs/DECISION_LOG.md, TASKS.md, and the domain document relevant to my request.

The current game is an eight-player continuous public FFA battleground, not the
older PvE roguelite or ranked 1v1 idea. The current milestone is the universal
combat foundation and a Gravity Sovereign vertical slice in one arena, The
Omniscience Coliseum, which is already built and validated.

Treat LOCKED decisions as approved direction, DEFAULT values as tunable, DRAFT
ideas as unapproved, OPEN questions as unresolved, and OUT items as outside the
current scope. Do not implement extra characters, ranked mode, saving, a store,
full destruction, or a finished city unless I explicitly change the scope.

For gameplay code, the server must own damage, cooldowns, hit eligibility, KOs,
assists, meter, and respawning. Clients may request actions and predict
presentation but may not declare results.

Before editing, summarize the exact acceptance condition you will target. After
editing, report files changed, Studio tests run, remaining risks, and the next
small task. Do not claim a Studio test ran unless you actually ran it or I
provided its output.

My task for this session is:
[INSERT ONE TASK FROM TASKS.md]
```

## Context packet for a narrow coding request

Give the LLM:

- `AGENTS.md`.
- The exact task from `TASKS.md`.
- `COMBAT_SYSTEM.md` for behavior.
- `TECHNICAL_ARCHITECTURE.md` for boundaries.
- The relevant character document.
- The current source files.
- Studio Explorer paths and Output errors when Studio MCP is unavailable.

Do not paste the whole conversation when these documents contain the current decision.

## Good task shape

```text
Implement only the shared combat-state transition module for M1.
Acceptance: invalid transitions are rejected, death overrides action states,
and respawn returns a fresh character to SpawnProtected then Neutral.
Do not implement remotes, hitboxes, abilities, or UI yet.
```

Avoid:

```text
Build the entire battleground game.
```

## Studio-awareness rule

An LLM editing local files does not automatically know:

- Which Instances currently exist in Studio.
- Whether Rojo is connected and syncing.
- Whether animations or assets are uploaded.
- What Output or Script Analysis reports.
- Whether a multiplayer or mobile test passed.

If Studio MCP is connected, verify the active private prototype before any action. If it is not connected, provide the relevant Explorer tree, property values, and error output.

Studio MCP changes only the first two items in that list. It lets an agent read the data model and Output instead of guessing, which is worth a great deal — but it does **not** let it judge whether a multiplayer or mobile test passed, and it must not be used to edit scripts, because Rojo overwrites Studio-side script edits silently (D-024). MCP servers also load at session start, so a server registered mid-session is unavailable until a new one begins.

## Decision-update prompt

```text
We are changing [OLD DECISION] to [NEW DECISION] because [EVIDENCE].
Show every document and active task affected. Update docs/DECISION_LOG.md by
marking the old direction superseded; do not erase the history. Do not edit
gameplay code until the documentation conflict is resolved.
```

## End-of-session handoff template

```markdown
## Session handoff — YYYY-MM-DD

### Target

- Task:
- Acceptance condition:

### Completed

- Behavior:
- Files changed:

### Verification

- Static checks:
- Studio solo test:
- Server/client test:
- Mobile/device test:

### Decisions

- New or changed:
- Documents updated:

### Risks and blockers

- Known issue:
- Assumption requiring confirmation:

### Next smallest task

- Task:
- Acceptance condition:
```

## Context-maintenance rule

After a meaningful session:

- Check completed items in `TASKS.md`.
- Update behavior in its domain document.
- Add product choices to `DECISION_LOG.md`.
- Remove resolved items from `OPEN_QUESTIONS.md` or mark them resolved with the decision ID.
- Do not copy large source files into Markdown.
- Keep `AGENTS.md` concise and stable; put system details in the domain documents.
