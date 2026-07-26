"""Generates the AI Computing and Robotics Laboratory exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/AIControlLaboratory/generate.py \
        -- --out art/exhibits/AIControlLaboratory/build/AIControlLaboratory.glb

Scientific reconstruction, per OMNISCIENCE_COLISEUM_EXHIBIT_ACCURACY.md:
"A truthful, generic inference-server, networking, sensing, and robotics
workflow; no fictional sentient core." Structure is representative rather than
a named site; no specific brand or facility is depicted.

THIS REPLACES A FICTIONAL AI CORE. The prototype it supersedes is a Neon
"Core" cube inside a Glass "GlassLab" box, which is exactly the "fictional
sentient core" pattern the accuracy doc lists as forbidden. Wholesale
replacement.

Elements shown, and why each one is real infrastructure a working lab has:

  Server racks    -- 19-inch equipment racks of 1U/2U rackmount servers. Every
                     data centre and every research lab that runs inference at
                     any scale has these.
  Network switch  -- a top-of-rack switch aggregating the servers' network
                     interfaces. Ports visible.
  Monitor         -- for the human running the workload. A single flat panel on
                     a stand, no fictional interface content.
  Workbench       -- a real workbench, not a "control panel". Where sensors
                     and robotics are mounted for testing.
  Collaborative arm -- a small robotic arm at the size and pose typical of
                       lab cobots (Universal Robots UR3 / Franka / xArm class).
                       Distinct from the Machines-sector "SIX-AXIS AND SCARA
                       ROBOT ARMS" exhibit which shows dedicated industrial
                       arms.
  Camera-sensor rig -- tripod-mounted vision sensor, the input side of the
                       "sensing" part of the workflow.

MATERIALS ARE AN ART CHOICE. Real racks are usually black steel; monitors are
grey/black; robots are grey/orange. This uses brass under D-016. The dossier
says so.
"""

import math
import os
import sys

import bpy

# --- envelope -----------------------------------------------------------------

# Shell 43.20 x 54.00 x 31.50, yaw 80 deg, plinth top Y 8.16, ceiling Y 71.16.
# 63 studs of vertical headroom.
SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00

STUDS_TO_BLENDER = 1.0

# --- layout -------------------------------------------------------------------

# The composition puts server infrastructure on the left half of the shell
# footprint and the human-scale workflow (bench, cobot, monitor, camera) on
# the right. Everything sits on a low base plate on the plinth.

BASE_HEIGHT = 0.6
FLOOR_Z = BASE_HEIGHT  # everything above the base sits here

# Server racks
RACK_COUNT = 2
RACK_W = 7.5
RACK_D = 9.0
RACK_H = 26.0
RACK_UNIT_H = 1.8  # ~1U per rack unit in exhibit scale
RACK_UNITS_PER_RACK = 10  # visible 1U slots per rack

# Network switch above the racks
SWITCH_W = 14.0
SWITCH_H = 1.5
SWITCH_D = 4.5

# Workbench
BENCH_W = 18.0
BENCH_D = 10.0
BENCH_H = 7.5
BENCH_LEG_W = 0.8

# Monitor stand behind the bench
MONITOR_W = 11.0
MONITOR_H = 7.5
MONITOR_D = 0.6

# Collaborative arm on the bench
ARM_BASE_R = 1.1
ARM_LINK_R = 0.5

# Camera-sensor rig
TRIPOD_H = 10.0
CAMERA_W = 1.8
CAMERA_H = 1.4
CAMERA_D = 2.0

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


def build_base_plate(parts):
	parts.append(box("BasePlate", SHELL_WIDTH * 0.94, SHELL_DEPTH * 0.88, BASE_HEIGHT, 0.0, 0.0, BASE_HEIGHT / 2))


