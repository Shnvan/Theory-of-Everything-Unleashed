--!strict

local ContextActionService = game:GetService("ContextActionService")
local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")

local localPlayer = Players.LocalPlayer

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
	| "Sprint"

export type InputPhase = "Begin" | "End" | "Cancel"

export type ActionInput = {
	action: ActionName,
	phase: InputPhase,
	movementDirection: Vector3,
	timestamp: number,
	inputType: Enum.UserInputType,
	keyCode: Enum.KeyCode,
}

export type ActionCallback = (actionInput: ActionInput) -> ()

type ActionDefinition = {
	action: ActionName,
	bindingName: string,
	touchButtonName: string,
	isHoldAction: boolean,
}

local ACTION_DEFINITIONS: { ActionDefinition } = {
	{
		action = "BasicAttack",
		bindingName = "TOEU_BasicAttack",
		touchButtonName = "BasicAttackButton",
		isHoldAction = false,
	},
	{
		action = "Ability1",
		bindingName = "TOEU_Ability1",
		touchButtonName = "Ability1Button",
		isHoldAction = false,
	},
	{
		action = "Ability2",
		bindingName = "TOEU_Ability2",
		touchButtonName = "Ability2Button",
		isHoldAction = false,
	},
	{
		action = "Ability3",
		bindingName = "TOEU_Ability3",
		touchButtonName = "Ability3Button",
		isHoldAction = false,
	},
	{
		action = "Ability4",
		bindingName = "TOEU_Ability4",
		touchButtonName = "Ability4Button",
		isHoldAction = false,
	},
	{
		action = "Block",
		bindingName = "TOEU_Block",
		touchButtonName = "BlockButton",
		isHoldAction = true,
	},
	{
		action = "Dash",
		bindingName = "TOEU_Dash",
		touchButtonName = "DashButton",
		isHoldAction = false,
	},
	{
		action = "Mechanic",
		bindingName = "TOEU_Mechanic",
		touchButtonName = "MechanicButton",
		isHoldAction = false,
	},
	{
		action = "Breakthrough",
		bindingName = "TOEU_Breakthrough",
		touchButtonName = "BreakthroughButton",
		isHoldAction = false,
	},
	{
		action = "Sprint",
		bindingName = "TOEU_Sprint",
		touchButtonName = "SprintButton",
		isHoldAction = true,
	},
}

local definitionByBinding: { [string]: ActionDefinition } = {}
local definitionByButton: { [string]: ActionDefinition } = {}

for _, definition in ACTION_DEFINITIONS do
	definitionByBinding[definition.bindingName] = definition
	definitionByButton[definition.touchButtonName] = definition
end

local actionEvent = Instance.new("BindableEvent")
actionEvent.Name = "ActionInput"

local actionDown: { [ActionName]: boolean } = {}
local touchInputActions: { [InputObject]: ActionDefinition } = {}
local connections: { RBXScriptConnection } = {}
local lastActionInput: ActionInput? = nil
local touchControls: Frame? = nil
local started = false

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

local function emitAction(definition: ActionDefinition, phase: InputPhase, inputObject: InputObject)
	local isBeginning = phase == "Begin"
	if isBeginning == (actionDown[definition.action] == true) then
		return
	end

	actionDown[definition.action] = isBeginning

	local actionInput: ActionInput = {
		action = definition.action,
		phase = phase,
		movementDirection = getMovementDirection(),
		timestamp = os.clock(),
		inputType = inputObject.UserInputType,
		keyCode = inputObject.KeyCode,
	}

	lastActionInput = actionInput
	actionEvent:Fire(actionInput)
end

local function finishAction(definition: ActionDefinition, inputObject: InputObject, wasCancelled: boolean)
	if actionDown[definition.action] ~= true then
		return
	end

	if definition.isHoldAction then
		emitAction(definition, if wasCancelled then "Cancel" else "End", inputObject)
	else
		actionDown[definition.action] = false
	end
end

local function handleBoundAction(
	bindingName: string,
	inputState: Enum.UserInputState,
	inputObject: InputObject
): Enum.ContextActionResult
	local definition = definitionByBinding[bindingName]
	if definition == nil then
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

local function bindKeyboardAndMouse()
	ContextActionService:BindAction(
		"TOEU_BasicAttack",
		handleBoundAction,
		false,
		Enum.UserInputType.MouseButton1
	)
	ContextActionService:BindAction("TOEU_Ability1", handleBoundAction, false, Enum.KeyCode.One)
	ContextActionService:BindAction("TOEU_Ability2", handleBoundAction, false, Enum.KeyCode.Two)
	ContextActionService:BindAction("TOEU_Ability3", handleBoundAction, false, Enum.KeyCode.Three)
	ContextActionService:BindAction("TOEU_Ability4", handleBoundAction, false, Enum.KeyCode.Four)
	ContextActionService:BindAction("TOEU_Block", handleBoundAction, false, Enum.KeyCode.F)
	ContextActionService:BindAction("TOEU_Dash", handleBoundAction, false, Enum.KeyCode.Q)
	ContextActionService:BindAction("TOEU_Mechanic", handleBoundAction, false, Enum.KeyCode.R)
	ContextActionService:BindAction("TOEU_Breakthrough", handleBoundAction, false, Enum.KeyCode.G)
	ContextActionService:BindAction(
		"TOEU_Sprint",
		handleBoundAction,
		false,
		Enum.KeyCode.LeftShift,
		Enum.KeyCode.RightShift
	)
end

local function isPointerInput(inputObject: InputObject): boolean
	return inputObject.UserInputType == Enum.UserInputType.Touch
		or inputObject.UserInputType == Enum.UserInputType.MouseButton1
end

local function bindTouchControls()
	local playerGui = localPlayer:WaitForChild("PlayerGui", 10)
	if playerGui == nil then
		warn("InputController could not find PlayerGui; touch controls are unavailable")
		return
	end

	local gameHud = playerGui:WaitForChild("GameHUD", 10)
	if gameHud == nil or not gameHud:IsA("ScreenGui") then
		warn("InputController could not find PlayerGui.GameHUD; touch controls are unavailable")
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

	for buttonName, definition in definitionByButton do
		local button = controls:FindFirstChild(buttonName)
		if button == nil or not button:IsA("GuiButton") then
			warn(`InputController could not find touch button {buttonName}`)
			continue
		end

		table.insert(
			connections,
			button.InputBegan:Connect(function(inputObject: InputObject)
				if not isPointerInput(inputObject) then
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
	bindKeyboardAndMouse()
	bindTouchControls()
end

function InputController.Stop()
	if not started then
		return
	end

	started = false

	for _, definition in ACTION_DEFINITIONS do
		ContextActionService:UnbindAction(definition.bindingName)
		actionDown[definition.action] = false
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
