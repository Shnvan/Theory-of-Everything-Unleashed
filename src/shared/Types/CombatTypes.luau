--!strict

--[[
	Shared combat vocabulary for Theory of Everything: Unleashed.

	This module exists so the client and the server describe combat with the
	same words. Until now `ActionName`, `InputPhase`, and `ActionInput` were
	declared inside a client controller, which meant the server would have had
	to duplicate them the moment the first remote appeared. The duplication had
	already begun: the client used `Block` plus a phase while
	docs/TECHNICAL_ARCHITECTURE.md described `BlockStart` and `BlockEnd`.

	Types only, plus the state-priority data and the pure predicates over it.
	No services, no instances, no side effects, so every function here is unit
	testable without the engine.

	Behavior source: docs/COMBAT_SYSTEM.md.
	Boundary rules: docs/TECHNICAL_ARCHITECTURE.md.
]]

local CombatTypes = {}

--[[
	Actions a player can request. Ability slots are explicit members rather than
	a generic `Ability` plus a numeric `slot` field, because one union the server
	can check exhaustively is cheaper to validate than a tag plus a range check.
	Use `CombatTypes.getAbilitySlot` when the slot number itself is needed.
]]
export type ActionName =
	"BasicAttack"
	| "Ability1"
	| "Ability2"
	| "Ability3"
	| "Ability4"
	| "Block"
	| "Dash"
	| "Mechanic"
	| "Breakthrough"
	| "Walk"

--[[
	`Begin` on press. `End` on release. `Cancel` when the engine withdraws an
	input the player did not release, such as focus loss mid-hold.

	Only hold actions produce `End` and `Cancel`; see `HOLD_ACTIONS`. A consumer
	that needs press duration must check that its action is a hold action first,
	because a tap action will never report a release.
]]
export type InputPhase = "Begin" | "End" | "Cancel"

--[[
	Client-local description of one input event. Includes fields that are useful
	for local presentation and deliberately never sent to the server:
	`inputType` and `keyCode` are device details the server has no use for, and
	`timestamp` comes from `os.clock()`, a client-monotonic value with an
	arbitrary epoch that cannot be compared against server time.

	`sequence` is the one field that crosses the boundary, because
	docs/TECHNICAL_ARCHITECTURE.md requires the server to reject stale and
	duplicated requests.
]]
export type ActionInput = {
	action: ActionName,
	phase: InputPhase,
	sequence: number,
	movementDirection: Vector3,
	timestamp: number,
	inputType: Enum.UserInputType,
	keyCode: Enum.KeyCode,
}

export type ActionCallback = (actionInput: ActionInput) -> ()

--[[
	The wire shape for a client action request.

	Carries strictly less than `ActionInput`: no device identity, no client
	clock, no local movement vector. `direction` is the normalized aim the
	server may re-normalize, and `targetPosition` is a requested ground point
	the server range-checks. Neither is trusted.

	This is a transport shape, not proof that a request is valid. Every field
	still passes the validation list in docs/TECHNICAL_ARCHITECTURE.md.
]]
export type ActionRequest = {
	sequence: number,
	action: ActionName,
	phase: InputPhase,
	direction: Vector3?,
	targetPosition: Vector3?,
}

--[[
	The single authoritative primary state a character is in. Short supplementary
	flags are allowed only when they cannot contradict this state.

	docs/COMBAT_SYSTEM.md: "Do not let each move invent its own stun, lock, or
	invulnerability flags."
]]
export type CombatState =
	"Neutral"
	| "Attacking"
	| "Blocking"
	| "Dashing"
	| "UsingAbility"
	| "Stunned"
	| "Ragdolled"
	| "Awakening"
	| "Dead"
	| "SpawnProtected"

--[[
	State strength, highest number strongest, matching the ordering in
	docs/COMBAT_SYSTEM.md. Encoded as data so transition rules compare priority
	in one place instead of re-deriving the order at each call site.

	Note that speed is not a state. Sprinting is automatic at full movement
	input and `Walk` is a deliberate slow-down modifier; both layer on
	`Neutral` rather than replacing it, so neither can suppress or be
	suppressed by a combat state. Recorded as D-028, which supersedes D-021.
]]
local STATE_PRIORITY: { [CombatState]: number } = table.freeze({
	Dead = 10,
	Ragdolled = 9,
	Stunned = 8,
	Awakening = 7,
	UsingAbility = 6,
	Dashing = 5,
	Attacking = 4,
	Blocking = 3,
	SpawnProtected = 2,
	Neutral = 1,
})

CombatTypes.STATE_PRIORITY = STATE_PRIORITY

--[[
	Actions that report a release. Every other action emits `Begin` only.
	Kept here rather than in the input layer because the server needs the same
	knowledge to decide whether an unmatched `Begin` is a protocol error.
]]
CombatTypes.HOLD_ACTIONS = table.freeze({
	Block = true,
	Walk = true,
}) :: { [ActionName]: boolean }

CombatTypes.ABILITY_SLOT_BY_ACTION = table.freeze({
	Ability1 = 1,
	Ability2 = 2,
	Ability3 = 3,
	Ability4 = 4,
}) :: { [ActionName]: number }

--[[
	Returns the 1-based ability slot for an ability action, or nil for any other
	action. Lets callers that genuinely need a slot number get one without
	putting a redundant `slot` field on the wire.
]]
function CombatTypes.getAbilitySlot(action: ActionName): number?
	return CombatTypes.ABILITY_SLOT_BY_ACTION[action]
end

--[[
	True when `candidate` may override `current`. Equal priority returns false:
	a state does not replace itself, so re-entering a state is an explicit
	decision at the call site rather than an accident of comparison.
]]
function CombatTypes.isStrongerThan(candidate: CombatState, current: CombatState): boolean
	return STATE_PRIORITY[candidate] > STATE_PRIORITY[current]
end

--[[
	True when the action is one that reports `End` or `Cancel`.
]]
function CombatTypes.isHoldAction(action: ActionName): boolean
	return CombatTypes.HOLD_ACTIONS[action] == true
end

return table.freeze(CombatTypes)
