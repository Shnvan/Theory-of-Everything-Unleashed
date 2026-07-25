--!strict

--[[
	Legal combat-state transitions.

	docs/COMBAT_SYSTEM.md fixes the ten states and their priority order but has
	never defined which transitions are legal, only that they must be defined
	"centrally" rather than by letting each move invent its own stun, lock, or
	invulnerability flags. This module is that central definition.

	Pure by construction: no services, no instances, no side effects, no timers.
	Callers pass state in and get a decision out, which is what makes transition
	legality unit testable without the engine and what keeps the module
	replay-safe if combat later moves under `BindToSimulation` (D-020).

	This module decides *whether* a transition is legal. It does not own the
	state itself. Per docs/TECHNICAL_ARCHITECTURE.md the server owns the
	character combat record and applies transitions; the client may never decide
	that it is blocking, invulnerable, awakened, or spawn-protected.

	Durations are deliberately absent. How long a stun lasts is a tunable that
	belongs in `CombatConfig` when something actually reads it, and timers belong
	to the server record, not here.
]]

local CombatTypes = require(script.Parent.Parent.Types.CombatTypes)

type CombatState = CombatTypes.CombatState
type ActionName = CombatTypes.ActionName

--[[
	Why a rejection happened, rather than a bare `false`.

	A caller that knows *why* a transition was refused can answer the "invalid
	action" feedback requirement in docs/DESIGN_PHILOSOPHY.md — silence reads as
	a bug and teaches the player nothing. Tests assert on these too, so a rule
	cannot pass for the wrong reason.
]]
export type TransitionReason = "Allowed" | "SameState" | "DeadIsTerminal" | "BlockEntryForbidden" | "WeakerThanCurrent"

export type TransitionResult = {
	allowed: boolean,
	reason: TransitionReason,
}

local CombatStateMachine = {}

--[[
	The only states a character may begin blocking from.

	docs/COMBAT_SYSTEM.md forbids blocking while stunned, ragdolled, dead, or
	attacking, and is silent about `Dashing`, `UsingAbility`, and `Awakening`.
	This takes the strict reading: committing to a dash or an ability means
	committing to it, so block cannot be used to erase that commitment. Recorded
	as a decision rather than inferred silently, because the document left it
	open.
]]
local BLOCK_ENTRY_STATES: { [CombatState]: boolean } = {
	Neutral = true,
	SpawnProtected = true,
}

--[[
	The state each action drives the character into.

	Central so that action eligibility and transition legality cannot disagree:
	`isActionPermitted` answers by asking `canEnter` about this target, rather
	than maintaining a second hand-written table that could drift.

	`Walk` is absent on purpose. Speed is a movement modifier layered on
	`Neutral`, not a combat state (D-028, superseding D-021), so it drives no
	transition at all.
]]
local ACTION_TARGET_STATE: { [ActionName]: CombatState } = {
	BasicAttack = "Attacking",
	Ability1 = "UsingAbility",
	Ability2 = "UsingAbility",
	Ability3 = "UsingAbility",
	Ability4 = "UsingAbility",
	Block = "Blocking",
	Dash = "Dashing",
	Mechanic = "UsingAbility",
	Breakthrough = "Awakening",
}

-- Frozen after construction, not inline. `table.freeze({...})` returns the type
-- Luau infers from the literal, which discards the annotation above and widens
-- the values back to plain `string`. InputConfig hit the same thing and records
-- the same workaround.
table.freeze(BLOCK_ENTRY_STATES)
table.freeze(ACTION_TARGET_STATE)

CombatStateMachine.BLOCK_ENTRY_STATES = BLOCK_ENTRY_STATES
CombatStateMachine.ACTION_TARGET_STATE = ACTION_TARGET_STATE

