# Roblox Game Development Playbook

**Status:** operating reference for human developers and AI agents

**Applies to:** planning, new systems, milestone changes, and cross-discipline production work

**Source review date:** 2026-07-23

## Purpose

This playbook describes how to take a Roblox game from an idea to a maintained live product. It is a decision and execution framework, not a promise that one person must become an expert in every discipline before building.

Use it to:

- identify which development discipline owns a problem;
- choose the next smallest piece of evidence needed;
- order work by player value and project risk;
- define acceptance before implementation;
- test on the actual client-server and device conditions Roblox uses;
- know when a solo developer should simplify, defer, or seek specialist help; and
- give agents a repeatable, auditable operating process.

Project-specific sources remain authoritative. For **Theory of Everything: Unleashed**, read the [Project Brief](PROJECT_BRIEF.md), [MVP Scope](MVP_SCOPE.md), [Decision Log](DECISION_LOG.md), relevant domain document, and [task board](../TASKS.md) before applying this general playbook.

## Operating principles

1. **Prove the player experience before scaling content.** A prototype answers a question; it is not a smaller production build.
2. **Start with the riskiest assumption.** Test uncertain fun, feasibility, networking, device performance, or content cost before polishing safe work.
3. **Make the smallest usable vertical change.** Prefer one complete interaction over several disconnected systems.
4. **Advance through evidence gates.** Time spent, code written, or visual polish does not satisfy an acceptance condition.
5. **Design for Roblox's real environment.** Treat multiplayer, mobile input, variable devices, streaming, moderation, and live updates as product constraints.
6. **The server decides consequential results.** A client may request and predict presentation; it must not award damage, currency, progression, or other authority.
7. **Measure before optimizing or expanding.** Capture a baseline, reproduce the problem, change one meaningful variable, and compare.
8. **Keep work recoverable.** Use source history, place version notes, asset provenance, migration plans, rollback paths, and small commits.
9. **Clarity beats ceremony.** Documents and meetings exist to make decisions, expose risk, and coordinate work.
10. **Protect players and the product.** Safety, accessibility, privacy, honest monetization, and IP provenance are design requirements.

## Competency map

No single contributor needs production-level mastery of every row. The minimum competency is the ability to make safe prototype decisions, recognize a failing quality gate, and escalate work beyond one's expertise.

