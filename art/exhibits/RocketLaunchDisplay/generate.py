"""Generates the Apollo 4 Saturn V + Launch Umbilical Tower exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/RocketLaunchDisplay/generate.py \
        -- --out art/exhibits/RocketLaunchDisplay/build/RocketLaunchDisplay.glb

Structure follows the vehicle designated SA-501 (Apollo 4, launched 9 Nov 1967),
its Mobile Launcher, and Launch Umbilical Tower as configured for Launch
Complex 39A at Kennedy Space Center.

Three real objects at ONE disclosed uniform display scale, per the accuracy
doc's requirement for this exhibit. The scale is set by the LUT height (the
tallest of the three) fitting the exhibit's vertical envelope: 446 ft into
63 studs, so 1 stud = 7.08 ft = 2.16 m.

At that scale the rocket alone is 51.3 studs tall and only 4.66 studs across,
so stage boundaries are the primary readable features. F-1 engine bells at the
base and the Launch Escape System spike at the tip carry the silhouette that
identifies it as Saturn V rather than any other rocket.

MATERIALS ARE AN ART CHOICE. Real Saturn V was white with black roll-pattern
stripes; this uses brass because D-016 locks the palette to marble, dark stone,
brass and glass. The LUT was painted red, also outside the palette. Dossier
states so.
"""

import math
import os
import sys

import bpy

# --- what the sources fix ----------------------------------------------------

# Saturn V, from Wikipedia's Saturn V article (cites NASA technical
# documentation).
STAGE_SIC_FT   = 138.0
STAGE_SII_FT   = 81.6
STAGE_SIVB_FT  = 58.6
STAGE_IU_FT    = 3.0
SPACECRAFT_FT  = 82.0  # CM + SM + LM adapter + LES, adjusts to fit 363 ft total
ROCKET_TOTAL_FT = STAGE_SIC_FT + STAGE_SII_FT + STAGE_SIVB_FT + STAGE_IU_FT + SPACECRAFT_FT
BASE_DIAMETER_FT = 33.0     # S-IC and S-II
UPPER_DIAMETER_FT = 21.7    # S-IVB and IU
SPACECRAFT_DIAMETER_FT = 13.0  # CM/SM; LM adapter tapers from 21.7 down

# LUT and Mobile Launcher, from the Wikipedia "Kennedy Space Center Launch
# Complex 39" article.
LUT_HEIGHT_FT = 446.0
MOBILE_LAUNCHER_W_FT = 161.0
MOBILE_LAUNCHER_D_FT = 135.0
MOBILE_LAUNCHER_H_FT = 25.0  # two-story
LUT_SWING_ARMS = 9

# --- envelope and scale ------------------------------------------------------

# RocketLaunchDisplay: shell 43.20 x 56.00 x 31.50, yaw -22 deg, plinth top
# Y 10.66, envelope ceiling Y 73.66. So 63 studs of vertical space.
SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00

STUDS_TO_BLENDER = 1.0

# Uniform display scale, fixed by LUT height fitting the envelope.
FT_PER_STUD = LUT_HEIGHT_FT / ENVELOPE_HEIGHT  # ~7.08
DISPLAY_SCALE_LINEAR = 1.0 / FT_PER_STUD

# Derived dimensions in studs
LUT_H         = LUT_HEIGHT_FT * DISPLAY_SCALE_LINEAR             # 63.00
ROCKET_H      = ROCKET_TOTAL_FT * DISPLAY_SCALE_LINEAR           # ~51.3
BASE_D        = BASE_DIAMETER_FT * DISPLAY_SCALE_LINEAR          # ~4.66
UPPER_D       = UPPER_DIAMETER_FT * DISPLAY_SCALE_LINEAR         # ~3.07
SPACECRAFT_D  = SPACECRAFT_DIAMETER_FT * DISPLAY_SCALE_LINEAR    # ~1.84

STAGE_SIC_H   = STAGE_SIC_FT * DISPLAY_SCALE_LINEAR              # ~19.5
STAGE_SII_H   = STAGE_SII_FT * DISPLAY_SCALE_LINEAR              # ~11.5
STAGE_SIVB_H  = STAGE_SIVB_FT * DISPLAY_SCALE_LINEAR             # ~8.3
STAGE_IU_H    = STAGE_IU_FT * DISPLAY_SCALE_LINEAR               # ~0.4
SPACECRAFT_H  = SPACECRAFT_FT * DISPLAY_SCALE_LINEAR             # ~11.6

ML_W = MOBILE_LAUNCHER_W_FT * DISPLAY_SCALE_LINEAR               # ~22.7
ML_D = MOBILE_LAUNCHER_D_FT * DISPLAY_SCALE_LINEAR               # ~19.1
ML_H = MOBILE_LAUNCHER_H_FT * DISPLAY_SCALE_LINEAR               # ~3.5

