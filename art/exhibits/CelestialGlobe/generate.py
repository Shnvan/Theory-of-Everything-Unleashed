"""Generates the Blaeu Celestial Globe (1603) exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/CelestialGlobe/generate.py \
        -- --out art/exhibits/CelestialGlobe/build/CelestialGlobe.glb

Structure follows Willem Janszoon Blaeu's 1603 celestial globe (Amsterdam),
Science Museum Group object 1980-1913 and its many surviving pairs at other
institutions. The 1603 pair (celestial + terrestrial) was Blaeu's first
published globe series and introduced the newly-mapped southern constellations
based on Dutch expedition observations, built on top of Tycho Brahe's star
catalogue.

Real construction: papier-mache sphere, internally hollow, covered with
plaster; 12 printed gores plus 2 polar caps pasted on. Suspended within a
graduated meridian ring pivoting on an ornate wooden stand with a horizon
ring at globe-centre height.

MATERIALS ARE AN ART CHOICE. Real globes are hand-coloured paper on plaster;
this uses brass under D-016. The dossier says so.
"""

import math
import os
import sys

import bpy

# --- what the sources fix ----------------------------------------------------

REAL_DIAMETER_MM = 340.0  # 34 cm, Blaeu's 1603 pair standard diameter

# --- envelope ----------------------------------------------------------------

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00

STUDS_TO_BLENDER = 1.0

# --- scale -------------------------------------------------------------------

# Scale to fill the vertical envelope reasonably. Real globe 34 cm; total
# assembly with stand ~1 m typical for library-scale globes. If total ~55
# studs, that maps 1 stud to ~1.8 cm.
GLOBE_DIAMETER = 22.0        # sphere diameter in studs; shell depth 31.5 binds
STAND_HEIGHT = 20.0          # height from plinth top to globe centre
GLOBE_CENTRE_Z = STAND_HEIGHT
MERIDIAN_RING_R = GLOBE_DIAMETER / 2 + 1.2
HORIZON_RING_R = GLOBE_DIAMETER / 2 + 2.4

DISPLAY_MM_PER_STUD = REAL_DIAMETER_MM / GLOBE_DIAMETER  # ~11.3 mm per stud

RING_THICKNESS = 0.9
RING_WIDTH = 1.8

SPHERE_SEGMENTS = 32
SPHERE_RINGS = 20
RING_MAJOR_SEGMENTS = 48
RING_MINOR_SEGMENTS = 6


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


def cyl(name, radius, depth, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0), verts=20):
	bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=verts, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def sphere(name, r, x=0.0, y=0.0, z=0.0, segments=SPHERE_SEGMENTS, rings=SPHERE_RINGS):
	bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=segments, ring_count=rings, location=(x, y, z))
	o = bpy.context.active_object
	o.name = name
	return o