| Discipline | Owns and produces | Minimum working competency | Evidence and quality gate | Simplify, defer, or seek help when |
|---|---|---|---|---|
| Product direction | Audience, player promise, pillars, commercial goal, constraints, success and stop signals | Can describe who the game serves, why they return, and what is deliberately excluded | A one-sentence promise, bounded scope, measurable gate, and aligned decision log | The audience or business model is unclear, or stakeholders disagree on the product |
| Production and project management | Milestones, backlog order, dependencies, capacity, risks, communication, release coordination | Can turn a goal into small acceptance-tested work and keep one source of truth | Current milestone has an exit condition; blockers and owners are visible; work-in-progress is limited | Dependencies, outsourcing, dates, or team coordination exceed what one person can track reliably |
| Game design | Rules, goals, challenge, feedback, pacing, failure, rewards, player agency | Can state a core loop and test whether choices are understandable and enjoyable | Uncoached players perform the intended loop and can explain important outcomes | The feature needs extensive content to reveal whether the basic interaction is fun |
| Systems and economy design | Progression, resources, sinks, sources, balance, rewards, pricing relationships | Can model inputs/outputs, identify exploits and runaway growth, and tune from data | The economy has explicit invariants, simulation cases, telemetry, and recovery from bad values | Real-money value, trading, paid randomness, or irreversible migrations are involved |
| Level and encounter design | Spatial flow, landmarks, routes, sightlines, pacing, spawn safety, difficulty | Can graybox to target traversal, readability, and encounter timing | Representative players navigate, understand goals, and avoid unintended traps or dominant positions | Layout depends on final art to be understood, or competitive geometry cannot be balanced internally |
| UX, UI, input, and accessibility | Information hierarchy, controls, onboarding, navigation, feedback, safe areas, readable interaction | Can design mobile-first layouts, support relevant input methods, and minimize cognitive load | Required actions are reachable and legible across target viewports; players understand feedback without coaching | Accessibility needs, localization layouts, or complex interaction research exceed internal validation |
| Gameplay and Luau engineering | Runtime behavior, modules, state, configuration, cleanup, debugging, maintainability | Can write strict, focused, event-driven Luau with explicit responsibilities and lifecycle cleanup | Static analysis passes; behavior is reproducible; failure paths clean up; tests cover boundaries | A framework or abstraction is being added without a demonstrated recurring need |
| Networking and security | Authority, replication, remotes, validation, rate limits, exploit resistance, network ownership | Understands that all client input is untrusted and can validate type, context, rate, range, and state | Adversarial requests fail safely; two-client and degraded-network tests preserve authoritative state | Security affects purchases, persistent value, trading, or broad arbitrary Instance/data mutation |
| Data and backend systems | Schemas, persistence, session state, migrations, retries, budgets, deletion, disaster recovery | Can separate session and persistent data and design idempotent, versioned writes | Load/save failure is safe; migrations are reversible or recoverable; production data is isolated from tests | Valuable player data, cross-server coordination, or compliance deletion enters scope |
| Tools and build pipeline | Studio/IDE ownership, synchronization, automation, asset pipeline, packages, CI, release tooling | Can preserve a clear source of truth and automate repeatable high-risk checks | A clean checkout and documented Studio state can reproduce the build; generated output is controlled | Tooling costs more than the repeated task or introduces a second conflicting source of truth |
| Quality assurance | Test strategy, cases, reproduction, severity, regressions, compatibility, exploratory testing | Can test from cheapest to most representative and write a minimal reliable reproduction | Acceptance matrix passes; P0/P1 defects are absent; regressions have recorded coverage | Specialized device labs, accessibility audits, security testing, or large-scale concurrency is required |
| Performance engineering | Frame time, memory, load time, server health, physics, rendering, network cost | Can establish device and player-count baselines and use Roblox profiling tools to find root cause | Measured budgets pass on a representative low-end device and target server load without sustained spikes | Profiling identifies engine, asset, or platform behavior outside the team's expertise |
| Environment and 3D art | Modular kits, props, terrain, materials, composition, optimization, world readability | Can move from graybox metrics to reusable assets without breaking gameplay silhouettes | Art preserves navigation and combat readability and stays inside geometry, texture, memory, and draw budgets | Bespoke high-detail assets consume time before the experience gate passes |
| Character modeling and rigging | Silhouette, topology, UVs, skinning, rigs, avatar compatibility, deformation | Can create or integrate an original, performant, correctly scaled and rigged character | Animations deform correctly on target rigs; silhouette and hit readability survive gameplay cameras | Custom faces, complex cloth/hair, advanced deformation, or identity-sensitive likeness work is required |
| Technical art | Shaders/materials, asset constraints, procedural workflows, art-engine bridge, optimization | Can define budgets and reusable setups that let art scale safely | Assets import predictably, render consistently across quality levels, and expose controllable parameters | Visual targets depend on unsupported features or costly one-off pipelines |
| Animation | Movement, combat timing, anticipation, impact, transitions, rig constraints | Can block timing for gameplay first and separate simulation timing from presentation | Actions remain readable from gameplay distance; transitions do not create stuck or misleading states | High-quality combat, facial, motion-capture, or complex rig work is a proven product bottleneck |
| Visual effects | Telegraphs, hits, states, environment effects, scalability, cleanup | Can communicate cause and result with bounded, non-blocking client presentation | Effects are readable, performant, color-safe where practical, and never decide gameplay | Effects obscure targets, overwhelm mobile GPUs, or require specialist simulation/content tools |
| Lighting and camera presentation | Mood, visibility, focus, contrast, post-processing, gameplay camera behavior | Can prioritize target visibility and navigation over cinematic composition | Important actors and hazards remain readable across graphics levels and camera conditions | Desired mood conflicts with competitive readability or accessibility |
| Audio | Feedback, ambience, music, mixing, spatial sound, loudness, licensing | Can create a priority hierarchy and make critical actions distinguishable without visuals | Important cues are clear at normal volume, do not clip, and have documented rights | Original composition, voice acting, advanced mixing, or accessibility alternatives need expertise |
| Narrative and worldbuilding | Theme, character voice, lore, quests, environmental storytelling, continuity | Can support the player fantasy without blocking the core loop or over-scoping content | Narrative is internally consistent, original, skippable where appropriate, and understood in play | Branching content or cinematic scope outruns production capacity |
| Analytics and experimentation | Event schema, funnels, cohorts, dashboards, experiments, interpretation | Can connect each event to a decision and distinguish directional samples from reliable evidence | Events are versioned, bounded, privacy-safe, and validated before decisions depend on them | Experiment size, causal inference, or data engineering exceeds the available sample and expertise |
| Monetization | Offers, value, storefront UX, receipts, policy eligibility, economy effects | Can design transparent, optional value without damaging fairness or first-session fun | Purchases are idempotent, clearly described, policy-compliant, and tested under failure/retry | Paid randomness, trading, regional restrictions, subscriptions, or valuable entitlements enter scope |
| Live operations and community | Update cadence, events, communication, moderation response, feedback loops | Can sustain updates by reusing proven systems and separating permanent content from events | Update workload is sustainable; goals, communication, monitoring, rollback, and retrospective exist | Cadence requires chronic overtime or community scale exceeds available moderation capacity |
| Safety, moderation, and privacy | Content maturity, text filtering, abuse controls, reports, policy checks, personal data | Can identify user-generated or social surfaces and apply Roblox safety services correctly | Questionnaire is accurate; text/UGC is controlled; abuse paths and data collection are minimized | Novel UGC, voice/social mechanics, regulated data, or ambiguous content requires specialist/legal review |
| IP, legal, and provenance | Ownership, licenses, permissions, trademarks, likeness, records, attribution | Can trace every external asset and avoid copying protected expression or implying endorsement | Asset ledger is complete and every shipped item has approved commercial-use status | Rights, identity, jurisdiction, or commercial conflicts are material or unclear |
| Publishing, localization, and marketing | Metadata, icons, thumbnails, discovery, translations, release notes, audience communication | Can present the real experience accurately and prepare recoverable releases | Store page matches gameplay; key text localizes safely; release has notes, owner, monitoring, and rollback | Paid acquisition begins before retention evidence or claims/assets lack clearance |

