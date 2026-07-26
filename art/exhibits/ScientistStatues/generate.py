"""Generates the Scientist Statues exhibit mesh: Einstein · Tesla · Newton.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/ScientistStatues/generate.py \
        -- --out art/exhibits/ScientistStatues/build/ScientistStatues.glb

Historical portrayals. User's chosen trio for the Hall of Minds, substituted
for the accuracy doc's original Galileo · Lovelace · Curie:
  - Curie -> Tesla (Q-021: Curie collides with Radiant Pioneer)
  - Galileo, Lovelace -> Einstein, Newton (user pick: maximum public recognition)

Two acknowledged trade-offs disclosed in the dossier:
  - Trio is all-male (Curie was the only globally-famous female alternative,
    and she's Q-021 blocked)
  - Both Einstein and Newton have weak associations with Gravity Sovereign
    (relativity, universal gravitation); neither is famous SOLELY for gravity
    the way Curie was for radiation, so the identifiability risk is much
    lower than the Curie/Radiant Pioneer collision

Sculptures are stylised silhouettes, not portrait-quality. The accuracy doc
explicitly says "original sculptures informed by separately cleared public-
domain or openly licensed portraits; no museum endorsement" -- stylisation
is the correct fidelity level.

MATERIALS ARE AN ART CHOICE. Real bronze busts would use bronze; brass
throughout under D-016.
"""

import math
import os
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0
SEGMENTS = 16

# --- shared plinth + individual pedestals -----------------------------------

SHARED_PLINTH_W = 30.0
SHARED_PLINTH_D = 8.0
SHARED_PLINTH_H = 3.5

MINI_PLINTH_W = 5.0
MINI_PLINTH_D = 5.0
MINI_PLINTH_H = 2.5

STATUE_H = 8.5   # standing figure height above mini-plinth top
STATUE_R = 0.9   # torso radius

# Slot positions along X for the three statues (equally spaced)
SLOT_X = [-9.0, 0.0, 9.0]  # Newton (left), Tesla (centre), Einstein (right)


def clear_scene():
	bpy.ops.object.select_all(action="SELECT")
	bpy.ops.object.delete(use_global=False)
	for block in (bpy.data.meshes, bpy.data.materials, bpy.data.objects):
		for item in list(block):
			if item.users == 0:
				block.remove(item)


def cyl(name, r, d, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0), verts=SEGMENTS):
	bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=verts, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def cone(name, r1, r2, d, x=0.0, y=0.0, z=0.0, verts=SEGMENTS):
	bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=d, vertices=verts, location=(x, y, z))
	o = bpy.context.active_object
	o.name = name
	return o


def box(name, sx, sy, sz, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	o.scale = (sx, sy, sz)
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return o


def sphere(name, r, x=0.0, y=0.0, z=0.0, segments=14, rings=10):
	bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=segments, ring_count=rings, location=(x, y, z))
	o = bpy.context.active_object
	o.name = name
	return o


def build_shared_plinth(parts):
	parts.append(box("SharedPlinth", SHARED_PLINTH_W, SHARED_PLINTH_D, SHARED_PLINTH_H,
		0.0, 0.0, SHARED_PLINTH_H / 2))
	# Decorative top rim
	parts.append(box("SharedPlinthRim", SHARED_PLINTH_W + 0.6, SHARED_PLINTH_D + 0.6, 0.4,
		0.0, 0.0, SHARED_PLINTH_H))


def build_mini_plinth(parts, cx, name):
	top_z = SHARED_PLINTH_H + 0.4
	parts.append(box(name, MINI_PLINTH_W, MINI_PLINTH_D, MINI_PLINTH_H, cx, 0.0, top_z + MINI_PLINTH_H / 2))
	return top_z + MINI_PLINTH_H  # returns statue base Z


def build_newton(parts, cx):
	"""Isaac Newton (1643-1727): scholar's robe (Kneller 1689 portrait). Long
	wig, formal collar, holding a prism at his side."""
	base_z = build_mini_plinth(parts, cx, "Newton_Plinth")
	# Robe -- cone flaring outward at bottom for a floor-length effect
	robe_h = STATUE_H * 0.62
	parts.append(cone("Newton_Robe", STATUE_R * 1.4, STATUE_R * 0.95, robe_h,
		cx, 0.0, base_z + robe_h / 2))
	# Torso -- upper body cylinder
	torso_h = STATUE_H * 0.22
	parts.append(cyl("Newton_Torso", STATUE_R * 0.95, torso_h,
		cx, 0.0, base_z + robe_h + torso_h / 2))
	# Head -- with the long Baroque wig (larger than head sphere)
	head_r = STATUE_R * 0.75
	parts.append(sphere("Newton_Head", head_r,
		cx, 0.0, base_z + robe_h + torso_h + head_r * 0.9))
	# Long wig -- flared cone hanging below the head
	wig_h = STATUE_H * 0.14
	parts.append(cone("Newton_Wig", head_r * 1.15, head_r * 0.7, wig_h,
		cx, 0.0, base_z + robe_h + torso_h - wig_h / 2 + head_r * 0.3))
	# Prism at his side -- small triangular cross-section (rendered as thin box)
	parts.append(box("Newton_Prism", 0.55, 0.55, 1.2,
		cx + STATUE_R * 1.7, 0.0, base_z + robe_h * 0.5,
		rot=(math.radians(15.0), 0.0, math.radians(15.0))))


