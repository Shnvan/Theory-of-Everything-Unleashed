--!strict

--[[
	Unit test entry point. Run from the repository root:

		lune run tests/run.luau

	These tests cover the pure shared modules only. They cannot prove combat
	behaviour, replication, or feel — docs/DEVELOPER_RULES.md puts unit tests at
	rung 2 of the verification ladder, above the static gates and below any
	Studio test. A green run here is a floor, not acceptance.

	Spec files are required directly rather than discovered, so a spec that fails
	to load raises here instead of quietly vanishing from the count.
]]

local process = require("@lune/process")
local testkit = require("./lib/testkit")

require("./specs/CombatTypes.spec")
require("./specs/CombatStateMachine.spec")

process.exit(testkit.report())