## Evidence-gated development lifecycle

Development is iterative. A later stage can expose a false assumption and send the project back to an earlier stage. The order below prevents expensive production from hiding an unproven game.

| Stage | Question to answer | Minimum outputs | Exit evidence |
|---|---|---|---|
| 1. Player and business problem | What player need or fantasy is served, and why should this product exist? | Problem statement, business constraint, success and stop signals | The team can reject attractive ideas that do not serve the stated problem |
| 2. Audience, platform, and constraints | Who plays, on what devices, for how long, with what team/budget/policy limits? | Target audience, session shape, supported inputs/devices, capacity and content boundary | The proposed game is feasible inside the real constraints |
| 3. Player promise and core-loop hypothesis | What repeatable action creates the intended feeling and reason to continue? | One-sentence promise, loop diagram, key decisions, expected feedback and reward | A low-cost test can isolate the loop's riskiest claim |
| 4. Genre and competitor research | What conventions help comprehension, and where is the product distinct? | Comparable products, convention/differentiation notes, IP-safe reference ledger | The product is understandable without being a clone |
| 5. Risk identification | Which unknown could invalidate fun, feasibility, safety, cost, or market fit? | Ranked risk register with probability, impact, test, owner, and trigger | The next prototype targets the highest combined risk |
| 6. Paper and Studio prototypes | Does the interaction work before production quality exists? | Disposable prototype, observation plan, acceptance threshold | The hypothesis passes repeated playtests or is revised/rejected |
| 7. Technical foundation and graybox | Can the core interaction run safely on Roblox's client-server model and target devices? | Graybox, minimal architecture, input path, server boundary, baseline profile | Solo, multiplayer, device, security, and performance checks meet the prototype gate |
| 8. Vertical slice | Can one representative path reach intended near-production quality end to end? | One complete content slice with representative code, art, audio, UI, and operations | The slice proves the quality bar and exposes a repeatable cost/pipeline |
| 9. Production and reusable content pipeline | Can the proven experience be produced repeatedly within budget? | Ordered backlog, asset templates, packages, definitions, naming/budgets, content calendar | A second content unit is cheaper and safer because the pipeline is reusable |
| 10. Closed testing and iteration | Do uncoached target players understand, enjoy, and repeat the loop under real conditions? | Private builds, observations, defect list, metrics, decisions and retests | Player-behavior thresholds pass and no known release-blocking issue remains |
| 11. Release readiness | Can the product launch safely, accurately, observably, and recoverably? | Compliance review, metadata, analytics validation, performance baseline, release and rollback plans | Go/no-go checklist has an owner and evidence for every required item |
| 12. Launch, analytics, LiveOps, and retrospectives | What happened, why, and what is the smallest valuable response? | Monitored release, incident response, player communication, review, reordered backlog | Decisions use observed behavior; updates remain sustainable and recoverable |

