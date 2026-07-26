"""Generates the Scientist Statues exhibit mesh: Newton · Tesla · Einstein.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/ScientistStatues/generate.py \
        -- --out art/exhibits/ScientistStatues/build/ScientistStatues.glb

Historical portrayals. User's chosen trio for the Hall of Minds, substituted
for the accuracy doc's original Galileo · Lovelace · Curie:
  - Curie -> Tesla (Q-021: Curie collides with Radiant Pioneer)
  - Galileo, Lovelace -> Einstein, Newton (user pick: maximum public
    recognition)

COMPOSITION: back-to-back hero pose, linear splay.

The user supplied a reference image -- a caricature of Tesla and Einstein
standing back-to-back, each with an outstretched arm holding a glowing
object -- and asked for that composition with Newton inserted in the middle.

  Tesla (x=-9, yaw -40 deg)  turned left,  orb arm reaching world -X
  Newton (x=0,  yaw   0 deg)  facing front, apple held forward at waist
  Einstein (x=+9, yaw +40 deg) turned right, orb arm reaching world +X

POSE TAKEN, CARICATURE STYLE NOT. The reference exaggerates heads and
features for comic effect. Museum statues of real historical people should
be dignified; caricaturing them would read as mocking and sits badly against
the accuracy doc's "historical portrayals" framing. Proportions here stay
realistic. See README.md.

EXPORTS THREE OBJECTS, not one. The orbs are Neon in Studio while everything
else is brass, and geometry cannot carry emissive material -- so material
differentiation requires separate meshes. Same principled split the black
hole uses; see art/README.md, "splitting for physics is different from
splitting for budget".

MATERIALS ARE AN ART CHOICE. Real bronze busts would use bronze; brass
throughout under D-016, with Neon on the two orbs.
"""

import math
import os
import sys

import bpy

SHELL_WIDTH = 43.20
SHELL_DEPTH = 31.50
ENVELOPE_HEIGHT = 63.00
STUDS_TO_BLENDER = 1.0
SEGMENTS = 16

# --- shared plinth + individual pedestals -----------------------------------

SHARED_PLINTH_W = 30.0
SHARED_PLINTH_D = 8.0
SHARED_PLINTH_H = 3.5

MINI_PLINTH_W = 5.0
MINI_PLINTH_D = 5.0
MINI_PLINTH_H = 2.5

STATUE_H = 8.5   # standing figure height above mini-plinth top
STATUE_R = 0.9   # torso radius

# --- composition ------------------------------------------------------------

# Slot positions along X, and the yaw each figure is turned by.
#
# Figures are BUILT facing -Y (toward the viewer). A Z-rotation theta maps the
# facing vector (0,-1) to (sin theta, -cos theta). So:
#   theta = -40 deg -> (-0.64, -0.77)  left and toward viewer   (Tesla)
#   theta =   0 deg -> ( 0.00, -1.00)  straight at viewer       (Newton)
#   theta = +40 deg -> (+0.64, -0.77)  right and toward viewer  (Einstein)
SLOT_TESLA_X, YAW_TESLA = -9.0, math.radians(-40.0)
SLOT_NEWTON_X, YAW_NEWTON = 0.0, math.radians(0.0)
SLOT_EINSTEIN_X, YAW_EINSTEIN = 9.0, math.radians(40.0)

# The outstretched arm is built in figure-LOCAL space along a 45 degree
# forward-outward diagonal. After each figure's yaw this lands almost exactly
# on the world X axis, putting both orbs at the outer extremes of the
# composition (which is what the reference framing does):
#
#   Tesla:    R(-40) . (-0.707, -0.707) ~= (-0.997, -0.087)  -> world -X
#   Einstein: R(+40) . (+0.707, -0.707) ~= (+0.997, -0.087)  -> world +X
ARM_DIAG = math.sqrt(0.5)  # 0.707

ARM_LENGTH = 2.6
ARM_R = 0.28
HAND_R = 0.34
ORB_R = 0.78