# The mobile launcher width outstrips the shell depth (22.7 vs 31.5) but not
# the shell width (43.20). Rotate the ML with its long axis along shell X.
# The LUT stands on the -X side, the rocket at ML centre.

LUT_X = -ML_W * 0.35  # LUT offset from ML centre toward one edge
LUT_CROSS = 2.4       # LUT cross-section (thin square lattice)

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


def cyl(name, radius, depth, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0), verts=SEGMENTS):
	bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=verts, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def cone(name, radius1, radius2, depth, x=0.0, y=0.0, z=0.0, verts=SEGMENTS):
	bpy.ops.mesh.primitive_cone_add(radius1=radius1, radius2=radius2, depth=depth, vertices=verts, location=(x, y, z))
	o = bpy.context.active_object
	o.name = name
	return o


def _bucket(buckets, key, part):
	"""Add a part to a named material bucket. Every sub-builder uses this
	instead of a bare list.append so build() can join per bucket at the end,
	one MeshPart per real material colour (D-037)."""
	if key not in buckets:
		buckets[key] = []
	buckets[key].append(part)


def build_mobile_launcher(buckets):
	"""Two-story rectangular platform. Real ML was industrial grey painted steel."""
	_bucket(buckets, "ml", box("MobileLauncherBase", ML_W, ML_D, ML_H * 0.6, 0.0, 0.0, ML_H * 0.3))
	_bucket(buckets, "ml", box("MobileLauncherUpper", ML_W * 0.95, ML_D * 0.95, ML_H * 0.4, 0.0, 0.0, ML_H * 0.8))
	# Four hold-down arms (small posts near where the rocket sits)
	rocket_r = BASE_D / 2 + 0.4
	rocket_cx = ML_W * 0.15  # rocket sits toward +X side of the ML, LUT on -X
	for i in range(4):
		a = math.radians(45 + i * 90)
		_bucket(buckets, "ml", cyl("HoldDownArm", 0.35, 1.6, rocket_cx + rocket_r * math.cos(a), rocket_r * math.sin(a), ML_H + 0.8))


def build_lut(buckets):
	"""Tall lattice tower on the -X side of the mobile launcher.

	Real LC-39A LUT was painted red-orange during the Apollo era (the
	Rocketdyne / lead-red primer colour visible in Apollo 4 launch photos).
	The retractable swing arms and their mechanical hardware were painted
	grey/silver, distinct from the tower structure.
	"""
	base_z = ML_H
	top_z = ML_H + LUT_H - ML_H  # tower rises to envelope top

	# Four vertical corner posts + horizontal braces + crane -- all red LUT structure
	half = LUT_CROSS / 2
	for sx in (-1.0, 1.0):
		for sy in (-1.0, 1.0):
			_bucket(buckets, "lut", cyl("LUTCornerPost", 0.25, top_z - base_z,
				LUT_X + sx * half, sy * half, (base_z + top_z) / 2))

	brace_spacing = 5.0
	n_braces = int((top_z - base_z) / brace_spacing)
	for i in range(1, n_braces):
		z = base_z + i * brace_spacing
		for sy in (-1.0, 1.0):
			_bucket(buckets, "lut", box("LUTHorizBrace", LUT_CROSS, 0.15, 0.15, LUT_X, sy * half, z))
		for sx in (-1.0, 1.0):
			_bucket(buckets, "lut", box("LUTHorizBrace", 0.15, LUT_CROSS, 0.15, LUT_X + sx * half, 0.0, z))

	_bucket(buckets, "lut", box("LUTCranePlatform", LUT_CROSS, LUT_CROSS, 0.5, LUT_X, 0.0, top_z - 0.3))
	_bucket(buckets, "lut", box("LUTCraneJib", 6.0, 0.35, 0.35, LUT_X + 3.0, 0.0, top_z - 0.9))

	# Swing arms + tips -- grey, in the mobile-launcher bucket (they're
	# mechanical equipment attached to the tower, not tower structure itself)
	rocket_cx = ML_W * 0.15
	arm_span = rocket_cx - LUT_X - half - BASE_D / 2
	for i in range(LUT_SWING_ARMS):
		frac = (i + 1) / (LUT_SWING_ARMS + 1)
		z = base_z + (top_z - base_z) * frac
		local_rocket_r = _rocket_radius_at(z - base_z)
		reach = rocket_cx - LUT_X - half - local_rocket_r
		arm_cx = LUT_X + half + reach / 2
		_bucket(buckets, "ml", box("LUTSwingArm", reach, 0.4, 0.35, arm_cx, 0.0, z))
		_bucket(buckets, "ml", cyl("LUTArmTip", 0.25, 0.6, arm_cx + reach / 2, 0.0, z))


