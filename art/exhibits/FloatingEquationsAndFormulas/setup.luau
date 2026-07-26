--!strict
--[[
	Setup script for the Foundational Equations of Physics exhibit.

	Second Luau-driven exhibit in the project (after PeriodicTableWalls). Not a
	Blender exhibit -- equations are text, and Roblox's SurfaceGui + TextLabel
	is the natural way to display them (vector-scaled text, no textures, no
	upload).

	Committed source of truth: this file. Run once via MCP execute_luau to
	build the wall + SurfaceGui + 12 equation tiles. Idempotent: destroys any
	prior ProductionMesh first.

	Equation list is the standard textbook canon covering the six major
	domains of physics. Any single equation is a curatorial choice and the
	dossier discloses them.
]]

local ChangeHistoryService = game:GetService("ChangeHistoryService")

-- ---------------------------------------------------------------------------
-- Equations
-- ---------------------------------------------------------------------------

type Equation = { text: string, name: string, domain: string }

local EQUATIONS: { Equation } = {
	{ text = "F = ma",             name = "Newton's Second Law",    domain = "mechanics"   },
	{ text = "F = G · m₁m₂ / r²",   name = "Universal Gravitation",  domain = "gravity"     },
	{ text = "T² ∝ a³",             name = "Kepler's Third Law",     domain = "gravity"     },
	{ text = "F = k · q₁q₂ / r²",   name = "Coulomb's Law",          domain = "em"          },
	{ text = "ε = -dΦ / dt",        name = "Faraday's Law",          domain = "em"          },
	{ text = "∮ E · dA = Q / ε₀",   name = "Gauss's Law",            domain = "em"          },
	{ text = "PV = nRT",            name = "Ideal Gas Law",          domain = "thermo"      },
	{ text = "S = k · ln W",        name = "Boltzmann Entropy",      domain = "thermo"      },
	{ text = "E = mc²",             name = "Mass-Energy Equivalence", domain = "relativity" },
	{ text = "E = hf",              name = "Planck-Einstein Relation", domain = "quantum"   },
	{ text = "iℏ ∂ψ/∂t = Ĥψ",       name = "Schrödinger Equation",   domain = "quantum"     },
	{ text = "Δx · Δp ≥ ℏ / 2",     name = "Uncertainty Principle",  domain = "quantum"     },
}

local DOMAIN_COLORS: { [string]: Color3 } = {
	mechanics  = Color3.fromRGB(255, 200, 150),
	gravity    = Color3.fromRGB(180, 210, 250),
	em         = Color3.fromRGB(255, 235, 150),
	thermo     = Color3.fromRGB(200, 235, 200),
	relativity = Color3.fromRGB(220, 200, 240),
	quantum    = Color3.fromRGB(190, 230, 230),
}

local DOMAIN_LABELS: { [string]: string } = {
	mechanics  = "MECHANICS",
	gravity    = "GRAVITY",
	em         = "ELECTROMAGNETISM",
	thermo     = "THERMODYNAMICS",
	relativity = "RELATIVITY",
	quantum    = "QUANTUM",
}

-- ---------------------------------------------------------------------------
-- Geometry
-- ---------------------------------------------------------------------------

-- Shell 43.20 x 54 x 31.50, plinth top Y 8.16. Wall centred on shell.
-- Studio placement position and yaw will be read from the shell at run-time.
local WALL_WIDTH = 40.0
local WALL_HEIGHT = 30.0
local WALL_THICKNESS = 5.0
local WALL_CENTRE_Y = 8.16 + WALL_HEIGHT / 2 + 2.0  -- some clearance above plinth

local exhibit = game.Workspace.TheOmniscienceColiseum.ExhibitSectors.Northwest_HallOfMinds.FloatingEquationsAndFormulas
local shell = exhibit.CollisionShells.PrimaryCollisionShell

-- Place the wall at the shell's own centre X/Z and yaw. That guarantees the
-- wall aligns with the exhibit's approach direction without hard-coded angles.
local shell_yaw = select(2, shell.CFrame:ToEulerAnglesYXZ())
local WALL_CFRAME = CFrame.new(shell.Position.X, WALL_CENTRE_Y, shell.Position.Z) * CFrame.Angles(0, shell_yaw, 0)
local WALL_SIZE = Vector3.new(WALL_WIDTH, WALL_HEIGHT, WALL_THICKNESS)