# Object names -- the export asserts on these, because if the orbs ever get
# joined into the main mesh they silently lose the ability to be Neon.
NAME_MAIN = "ScientistStatues"
NAME_TESLA_ORB = "Statues_TeslaOrb"
NAME_EINSTEIN_ORB = "Statues_EinsteinOrb"


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


def cone(name, r1, r2, d, x=0.0, y=0.0, z=0.0, verts=SEGMENTS):
	bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=d, vertices=verts, location=(x, y, z))
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


def sphere(name, r, x=0.0, y=0.0, z=0.0, segments=14, rings=10):
	bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=segments, ring_count=rings, location=(x, y, z))
	o = bpy.context.active_object
	o.name = name
	return o


def torus(name, major, minor, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0), major_seg=24, minor_seg=6):
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=major_seg, minor_segments=minor_seg, location=(x, y, z), rotation=rot)
	o = bpy.context.active_object
	o.name = name
	return o


def join_as(name, parts):
	"""Join a list of objects into one named object and return it."""
	bpy.ops.object.select_all(action="DESELECT")
	for p in parts:
		p.select_set(True)
	bpy.context.view_layer.objects.active = parts[0]
	if len(parts) > 1:
		bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	return merged


def place_figure(obj, slot_x, yaw):
	"""Rotate a figure built at origin by `yaw` about Z, then move to its slot.

	Only X and Y are set. Z is left alone deliberately: join() leaves the merged
	object's origin wherever parts[0] happened to sit (well above the ground,
	since parts[0] is a leg or robe centred at mid-height), so forcing
	location.z = 0 would drag the whole figure down by that amount and sink it
	through the plinth. Rotation about Z still spins the figure on the spot,
	because the origin's XY is (0, 0).
	"""
	obj.rotation_euler = (0.0, 0.0, yaw)
	obj.location.x = slot_x
	obj.location.y = 0.0
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.select_all(action="DESELECT")
	obj.select_set(True)
	bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
	return obj


def cyl_along(name, r, p0, p1, verts=10):
	"""Cylinder spanning p0 -> p1, oriented by axis-angle.

	Uses the same construction as the B-DNA generator. An earlier version here
	built the rotation from euler (0, pitch, yaw + pi/2), which is wrong:
	Blender's XYZ euler composes as Rz @ Ry, so +Z maps to
	(sin p * cos(yaw+90), sin p * sin(yaw+90), cos p) -- a 90 degree error in
	the horizontal plane. The arms pointed sideways and read as detached stubs
	while the hands and props (computed from the direction vector directly)
	sat correctly, so the figures looked broken.
	"""
	import mathutils
	dx, dy, dz = p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]
	length = math.sqrt(dx * dx + dy * dy + dz * dz)
	if length < 1e-6:
		return None
	mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2)
	o = cyl(name, r, length, mid[0], mid[1], mid[2], verts=verts)
	direction = mathutils.Vector((dx, dy, dz)).normalized()
	up = mathutils.Vector((0.0, 0.0, 1.0))
	dot = max(-1.0, min(1.0, up.dot(direction)))
	if dot > 0.9999:
		pass
	elif dot < -0.9999:
		o.rotation_euler = (math.pi, 0.0, 0.0)
	else:
		axis = up.cross(direction).normalized()
		o.rotation_euler = mathutils.Matrix.Rotation(math.acos(dot), 4, axis).to_euler()
	return o


def _unit(v):
	mag = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
	return (v[0] / mag, v[1] / mag, v[2] / mag)


