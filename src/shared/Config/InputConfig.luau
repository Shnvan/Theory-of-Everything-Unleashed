--!strict

--[[
	The single source of truth for what each combat action is bound to.

	Previously the client controller held this three times over: once in its
	definition table, once as re-typed string literals at bind time, and once
	again at unbind time. A typo in any copy produced a silently dead action,
	because the bind name would not match the lookup used to dispatch it.

	Shared rather than client-local for two reasons. The server validates the
	same action set, and mobile parity is a pillar-level constraint
	(docs/PROJECT_BRIEF.md), so the touch-button contract needs to be visible to
	anything that reasons about it. The Studio-side GUI those button names refer
	to is specified in docs/HUD_AND_UI_SPEC.md.

	Keyboard bindings are DEFAULT and match the table in docs/COMBAT_SYSTEM.md.
	Shift is `Walk`, a deliberate slow-down, because sprinting is automatic at
	full movement input and therefore not an input action at all. Recorded as
	D-028, which supersedes D-021.
]]

local CombatTypes = require(script.Parent.Parent.Types.CombatTypes)

type ActionName = CombatTypes.ActionName

-- ContextActionService:BindAction accepts both KeyCode and UserInputType, and
-- the basic attack is a mouse button while everything else is a key.
export type ActionInputSource = Enum.KeyCode | Enum.UserInputType

export type ActionDefinition = {
	action: ActionName,
	-- ContextActionService binding name. Prefixed so it cannot collide with a
	-- binding created by another system or by Roblox's own player scripts.
	bindingName: string,
	-- Name of the GuiButton under GameHUD.TouchControls that triggers this
	-- action. See docs/HUD_AND_UI_SPEC.md for the required GUI tree.
	--
	-- Optional, because not every action needs a touch button. `Walk` has none:
	-- the mobile thumbstick is analogue, so pushing it part-way already walks,
	-- while a keyboard is binary and needs an explicit modifier. An action with
	-- no button here simply never appears in DEFINITION_BY_TOUCH_BUTTON.
	touchButtonName: string?,
	-- Hold actions report End and Cancel. Tap actions report Begin only.
	isHoldAction: boolean,
	-- Passed straight to ContextActionService:BindAction.
	inputs: { ActionInputSource },
}

local InputConfig = {}

-- Annotated rather than cast, so each entry is checked against ActionDefinition
-- individually. Casting the whole array instead lets Luau infer a narrower
-- element type from the first entry, which then conflicts with the union in
-- `inputs`. Frozen after construction by freezeDefinitions below.
local ACTION_DEFINITIONS: { ActionDefinition } = {
	{
		action = "BasicAttack",
		bindingName = "TOEU_BasicAttack",
		touchButtonName = "BasicAttackButton",
		isHoldAction = false,
		inputs = { Enum.UserInputType.MouseButton1 },
	},
	{
		action = "Ability1",
		bindingName = "TOEU_Ability1",
		touchButtonName = "Ability1Button",
		isHoldAction = false,
		inputs = { Enum.KeyCode.One },
	},
	{
		action = "Ability2",
		bindingName = "TOEU_Ability2",
		touchButtonName = "Ability2Button",
		isHoldAction = false,
		inputs = { Enum.KeyCode.Two },
	},
	{
		action = "Ability3",
		bindingName = "TOEU_Ability3",
		touchButtonName = "Ability3Button",
		isHoldAction = false,
		inputs = { Enum.KeyCode.Three },
	},
	{
		action = "Ability4",
		bindingName = "TOEU_Ability4",
		touchButtonName = "Ability4Button",
		isHoldAction = false,
		inputs = { Enum.KeyCode.Four },
	},
	{
		action = "Block",
		bindingName = "TOEU_Block",
		touchButtonName = "BlockButton",
		isHoldAction = true,
		inputs = { Enum.KeyCode.F },
	},
	{
		action = "Dash",
		bindingName = "TOEU_Dash",
		touchButtonName = "DashButton",
		isHoldAction = false,
		inputs = { Enum.KeyCode.Q },
	},
	{
		action = "Mechanic",
		bindingName = "TOEU_Mechanic",
		touchButtonName = "MechanicButton",
		isHoldAction = false,
		inputs = { Enum.KeyCode.R },
	},
	{
		action = "Breakthrough",
		bindingName = "TOEU_Breakthrough",
		touchButtonName = "BreakthroughButton",
		isHoldAction = false,
		inputs = { Enum.KeyCode.G },
	},
	{
		action = "Walk",
		bindingName = "TOEU_Walk",
		-- No touch button by design; see the ActionDefinition comment above.
		touchButtonName = nil,
		isHoldAction = true,
		inputs = { Enum.KeyCode.LeftShift, Enum.KeyCode.RightShift },
	},
}

--[[
	Fails loudly at require time if a definition's `isHoldAction` disagrees with
	CombatTypes.HOLD_ACTIONS. The two are separate because the server needs the
	hold set without needing keybinds, and a silent disagreement between them
	would make an unmatched Begin look like a protocol error on one side and
	normal on the other.
]]
local function assertHoldActionsAgree()
	for _, definition in ACTION_DEFINITIONS do
		local sharedSaysHold = CombatTypes.isHoldAction(definition.action)
		if definition.isHoldAction ~= sharedSaysHold then
			error(
				`InputConfig and CombatTypes disagree about whether {definition.action} is a hold action`
					.. ` (InputConfig: {definition.isHoldAction}, CombatTypes: {sharedSaysHold})`
			)
		end
	end
end

--[[
	Freezes each definition and its input list, then the outer array. Done after
	construction rather than inline so the annotation above can typecheck the
	`inputs` union; freezing inline narrows the inferred element type.
]]
local function freezeDefinitions()
	for _, definition in ACTION_DEFINITIONS do
		table.freeze(definition.inputs)
		table.freeze(definition)
	end

	table.freeze(ACTION_DEFINITIONS)
end

assertHoldActionsAgree()
freezeDefinitions()

InputConfig.ACTION_DEFINITIONS = ACTION_DEFINITIONS

-- Derived lookups rather than hand-maintained parallel tables.
local definitionByBinding: { [string]: ActionDefinition } = {}
local definitionByTouchButton: { [string]: ActionDefinition } = {}

for _, definition in ACTION_DEFINITIONS do
	definitionByBinding[definition.bindingName] = definition

	-- Actions without a touch button are simply absent from this map, so the
	-- input layer never looks for a GuiButton that the HUD spec does not list.
	local touchButtonName = definition.touchButtonName
	if touchButtonName ~= nil then
		definitionByTouchButton[touchButtonName] = definition
	end
end

InputConfig.DEFINITION_BY_BINDING = table.freeze(definitionByBinding)
InputConfig.DEFINITION_BY_TOUCH_BUTTON = table.freeze(definitionByTouchButton)

return table.freeze(InputConfig)