## Planning and management system

### Sources of truth

Maintain one authoritative location for each kind of information:

- **Product goal and constraints:** brief and decision log.
- **Current execution:** ordered task board or backlog.
- **System behavior:** domain design and architecture documents.
- **Runtime truth:** the current tested build and its logs.
- **Code truth:** version-controlled source.
- **Place and asset truth:** Studio/cloud versions with notes and provenance.
- **Unknowns:** risk register and open-questions list.

When sources conflict, stop. Resolve the conflict before implementation rather than choosing the most convenient version.

### Solo-developer cadence

- **At the start of a work block:** select one primary acceptance target, confirm dependencies, and define the cheapest valid test.
- **During work:** keep a WIP limit of one primary implementation task. Small diagnostics or unblockers may support it but must not become hidden parallel features.
- **At the end of a work block:** run the relevant test, record evidence, commit a coherent checkpoint, and name the next smallest task.
- **At least weekly or at a milestone boundary:** play the current build, inspect risks and metrics, reorder the backlog, remove unnecessary scope, and record one process improvement.
- **At a release boundary:** freeze unrelated changes, validate the candidate, save with version notes, publish deliberately, monitor, and retain a known rollback version.

Use the useful parts of iterative methods: one product goal, a transparent ordered backlog, a testable increment, review, and retrospective. Do not create meetings or estimates that provide no decision value.

### Backlog ordering

Order work using:

1. milestone exit requirements;
2. player-facing value;
3. risk retired or evidence gained;
4. dependencies unblocked;
5. severity of defects;
6. implementation and content cost;
7. reversibility.

Cosmetic polish does not outrank a broken core loop, unsafe remote, stuck lifecycle, inaccessible control, or missing rollback.

## Work item templates

### Feature brief

```markdown
## Feature

- Player problem:
- Intended player behavior:
- Why now / milestone link:
- In scope:
- Out of scope:
- Dependencies:
- Primary risks:
- Interfaces or data affected:
- Acceptance conditions:
- Cheapest test:
- Representative test:
- Performance/security/accessibility/safety checks:
- Rollback or disable path:
- Documentation and analytics impact:
```

### Definition of Ready

A work item is ready only when:

- it supports the current milestone or an explicitly approved scope change;
- the player outcome and acceptance condition are observable;
- important dependencies and source-of-truth conflicts are resolved;
- OPEN or DRAFT decisions required for implementation have explicit approval;
- security, data, device, content, and asset-provenance implications are known;
- a smaller prototype cannot answer the same question more cheaply; and
- the first relevant test can be named before coding begins.

### Definition of Done

A work item is done only when:

- the acceptance behavior exists in the intended runtime context;
- focused static checks and the cheapest relevant runtime test pass;
- multiplayer, mobile, degraded-network, persistence, or scale tests run when the change affects them;
- failure, interruption, cleanup, respawn/rejoin, and retry paths are tested where applicable;
- no known P0/P1 defect is introduced or hidden;
- performance and memory are measured when the feature can affect them;
- security, accessibility, content safety, and provenance are reviewed in proportion to risk;
- documentation, decision records, and task state match reality;
- the place/build is saved with a meaningful version note when Studio changed;
- the source change is reviewed and committed as one coherent checkpoint; and
- the handoff reports evidence, remaining risk, and the next smallest task.

"Implemented" is not synonymous with "done."

### Risk register

```markdown
| Risk | Category | Probability | Impact | Earliest cheap test | Mitigation | Trigger / owner | Status |
|---|---|---:|---:|---|---|---|---|
```

Review risks before choosing the next prototype and at every milestone gate. Retire a risk only with evidence.

### Playtest note

Canonical template: [templates/PLAYTEST_NOTE.md](templates/PLAYTEST_NOTE.md).

Ask players to demonstrate and explain. Do not replace observation with leading questions about whether the concept "could be good."

### Other templates

- Move, ability, or mechanic design: [templates/MOVE_SPEC.md](templates/MOVE_SPEC.md).
- End-of-session handoff: [templates/SESSION_HANDOFF.md](templates/SESSION_HANDOFF.md).

### Release and rollback record

```markdown
## Release

- Version and date:
- Goal and included changes:
- Excluded changes:
- Validation evidence:
- Analytics/health signals:
- Content and policy review:
- Known risks:
- Release owner:
- Rollback version:
- Disable/mitigation path:
- Monitoring window:
- Result and retrospective:
```

For persistent data, document schema versions, migration behavior, retry/idempotency, backup/export options, and how old servers or clients behave during rollout.

## Agent execution loop

Agents use the following loop for every substantial task:

1. **Read:** load `AGENTS.md`, required core documents, the active task, and relevant domain sources in full.
2. **Inspect:** examine repository and Studio/runtime truth. Do not ask the user for discoverable facts.
3. **Reconcile:** identify conflicts, dirty user work, OPEN decisions, missing authority, and out-of-scope requests.
4. **State the target:** name the player behavior, boundaries, acceptance evidence, and tests.
5. **Choose the smallest change:** avoid speculative frameworks, unrelated cleanup, future content, and premature final art.
6. **Implement safely:** preserve existing work, respect client/server ownership, keep responsibilities explicit, and make changes recoverable.
7. **Verify progressively:** static/pure checks, solo runtime, server and clients, device emulation, network conditions, scale, then external playtest as applicable.
8. **Review cross-cutting risks:** security, cleanup, performance, accessibility, safety, IP/provenance, analytics, and rollback.
9. **Synchronize truth:** update tasks only after acceptance passes; update decisions and domain docs when behavior changes.
10. **Checkpoint and hand off:** save Studio with notes, review the diff, commit focused source, and report evidence, risks, and the next task.

Agents must not:

- silently turn an OPEN or DRAFT item into a requirement;
- claim a Studio, device, multiplayer, or external test they did not run;
- add content outside the active milestone because it is easy or visually attractive;
- trust client-declared results or arbitrary Instance/data references;
- overwrite user work, delete conflicting objects, or publish externally without authority;
- optimize from intuition when a profiler or baseline can identify the actual bottleneck; or
- mark a task complete when only implementation, not acceptance, is complete.