def build_bent_arm(parts, shoulder_z, side, name_prefix,
		upper_dir, fore_dir, upper_len=1.5, fore_len=1.8, prop_gap=None):
	"""Two-segment arm with an elbow: shoulder -> elbow -> hand.

	A single straight cylinder reads as a broom handle; the bend makes the
	pose read as a deliberate gesture, which is the whole point of this
	composition. Triangle cost is trivial (~400 tri per figure) against a
	20,000 cap.

	`side` is -1 (arm goes local -X) or +1 (local +X). Direction tuples are
	given in local space with their X component already signed by the caller.

	Returns the prop centre, just beyond the hand along the forearm direction.
	"""
	u = _unit(upper_dir)
	f = _unit(fore_dir)

	shoulder = (side * STATUE_R * 0.85, 0.0, shoulder_z)
	elbow = (shoulder[0] + u[0] * upper_len,
		shoulder[1] + u[1] * upper_len,
		shoulder[2] + u[2] * upper_len)
	hand = (elbow[0] + f[0] * fore_len,
		elbow[1] + f[1] * fore_len,
		elbow[2] + f[2] * fore_len)

	seg = cyl_along(f"{name_prefix}_UpperArm", ARM_R, shoulder, elbow)
	if seg:
		parts.append(seg)
	parts.append(sphere(f"{name_prefix}_Elbow", ARM_R * 1.1, elbow[0], elbow[1], elbow[2], segments=8, rings=6))
	seg = cyl_along(f"{name_prefix}_Forearm", ARM_R * 0.9, elbow, hand)
	if seg:
		parts.append(seg)
	parts.append(sphere(f"{name_prefix}_Hand", HAND_R, hand[0], hand[1], hand[2], segments=10, rings=6))

	gap = prop_gap if prop_gap is not None else (HAND_R + ORB_R * 0.6)
	return (hand[0] + f[0] * gap, hand[1] + f[1] * gap, hand[2] + f[2] * gap + ORB_R * 0.2)


def add_facing_cues(parts, prefix, torso_z, torso_r, torso_h, head_z, head_r):
	"""Chest plate and nose on the figure's local front (-Y).

	Without these the splay is invisible: the torsos are rotationally
	symmetric cylinders, so a yaw about Z changes nothing you can see, and
	only the arms betray that the figures are turned. A flat chest and a nose
	give the eye a facing direction, which is what sells the back-to-back
	reading in the reference composition.
	"""
	parts.append(box(f"{prefix}_Chest", torso_r * 1.5, 0.25, torso_h * 0.6,
		0.0, -torso_r * 0.92, torso_z))
	parts.append(sphere(f"{prefix}_Nose", head_r * 0.24,
		0.0, -head_r * 0.92, head_z, segments=6, rings=5))


def build_mini_plinth(parts, cx, name):
	"""Axis-aligned pedestal. Deliberately NOT rotated with the figure -- a
	statue turned on a square pedestal is how real museum statues sit."""
	top_z = SHARED_PLINTH_H + 0.4
	parts.append(box(name, MINI_PLINTH_W, MINI_PLINTH_D, MINI_PLINTH_H, cx, 0.0, top_z + MINI_PLINTH_H / 2))
	return top_z + MINI_PLINTH_H


def build_shared_plinth(parts):
	parts.append(box("SharedPlinth", SHARED_PLINTH_W, SHARED_PLINTH_D, SHARED_PLINTH_H,
		0.0, 0.0, SHARED_PLINTH_H / 2))
	parts.append(box("SharedPlinthRim", SHARED_PLINTH_W + 0.6, SHARED_PLINTH_D + 0.6, 0.4,
		0.0, 0.0, SHARED_PLINTH_H))


# --- figures, all built at ORIGIN facing -Y ---------------------------------

