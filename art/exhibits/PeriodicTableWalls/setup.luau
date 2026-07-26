--!strict
--[[
	Setup script for the IUPAC Periodic Table of the Elements exhibit.

	This is the committed source of truth for the exhibit's content and layout.
	It is not a runtime script -- run it once through the Roblox Studio MCP
	tool's execute_luau against the Edit datamodel to (re-)build the exhibit's
	wall, SurfaceGui, and 118 element cells. Running it again is idempotent:
	an existing ProductionMesh is removed first.

	Not a Blender exhibit. The Life & Computation sector introduces text-and-
	data displays that don't fit the mesh pipeline; this is that pipeline
	change made once so the AI lab can build on it if needed.

	Element data below is transcribed from the current IUPAC list. Atomic
	weights for elements with no stable isotope are shown as the mass number
	of the longest-lived isotope, in brackets, following the IUPAC convention.

	Source: iupac.org/what-we-do/periodic-table-of-elements/ (accessed 2026-07-26).
]]

local ChangeHistoryService = game:GetService("ChangeHistoryService")

-- ---------------------------------------------------------------------------
-- Element data
-- ---------------------------------------------------------------------------

type Element = { z: number, sym: string, name: string, mass: string, cat: string }

local ELEMENTS: { Element } = {
	{ z = 1,   sym = "H",   name = "Hydrogen",       mass = "1.008",     cat = "nonmetal"        },
	{ z = 2,   sym = "He",  name = "Helium",         mass = "4.003",     cat = "noble"           },
	{ z = 3,   sym = "Li",  name = "Lithium",        mass = "6.94",      cat = "alkali"          },
	{ z = 4,   sym = "Be",  name = "Beryllium",      mass = "9.012",     cat = "alkaline"        },
	{ z = 5,   sym = "B",   name = "Boron",          mass = "10.81",     cat = "metalloid"       },
	{ z = 6,   sym = "C",   name = "Carbon",         mass = "12.011",    cat = "nonmetal"        },
	{ z = 7,   sym = "N",   name = "Nitrogen",       mass = "14.007",    cat = "nonmetal"        },
	{ z = 8,   sym = "O",   name = "Oxygen",         mass = "15.999",    cat = "nonmetal"        },
	{ z = 9,   sym = "F",   name = "Fluorine",       mass = "18.998",    cat = "halogen"         },
	{ z = 10,  sym = "Ne",  name = "Neon",           mass = "20.180",    cat = "noble"           },
	{ z = 11,  sym = "Na",  name = "Sodium",         mass = "22.990",    cat = "alkali"          },
	{ z = 12,  sym = "Mg",  name = "Magnesium",      mass = "24.305",    cat = "alkaline"        },
	{ z = 13,  sym = "Al",  name = "Aluminium",      mass = "26.982",    cat = "post_transition" },
	{ z = 14,  sym = "Si",  name = "Silicon",        mass = "28.085",    cat = "metalloid"       },
	{ z = 15,  sym = "P",   name = "Phosphorus",     mass = "30.974",    cat = "nonmetal"        },
	{ z = 16,  sym = "S",   name = "Sulfur",         mass = "32.06",     cat = "nonmetal"        },
	{ z = 17,  sym = "Cl",  name = "Chlorine",       mass = "35.45",     cat = "halogen"         },
	{ z = 18,  sym = "Ar",  name = "Argon",          mass = "39.95",     cat = "noble"           },
	{ z = 19,  sym = "K",   name = "Potassium",      mass = "39.098",    cat = "alkali"          },
	{ z = 20,  sym = "Ca",  name = "Calcium",        mass = "40.078",    cat = "alkaline"        },
	{ z = 21,  sym = "Sc",  name = "Scandium",       mass = "44.956",    cat = "transition"      },
	{ z = 22,  sym = "Ti",  name = "Titanium",       mass = "47.867",    cat = "transition"      },
	{ z = 23,  sym = "V",   name = "Vanadium",       mass = "50.942",    cat = "transition"      },
	{ z = 24,  sym = "Cr",  name = "Chromium",       mass = "51.996",    cat = "transition"      },
	{ z = 25,  sym = "Mn",  name = "Manganese",      mass = "54.938",    cat = "transition"      },
	{ z = 26,  sym = "Fe",  name = "Iron",           mass = "55.845",    cat = "transition"      },
	{ z = 27,  sym = "Co",  name = "Cobalt",         mass = "58.933",    cat = "transition"      },
	{ z = 28,  sym = "Ni",  name = "Nickel",         mass = "58.693",    cat = "transition"      },
	{ z = 29,  sym = "Cu",  name = "Copper",         mass = "63.546",    cat = "transition"      },
	{ z = 30,  sym = "Zn",  name = "Zinc",           mass = "65.38",     cat = "transition"      },
	{ z = 31,  sym = "Ga",  name = "Gallium",        mass = "69.723",    cat = "post_transition" },
	{ z = 32,  sym = "Ge",  name = "Germanium",      mass = "72.630",    cat = "metalloid"       },
	{ z = 33,  sym = "As",  name = "Arsenic",        mass = "74.922",    cat = "metalloid"       },
	{ z = 34,  sym = "Se",  name = "Selenium",       mass = "78.971",    cat = "nonmetal"        },
	{ z = 35,  sym = "Br",  name = "Bromine",        mass = "79.904",    cat = "halogen"         },
	{ z = 36,  sym = "Kr",  name = "Krypton",        mass = "83.798",    cat = "noble"           },
	{ z = 37,  sym = "Rb",  name = "Rubidium",       mass = "85.468",    cat = "alkali"          },
	{ z = 38,  sym = "Sr",  name = "Strontium",      mass = "87.62",     cat = "alkaline"        },
	{ z = 39,  sym = "Y",   name = "Yttrium",        mass = "88.906",    cat = "transition"      },
	{ z = 40,  sym = "Zr",  name = "Zirconium",      mass = "91.224",    cat = "transition"      },
	{ z = 41,  sym = "Nb",  name = "Niobium",        mass = "92.906",    cat = "transition"      },
	{ z = 42,  sym = "Mo",  name = "Molybdenum",     mass = "95.95",     cat = "transition"      },
	{ z = 43,  sym = "Tc",  name = "Technetium",     mass = "[98]",      cat = "transition"      },
	{ z = 44,  sym = "Ru",  name = "Ruthenium",      mass = "101.07",    cat = "transition"      },
	{ z = 45,  sym = "Rh",  name = "Rhodium",        mass = "102.906",   cat = "transition"      },
	{ z = 46,  sym = "Pd",  name = "Palladium",      mass = "106.42",    cat = "transition"      },
	{ z = 47,  sym = "Ag",  name = "Silver",         mass = "107.868",   cat = "transition"      },
	{ z = 48,  sym = "Cd",  name = "Cadmium",        mass = "112.414",   cat = "transition"      },
	{ z = 49,  sym = "In",  name = "Indium",         mass = "114.818",   cat = "post_transition" },
	{ z = 50,  sym = "Sn",  name = "Tin",            mass = "118.710",   cat = "post_transition" },
	{ z = 51,  sym = "Sb",  name = "Antimony",       mass = "121.760",   cat = "metalloid"       },
	{ z = 52,  sym = "Te",  name = "Tellurium",      mass = "127.60",    cat = "metalloid"       },
	{ z = 53,  sym = "I",   name = "Iodine",         mass = "126.904",   cat = "halogen"         },
	{ z = 54,  sym = "Xe",  name = "Xenon",          mass = "131.293",   cat = "noble"           },
	{ z = 55,  sym = "Cs",  name = "Caesium",        mass = "132.905",   cat = "alkali"          },
	{ z = 56,  sym = "Ba",  name = "Barium",         mass = "137.327",   cat = "alkaline"        },
	{ z = 57,  sym = "La",  name = "Lanthanum",      mass = "138.905",   cat = "lanthanide"      },
	{ z = 58,  sym = "Ce",  name = "Cerium",         mass = "140.116",   cat = "lanthanide"      },
	{ z = 59,  sym = "Pr",  name = "Praseodymium",   mass = "140.908",   cat = "lanthanide"      },
	{ z = 60,  sym = "Nd",  name = "Neodymium",      mass = "144.242",   cat = "lanthanide"      },
	{ z = 61,  sym = "Pm",  name = "Promethium",     mass = "[145]",     cat = "lanthanide"      },
	{ z = 62,  sym = "Sm",  name = "Samarium",       mass = "150.36",    cat = "lanthanide"      },
	{ z = 63,  sym = "Eu",  name = "Europium",       mass = "151.964",   cat = "lanthanide"      },
	{ z = 64,  sym = "Gd",  name = "Gadolinium",     mass = "157.25",    cat = "lanthanide"      },
	{ z = 65,  sym = "Tb",  name = "Terbium",        mass = "158.925",   cat = "lanthanide"      },
	{ z = 66,  sym = "Dy",  name = "Dysprosium",     mass = "162.500",   cat = "lanthanide"      },
	{ z = 67,  sym = "Ho",  name = "Holmium",        mass = "164.930",   cat = "lanthanide"      },
	{ z = 68,  sym = "Er",  name = "Erbium",         mass = "167.259",   cat = "lanthanide"      },
	{ z = 69,  sym = "Tm",  name = "Thulium",        mass = "168.934",   cat = "lanthanide"      },
	{ z = 70,  sym = "Yb",  name = "Ytterbium",      mass = "173.045",   cat = "lanthanide"      },
	{ z = 71,  sym = "Lu",  name = "Lutetium",       mass = "174.967",   cat = "lanthanide"      },
	{ z = 72,  sym = "Hf",  name = "Hafnium",        mass = "178.49",    cat = "transition"      },
	{ z = 73,  sym = "Ta",  name = "Tantalum",       mass = "180.948",   cat = "transition"      },
	{ z = 74,  sym = "W",   name = "Tungsten",       mass = "183.84",    cat = "transition"      },
	{ z = 75,  sym = "Re",  name = "Rhenium",        mass = "186.207",   cat = "transition"      },
	{ z = 76,  sym = "Os",  name = "Osmium",         mass = "190.23",    cat = "transition"      },
	{ z = 77,  sym = "Ir",  name = "Iridium",        mass = "192.217",   cat = "transition"      },
	{ z = 78,  sym = "Pt",  name = "Platinum",       mass = "195.084",   cat = "transition"      },
	{ z = 79,  sym = "Au",  name = "Gold",           mass = "196.967",   cat = "transition"      },
	{ z = 80,  sym = "Hg",  name = "Mercury",        mass = "200.592",   cat = "transition"      },
	{ z = 81,  sym = "Tl",  name = "Thallium",       mass = "204.38",    cat = "post_transition" },
	{ z = 82,  sym = "Pb",  name = "Lead",           mass = "207.2",     cat = "post_transition" },
	{ z = 83,  sym = "Bi",  name = "Bismuth",        mass = "208.980",   cat = "post_transition" },
	{ z = 84,  sym = "Po",  name = "Polonium",       mass = "[209]",     cat = "post_transition" },
	{ z = 85,  sym = "At",  name = "Astatine",       mass = "[210]",     cat = "halogen"         },
	{ z = 86,  sym = "Rn",  name = "Radon",          mass = "[222]",     cat = "noble"           },
	{ z = 87,  sym = "Fr",  name = "Francium",       mass = "[223]",     cat = "alkali"          },
	{ z = 88,  sym = "Ra",  name = "Radium",         mass = "[226]",     cat = "alkaline"        },
	{ z = 89,  sym = "Ac",  name = "Actinium",       mass = "[227]",     cat = "actinide"        },
	{ z = 90,  sym = "Th",  name = "Thorium",        mass = "232.038",   cat = "actinide"        },
	{ z = 91,  sym = "Pa",  name = "Protactinium",   mass = "231.036",   cat = "actinide"        },
	{ z = 92,  sym = "U",   name = "Uranium",        mass = "238.029",   cat = "actinide"        },
	{ z = 93,  sym = "Np",  name = "Neptunium",      mass = "[237]",     cat = "actinide"        },
	{ z = 94,  sym = "Pu",  name = "Plutonium",      mass = "[244]",     cat = "actinide"        },
	{ z = 95,  sym = "Am",  name = "Americium",      mass = "[243]",     cat = "actinide"        },
	{ z = 96,  sym = "Cm",  name = "Curium",         mass = "[247]",     cat = "actinide"        },
	{ z = 97,  sym = "Bk",  name = "Berkelium",      mass = "[247]",     cat = "actinide"        },
	{ z = 98,  sym = "Cf",  name = "Californium",    mass = "[251]",     cat = "actinide"        },
	{ z = 99,  sym = "Es",  name = "Einsteinium",    mass = "[252]",     cat = "actinide"        },
	{ z = 100, sym = "Fm",  name = "Fermium",        mass = "[257]",     cat = "actinide"        },
	{ z = 101, sym = "Md",  name = "Mendelevium",    mass = "[258]",     cat = "actinide"        },
	{ z = 102, sym = "No",  name = "Nobelium",       mass = "[259]",     cat = "actinide"        },
	{ z = 103, sym = "Lr",  name = "Lawrencium",     mass = "[266]",     cat = "actinide"        },
	{ z = 104, sym = "Rf",  name = "Rutherfordium",  mass = "[267]",     cat = "transition"      },
	{ z = 105, sym = "Db",  name = "Dubnium",        mass = "[268]",     cat = "transition"      },
	{ z = 106, sym = "Sg",  name = "Seaborgium",     mass = "[269]",     cat = "transition"      },
	{ z = 107, sym = "Bh",  name = "Bohrium",        mass = "[270]",     cat = "transition"      },
	{ z = 108, sym = "Hs",  name = "Hassium",        mass = "[269]",     cat = "transition"      },
	{ z = 109, sym = "Mt",  name = "Meitnerium",     mass = "[278]",     cat = "unknown"         },
	{ z = 110, sym = "Ds",  name = "Darmstadtium",   mass = "[281]",     cat = "unknown"         },
	{ z = 111, sym = "Rg",  name = "Roentgenium",    mass = "[282]",     cat = "unknown"         },
	{ z = 112, sym = "Cn",  name = "Copernicium",    mass = "[285]",     cat = "transition"      },
	{ z = 113, sym = "Nh",  name = "Nihonium",       mass = "[286]",     cat = "unknown"         },
	{ z = 114, sym = "Fl",  name = "Flerovium",      mass = "[289]",     cat = "unknown"         },
	{ z = 115, sym = "Mc",  name = "Moscovium",      mass = "[289]",     cat = "unknown"         },
	{ z = 116, sym = "Lv",  name = "Livermorium",    mass = "[293]",     cat = "unknown"         },
	{ z = 117, sym = "Ts",  name = "Tennessine",     mass = "[294]",     cat = "unknown"         },
	{ z = 118, sym = "Og",  name = "Oganesson",      mass = "[294]",     cat = "unknown"         },
}