## Test strategy

### Cheapest-to-most-representative ladder

1. Pure functions, type/static analysis, and deterministic module checks.
2. Focused Studio `Run` or solo play.
3. Local server with two clients.
4. Device emulation and touch simulation.
5. Network simulation with latency, jitter, packet loss, duplicate/reordered requests where relevant.
6. Target-scale server test.
7. Representative physical lower-end device profile.
8. Small uncoached private playtest.
9. Staged/private release with monitoring.

An earlier failure blocks later confidence. A later test does not erase missing focused coverage.

### Cross-cutting test matrix

| Area | Required questions |
|---|---|
| Player comprehension | Can an uncoached player identify the goal, available action, result, and next decision? |
| Input and UI | Are all required actions reachable, readable, and non-overlapping across target input methods, aspect ratios, safe areas, and text lengths? |
| Lifecycle | What happens on spawn, reset, death, respawn, leave/rejoin, interruption, cancellation, and character replacement? |
| Networking | Are requests validated for type, finite values, context, state, rate, sequence, range, ownership, and authority? |
| Persistence | Do load failure, save failure, retry, duplicate receipt, old schema, deletion request, and concurrent server cases preserve data integrity? |
| Performance | What are client/server frame time, memory, load time, physics, rendering, replication, and instance trends at target scale? |
| Accessibility | Can critical information be understood without depending only on color, tiny text, precise tapping, sound, or rapid reading? |
| Safety and privacy | Are text/UGC filtered, abuse paths bounded, maturity answers accurate, personal data minimized, and policy eligibility checked? |
| Content and IP | Is every asset original or traceably licensed, and does marketing avoid copying or false endorsement? |
| Operations | Can the feature be disabled, rolled back, monitored, and explained to players without corrupting state? |

## Genre-risk matrix

Genre labels do not replace observation. Use the row that matches the dominant loop, then add risks from any secondary genre.

| Genre family | Prove first | Dominant production and technical risks | Representative acceptance evidence |
|---|---|---|---|
| Fighting, battleground, shooter, action | Input-to-feedback feel, readable cause/effect, counterplay, re-engagement | Latency, authority, hit validation, state locks, camera/VFX clutter, spawn pressure, animation cost, mobile controls | Two clients repeat attack/defend/KO loops; players explain why outcomes occurred; target-scale combat stays readable |
| Obby, platformer, racing, sports | Control precision, camera, fair collision/physics, recovery pace | Device/input variance, network ownership, checkpoint integrity, timing fairness, exploit shortcuts, level difficulty | Players complete representative routes consistently across devices; failures feel attributable and recovery is fast |
| RPG, simulator, tycoon, incremental | Satisfying short loop and meaningful progression choices | Economy inflation, persistence loss, exploit duplication, content burden, grind, opaque monetization, update treadmill | New players understand the loop; progression simulations remain bounded; save/rejoin and purchase retries preserve value |
| Strategy, tower defense, card, puzzle | Rule clarity, decision depth, readable state, fair difficulty | Determinism, large state replication, balance combinatorics, pathfinding, AI cost, tutorial burden, stale dominant strategies | Players predict consequences, recover from mistakes, and complete cases without hidden rules or state divergence |
| Horror, narrative, adventure | Pacing, curiosity, navigation, atmosphere, emotional safety | One-use content cost, scripting brittleness, spoiler-sensitive testing, lighting readability, checkpoint/save branches, maturity limits | Players progress without coaching, understand objectives, and experience intended beats without technical dead ends |
| Social, roleplay, sandbox, building, UGC | Safe social value, expressive tools, creation-to-sharing loop | Moderation, text/voice/UGC abuse, permissions, ownership, persistence scale, streaming, discovery, griefing, privacy | Players create/share safely; abusive inputs are bounded; permissions and recovery prevent griefing or irreversible loss |

### Adapting to any other genre