def build_tesla(parts, cx):
	"""Nikola Tesla (1856-1943): three-piece suit (Sarony 1893 portrait). Slim
	standing figure, hand on a small Tesla coil at his side."""
	base_z = build_mini_plinth(parts, cx, "Tesla_Plinth")
	# Trousers -- narrower cylinder for legs
	leg_h = STATUE_H * 0.42
	parts.append(cyl("Tesla_Legs", STATUE_R * 0.85, leg_h,
		cx, 0.0, base_z + leg_h / 2))
	# Suit jacket -- slightly wider torso
	torso_h = STATUE_H * 0.36
	parts.append(cyl("Tesla_Suit", STATUE_R * 1.05, torso_h,
		cx, 0.0, base_z + leg_h + torso_h / 2))
	# Head
	head_r = STATUE_R * 0.7
	parts.append(sphere("Tesla_Head", head_r,
		cx, 0.0, base_z + leg_h + torso_h + head_r * 0.9))
	# Formal hair -- neat, small dome on top of head
	parts.append(sphere("Tesla_Hair", head_r * 0.85,
		cx, 0.0, base_z + leg_h + torso_h + head_r * 1.35))
	# Small Tesla coil at side -- vertical cylinder with torus top
	coil_h = STATUE_H * 0.25
	coil_x = cx + STATUE_R * 1.6
	parts.append(cyl("Tesla_MiniCoil", 0.4, coil_h,
		coil_x, 0.0, base_z + coil_h / 2))
	bpy.ops.mesh.primitive_torus_add(major_radius=0.7, minor_radius=0.2,
		major_segments=16, minor_segments=6, location=(coil_x, 0.0, base_z + coil_h + 0.15))
	t = bpy.context.active_object
	t.name = "Tesla_MiniCoilTop"
	parts.append(t)


def build_einstein(parts, cx):
	"""Albert Einstein (1879-1955): casual clothes with iconic wild hair,
	holding a notebook or chalkboard."""
	base_z = build_mini_plinth(parts, cx, "Einstein_Plinth")
	# Trousers
	leg_h = STATUE_H * 0.40
	parts.append(cyl("Einstein_Legs", STATUE_R * 0.9, leg_h,
		cx, 0.0, base_z + leg_h / 2))
	# Casual shirt / sweater -- slightly baggy torso
	torso_h = STATUE_H * 0.38
	parts.append(cyl("Einstein_Torso", STATUE_R * 1.1, torso_h,
		cx, 0.0, base_z + leg_h + torso_h / 2))
	# Head
	head_r = STATUE_R * 0.75
	parts.append(sphere("Einstein_Head", head_r,
		cx, 0.0, base_z + leg_h + torso_h + head_r * 0.9))
	# WILD HAIR -- larger sphere on top, plus a few spikes
	parts.append(sphere("Einstein_Hair", head_r * 1.25,
		cx, 0.0, base_z + leg_h + torso_h + head_r * 1.35))
	# Chalkboard at his side -- flat panel
	board_x = cx + STATUE_R * 1.7
	parts.append(box("Einstein_Chalkboard", 0.3, 1.6, 1.4,
		board_x, 0.0, base_z + leg_h * 1.1))


def build():
	clear_scene()
	parts = []
	build_shared_plinth(parts)
	build_newton(parts, SLOT_X[0])
	build_tesla(parts, SLOT_X[1])
	build_einstein(parts, SLOT_X[2])

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "ScientistStatues"
	merged.data.name = "ScientistStatues"
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
	bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
	merged.location = (0.0, 0.0, 0.0)


def report(obj):
	mesh = obj.data
	tris = sum(max(len(p.vertices) - 2, 0) for p in mesh.polygons)
	d = obj.dimensions
	print(f"GEN_OBJECT {obj.name}")
	print(f"GEN_TRIANGLES {tris}")
	print(f"GEN_SIZE_STUDS {d.x:.2f} x {d.y:.2f} x {d.z:.2f}")
	if tris > 20000:
		raise SystemExit(f"FAIL: {tris} tri exceeds 20000")
	if d.z > ENVELOPE_HEIGHT:
		raise SystemExit(f"FAIL: height {d.z:.2f} exceeds envelope")
	if d.x > SHELL_WIDTH:
		raise SystemExit(f"FAIL: width {d.x:.2f} overhangs shell {SHELL_WIDTH:.2f}")
	if d.y > SHELL_DEPTH:
		raise SystemExit(f"FAIL: depth {d.y:.2f} overhangs shell {SHELL_DEPTH:.2f}")
	print(f"GEN_SHELL_MARGIN {SHELL_WIDTH - d.x:.2f} x {SHELL_DEPTH - d.y:.2f}")
	print("GEN_BUDGET_OK yes")
	print("GEN_ENVELOPE_OK yes")


def main():
	argv = sys.argv
	out_path = None
	if "--" in argv:
		rest = argv[argv.index("--") + 1 :]
		if "--out" in rest:
			out_path = rest[rest.index("--out") + 1]
	if out_path is None:
		raise SystemExit("usage: ... --python generate.py -- --out <path.glb>")
	build()
	obj = bpy.context.active_object
	report(obj)
	os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
	bpy.ops.export_scene.gltf(filepath=out_path, export_format="GLB", use_selection=False, export_apply=True)
	print(f"GEN_WROTE {out_path}")


if __name__ == "__main__":
	main()