-- Category background colours. Pastel palette that reads on brass and keeps
-- black text legible.
local CATEGORY_COLORS: { [string]: Color3 } = {
	alkali          = Color3.fromRGB(255, 179, 128),
	alkaline        = Color3.fromRGB(255, 217, 128),
	transition      = Color3.fromRGB(255, 189, 189),
	post_transition = Color3.fromRGB(210, 200, 220),
	metalloid       = Color3.fromRGB(190, 230, 220),
	nonmetal        = Color3.fromRGB(190, 235, 190),
	halogen         = Color3.fromRGB(230, 240, 160),
	noble           = Color3.fromRGB(180, 220, 250),
	lanthanide      = Color3.fromRGB(240, 200, 220),
	actinide        = Color3.fromRGB(240, 195, 190),
	unknown         = Color3.fromRGB(220, 220, 220),
}

-- Standard 18-column IUPAC layout. Returns (row, col) 1-indexed.
-- Lanthanides go on row 9, actinides on row 10, with row 8 as a visual gap.
local function gridPosition(z: number): (number, number)
	if z == 1 then return 1, 1 end
	if z == 2 then return 1, 18 end
	if z == 3 then return 2, 1 end
	if z == 4 then return 2, 2 end
	if z >= 5 and z <= 10 then return 2, z + 8 end
	if z == 11 then return 3, 1 end
	if z == 12 then return 3, 2 end
	if z >= 13 and z <= 18 then return 3, z end
	if z == 19 then return 4, 1 end
	if z == 20 then return 4, 2 end
	if z >= 21 and z <= 30 then return 4, z - 18 end
	if z >= 31 and z <= 36 then return 4, z - 18 end
	if z == 37 then return 5, 1 end
	if z == 38 then return 5, 2 end
	if z >= 39 and z <= 54 then return 5, z - 36 end
	if z == 55 then return 6, 1 end
	if z == 56 then return 6, 2 end
	if z >= 57 and z <= 71 then return 9, z - 54 end
	if z >= 72 and z <= 86 then return 6, z - 68 end
	if z == 87 then return 7, 1 end
	if z == 88 then return 7, 2 end
	if z >= 89 and z <= 103 then return 10, z - 86 end
	if z >= 104 and z <= 118 then return 7, z - 100 end
	error("no grid position for z=" .. tostring(z))
