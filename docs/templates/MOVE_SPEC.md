# Move Spec — template

Copy into `docs/moves/<fighter-id>-<move-name>.md` before implementing any attack, ability, character mechanic, or Breakthrough.

**Why before, not after.** A move spec is the cheapest place to discover that an ability has no counterplay, no readable telegraph, or no mobile input. Filling it in takes minutes; finding those problems in Studio takes a session.

**Do not implement a move whose spec has an unanswered required field.** Per the Definition of Ready, an OPEN or DRAFT decision needed for implementation must have explicit approval first.

---

```markdown
## <Move name>

- Fighter:
- Slot: M1 chain step / Ability 1-4 / R mechanic / Breakthrough / Final Proof
- Status: DRAFT | LOCKED
- Approved by, and when:

### Identity

- Scientific phenomenon:
- What it does to bodies in space (pull, push, redirect, slow, reflect, ...):
- One sentence a player would use to describe it:

### Frame data

All values in seconds, and all of them live in shared config -- not in the move's code,
and not derived from an animation length.

| Phase | Duration | Notes |
|---|---:|---|
| Startup (telegraph visible from) | | |
| Active (hitbox live) | | |
| Recovery | | |
| Cancel window opens at | | |
| Cooldown | | |

- Animation markers driving the hitbox:
- Can it be buffered from a previous action?
- What cancels it?

### Effect

- Damage:
- Hitbox shape and size:
- Range / max cast distance:
- Knockback, hitstun, or ragdoll, and for how long:
- End condition for any crowd control:
- Meter gain, if any:

### Counterplay -- at least one, name which

- [ ] Avoidable, by:
- [ ] Blockable: yes / no / reduced
- [ ] Interruptible, during:
- [ ] Punishable, on whiff or block, by:

If only one box is ticked, say why that is acceptable:

### Telegraph and readability

- What the defender sees, and when:
- Is the danger *area* shown, not just the caster?
- Readable at eight-player density on the smallest supported viewport?
- Is it guard-breaking or unblockable? If so, how is it telegraphed more strongly than anything else?

### Presentation

- VFX:
- Sound (must be identifiable with music muted):
- Camera effect, if any -- and confirm it carries no gameplay timing:

### Input

- Keyboard/mouse:
- Touch (not an afterthought -- see HUD_AND_UI_SPEC.md):

### Server validation

Beyond the standard list in TECHNICAL_ARCHITECTURE.md, this move additionally needs:

-

### Cleanup

All four cases are required.

- Normal completion:
- Interruption:
- Death (user's and target's):
- Target removal / disconnect:

### Acceptance

- Cheapest test:
- Two-client test:
- Device test:
- What would make me revert this move:
```

---

## Before marking a move done

Run the consistency checklist in [DESIGN_PHILOSOPHY.md](../DESIGN_PHILOSOPHY.md). A "no" there is a blocker, not a note.

For a fighter's whole kit, the ten-item roster production gate in [CHARACTER_ROSTER.md](../CHARACTER_ROSTER.md) applies on top. Do not begin the next fighter until every item passes.
