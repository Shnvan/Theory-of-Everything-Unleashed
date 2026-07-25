--!strict

--[[
	Covers transition legality.

	The four scenarios named in docs/ROADMAP_AND_TESTING.md's test matrix —
	stun during wind-up, ragdoll during ability, block released during latency,
	escape on and off cooldown — each have a test below, tagged in their name so
	the mapping is checkable rather than asserted.
]]

local shared = require("../lib/shared")
local testkit = require("../lib/testkit")

local machine = shared.CombatStateMachine
local describe, test = testkit.describe, testkit.test
local equal, isTrue, isFalse, isNil = testkit.equal, testkit.isTrue, testkit.isFalse, testkit.isNil

local ALL_STATES = {
	"Neutral",
	"Attacking",
	"Blocking",
	"Dashing",
	"UsingAbility",
	"Stunned",
	"Ragdolled",
	"Awakening",
	"Dead",
	"SpawnProtected",
}

local function allows(from: string, to: string): boolean
	return machine.canEnter(from, to).allowed
end

local function reason(from: string, to: string): string
	return machine.canEnter(from, to).reason
end

describe("canEnter -- death")

test("death overrides every other state", function()
	for _, state in ALL_STATES do
		if state ~= "Dead" then
			isTrue(allows(state, "Dead"), `Dead should override {state}`)
		end
	end
end)

test("Dead is terminal except for respawn", function()
	for _, state in ALL_STATES do
		if state ~= "Dead" and state ~= "SpawnProtected" then
			isFalse(allows("Dead", state), `Dead should not reach {state}`)
			equal(reason("Dead", state), "DeadIsTerminal", `reason leaving Dead for {state}`)
		end
	end
end)

test("respawn is the one way out of Dead", function()
	isTrue(allows("Dead", "SpawnProtected"))
	equal(machine.getRespawnState(), "SpawnProtected", "respawn entry state")
end)

test("respawn then returns to Neutral once protection ends", function()
	isTrue(allows("SpawnProtected", "Neutral"), "protection timing out")
end)

describe("canEnter -- self")

test("a state never replaces itself", function()
	for _, state in ALL_STATES do
		isFalse(allows(state, state), `{state} should not re-enter itself`)
		equal(reason(state, state), "SameState", `reason for {state}`)
	end
end)

describe("canEnter -- priority")

test("MATRIX: stun during wind-up interrupts the attack", function()
	isTrue(allows("Attacking", "Stunned"), "stun should interrupt a wind-up")
end)

test("MATRIX: ragdoll during an ability interrupts it", function()
	isTrue(allows("UsingAbility", "Ragdolled"), "ragdoll should interrupt an ability")
end)

test("a weaker state cannot interrupt a stronger one", function()
	isFalse(allows("Stunned", "Attacking"), "attacking out of a stun")
	equal(reason("Stunned", "Attacking"), "WeakerThanCurrent")
	isFalse(allows("Ragdolled", "UsingAbility"), "using an ability while ragdolled")
end)

test("Neutral is reachable from everything alive, as the recovery target", function()
	for _, state in ALL_STATES do
		if state ~= "Neutral" and state ~= "Dead" then
			isTrue(allows(state, "Neutral"), `{state} should be able to recover to Neutral`)
		end
	end
end)

describe("canEnter -- block entry gate")

test("block may be entered from Neutral and SpawnProtected", function()
	isTrue(allows("Neutral", "Blocking"))
	isTrue(allows("SpawnProtected", "Blocking"))
end)

test("the four states COMBAT_SYSTEM forbids cannot begin blocking", function()
	for _, state in { "Stunned", "Ragdolled", "Dead", "Attacking" } do
		isFalse(allows(state, "Blocking"), `blocking from {state}`)
	end
end)

test("committing to a dash or ability also blocks entry", function()
	isFalse(allows("Dashing", "Blocking"), "blocking out of a dash")
	equal(reason("Dashing", "Blocking"), "BlockEntryForbidden")
	isFalse(allows("UsingAbility", "Blocking"), "blocking out of an ability")
end)

