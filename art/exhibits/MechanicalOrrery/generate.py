"""Generates the Rowley Orrery (1712-1713) exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/MechanicalOrrery/generate.py \
        -- --out art/exhibits/MechanicalOrrery/build/MechanicalOrrery.glb

Structure follows John Rowley's orrery for Charles Boyle, 4th Earl of Orrery
(1712-1713) — the instrument that gave the class its name. Science Museum
Group object 1952-73.

Rowley's design is a **grand orrery** on a tall pedestal: central Sun on a
brass column, with Mercury, Venus, Earth (with its own Moon), and Mars on
concentric arms driven by clockwork. Outer planets (Jupiter, Saturn) were not
included in the 1712 design -- Uranus wasn't discovered until 1781.

MATERIALS ARE AN ART CHOICE. Real orrery is brass and mahogany; this uses
brass throughout under D-016. Dossier says so.
"""

import math
import os
import sys

import bpy

# --- what the sources establish ----------------------------------------------

# Rowley 1712 planet set (Ptolemaic-order for a heliocentric grand orrery of
# the period). Uranus/Neptune postdate the instrument.
PLANETS = [
	{"name": "Mercury", "orbit_r": 3.0,  "size": 0.6},
	{"name": "Venus",   "orbit_r": 4.8,  "size": 0.9},
	{"name": "Earth",   "orbit_r": 7.0,  "size": 1.0, "has_moon": True},
	{"name": "Mars",    "orbit_r": 9.6,  "size": 0.8},
]

# --- envelope ----------------------------------------------------------------

SHELL_WIDTH = 47.9    # this exhibit's shell is wider
SHELL_DEPTH = 36.0
ENVELOPE_HEIGHT = 63.0

STUDS_TO_BLENDER = 1.0

# --- layout ------------------------------------------------------------------

PEDESTAL_H = 24.0
PEDESTAL_R_TOP = 4.0
PEDESTAL_R_BASE = 6.5
DECK_R = 12.5       # brass deck holding orbital rings, larger than outer orbit
DECK_H = 0.6
SUN_R = 1.6

ORBIT_RING_THICK = 0.12
ORBIT_ARM_THICK = 0.25

SEGMENTS = 24


def clear_scene():
	bpy.ops.object.select_all(action="SELECT")
	bpy.ops.object.delete(use_global=False)
	for block in (bpy.data.meshes, bpy.data.materials, bpy.data.objects):
		for item in list(block):
			if item.users == 0:
				block.remove(item)


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


def torus(name, major, minor, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=48, minor_segments=6, location=(x, y, z), rotation=rot)
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


def build_pedestal(parts):
	# Cone-frustum column via two cylinders stacked
	parts.append(cyl("PedestalBase", PEDESTAL_R_BASE, 2.0, 0.0, 0.0, 1.0))
	parts.append(cyl("PedestalColumn", PEDESTAL_R_TOP, PEDESTAL_H - 4.0, 0.0, 0.0, 2.0 + (PEDESTAL_H - 4.0) / 2))
	parts.append(cyl("PedestalCap", PEDESTAL_R_TOP * 1.4, 1.2, 0.0, 0.0, PEDESTAL_H - 2.0 + 0.6))
	# Decorative rings at top and bottom
	parts.append(torus("PedestalBaseRing", PEDESTAL_R_BASE - 0.1, 0.3, 0.0, 0.0, 2.0))
	parts.append(torus("PedestalTopRing", PEDESTAL_R_TOP * 1.3, 0.3, 0.0, 0.0, PEDESTAL_H - 2.0))


def build_deck(parts):
	deck_z = PEDESTAL_H + DECK_H / 2
	parts.append(cyl("Deck", DECK_R, DECK_H, 0.0, 0.0, deck_z))
	# Deck rim
	parts.append(torus("DeckRim", DECK_R, 0.3, 0.0, 0.0, deck_z))


def build_sun(parts):
	sun_z = PEDESTAL_H + DECK_H + SUN_R + 1.5  # small brass column raising the Sun
	parts.append(cyl("SunPost", 0.4, 1.5, 0.0, 0.0, PEDESTAL_H + DECK_H + 0.75))
	parts.append(sphere("Sun", SUN_R, 0.0, 0.0, sun_z, segments=24, rings=16))


def build_planets(parts):
	sun_z = PEDESTAL_H + DECK_H + SUN_R + 1.5
	for p in PLANETS:
		# Orbital ring
		parts.append(torus(f"Orbit_{p['name']}", p["orbit_r"], ORBIT_RING_THICK,
			0.0, 0.0, PEDESTAL_H + DECK_H + 0.3))
		# Arm carrying the planet — a horizontal rod from centre to planet, rotated
		# to a plausible pose (each at a different angle).
		# We pick fixed angles so the arms don't overlap in the view.
		angle_deg = {"Mercury": 30.0, "Venus": 120.0, "Earth": 200.0, "Mars": 290.0}[p["name"]]
		a = math.radians(angle_deg)
		arm_len = p["orbit_r"]
		# Arm rod from origin to planet
		parts.append(box(f"Arm_{p['name']}", arm_len, ORBIT_ARM_THICK, ORBIT_ARM_THICK,
			math.cos(a) * arm_len / 2, math.sin(a) * arm_len / 2,
			PEDESTAL_H + DECK_H + 0.9,
			rot=(0.0, 0.0, a)))
		# Vertical post from arm to planet ball
		planet_x = math.cos(a) * p["orbit_r"]
		planet_y = math.sin(a) * p["orbit_r"]
		post_h = 2.5
		parts.append(cyl(f"Post_{p['name']}", 0.15, post_h,
			planet_x, planet_y, PEDESTAL_H + DECK_H + 0.9 + post_h / 2))
		# Planet ball
		parts.append(sphere(f"Planet_{p['name']}", p["size"], planet_x, planet_y,
			PEDESTAL_H + DECK_H + 0.9 + post_h + p["size"]))
		# Earth's Moon
		if p.get("has_moon"):
			moon_r = 0.35
			moon_offset = 1.3
			moon_a = math.radians(40)
			parts.append(sphere(f"Moon", moon_r,
				planet_x + math.cos(a + moon_a) * moon_offset,
				planet_y + math.sin(a + moon_a) * moon_offset,
				PEDESTAL_H + DECK_H + 0.9 + post_h + p["size"]))


def build():
	clear_scene()
	parts = []
	build_pedestal(parts)
	build_deck(parts)
	build_sun(parts)
	build_planets(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "RowleyOrrery"
	merged.data.name = "RowleyOrrery"
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
		raise SystemExit(f"FAIL: {tris} triangles exceeds the 20000 cap")
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