def torus(name, major, minor, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_torus_add(
		major_radius=major, minor_radius=minor,
		major_segments=RING_MAJOR_SEGMENTS, minor_segments=RING_MINOR_SEGMENTS,
		location=(x, y, z), rotation=rot,
	)
	o = bpy.context.active_object
	o.name = name
	return o


def build_globe(parts):
	"""The papier-mache celestial sphere."""
	parts.append(sphere("Globe", GLOBE_DIAMETER / 2, 0.0, 0.0, GLOBE_CENTRE_Z))
	bpy.ops.object.shade_smooth()


def build_meridian_ring(parts):
	"""Vertical brass ring the globe pivots inside. Graduated in real life."""
	parts.append(torus("MeridianRing", MERIDIAN_RING_R, RING_THICKNESS,
		0.0, 0.0, GLOBE_CENTRE_Z, rot=(0.0, math.radians(90.0), 0.0)))


def build_horizon_ring(parts):
	"""Horizontal wooden ring at globe-centre height. Held by the stand columns
	and carries zodiac and calendar scales in real life. Rendered here as two
	stacked toruses so the ring reads as a wider flat band."""
	parts.append(torus("HorizonRingOuter", HORIZON_RING_R, RING_THICKNESS,
		0.0, 0.0, GLOBE_CENTRE_Z))
	parts.append(torus("HorizonRingInner", HORIZON_RING_R * 0.92, RING_THICKNESS,
		0.0, 0.0, GLOBE_CENTRE_Z))
	# Web ring linking to meridian pivot points
	parts.append(cyl("HorizonPivot", 0.6, HORIZON_RING_R * 2 * 0.98,
		0.0, 0.0, GLOBE_CENTRE_Z, rot=(math.radians(90.0), 0.0, 0.0)))


def build_stand(parts):
	"""Four-legged wooden stand supporting the horizon ring.

	Turned column bases on four splayed feet, joined by cross-stretchers, with
	four vertical posts rising to meet the horizon ring at four points. This is
	the Baroque library-globe silhouette; real Blaeu 1603 stands were more
	ornate but this reads as the same class of object.
	"""
	foot_span = HORIZON_RING_R * 1.1  # keep total diameter inside shell depth 31.5
	foot_h = 1.4
	# Four splayed feet
	for i in range(4):
		a = math.radians(45 + i * 90)
		fx = math.cos(a) * foot_span
		fy = math.sin(a) * foot_span
		# Foot
		parts.append(box("StandFoot", 2.2, 2.2, foot_h, fx, fy, foot_h / 2))
		# Column rising from foot to horizon ring
		col_h = GLOBE_CENTRE_Z - foot_h
		parts.append(cyl("StandColumn", 0.7, col_h, fx * 0.65, fy * 0.65, foot_h + col_h / 2))
		# Turned finial where column meets horizon ring
		parts.append(sphere("StandFinial", 0.9, fx * 0.65, fy * 0.65, GLOBE_CENTRE_Z - 0.2, segments=14, rings=8))
	# Cross-stretchers between adjacent feet, at foot height
	for i in range(4):
		a1 = math.radians(45 + i * 90)
		a2 = math.radians(45 + (i + 1) * 90)
		x1, y1 = math.cos(a1) * foot_span * 0.55, math.sin(a1) * foot_span * 0.55
		x2, y2 = math.cos(a2) * foot_span * 0.55, math.sin(a2) * foot_span * 0.55
		mx, my = (x1 + x2) / 2, (y1 + y2) / 2
		length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
		yaw = math.atan2(y2 - y1, x2 - x1)
		parts.append(box("StandStretcher", length, 0.4, 0.4, mx, my, foot_h * 1.2, rot=(0.0, 0.0, yaw)))
	# Central turned column below globe, decorative
	parts.append(cyl("StandCentreColumn", 1.2, GLOBE_CENTRE_Z - foot_h,
		0.0, 0.0, foot_h + (GLOBE_CENTRE_Z - foot_h) / 2))


def build_polar_axis_indicator(parts):
	"""A thin rod along the polar axis, sticking out top and bottom of the
	globe -- the axis about which the globe rotates in its meridian ring."""
	axis_len = GLOBE_DIAMETER + 4.0
	tilt = math.radians(23.44)  # obliquity, shown by tilting the meridian ring stops
	# Just draw the polar axis, keep vertical for simplicity
	parts.append(cyl("PolarAxis", 0.2, axis_len, 0.0, 0.0, GLOBE_CENTRE_Z))


def build():
	clear_scene()
	parts = []
	build_stand(parts)
	build_horizon_ring(parts)
	build_meridian_ring(parts)
	build_polar_axis_indicator(parts)
	build_globe(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "BlaeuCelestialGlobe"
	merged.data.name = "BlaeuCelestialGlobe"
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
	print(f"GEN_SCALE 1 stud = {DISPLAY_MM_PER_STUD:.2f} mm (real 34 cm globe -> {GLOBE_DIAMETER:.0f} studs)")

	if tris > 20000:
		raise SystemExit(f"FAIL: {tris} triangles exceeds the 20000 per-mesh cap")
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
