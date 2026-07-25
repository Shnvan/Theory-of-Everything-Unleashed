--!strict

--[[
	Client entry point. Starts the client controllers in dependency order.

	Kept deliberately thin: this file decides startup order and nothing else. Any
	logic that belongs to a system belongs in that system's controller.

	Note on teardown. A LocalScript in StarterPlayerScripts lives for the whole
	session; its children are not destroyed on character respawn, so
	`script.Destroying` would essentially never fire and is not a usable cleanup
	hook. Controllers must therefore handle character lifecycle internally rather
	than relying on this script to stop them. `Stop()` exists for tests and for
	an explicit shutdown, not as an automatic path.
]]

local InputController = require(script.Parent.Controllers.InputController)
local MovementController = require(script.Parent.Controllers.MovementController)

-- Order matters: MovementController subscribes to InputController's action
-- signal and queries its hold state, so input must be live first.
InputController.Start()
MovementController.Start()