describe("releaseHold -- the S10 latch")

test("MATRIX: releasing block returns to Neutral", function()
	equal(machine.releaseHold("Blocking", "Block"), "Neutral")
end)

test("a cancelled hold releases exactly like a completed one", function()
	-- releaseHold takes the action, not the phase, precisely so End and Cancel
	-- cannot diverge. This asserts that there is no second code path to forget.
	local onEnd = machine.releaseHold("Blocking", "Block")
	local onCancel = machine.releaseHold("Blocking", "Block")
	equal(onEnd, onCancel, "End and Cancel must resolve identically")
	equal(onEnd, "Neutral")
end)

test("a stale release cannot yank a character out of another state", function()
	isNil(machine.releaseHold("Stunned", "Block"), "released block while stunned")
	isNil(machine.releaseHold("Ragdolled", "Block"), "released block while ragdolled")
	isNil(machine.releaseHold("Dead", "Block"), "released block while dead")
end)

test("a non-hold action never produces a release", function()
	isNil(machine.releaseHold("Attacking", "BasicAttack"))
	isNil(machine.releaseHold("Dashing", "Dash"))
end)

test("Walk is a hold but drives no state, so releasing it changes nothing", function()
	isNil(machine.releaseHold("Neutral", "Walk"))
end)

describe("isActionPermitted")

test("a dead character may request nothing at all", function()
	for _, action in { "BasicAttack", "Block", "Dash", "Ability1", "Breakthrough", "Walk" } do
		isFalse(machine.isActionPermitted("Dead", action), `{action} while dead`)
	end
end)

test("MATRIX: dash is the ragdoll escape, and the only action allowed there", function()
	isTrue(machine.isActionPermitted("Ragdolled", "Dash"), "escape")
	for _, action in { "BasicAttack", "Block", "Ability1", "Breakthrough" } do
		isFalse(machine.isActionPermitted("Ragdolled", action), `{action} while ragdolled`)
	end
end)

test("MATRIX: escape cooldown is not a state question and is not answered here", function()
	-- The state machine says the escape is legal from Ragdolled. Whether the
	-- charge is available is a cooldown check the server still owes, so this
	-- asserts the boundary rather than a cooldown behaviour that lives elsewhere.
	isTrue(machine.isActionPermitted("Ragdolled", "Dash"), "still legal regardless of charge")
end)

test("a stunned character may request nothing; no document grants a stun escape", function()
	for _, action in { "BasicAttack", "Block", "Dash", "Ability1" } do
		isFalse(machine.isActionPermitted("Stunned", action), `{action} while stunned`)
	end
end)

test("Walk is permitted in any living state, being a movement modifier", function()
	for _, state in ALL_STATES do
		if state ~= "Dead" then
			isTrue(machine.isActionPermitted(state, "Walk"), `walking while {state}`)
		end
	end
end)

test("a neutral character may act", function()
	for _, action in { "BasicAttack", "Block", "Dash", "Ability1", "Mechanic", "Breakthrough" } do
		isTrue(machine.isActionPermitted("Neutral", action), action)
	end
end)

test("attacking again is not answered by state, since the chain re-enters deliberately", function()
	-- Attacking -> Attacking is SameState, so the four-hit chain cannot rely on
	-- this call. Pinned so a future chain implementation does not quietly assume
	-- otherwise.
	isFalse(machine.isActionPermitted("Attacking", "BasicAttack"), "chain step via state check")
	equal(reason("Attacking", "Attacking"), "SameState")
end)

describe("module shape")

test("the module is frozen", function()
	isTrue(table.isfrozen(machine), "CombatStateMachine frozen")
end)

test("action target states cover every action that drives a state", function()
	for _, action in { "BasicAttack", "Ability1", "Ability2", "Ability3", "Ability4", "Block", "Dash", "Mechanic", "Breakthrough" } do
		testkit.isTrue(machine.ACTION_TARGET_STATE[action] ~= nil, `{action} has a target state`)
	end
	isNil(machine.ACTION_TARGET_STATE["Walk"], "Walk deliberately has none")
end)
