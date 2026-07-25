--!strict

--[[
	Client input layer. Turns keyboard, mouse, and touch input into combat
	action events.

	This module reads input and reports it. It does not decide whether an action
	is legal, whether it hit anything, or what it cost. Per
	docs/TECHNICAL_ARCHITECTURE.md the server owns all of that; this layer's only
	obligation to the server is a monotonically increasing sequence number so
	stale and duplicated requests can be rejected.

	Action names, keybinds, and touch-button names come from the shared config so
	the server sees the same action set. The Studio-side GUI that the touch
	buttons resolve against is specified in docs/HUD_AND_UI_SPEC.md; if it is
	missing, touch degrades to a warning and desktop input still works.

	Still on ContextActionService rather than the Input Action System. That is a
	recorded decision with a trigger, not an oversight: see D-019.
]]

local ContextActionService = game:GetService("ContextActionService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local GameShared = ReplicatedStorage:WaitForChild("GameShared")

local CombatTypes = require(GameShared:WaitForChild("Types"):WaitForChild("CombatTypes"))
local InputConfig = require(GameShared:WaitForChild("Config"):WaitForChild("InputConfig"))

local localPlayer = Players.LocalPlayer

export type ActionName = CombatTypes.ActionName
export type InputPhase = CombatTypes.InputPhase
export type ActionInput = CombatTypes.ActionInput
export type ActionCallback = CombatTypes.ActionCallback

type ActionDefinition = InputConfig.ActionDefinition

-- How long to wait for the HUD before giving up on touch controls. Applied on a
-- separate thread so a missing HUD cannot delay Start().
local HUD_WAIT_SECONDS = 10

local actionEvent = Instance.new("BindableEvent")
actionEvent.Name = "ActionInput"

local actionDown: { [ActionName]: boolean } = {}
local touchInputActions: { [InputObject]: ActionDefinition } = {}
local connections: { RBXScriptConnection } = {}
local lastActionInput: ActionInput? = nil
local touchControls: Frame? = nil
local started = false
local enabled = true

-- Monotonic per-session counter. The server rejects a request whose sequence is
-- not newer than the last one it accepted, so this must never decrease or
-- repeat within a session.
local nextSequence = 0

local InputController = {}

local function getMovementDirection(): Vector3
	local character = localPlayer.Character
	if character == nil then
		return Vector3.zero
	end

	local humanoid = character:FindFirstChildOfClass("Humanoid")
	if humanoid == nil then
		return Vector3.zero
	end

	local moveDirection = humanoid.MoveDirection
	if moveDirection.Magnitude > 1 then
		return moveDirection.Unit
	end

	return moveDirection
end

local function emitAction(definition: ActionDefinition, phase: InputPhase, inputObject: InputObject?)
	local isBeginning = phase == "Begin"
	if isBeginning == (actionDown[definition.action] == true) then
		return
	end

	actionDown[definition.action] = isBeginning
	nextSequence += 1

	local actionInput: ActionInput = {
		action = definition.action,
		phase = phase,
		sequence = nextSequence,
		movementDirection = getMovementDirection(),
		timestamp = os.clock(),
		-- A synthetic release, from focus loss or from being disabled, has no
		-- originating InputObject. Report it as Enum.UserInputType.None rather
		-- than inventing a device.
		inputType = if inputObject ~= nil then inputObject.UserInputType else Enum.UserInputType.None,
		keyCode = if inputObject ~= nil then inputObject.KeyCode else Enum.KeyCode.None,
	}

	lastActionInput = actionInput
	actionEvent:Fire(actionInput)
end

local function finishAction(definition: ActionDefinition, inputObject: InputObject?, wasCancelled: boolean)
	if actionDown[definition.action] ~= true then
		return
	end

	if definition.isHoldAction then
		emitAction(definition, if wasCancelled then "Cancel" else "End", inputObject)
	else
		actionDown[definition.action] = false
	end
end

--[[
	Releases every action currently held.

	Needed because a held touch does not always produce InputEnded. Losing window
	focus mid-press, or the HUD being destroyed under the finger, previously left
	the action latched down for the rest of the session, so IsActionDown("Block")
	would keep returning true forever.
]]
local function releaseAllHeldActions(wasCancelled: boolean)
	table.clear(touchInputActions)

	for _, definition in InputConfig.ACTION_DEFINITIONS do
		finishAction(definition, nil, wasCancelled)
		actionDown[definition.action] = false
	end
end

local function handleBoundAction(
	bindingName: string,
	inputState: Enum.UserInputState,
	inputObject: InputObject
): Enum.ContextActionResult
	local definition = InputConfig.DEFINITION_BY_BINDING[bindingName]
	if definition == nil then
		return Enum.ContextActionResult.Pass
	end

	-- Pass rather than Sink when this layer is not consuming the input, so a
	-- disabled combat layer does not swallow left-click for the whole game.
	-- Without this, Sink on MouseButton1 blocked every other click interaction
	-- for as long as the module was started.
	if not enabled then
		return Enum.ContextActionResult.Pass
	end

	if inputState == Enum.UserInputState.Begin then
		if UserInputService:GetFocusedTextBox() ~= nil then
			return Enum.ContextActionResult.Pass
		end

		emitAction(definition, "Begin", inputObject)
	elseif inputState == Enum.UserInputState.End then
		finishAction(definition, inputObject, false)
	elseif inputState == Enum.UserInputState.Cancel then
		finishAction(definition, inputObject, true)
	end

	return Enum.ContextActionResult.Sink
end

--[[
	Binds every action from one table, so a binding name is written once. The
	previous version re-typed each name at bind time, where a typo would
	desynchronize the bind from both the dispatch lookup and the unbind, leaving
	an action that silently never fired.
]]
local function bindKeyboardAndMouse()
	for _, definition in InputConfig.ACTION_DEFINITIONS do
		ContextActionService:BindAction(
			definition.bindingName,
			handleBoundAction,
			false,
			table.unpack(definition.inputs)
		)
	end
end

local function isPointerInput(inputObject: InputObject): boolean
	return inputObject.UserInputType == Enum.UserInputType.Touch
		or inputObject.UserInputType == Enum.UserInputType.MouseButton1
end

local function bindTouchControls()
	local playerGui = localPlayer:WaitForChild("PlayerGui", HUD_WAIT_SECONDS)
	if playerGui == nil then
		warn("InputController could not find PlayerGui; touch controls are unavailable")
		return
	end

	local gameHud = playerGui:WaitForChild("GameHUD", HUD_WAIT_SECONDS)
	if gameHud == nil or not gameHud:IsA("ScreenGui") then
		warn("InputController could not find PlayerGui.GameHUD; touch controls are unavailable")
		return
	end

	-- Stop() may have run while this thread was waiting on the HUD. Binding now
	-- would leak connections into a stopped controller.
	if not started then
		return
	end

	local controls = gameHud:FindFirstChild("TouchControls")
	if controls == nil or not controls:IsA("Frame") then
		warn("InputController could not find GameHUD.TouchControls; touch controls are unavailable")
		return
	end

	touchControls = controls

	local function updateVisibility()
		controls.Visible = UserInputService.TouchEnabled
	end

	updateVisibility()
	table.insert(connections, UserInputService:GetPropertyChangedSignal("TouchEnabled"):Connect(updateVisibility))

	for buttonName, definition in InputConfig.DEFINITION_BY_TOUCH_BUTTON do
		local button = controls:FindFirstChild(buttonName)
		if button == nil or not button:IsA("GuiButton") then
			warn(`InputController could not find touch button {buttonName}; see docs/HUD_AND_UI_SPEC.md`)
			continue
		end

		table.insert(
			connections,
			button.InputBegan:Connect(function(inputObject: InputObject)
				if not enabled or not isPointerInput(inputObject) then
					return
				end

				touchInputActions[inputObject] = definition
				emitAction(definition, "Begin", inputObject)
			end)
		)
	end

	table.insert(
		connections,
		UserInputService.InputEnded:Connect(function(inputObject: InputObject)
			local definition = touchInputActions[inputObject]
			if definition == nil then
				return
			end

			touchInputActions[inputObject] = nil
			finishAction(definition, inputObject, false)
		end)
	)
end

function InputController.Start()
	if started then
		return
	end

	started = true
	enabled = true
	bindKeyboardAndMouse()

	-- Off the caller's thread: bindTouchControls waits on two instances and can
	-- take up to 2 * HUD_WAIT_SECONDS. Keyboard and mouse are already live by
	-- this point, so nothing the player can do is delayed, and Bootstrap can
	-- start further controllers without stalling behind a missing HUD.
	task.spawn(bindTouchControls)

	-- A held touch does not reliably produce InputEnded when the window loses
	-- focus, which is the latch this releases.
	table.insert(
		connections,
		UserInputService.WindowFocusReleased:Connect(function()
			releaseAllHeldActions(true)
		end)
	)
end

function InputController.Stop()
	if not started then
		return
	end

	started = false

	-- Release before unbinding, so consumers observe End or Cancel for anything
	-- they were told was held rather than being left with a stale down flag.
	releaseAllHeldActions(true)

	for _, definition in InputConfig.ACTION_DEFINITIONS do
		ContextActionService:UnbindAction(definition.bindingName)
	end

	for _, connection in connections do
		connection:Disconnect()
	end

	table.clear(connections)
	table.clear(touchInputActions)

	if touchControls ~= nil then
		touchControls.Visible = false
		touchControls = nil
	end
end

--[[
	Suspends and resumes input consumption without tearing down bindings.

	Use this for character selection, menus, cutscenes, and spectating. While
	disabled, bound inputs pass through to whatever else wants them instead of
	being sunk, and any held action is released so nothing stays latched across
	the gap.
]]
function InputController.SetEnabled(isEnabled: boolean)
	if enabled == isEnabled then
		return
	end

	enabled = isEnabled

	if not isEnabled then
		releaseAllHeldActions(true)
	end
end

function InputController.IsEnabled(): boolean
	return enabled
end

function InputController.OnAction(callback: ActionCallback): RBXScriptConnection
	return actionEvent.Event:Connect(callback)
end

function InputController.IsActionDown(action: ActionName): boolean
	return actionDown[action] == true
end

function InputController.GetMovementDirection(): Vector3
	return getMovementDirection()
end

function InputController.GetLastActionInput(): ActionInput?
	if lastActionInput == nil then
		return nil
	end

	return table.clone(lastActionInput) :: ActionInput
end

function InputController.IsStarted(): boolean
	return started
end

return InputController
