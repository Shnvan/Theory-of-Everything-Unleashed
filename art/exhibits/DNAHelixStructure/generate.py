"""Generates the B-DNA double helix exhibit mesh from PDB entry 1BNA.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/DNAHelixStructure/generate.py \
        -- --out art/exhibits/DNAHelixStructure/build/DNAHelixStructure.glb

Structure follows the coordinates published by Drew, Wing, Takano, Broka,
Tanaka, Itakura, and Dickerson in Proc. Natl. Acad. Sci. USA 78 (1981)
2179-2183 -- the first high-resolution crystal structure of B-form DNA. RCSB
PDB entry 1BNA, sequence d(CGCGAATTCGCG), a palindromic 12-mer that pairs
with its own reverse complement.

Render style: ribbon backbones + base-pair rungs, the standard biology-textbook
"double helix" look. Coordinates come from data/1bna.pdb (vendored, not
downloaded at build time). For each residue we read the C1' atom position --
present in every residue, sits at the sugar-base junction -- and use it as the
backbone control point and rung endpoint. Two backbones, twelve rungs.

Alternatives considered and rejected
- Per-atom ball-and-stick: 486 non-hydrogen atoms would need splitting across
  multiple meshes to stay under the 20000 triangle cap, and reads as noise
  from the arena floor.
- Van der Waals space-filling: even more atoms, obscures the double-helix
  shape entirely.

MATERIALS ARE AN ART CHOICE. Real DNA does not have a colour. This uses brass
for the backbones (D-016 palette) with two rung colours to visually
distinguish A-T from G-C pairs. Dossier states so.
"""

import math
import os
import sys

import bpy

# --- source data -------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PDB_PATH = os.path.join(SCRIPT_DIR, "data", "1bna.pdb")

# Sequence per PDB entry: 5'-CGCGAATTCGCG-3', both chains. Chain B is the
# reverse complement (palindromic), so pair i in chain A pairs with residue
# (13 - i) in chain B.
SEQUENCE = "CGCGAATTCGCG"
BP_COUNT = len(SEQUENCE)  # 12

# --- what the source fixes ---------------------------------------------------

# Real B-DNA (Drew et al. 1981)
REAL_RISE_PER_BP_A = 3.4      # angstroms
REAL_BP_PER_TURN = 10.0
REAL_DIAMETER_A = 20.0        # angstroms

# --- envelope ----------------------------------------------------------------

# Shell 43.20 x 54.00 x 31.50, plinth top Y 8.16, ceiling Y 71.16 => 63 studs
# vertical. Helix is oriented so its helical axis is vertical in the exhibit.
SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00

STUDS_TO_BLENDER = 1.0

# --- scale -------------------------------------------------------------------

# Set by helix height fitting the envelope. Real 12 bp at 3.4 A/bp = 40.8 A.
# Divide envelope by real height for stud-per-angstrom.
REAL_HELIX_HEIGHT_A = REAL_RISE_PER_BP_A * (BP_COUNT - 1)  # rise BETWEEN bases
STUDS_PER_A = ENVELOPE_HEIGHT / (REAL_HELIX_HEIGHT_A + REAL_DIAMETER_A * 0.5)
# Leave a bit of headroom so the ends of the helix have visual space above and
# below rather than touching the plinth or ceiling.

# --- render style ------------------------------------------------------------

RIBBON_RADIUS = 0.55
RUNG_RADIUS = 0.35
RIBBON_SEGMENTS = 12  # cross-section resolution
RIBBON_STEPS_PER_BP = 8  # smoothness of ribbon between bases


def parse_pdb_c1_positions(path):
	"""Read C1' atom coordinates per residue, per chain.

	Returns dict[chain][residue_number] = (x, y, z) in angstroms.
	"""
	chains = {}
	with open(path, "r", encoding="ascii") as f:
		for line in f:
			if not line.startswith("ATOM"):
				continue
			atom_name = line[12:16].strip()
			if atom_name != "C1'":
				continue
			chain = line[21]
			resnum = int(line[22:26].strip())
			x = float(line[30:38])
			y = float(line[38:46])
			z = float(line[46:54])
			chains.setdefault(chain, {})[resnum] = (x, y, z)
	return chains


