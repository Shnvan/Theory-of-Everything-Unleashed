"""Generates the Galilean Refractor + Hooker Telescope exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/TelescopeTowers/generate.py \
        -- --out art/exhibits/TelescopeTowers/build/TelescopeTowers.glb

Mixed replica display, per the accuracy doc:
- **Galileo-type refractor** (~1610): small wooden tube on a light tripod
- **Hooker Telescope** (Mount Wilson, 1917): 100-inch reflector on an
  English-yoke / horseshoe equatorial mount

The two are DELIBERATELY at different visual scales -- side by side reads
as "300 years of telescope development", with the tiny Galilean beside the
massive Hooker being the point. Neither is at 1:1 to the other; a factual
card discloses the real dimensions.

MATERIALS ARE AN ART CHOICE. Real Galilean tubes were wood + leather;
Hooker is painted steel. Brass throughout under D-016.
"""

import math
import os
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 36.00  # this exhibit's shell is deeper
ENVELOPE_HEIGHT = 63.00

STUDS_TO_BLENDER = 1.0
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


def torus(name, major, minor, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=32, minor_segments=6, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def build_galilean(parts, cx, cy):
	"""1610 refractor: long thin wooden tube on a simple tripod, tilted upward."""
	tube_len = 12.0
	tube_r = 0.4
	tripod_h = 8.0
	pitch = math.radians(35.0)
	# Tripod: three legs splayed outward. Build each as a box aligned along
	# the leg direction, using a rotation that pitches out from vertical by
	# a splay angle. Simpler and more robust than earlier axis-angle attempt.
	splay = math.radians(20.0)
	leg_len = tripod_h / math.cos(splay) + 0.5
	for a_deg in (0, 120, 240):
		a = math.radians(a_deg)
		# Position leg centre halfway along it
		leg_dx = math.sin(splay) * math.cos(a) * leg_len / 2
		leg_dy = math.sin(splay) * math.sin(a) * leg_len / 2
		# Rotation: yaw a about Z, then pitch splay about the horizontal axis
		# perpendicular to the yaw direction
		parts.append(box("GalileanLeg", 0.25, 0.25, leg_len,
			cx + leg_dx, cy + leg_dy, tripod_h / 2,
			rot=(math.sin(a) * splay, -math.cos(a) * splay, 0.0)))
	# Central mount head
	parts.append(cyl("GalileanHead", 0.5, 0.8, cx, cy, tripod_h + 0.4))
	# Telescope tube -- angled up along -Y toward the sky
	tube_dx = 0.0
	tube_dy = -math.sin(pitch) * tube_len / 2
	tube_dz = math.cos(pitch) * tube_len / 2
	parts.append(cyl("GalileanTube", tube_r, tube_len,
		cx + tube_dx, cy + tube_dy, tripod_h + 0.8 + tube_dz,
		rot=(math.radians(90.0) - pitch, 0.0, 0.0)))
	# Objective lens (flared end)
	obj_dx = -math.sin(pitch) * tube_len
	obj_dz = math.cos(pitch) * tube_len
	parts.append(cyl("GalileanObjective", tube_r * 1.4, 0.3,
		cx, cy + obj_dx, tripod_h + 0.8 + obj_dz,
		rot=(math.radians(90.0) - pitch, 0.0, 0.0)))


def build_hooker(parts, cx, cy):
	"""Mount Wilson 100-inch (1917): fork/yoke equatorial mount with a big
	Cassegrain tube. Simplified from a real English-yoke geometry to a fork.
	"""
	# Pier base
	pier_h = 6.0
	parts.append(cyl("HookerPier", 3.0, pier_h, cx, cy, pier_h / 2))
	# Polar axis housing (tilted, roughly at Mount Wilson's latitude ~34 deg)
	polar_pitch = math.radians(-34.0)
	polar_len = 12.0
	polar_top_z = pier_h + math.cos(polar_pitch) * polar_len
	polar_top_y = math.sin(polar_pitch) * polar_len
	parts.append(cyl("HookerPolarAxis", 1.0, polar_len,
		cx, cy + polar_top_y / 2, pier_h + math.cos(polar_pitch) * polar_len / 2,
		rot=(polar_pitch, 0.0, 0.0)))
	# Fork mount at top of polar axis
	fork_span = 8.0
	fork_h = 12.0
	for sx in (-1.0, 1.0):
		parts.append(cyl("HookerForkArm", 0.7, fork_h,
			cx + sx * fork_span / 2, cy + polar_top_y, polar_top_z + fork_h / 2))
	# Cross bar at top of fork
	parts.append(box("HookerForkCrossbar", fork_span, 1.0, 0.6,
		cx, cy + polar_top_y, polar_top_z + fork_h + 0.3))
	# Telescope tube -- large Cassegrain, mounted on the fork trunnions, pointing up
	tube_r = 3.5
	tube_len = 14.0
	tube_z = polar_top_z + fork_h * 0.5
	parts.append(cyl("HookerTube", tube_r, tube_len,
		cx, cy + polar_top_y, tube_z, rot=(math.radians(15.0), 0.0, 0.0)))
	# Top ring (secondary mirror support)
	parts.append(torus("HookerTopRing", tube_r * 0.95, 0.25,
		cx, cy + polar_top_y - math.sin(math.radians(15.0)) * tube_len / 2,
		tube_z + math.cos(math.radians(15.0)) * tube_len / 2))
	# Secondary mirror spider (crossed bars)
	for angle_deg in (0.0, 90.0):
		a = math.radians(angle_deg)
		spider_dx = math.cos(a) * tube_r * 0.9
		spider_dy = math.sin(a) * tube_r * 0.9
		# just decorative crossed bars near top ring
		if angle_deg == 0:
			parts.append(box("HookerSpider", tube_r * 1.7, 0.15, 0.15,
				cx, cy + polar_top_y - math.sin(math.radians(15.0)) * tube_len / 2,
				tube_z + math.cos(math.radians(15.0)) * tube_len / 2))
		else:
			parts.append(box("HookerSpider", 0.15, 0.15, tube_r * 1.7,
				cx, cy + polar_top_y - math.sin(math.radians(15.0)) * tube_len / 2,
				tube_z + math.cos(math.radians(15.0)) * tube_len / 2))


def build():
	clear_scene()
	parts = []
	# Base plate covering both telescopes
	# Later moved to build_base_plate style; skip for now, keep separate footprints
	# Galilean on the left, Hooker on the right
	build_galilean(parts, cx=-14.0, cy=0.0)
	build_hooker(parts, cx=8.0, cy=0.0)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "TelescopeTowers"
	merged.data.name = "TelescopeTowers"
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