def build_server_racks(parts):
	"""Two 19-inch equipment racks side by side, at the back of the exhibit.

	Each rack has a frame and a stack of 1U server chassis with LED strips
	suggesting drive bays and network activity lights. This is what an
	inference-server rack looks like at any scale.
	"""
	# Racks at back of shell, centred pair sits to the left of centre.
	rack_x_centres = []
	total_rack_span = RACK_COUNT * RACK_W + (RACK_COUNT - 1) * 0.3
	rack_left = -SHELL_WIDTH * 0.42 + RACK_W / 2  # left-align on the shell
	for i in range(RACK_COUNT):
		x = rack_left + i * (RACK_W + 0.3)
		rack_x_centres.append(x)
	rack_y = SHELL_DEPTH * 0.32  # push toward the back

	for i, x in enumerate(rack_x_centres):
		# Frame -- four vertical posts and a top and bottom rail
		for dx in (-1.0, 1.0):
			for dy in (-1.0, 1.0):
				parts.append(cyl(f"RackPost", 0.28, RACK_H,
					x + dx * RACK_W / 2 * 0.9,
					rack_y + dy * RACK_D / 2 * 0.9,
					FLOOR_Z + RACK_H / 2))
		parts.append(box("RackTop", RACK_W * 0.92, RACK_D * 0.92, 0.4, x, rack_y, FLOOR_Z + RACK_H))
		parts.append(box("RackBottom", RACK_W * 0.92, RACK_D * 0.92, 0.4, x, rack_y, FLOOR_Z + 0.2))

		# Rack side panels -- solid boxes for the left/right skins
		for dx in (-1.0, 1.0):
			parts.append(box("RackSidePanel", 0.3, RACK_D * 0.85, RACK_H * 0.9,
				x + dx * RACK_W / 2 * 0.92, rack_y, FLOOR_Z + RACK_H / 2))

		# Server units stacked from the bottom up
		for u in range(RACK_UNITS_PER_RACK):
			unit_z = FLOOR_Z + 1.5 + u * (RACK_UNIT_H + 0.15)
			parts.append(box("ServerUnit", RACK_W * 0.82, RACK_D * 0.82, RACK_UNIT_H,
				x, rack_y - 0.2, unit_z))
			# Front bezel bar with LED indicator strip
			parts.append(box("ServerFrontBar", RACK_W * 0.75, 0.25, RACK_UNIT_H * 0.85,
				x, rack_y - RACK_D * 0.42, unit_z))
			# Small LED nub on the bezel -- keeps it from reading as a plain box
			parts.append(cyl("ServerLED", 0.12, 0.28,
				x + RACK_W * 0.3, rack_y - RACK_D * 0.44, unit_z,
				rot=(math.radians(90.0), 0.0, 0.0)))

	# Network switch above the racks, spanning both
	switch_x = (rack_x_centres[0] + rack_x_centres[-1]) / 2
	switch_z = FLOOR_Z + RACK_H + 1.5
	parts.append(box("NetworkSwitch", SWITCH_W, SWITCH_D, SWITCH_H, switch_x, rack_y, switch_z))
	# Port array on the front of the switch -- 8 small holes suggested by small boxes
	for p in range(8):
		port_x = switch_x - SWITCH_W * 0.35 + p * (SWITCH_W * 0.7 / 7)
		parts.append(box("SwitchPort", 0.55, 0.2, 0.55, port_x, rack_y - SWITCH_D * 0.42, switch_z))


def build_workbench(parts):
	"""A simple flat-topped bench, placed to the right of the server racks."""
	bench_x = SHELL_WIDTH * 0.15
	bench_y = -SHELL_DEPTH * 0.05
	# Top slab
	parts.append(box("BenchTop", BENCH_W, BENCH_D, 0.6, bench_x, bench_y, FLOOR_Z + BENCH_H))
	# Four legs
	for dx in (-1.0, 1.0):
		for dy in (-1.0, 1.0):
			parts.append(box("BenchLeg", BENCH_LEG_W, BENCH_LEG_W, BENCH_H,
				bench_x + dx * (BENCH_W / 2 - BENCH_LEG_W),
				bench_y + dy * (BENCH_D / 2 - BENCH_LEG_W),
				FLOOR_Z + BENCH_H / 2))
	return bench_x, bench_y


def build_monitor(parts, bench_x, bench_y):
	"""A flat panel on a stand at the back edge of the bench."""
	monitor_stand_h = 4.0
	stand_x = bench_x
	stand_y = bench_y + BENCH_D * 0.35
	panel_z = FLOOR_Z + BENCH_H + monitor_stand_h + MONITOR_H / 2
	# Vertical stand column
	parts.append(cyl("MonitorStand", 0.35, monitor_stand_h, stand_x, stand_y, FLOOR_Z + BENCH_H + monitor_stand_h / 2))
	# The panel itself -- thin box tilted slightly forward
	parts.append(box("MonitorPanel", MONITOR_W, MONITOR_D, MONITOR_H,
		stand_x, stand_y, panel_z,
		rot=(math.radians(-8.0), 0.0, 0.0)))
	# Bezel frame around the panel for readability
	parts.append(box("MonitorBezel", MONITOR_W + 0.4, MONITOR_D + 0.1, MONITOR_H + 0.4,
		stand_x, stand_y - 0.02, panel_z,
		rot=(math.radians(-8.0), 0.0, 0.0)))