def _rocket_radius_at(z_from_ml_top):
	"""Rocket radius at a given height above the mobile launcher top."""
	z = z_from_ml_top
	if z < STAGE_SIC_H:
		return BASE_D / 2
	z -= STAGE_SIC_H
	if z < STAGE_SII_H:
		return BASE_D / 2
	z -= STAGE_SII_H
	if z < STAGE_SIVB_H + STAGE_IU_H:
		return UPPER_D / 2
	z -= STAGE_SIVB_H + STAGE_IU_H
	if z < SPACECRAFT_H:
		return SPACECRAFT_D / 2
	return 0.0


def build_saturn_v(buckets):
	"""The vehicle, from base of S-IC to tip of LES.

	Real Saturn V was painted white with black roll-pattern stripes at stage
	joins (for optical tracking during launch). F-1 engine bells and the LES
	motor were dark grey / metallic. The Command Module was silver-grey with
	an ablative heat-shield coating.

	Material buckets used:
	  body   -> white (SmoothPlastic, Institutional white)
	  engine -> dark grey (Metal, dark grey / near-black)
	"""
	rocket_cx = ML_W * 0.15
	z = ML_H

	# S-IC body + fins (all white)
	_bucket(buckets, "body", cyl("Saturn_S_IC", BASE_D / 2, STAGE_SIC_H, rocket_cx, 0.0, z + STAGE_SIC_H / 2, verts=SEGMENTS))
	for i in range(4):
		a = math.radians(45 + i * 90)
		fin_r = BASE_D / 2
		fin_h = 4.0
		fin_w = 1.0
		fin_out = 1.2
		_bucket(buckets, "body", box("Saturn_S_IC_Fin", fin_out, fin_w, fin_h,
			rocket_cx + (fin_r + fin_out / 2) * math.cos(a),
			(fin_r + fin_out / 2) * math.sin(a),
			z + fin_h / 2,
			rot=(0.0, 0.0, a)))
	# Five F-1 engine bells at S-IC base -- dark grey, in the engine bucket
	for i in range(5):
		if i == 0:
			ex, ey = 0.0, 0.0
		else:
			a = math.radians(90 + (i - 1) * 90)
			r = BASE_D / 2 * 0.55
			ex, ey = r * math.cos(a), r * math.sin(a)
		_bucket(buckets, "engine", cone("Saturn_F1_Bell", 0.55, 0.35, 1.6,
			rocket_cx + ex, ey, z - 0.8))
	z += STAGE_SIC_H

	# Interstage (white)
	_bucket(buckets, "body", cyl("Saturn_Interstage_SIC_SII", BASE_D / 2 * 0.98, 0.6, rocket_cx, 0.0, z + 0.3))
	z += 0.6

	# S-II (white)
	_bucket(buckets, "body", cyl("Saturn_S_II", BASE_D / 2, STAGE_SII_H - 0.6, rocket_cx, 0.0, z + (STAGE_SII_H - 0.6) / 2))
	z += STAGE_SII_H - 0.6

	# S-II/S-IVB interstage taper (white)
	taper_h = 1.2
	_bucket(buckets, "body", cone("Saturn_Interstage_SII_SIVB", BASE_D / 2, UPPER_D / 2, taper_h,
		rocket_cx, 0.0, z + taper_h / 2))
	z += taper_h

	# S-IVB (white)
	_bucket(buckets, "body", cyl("Saturn_S_IVB", UPPER_D / 2, STAGE_SIVB_H - taper_h, rocket_cx, 0.0, z + (STAGE_SIVB_H - taper_h) / 2))
	z += STAGE_SIVB_H - taper_h

	# Instrument Unit (white with black stripe in reality; simplified to white)
	_bucket(buckets, "body", cyl("Saturn_InstrumentUnit", UPPER_D / 2 * 1.02, STAGE_IU_H, rocket_cx, 0.0, z + STAGE_IU_H / 2))
	z += STAGE_IU_H

	# Apollo spacecraft assembly
	adapter_h = SPACECRAFT_H * 0.30
	_bucket(buckets, "body", cone("Apollo_LMAdapter", UPPER_D / 2, SPACECRAFT_D / 2, adapter_h,
		rocket_cx, 0.0, z + adapter_h / 2))
	z += adapter_h
	sm_h = SPACECRAFT_H * 0.32
	_bucket(buckets, "body", cyl("Apollo_ServiceModule", SPACECRAFT_D / 2, sm_h, rocket_cx, 0.0, z + sm_h / 2))
	z += sm_h
	# Command Module -- silver-grey heat shield, put in engine bucket for the darker material
	cm_h = SPACECRAFT_H * 0.14
	_bucket(buckets, "engine", cone("Apollo_CommandModule", SPACECRAFT_D / 2, SPACECRAFT_D / 2 * 0.35, cm_h,
		rocket_cx, 0.0, z + cm_h / 2))
	z += cm_h
	# LES tower -- white body with the LES-tip motor at top
	les_h = SPACECRAFT_H * 0.24
	_bucket(buckets, "body", cyl("Apollo_LES", SPACECRAFT_D / 2 * 0.18, les_h, rocket_cx, 0.0, z + les_h / 2))
	# Motor nozzle at very top (dark)
	_bucket(buckets, "engine", cone("Apollo_LESTip", SPACECRAFT_D / 2 * 0.10, SPACECRAFT_D / 2 * 0.02, 0.4,
		rocket_cx, 0.0, z + les_h + 0.2))


