# Open Questions

These choices are intentionally unresolved. An LLM must not silently decide them.

An unknown with no ID cannot be tracked or closed. Six live unknowns were previously scattered across other documents without one; they are now Q-016 through Q-023. If you find another, give it the next ID rather than leaving it in prose.

## Required before the full Gravity Sovereign kit

| ID | Question | Recommended starting point | Decision deadline |
|---|---|---|---|
| Q-001 | Exact combat feel: fast/chaotic, heavy/cinematic, or hybrid? | Hybrid: responsive basics and heavier abilities | Before tuning M1 and hitstun |
| Q-002 | Exact third-person camera distance, field of view, lock behavior, and aim assist? | Free third-person camera with soft directional assist; no hard target lock in FFA | Before ability targeting |
| Q-003 | What is Gravity Sovereign's `R` mechanic? | A short force-state modifier, not another full ability | Before Scope B |
| Q-004 | Which four normal abilities form the final kit? | Use the draft in `GRAVITY_SOVEREIGN.md` only as a discussion base | Before Scope B |
| Q-005 | How does Breakthrough replace or empower moves? | Temporary replacement moveset with a clear duration | Before Scope B |
| Q-006 | How much destruction belongs in the first vertical slice? | Four resettable breakable wall panels at most | After universal combat is stable |
| Q-016 | Breakthrough gain rate, duration, cancel rules, and behavior on death? | Broader than Q-005, which covers only how moves are replaced. Decide duration first; it constrains everything else | Before Scope B |
| Q-017 | Gravity Well's numbers: radius, duration, damage, pull strength, cooldown? | All five are currently unset. Fill in a move spec before implementing | Before implementing the ability |

`docs/DESIGN_PHILOSOPHY.md` restates Q-001, Q-002, Q-007, and Q-008 in decidable form. It does not decide them.

## Required before finished art

| ID | Question | Recommended starting point |
|---|---|---|
| Q-007 | Character rig style? | Stylized R15-compatible proportions for animation and avatar familiarity. Also the cheaper animation pipeline; see `docs/TOOLING_AND_PIPELINE.md` |
| Q-008 | Visual art direction? | Exaggerated science-superhero silhouettes with simple materials and strong color coding. Note that D-016 has already committed the arena to a restrained marble/brass/glass palette, so the live question is whether characters match it or contrast with it |
| Q-010 | Final title/logo treatment? | Use the current title internally; run trademark and marketplace-confusion checks before release |
| Q-014 | Minimum supported device and performance budget? | **Moved here from "before public alpha."** Step 2 of the LOCKED post-M4 art pipeline depends on it, so its real deadline is before any art work, not before alpha. The arena already has measurements (2,909 instances, 74,238 triangles, 25 draw calls) and no budget to compare them against. Cheap to close: pick one representative low-end device and record the numbers |
| Q-018 | Which Prague Astronomical Clock restoration era does the exhibit represent? | Lock it before modeling; the clock's appearance differs materially by era |
| Q-021 | Does a named MARIE CURIE statue conflict with the Radiant Pioneer identifiability rule? | Raised as S4 in `docs/PROJECT_AUDIT_2026-07-25.md`. A named Curie monument in the arena where a radiation-and-decay "original" character fights invites exactly the association the roster rule exists to prevent, and it fails this project's own five-unprompted-testers test. Options: substitute another figure, drop the statue, or retheme Radiant Pioneer |

## Resolved questions

| ID | Resolution | Decision |
|---|---|---|
| Q-009 | RESOLVED by D-013 and refined by D-014 and D-015 on 2026-07-23 | The first arena is **The Omniscience Coliseum**, a monumental Greco-Roman science coliseum with an approximately 759-stud contained combat disc and 5× physical exhibits distributed across its interior. |
| Q-019 | RESOLVED by D-021 on 2026-07-25 | Sprint is `LeftShift`/`RightShift` held, with a `SprintButton` touch control, and is a movement modifier rather than a combat state. Assigned an ID retroactively because the code had already decided it without a record. |

## Required before public alpha

| ID | Question | Recommended starting point |
|---|---|---|
| Q-011 | Persistence model for mastery and cosmetics? | Save only stable versioned profile data; no combat power |
| Q-012 | First paid offer and exact Robux price? | One cosmetic Founder Pack after retention evidence |
| Q-013 | Content maturity label and questionnaire answers? | Reassess the finished combat and every uploaded asset before publishing |
| Q-015 | Test community and moderation process? | Small invitation-only group before public discovery. Gates the M3 exit condition, which needs three uninstructed testers, so it is nearer than "before public alpha" suggests |
| Q-020 | What are the public-alpha metric targets? | Cannot be set until closed-test baselines exist. Do not invent numbers before then |
| Q-022 | May the name "Isaac Newton" appear in player-facing text? | `docs/GRAVITY_SOVEREIGN.md` permits it "only after the project completes its clearance record." Until then, select-screen titles only |
| Q-023 | Does AI-agent sign-off satisfy the ledger's "named reviewer" requirement for rights decisions? | Raised as S16 in `docs/PROJECT_AUDIT_2026-07-25.md`: the single existing ledger row records "Codex" as its reviewer. Recommended answer is no — an agent may prepare a provenance row, but a human names themselves on it |

## Not questions for the current milestone

Do not spend prototype time deciding:

- The kits of fighters four through twelve.
- Ranked tiers.
- A second map.
- Trading or an economy.
- Seasonal content.
- Story lore.
- Tournament rules.