def build_newton_figure(base_z):
	"""Isaac Newton (1643-1727): scholar's robe, long Baroque wig, apple held
	forward in an open palm at waist height. Reference: Kneller 1689 portrait.

	Newton is the centre figure and faces straight out, so his arm reaches
	forward rather than outward -- he shouldn't compete with the two orbs.
	"""
	parts = []
	robe_h = STATUE_H * 0.62
	parts.append(cone("Newton_Robe", STATUE_R * 1.4, STATUE_R * 0.95, robe_h, 0.0, 0.0, base_z + robe_h / 2))
	torso_h = STATUE_H * 0.22
	parts.append(cyl("Newton_Torso", STATUE_R * 0.95, torso_h, 0.0, 0.0, base_z + robe_h + torso_h / 2))
	head_r = STATUE_R * 0.75
	shoulder_z = base_z + robe_h + torso_h * 0.75
	parts.append(sphere("Newton_Head", head_r, 0.0, 0.0, base_z + robe_h + torso_h + head_r * 0.9))
	wig_h = STATUE_H * 0.14
	parts.append(cone("Newton_Wig", head_r * 1.15, head_r * 0.7, wig_h,
		0.0, 0.0, base_z + robe_h + torso_h - wig_h / 2 + head_r * 0.3))
	add_facing_cues(parts, "Newton", base_z + robe_h + torso_h / 2, STATUE_R * 0.95, torso_h,
		base_z + robe_h + torso_h + head_r * 0.9, head_r)

	# Arm angled forward-and-outward toward viewer-left, palm up.
	#
	# Newton's yaw is 0, so a straight-forward arm points directly at the
	# camera and foreshortens to nothing -- the first render showed the apple
	# as a sphere apparently stuck to his chest. Angling it out to local -X
	# (the empty gap between Newton and Tesla, since Tesla's own arm reaches
	# the far side) makes the gesture read from the arena's approach direction.
	apple_pos = build_bent_arm(parts, shoulder_z, side=-1, name_prefix="Newton",
		upper_dir=(-0.42, -0.38, -0.82), fore_dir=(-0.46, -0.80, 0.38),
		upper_len=1.4, fore_len=1.7, prop_gap=HAND_R + 0.32)

	# Apple -- solid brass, joins the main mesh (a physical object, not a
	# phenomenon, so it does not glow)
	parts.append(sphere("Newton_Apple", 0.5, apple_pos[0], apple_pos[1], apple_pos[2], segments=12, rings=8))
	parts.append(cyl("Newton_AppleStem", 0.07, 0.35,
		apple_pos[0], apple_pos[1], apple_pos[2] + 0.5, verts=6))
	return parts, None


def build_tesla_figure(base_z):
	"""Nikola Tesla (1856-1943): three-piece suit, groomed hair, outstretched
	arm holding a lightning orb. Reference: Sarony 1893 portrait.

	Outward arm on local -X so that after yaw -40 deg it reaches world -X.
	"""
	parts = []
	leg_h = STATUE_H * 0.42
	parts.append(cyl("Tesla_Legs", STATUE_R * 0.85, leg_h, 0.0, 0.0, base_z + leg_h / 2))
	torso_h = STATUE_H * 0.36
	parts.append(cyl("Tesla_Suit", STATUE_R * 1.05, torso_h, 0.0, 0.0, base_z + leg_h + torso_h / 2))
	head_r = STATUE_R * 0.7
	shoulder_z = base_z + leg_h + torso_h * 0.82
	parts.append(sphere("Tesla_Head", head_r, 0.0, 0.0, base_z + leg_h + torso_h + head_r * 0.9))
	parts.append(sphere("Tesla_Hair", head_r * 0.85, 0.0, 0.0, base_z + leg_h + torso_h + head_r * 1.35))
	add_facing_cues(parts, "Tesla", base_z + leg_h + torso_h / 2, STATUE_R * 1.05, torso_h,
		base_z + leg_h + torso_h + head_r * 0.9, head_r)

	# Bent arm reaching forward-outward. Net shoulder->hand direction is a
	# ~36 degree local diagonal, which after the -40 degree yaw lands at
	# world (-0.998, +0.069) -- essentially straight out along -X.
	orb_pos = build_bent_arm(parts, shoulder_z, side=-1, name_prefix="Tesla",
		upper_dir=(-0.60, -0.35, -0.72), fore_dir=(-0.75, -0.62, 0.25))
	return parts, orb_pos