For an unlisted or hybrid genre, answer:

1. What actions form the shortest satisfying core loop?
2. What is the expected session length and time to first meaningful action?
3. Is the important state local, server-authoritative multiplayer, cross-server, or persistent?
4. What progression or reward makes repetition meaningful?
5. How much bespoke content is consumed per minute of play?
6. What player failure is most costly: unfairness, confusion, boredom, lost progress, social harm, or technical interruption?
7. Which platform constraint is dominant: input, device performance, networking, moderation, localization, or discoverability?
8. What is the cheapest prototype that could disprove the idea?
9. Which single metric and observation together determine whether to continue?

Use those answers to select prototypes, architecture, team skills, budgets, and quality gates. Do not inherit another genre's feature list without inheriting its production cost and failure modes.

## Roblox-specific engineering and production rules

- Organize the DataModel intentionally and document ownership between Studio, local source, packages, and cloud assets.
- Treat Roblox as multiplayer by default. Keep consequential state on the server and validate every client-triggered action.
- Prefer asynchronous one-way remotes for requests/events; use yielding calls only when the caller truly needs a response and failure is bounded.
- Use event-driven code and bounded work. Avoid unnecessary per-frame loops, uncontrolled Instance growth, and leaked connections/tasks.
- Establish a representative lower-end mobile device and target player count early. Device emulation checks layout and input but does not replace profiling on hardware.
- Profile frame time, memory, load time, server health, rendering, physics, and scripts before choosing an optimization.
- Use reusable packages and asset kits once repeated content is proven; do not turn disposable prototypes into heavy pipelines prematurely.
- Keep Studio tests isolated from live persistent data. Add versioned schemas and migrations before persistence becomes valuable.
- Save and publish with meaningful version notes so place checkpoints can be searched and restored.
- Keep offers transparent and optional. Confirm receipt processing, entitlement persistence, regional/policy eligibility, and retry behavior.
- Filter text, constrain UGC, minimize personal data, maintain accurate content maturity information, and monitor abuse surfaces.
- Build onboarding around immediate action, contextual feedback, and observation; avoid front-loading text players must memorize.
- Use analytics to answer named decisions. Avoid high-volume events that have no owner, threshold, or planned response.
- Plan LiveOps only after the core loop and production pipeline are sustainable.

## Application to Theory of Everything: Unleashed

This section applies the playbook without changing any LOCKED direction or current task.

### Current lifecycle position

- **Product and audience:** established in the [Project Brief](PROJECT_BRIEF.md).
- **Scope:** Scope A combat foundation in the [MVP Scope](MVP_SCOPE.md).
- **Current stage:** technical foundation and graybox, moving toward the first combat vertical slice.
- **Current milestone:** M1 movement and combat states in [TASKS.md](../TASKS.md).
- **Highest current product risks:** input feel, mobile reachability, state correctness, lifecycle cleanup, and whether basic combat creates voluntary re-engagement.
- **Deferred production:** final art, full roster, persistence, monetization, public release, and LiveOps.

### Project-specific operating order

1. Complete one unchecked M1 task at a time.
2. State its acceptance behavior before editing.
3. Preserve the architecture and server-authority rules in [Technical Architecture](TECHNICAL_ARCHITECTURE.md).
4. Use the test ladder in [Roadmap and Testing](ROADMAP_AND_TESTING.md).
5. Do not begin other fighters or production art while the universal loop remains unproven.
6. Check a task only after its acceptance evidence exists.
7. Use playtest evidence to tune DEFAULT values; obtain approval before changing LOCKED decisions.
8. At the Scope A gate, decide whether to iterate, continue, or stop based on player behavior and defect evidence.

Input mapping is now implemented and committed, with acceptance still pending Studio verification. The next task is the shared combat state machine, which consumes `CombatTypes.STATE_PRIORITY` and should be written as pure functions so its transition table can be unit tested without the engine.

