"""Generates the Cavendish torsion balance exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/GravityControlChamber/generate.py \
        -- --out art/exhibits/GravityControlChamber/build/GravityControlChamber.glb

Structure follows Henry Cavendish's 1798 experiment "to determine the density of
the Earth", published in Philosophical Transactions of the Royal Society vol. 88
pp. 469-526. The apparatus is a torsion balance: a horizontal rod carrying two
small lead balls, suspended in the middle by a thin fibre, with two much larger
lead balls placed near the small ones on a separate swing arm. Gravitational
attraction between the balls twists the fibre by a measurable angle, from which
Cavendish computed G.

THIS REPLACES A FICTIONAL ENERGY CHAMBER. The prototype it supersedes was built
from Chamber, Core, and FieldRing_01..08 -- a science-fantasy device, not an
apparatus. Wrong class of object entirely, and the internal Studio identity
GravityControlChamber is retained only because the accuracy doc's real-name pass
renames it to CAVENDISH TORSION BALANCE. See D-017.

MATERIALS ARE AN ART CHOICE. Real enclosure was mahogany; this uses brass frame
with glass panels because D-016 locks the palette to marble, dark stone, brass
and glass. The dossier says so.
"""

import math
import os
import sys

import bpy

# --- what the primary source fixes -------------------------------------------

# From Cavendish 1798, cited in Wikipedia. Wire specifications not given in the
# secondary source; the article says Cavendish switched to a "stiffer wire"
# after his third experiment but records no material or length. Fibre thickness
# below is display-only, not measured, and the dossier says so.
REAL_ROD_LENGTH_MM = 1830.0        # 6 ft
REAL_SMALL_BALL_MM = 51.0          # 2 in
REAL_LARGE_BALL_MM = 300.0         # 12 in
REAL_BALL_SEPARATION_MM = 225.0    # 8.85 in
REAL_CASE_WIDTH_MM = 1980.0
REAL_CASE_HEIGHT_MM = 1270.0
REAL_CASE_DEPTH_MM = 140.0

# --- envelope -----------------------------------------------------------------

# Shell 43.20 x 54.00 x 31.50, yaw -48 deg, plinth top Y 8.16, envelope ceiling
# Y 71.16 (so 63 studs of headroom). Rod length is the sizing driver: at 30
# studs it fits the shell depth comfortably.
SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00

STUDS_TO_BLENDER = 1.0

# --- scale --------------------------------------------------------------------

# 17x linear. Chosen so the 1.83 m rod becomes 31.1 studs, filling the shell's
# depth without touching it. Everything except the small balls scales at this
# rate; the small balls are enlarged for visibility -- at true 17x they would be
# 0.87 studs across and read as pinheads at gameplay distance. Enlargement is
# disclosed in the dossier.
DISPLAY_SCALE = 17.0
MM_PER_STUD = 1000.0 / DISPLAY_SCALE  # ~58.8 mm per stud

ROD_LENGTH   = REAL_ROD_LENGTH_MM / MM_PER_STUD          # ~31.1
LARGE_BALL_D = REAL_LARGE_BALL_MM / MM_PER_STUD          # ~5.1
BALL_SEP     = REAL_BALL_SEPARATION_MM / MM_PER_STUD     # ~3.8
CASE_WIDTH   = REAL_CASE_WIDTH_MM / MM_PER_STUD          # ~33.7
CASE_HEIGHT  = REAL_CASE_HEIGHT_MM / MM_PER_STUD         # ~21.6
CASE_DEPTH   = REAL_CASE_DEPTH_MM / MM_PER_STUD          # ~2.4

# Small balls: displayed at 1.6 studs to be legible. Real is 0.87.
SMALL_BALL_D = 1.6

ROD_THICKNESS = 0.35
FIBRE_THICKNESS = 0.14

# Vertical placement inside the exhibit. Case sits on plinth; rod is at case
# mid-height; the supporting gantry rises above the case.
CASE_BASE_Y = 1.0                                    # above a base plate
ROD_Y = CASE_BASE_Y + CASE_HEIGHT * 0.55
GANTRY_TOP_Y = CASE_BASE_Y + CASE_HEIGHT + 12.0
BASE_PLATE_H = 1.5

SEGMENTS = 20


def clear_scene() -> None:
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