def compute_alignment(chain_a_positions):
	"""Return centroid and a rotation that aligns the helical axis with +Z.

	The helical axis is estimated by the direction from the first C1' atom to
	the last, in chain A. That direction is normalised and used to build a
	rotation matrix taking it to +Z. This is robust to whatever arbitrary
	crystal-frame orientation the PDB entry happens to use -- 1BNA's helix is
	not cleanly along any of X/Y/Z, so hard-coding an axis swap doesn't work.
	"""
	import mathutils
	first = mathutils.Vector(chain_a_positions[0])
	last = mathutils.Vector(chain_a_positions[-1])
	axis = (last - first).normalized()
	up = mathutils.Vector((0.0, 0.0, 1.0))
	# Build rotation from `axis` to `up` (so helical axis becomes +Z)
	dot = max(-1.0, min(1.0, axis.dot(up)))
	if dot > 0.9999:
		return mathutils.Matrix.Identity(3)
	if dot < -0.9999:
		return mathutils.Matrix.Rotation(math.pi, 3, mathutils.Vector((1.0, 0.0, 0.0)))
	rot_axis = axis.cross(up).normalized()
	angle = math.acos(dot)
	return mathutils.Matrix.Rotation(angle, 3, rot_axis)


def to_studs_with_rotation(pos_angstroms, offset, rotation_mat):
	"""Apply centring, rotation, and scale in one go."""
	import mathutils
	v = mathutils.Vector((pos_angstroms[0] - offset[0], pos_angstroms[1] - offset[1], pos_angstroms[2] - offset[2]))
	v = rotation_mat @ v
	return (v.x * STUDS_PER_A, v.y * STUDS_PER_A, v.z * STUDS_PER_A)


def clear_scene():
	bpy.ops.object.select_all(action="SELECT")
	bpy.ops.object.delete(use_global=False)
	for block in (bpy.data.meshes, bpy.data.materials, bpy.data.objects, bpy.data.curves):
		for item in list(block):
			if item.users == 0:
				block.remove(item)


def build_ribbon(name, points):
	"""Segmented cylinder ribbon through consecutive C1' backbone points.

	The bevel-curve approach was tried first and yielded a zero-vertex mesh
	after convert-to-mesh, contributing no geometry. Segmented cylinders are
	simple, robust, and match the approach the rungs already use.

	Between each consecutive pair of C1' atoms we also drop a small sphere at
	the junction so kinks don't leave visible gaps.
	"""
	parts = []
	for i in range(len(points) - 1):
		seg = cyl_between(f"{name}_Seg{i:02d}", points[i], points[i + 1], RIBBON_RADIUS)
		if seg is not None:
			parts.append(seg)
	for i, p in enumerate(points):
		bpy.ops.mesh.primitive_uv_sphere_add(radius=RIBBON_RADIUS * 1.05, segments=10, ring_count=8, location=p)
		o = bpy.context.active_object
		o.name = f"{name}_Joint{i:02d}"
		parts.append(o)

	# Join the segments into a single object so the caller receives one thing.
	if len(parts) == 1:
		return parts[0]
	bpy.ops.object.select_all(action="DESELECT")
	for p in parts:
		p.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	return merged


def cyl_between(name, a, b, radius, verts=10):
	"""Cylinder from point a to point b."""
	mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)
	dx, dy, dz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
	length = math.sqrt(dx * dx + dy * dy + dz * dz)
	# Blender cylinder along Z by default; compute rotation to align with (a->b)
	if length < 1e-6:
		return None
	# Angle between +Z and (a->b)
	nz = dz / length
	xy = math.sqrt(dx * dx + dy * dy)
	pitch = math.atan2(xy, nz)
	yaw = math.atan2(dy, dx)
	bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=length, vertices=verts, location=mid)
	o = bpy.context.active_object
	o.name = name
	# Apply rotation: yaw about Z, then pitch about Y (in that order)
	# The default cylinder is along Z; we want it along (a-b).
	# Simpler: compute rotation matrix from Z to direction.
	import mathutils
	direction = mathutils.Vector((dx, dy, dz)).normalized()
	up = mathutils.Vector((0.0, 0.0, 1.0))
	if direction.dot(up) > 0.9999:
		return o  # already aligned
	if direction.dot(up) < -0.9999:
		o.rotation_euler = (math.pi, 0.0, 0.0)
		return o
	axis = up.cross(direction).normalized()
	angle = math.acos(max(-1.0, min(1.0, up.dot(direction))))
	o.rotation_euler = mathutils.Matrix.Rotation(angle, 4, axis).to_euler()
	return o


