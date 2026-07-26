"""Generates the Prague Astronomical Clock (1865-1866 era) exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/AstronomicalClockTower/generate.py \
        -- --out art/exhibits/AstronomicalClockTower/build/AstronomicalClockTower.glb

Named replica of the Prague Orloj -- the astronomical clock on the south face
of Prague's Old Town Hall tower -- as it appeared after the 1865-1866
restoration. That restoration is the "iconic" postcard look:

  - Astronomical dial (upper) with golden Sun/Moon indicator, Schwabacher
    Czech-time numerals on the outer ring, and gilded zodiac
  - Josef Mánes calendar plaque (1865) below the astronomical dial with
    12 zodiac medallions and the Prague coat of arms
  - Twelve apostles procession windows (two circular openings above the
    astronomical dial, from which the apostles rotate)
  - Four side statues at astronomical-dial height: Death (skeleton),
    Vanity, Miser, Turk -- moralised figures added/restored in 1865
  - Four side statues at calendar-plaque height: Chronicler, Angel,
    Astronomer, Philosopher -- 1865 additions

Real dimensions: each dial ~2.6 m diameter; overall face ~6 m tall.

MATERIALS ARE AN ART CHOICE. Real Orloj is stone tower with painted metal
dials and gilded ornaments; this uses brass throughout under D-016. The
gilded parts of the real clock map to brass naturally, so this exhibit's
material gap is smaller than most.
"""

import math
import os
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0
SEGMENTS = 32

# --- what the sources fix ---------------------------------------------------

# Prague Orloj dimensions (approximate, per public tourism records):
#   astronomical dial diameter ~2.6 m
#   calendar plaque diameter   ~2.6 m
#   overall clock face height  ~6 m (with apostles windows + both dials)
REAL_DIAL_D_M = 2.6

# --- scale and layout -------------------------------------------------------

# Scale to fill the vertical envelope while fitting inside the shell.
# Panel content ~45 studs tall to leave headroom.
DIAL_D = 13.0                       # each dial diameter
DIAL_R = DIAL_D / 2
STUDS_PER_M = DIAL_D / REAL_DIAL_D_M  # ~5 studs per real metre

PANEL_W = 30.0
PANEL_H = 45.0
PANEL_D = 2.0

# Height layout (bottom to top):
BASE_Z = 0.4
CALENDAR_CENTRE_Z = BASE_Z + 2.0 + DIAL_R      # ~9
ASTRO_CENTRE_Z = CALENDAR_CENTRE_Z + DIAL_D + 2.0  # ~24
APOSTLES_ROW_Z = ASTRO_CENTRE_Z + DIAL_R + 3.0     # ~33
PANEL_TOP_Z = APOSTLES_ROW_Z + 3.0                 # ~36

STATUE_H = 3.8
STATUE_R = 0.6


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


def torus(name, major, minor, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0), major_seg=48, minor_seg=6):
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=major_seg, minor_segments=minor_seg, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def build_panel_background(parts):
	"""Tall stone-tower-style panel that carries every clock feature."""
	parts.append(box("Panel", PANEL_W, PANEL_D, PANEL_H, 0.0, 0.0, BASE_Z + PANEL_H / 2))
	# Decorative frame ridges around the outer edge
	for sx in (-1.0, 1.0):
		parts.append(box("PanelFrameSide", 0.6, PANEL_D + 0.4, PANEL_H, sx * (PANEL_W / 2 - 0.3), 0.0, BASE_Z + PANEL_H / 2))
	parts.append(box("PanelFrameTop", PANEL_W, PANEL_D + 0.4, 0.6, 0.0, 0.0, BASE_Z + PANEL_H - 0.3))
	parts.append(box("PanelFrameBottom", PANEL_W, PANEL_D + 0.4, 0.6, 0.0, 0.0, BASE_Z + 0.3))