def cyl(name, radius, depth, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0), verts=SEGMENTS):
	bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=verts, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def sphere(name, r, x=0.0, y=0.0, z=0.0, segments=18, rings=12):
	bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=segments, ring_count=rings, location=(x, y, z))
	o = bpy.context.active_object
	o.name = name
	return o


def build_base_plate(parts):
	parts.append(box("BasePlate", CASE_WIDTH + 4.0, 22.0, BASE_PLATE_H, 0.0, 0.0, BASE_PLATE_H / 2))


def build_case(parts):
	"""Frame-only cabinet outline. No panels.

	Cavendish's real enclosure was a mahogany box shielding the mechanism from
	air currents. That is a real reason in the lab and a bad reason in a museum
	exhibit -- panels hide the very thing a visitor is here to see. So this
	renders the cabinet as brass corner posts and rails only, with no walls, and
	the balance stands exposed inside them.

	The first pass built solid rear and base panels, and the render showed
	exactly nothing: the panel dominated the frame and every ball and rod hid
	behind it. Removing the panels is the fix.
	"""
	x = CASE_WIDTH / 2
	y_dep = CASE_DEPTH * 4.0  # thickened depth for a readable outline
	z_bot = CASE_BASE_Y
	z_top = CASE_BASE_Y + CASE_HEIGHT
	frame_t = 0.35
	# Four vertical corner posts
	for sx in (-1.0, 1.0):
		for sy in (-1.0, 1.0):
			parts.append(cyl("CabinetPost", 0.3, CASE_HEIGHT,
				sx * x, sy * y_dep, (z_bot + z_top) / 2))
	# Top and bottom horizontal rails on both sides
	for sy in (-1.0, 1.0):
		parts.append(box("CabinetTopRail", CASE_WIDTH, frame_t, frame_t, 0.0, sy * y_dep, z_top))
		parts.append(box("CabinetBottomRail", CASE_WIDTH, frame_t, frame_t, 0.0, sy * y_dep, z_bot))


def build_torsion_rod_and_small_balls(parts):
	"""The horizontal beam suspended from a fibre, carrying two small lead balls."""
	# Rod along X axis at height ROD_Y
	parts.append(cyl("TorsionRod", ROD_THICKNESS, ROD_LENGTH, 0.0, 0.0, ROD_Y, rot=(0.0, math.radians(90.0), 0.0)))
	# Two small balls, one at each end
	half = ROD_LENGTH / 2 - SMALL_BALL_D * 0.3
	for sx in (-1.0, 1.0):
		parts.append(sphere("SmallBall", SMALL_BALL_D / 2, sx * half, 0.0, ROD_Y))


def build_fibre(parts):
	"""Suspension fibre from case top to rod centre."""
	fibre_top = CASE_BASE_Y + CASE_HEIGHT - 0.4
	fibre_h = fibre_top - ROD_Y
	parts.append(cyl("TorsionFibre", FIBRE_THICKNESS, fibre_h, 0.0, 0.0, (ROD_Y + fibre_top) / 2))


def build_swing_arm_and_large_balls(parts):
	"""Two large lead balls suspended from a swing arm above the case.

	Cavendish's swing arm rotates about a vertical axis to bring the large balls
	close to the small ones. Drawn in the "close" position (the interesting one).
	The arm is above the case in this compressed layout; in the real apparatus
	the large balls were at the same height as the small ones, but that would put
	them inside the case here. This is stylised, dossier says so.
	"""
	arm_z = ROD_Y  # keep balls at rod height, the physics-honest position

	# Gravitational torque on the rod requires the force to be TANGENT to the
	# small ball's swing path. The rod is along X and swings in the XY plane
	# (rotating about the vertical Z fibre), so a tangent force is in +/-Y.
	# That means each large ball goes at the same X as its small ball, offset
	# perpendicularly in Y by BALL_SEP -- not further out along the rod axis,
	# which was the first draft's mistake.
	small_ball_centre_x = ROD_LENGTH / 2 - SMALL_BALL_D * 0.3

	# The two large balls sit on the same side (+Y, viewer's side) so both are
	# visible in a single view. Real Cavendish alternated sides on his two
	# balls to double the torque; the visualisation gives up that detail for
	# clarity. Dossier states so.
	by = BALL_SEP + LARGE_BALL_D / 2 - SMALL_BALL_D / 2

	for sx in (-1.0, 1.0):
		bx = sx * small_ball_centre_x
		parts.append(sphere("LargeBall", LARGE_BALL_D / 2, bx, by, arm_z, segments=24, rings=16))
		# Hanger rod up to the swing arm above
		parts.append(cyl("LargeBallHanger", 0.18,
			GANTRY_TOP_Y - arm_z - LARGE_BALL_D / 2,
			bx, by, (arm_z + LARGE_BALL_D / 2 + GANTRY_TOP_Y) / 2))
	# Swing arm across the top
	parts.append(box("SwingArm", 2 * small_ball_centre_x + 1.5, 0.6, 0.5,
		0.0, by, GANTRY_TOP_Y))
	# Swing arm pivot column, on the centre line
	parts.append(cyl("SwingArmPivot", 0.4, GANTRY_TOP_Y - CASE_BASE_Y - CASE_HEIGHT,
		0.0, by, (GANTRY_TOP_Y + CASE_BASE_Y + CASE_HEIGHT) / 2))