--[[
	True when `candidate` may legally replace `current`.

	Rules are ordered, and the order matters: the special cases below cannot be
	expressed by priority alone, so they are checked before falling through to
	it.

	1. A state does not replace itself. This matches `isStrongerThan`, which
	   returns false for equal priority so that re-entry is always a deliberate
	   call. The four-hit chain re-entering `Attacking` per hit is exactly such a
	   call and does not go through here.
	2. Death overrides everything, which is the documented acceptance condition.
	3. `Dead` is otherwise terminal; only respawn leaves it.
	4. Block has an entry gate, above.
	5. `Neutral` is always reachable. It is the universal recovery target —
	   stun expiry, ragdoll recovery, and block release all land here, and any
	   onward transition then follows priority normally. Without this, a
	   character leaving a strong state could never reach a weaker one.
	6. Otherwise priority decides.
]]
function CombatStateMachine.canEnter(current: CombatState, candidate: CombatState): TransitionResult
	if current == candidate then
		return { allowed = false, reason = "SameState" }
	end

	if candidate == "Dead" then
		return { allowed = true, reason = "Allowed" }
	end

	if current == "Dead" then
		if candidate == "SpawnProtected" then
			return { allowed = true, reason = "Allowed" }
		end
		return { allowed = false, reason = "DeadIsTerminal" }
	end

	if candidate == "Blocking" and not BLOCK_ENTRY_STATES[current] then
		return { allowed = false, reason = "BlockEntryForbidden" }
	end

	if candidate == "Neutral" then
		return { allowed = true, reason = "Allowed" }
	end

	if CombatTypes.isStrongerThan(candidate, current) then
		return { allowed = true, reason = "Allowed" }
	end

	return { allowed = false, reason = "WeakerThanCurrent" }
end

--[[
	True when `current` permits the player to request `action`.

	This answers validation item 6 in docs/TECHNICAL_ARCHITECTURE.md, "current
	combat state permits the action". It is a state check only — cooldowns,
	rate limits, range, and target validity are separate checks the server still
	owes.

	Two cases are not derivable from `canEnter`:

	- `Walk` drives no state, so it is permitted whenever the character is
	  alive. A dead character requests nothing.
	- `Dash` while `Ragdolled` is the ragdoll escape, which docs/COMBAT_SYSTEM.md
	  grants explicitly. Priority would otherwise refuse it, since `Dashing` is
	  weaker than `Ragdolled`. Whether the escape charge is available is a
	  cooldown question, not a state question, and is not decided here.
]]
function CombatStateMachine.isActionPermitted(current: CombatState, action: ActionName): boolean
	if current == "Dead" then
		return false
	end

	if action == "Walk" then
		return true
	end

	if current == "Ragdolled" then
		return action == "Dash"
	end

	-- Annotated, not inferred. Indexing the table widens the value back to plain
	-- `string`, which then fails to match the CombatState union at the call
	-- below. Keep the annotation.
	local target: CombatState? = ACTION_TARGET_STATE[action]
	if target == nil then
		return false
	end

	return CombatStateMachine.canEnter(current, target).allowed
end

--[[
	The state to return to when a held action stops being held, or nil when the
	release changes nothing.

	Takes the action rather than the phase deliberately: `End` and `Cancel` must
	resolve identically, so there is no branch where one is handled and the
	other is forgotten. That is the S10 regression — a held touch that never
	produced `InputEnded` latched Block down for the rest of the session — and
	docs/DEVELOPER_RULES.md requires every hold to have a release path that
	fires even when the release event never arrives.

	Returns nil for a non-hold action, and for a hold action whose state the
	character is not actually in, so a stale release cannot yank a character out
	of a state it reached some other way.
]]
function CombatStateMachine.releaseHold(current: CombatState, action: ActionName): CombatState?
	if not CombatTypes.isHoldAction(action) then
		return nil
	end

	local target: CombatState? = ACTION_TARGET_STATE[action]
	if target ~= nil and current == target then
		return "Neutral"
	end

	return nil
end

--[[
	The state a freshly respawned character enters.

	Protection then ends on its timer or when the player begins an attack or
	ability, both of which are ordinary `canEnter` transitions from
	`SpawnProtected`.
]]
function CombatStateMachine.getRespawnState(): CombatState
	return "SpawnProtected"
end

return table.freeze(CombatStateMachine)