def build_astronomical_dial(parts):
	"""Upper dial: astronomical time, with outer ring + zodiac + hands."""
	# Dial face -- flat disk mounted on the panel front
	dial_y = -PANEL_D * 0.6
	parts.append(cyl("AstroDialFace", DIAL_R, 0.4, 0.0, dial_y, ASTRO_CENTRE_Z, rot=(math.radians(90.0), 0.0, 0.0)))
	# Outer ring (Schwabacher old-Czech-time numerals) -- represented as a raised torus rim
	parts.append(torus("AstroOuterRing", DIAL_R, 0.35, 0.0, dial_y - 0.2, ASTRO_CENTRE_Z))
	# Middle ring (24-hour zodiac ring) -- inset torus
	parts.append(torus("AstroZodiacRing", DIAL_R * 0.75, 0.28, 0.0, dial_y - 0.3, ASTRO_CENTRE_Z))
	# Inner disk (background)
	parts.append(cyl("AstroInnerDisk", DIAL_R * 0.55, 0.2, 0.0, dial_y - 0.35, ASTRO_CENTRE_Z, rot=(math.radians(90.0), 0.0, 0.0)))
	# Sun hand -- long thin bar from centre outward, at a plausible angle
	sun_angle = math.radians(35.0)
	hand_len = DIAL_R * 0.85
	sx_end = math.cos(sun_angle) * hand_len
	sz_end = math.sin(sun_angle) * hand_len
	parts.append(box("AstroSunHand", hand_len, 0.35, 0.35,
		sx_end / 2, dial_y - 0.55, ASTRO_CENTRE_Z + sz_end / 2,
		rot=(0.0, -sun_angle, 0.0)))
	# Sun ball at the end of the sun hand
	parts.append(cyl("AstroSun", 0.6, 0.4, sx_end, dial_y - 0.65, ASTRO_CENTRE_Z + sz_end, rot=(math.radians(90.0), 0.0, 0.0)))
	# Moon hand -- shorter, at a different angle
	moon_angle = math.radians(155.0)
	moon_len = DIAL_R * 0.75
	mx_end = math.cos(moon_angle) * moon_len
	mz_end = math.sin(moon_angle) * moon_len
	parts.append(box("AstroMoonHand", moon_len, 0.3, 0.3,
		mx_end / 2, dial_y - 0.55, ASTRO_CENTRE_Z + mz_end / 2,
		rot=(0.0, -moon_angle, 0.0)))
	# Moon sphere at end
	parts.append(cyl("AstroMoon", 0.5, 0.35, mx_end, dial_y - 0.65, ASTRO_CENTRE_Z + mz_end, rot=(math.radians(90.0), 0.0, 0.0)))
	# Central hub
	parts.append(cyl("AstroHub", 0.7, 0.6, 0.0, dial_y - 0.7, ASTRO_CENTRE_Z, rot=(math.radians(90.0), 0.0, 0.0)))


def build_calendar_dial(parts):
	"""Lower dial: Josef Mánes 1865 calendar plaque with zodiac medallions."""
	dial_y = -PANEL_D * 0.6
	parts.append(cyl("CalendarFace", DIAL_R, 0.4, 0.0, dial_y, CALENDAR_CENTRE_Z, rot=(math.radians(90.0), 0.0, 0.0)))
	parts.append(torus("CalendarOuterRing", DIAL_R, 0.35, 0.0, dial_y - 0.2, CALENDAR_CENTRE_Z))
	# Twelve zodiac medallions around the rim
	for i in range(12):
		a = math.radians(90 - i * 30)  # start at top, go clockwise
		cx = math.cos(a) * DIAL_R * 0.78
		cz = math.sin(a) * DIAL_R * 0.78 + CALENDAR_CENTRE_Z
		parts.append(cyl(f"ZodiacMedallion{i:02d}", 0.55, 0.3,
			cx, dial_y - 0.35, cz, rot=(math.radians(90.0), 0.0, 0.0)))
	# Central Prague coat of arms area -- rectangular boss
	parts.append(box("CoatOfArms", 2.0, 0.4, 2.4, 0.0, dial_y - 0.45, CALENDAR_CENTRE_Z))


def build_apostles_windows(parts):
	"""Two circular openings above the astronomical dial where the twelve
	apostles rotated through. Rendered as raised bezel rings on the panel.
	"""
	dial_y = -PANEL_D * 0.6
	window_r = 1.6
	for sx in (-1.0, 1.0):
		x = sx * 3.5
		# Ring bezel
		parts.append(torus(f"ApostleWindow_{sx > 0 and 'R' or 'L'}", window_r, 0.35, x, dial_y - 0.15, APOSTLES_ROW_Z))
		# Recessed dark cylinder (visible apostle behind the window)
		parts.append(cyl(f"ApostleWindowRecess_{sx > 0 and 'R' or 'L'}", window_r * 0.85, 0.5,
			x, dial_y + 0.1, APOSTLES_ROW_Z, rot=(math.radians(90.0), 0.0, 0.0)))
	# Rooster above the windows -- Orloj's crowing golden cockerel
	parts.append(cyl("Rooster", 0.5, 0.7, 0.0, dial_y - 0.4, APOSTLES_ROW_Z + 2.2, rot=(math.radians(90.0), 0.0, 0.0)))
	parts.append(box("RoosterTail", 0.6, 0.3, 1.0, 0.35, dial_y - 0.4, APOSTLES_ROW_Z + 2.5, rot=(0.0, math.radians(-35.0), 0.0)))


