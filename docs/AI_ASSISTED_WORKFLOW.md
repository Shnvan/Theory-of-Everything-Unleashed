# AI-Assisted Development Workflow

**Status:** LOCKED as working method.

**Relationship to [LLM_HANDOFF.md](LLM_HANDOFF.md):** that document holds the reusable *prompts*. This one holds the *method* — how experienced developers get reliable work out of coding agents like Claude Code and Codex, and where those tools fail on a Roblox project specifically.

---

## What actually determines output quality

Not prompt phrasing. In order of real impact:

1. **A persistent instruction file the agent reads every session.** [AGENTS.md](../AGENTS.md), [CLAUDE.md](../CLAUDE.md), and `.github/copilot-instructions.md` already do this, and it is why this project's docs are unusually coherent. Every rule you write once there is a rule you stop repeating.
2. **A narrow task with a stated acceptance condition.** "Implement only the shared combat-state transition module; acceptance is that invalid transitions are rejected and death overrides action states" produces good work. "Build the combat system" produces plausible-looking sprawl.
3. **Machine-checkable gates.** An agent cannot reliably self-assess. It can run `selene`, `stylua --check`, `luau-lsp analyze`, and a test suite. Everything checkable should be checked by a tool, not by trust — which is much of why the toolchain was adopted (D-018).
4. **A small diff.** Review cost scales with diff size, and unreviewed agent output is where defects enter.
5. Prompt wording, a distant fifth.

---

## The loop

Four phases. Do not collapse them; the collapse is where projects lose control of their own codebase.

### 1. Explore

Have the agent read before it writes. On an unfamiliar area, ask for a written summary of what exists and where — and check that summary against reality before trusting it.

Use read-only sub-agents for broad searches so the search output does not crowd out the actual work. Sub-agents are for **fan-out reading**, not for parallel writing: two agents editing the same tree will conflict.

### 2. Plan

For anything touching more than one file, get a written plan first and read it properly. This is the cheapest possible place to catch a wrong approach — a bad plan costs one paragraph to fix and a whole diff to undo.

A plan is good when it names the files, the acceptance condition, and what it will **not** do. Push back on plans that are lists of everything the agent noticed.

### 3. Implement

- One acceptance target per work block. The playbook's WIP limit of one primary implementation task applies to agent work too, and is easier to violate with an agent because it is happy to do ten things.
- Commit checkpoints as you go. The reason this project's first code sat untracked for a whole session is that nobody stopped to commit.
- Watch for scope drift. "While I was there I also…" is where unreviewed changes come from. It is legitimate to ask for the extra work to be reverted and proposed separately.

### 4. Verify

- Run the static gates every time. They are seconds and they catch real bugs — both defects found in this project's first lint run were things a human reviewer would plausibly have missed.
- **Studio, device, and multiplayer tests are yours.** An agent editing files cannot know what is in the DataModel, whether sync is live, what Output says, or whether a two-client test passed. The standing rule — "Do not claim a Studio test ran unless you actually ran it or I provided its output" — exists because this is the single most likely place for an agent to produce a confident falsehood.
- Feed real output back. Paste the Output pane, the error, the Script Analysis entry. An agent given the actual error fixes the actual bug; an agent asked to guess invents a plausible one.

---

## The Roblox-specific problem

This is the part general AI-coding advice misses, and it is the defining constraint here.

**An agent can complete file work and cannot complete acceptance.** Split every task accordingly:

| Agent can finish alone | Needs you in Studio |
|---|---|
| Pure logic: state machines, cooldown math, meter clamping, geometry | Anything about how it *feels* |
| Type and config modules | Whether an instance exists or is named correctly |
| Validation code and its rejection paths | Whether a remote actually behaves under two clients |
| Docs, decisions, task bookkeeping | Touch reachability, safe areas, viewport readability |
| Static-gate fixes | Performance on a real device |

Practical consequences:

- **Write pure logic first, in `src/shared`, and unit test it.** This is the largest available lever on this project. Frame data, transition legality, cooldown math, assist attribution, and block-arc geometry are all pure functions. Today each of them costs a manual two-client playtest to check, which makes iteration expensive forever. Moving that verification into tests is what makes agent work compound.
- **Give the agent Explorer trees and property values** when Studio MCP is not connected. Otherwise it will invent instance names — and the project already has one bug of exactly that shape (S3 in [PROJECT_AUDIT_2026-07-25.md](PROJECT_AUDIT_2026-07-25.md)).
- **Studio MCP** narrows the left column and widens the blast radius. It is connected here (D-024), with three things worth knowing:
  - **Servers load at session start.** Registering or changing an MCP server does nothing for a session already running, and an agent cannot gain the capability mid-conversation. If it claims to, it is wrong.
  - **Scripts are read-only over MCP.** Rojo overwrites Studio-side script edits silently. Reads and non-script instances only; see [STUDIO_IDE_WORKFLOW.md](STUDIO_IDE_WORKFLOW.md).
  - **It removes guessing, not testing.** The right column above is unchanged. Feel, thumb reach, and whether combat is fun are not inspectable, and an agent with MCP still cannot tell you a two-client test passed.
- **Do not add MCP servers speculatively.** Each one is a process with real access, launched on your machine. D-025 records Blender, GitHub, design-tool, and filesystem MCP servers as OUT, with the reasoning and a revisit trigger. "It might be useful later" is the same failure this project already has a named risk for.

---

## Context hygiene

- Point at documents; do not paste them. This repository is structured so `AGENTS.md` plus one domain document is usually the whole briefing.
- Long sessions drift. When the agent starts re-deriving things it established an hour ago, write a handoff and start fresh — that is what [the handoff template](templates/SESSION_HANDOFF.md) is for.
- **One task per session** works better than a session that wanders, because the record of what was done stays legible afterwards.
- Zero handoff records exist in this project so far. That is the difference between work that compounds and work that restarts.

---

## Reviewing agent output

Read the diff. Every line. If a diff is too large to read, that is a finding about the task, not about your patience.

Specific things to look for in Roblox work, all of which an agent will produce confidently:

- **Invented authority.** A client computing damage, choosing victims, or deciding it is invulnerable. Grep the diff for anything consequential happening client-side.
- **Missing cleanup.** A delayed callback that does not re-check that its character still exists. An ability with cleanup for completion but not for death.
- **Magic numbers.** Tunables inlined instead of added to shared config.
- **Silent decisions.** A value chosen where a document says OPEN. This project's first code did exactly that with the sprint keybind (S2).
- **Overbuilding.** A framework, an abstraction layer, or a generalization for one caller. "Do not add a framework or package manager without a concrete need" applies to agent suggestions especially, because generalizing is cheap for an agent and expensive for you.
- **Claimed verification.** Any statement that a test passed. Check whether it could have been run.

Use `/code-review` on the working diff, and `/security-review` on anything touching remotes or validation.

---

## Task shapes

Good, because acceptance is observable and the boundary is explicit:

```text
Implement only the shared combat-state transition module for M1.
Acceptance: invalid transitions are rejected, death overrides action states,
and respawn returns a fresh character to SpawnProtected then Neutral.
Do not implement remotes, hitboxes, abilities, or UI yet.
```

Also good — verification-shaped, and the agent can finish it completely:

```text
Write unit tests for CombatConfig.getAssistDamageThreshold and
CombatTypes.isStrongerThan. Cover equal priority, Dead overriding everything,
and MAX_HEALTH being tuned.
```

Bad:

```text
Build the combat system.
Make the game feel better.
Fix everything you find.
```

The last is the worst of the three: it invites exactly the unreviewed sprawl this document exists to prevent.

---

## What agents must never do

Restated from the playbook because it is the operative list:

- Silently turn an OPEN or DRAFT item into a requirement.
- Claim a Studio, device, multiplayer, or external test they did not run.
- Add content outside the active milestone because it is easy or looks good.
- Trust client-declared results or arbitrary Instance references.
- Overwrite user work, delete conflicting objects, or publish externally without authority.
- Optimize from intuition when a profiler would identify the real bottleneck.
- Mark a task complete when only implementation, not acceptance, is complete.

---

## Session checklist

**Start:** name one task from [TASKS.md](../TASKS.md). State its acceptance condition. Confirm the working tree is clean and committed — check `git status` for untracked work before anything else, because that is how this project nearly lost its only implementation.

**End:** run the static gates. Commit a coherent checkpoint. Write a [handoff](templates/SESSION_HANDOFF.md) naming what was verified, what was not, and the next smallest task. Update `TASKS.md` **only** if acceptance actually passed.
