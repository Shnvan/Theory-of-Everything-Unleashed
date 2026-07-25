--!strict

local InputController = require(script.Parent.Controllers.InputController)

InputController.Start()

script.Destroying:Connect(function()
	InputController.Stop()
end)
