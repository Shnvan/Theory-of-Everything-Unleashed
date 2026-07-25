--!strict

--[[
	Applies movement speed to the local character.

	The whole feature is one cap. Sprinting is not an action and has no
	threshold: the engine already scales speed by the magnitude of the move
	vector, so a part-deflected thumbstick walks by itself and full deflection
	reaches `SPRINT_SPEED`. `Walk` exists only because a keyboard is binary --
	`W` is always full magnitude, so a desktop player would otherwise have one
	speed. Recorded as D-028.

	This controller decides nothing. `CombatConfig.getMoveSpeed` owns the rule,
	`InputController` owns reading the input, and this only moves the resulting
	number onto the `Humanoid`.

	Speed is applied client-side. That is normal for a Roblox prototype and is
	not exploit-resistant; docs/TECHNICAL_ARCHITECTURE.md gives the server
	authority over combat state, not over `WalkSpeed`, and server-side movement
	validation is a later concern rather than something this pretends to solve.
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GameShared = ReplicatedStorage:WaitForChild("GameShared")
local CombatConfig = require(GameShared:WaitForChild("Config"):WaitForChild("CombatConfig"))
local CombatTypes = require(GameShared:WaitForChild("Types"):WaitForChild("CombatTypes"))

local InputController = require(script.Parent.InputController)

type ActionInput = CombatTypes.ActionInput

local localPlayer = Players.LocalPlayer

local connections: { RBXScriptConnection } = {}
local humanoid: Humanoid? = nil
local started = false

local MovementController = {}

--[[
	Pushes the current speed onto the live humanoid.

	Reads the hold state rather than tracking its own copy. A second copy of
	"is Walk down" is a second thing that can be wrong, and the authoritative
	answer already exists one module away.
]]
local function applySpeed()
	local currentHumanoid = humanoid
	if currentHumanoid == nil or currentHumanoid.Parent == nil then
		return
	end

	currentHumanoid.WalkSpeed = CombatConfig.getMoveSpeed(InputController.IsActionDown("Walk"))
end

--[[
	Binds to a newly spawned character.

	The speed is applied immediately rather than waiting for the next input,
	because a fresh Humanoid starts at the engine default. Respawning while Walk
	is held must come back walking, not sprinting — the same class of bug as the
	S10 latch, and the reason this asks `IsActionDown` instead of assuming a
	neutral start.
]]
local function onCharacterAdded(character: Model)
	local newHumanoid = character:FindFirstChildOfClass("Humanoid")
		or character:WaitForChild("Humanoid", 10) :: Humanoid?

	if newHumanoid == nil or not started then
		return
	end

	humanoid = newHumanoid
	applySpeed()
end

function MovementController.Start()
	if started then
		return
	end
	started = true

	table.insert(
		connections,
		InputController.OnAction(function(actionInput: ActionInput)
			if actionInput.action ~= "Walk" then
				return
			end

			-- Every phase re-reads the hold state and reapplies, so `End` and
			-- `Cancel` need no separate handling and cannot diverge.
			applySpeed()
		end)
	)

	table.insert(connections, localPlayer.CharacterAdded:Connect(onCharacterAdded))

	local existing = localPlayer.Character
	if existing ~= nil then
		task.spawn(onCharacterAdded, existing)
	end
end

function MovementController.Stop()
	if not started then
		return
	end
	started = false

	for _, connection in connections do
		connection:Disconnect()
	end
	table.clear(connections)

	humanoid = nil
end

--[[
	The speed currently applied, or nil when there is no character. For tests and
	diagnostics; nothing in gameplay should need to ask.
]]
function MovementController.GetAppliedSpeed(): number?
	local currentHumanoid = humanoid
	if currentHumanoid == nil or currentHumanoid.Parent == nil then
		return nil
	end
	return currentHumanoid.WalkSpeed
end

function MovementController.IsStarted(): boolean
	return started
end

return MovementController
