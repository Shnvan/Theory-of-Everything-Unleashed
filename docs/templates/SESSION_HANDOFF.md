# Session Handoff — template

Copy into `docs/handoffs/YYYY-MM-DD-topic.md` at the end of a meaningful work session.

**Why bother.** This is what makes work compound instead of restart. Zero handoff records existed in this project's first nine commits, which is why each session had to re-derive the same context. The Verification section is the important one: it is the difference between "implemented" and "done".

---

```markdown
## Session handoff — YYYY-MM-DD

### Target

- Task (one, from TASKS.md):
- Acceptance condition:

### Completed

- Behavior changed:
- Files changed:
- Commits:

### Verification

State honestly, including what did not run. "Not run" is a valid and useful entry.

- Static checks (stylua, selene, luau-lsp, rojo build):
- Unit tests:
- Studio solo test:
- Server + two clients:
- Device emulation / mobile:
- Eight clients:

### Decisions

- New or changed decisions (with IDs):
- Open questions resolved (with the deciding ID):
- Documents updated:

### Risks and blockers

- Known issue:
- Assumption needing confirmation:
- Anything left in a partial state:

### Next smallest task

- Task:
- Acceptance condition:
```

---

## Rules

- **Never record a test you did not run.** An unrun test written as passed is worse than no record, because it retires a risk that is still live.
- Check a `TASKS.md` box only when the acceptance condition in the Target section actually passed.
- If Studio changed, save and publish the place with a version note and record it here. `*.rbxl` is gitignored, so the cloud version is the only backup that exists.
- Run `git status` before finishing. Untracked work is not saved work.