end

-- ---------------------------------------------------------------------------
-- Placement geometry
-- ---------------------------------------------------------------------------

-- Reuse the prototype Wall's exact CFrame and size, so the exhibit footprint
-- doesn't change (D-017). Wall is a Studio Part, not a Blender mesh; text-and-
-- data displays don't need meshes.
local WALL_CFRAME = CFrame.new(170.57, 28.16, -153.58) * CFrame.Angles(0, math.rad(132.0), 0)
local WALL_SIZE = Vector3.new(60.0, 45.0, 5.0)

-- Rows counted from top; 10 rows total counting the f-block strip and gap.
local ROWS = 10
local COLS = 18

-- ---------------------------------------------------------------------------
-- Main build
-- ---------------------------------------------------------------------------

local exhibit = game.Workspace.TheOmniscienceColiseum.ExhibitSectors.Southwest_LifeAndComputation.PeriodicTableWalls

-- Compute baseline AABB so we can prove nothing moved
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

-- Preserved children (keep untouched)
local preserved = {
	CollisionShells = true, Plinth = true, LabelAnchor = true,
	NamePlaque = true, VisualDetail = true,
}

-- Prototype visual parts to hide
local proto = {}
for _, c in ipairs(exhibit:GetChildren()) do
	if c:IsA("BasePart") and not preserved[c.Name] then
		table.insert(proto, c)
	end
