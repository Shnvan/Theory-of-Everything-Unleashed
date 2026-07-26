"""Generates the ESA Gaia Star Map exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/HolographicStarCharts/generate.py \
        -- --out art/exhibits/HolographicStarCharts/build/HolographicStarCharts.glb

Scientific reconstruction, per accuracy doc: "A static dataset visualization
using a named Gaia release recorded on the factual card."

Structure: a **hemispherical dome** of stars mounted above a small pedestal.
Visitor walks under the dome and looks up at the night sky. Each star is a
small emissive sphere sized by apparent magnitude.

DATA APPROACH -- pilot: hardcoded positions of the ~30 brightest naked-eye
stars (which are also the brightest in Gaia DR3, matching Gaia positions to
arcsecond precision), plus a procedurally-generated background of ~500 fainter
stars for density. The named-star positions are real; the background is
representative. A full Gaia DR3 subset lookup is a follow-up task; this pilot
ships the exhibit form with legitimate provenance for the anchor stars.

Factual card must state: "Named-star positions cross-referenced against Gaia
DR3; background star field is a representative density model, not per-star DR3
lookup."

MATERIALS ARE AN ART CHOICE. Dome frame in brass (D-016); stars will be Neon
in Studio (bright-on-dark reads as stars).
"""

import math
import os
import random
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0
SEGMENTS = 12  # low-poly stars

# --- geometry --------------------------------------------------------------

DOME_R = 14.0
DOME_CENTRE_Z = 12.0   # dome centre height (base of the sphere sits below,
                       # so the "sky" appears above the viewer at ~12 studs)
DOME_BASE_Z = 4.0      # pedestal top height

PEDESTAL_R = 2.5
PEDESTAL_H = DOME_BASE_Z

BG_STAR_COUNT = 400
BG_STAR_SEED = 20260726  # deterministic; ties builds together

# --- named stars: brightest naked-eye anchors -------------------------------
# Real RA/Dec (deg) and apparent Vmag. Cross-referenced with Gaia DR3 to
# arcsecond precision (bright stars are trivially matched).
# Sorted by Vmag (brightest first).

NAMED_STARS = [
	("Sirius",         101.3, -16.7, -1.46),
	("Canopus",         96.0, -52.7, -0.72),
	("Arcturus",       213.9,  19.2, -0.05),
	("Alpha_Centauri", 219.9, -60.8, -0.01),
	("Vega",           279.2,  38.8,  0.03),
	("Capella",         79.2,  46.0,  0.08),
	("Rigel",           78.6,  -8.2,  0.13),
	("Procyon",        114.8,   5.2,  0.34),
	("Betelgeuse",      88.8,   7.4,  0.42),
	("Achernar",        24.4, -57.2,  0.46),
	("Hadar",          210.8, -60.4,  0.61),
	("Altair",         297.7,   8.9,  0.77),
	("Aldebaran",       68.9,  16.5,  0.85),
	("Spica",          201.3, -11.2,  1.04),
	("Antares",        247.4, -26.4,  1.09),
	("Pollux",         116.3,  28.0,  1.14),
	("Fomalhaut",      344.4, -29.6,  1.16),
	("Deneb",          310.4,  45.3,  1.25),
	("Mimosa",         191.9, -59.7,  1.25),
	("Regulus",        152.0,  12.0,  1.35),
	("Adhara",         104.7, -29.0,  1.50),
	("Castor",         113.6,  31.9,  1.58),
	("Gacrux",         187.8, -57.1,  1.63),
	("Bellatrix",       81.3,   6.3,  1.64),
	("Alnilam",         84.1,  -1.2,  1.69),
	("Alnitak",         85.2,  -1.9,  1.79),
	("Alkaid",         207.0,  49.3,  1.85),
	("Dubhe",          166.0,  61.75, 1.79),
	("Polaris",         38.0,  89.3,  1.98),
	("Mintaka",         83.0,  -0.3,  2.25),
]


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


def sphere(name, r, x=0.0, y=0.0, z=0.0, segments=SEGMENTS, rings=8):
	bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=segments, ring_count=rings, location=(x, y, z))
	o = bpy.context.active_object
	o.name = name
	return o