-- Grid layout: 4 columns x 3 rows = 12 tiles
local COLS = 4
local ROWS = 3

-- ---------------------------------------------------------------------------
-- Baseline + hide prototypes
-- ---------------------------------------------------------------------------

local function computeAabb(model: Instance): (Vector3, Vector3)
	local lo = Vector3.new(math.huge, math.huge, math.huge)
	local hi = Vector3.new(-math.huge, -math.huge, -math.huge)
	for _, d in ipairs(model:GetDescendants()) do
		if d:IsA("BasePart") then
			local c, s = d.CFrame, d.Size / 2
			for i = -1, 1, 2 do
				for j = -1, 1, 2 do
					for k = -1, 1, 2 do
						local p = c * CFrame.new(s.X * i, s.Y * j, s.Z * k)
						lo = Vector3.new(math.min(lo.X, p.X), math.min(lo.Y, p.Y), math.min(lo.Z, p.Z))
						hi = Vector3.new(math.max(hi.X, p.X), math.max(hi.Y, p.Y), math.max(hi.Z, p.Z))
					end
				end
			end
		end
	end
	return lo, hi
end
local lo0, hi0 = computeAabb(exhibit)

local preserved = { CollisionShells = true, Plinth = true, LabelAnchor = true, NamePlaque = true, VisualDetail = true }
local proto = {}
for _, c in ipairs(exhibit:GetChildren()) do
	if c:IsA("BasePart") and not preserved[c.Name] then table.insert(proto, c) end
end
local vd = exhibit:FindFirstChild("VisualDetail")
if vd then
	for _, d in ipairs(vd:GetDescendants()) do
		if d:IsA("BasePart") then table.insert(proto, d) end
	end
end

local existing = exhibit:FindFirstChild("ProductionMesh")
if existing then existing:Destroy() end

local label = exhibit.NamePlaque.InscriptionStone.Inscription.ExhibitName
local oldText = label.Text

-- ---------------------------------------------------------------------------
-- Build
-- ---------------------------------------------------------------------------

local recording = ChangeHistoryService:TryBeginRecording("Build Foundational Equations exhibit")

local wall = Instance.new("Part")
wall.Name = "ProductionMesh"
wall.Size = WALL_SIZE
wall.CFrame = WALL_CFRAME
wall.Anchored = true
wall.CanCollide = false
wall.Material = Enum.Material.Metal
wall.BrickColor = BrickColor.new("Br. yellowish orange")
wall.TopSurface = Enum.SurfaceType.Smooth
wall.BottomSurface = Enum.SurfaceType.Smooth
wall.Parent = exhibit

local gui = Instance.new("SurfaceGui")
gui.Name = "EquationsWall"
gui.Face = Enum.NormalId.Front
gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
gui.PixelsPerStud = 50
gui.CanvasSize = Vector2.new(WALL_SIZE.X * 50, WALL_SIZE.Y * 50)
gui.LightInfluence = 0
gui.Parent = wall

-- Title
local title = Instance.new("TextLabel")
title.Name = "Title"
title.Text = "FOUNDATIONAL EQUATIONS OF PHYSICS"
title.Font = Enum.Font.SourceSansBold
title.TextScaled = true
title.BackgroundTransparency = 1
title.TextColor3 = Color3.fromRGB(30, 20, 10)
title.Size = UDim2.fromScale(0.9, 0.08)
title.Position = UDim2.fromScale(0.05, 0.01)
title.Parent = gui

-- Grid layout
local GRID_TOP = 0.11
local GRID_BOTTOM = 0.99
local CELL_MARGIN = 0.08

