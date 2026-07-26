"""Generates the Six-Axis and SCARA Robot Arms exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/RoboticArms/generate.py \
        -- --out art/exhibits/RoboticArms/build/RoboticArms.glb

Scientific reconstruction, per the accuracy doc: "Two real industrial
kinematic arrangements with generic, non-branded housings and mechanically
possible joints."

Two distinct industrial arm classes side by side:

  Six-axis articulated arm: 6 rotational joints (base yaw, shoulder pitch,
                             elbow pitch, wrist roll/pitch/yaw). Human-arm-
                             like reach. Class of KUKA, ABB, Fanuc, Franka.

  SCARA (Selective Compliance Assembly Robot Arm): a vertical Z-axis
        column carrying two horizontal rotational shoulders and a wrist,
        typical of Epson/Yamaha assembly arms. Fast planar reach with a
        vertical picker.

MATERIALS ARE AN ART CHOICE. Real arms are painted steel and aluminium in
orange, white, or grey; brass throughout under D-016. Housings are generic
to avoid depicting any specific manufacturer.
"""

import math
import os
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0
SEGMENTS = 18


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


def build_base_plate(parts):
	parts.append(box("BasePlate", 38.0, 20.0, 1.0, 0.0, 0.0, 0.5))


def build_six_axis_arm(parts, cx, cy):
	"""Articulated 6-DOF arm at (cx, cy) on the base plate.

	Silhouette: base cylinder + shoulder rotator + upper arm link (angled) +
	elbow + forearm link (angled) + wrist joints + end effector.
	"""
	base_z = 1.0
	# Base pedestal
	parts.append(cyl("SA_Base", 1.8, 3.0, cx, cy, base_z + 1.5))
	# Shoulder yoke
	parts.append(cyl("SA_ShoulderYoke", 1.3, 2.0, cx, cy, base_z + 3.5, rot=(math.radians(90.0), 0.0, 0.0)))
	# Upper arm link -- angled forward and up
	link1_pitch = math.radians(60.0)
	link1_len = 7.0
	link1_z_end = base_z + 3.5 + math.sin(link1_pitch) * link1_len
	link1_x_end = cx  # in-plane arm
	link1_y_end = cy + math.cos(link1_pitch) * link1_len
	parts.append(cyl("SA_UpperArm", 0.6, link1_len,
		cx, (cy + link1_y_end) / 2, (base_z + 3.5 + link1_z_end) / 2,
		rot=(math.pi/2 - link1_pitch, 0.0, 0.0)))
	# Elbow joint
	parts.append(cyl("SA_Elbow", 0.85, 1.6, link1_x_end, link1_y_end, link1_z_end,
		rot=(math.radians(90.0), 0.0, 0.0)))
	# Forearm link -- angled forward/down
	link2_pitch = math.radians(30.0)
	link2_len = 6.0
	link2_z_end = link1_z_end + math.sin(link2_pitch) * link2_len
	link2_y_end = link1_y_end + math.cos(link2_pitch) * link2_len
	parts.append(cyl("SA_Forearm", 0.5, link2_len,
		link1_x_end, (link1_y_end + link2_y_end) / 2, (link1_z_end + link2_z_end) / 2,
		rot=(math.pi/2 - link2_pitch, 0.0, 0.0)))
	# Wrist assembly -- three small cylinders for the three wrist joints
	wx, wy, wz = link1_x_end, link2_y_end, link2_z_end
	parts.append(cyl("SA_Wrist1", 0.5, 1.0, wx, wy, wz, rot=(math.radians(90.0), 0.0, 0.0)))
	parts.append(cyl("SA_Wrist2", 0.4, 0.8, wx, wy + 0.8, wz))
	# End effector -- small gripper block
	parts.append(box("SA_EndEffector", 0.8, 0.8, 1.0, wx, wy + 0.8, wz - 0.8))


def build_scara(parts, cx, cy):
	"""SCARA arm: tall vertical column with two horizontal shoulder joints
	and a downward-facing wrist/picker.
	"""
	base_z = 1.0
	column_h = 14.0
	# Base + column
	parts.append(cyl("SCARA_Base", 2.0, 1.6, cx, cy, base_z + 0.8))
	parts.append(cyl("SCARA_Column", 1.0, column_h, cx, cy, base_z + 1.6 + column_h / 2))
	column_top_z = base_z + 1.6 + column_h
	# First shoulder link -- horizontal from column
	link1_len = 5.5
	link1_yaw = math.radians(30.0)
	l1_x_end = cx + math.cos(link1_yaw) * link1_len
	l1_y_end = cy + math.sin(link1_yaw) * link1_len
	parts.append(box("SCARA_Link1", link1_len, 1.2, 0.9,
		(cx + l1_x_end) / 2, (cy + l1_y_end) / 2, column_top_z - 0.4,
		rot=(0.0, 0.0, link1_yaw)))
	# Second shoulder link -- horizontal, from end of link1
	link2_len = 4.5
	link2_yaw = link1_yaw + math.radians(-40.0)
	l2_x_end = l1_x_end + math.cos(link2_yaw) * link2_len
	l2_y_end = l1_y_end + math.sin(link2_yaw) * link2_len
	parts.append(box("SCARA_Link2", link2_len, 0.9, 0.7,
		(l1_x_end + l2_x_end) / 2, (l1_y_end + l2_y_end) / 2, column_top_z - 0.8,
		rot=(0.0, 0.0, link2_yaw)))
	# Vertical picker (Z-axis prismatic) hanging down from end of link 2
	picker_h = 4.5
	parts.append(cyl("SCARA_ZAxis", 0.4, picker_h, l2_x_end, l2_y_end, column_top_z - 0.8 - picker_h / 2))
	# End effector at bottom of picker
	parts.append(cyl("SCARA_EndEffector", 0.7, 0.5, l2_x_end, l2_y_end, column_top_z - 0.8 - picker_h))


def build():
	clear_scene()
	parts = []
	build_base_plate(parts)
	# Six-axis on the left, SCARA on the right
	build_six_axis_arm(parts, cx=-9.0, cy=-2.0)
	build_scara(parts, cx=10.0, cy=-2.0)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "RobotArms"
	merged.data.name = "RobotArms"
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