def build_gantry(parts):
	"""Overhead structure holding the swing arm."""
	# Two vertical support columns at case corners, rising to top of gantry
	for sx in (-1.0, 1.0):
		parts.append(cyl("GantryColumn", 0.45,
			GANTRY_TOP_Y - CASE_BASE_Y,
			sx * (CASE_WIDTH / 2 + 0.6), -CASE_DEPTH * 4.0,
			(GANTRY_TOP_Y + CASE_BASE_Y) / 2))
	# Cross-beam at the top connecting the two columns
	parts.append(box("GantryCrossbeam", CASE_WIDTH + 1.4, 0.5, 0.5,
		0.0, -CASE_DEPTH * 4.0, GANTRY_TOP_Y))


def build() -> None:
	clear_scene()
	parts = []
	build_base_plate(parts)
	build_case(parts)
	build_torsion_rod_and_small_balls(parts)
	build_fibre(parts)
	build_swing_arm_and_large_balls(parts)
	build_gantry(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "CavendishBalance"
	merged.data.name = "CavendishBalance"
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
	bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
	merged.location = (0.0, 0.0, 0.0)


def report(obj):
	mesh = obj.data
	tris = sum(max(len(p.vertices) - 2, 0) for p in mesh.polygons)
	d = obj.dimensions

	print(f"GEN_OBJECT {obj.name}")
	print(f"GEN_TRIANGLES {tris}")
	print(f"GEN_VERTICES {len(mesh.vertices)}")
	print(f"GEN_SIZE_STUDS {d.x:.2f} x {d.y:.2f} x {d.z:.2f}")
	print(f"GEN_SCALE 1 stud = {MM_PER_STUD:.1f} mm, real 1.83 m rod -> {ROD_LENGTH:.2f} studs")

	if tris > 20000:
		raise SystemExit(f"FAIL: {tris} triangles exceeds the 20000 per-mesh cap")

	# Shell binds, not exhibit extents.
	if d.z > ENVELOPE_HEIGHT:
		raise SystemExit(f"FAIL: height {d.z:.2f} exceeds the {ENVELOPE_HEIGHT:.2f} stud envelope")
	if d.x > SHELL_WIDTH:
		raise SystemExit(f"FAIL: width {d.x:.2f} overhangs the {SHELL_WIDTH:.2f} stud collision shell")
	if d.y > SHELL_DEPTH:
		raise SystemExit(f"FAIL: depth {d.y:.2f} overhangs the {SHELL_DEPTH:.2f} stud collision shell")

	# The teaching point of this exhibit is the rod-plus-large-ball geometry.
	# Assert the rod is close to the real 6-foot proportion (in studs) so a
	# future edit cannot silently shrink it.
	expected_rod = REAL_ROD_LENGTH_MM / MM_PER_STUD
	if abs(ROD_LENGTH - expected_rod) > 0.01:
		raise SystemExit(f"FAIL: rod length constant drifted from {expected_rod:.2f} to {ROD_LENGTH:.2f}")

	print(f"GEN_SHELL_MARGIN {SHELL_WIDTH - d.x:.2f} x {SHELL_DEPTH - d.y:.2f} studs")
	print("GEN_BUDGET_OK yes")
	print("GEN_ENVELOPE_OK yes")


def main() -> None:
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
