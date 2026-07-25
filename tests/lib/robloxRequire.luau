--!strict

--[[
	Loads Roblox-style ModuleScripts outside Roblox.

	Our shared modules require each other the way Roblox expects —
	`require(script.Parent.Parent.Types.CombatTypes)` — because that is what
	ships. Lune resolves requires by file path and has no `script`, so it cannot
	load them directly.

	This builds a synthetic instance tree over a real directory, gives each
	module a `script` whose `.Parent` chain mirrors the folder layout, and swaps
	in a `require` that understands those nodes. Modules are executed with
	`luau.load` against that environment and memoised, so a module required
	twice runs once, exactly as Roblox behaves.

	Deliberately minimal. It supports what our shared modules actually use:
	folder and module traversal by name, and `script.Parent`. It does not
	pretend to be the Roblox DataModel, and it does not provide `Enum` or any
	datatype, so a module touching those cannot be loaded here — which is a
	feature. Anything needing `Enum` is not a pure module and belongs in a
	Studio test instead.
]]

local fs = require("@lune/fs")
local luau = require("@lune/luau")

export type Node = {
	Name: string,
	Parent: Node?,
	path: string,
	isFolder: boolean,
	[string]: any,
}

local robloxRequire = {}

-- Globals a pure shared module may legitimately reach for. Anything absent here
-- fails loudly at load time rather than silently returning nil, which is how a
-- module that is not actually pure gets caught.
local ALLOWED_GLOBALS = {
	"assert",
	"error",
	"getmetatable",
	"ipairs",
	"next",
	"pairs",
	"pcall",
	"print",
	"rawequal",
	"rawget",
	"rawlen",
	"rawset",
	"select",
	"setmetatable",
	"tonumber",
	"tostring",
	"type",
	"typeof",
	"unpack",
	"xpcall",
	"bit32",
	"buffer",
	"coroutine",
	"math",
	"os",
	"string",
	"table",
	"utf8",
}

local function buildNode(path: string, name: string, parent: Node?): Node
	local node: Node = {
		Name = name,
		Parent = parent,
		path = path,
		isFolder = fs.isDir(path),
	}

	if node.isFolder then
		for _, entry in fs.readDir(path) do
			local childPath = path .. "/" .. entry
			if fs.isDir(childPath) then
				node[entry] = buildNode(childPath, entry, node)
			elseif entry:match("%.luau$") ~= nil then
				local childName = (entry:gsub("%.luau$", ""))
				node[childName] = buildNode(childPath, childName, node)
			end
		end
	end

	return node
end

--[[
	Builds a synthetic tree over `rootPath`. The root node stands in for the
	folder itself, so `root.Types.CombatTypes` mirrors `src/shared/Types/`.
]]
function robloxRequire.tree(rootPath: string, rootName: string): Node
	if not fs.isDir(rootPath) then
		error(`robloxRequire.tree: not a directory: {rootPath}`)
	end
	return buildNode(rootPath, rootName, nil)
end

local cache: { [string]: any } = {}

--[[
	Requires a node from a tree, running it once and memoising the result.
]]
function robloxRequire.load(node: Node): any
	if node.isFolder then
		error(`attempted to require a folder: {node.path}`)
	end

	local cached = cache[node.path]
	if cached ~= nil then
		return cached
	end

	local source = fs.readFile(node.path)

	local environment: { [string]: any } = {}
	for _, name in ALLOWED_GLOBALS do
		environment[name] = (getfenv(0) :: any)[name]
	end
	environment.script = node
	environment.require = robloxRequire.load
	environment._G = {}

	local chunk = luau.load(source, {
		debugName = node.path,
		environment = environment,
	})

	local result = chunk()
	if result == nil then
		error(`module returned nil: {node.path}`)
	end

	cache[node.path] = result
	return result
end

return robloxRequire