def build_einstein_figure(base_z):
	"""Albert Einstein (1879-1955): casual clothes, iconic wild hair,
	outstretched arm holding a galaxy orb.

	Outward arm on local +X so that after yaw +40 deg it reaches world +X.

	PILOT — recognisable-figurine fidelity (~60-80 primitives instead of ~15).
	Compared to Tesla and Newton in the same session, Einstein gets:
	  - Real body proportions (shoulders + torso taper + hips + separate legs
	    + feet), not one cylinder for legs and one for torso
	  - Casual sweater with visible collar and lower hem
	  - Face features: nose, moustache, eyebrow ridges, chin
	  - Wild hair as 10 radial spikes around a smaller head, not one big sphere
	This is the signature Einstein silhouette the low-primitive version cannot
	produce. If the pilot reads as recognisably him, the same technique goes
	on Newton and Tesla in a follow-up session.
	"""
	parts = []

	# --- lower body: separate legs and feet, hip block above -----------------
	foot_h = 0.4
	foot_len = 1.0
	foot_w = 0.55
	leg_h = STATUE_H * 0.34
	leg_r = STATUE_R * 0.42
	for side in (-1.0, 1.0):
		lx = side * STATUE_R * 0.48
		# Foot
		parts.append(box(f"Einstein_Foot_{side > 0 and 'R' or 'L'}", foot_w, foot_len, foot_h,
			lx, -0.15, base_z + foot_h / 2))
		# Trouser leg
		parts.append(cyl(f"Einstein_Leg_{side > 0 and 'R' or 'L'}", leg_r, leg_h,
			lx, 0.0, base_z + foot_h + leg_h / 2))
	# Hip block spans between the leg tops
	hip_h = STATUE_H * 0.09
	hip_z = base_z + foot_h + leg_h + hip_h / 2
	parts.append(box("Einstein_Hips", STATUE_R * 1.4, STATUE_R * 1.1, hip_h,
		0.0, 0.0, hip_z))
	# Belt / trouser waistband — thin stripe of contrast at the top of the hips
	parts.append(box("Einstein_Belt", STATUE_R * 1.45, STATUE_R * 1.12, 0.18,
		0.0, 0.0, hip_z + hip_h / 2 + 0.09))

	# --- torso: sweater tapering slightly outward from waist to shoulders ----
	torso_h = STATUE_H * 0.30
	torso_bottom_r = STATUE_R * 1.05
	torso_top_r = STATUE_R * 1.15
	torso_bottom_z = base_z + foot_h + leg_h + hip_h
	torso_top_z = torso_bottom_z + torso_h
	parts.append(cone("Einstein_Sweater", torso_bottom_r, torso_top_r, torso_h,
		0.0, 0.0, torso_bottom_z + torso_h / 2))
	# Sweater lower hem — the fold where the sweater meets the trousers
	parts.append(torus("Einstein_SweaterHem", torso_bottom_r * 1.02, 0.15,
		0.0, 0.0, torso_bottom_z + 0.15, major_seg=20, minor_seg=4))
	# Collar around the neck opening — V-neck-ish
	collar_z = torso_top_z - 0.2
	parts.append(torus("Einstein_Collar", STATUE_R * 0.55, 0.16,
		0.0, 0.0, collar_z, major_seg=20, minor_seg=4))

	# --- neck ----------------------------------------------------------------
	neck_h = STATUE_H * 0.04
	parts.append(cyl("Einstein_Neck", STATUE_R * 0.35, neck_h,
		0.0, 0.0, torso_top_z + neck_h / 2))

	# --- head + face features ------------------------------------------------
	# Head slightly smaller than the ~1.25 hair sphere the naive version used,
	# because the hair spikes will sit around it and take the extra volume.
	head_r = STATUE_R * 0.62
	head_z = torso_top_z + neck_h + head_r
	parts.append(sphere("Einstein_Head", head_r, 0.0, 0.0, head_z, segments=20, rings=14))
	# Nose — elongated small box, facing -Y (the figure's own front, before yaw)
	parts.append(box("Einstein_Nose", 0.18, 0.35, 0.24,
		0.0, -head_r * 0.98, head_z - 0.05))
	# Moustache — the tag-line Einstein feature. Flat wide box below the nose.
	parts.append(box("Einstein_Moustache", 0.62, 0.18, 0.14,
		0.0, -head_r * 0.94, head_z - 0.32))
	# Eyebrow ridges — thick, one per eye
	for side in (-1.0, 1.0):
		parts.append(box(f"Einstein_Brow_{side > 0 and 'R' or 'L'}", 0.28, 0.14, 0.09,
			side * 0.20, -head_r * 0.92, head_z + 0.20))
	# Eye recesses — small dark spheres for eye sockets
	for side in (-1.0, 1.0):
		parts.append(sphere(f"Einstein_Eye_{side > 0 and 'R' or 'L'}", 0.10,
			side * 0.18, -head_r * 0.94, head_z + 0.05, segments=8, rings=6))
	# Chin definition — a small tapered stub below the moustache
	parts.append(box("Einstein_Chin", 0.42, 0.24, 0.22,
		0.0, -head_r * 0.88, head_z - 0.55))
	# Ears — two small spheres on the sides of the head
	for side in (-1.0, 1.0):
		parts.append(sphere(f"Einstein_Ear_{side > 0 and 'R' or 'L'}", 0.14,
			side * head_r * 0.92, 0.0, head_z, segments=8, rings=6))

	# --- WILD HAIR as radial spikes ------------------------------------------
	# 10 spikes distributed over the top and back of the head. Each spike is
	# an elongated cone pointing outward from the head centre, giving the
	# characteristic "electrocuted" silhouette.
	spike_count = 10
	spike_len = 0.9
	spike_base_r = 0.22
	for i in range(spike_count):
		# Skew the distribution toward the top and back of the head, away from
		# the face. Azimuth avoids the front-centre; elevation biases upward.
		azimuth = math.radians(-140.0 + (280.0 * i / (spike_count - 1)))
		elevation = math.radians(35.0 + 30.0 * ((i * 137) % 40) / 40.0)  # jittered per-spike
		# Spike tip direction
		dx = math.cos(elevation) * math.sin(azimuth)
		dy = -math.cos(elevation) * math.cos(azimuth)   # -Y is "front", so most spikes point away
		dz = math.sin(elevation)
		# Spike root sits on the head surface; centre halfway to the tip
		root = (dx * head_r * 0.95, dy * head_r * 0.95, head_z + dz * head_r * 0.95)
		tip = (root[0] + dx * spike_len, root[1] + dy * spike_len, root[2] + dz * spike_len)
		mid = ((root[0] + tip[0]) / 2, (root[1] + tip[1]) / 2, (root[2] + tip[2]) / 2)
		# Orient a cone from root to tip using axis-angle
		import mathutils
		bpy.ops.mesh.primitive_cone_add(radius1=spike_base_r, radius2=0.03,
			depth=spike_len, vertices=8, location=mid)
		spike = bpy.context.active_object
		spike.name = f"Einstein_HairSpike{i:02d}"
		direction = mathutils.Vector((dx, dy, dz)).normalized()
		up = mathutils.Vector((0.0, 0.0, 1.0))
		dot = max(-1.0, min(1.0, up.dot(direction)))
		if dot < 0.9999 and dot > -0.9999:
			axis = up.cross(direction).normalized()
			spike.rotation_euler = mathutils.Matrix.Rotation(math.acos(dot), 4, axis).to_euler()
		elif dot < -0.9999:
			spike.rotation_euler = (math.pi, 0.0, 0.0)
		parts.append(spike)

	# --- second, non-outstretched arm ----------------------------------------
	# The current build_bent_arm handles the outstretched right arm reaching
	# for the orb. Add a shorter left arm hanging down beside the body so the
	# figure doesn't look one-armed at higher fidelity.
	shoulder_z = torso_top_z - 0.1
	# Left arm — bent slightly forward, hand near hip
	left_shoulder = (-STATUE_R * 1.05, 0.0, shoulder_z)
	left_elbow = (-STATUE_R * 1.25, -0.35, shoulder_z - 2.0)
	left_hand = (-STATUE_R * 1.05, -0.55, shoulder_z - 3.4)
	seg = cyl_along("Einstein_UpperArmL", ARM_R, left_shoulder, left_elbow)
	if seg: parts.append(seg)
	parts.append(sphere("Einstein_ElbowL", ARM_R * 1.1, left_elbow[0], left_elbow[1], left_elbow[2], segments=8, rings=6))
	seg = cyl_along("Einstein_ForearmL", ARM_R * 0.9, left_elbow, left_hand)
	if seg: parts.append(seg)
	parts.append(sphere("Einstein_HandL", HAND_R, left_hand[0], left_hand[1], left_hand[2], segments=10, rings=6))

	# --- right arm + orb (unchanged bent-arm pose) ---------------------------
	orb_pos = build_bent_arm(parts, shoulder_z, side=+1, name_prefix="Einstein",
		upper_dir=(0.60, -0.35, -0.72), fore_dir=(0.75, -0.62, 0.25))
	return parts, orb_pos