end
local visualDetail = exhibit:FindFirstChild("VisualDetail")
if visualDetail then
	for _, d in ipairs(visualDetail:GetDescendants()) do
		if d:IsA("BasePart") then
			table.insert(proto, d)
		end
	end
end

-- Idempotent: if a ProductionMesh already exists from a prior run, remove it.
local existing = exhibit:FindFirstChild("ProductionMesh")
if existing then
	existing:Destroy()
end

local label = exhibit.NamePlaque.InscriptionStone.Inscription.ExhibitName
local oldText = label.Text

local recording = ChangeHistoryService:TryBeginRecording("Build IUPAC Periodic Table exhibit")

-- Build the wall Part
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

-- SurfaceGui on the wall's Front face. Wall LookVector at yaw 132° points
-- toward the arena centre, so Front is what the viewer sees.
local gui = Instance.new("SurfaceGui")
gui.Name = "PeriodicTable"
gui.Face = Enum.NormalId.Front
gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
gui.PixelsPerStud = 50
gui.CanvasSize = Vector2.new(WALL_SIZE.X * 50, WALL_SIZE.Y * 50)
gui.LightInfluence = 0
gui.AlwaysOnTop = false
gui.Parent = wall

-- Title bar at the top
local title = Instance.new("TextLabel")
title.Name = "Title"
title.Text = "IUPAC PERIODIC TABLE OF THE ELEMENTS"
title.Font = Enum.Font.SourceSansBold
title.TextScaled = true
title.BackgroundTransparency = 1
title.TextColor3 = Color3.fromRGB(30, 20, 10)
title.Size = UDim2.fromScale(0.9, 0.05)
title.Position = UDim2.fromScale(0.05, 0.005)
title.Parent = gui

