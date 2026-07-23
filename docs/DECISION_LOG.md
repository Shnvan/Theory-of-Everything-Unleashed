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
| D-010 | 2026-07-23 | LOCKED | Do not require Rojo for the prototype. | A full file-system-first data model is unnecessary before the project grows. |
| D-011 | 2026-07-23 | LOCKED | Server authority covers damage, cooldowns, KOs, assists, meter, and respawn. | Competitive PvP cannot trust client-declared results. |
| D-012 | 2026-07-23 | LOCKED | Monetization is cosmetic-only and begins after combat validation. | Revenue systems cannot rescue an unfun loop; combat power sales damage fairness. |
| D-013 | 2026-07-23 | LOCKED | The first arena is internally named **The Omniscience Coliseum**, a compact Greco-Roman monument to science and invention. Its M1 version uses static graybox proxies for 24 exhibits and original fighter-title monuments. | Establishes a distinct science-fantasy identity while preserving a readable combat disc and avoiding modern-person likeness or endorsement risk. |
| D-014 | 2026-07-23 | LOCKED | Expand The Omniscience Coliseum to a 240-stud combat disc on a 420×420 foundation, distribute the 24 static exhibits across the interior, and hide exhibit-name labels. Keep exhibits non-colliding and preserve clear traversal lanes. | Direct scale review found the former 137-stud playable area too small. The larger layout creates the intended monumental scale while retaining one contained eight-player arena. This refines the size and exhibit-placement aspects of D-003 and D-013. |
| D-015 | 2026-07-23 | LOCKED | Increase The Omniscience Coliseum to ten times D-014's floor area by scaling the arena uniformly by `√10`, scale all 24 exhibits to five times their D-014 dimensions, make visible exhibit geometry collidable, and add visible plus invisible perimeter containment. | The approved monumental scale requires larger architecture and physical landmarks while preventing players from walking or jumping outside. This supersedes D-014's exact dimensions and non-colliding-exhibit rule while preserving its theme, organization, and hidden exhibit-name labels. |

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
| P-008 | DEFAULT | Ten-area arena clear-lane crossing time estimated at about 53 seconds |

Change defaults through documented playtest evidence without treating the change as a project pivot.

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