The competency map above is generic. For which of its rows this project's solo developer must personally hold, defer, or eventually buy, see [TEAM_AND_SKILLS.md](TEAM_AND_SKILLS.md). For the current findings and the populated risk register, see [PROJECT_AUDIT_2026-07-25.md](PROJECT_AUDIT_2026-07-25.md).

## Release readiness checklist

Before any public release:

- [ ] The current scope and player promise are accurately represented.
- [ ] Core loop and onboarding pass uncoached target-player tests.
- [ ] Required keyboard/mouse, touch, and other supported inputs pass.
- [ ] Target player-count, device, network, lifecycle, and exploit tests pass.
- [ ] Performance baseline meets documented budgets on representative hardware.
- [ ] Persistent data, purchases, receipts, migrations, and rollback are tested if present.
- [ ] Analytics events and health signals are validated.
- [ ] Safety, moderation, privacy, policy eligibility, and maturity information are accurate.
- [ ] Every asset and dependency has approved provenance.
- [ ] Store metadata, icon, thumbnails, descriptions, and localized text match the product.
- [ ] Version notes, rollback version, disable path, monitoring owner, and incident response exist.
- [ ] No known P0 or P1 issue remains.
- [ ] The release decision and known risks are recorded.

## Primary references

The practices above synthesize and adapt these sources; they do not reproduce them.

### Roblox Creator Hub

- [Design games on Roblox](https://create.roblox.com/docs/production/game-design)
- [Design for Roblox](https://create.roblox.com/docs/production/game-design/design-for-roblox)
- [Prototyping](https://create.roblox.com/docs/production/game-design/prototyping)
- [UI and UX design](https://create.roblox.com/docs/production/game-design/ui-ux-design)
- [Onboarding techniques](https://create.roblox.com/docs/production/game-design/onboarding-techniques)
- [Projects](https://create.roblox.com/docs/projects)
- [Collaboration](https://create.roblox.com/docs/projects/collaboration)
- [Packages](https://create.roblox.com/docs/projects/assets/packages)
- [Version History](https://create.roblox.com/docs/projects/version-history)
- [Client-server runtime](https://create.roblox.com/docs/projects/client-server)
- [Remote events and callbacks](https://create.roblox.com/docs/scripting/events/remote)
- [Securing the client-server boundary](https://create.roblox.com/docs/scripting/security/client-server-boundary)
- [Data stores](https://create.roblox.com/docs/cloud-services/data-stores)
- [Studio testing modes](https://create.roblox.com/docs/studio/testing-modes)
- [Performance optimization](https://create.roblox.com/docs/performance-optimization)
- [Design for performance](https://create.roblox.com/docs/performance-optimization/design)
- [MicroProfiler](https://create.roblox.com/docs/performance-optimization/microprofiler)
- [Analytics](https://create.roblox.com/docs/production/analytics)
- [Retention](https://create.roblox.com/docs/production/analytics/retention)
- [Monetization](https://create.roblox.com/docs/production/monetization)
- [LiveOps essentials](https://create.roblox.com/docs/production/game-design/liveops-essentials)
- [LiveOps planning](https://create.roblox.com/docs/production/game-design/liveops-planning)
- [Content updates](https://create.roblox.com/docs/production/game-design/content-updates)
- [Localization](https://create.roblox.com/docs/production/localization)
- [Safety](https://create.roblox.com/docs/safety)
- [Content maturity and compliance](https://create.roblox.com/docs/production/promotion/content-maturity)
- [3D art in Roblox](https://create.roblox.com/docs/art)

### Production framework

- [The 2020 Scrum Guide](https://scrumguides.org/scrum-guide.html), used only for its product-goal, ordered-backlog, inspect/adapt, and Definition-of-Done concepts.
- [International Game Developers Association](https://igda.org/), used as a cross-discipline industry reference.

These sources can change. Recheck current Roblox documentation and policy before implementing publishing, monetization, privacy, safety, platform, or API-sensitive work.