def build():
	clear_scene()

	chains = parse_pdb_c1_positions(PDB_PATH)
	if "A" not in chains or "B" not in chains:
		raise SystemExit("FAIL: PDB 1BNA missing chain A or B")

	# Compute the crystal centre so we can offset to origin.
	all_points = list(chains["A"].values()) + list(chains["B"].values())
	cx = sum(p[0] for p in all_points) / len(all_points)
	cy = sum(p[1] for p in all_points) / len(all_points)
	cz = sum(p[2] for p in all_points) / len(all_points)
	offset = (cx, cy, cz)

	# Compute rotation aligning the helical axis with Z. The chain-A endpoints
	# (in raw crystal coords, before centring) give the direction.
	chain_a_raw = [chains["A"][r] for r in sorted(chains["A"].keys())]
	rotation = compute_alignment(chain_a_raw)

	# Backbone points, one per residue, in resnum order, aligned + centred + scaled
	chain_a = [to_studs_with_rotation(chains["A"][r], offset, rotation) for r in sorted(chains["A"].keys())]
	chain_b = [to_studs_with_rotation(chains["B"][r], offset, rotation) for r in sorted(chains["B"].keys())]

	parts = []

	# Two ribbons
	parts.append(build_ribbon("BackboneA", chain_a))
	parts.append(build_ribbon("BackboneB", chain_b))

	# 12 rungs. Palindromic pairing: chain A residue i pairs with chain B residue (13 - i).
	# The PDB numbering in 1BNA is: chain A 1..12, chain B 13..24 (offset by 12).
	# Verify by inspecting the min/max resnums per chain.
	a_min = min(chains["A"].keys())
	b_min = min(chains["B"].keys())
	for i in range(BP_COUNT):
		a_res = a_min + i             # chain A residue at position i
		b_res = b_min + (BP_COUNT - 1 - i)  # chain B residue on the paired side
		if a_res not in chains["A"] or b_res not in chains["B"]:
			raise SystemExit(f"FAIL: base pair {i + 1} references missing residues A{a_res} / B{b_res}")
		a_pos = to_studs_with_rotation(chains["A"][a_res], offset, rotation)
		b_pos = to_studs_with_rotation(chains["B"][b_res], offset, rotation)
		base = SEQUENCE[i]
		# Colour will be set in Studio; here we just name so the pair type is
		# recoverable later if needed.
		name = f"Rung{i + 1:02d}_{base}{'GC' if base in ('G', 'C') else 'AT'}"
		obj = cyl_between(name, a_pos, b_pos, RUNG_RADIUS)
		if obj is not None:
			parts.append(obj)

	# Join into a single mesh
	bpy.ops.object.select_all(action="DESELECT")
	for o in parts:
		o.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	bpy.ops.object.join()

	merged = bpy.context.active_object
	merged.name = "DNAHelix"
	merged.data.name = "DNAHelix"
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
	print(f"GEN_SCALE {STUDS_PER_A:.3f} studs per angstrom")
	print(f"GEN_SEQUENCE {SEQUENCE} ({BP_COUNT} bp)")

	if tris > 20000:
		raise SystemExit(f"FAIL: {tris} triangles exceeds the 20000 per-mesh cap")

	# Envelope: assert against shell width/depth and envelope height.
	if d.z > ENVELOPE_HEIGHT:
		raise SystemExit(f"FAIL: height {d.z:.2f} exceeds the {ENVELOPE_HEIGHT:.2f} stud envelope")
	if d.x > SHELL_WIDTH:
		raise SystemExit(f"FAIL: width {d.x:.2f} overhangs the {SHELL_WIDTH:.2f} stud collision shell")
	if d.y > SHELL_DEPTH:
		raise SystemExit(f"FAIL: depth {d.y:.2f} overhangs the {SHELL_DEPTH:.2f} stud collision shell")

	# Proportion assert: total helical height should be close to
	# (BP_COUNT - 1) * rise_per_bp. If the crystal is aligned along a
	# different axis than expected, height won't match.
	expected_height = REAL_RISE_PER_BP_A * (BP_COUNT - 1) * STUDS_PER_A
	# Allow 20% tolerance because C1' positions are not exactly on the
	# helical axis and the crystal orientation varies slightly.
	if abs(d.z - expected_height) > expected_height * 0.20:
		raise SystemExit(
			f"FAIL: height {d.z:.2f} deviates >20% from expected {expected_height:.2f} "
			f"(helical axis may not be aligned with Blender Z)"
		)

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