def build():
	clear_scene()

	main_parts = []
	build_shared_plinth(main_parts)

	# Pedestals stay axis-aligned; only the figures rotate.
	base_z = build_mini_plinth(main_parts, SLOT_TESLA_X, "Tesla_Plinth")
	build_mini_plinth(main_parts, SLOT_NEWTON_X, "Newton_Plinth")
	build_mini_plinth(main_parts, SLOT_EINSTEIN_X, "Einstein_Plinth")

	orb_objects = []

	# Tesla
	tesla_parts, tesla_orb_pos = build_tesla_figure(base_z)
	tesla_fig = join_as("TeslaFigure", tesla_parts)
	place_figure(tesla_fig, SLOT_TESLA_X, YAW_TESLA)
	main_parts.append(tesla_fig)

	# Newton (no orb)
	newton_parts, _ = build_newton_figure(base_z)
	newton_fig = join_as("NewtonFigure", newton_parts)
	place_figure(newton_fig, SLOT_NEWTON_X, YAW_NEWTON)
	main_parts.append(newton_fig)

	# Einstein
	einstein_parts, einstein_orb_pos = build_einstein_figure(base_z)
	einstein_fig = join_as("EinsteinFigure", einstein_parts)
	place_figure(einstein_fig, SLOT_EINSTEIN_X, YAW_EINSTEIN)
	main_parts.append(einstein_fig)

	# Main brass mesh
	main = join_as(NAME_MAIN, main_parts)
	main.data.name = NAME_MAIN
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

	# --- orbs, as SEPARATE objects so they can be Neon in Studio ------------
	# Their local positions were computed pre-rotation, so apply the same
	# yaw + slot translation the figure got.
	def world_orb(local_pos, slot_x, yaw, name, r):
		lx, ly, lz = local_pos
		wx = lx * math.cos(yaw) - ly * math.sin(yaw) + slot_x
		wy = lx * math.sin(yaw) + ly * math.cos(yaw)
		o = sphere(name, r, wx, wy, lz, segments=18, rings=12)
		o.data.name = name
		bpy.ops.object.shade_smooth()
		return o

	orb_objects.append(world_orb(tesla_orb_pos, SLOT_TESLA_X, YAW_TESLA, NAME_TESLA_ORB, ORB_R))
	orb_objects.append(world_orb(einstein_orb_pos, SLOT_EINSTEIN_X, YAW_EINSTEIN, NAME_EINSTEIN_ORB, ORB_R))

	return [main] + orb_objects


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

	# The orbs MUST stay separate objects. If a future edit joins them into the
	# main mesh they silently lose the ability to carry a Neon material, and
	# the exhibit ships with two dead brass balls instead of glowing orbs.
	expected = {NAME_MAIN, NAME_TESLA_ORB, NAME_EINSTEIN_ORB}
	if set(names) != expected:
		raise SystemExit(f"FAIL: expected exactly {sorted(expected)}, got {sorted(names)}")
	print("GEN_SPLIT_OK 3 objects, orbs separate for Neon")

	if size[2] > ENVELOPE_HEIGHT:
		raise SystemExit(f"FAIL: height {size[2]:.2f} exceeds envelope {ENVELOPE_HEIGHT:.2f}")
	if size[0] > SHELL_WIDTH:
		raise SystemExit(f"FAIL: width {size[0]:.2f} overhangs shell {SHELL_WIDTH:.2f}")
	if size[1] > SHELL_DEPTH:
		raise SystemExit(f"FAIL: depth {size[1]:.2f} overhangs shell {SHELL_DEPTH:.2f}")

	print(f"GEN_SHELL_MARGIN {SHELL_WIDTH - size[0]:.2f} x {SHELL_DEPTH - size[1]:.2f}")
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
