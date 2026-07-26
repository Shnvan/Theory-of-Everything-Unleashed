"""Generates the Spacetime Curvature and Gravitational Lensing exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/SpaceTimePortal/generate.py \
        -- --out art/exhibits/SpaceTimePortal/build/SpaceTimePortal.glb

Scientific visualization, per the accuracy doc: "A clearly labeled visualization
of general-relativistic curvature and lensing; never described as a working
portal."

Structure: a horizontal "rubber sheet" -- the standard museum analogy for a
spatial slice of spacetime -- deformed downward around a central mass. The
mass is shown as a small dark sphere sitting in the depression. A few marker
lines curve around the depression to hint at bent geodesics.

The depression profile is `z(r) = -A / (r + r0)`, a smoothed 1/r well. This
is a VISUAL ANALOGY, not the Schwarzschild spatial-slice embedding (which uses
z(r) = 2*sqrt(r_s * (r - r_s))). The analogy is a museum convention and the
factual card must say so.

MATERIALS ARE AN ART CHOICE. Brass sheet + Neon geodesic lines, under D-016.
"""

import math
import os
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 34.3
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0

# --- geometry ---------------------------------------------------------------

SHEET_HALF_W = 18.0     # half-width of sheet in X
SHEET_HALF_D = 15.0     # half-depth in Y
GRID_STEPS_X = 40       # sampling resolution
GRID_STEPS_Y = 34

DEPRESSION_AMPL = 12.0  # depth of the well at r=0 (approximate)
DEPRESSION_R0 = 2.0     # softening -- keeps the well finite instead of singular
BASE_Z = 30.0           # sheet base height above plinth; well descends below this

MASS_R = 1.6            # central mass marker radius

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


def sphere(name, r, x=0.0, y=0.0, z=0.0, segments=18, rings=12):
	bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=segments, ring_count=rings, location=(x, y, z))
	o = bpy.context.active_object
	o.name = name
	return o


def build_curvature_sheet(parts):
	"""A warped grid mesh, built directly by placing vertices and connecting
	them into quads. Depression is 1/(r + r0)-shaped, capped at BASE_Z below.
	"""
	verts = []
	for j in range(GRID_STEPS_Y + 1):
		for i in range(GRID_STEPS_X + 1):
			x = -SHEET_HALF_W + (2 * SHEET_HALF_W) * i / GRID_STEPS_X
			y = -SHEET_HALF_D + (2 * SHEET_HALF_D) * j / GRID_STEPS_Y
			r = math.sqrt(x * x + y * y)
			z = BASE_Z - DEPRESSION_AMPL / (r + DEPRESSION_R0) + DEPRESSION_AMPL / DEPRESSION_R0
			# Rebase so the flat far-field is at BASE_Z, well descends downward
			# The formula above evaluates: at r=0 the term (-A/r0 + A/r0) = 0 -> z = BASE_Z
			# at r=infty the term goes to A/r0 -> z = BASE_Z + A/r0 (upward from base)
			# Fix: use the negative-going form
			z = BASE_Z - DEPRESSION_AMPL * (1.0 / (r + DEPRESSION_R0) - 1.0 / (SHEET_HALF_W + DEPRESSION_R0))
			verts.append((x, y, z))

	faces = []
	stride = GRID_STEPS_X + 1
	for j in range(GRID_STEPS_Y):
		for i in range(GRID_STEPS_X):
			a = j * stride + i
			faces.append((a, a + 1, a + stride + 1, a + stride))

	mesh = bpy.data.meshes.new("CurvatureSheet_Mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new("CurvatureSheet", mesh)
	bpy.context.collection.objects.link(obj)
	# Give thickness so it isn't invisible edge-on
	bpy.context.view_layer.objects.active = obj
	mod = obj.modifiers.new("Solidify", "SOLIDIFY")
	mod.thickness = 0.25
	mod.offset = 0.0
	bpy.ops.object.modifier_apply(modifier=mod.name)
	parts.append(obj)


def build_mass_marker(parts):
	# Sit the mass in the bottom of the well
	well_bottom = BASE_Z - DEPRESSION_AMPL * (1.0 / DEPRESSION_R0 - 1.0 / (SHEET_HALF_W + DEPRESSION_R0))
	parts.append(sphere("MassPoint", MASS_R, 0.0, 0.0, well_bottom + MASS_R * 0.9))


def build_geodesic_lines(parts):
	"""Two curved marker lines representing bent light paths passing near the
	mass. Each is a chain of short cylinder segments following a bent trajectory.
	"""
	def path_z(x, y):
		r = math.sqrt(x * x + y * y)
		return BASE_Z - DEPRESSION_AMPL * (1.0 / (r + DEPRESSION_R0) - 1.0 / (SHEET_HALF_W + DEPRESSION_R0))

	# Two paths passing on opposite sides of the mass, each curved slightly
	# toward it. Represented as straight lines above the sheet with slight
	# hyperbolic bend.
	for sign in (-1.0, 1.0):
		N = 24
		pts = []
		for k in range(N + 1):
			t = -1.0 + 2.0 * k / N
			x = SHEET_HALF_W * t * 0.9
			# Impact parameter -- how close the path passes the mass
			b = sign * 3.5
			# Simple hyperbolic-like bend toward mass
			bend = 1.5 * sign / (1.0 + t * t * 3.0)
			y = b - bend
			z = path_z(x, y) + 0.3  # just above the sheet surface
			pts.append((x, y, z))
		for k in range(N):
			p1, p2 = pts[k], pts[k + 1]
			dx = p2[0] - p1[0]
			dy = p2[1] - p1[1]
			dz = p2[2] - p1[2]
			length = math.sqrt(dx * dx + dy * dy + dz * dz)
			if length < 1e-4:
				continue
			mx, my, mz = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2
			import mathutils
			direction = mathutils.Vector((dx, dy, dz)).normalized()
			up = mathutils.Vector((0.0, 0.0, 1.0))
			if abs(direction.dot(up)) > 0.9999:
				rot_euler = (0.0, 0.0, 0.0) if direction.dot(up) > 0 else (math.pi, 0.0, 0.0)
			else:
				axis = up.cross(direction).normalized()
				angle = math.acos(max(-1.0, min(1.0, up.dot(direction))))
				rot_euler = mathutils.Matrix.Rotation(angle, 4, axis).to_euler()
			c = cyl(f"Geodesic_{'A' if sign < 0 else 'B'}", 0.15, length, mx, my, mz, verts=6)
			c.rotation_euler = rot_euler
			parts.append(c)


def build_support_plinth(parts):
	"""A short pedestal that raises the sheet above the exhibit's own plinth."""
	parts.append(cyl("SupportPlinth", 3.5, 4.0, 0.0, 0.0, 2.0))


def build():
	clear_scene()
	parts = []
	build_support_plinth(parts)
	build_curvature_sheet(parts)
	build_mass_marker(parts)
	build_geodesic_lines(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "SpacetimeLensing"
	merged.data.name = "SpacetimeLensing"
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
