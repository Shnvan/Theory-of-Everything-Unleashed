--!strict

--[[
	Covers the movement speed rule.

	Only the pure decision is testable here. Applying it to a `Humanoid` needs
	the engine, and whether the result *feels* right needs a person — neither is
	claimed by these tests.
]]

local shared = require("../lib/shared")
local testkit = require("../lib/testkit")

local CombatConfig = shared.CombatConfig
local describe, test = testkit.describe, testkit.test
local equal, isTrue = testkit.equal, testkit.isTrue

describe("CombatConfig.getMoveSpeed")

test("holding Walk gives walk speed", function()
	equal(CombatConfig.getMoveSpeed(true), CombatConfig.WALK_SPEED)
end)

test("not holding Walk gives sprint speed", function()
	equal(CombatConfig.getMoveSpeed(false), CombatConfig.SPRINT_SPEED)
end)

test("walking is strictly slower than sprinting", function()
	isTrue(CombatConfig.WALK_SPEED < CombatConfig.SPRINT_SPEED, "walk must be slower")
end)

test("both speeds are positive, so neither state freezes the character", function()
	isTrue(CombatConfig.WALK_SPEED > 0, "walk speed positive")
	isTrue(CombatConfig.SPRINT_SPEED > 0, "sprint speed positive")
end)

test("sprint speed stays at the value the arena crossing time was measured against", function()
	-- docs/OMNISCIENCE_COLISEUM.md timed the arena at WalkSpeed 16, and P-008's
	-- ~53 second crossing estimate depends on it. Changing this is legitimate,
	-- but it invalidates that measurement -- so this test exists to make the
	-- coupling impossible to change by accident.
	equal(CombatConfig.SPRINT_SPEED, 16, "sprint speed")
end)

describe("movement is not a combat state")

test("Walk drives no state and is permitted in every living state", function()
	-- D-028 and D-031: speed layers on Neutral rather than replacing it, so it
	-- can neither suppress nor be suppressed by a combat state.
	local machine = shared.CombatStateMachine
	testkit.isNil(machine.ACTION_TARGET_STATE["Walk"], "Walk target state")
	for _, state in { "Neutral", "Attacking", "Blocking", "Dashing", "UsingAbility", "Stunned", "Ragdolled", "Awakening", "SpawnProtected" } do
		isTrue(machine.isActionPermitted(state, "Walk"), `walking while {state}`)
	end
end)
