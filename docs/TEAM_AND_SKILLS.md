# Team and Skills

**Status:** DRAFT. The gap assessment is a proposal; no hiring, commissioning, or spend is approved.

**Relationship to the playbook.** [ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md](ROBLOX_GAME_DEVELOPMENT_PLAYBOOK.md) has the full 24-discipline competency map, with what each owns, its minimum competency, and its quality gate. **That table is not repeated here.** This document answers the narrower question: for *this* project, at *this* stage, with one developer — which disciplines must you personally hold, which can wait, and which will eventually need someone else?

Founder constraints from [PROJECT_BRIEF.md](PROJECT_BRIEF.md): solo, Luau "Advanced", ~60 hours per week, ~US$100 cash, no existing models, animations, audience, or testers, and revenue as the primary goal.

---

## The honest summary

A solo developer can reach the M4 gate on this project without acquiring a single new discipline, because **the prototype's question is whether combat feels good** — and that is answered by engineering, design, and testing, all of which you have or can reach.

The disciplines you do not have become blocking at **Scope B**, not now. The order in which they bite is: **animation, then VFX, then audio, then UX**. Animation is the real bottleneck, and it is also the one most people underestimate.

---

## What you must hold personally, now

These cannot be delegated on this project at this stage, because they define what everything else serves.

| Discipline | Why it cannot wait | Where the standard is written |
|---|---|---|
| **Product direction** | Nobody else can decide what this game is or when to stop. The M4 go/no-go is the highest-value decision in the project. | [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [MVP_SCOPE.md](MVP_SCOPE.md) |
| **Game design** | Combat feel is the entire prototype hypothesis. It is not specifiable to someone else before it exists. | [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md), [COMBAT_SYSTEM.md](COMBAT_SYSTEM.md) |
| **Gameplay / Luau engineering** | Already your strength, and it is the critical path. | [DEVELOPER_RULES.md](DEVELOPER_RULES.md) |
| **Networking and security** | The one discipline where a gap is *unrecoverable* rather than merely slow. Exploitable combat destroys a PvP game's credibility permanently, and D-011 depends entirely on this being done properly. | [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) |
| **QA** | Nobody else will run your two-client tests, and the project's own rule makes them mandatory. | [ROADMAP_AND_TESTING.md](ROADMAP_AND_TESTING.md) |
| **Production / project management** | You are already doing this well. The visible failure mode is ordering, not tracking. | [TASKS.md](../TASKS.md) |
| **IP, legal, provenance** | Non-delegable because the *decisions* are yours, and this project's design deliberately runs close to real people's identities. | [IP_CONTENT_SAFETY.md](IP_CONTENT_SAFETY.md) |

---

## What you need enough of, soon

Not mastery. Enough to make a safe prototype decision and recognize a failing gate.

| Discipline | The minimum that unblocks you | When it bites |
|---|---|---|
| **UX, UI, input, accessibility** | Mobile-first layout, safe areas, touch reachability. Mobile parity is a pillar, so this is not optional polish. | Now — [HUD_AND_UI_SPEC.md](HUD_AND_UI_SPEC.md) exists but is unverified |
| **Animation** | Blocking gameplay timing: startup, active, recovery, and readable poses. **Not** production-quality motion. | M3, first real ability |
| **VFX** | Communicating cause and result inside a bounded budget. Telegraph clarity, not beauty. | M3 |
| **Audio** | A priority hierarchy where critical cues survive with music muted. | M3 |
| **Performance engineering** | Establish a device baseline and read a profiler. Q-014 is unresolved and gates a LOCKED plan. | Before any art work |
| **Level design** | Already demonstrated — the Coliseum acceptance evidence is genuinely strong work. | Done for now |

---

## What defers safely

Do not spend time here during the combat foundation. Each is explicitly out of current scope.

Systems and economy design · data and backend · analytics · monetization · live operations and community · narrative and worldbuilding · publishing, localization, and marketing · character modeling and rigging (until the rig-style question Q-007 is answered) · technical art · lighting and camera presentation beyond basic readability.

---

## What will eventually need someone else

Ranked by how likely it is to become a real bottleneck.

| Need | Why it outruns a solo developer | Cheapest first step |
|---|---|---|
| **Combat animation** | High-quality fighting animation is a specialist craft measured in years, and a 12-fighter roadmap multiplies it. The playbook's own trigger is "high-quality combat animation is a proven product bottleneck." | Prove combat with placeholders. Only then price one polished ability, and use that number to decide buy versus commission. |
| **Character modeling and rigging** | Original, performant, correctly proportioned rigs, with identity-sensitive likeness constraints on top. | Answer Q-007 first. A rig decision made after animations exist is expensive. |
| **Audio** | Original composition, mixing, and rights are three separate skills. | Assess licensed libraries against the provenance rules before considering commissions. |
| **VFX at scale** | 12 fighters times four abilities plus Breakthroughs is a content pipeline, not a task. | Build 3–4 reusable effect families instead of bespoke effects. |
| **Playtesters** | You cannot observe your own game uncoached, and Scope B's gate requires three uninstructed testers. | Q-015: a small invitation-only group. Costs nothing but organization, and it gates the M3 exit. |

**Deliberate non-recommendation:** do not hire, commission, or buy anything before the M4 gate. Spending on content for an unproven loop is the most common way small projects die, and it directly contradicts operating principle 1 — "Prove the player experience before scaling content."

---

## Commission brief format

When you do commission work, a brief with these fields prevents the two failure modes that matter: an asset you cannot legally ship, and an asset that does not fit the game.

```markdown
## Commission

- Deliverable and exact file formats:
- Technical constraints: rig, poly/tri budget, texture budget, naming, pivot/origin, scale
- Style reference: (own material only -- never another game's assets)
- Gameplay constraints: silhouette readability at gameplay distance, telegraph clarity, viewport
- Revisions included:
- Deadline:
- Price, currency, and whether recurring:
- Rights: commercial use, modification, sublicensing, exclusivity, credit requirement
- Provenance: every third-party element the creator used, with its licence
- Confirmation that no scripts, remotes, packages, or hidden executable content are included
- Acceptance test before payment:
```

Every one of these routes into a row in [ASSET_PROVENANCE_LEDGER.md](ASSET_PROVENANCE_LEDGER.md). Two standing rules apply: **"Treat `unclear` as `HOLD`, not as approval"**, and approval of one item never authorizes another purchase or a renewal.

---

## The capacity risk nobody writes down

60 hours a week is not the constraint. **Attention is.** The evidence is already in this project's own history: six of nine commits went to the arena, which is now over-built relative to combat, while the M1 combat tasks it was meant to unblock went untouched and the only code written sat uncommitted (S7 and S1 in [PROJECT_AUDIT_2026-07-25.md](PROJECT_AUDIT_2026-07-25.md)).

The arena work was good. It was simply not the riskiest assumption, and building it did not answer the question the prototype exists to answer.

Mitigations already available in this repository, all currently unused:

- The **WIP limit of one primary implementation task**.
- The three-question scope test in [AGENTS.md](../AGENTS.md).
- The **risk register**, now populated for the first time in the audit — review it at every milestone boundary.
- Backlog ordering by milestone exit requirement first, cost and attractiveness last.

The single most useful discipline to develop is not on the playbook's list of 24: **noticing when the work in front of you is more attractive than the work that retires risk.**
