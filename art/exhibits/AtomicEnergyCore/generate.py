"""Generates the Chicago Pile-1 (1942) exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/AtomicEnergyCore/generate.py \
        -- --out art/exhibits/AtomicEnergyCore/build/AtomicEnergyCore.glb

Historical reconstruction, per accuracy doc: "Argonne documentation of the
graphite-and-uranium pile, lattice, control system, and 57-layer
construction."

Structure follows the 2 December 1942 assembly under the west stands of
Stagg Field, University of Chicago. Rough envelope from published records:
approximately 25 ft x 25 ft x 20 ft (7.6 x 7.6 x 6.1 m), 57 layers of
machined graphite bricks, some containing uranium metal or uranium oxide
pseudospheres, in a wooden support frame. Control rods were cadmium sheets
mounted on wooden strips, withdrawn horizontally.

The pile was ellipsoidal ("oblate spheroid") -- flatter than a sphere, wider
than tall -- not a plain box, though museum diagrams often simplify to a
rectangular stack.

MATERIALS ARE AN ART CHOICE. Real graphite is dark grey and matte; brass
throughout under D-016. Dossier says so.
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
REAL_W_M = 7.6
REAL_D_M = 7.6
REAL_H_M = 6.1

# Display scale set by fitting width to shell (~5.4 studs/m)
STUDS_PER_M = 4.6  # frame + base plate must fit inside shell width 43.20
PILE_W = REAL_W_M * STUDS_PER_M   # ~41.8
PILE_D = REAL_D_M * STUDS_PER_M   # ~41.8; will limit by shell depth
PILE_D = min(PILE_D, SHELL_DEPTH - 6.0)  # room for frame + base plate + rod handle
PILE_H = REAL_H_M * STUDS_PER_M   # ~33.6

# Layers: 57 real; simplified to visible layer slabs
VISIBLE_LAYERS = 15  # each display layer represents ~4 real graphite layers
LAYER_H = PILE_H / VISIBLE_LAYERS

# Wood support frame
FRAME_POST_W = 0.9

SEGMENTS = 16


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


def build_pile(parts):
	"""Oblate-spheroid pile of stacked graphite layer slabs.

	Each layer's horizontal extent varies with height like an ellipse cross-
	section, capturing the "not a plain box" real shape. Bottom layers are
	widest, top and bottom are narrower.
	"""
	base_z = 0.5  # small base plate underneath
	for i in range(VISIBLE_LAYERS):
		z_frac = (i + 0.5) / VISIBLE_LAYERS  # 0 to 1 from bottom to top
		# Ellipse cross-section: scale by sin(pi * z_frac), so waist is max at middle
		waist_scale = 0.5 + 0.5 * math.sin(math.pi * z_frac)
		layer_w = PILE_W * (0.65 + 0.35 * waist_scale)
		layer_d = PILE_D * (0.65 + 0.35 * waist_scale)
		layer_z = base_z + i * LAYER_H + LAYER_H / 2
		# Split into 3x3 sub-blocks to hint at the block-construction texture
		sub_w = layer_w / 3
		sub_d = layer_d / 3
		for gx in range(3):
			for gy in range(3):
				bx = (gx - 1) * sub_w
				by = (gy - 1) * sub_d
				parts.append(box(f"GraphiteBlock_L{i:02d}", sub_w * 0.94, sub_d * 0.94, LAYER_H * 0.92,
					bx, by, layer_z))


def build_wooden_frame(parts):
	"""Wooden support frame around the pile: four corner posts + a couple of
	beams. Real pile had square timber cribs holding it upright.
	"""
	frame_h = PILE_H + 2.0
	half_w = PILE_W / 2 + 1.4
	half_d = PILE_D / 2 + 1.4
	for sx in (-1.0, 1.0):
		for sy in (-1.0, 1.0):
			parts.append(box("FramePost", FRAME_POST_W, FRAME_POST_W, frame_h,
				sx * half_w, sy * half_d, frame_h / 2))
	# Top rails
	for sy in (-1.0, 1.0):
		parts.append(box("FrameRailTop", half_w * 2, FRAME_POST_W, FRAME_POST_W,
			0.0, sy * half_d, frame_h - FRAME_POST_W / 2))
	# Base plate
	parts.append(box("BasePlate", PILE_W + 3.5, PILE_D + 3.5, 0.7,
		0.0, 0.0, 0.35))


def build_control_rod(parts):
	"""A single control rod (cadmium sheet on a wooden strip) inserted
	horizontally into the pile. Handle sticks out the front for visibility.
	"""
	rod_length = PILE_W + 6.0
	rod_z = 0.5 + PILE_H * 0.55  # midway up the pile
	# Wooden strip with cadmium plate — one long thin bar
	parts.append(box("ControlRod", rod_length, 0.4, 0.35, 0.0, PILE_D / 2 + 1.0, rod_z))
	# Handle on the front end (protrudes toward +Y)
	handle_offset = PILE_W / 2 + 4.5
	parts.append(box("ControlRodHandle", 1.2, 1.2, 0.6, handle_offset, PILE_D / 2 + 1.0, rod_z))
	parts.append(cyl("HandleGrip", 0.35, 1.6, handle_offset, PILE_D / 2 + 1.0, rod_z + 1.0))


def build():
	clear_scene()
	parts = []
	build_wooden_frame(parts)
	build_pile(parts)
	build_control_rod(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "ChicagoPile1"
	merged.data.name = "ChicagoPile1"
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
	print(f"GEN_SCALE {STUDS_PER_M:.1f} studs/m; real 7.6x7.6x6.1 m -> {REAL_W_M*STUDS_PER_M:.1f}x{REAL_D_M*STUDS_PER_M:.1f}x{REAL_H_M*STUDS_PER_M:.1f} studs")
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
