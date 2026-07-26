"""Generates the Landmark Inventions Collection exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/InventionMuseumCases/generate.py \
        -- --out art/exhibits/InventionMuseumCases/build/InventionMuseumCases.glb

Miniature replica collection, per the accuracy doc: "A Gutenberg-type press,
Pascaline, Faraday disk, and 1903 Wright Flyer, each with its own source and
scale record."

Four small display objects on a shared plinth arranged in a row:

  1. Gutenberg-type press (c. 1440s) -- wooden screw press with a bed
  2. Pascaline (1642) -- Pascal's mechanical calculator, small box with dials
  3. Faraday disk (1831) -- homopolar generator, disk between magnets
  4. Wright Flyer (1903) -- biplane on skid frame

Each is at a different real scale in life; in the exhibit they are shown
at COMPRESSED SIZES so all four fit in a single display. Factual card
must state real sizes and disclose the display compression.

MATERIALS ARE AN ART CHOICE. Brass throughout under D-016.
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


def box(name, sx, sy, sz, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	o.scale = (sx, sy, sz)
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return o


def build_shared_plinth(parts):
	parts.append(box("SharedPlinth", 40.0, 12.0, 2.5, 0.0, 0.0, 1.25))


def build_gutenberg_press(parts, cx, cy):
	"""Wooden screw press with two vertical columns, top and bottom platens,
	and a bed underneath. Central screw threads down from the top."""
	base_z = 2.5
	press_h = 12.0
	# Vertical columns
	for sx in (-1.0, 1.0):
		parts.append(box("PressColumn", 0.8, 0.8, press_h, cx + sx * 2.2, cy, base_z + press_h / 2))
	# Top and bottom platens
	parts.append(box("PressTopPlaten", 5.6, 3.0, 0.8, cx, cy, base_z + press_h - 0.4))
	parts.append(box("PressBed", 5.6, 3.5, 1.0, cx, cy, base_z + 0.5))
	# Central screw
	parts.append(cyl("PressScrew", 0.5, press_h - 3.0, cx, cy, base_z + 1.5 + (press_h - 3.0) / 2))
	# Handle across the top
	parts.append(cyl("PressHandle", 0.3, 4.0, cx, cy, base_z + press_h + 0.5,
		rot=(0.0, math.radians(90.0), 0.0)))


def build_pascaline(parts, cx, cy):
	"""Small rectangular box with a row of number dials on the top face."""
	base_z = 2.5
	box_w = 5.0
	box_d = 3.0
	box_h = 1.4
	parts.append(box("PascalineBox", box_w, box_d, box_h, cx, cy, base_z + box_h / 2))
	# 6 dials on top
	for i in range(6):
		dx = -box_w / 2 + (i + 0.5) * box_w / 6
		parts.append(cyl("PascalineDial", 0.35, 0.35, cx + dx, cy, base_z + box_h + 0.15))
	# Small display window strip on the top edge
	parts.append(box("PascalineWindow", box_w * 0.85, 0.5, 0.15, cx, cy - box_d * 0.3, base_z + box_h + 0.08))


def build_faraday_disk(parts, cx, cy):
	"""Vertical disk mounted between two horseshoe-style magnet arms, on a base."""
	base_z = 2.5
	# Central disk (vertical, facing +X for visibility)
	disk_r = 2.5
	parts.append(cyl("FaradayDisk", disk_r, 0.3, cx, cy, base_z + disk_r + 1.0,
		rot=(0.0, math.radians(90.0), 0.0)))
	# Axle through disk
	parts.append(cyl("FaradayAxle", 0.2, 4.0, cx, cy, base_z + disk_r + 1.0,
		rot=(0.0, math.radians(90.0), 0.0)))
	# Two magnet poles either side of disk
	for sx in (-1.0, 1.0):
		parts.append(box("FaradayMagnet", 0.5, 1.4, 3.0,
			cx + sx * 1.8, cy, base_z + disk_r + 1.0))
	# Base support
	parts.append(box("FaradayBase", 5.0, 3.0, 1.0, cx, cy, base_z + 0.5))
	# Vertical support post to axle height
	parts.append(cyl("FaradayPost", 0.3, disk_r, cx, cy, base_z + 1.0 + disk_r / 2))


def build_wright_flyer(parts, cx, cy):
	"""Biplane silhouette: two horizontal wing rectangles, four struts, a
	tail assembly, and a fuselage/skid frame."""
	base_z = 2.5
	wingspan = 8.0
	wing_chord = 1.4
	wing_gap = 2.2
	fuselage_len = 5.5
	# Skid frame under the wings (thin rectangle)
	parts.append(box("WrightSkid", fuselage_len, 2.0, 0.2, cx, cy, base_z + 0.4))
	# Lower wing
	parts.append(box("WrightLowerWing", wingspan, wing_chord, 0.2, cx, cy, base_z + 0.9))
	# Upper wing
	parts.append(box("WrightUpperWing", wingspan, wing_chord, 0.2, cx, cy, base_z + 0.9 + wing_gap))
	# Interplane struts (four)
	for sx in (-1.0, 1.0):
		for sy in (-1.0, 1.0):
			parts.append(cyl("WrightStrut", 0.1, wing_gap,
				cx + sx * wingspan * 0.35, cy + sy * wing_chord * 0.3,
				base_z + 0.9 + wing_gap / 2))
	# Tail assembly at rear (small horizontal + vertical panel)
	tail_x = cx - fuselage_len / 2 - 1.0
	parts.append(box("WrightTailHoriz", 2.0, 1.0, 0.1, tail_x, cy, base_z + 1.4))
	parts.append(box("WrightTailVert", 2.0, 0.1, 0.8, tail_x, cy, base_z + 1.7))
	# Forward canard at front
	fwd_x = cx + fuselage_len / 2 + 1.0
	parts.append(box("WrightCanard", 2.6, 0.8, 0.1, fwd_x, cy, base_z + 1.3))


def build():
	clear_scene()
	parts = []
	build_shared_plinth(parts)
	# Four objects at x positions -15, -5, +5, +15
	build_gutenberg_press(parts, cx=-15.0, cy=0.0)
	build_pascaline(parts, cx=-5.0, cy=0.0)
	build_faraday_disk(parts, cx=5.0, cy=0.0)
	build_wright_flyer(parts, cx=15.0, cy=0.0)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "LandmarkInventions"
	merged.data.name = "LandmarkInventions"
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
