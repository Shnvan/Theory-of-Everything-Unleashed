--!strict

--[[
	A minimal test harness.

	Deliberately small: a describe/test pair, a few assertions, and a report that
	returns a process exit code. This exists instead of a framework because the
	only thing under test is pure logic over strings and booleans, and adding a
	dependency to assert `a == b` would fail the project's own rule against
	adding packages without a concrete need.

	`report` fails when zero tests ran. A suite that silently collapses to
	nothing is worse than a failing one, because it reports success.
]]

local testkit = {}

local passed = 0
local failures: { string } = {}
local currentSuite = "(no suite)"

function testkit.describe(name: string)
	currentSuite = name
end

function testkit.test(name: string, body: () -> ())
	local ok, err = pcall(body)
	if ok then
		passed += 1
	else
		table.insert(failures, `{currentSuite} > {name}\n      {tostring(err)}`)
	end
end

--[[
	Assertions raise at level 2 so the reported line is the failing assertion in
	the spec, not this file.
]]
function testkit.equal(actual: any, expected: any, what: string?)
	if actual ~= expected then
		local label = if what ~= nil then `{what}: ` else ""
		error(`{label}expected {tostring(expected)}, got {tostring(actual)}`, 2)
	end
end

function testkit.isTrue(value: any, what: string?)
	if value ~= true then
		local label = if what ~= nil then `{what}: ` else ""
		error(`{label}expected true, got {tostring(value)}`, 2)
	end
end

function testkit.isFalse(value: any, what: string?)
	if value ~= false then
		local label = if what ~= nil then `{what}: ` else ""
		error(`{label}expected false, got {tostring(value)}`, 2)
	end
end

function testkit.isNil(value: any, what: string?)
	if value ~= nil then
		local label = if what ~= nil then `{what}: ` else ""
		error(`{label}expected nil, got {tostring(value)}`, 2)
	end
end

--[[
	Prints the result and returns the exit code the runner should use.
]]
function testkit.report(): number
	print("")
	if #failures > 0 then
		print(`FAILED  {#failures} of {passed + #failures}`)
		for _, failure in failures do
			print(`  x {failure}`)
		end
		return 1
	end

	if passed == 0 then
		print("FAILED  no tests ran -- a spec file probably failed to load")
		return 1
	end

	print(`PASSED  {passed} tests`)
	return 0
end

return testkit
