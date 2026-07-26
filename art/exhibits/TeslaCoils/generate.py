"""Generates the Tesla Coil Apparatus exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/TeslaCoils/generate.py \
        -- --out art/exhibits/TeslaCoils/build/TeslaCoils.glb

Scientific reconstruction, per the accuracy doc: "A documented spark-gap
Tesla-coil circuit with credible primary, secondary, terminal, capacitor,
and grounding geometry."

Structure (standard bipolar spark-gap Tesla coil):
- Wooden base (rectangular platform)
- Primary coil: a flat pancake spiral of thick copper tube around the base
- Secondary coil: a tall thin cylinder wound with fine wire, mounted at the
  centre of the primary
- Top load / terminal: a large toroidal capacitor at the top of the secondary
- Spark gap unit and capacitor bank on the base beside the coils
- Ground wire trailing off one side

MATERIALS ARE AN ART CHOICE. Brass throughout under D-016 (real coils are
copper, wood, and ceramic — the arena palette is close enough).
"""

import math
import os
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0

# --- geometry ---------------------------------------------------------------

BASE_W = 26.0
BASE_D = 16.0
BASE_H = 1.6

PRIMARY_INNER_R = 4.5
PRIMARY_OUTER_R = 9.0
PRIMARY_TURNS = 6
PRIMARY_TUBE_R = 0.35
PRIMARY_HEIGHT = BASE_H + 1.5

SECONDARY_R = 3.2
SECONDARY_H = 32.0
SECONDARY_BASE_Z = PRIMARY_HEIGHT
SECONDARY_TOP_Z = SECONDARY_BASE_Z + SECONDARY_H

TERMINAL_MAJOR_R = 6.0    # toroid major radius
TERMINAL_MINOR_R = 1.6    # toroid tube radius

SPARK_GAP_W = 3.5
SPARK_GAP_H = 2.5
SPARK_GAP_D = 2.0

CAP_BANK_W = 5.0
CAP_BANK_H = 4.0
CAP_BANK_D = 3.0

SEGMENTS = 20


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


def torus(name, major, minor, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0), major_seg=48, minor_seg=10):
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=major_seg, minor_segments=minor_seg, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def build_base(parts):
	parts.append(box("Base", BASE_W, BASE_D, BASE_H, 0.0, 0.0, BASE_H / 2))


def build_primary_coil(parts):
	"""Flat pancake spiral: series of concentric toruses at slightly different
	radii, simplifying the actual spiral into visible rings.
	"""
	for i in range(PRIMARY_TURNS):
		r = PRIMARY_INNER_R + (PRIMARY_OUTER_R - PRIMARY_INNER_R) * i / (PRIMARY_TURNS - 1)
		parts.append(torus(f"PrimaryTurn{i:02d}", r, PRIMARY_TUBE_R, 0.0, 0.0, PRIMARY_HEIGHT))


def build_secondary_coil(parts):
	"""Tall thin cylinder representing the wound secondary. Coil windings hinted
	at with a stack of thin ridges (toruses).
	"""
	# Cylinder core
	parts.append(cyl("SecondaryCore", SECONDARY_R, SECONDARY_H,
		0.0, 0.0, SECONDARY_BASE_Z + SECONDARY_H / 2))
	# Winding ridges every few studs
	ridge_count = 14
	for i in range(ridge_count):
		z = SECONDARY_BASE_Z + (i + 0.5) * SECONDARY_H / ridge_count
		parts.append(torus(f"SecondaryRidge{i:02d}", SECONDARY_R + 0.1, 0.15, 0.0, 0.0, z, major_seg=24, minor_seg=4))


def build_terminal(parts):
	"""Toroidal top load."""
	parts.append(torus("TopTerminal", TERMINAL_MAJOR_R, TERMINAL_MINOR_R,
		0.0, 0.0, SECONDARY_TOP_Z + TERMINAL_MINOR_R, major_seg=48, minor_seg=14))
	# Central spike (breakout point)
	parts.append(cyl("BreakoutSpike", 0.15, 1.8, 0.0, 0.0, SECONDARY_TOP_Z + TERMINAL_MINOR_R * 2 + 0.9))


def build_spark_gap(parts):
	"""Spark gap unit on the base -- two electrodes on a small stand."""
	sx = BASE_W / 2 - CAP_BANK_W - 2.5
	sy = -BASE_D / 2 + SPARK_GAP_D / 2 + 0.5
	sz = BASE_H + SPARK_GAP_H / 2
	parts.append(box("SparkGapHousing", SPARK_GAP_W, SPARK_GAP_D, SPARK_GAP_H, sx, sy, sz))
	# Two electrode balls on top
	for dx in (-1.0, 1.0):
		parts.append(cyl("SparkElectrode", 0.35, 0.5, sx + dx * SPARK_GAP_W * 0.28,
			sy, sz + SPARK_GAP_H / 2 + 0.25, rot=(math.radians(90.0), 0.0, 0.0)))


def build_capacitor_bank(parts):
	"""Small capacitor bank on the base beside the coils."""
	cx = BASE_W / 2 - CAP_BANK_W / 2 - 0.5
	cy = -BASE_D / 2 + CAP_BANK_D / 2 + 0.5
	cz = BASE_H + CAP_BANK_H / 2
	parts.append(box("CapacitorBank", CAP_BANK_W, CAP_BANK_D, CAP_BANK_H, cx, cy, cz))
	# Two terminal posts on top
	for dx in (-0.35, 0.35):
		parts.append(cyl("CapTerminal", 0.25, 0.6, cx + dx * CAP_BANK_W, cy, cz + CAP_BANK_H / 2 + 0.3))


def build_ground_wire(parts):
	"""Wire trailing off one edge of the base to ground."""
	parts.append(cyl("GroundWire", 0.18, 6.0,
		-BASE_W / 2 - 3.0, 0.0, BASE_H, rot=(0.0, math.radians(90.0), 0.0)))


def build():
	clear_scene()
	parts = []
	build_base(parts)
	build_primary_coil(parts)
	build_secondary_coil(parts)
	build_terminal(parts)
	build_spark_gap(parts)
	build_capacitor_bank(parts)
	build_ground_wire(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "TeslaCoil"
	merged.data.name = "TeslaCoil"
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
