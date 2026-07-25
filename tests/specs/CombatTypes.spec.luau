--!strict

--[[
	Covers the state-priority data and the pure predicates over it.

	These look trivial, and that is the point: the priority order is LOCKED in
	docs/COMBAT_SYSTEM.md, so a silent edit to the table is a design change
	disguised as a typo. This pins it.
]]

local shared = require("../lib/shared")
local testkit = require("../lib/testkit")

local CombatTypes = shared.CombatTypes
local describe, test = testkit.describe, testkit.test
local equal, isTrue, isFalse = testkit.equal, testkit.isTrue, testkit.isFalse

describe("CombatTypes.STATE_PRIORITY")

test("matches the locked order in COMBAT_SYSTEM.md", function()
	local expected = {
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
	}
	for state, priority in expected do
		equal(CombatTypes.STATE_PRIORITY[state], priority, state)
	end
end)

test("covers every state exactly once, with no extras", function()
	local count = 0
	for _ in CombatTypes.STATE_PRIORITY do
		count += 1
	end
	equal(count, 10, "state count")
end)

describe("CombatTypes.isStrongerThan")

test("a stronger state overrides a weaker one", function()
	isTrue(CombatTypes.isStrongerThan("Dead", "Neutral"))
	isTrue(CombatTypes.isStrongerThan("Stunned", "Attacking"))
	isTrue(CombatTypes.isStrongerThan("Dashing", "Blocking"))
end)

test("a weaker state does not override a stronger one", function()
	isFalse(CombatTypes.isStrongerThan("Neutral", "Dead"))
	isFalse(CombatTypes.isStrongerThan("Attacking", "Stunned"))
end)

test("equal priority returns false, so re-entry is always deliberate", function()
	isFalse(CombatTypes.isStrongerThan("Attacking", "Attacking"))
	isFalse(CombatTypes.isStrongerThan("Neutral", "Neutral"))
end)

describe("CombatTypes.isHoldAction")

test("Block and Walk report a release; nothing else does", function()
	isTrue(CombatTypes.isHoldAction("Block"))
	isTrue(CombatTypes.isHoldAction("Walk"))
	isFalse(CombatTypes.isHoldAction("BasicAttack"))
	isFalse(CombatTypes.isHoldAction("Dash"))
	isFalse(CombatTypes.isHoldAction("Breakthrough"))
end)

describe("CombatTypes.getAbilitySlot")

test("maps the four ability actions to their slot numbers", function()
	equal(CombatTypes.getAbilitySlot("Ability1"), 1)
	equal(CombatTypes.getAbilitySlot("Ability2"), 2)
	equal(CombatTypes.getAbilitySlot("Ability3"), 3)
	equal(CombatTypes.getAbilitySlot("Ability4"), 4)
end)

test("returns nil for a non-ability action", function()
	testkit.isNil(CombatTypes.getAbilitySlot("BasicAttack"))
	testkit.isNil(CombatTypes.getAbilitySlot("Block"))
end)

describe("CombatConfig")

test("assist threshold tracks MAX_HEALTH rather than being a flat number", function()
	local CombatConfig = shared.CombatConfig
	equal(
		CombatConfig.getAssistDamageThreshold(),
		CombatConfig.MAX_HEALTH * CombatConfig.ASSIST_DAMAGE_FRACTION,
		"assist threshold"
	)
end)

test("block half-arc is half the configured arc", function()
	local CombatConfig = shared.CombatConfig
	equal(CombatConfig.getBlockHalfArcDegrees(), CombatConfig.BLOCK_ARC_DEGREES / 2, "half arc")
end)