def build_cobot(parts, bench_x, bench_y):
	"""A small collaborative arm on the bench.

	Six-link chain, small enough to fit on the bench. Distinct from the
	dedicated Machines-sector arm exhibit: this reads as an incidental cobot
	in a lab workflow, not the featured object.
	"""
	origin_x = bench_x + BENCH_W * 0.25
	origin_y = bench_y - BENCH_D * 0.1
	base_z = FLOOR_Z + BENCH_H + 0.3

	# Cylindrical base
	parts.append(cyl("CobotBase", ARM_BASE_R, 0.8, origin_x, origin_y, base_z + 0.4))
	# Link 1 -- shoulder rotation, vertical
	link1_h = 3.5
	parts.append(cyl("CobotLink1", ARM_LINK_R * 1.1, link1_h, origin_x, origin_y, base_z + 0.8 + link1_h / 2))
	# Link 2 -- upper arm, tilted forward
	link2_h = 4.5
	link2_pitch = math.radians(-30.0)
	link2_top_z = base_z + 0.8 + link1_h
	link2_dx = math.sin(-link2_pitch) * link2_h / 2
	link2_dz = math.cos(-link2_pitch) * link2_h / 2
	parts.append(cyl("CobotLink2", ARM_LINK_R, link2_h,
		origin_x + link2_dx, origin_y, link2_top_z + link2_dz,
		rot=(0.0, link2_pitch, 0.0)))
	# Elbow joint
	elbow_x = origin_x + 2 * link2_dx
	elbow_z = link2_top_z + 2 * link2_dz
	parts.append(cyl("CobotElbow", ARM_LINK_R * 1.15, 0.6, elbow_x, origin_y, elbow_z,
		rot=(math.radians(90.0), 0.0, 0.0)))
	# Link 3 -- forearm, angled down and forward
	link3_h = 3.5
	link3_pitch = math.radians(-70.0)
	link3_dx = math.sin(-link3_pitch) * link3_h / 2
	link3_dz = math.cos(-link3_pitch) * link3_h / 2
	parts.append(cyl("CobotLink3", ARM_LINK_R * 0.9, link3_h,
		elbow_x + link3_dx, origin_y, elbow_z + link3_dz,
		rot=(0.0, link3_pitch, 0.0)))
	# End effector (a simple gripper block)
	ee_x = elbow_x + 2 * link3_dx
	ee_z = elbow_z + 2 * link3_dz
	parts.append(box("CobotEndEffector", 0.8, 0.8, 1.2, ee_x, origin_y, ee_z))
	# Two-finger gripper
	for dy in (-1.0, 1.0):
		parts.append(box("CobotFinger", 0.2, 0.25, 0.9, ee_x, origin_y + dy * 0.35, ee_z - 0.9))


def build_camera_rig(parts, bench_x, bench_y):
	"""Tripod-mounted camera on the free end of the bench.

	Represents the sensing input of the workflow. Reads as a stationary
	vision sensor rather than a security camera because of the tripod.
	"""
	tripod_x = bench_x + BENCH_W * 0.42
	tripod_y = bench_y + BENCH_D * 0.1
	# Three tripod legs splayed outward
	for a_deg in (0.0, 120.0, 240.0):
		a = math.radians(a_deg)
		lx = tripod_x + math.cos(a) * 1.5
		ly = tripod_y + math.sin(a) * 1.5
		parts.append(cyl("TripodLeg", 0.14, math.sqrt(TRIPOD_H * TRIPOD_H + 2.25) + 0.5,
			(tripod_x + lx) / 2, (tripod_y + ly) / 2, FLOOR_Z + BENCH_H + TRIPOD_H / 2,
			rot=(0.0, 0.0, 0.0)))
	# Central column
	parts.append(cyl("TripodColumn", 0.2, TRIPOD_H, tripod_x, tripod_y, FLOOR_Z + BENCH_H + TRIPOD_H / 2))
	# Camera body
	cam_z = FLOOR_Z + BENCH_H + TRIPOD_H + CAMERA_H / 2
	parts.append(box("CameraBody", CAMERA_W, CAMERA_D, CAMERA_H, tripod_x, tripod_y, cam_z))
	# Lens barrel pointing forward
	parts.append(cyl("CameraLens", 0.5, 1.0, tripod_x, tripod_y - CAMERA_D * 0.6, cam_z,
		rot=(math.radians(90.0), 0.0, 0.0)))


def build():
	clear_scene()
	parts = []
	build_base_plate(parts)
	build_server_racks(parts)
	bench_x, bench_y = build_workbench(parts)
	build_monitor(parts, bench_x, bench_y)
	build_cobot(parts, bench_x, bench_y)
	build_camera_rig(parts, bench_x, bench_y)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "AILaboratory"
	merged.data.name = "AILaboratory"
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

	if tris > 20000:
		raise SystemExit(f"FAIL: {tris} triangles exceeds the 20000 per-mesh cap")
	if d.z > ENVELOPE_HEIGHT:
		raise SystemExit(f"FAIL: height {d.z:.2f} exceeds the {ENVELOPE_HEIGHT:.2f} stud envelope")
	if d.x > SHELL_WIDTH:
		raise SystemExit(f"FAIL: width {d.x:.2f} overhangs the {SHELL_WIDTH:.2f} stud collision shell")
	if d.y > SHELL_DEPTH:
		raise SystemExit(f"FAIL: depth {d.y:.2f} overhangs the {SHELL_DEPTH:.2f} stud collision shell")

	print(f"GEN_SHELL_MARGIN {SHELL_WIDTH - d.x:.2f} x {SHELL_DEPTH - d.y:.2f} studs")
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