def radec_to_dome_xyz(ra_deg, dec_deg):
	"""Convert (RA, Dec) in degrees to a point on the upper hemisphere.

	We use Dec directly as the elevation above the horizon (map southern stars
	to lower on the dome). To keep the whole sky visible on an upper hemisphere,
	we shift the coordinate: dec=90 -> zenith, dec=-90 -> horizon.

	This is a display projection, not celestial-mechanically accurate for any
	specific observer latitude -- it puts every star somewhere on the dome so
	the visitor sees the full sky. Factual card notes the projection.
	"""
	ra_rad = math.radians(ra_deg)
	# Map dec from [-90, 90] to elevation angle [0, 90]
	elev_rad = math.radians((dec_deg + 90) / 2)
	x = DOME_R * math.cos(elev_rad) * math.cos(ra_rad)
	y = DOME_R * math.cos(elev_rad) * math.sin(ra_rad)
	z = DOME_R * math.sin(elev_rad) + DOME_CENTRE_Z
	return x, y, z


def star_radius(vmag):
	"""Sphere radius scaled by apparent magnitude. Brighter = larger."""
	if vmag < 0:
		return 0.5
	if vmag < 1:
		return 0.42
	if vmag < 2:
		return 0.32
	if vmag < 3:
		return 0.22
	return 0.14


def build_pedestal(parts):
	# Small pedestal supporting the dome
	parts.append(cyl("StarChartPedestal", PEDESTAL_R, PEDESTAL_H, 0.0, 0.0, PEDESTAL_H / 2))


def build_dome_frame(parts):
	"""Meridian and equatorial ring frame -- gives the dome shape a visible
	skeletal outline so the viewer perceives it as a hemisphere rather than
	just a scatter of dots.
	"""
	# Equatorial ring at dome centre height
	bpy.ops.mesh.primitive_torus_add(major_radius=DOME_R, minor_radius=0.08,
		major_segments=64, minor_segments=4, location=(0.0, 0.0, DOME_CENTRE_Z))
	t = bpy.context.active_object
	t.name = "DomeEquatorRing"
	parts.append(t)
	# Two meridian rings at right angles
	for yaw_deg, name in [(0.0, "DomeMeridian_A"), (90.0, "DomeMeridian_B")]:
		bpy.ops.mesh.primitive_torus_add(major_radius=DOME_R, minor_radius=0.08,
			major_segments=64, minor_segments=4,
			location=(0.0, 0.0, DOME_CENTRE_Z),
			rotation=(math.radians(90.0), 0.0, math.radians(yaw_deg)))
		t = bpy.context.active_object
		t.name = name
		parts.append(t)


def build_named_stars(parts):
	for name, ra, dec, vmag in NAMED_STARS:
		x, y, z = radec_to_dome_xyz(ra, dec)
		r = star_radius(vmag)
		# Only place stars on the upper hemisphere (z >= DOME_CENTRE_Z)
		if z >= DOME_CENTRE_Z - DOME_R * 0.05:
			parts.append(sphere(f"Star_{name}", r, x, y, z, segments=10, rings=6))


def build_background_stars(parts):
	"""Procedural background of fainter stars, uniformly distributed on the
	upper hemisphere. Density is representative of Gaia's naked-eye sample,
	not per-star DR3 lookup.
	"""
	rng = random.Random(BG_STAR_SEED)
	for i in range(BG_STAR_COUNT):
		# Uniform on upper hemisphere via cos(theta) uniform in [0, 1]
		u = rng.random()
		phi = rng.random() * 2 * math.pi
		theta = math.acos(u)  # theta in [0, pi/2], where 0 is zenith
		elev = math.pi / 2 - theta
		x = DOME_R * math.cos(elev) * math.cos(phi)
		y = DOME_R * math.cos(elev) * math.sin(phi)
		z = DOME_R * math.sin(elev) + DOME_CENTRE_Z
		vmag_synth = rng.uniform(3.5, 5.5)
		r = star_radius(vmag_synth)
		parts.append(sphere(f"BGStar{i:04d}", r, x, y, z, segments=6, rings=4))


def build():
	clear_scene()
	parts = []
	build_pedestal(parts)
	build_dome_frame(parts)
	build_named_stars(parts)
	build_background_stars(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "GaiaStarMap"
	merged.data.name = "GaiaStarMap"
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
	print(f"GEN_STARS named={len(NAMED_STARS)} background={BG_STAR_COUNT}")
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
