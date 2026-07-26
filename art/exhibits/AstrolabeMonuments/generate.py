"""Generates the Arsenius Planispheric Astrolabe (1607-1618) exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/AstrolabeMonuments/generate.py \
        -- --out art/exhibits/AstrolabeMonuments/build/AstrolabeMonuments.glb

Structure follows the Arsenius (Louvain) workshop planispheric astrolabes of
the early 17th century, per the accuracy doc's anchor Science Museum Group
object 1878-11. The exhibit shows **front and reverse** side by side on a
shared stand, as the accuracy doc requires.

A planispheric astrolabe has:
  - Mater: main plate carrying the throne and suspension ring
  - Climate/tympan plate: engraved with almucantars for a given latitude
  - Rete: openwork star pointer + zodiac ring, rotates over the tympan
  - Alidade: sighting rule on the back with a graduated scale
  - Throne: decorative crown at the top holding the suspension ring

MATERIALS ARE AN ART CHOICE. Real Arsenius astrolabes are engraved brass,
which happens to match D-016's palette exactly.
"""

import math
import os
import sys

import bpy

# --- envelope ----------------------------------------------------------------

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0

# --- what the sources establish ---------------------------------------------
# Arsenius large astrolabes are typically ~30-40 cm mater diameter. Scale
# below is a display choice: two disks side by side, each 14 studs diameter,
# mounted on a shared stand at eye level.

ASTROLABE_D = 14.0
ASTROLABE_THICK = 0.8
DISK_GAP = 4.0
STAND_H = 22.0  # bench height under the disks

SEGMENTS = 24


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


def torus(name, major, minor, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=48, minor_segments=6, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def build_stand(parts):
	# Base plate
	parts.append(box("BasePlate", ASTROLABE_D * 2 + DISK_GAP + 4, 8.0, 1.0, 0.0, 0.0, 0.5))
	# Two support columns, one under each disk
	half_span = ASTROLABE_D / 2 + DISK_GAP / 2
	for sx in (-1.0, 1.0):
		parts.append(cyl("StandColumn", 0.8, STAND_H, sx * half_span, 0.0, STAND_H / 2))
		# Small base at the foot
		parts.append(cyl("StandColumnBase", 1.5, 0.6, sx * half_span, 0.0, 1.3))


def build_disk_front(parts):
	"""Front of astrolabe: mater with rete overlaid."""
	half_span = ASTROLABE_D / 2 + DISK_GAP / 2
	cx = -half_span
	disk_z = STAND_H + ASTROLABE_D / 2
	# Mater (main plate) — a shallow cylinder oriented like a disk facing +Y
	parts.append(cyl("Mater_Front", ASTROLABE_D / 2, ASTROLABE_THICK, cx, 0.0, disk_z,
		rot=(math.radians(90.0), 0.0, 0.0)))
	# Rim (raised)
	parts.append(torus("Rim_Front", ASTROLABE_D / 2, 0.3, cx, 0.15, disk_z))
	# Rete: openwork star pointer -- represented as a small tilted cross + zodiac ring
	rete_r = ASTROLABE_D / 2 * 0.75
	parts.append(torus("ZodiacRing", rete_r, 0.2, cx, -ASTROLABE_THICK * 0.6, disk_z))
	# Rete arms -- two crossed bars
	for angle_deg in (0.0, 60.0, 120.0):
		a = math.radians(angle_deg)
		parts.append(box("ReteArm", rete_r * 1.9, 0.3, 0.15,
			cx, -ASTROLABE_THICK * 0.5, disk_z,
			rot=(0.0, a, 0.0)))
	# Central pin
	parts.append(cyl("CentralPin", 0.35, 0.5, cx, -ASTROLABE_THICK * 0.9, disk_z,
		rot=(math.radians(90.0), 0.0, 0.0)))
	# Throne (top ornament)
	parts.append(box("Throne_Front", 2.0, ASTROLABE_THICK, 1.6, cx, 0.0, disk_z + ASTROLABE_D / 2 + 0.8))
	# Suspension ring above throne
	parts.append(torus("Ring_Front", 0.8, 0.2, cx, 0.0, disk_z + ASTROLABE_D / 2 + 2.4))


def build_disk_back(parts):
	"""Back of astrolabe: alidade + graduated scale."""
	half_span = ASTROLABE_D / 2 + DISK_GAP / 2
	cx = half_span
	disk_z = STAND_H + ASTROLABE_D / 2
	parts.append(cyl("Mater_Back", ASTROLABE_D / 2, ASTROLABE_THICK, cx, 0.0, disk_z,
		rot=(math.radians(90.0), 0.0, 0.0)))
	parts.append(torus("Rim_Back", ASTROLABE_D / 2, 0.3, cx, -0.15, disk_z))
	# Alidade -- a straight sighting rule across the diameter
	parts.append(box("Alidade", ASTROLABE_D * 0.94, 0.35, 0.2,
		cx, -ASTROLABE_THICK * 0.6, disk_z,
		rot=(0.0, math.radians(35.0), 0.0)))
	# Two sight vanes at ends of alidade (small upright rectangles)
	for offset_frac in (-0.42, 0.42):
		a = math.radians(35.0)
		lx = cx + math.cos(a) * offset_frac * ASTROLABE_D
		lz = disk_z + math.sin(a) * offset_frac * ASTROLABE_D
		parts.append(box("SightVane", 0.25, 0.2, 0.7, lx, -ASTROLABE_THICK * 0.6, lz))
	parts.append(cyl("CentralPin_Back", 0.35, 0.5, cx, -ASTROLABE_THICK * 0.9, disk_z,
		rot=(math.radians(90.0), 0.0, 0.0)))
	parts.append(box("Throne_Back", 2.0, ASTROLABE_THICK, 1.6, cx, 0.0, disk_z + ASTROLABE_D / 2 + 0.8))
	parts.append(torus("Ring_Back", 0.8, 0.2, cx, 0.0, disk_z + ASTROLABE_D / 2 + 2.4))


def build():
	clear_scene()
	parts = []
	build_stand(parts)
	build_disk_front(parts)
	build_disk_back(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "ArseniusAstrolabe"
	merged.data.name = "ArseniusAstrolabe"
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
		raise SystemExit(f"FAIL: height {d.z:.2f} exceeds envelope {ENVELOPE_HEIGHT:.2f}")
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