-- 118 element cells. Position each by its (row, col) in the 10x18 grid.
-- Content starts below the title, uses ~92% of vertical space.
local GRID_TOP = 0.07
local GRID_BOTTOM = 0.99
local CELL_MARGIN = 0.15  -- fraction of cell size used as spacing

for _, e in ipairs(ELEMENTS) do
	local row, col = gridPosition(e.z)

	local cellW = 1.0 / COLS
	local cellH = (GRID_BOTTOM - GRID_TOP) / ROWS

	local cx = (col - 0.5) * cellW
	local cy = GRID_TOP + (row - 0.5) * cellH

	local cell = Instance.new("Frame")
	cell.Name = string.format("El_%03d_%s", e.z, e.sym)
	cell.AnchorPoint = Vector2.new(0.5, 0.5)
	cell.Position = UDim2.fromScale(cx, cy)
	cell.Size = UDim2.fromScale(cellW * (1 - CELL_MARGIN), cellH * (1 - CELL_MARGIN))
	cell.BackgroundColor3 = CATEGORY_COLORS[e.cat] or CATEGORY_COLORS.unknown
	cell.BorderSizePixel = 0
	cell.Parent = gui

	local border = Instance.new("UIStroke")
	border.Thickness = 1
	border.Color = Color3.fromRGB(60, 40, 20)
	border.Parent = cell

	local number = Instance.new("TextLabel")
	number.Name = "AtomicNumber"
	number.Text = tostring(e.z)
	number.Font = Enum.Font.SourceSans
	number.TextScaled = true
	number.BackgroundTransparency = 1
	number.TextColor3 = Color3.fromRGB(30, 20, 10)
	number.TextXAlignment = Enum.TextXAlignment.Left
	number.Size = UDim2.fromScale(0.5, 0.22)
	number.Position = UDim2.fromScale(0.06, 0.04)
	number.Parent = cell

	local symbol = Instance.new("TextLabel")
	symbol.Name = "Symbol"
	symbol.Text = e.sym
	symbol.Font = Enum.Font.SourceSansBold
	symbol.TextScaled = true
	symbol.BackgroundTransparency = 1
	symbol.TextColor3 = Color3.fromRGB(20, 15, 5)
	symbol.Size = UDim2.fromScale(1, 0.5)
	symbol.Position = UDim2.fromScale(0, 0.25)
	symbol.Parent = cell

	local mass = Instance.new("TextLabel")
	mass.Name = "AtomicMass"
	mass.Text = e.mass
	mass.Font = Enum.Font.SourceSans
	mass.TextScaled = true
	mass.BackgroundTransparency = 1
	mass.TextColor3 = Color3.fromRGB(40, 25, 15)
	mass.Size = UDim2.fromScale(0.94, 0.17)
	mass.Position = UDim2.fromScale(0.03, 0.79)
	mass.Parent = cell
