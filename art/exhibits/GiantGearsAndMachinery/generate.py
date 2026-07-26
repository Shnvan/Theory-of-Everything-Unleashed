"""Generates the Babbage Difference Engine No. 2 exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/GiantGearsAndMachinery/generate.py \
        -- --out art/exhibits/GiantGearsAndMachinery/build/GiantGearsAndMachinery.glb

Structure follows Charles Babbage's 1847-1849 Difference Engine No. 2 as
first physically constructed by the Science Museum in 1991 (Science Museum
Group object 1992-556).

Real dimensions: **3.35 m tall x 4.65 m wide x 1.83 m deep**, ~8,000 parts,
weight ~5 tonnes. Central calculating mechanism has **seven vertical
columns, each with 31 gear wheels**, driven by a hand crank. A printing
mechanism sits on the left side for hardcopy output.

MATERIALS ARE AN ART CHOICE. Real DE#2 is bronze on cast iron; brass
throughout under D-016 is close.
"""

import math
import os
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0

# Real approximate dimensions
REAL_W_M = 4.65
REAL_H_M = 3.35
REAL_D_M = 1.83
STUDS_PER_M = 8.0
ENGINE_W = REAL_W_M * STUDS_PER_M
ENGINE_H = REAL_H_M * STUDS_PER_M
ENGINE_D = REAL_D_M * STUDS_PER_M

# Calculating columns
N_COLUMNS = 7
WHEELS_PER_COLUMN_DISPLAY = 8  # simplified from real 31; tooth rings dropped to stay under triangle cap

FRAME_POST_W = 0.7
BASE_H = 1.8

SEGMENTS = 20


def clear_scene():
	bpy.ops.object.select_all(action="SELECT")
	bpy.ops.object.delete(use_global=False)
	for block in (bpy.data.meshes, bpy.data.materials, bpy.data.objects):
		for item in list(block):
			if item.users == 0:
				block.remove(item)


def box(name, sx, sy, sz, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	o.scale = (sx, sy, sz)
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return o


def cyl(name, r, d, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0), verts=SEGMENTS):
	bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=verts, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def torus(name, major, minor, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=24, minor_segments=6, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def build_base_and_frame(parts):
	# Base plate
	parts.append(box("Base", ENGINE_W + 2, ENGINE_D + 2, BASE_H, 0.0, 0.0, BASE_H / 2))
	# Four corner posts
	frame_h = ENGINE_H
	for sx in (-1.0, 1.0):
		for sy in (-1.0, 1.0):
			parts.append(box("FramePost", FRAME_POST_W, FRAME_POST_W, frame_h,
				sx * (ENGINE_W / 2 - 0.4), sy * (ENGINE_D / 2 - 0.4), BASE_H + frame_h / 2))
	# Top rail
	for sy in (-1.0, 1.0):
		parts.append(box("FrameTopRail", ENGINE_W - 0.8, FRAME_POST_W, FRAME_POST_W,
			0.0, sy * (ENGINE_D / 2 - 0.4), BASE_H + frame_h - FRAME_POST_W / 2))
	# Bottom cross rail
	for sy in (-1.0, 1.0):
		parts.append(box("FrameBotRail", ENGINE_W - 0.8, FRAME_POST_W, FRAME_POST_W,
			0.0, sy * (ENGINE_D / 2 - 0.4), BASE_H + FRAME_POST_W / 2))


def build_calculating_columns(parts):
	"""Seven vertical columns, each a stack of gear-wheel discs on a central
	shaft. Printing mechanism reserves the leftmost column-slot, so calculating
	columns are laid out to the right of centre.
	"""
	col_start_x = -ENGINE_W / 2 + 6.5   # leave 6.5 studs for printer on left
	col_span = ENGINE_W - 7.5 - 2.0     # remaining width for 7 columns
	col_spacing = col_span / (N_COLUMNS - 1)
	shaft_r = 0.35
	wheel_r = 1.6
	wheel_h = 0.35

	col_bottom_z = BASE_H + 1.0
	col_top_z = BASE_H + ENGINE_H - 1.0
	col_h = col_top_z - col_bottom_z

	for c in range(N_COLUMNS):
		x = col_start_x + c * col_spacing
		# Central shaft
		parts.append(cyl(f"ColShaft{c:02d}", shaft_r, col_h, x, 0.0, (col_bottom_z + col_top_z) / 2))
		# Stack of wheels — plain cylinders, no tooth rings (kept the budget under
		# the 20000 triangle cap). At gameplay distance the stacked-disc shape
		# reads as a gear column without individual teeth.
		for w in range(WHEELS_PER_COLUMN_DISPLAY):
			z = col_bottom_z + (w + 0.5) * col_h / WHEELS_PER_COLUMN_DISPLAY
			parts.append(cyl(f"Wheel_C{c:02d}_W{w:02d}", wheel_r, wheel_h, x, 0.0, z))


def build_printer(parts):
	"""Printing mechanism on the left side: rectangular housing with a paper roll on top."""
	printer_x = -ENGINE_W / 2 + 3.5
	printer_w = 5.5
	printer_d = ENGINE_D - 3.0
	printer_h = ENGINE_H * 0.62
	printer_bottom_z = BASE_H + 0.5
	parts.append(box("PrinterHousing", printer_w, printer_d, printer_h,
		printer_x, 0.0, printer_bottom_z + printer_h / 2))
	# Paper roll on top
	parts.append(cyl("PaperRoll", 1.8, printer_w * 0.7,
		printer_x, 0.0, printer_bottom_z + printer_h + 1.9,
		rot=(0.0, math.radians(90.0), 0.0)))


def build_crank_and_platform(parts):
	"""Hand crank on the right end of the engine at operator height."""
	crank_x = ENGINE_W / 2 + 1.0
	crank_z = BASE_H + ENGINE_H * 0.55
	# Crank axle (extends into the engine)
	parts.append(cyl("CrankAxle", 0.4, 2.2, crank_x - 0.6, 0.0, crank_z,
		rot=(0.0, math.radians(90.0), 0.0)))
	# Crank arm
	parts.append(box("CrankArm", 0.4, 0.4, 3.5, crank_x, 0.0, crank_z - 1.75, rot=(math.radians(20.0), 0.0, 0.0)))
	# Handle
	parts.append(cyl("CrankHandle", 0.35, 1.5, crank_x, 1.0, crank_z - 3.3, rot=(math.radians(90.0), 0.0, 0.0)))


def build():
	clear_scene()
	parts = []
	build_base_and_frame(parts)
	build_calculating_columns(parts)
	build_printer(parts)
	build_crank_and_platform(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "BabbageDifferenceEngine"
	merged.data.name = "BabbageDifferenceEngine"
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
	print(f"GEN_SCALE {STUDS_PER_M} studs/m; real {REAL_W_M}x{REAL_H_M}x{REAL_D_M} m")
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