for i, e in ipairs(EQUATIONS) do
	local zero = i - 1
	local row = math.floor(zero / COLS) + 1
	local col = (zero % COLS) + 1

	local cellW = 1.0 / COLS
	local cellH = (GRID_BOTTOM - GRID_TOP) / ROWS
	local cx = (col - 0.5) * cellW
	local cy = GRID_TOP + (row - 0.5) * cellH

	local tile = Instance.new("Frame")
	tile.Name = string.format("Eq_%02d", i)
	tile.AnchorPoint = Vector2.new(0.5, 0.5)
	tile.Position = UDim2.fromScale(cx, cy)
	tile.Size = UDim2.fromScale(cellW * (1 - CELL_MARGIN), cellH * (1 - CELL_MARGIN))
	tile.BackgroundColor3 = DOMAIN_COLORS[e.domain] or Color3.fromRGB(220, 220, 220)
	tile.BorderSizePixel = 0
	tile.Parent = gui

	local border = Instance.new("UIStroke")
	border.Thickness = 1
	border.Color = Color3.fromRGB(60, 40, 20)
	border.Parent = tile

	-- Domain label (top strip)
	local domainLabel = Instance.new("TextLabel")
	domainLabel.Name = "Domain"
	domainLabel.Text = DOMAIN_LABELS[e.domain] or ""
	domainLabel.Font = Enum.Font.SourceSansBold
	domainLabel.TextScaled = true
	domainLabel.BackgroundTransparency = 1
	domainLabel.TextColor3 = Color3.fromRGB(60, 40, 20)
	domainLabel.Size = UDim2.fromScale(0.94, 0.15)
	domainLabel.Position = UDim2.fromScale(0.03, 0.03)
	domainLabel.Parent = tile

	-- Equation text (large, centred)
	local eqLabel = Instance.new("TextLabel")
	eqLabel.Name = "Equation"
	eqLabel.Text = e.text
	eqLabel.Font = Enum.Font.SourceSansBold
	eqLabel.TextScaled = true
	eqLabel.BackgroundTransparency = 1
	eqLabel.TextColor3 = Color3.fromRGB(20, 15, 5)
	eqLabel.Size = UDim2.fromScale(0.94, 0.45)
	eqLabel.Position = UDim2.fromScale(0.03, 0.24)
	eqLabel.Parent = tile

	-- Named title (bottom)
	local nameLabel = Instance.new("TextLabel")
	nameLabel.Name = "EquationName"
	nameLabel.Text = e.name
	nameLabel.Font = Enum.Font.SourceSans
	nameLabel.TextScaled = true
	nameLabel.BackgroundTransparency = 1
	nameLabel.TextColor3 = Color3.fromRGB(40, 25, 15)
	nameLabel.Size = UDim2.fromScale(0.94, 0.25)
	nameLabel.Position = UDim2.fromScale(0.03, 0.72)
	nameLabel.Parent = tile
end

-- Hide prototype parts + their child GUIs (lesson from periodic table)
for _, p in ipairs(proto) do
	if p:GetAttribute("PrototypeOriginalTransparency") == nil then
		p:SetAttribute("PrototypeOriginalTransparency", p.Transparency)
		p:SetAttribute("PrototypeOriginalCanCollide", p.CanCollide)
	end
	p.Transparency = 1
	p.CanCollide = false
	for _, child in ipairs(p:GetDescendants()) do
		if child:IsA("SurfaceGui") or child:IsA("BillboardGui") then
			if child:GetAttribute("PrototypeOriginalEnabled") == nil then
				child:SetAttribute("PrototypeOriginalEnabled", child.Enabled)
			end
			child.Enabled = false
		end
	end
end

label.Text = "FOUNDATIONAL EQUATIONS OF PHYSICS"
exhibit:SetAttribute("DisplayName", "FOUNDATIONAL EQUATIONS OF PHYSICS")

if recording then
	ChangeHistoryService:FinishRecording(recording, Enum.FinishRecordingOperation.Commit)
end

-- Verify
local lo1, hi1 = computeAabb(exhibit)
local delta = { lo1.X - lo0.X, lo1.Y - lo0.Y, lo1.Z - lo0.Z, hi1.X - hi0.X, hi1.Y - hi0.Y, hi1.Z - hi0.Z }
local colliders = {}
for _, d in ipairs(exhibit:GetDescendants()) do
	if d:IsA("BasePart") and d.CanCollide then table.insert(colliders, d.Name) end
end
local eqTiles = 0
for _, c in ipairs(gui:GetChildren()) do
	if c.Name:sub(1, 3) == "Eq_" then eqTiles = eqTiles + 1 end
end

return string.format(
	"prototype hidden: %d\nequation tiles: %d (expect 12)\nwall size=%.1fx%.1fx%.1f pos=(%.1f,%.1f,%.1f)\nAABB delta: %.4f,%.4f,%.4f | %.4f,%.4f,%.4f\ncolliders: %d (%s)\nstone: %q -> %q",
	#proto, eqTiles,
	wall.Size.X, wall.Size.Y, wall.Size.Z, wall.Position.X, wall.Position.Y, wall.Position.Z,
	delta[1], delta[2], delta[3], delta[4], delta[5], delta[6],
	#colliders, table.concat(colliders, ","),
	oldText, label.Text
)