end

-- Placeholder cells at (6,3) and (7,3) pointing to the lanthanide/actinide
-- strips below. Standard museum convention: the main table shows "57-71" and
-- "89-103" cells to indicate where the f-block inserts.
local function addPlaceholder(name: string, row: number, col: number, text: string, bgcolor: Color3)
	local cellW = 1.0 / COLS
	local cellH = (GRID_BOTTOM - GRID_TOP) / ROWS
	local cx = (col - 0.5) * cellW
	local cy = GRID_TOP + (row - 0.5) * cellH

	local cell = Instance.new("Frame")
	cell.Name = name
	cell.AnchorPoint = Vector2.new(0.5, 0.5)
	cell.Position = UDim2.fromScale(cx, cy)
	cell.Size = UDim2.fromScale(cellW * (1 - CELL_MARGIN), cellH * (1 - CELL_MARGIN))
	cell.BackgroundColor3 = bgcolor
	cell.BorderSizePixel = 0
	cell.Parent = gui

	local border = Instance.new("UIStroke")
	border.Thickness = 1
	border.Color = Color3.fromRGB(60, 40, 20)
	border.Parent = cell

	local label = Instance.new("TextLabel")
	label.Name = "Placeholder"
	label.Text = text
	label.Font = Enum.Font.SourceSansBold
	label.TextScaled = true
	label.BackgroundTransparency = 1
	label.TextColor3 = Color3.fromRGB(30, 20, 10)
	label.Size = UDim2.fromScale(1, 1)
	label.Position = UDim2.fromScale(0, 0)
	label.Parent = cell