def _statue(name, x, z, statue_type):
	"""Small statue silhouette in a niche. statue_type distinguishes the four
	astronomical-dial figures; each gets a basic identifying prop."""
	dial_y = -PANEL_D * 0.6 - 0.8  # protrudes further from panel
	parts_local = []
	# Body -- upright cylinder
	body = cyl(f"{name}_Body", STATUE_R, STATUE_H * 0.7, x, dial_y, z + STATUE_H * 0.35)
	parts_local.append(body)
	# Head -- small sphere
	bpy.ops.mesh.primitive_uv_sphere_add(radius=STATUE_R * 0.75, segments=14, ring_count=10, location=(x, dial_y, z + STATUE_H * 0.85))
	head = bpy.context.active_object
	head.name = f"{name}_Head"
	parts_local.append(head)
	# Identifying prop (small object beside the statue)
	if statue_type == "death":
		# Hourglass -- two stacked cones would be complex; use a box
		parts_local.append(box(f"{name}_Hourglass", 0.35, 0.35, 0.9, x + STATUE_R + 0.3, dial_y, z + STATUE_H * 0.5))
	elif statue_type == "vanity":
		# Mirror -- flat disk on a stem
		parts_local.append(cyl(f"{name}_Mirror", 0.5, 0.1, x + STATUE_R + 0.5, dial_y, z + STATUE_H * 0.7, rot=(0.0, math.radians(90.0), 0.0)))
	elif statue_type == "miser":
		# Money bag -- small sphere at side
		bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45, segments=10, ring_count=8, location=(x + STATUE_R + 0.4, dial_y, z + STATUE_H * 0.4))
		bag = bpy.context.active_object
		bag.name = f"{name}_MoneyBag"
		parts_local.append(bag)
	elif statue_type == "turk":
		# Turban -- flatter head with wider ring
		parts_local.append(cyl(f"{name}_Turban", STATUE_R * 0.9, 0.4, x, dial_y, z + STATUE_H * 0.98))
	else:
		# Generic scroll for the calendar-side statues
		parts_local.append(box(f"{name}_Scroll", 0.3, 0.3, 0.8, x + STATUE_R + 0.3, dial_y, z + STATUE_H * 0.55))
	# Small plinth under each statue
	parts_local.append(box(f"{name}_Plinth", 1.4, 1.0, 0.6, x, dial_y, z + 0.3))
	return parts_local


def build_side_statues(parts):
	"""Four astronomical-dial statues + four calendar-plaque statues.

	Left side of astro dial: Death (skeleton with hourglass), Turk (turban)
	Right side of astro dial: Vanity (mirror), Miser (money bag)
	Below each (calendar row): four 1865-added figures (generic silhouettes)
	"""
	astro_stat_x = DIAL_R + 2.5  # outside the dial
	# Astronomical dial statues
	parts.extend(_statue("Death", -astro_stat_x, ASTRO_CENTRE_Z + 1.5, "death"))
	parts.extend(_statue("Turk", -astro_stat_x, ASTRO_CENTRE_Z - 3.0, "turk"))
	parts.extend(_statue("Vanity", astro_stat_x, ASTRO_CENTRE_Z + 1.5, "vanity"))
	parts.extend(_statue("Miser", astro_stat_x, ASTRO_CENTRE_Z - 3.0, "miser"))
	# Calendar dial statues (1865 additions -- Chronicler, Angel, Astronomer, Philosopher)
	cal_stat_x = DIAL_R + 2.5
	parts.extend(_statue("Chronicler", -cal_stat_x, CALENDAR_CENTRE_Z + 1.5, "scroll"))
	parts.extend(_statue("Angel", -cal_stat_x, CALENDAR_CENTRE_Z - 3.0, "scroll"))
	parts.extend(_statue("Astronomer", cal_stat_x, CALENDAR_CENTRE_Z + 1.5, "scroll"))
	parts.extend(_statue("Philosopher", cal_stat_x, CALENDAR_CENTRE_Z - 3.0, "scroll"))


def build():
	clear_scene()
	parts = []
	build_panel_background(parts)
	build_calendar_dial(parts)
	build_astronomical_dial(parts)
	build_apostles_windows(parts)
	build_side_statues(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "PragueAstronomicalClock"
	merged.data.name = "PragueAstronomicalClock"
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
	print(f"GEN_SCALE {STUDS_PER_M:.2f} studs/m; real 2.6 m dial -> {DIAL_D:.1f} studs")
	if tris > 20000:
		raise SystemExit(f"FAIL: {tris} tri exceeds 20000")
	if d.z > ENVELOPE_HEIGHT:
		raise SystemExit(f"FAIL: height {d.z:.2f} exceeds envelope")
	if d.x > SHELL_WIDTH:
		raise SystemExit(f"FAIL: width {d.x:.2f} overhangs shell {SHELL_WIDTH:.2f}")
	if d.y > SHELL_DEPTH:
		raise SystemExit(f"FAIL: depth {d.y:.2f} overhangs shell {SHELL_DEPTH:.2f}")
	# Both dials same diameter is a real-object relationship worth locking in
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
