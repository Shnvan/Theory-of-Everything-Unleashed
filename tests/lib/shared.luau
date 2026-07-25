--!strict

--[[
	The one place the shared tree is mounted, so every spec loads the same
	instances from the same cache and a module required by two specs still runs
	once.
]]

local robloxRequire = require("./robloxRequire")

local root = robloxRequire.tree("src/shared", "GameShared")

return {
	root = root,
	CombatTypes = robloxRequire.load(root.Types.CombatTypes),
	CombatConfig = robloxRequire.load(root.Config.CombatConfig),
	CombatStateMachine = robloxRequire.load(root.Combat.CombatStateMachine),
}