end

addPlaceholder("Placeholder_Lanthanides", 6, 3, "57-71",  CATEGORY_COLORS.lanthanide)
addPlaceholder("Placeholder_Actinides",   7, 3, "89-103", CATEGORY_COLORS.actinide)

-- Hide prototype parts, storing originals for one-line restoration.
-- SurfaceGuis parented to those hidden parts must be Enabled=false too --
-- the first run left the prototype Wall's PeriodicTableDisplay SurfaceGui
-- rendering through the invisible Part, producing a ghost row 8 and an
-- overlaid title that hid the "IUPAC" prefix. Storing the original Enabled
-- state on the SurfaceGui itself keeps restoration a one-liner.
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

-- Rename stone to accuracy-doc name
label.Text = "IUPAC PERIODIC TABLE OF THE ELEMENTS"
exhibit:SetAttribute("DisplayName", "IUPAC PERIODIC TABLE OF THE ELEMENTS")

if recording then
	ChangeHistoryService:FinishRecording(recording, Enum.FinishRecordingOperation.Commit)
end

-- Verification
local lo1, hi1 = computeAabb(exhibit)
local delta = {
	lo1.X - lo0.X, lo1.Y - lo0.Y, lo1.Z - lo0.Z,
	hi1.X - hi0.X, hi1.Y - hi0.Y, hi1.Z - hi0.Z,
}

local colliders = {}
for _, d in ipairs(exhibit:GetDescendants()) do
	if d:IsA("BasePart") and d.CanCollide then
		table.insert(colliders, d.Name)
	end
end

local elementCells = 0
for _, c in ipairs(gui:GetChildren()) do
	if c.Name:sub(1, 3) == "El_" then
		elementCells = elementCells + 1
	end
end

return string.format(
	"prototype hidden: %d\nelement cells: %d (expect 118)\nwall size=%.1fx%.1fx%.1f  pos=(%.1f,%.1f,%.1f)\nAABB delta: %.4f,%.4f,%.4f | %.4f,%.4f,%.4f\ncolliders: %d (%s)\nstone renamed: %q -> %q",
	#proto, elementCells,
	wall.Size.X, wall.Size.Y, wall.Size.Z, wall.Position.X, wall.Position.Y, wall.Position.Z,
	delta[1], delta[2], delta[3], delta[4], delta[5], delta[6],
	#colliders, table.concat(colliders, ","),
	oldText, label.Text
)
