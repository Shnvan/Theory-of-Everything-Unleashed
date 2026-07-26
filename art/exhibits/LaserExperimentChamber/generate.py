"""Generates the Michelson Laser Interferometer exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/LaserExperimentChamber/generate.py \
        -- --out art/exhibits/LaserExperimentChamber/build/LaserExperimentChamber.glb

Scientific reconstruction, per the accuracy doc: "A physically coherent
optical path informed by LIGO and laboratory Michelson-interferometer
documentation."

Structure: an optical bench with the four canonical Michelson elements plus
a detector, arranged as a classic Michelson interferometer:

    laser --> beam splitter --> mirror A (arm 1 end)
                             \--> mirror B (arm 2 end)
             recombine at beam splitter --> detector

MATERIALS ARE AN ART CHOICE. Brass throughout under D-016; beam paths in
Neon (per the black-hole exhibit precedent for light).
"""

import math
import os
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0

# --- optical layout ---------------------------------------------------------

TABLE_W = 36.0
TABLE_D = 24.0
TABLE_H = 12.0
TABLE_TOP_Z = TABLE_H

ARM_LENGTH = 11.0          # from beam splitter to each end mirror
BEAM_HEIGHT = TABLE_TOP_Z + 2.0

BEAM_SPLITTER_SIZE = 2.0
END_MIRROR_W = 3.0
END_MIRROR_H = 3.5
END_MIRROR_D = 0.6

LASER_LEN = 5.0
LASER_R = 0.9

DETECTOR_W = 2.5
DETECTOR_H = 2.5
DETECTOR_D = 2.0

BEAM_R = 0.15

# Layout: put the beam splitter at origin (in bench coords). Laser to the
# -X arm; mirror A to the -X end of arm 1; mirror B to the +Y end of arm 2;
# detector to the -Y end (unused arm receives recombined output).

SEGMENTS = 16


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


def build_optical_bench(parts):
	parts.append(box("BenchTop", TABLE_W, TABLE_D, 0.8, 0.0, 0.0, TABLE_H))
	# Four legs
	for sx in (-1.0, 1.0):
		for sy in (-1.0, 1.0):
			parts.append(box("BenchLeg", 0.7, 0.7, TABLE_H,
				sx * (TABLE_W / 2 - 1.0), sy * (TABLE_D / 2 - 1.0), TABLE_H / 2))


def build_laser(parts):
	# Laser body along X axis, pointing +X toward the beam splitter
	laser_x = -ARM_LENGTH - LASER_LEN / 2 - 0.5
	parts.append(cyl("LaserBody", LASER_R, LASER_LEN, laser_x, 0.0, BEAM_HEIGHT,
		rot=(0.0, math.radians(90.0), 0.0)))
	# Laser aperture flare on the emitting end
	parts.append(cyl("LaserAperture", LASER_R * 1.15, 0.4,
		laser_x + LASER_LEN / 2, 0.0, BEAM_HEIGHT, rot=(0.0, math.radians(90.0), 0.0)))
	# Mount block under the laser
	parts.append(box("LaserMount", LASER_LEN * 0.7, 1.8, BEAM_HEIGHT - TABLE_TOP_Z,
		laser_x, 0.0, TABLE_TOP_Z + (BEAM_HEIGHT - TABLE_TOP_Z) / 2))


def build_beam_splitter(parts):
	"""Cube at 45 degrees at the intersection of the two arms."""
	parts.append(box("BeamSplitter", BEAM_SPLITTER_SIZE, BEAM_SPLITTER_SIZE, BEAM_SPLITTER_SIZE,
		0.0, 0.0, BEAM_HEIGHT, rot=(0.0, 0.0, math.radians(45.0))))
	# Mount post
	parts.append(cyl("BeamSplitterPost", 0.4, BEAM_HEIGHT - TABLE_TOP_Z, 0.0, 0.0,
		TABLE_TOP_Z + (BEAM_HEIGHT - TABLE_TOP_Z) / 2))


def build_end_mirror(parts, cx, cy, facing_x):
	"""End mirror at the given position. facing_x is +1 (mirror faces -X) or
	-1 (mirror faces +X), or same for Y via rot.
	"""
	# Mirror plate
	if abs(facing_x) > 0.0:
		# Mirror facing along X: plate normal is +X or -X
		rot = (0.0, 0.0, 0.0)
	else:
		rot = (0.0, 0.0, math.radians(90.0))
	parts.append(box("EndMirror", END_MIRROR_D, END_MIRROR_W, END_MIRROR_H, cx, cy, BEAM_HEIGHT, rot=rot))
	# Mount block
	parts.append(box("MirrorMount", 1.4, 1.4, BEAM_HEIGHT - TABLE_TOP_Z - 0.5,
		cx, cy, TABLE_TOP_Z + (BEAM_HEIGHT - TABLE_TOP_Z - 0.5) / 2))


def build_detector(parts):
	"""Detector at the -Y end where the recombined beam exits."""
	cx = 0.0
	cy = -ARM_LENGTH
	parts.append(box("Detector", DETECTOR_W, DETECTOR_D, DETECTOR_H,
		cx, cy, BEAM_HEIGHT))
	parts.append(box("DetectorMount", 1.8, 1.8, BEAM_HEIGHT - TABLE_TOP_Z,
		cx, cy, TABLE_TOP_Z + (BEAM_HEIGHT - TABLE_TOP_Z) / 2))


def build_beam_paths(parts):
	"""Thin cylinder segments showing beam paths. Will be materialised as Neon
	in Studio placement — for now they read as bright brass paths.
	"""
	# Beam 1: laser -> beam splitter
	laser_end_x = -ARM_LENGTH - 0.5
	parts.append(cyl("BeamPath_LaserToBS", BEAM_R, abs(laser_end_x),
		laser_end_x / 2, 0.0, BEAM_HEIGHT, rot=(0.0, math.radians(90.0), 0.0)))
	# Beam 2: beam splitter -> end mirror A (along +X)
	parts.append(cyl("BeamPath_Arm1", BEAM_R, ARM_LENGTH,
		ARM_LENGTH / 2, 0.0, BEAM_HEIGHT, rot=(0.0, math.radians(90.0), 0.0)))
	# Beam 3: beam splitter -> end mirror B (along +Y)
	parts.append(cyl("BeamPath_Arm2", BEAM_R, ARM_LENGTH,
		0.0, ARM_LENGTH / 2, BEAM_HEIGHT, rot=(math.radians(90.0), 0.0, 0.0)))
	# Beam 4: beam splitter -> detector (along -Y)
	parts.append(cyl("BeamPath_Output", BEAM_R, ARM_LENGTH,
		0.0, -ARM_LENGTH / 2, BEAM_HEIGHT, rot=(math.radians(90.0), 0.0, 0.0)))


def build():
	clear_scene()
	parts = []
	build_optical_bench(parts)
	build_laser(parts)
	build_beam_splitter(parts)
	# Two end mirrors: arm 1 at (+ARM_LENGTH, 0), arm 2 at (0, +ARM_LENGTH)
	build_end_mirror(parts, ARM_LENGTH, 0.0, facing_x=-1)
	build_end_mirror(parts, 0.0, ARM_LENGTH, facing_x=0)
	build_detector(parts)
	build_beam_paths(parts)

	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "MichelsonInterferometer"
	merged.data.name = "MichelsonInterferometer"
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