BUCKET_TO_MESH_NAME = {
	"body":   "SaturnV_Body",     # white rocket body + fins + LM adapter + SM + LES tower
	"engine": "SaturnV_Engines",  # F-1 bells + Command Module + LES tip (dark grey)
	"lut":    "SaturnV_LUT",      # LUT tower + crane (red)
	"ml":     "SaturnV_ML",       # Mobile Launcher + hold-down arms + swing arms (grey)
}


def _join_bucket(name, parts):
	bpy.ops.object.select_all(action="DESELECT")
	for p in parts:
		p.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	if len(parts) > 1:
		bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	merged.data.name = name
	# Every bucket keeps its authored world position -- do NOT re-origin, or the
	# meshes drift apart when placed in Studio at a shared PivotTo. Shared origin
	# is the entire point of the multi-mesh material split.
	return merged


def build():
	clear_scene()
	buckets = {}
	build_mobile_launcher(buckets)
	build_saturn_v(buckets)
	build_lut(buckets)

	# Deterministic bucket order so the exported GLB names are stable across runs.
	objs = []
	for key in ("body", "engine", "lut", "ml"):
		if key in buckets and buckets[key]:
			objs.append(_join_bucket(BUCKET_TO_MESH_NAME[key], buckets[key]))
	return objs


def report(objs):
	total_tris = 0
	lo = [float("inf")] * 3
	hi = [float("-inf")] * 3

	names = []
	for o in objs:
		tris = sum(max(len(p.vertices) - 2, 0) for p in o.data.polygons)
		total_tris += tris
		names.append(o.name)
		d = o.dimensions
		print(f"GEN_PART {o.name} tris={tris} size={d.x:.2f}x{d.y:.2f}x{d.z:.2f}")
		if tris > 20000:
			raise SystemExit(f"FAIL: {o.name} has {tris} triangles, over the 20000 per-mesh cap")
		for v in o.data.vertices:
			w = o.matrix_world @ v.co
			for i in range(3):
				lo[i] = min(lo[i], w[i])
				hi[i] = max(hi[i], w[i])

	size = [hi[i] - lo[i] for i in range(3)]
	print(f"GEN_PARTS {len(objs)}")
	print(f"GEN_TRIANGLES {total_tris}")
	print(f"GEN_SIZE_STUDS {size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f}")
	print(f"GEN_SCALE 1 stud = {FT_PER_STUD:.2f} ft = {FT_PER_STUD * 0.3048:.2f} m")

	# Assert multi-mesh split preserved: if a future edit collapsed buckets,
	# the polychrome pilot silently loses its whole point.
	expected = {"SaturnV_Body", "SaturnV_Engines", "SaturnV_LUT", "SaturnV_ML"}
	if set(names) != expected:
		raise SystemExit(f"FAIL: expected exactly {sorted(expected)}, got {sorted(names)}")
	print("GEN_SPLIT_OK 4 objects, one per material group")

	if size[2] > ENVELOPE_HEIGHT + 0.5:  # small tolerance for LES tip
		raise SystemExit(f"FAIL: height {size[2]:.2f} exceeds the {ENVELOPE_HEIGHT:.2f} stud envelope")
	if size[0] > SHELL_WIDTH:
		raise SystemExit(f"FAIL: width {size[0]:.2f} overhangs the {SHELL_WIDTH:.2f} stud shell")
	if size[1] > SHELL_DEPTH:
		raise SystemExit(f"FAIL: depth {size[1]:.2f} overhangs the {SHELL_DEPTH:.2f} stud shell")

	if LUT_H <= ROCKET_H:
		raise SystemExit(f"FAIL: LUT height {LUT_H:.2f} not greater than rocket {ROCKET_H:.2f}")

	print(f"GEN_SHELL_MARGIN {SHELL_WIDTH - size[0]:.2f} x {SHELL_DEPTH - size[1]:.2f} studs")
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

	objs = build()
	report(objs)

	os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
	bpy.ops.export_scene.gltf(filepath=out_path, export_format="GLB", use_selection=False, export_apply=True)
	print(f"GEN_WROTE {out_path}")


if __name__ == "__main__":
	main()
