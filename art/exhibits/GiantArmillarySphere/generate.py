"""Generates the armillary sphere exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/GiantArmillarySphere/generate.py \
        -- --out art/exhibits/GiantArmillarySphere/build/GiantArmillarySphere.glb

Structure follows Science Museum Group object 1878-12, Girolamo della Volpaia,
Florence 1554: a Ptolemaic armillary sphere 500 x 300 x 300 mm on triple claw
feet, enclosing a terrestrial globe. Corroborated by della Volpaia's 1564 sphere
at MHS Oxford, which supplies the ring detail 1878-12's record omits.

MATERIALS ARE AN ART CHOICE, NOT AN ACCURACY CLAIM. The real object is wood.
This is authored for brass because D-016 locks the arena to marble, dark stone,
brass and glass, and wood is not in that palette. See README.md -- the factual
museum card must not claim material accuracy.
"""

import math
import os
import sys

import bpy

# --- proportions, from the real object ----------------------------------------

# 1878-12 measures H 500 x W 300 x D 300 mm. Everything below derives from that
# 5:3 ratio rather than being chosen by eye; the previous version was 1.15:1 and
# read as a ball rather than the tall upright instrument it should be.
REAL_HEIGHT_MM = 500.0
REAL_WIDTH_MM = 300.0
TARGET_RATIO = REAL_HEIGHT_MM / REAL_WIDTH_MM  # 1.667

# Sized to the exhibit envelope, which must not grow: the stand seats on the
# plinth top at Y 8.16 and the visual has to stay under Y 71.16, leaving about
# 62.5 studs of height.
#
# Chosen empirically rather than solved. Ring band widths are absolute, so they
# do not scale with the diameter and the finished height runs a little over the
# nominal diameter * ratio. 35.5 measures 62.9 studs tall, which fits; 37.8
# measured 66.98 and overshot the envelope by four studs.
SPHERE_DIAMETER = 35.5
TOTAL_HEIGHT = SPHERE_DIAMETER * TARGET_RATIO

OUTER_RADIUS = SPHERE_DIAMETER / 2.0

# One Blender unit imports as one stud. Verified 2026-07-26: an earlier version
# scaled by 0.01 on the belief that Roblox reads a Blender metre as 100 studs.
# It does not -- with the importer's Scale Unit set to Stud, one unit is one
# stud, and that conversion made the mesh 100x too small.
STUDS_TO_BLENDER = 1.0

# --- ring profile -------------------------------------------------------------

RING_THICKNESS = 0.42

# The 1564 sphere carries a zodiac band 65 mm wide on a 700 mm instrument --
# markedly wider than the plain circles. Differentiating them gives the eye a
# hierarchy; eight identical hoops read as a ball of wire.
BAND_WIDTH_PLAIN = 1.9
BAND_WIDTH_ZODIAC = 3.8
BAND_WIDTH_STRUCTURAL = 2.6

# Real astronomical constants.
OBLIQUITY_DEG = 23.44
POLAR_CIRCLE_DEG = 90.0 - OBLIQUITY_DEG
LATITUDE_DEG = 45.0

MAJOR_SEGMENTS = 64
MINOR_SEGMENTS = 6
GLOBE_SEGMENTS = 32
GLOBE_RINGS = 16


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.objects):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def add_ring(name, radius, band_width, height=0.0, rotation=(0.0, 0.0, 0.0)):
    """One celestial band: a torus flattened into a hoop of the given width."""
    bpy.ops.mesh.primitive_torus_add(
        major_radius=radius,
        minor_radius=RING_THICKNESS,
        major_segments=MAJOR_SEGMENTS,
        minor_segments=MINOR_SEGMENTS,
        location=(0.0, 0.0, height),
        rotation=rotation,
    )
    ring = bpy.context.active_object
    ring.name = name
    ring.scale = (1.0, 1.0, band_width / (RING_THICKNESS * 2.0))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ring


def add_declination_circle(name, declination_deg, band_width):
    """A circle of constant declination -- a tropic or polar circle.

    Radius shrinks with the cosine of the declination and the ring rides up the
    axis with the sine, so these are genuine latitude circles rather than
    evenly spaced hoops.
    """
    d = math.radians(declination_deg)
    return add_ring(name, OUTER_RADIUS * math.cos(d), band_width, OUTER_RADIUS * math.sin(d))


def add_claw_foot(name, angle_deg, base_z):
    """One of three claw feet.

    1878-12 stands on triple claw feet. Approximated as a splayed tapered leg
    with a rounded toe -- the silhouette is what reads at gameplay distance, and
    the real carving is not documented in the object record.
    """
    a = math.radians(angle_deg)
    reach = OUTER_RADIUS * 0.62
    x, y = math.cos(a) * reach, math.sin(a) * reach

    bpy.ops.mesh.primitive_cone_add(
        radius1=OUTER_RADIUS * 0.075,
        radius2=OUTER_RADIUS * 0.03,
        depth=OUTER_RADIUS * 0.55,
        vertices=12,
        location=(x * 0.55, y * 0.55, base_z + OUTER_RADIUS * 0.26),
        rotation=(math.radians(22.0) * math.sin(a), -math.radians(22.0) * math.cos(a), 0.0),
    )
    leg = bpy.context.active_object
    leg.name = f"{name}_Leg"

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=OUTER_RADIUS * 0.062,
        segments=12,
        ring_count=8,
        location=(x, y, base_z + OUTER_RADIUS * 0.05),
    )
    toe = bpy.context.active_object
    toe.name = f"{name}_Toe"
    return [leg, toe]


def build() -> None:
    clear_scene()

    parts = []

    # Structural rings: the meridian carries the sphere, the horizon sits level.
    # On the real instrument these are fixed to the stand, not to the celestial
    # assembly, so they are not tilted with it below.
    parts.append(add_ring("Meridian", OUTER_RADIUS * 1.05, BAND_WIDTH_STRUCTURAL, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_ring("Horizon", OUTER_RADIUS * 1.05, BAND_WIDTH_STRUCTURAL))

    celestial = []
    celestial.append(add_ring("Equator", OUTER_RADIUS, BAND_WIDTH_PLAIN))
    celestial.append(add_declination_circle("TropicOfCancer", OBLIQUITY_DEG, BAND_WIDTH_PLAIN))
    celestial.append(add_declination_circle("TropicOfCapricorn", -OBLIQUITY_DEG, BAND_WIDTH_PLAIN))
    celestial.append(add_declination_circle("ArcticCircle", POLAR_CIRCLE_DEG, BAND_WIDTH_PLAIN))
    celestial.append(add_declination_circle("AntarcticCircle", -POLAR_CIRCLE_DEG, BAND_WIDTH_PLAIN))

    # The zodiac band. Widest ring on the instrument because it carries the sign
    # names and symbols, and the feature that makes an armillary sphere readable
    # rather than a wire globe.
    celestial.append(
        add_ring("ZodiacEcliptic", OUTER_RADIUS, BAND_WIDTH_ZODIAC, rotation=(math.radians(OBLIQUITY_DEG), 0.0, 0.0))
    )

    # Colures: two great circles through the poles, at right angles.
    celestial.append(add_ring("EquinoctialColure", OUTER_RADIUS, BAND_WIDTH_PLAIN, rotation=(math.radians(90.0), 0.0, 0.0)))
    celestial.append(
        add_ring("SolsticialColure", OUTER_RADIUS, BAND_WIDTH_PLAIN, rotation=(math.radians(90.0), 0.0, math.radians(90.0)))
    )

    # Polar axis, which the 1564 record describes as piercing the central sphere.
    bpy.ops.mesh.primitive_cylinder_add(
        radius=RING_THICKNESS * 0.7,
        depth=OUTER_RADIUS * 2.3,
        vertices=16,
        location=(0.0, 0.0, 0.0),
    )
    axis = bpy.context.active_object
    axis.name = "PolarAxis"
    celestial.append(axis)

    # The terrestrial globe. 1878-12 encloses a manuscript globe, so this is a
    # sphere large enough to read as a world rather than a bead.
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=OUTER_RADIUS * 0.22,
        segments=GLOBE_SEGMENTS,
        ring_count=GLOBE_RINGS,
        location=(0.0, 0.0, 0.0),
    )
    globe = bpy.context.active_object
    globe.name = "TerrestrialGlobe"
    celestial.append(globe)

    tilt = math.radians(90.0 - LATITUDE_DEG)
    for obj in celestial:
        obj.rotation_euler = (obj.rotation_euler[0] + tilt, obj.rotation_euler[1], obj.rotation_euler[2])
    parts.extend(celestial)

    # Stand. The sphere's lowest point is at -OUTER_RADIUS * 1.05; the stand
    # occupies the space below it, and its depth is what carries the object to
    # the real 5:3 height.
    sphere_bottom = -OUTER_RADIUS * 1.05
    stand_depth = TOTAL_HEIGHT - (OUTER_RADIUS * 1.05 * 2.0)
    base_z = sphere_bottom - stand_depth

    bpy.ops.mesh.primitive_cylinder_add(
        radius=OUTER_RADIUS * 0.11,
        depth=stand_depth * 0.72,
        vertices=16,
        location=(0.0, 0.0, sphere_bottom - stand_depth * 0.36),
    )
    column = bpy.context.active_object
    column.name = "StandColumn"
    parts.append(column)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=OUTER_RADIUS * 0.30,
        depth=stand_depth * 0.16,
        vertices=32,
        location=(0.0, 0.0, base_z + stand_depth * 0.30),
    )
    collar = bpy.context.active_object
    collar.name = "StandCollar"
    parts.append(collar)

    for i, angle in enumerate((90.0, 210.0, 330.0)):
        parts.extend(add_claw_foot(f"ClawFoot{i + 1}", angle, base_z))

    bpy.ops.object.select_all(action="DESELECT")
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    merged = bpy.context.active_object
    merged.name = "GiantArmillarySphere"
    # The importer names the MeshPart from the mesh DATA, not the object.
    merged.data.name = "GiantArmillarySphere"

    # join() merges into parts[0], which is the meridian ring and carries a 90
    # degree X rotation. The merged object inherits it, so its local axes are
    # swapped relative to the world and `dimensions` reports height as Y.
    # Baking the rotation in leaves vertex positions untouched but makes local
    # space match world space, so measurements mean what they say.
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    merged.location = (0.0, 0.0, 0.0)

    if STUDS_TO_BLENDER != 1.0:
        merged.scale = (STUDS_TO_BLENDER,) * 3
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


def report(obj) -> None:
    """Prints the numbers the pipeline is judged on, and fails loudly on the
    one error that previously slipped through unnoticed."""
    mesh = obj.data
    tris = sum(max(len(p.vertices) - 2, 0) for p in mesh.polygons)
    d = obj.dimensions
    # Z is up in Blender, and the object's rotation has been applied above so
    # local matches world. Width is the larger horizontal axis; the sphere is
    # round, so X and Y should agree closely.
    width = max(d.x, d.y) / STUDS_TO_BLENDER
    height = d.z / STUDS_TO_BLENDER
    ratio = height / width

    print(f"GEN_OBJECT {obj.name}")
    print(f"GEN_TRIANGLES {tris}")
    print(f"GEN_VERTICES {len(mesh.vertices)}")
    print(f"GEN_SIZE_STUDS {d.x / STUDS_TO_BLENDER:.2f} x {d.y / STUDS_TO_BLENDER:.2f} x {d.z / STUDS_TO_BLENDER:.2f}")
    print(f"GEN_RATIO {ratio:.3f} (target {TARGET_RATIO:.3f} from 1878-12's 500x300mm)")

    if tris > 20000:
        raise SystemExit(f"FAIL: {tris} triangles exceeds the 20000 per-mesh importer cap")

    # The previous version shipped at 1.15:1 and nobody noticed until the real
    # object was measured. Assert it so that cannot recur silently.
    if abs(ratio - TARGET_RATIO) > 0.02:
        raise SystemExit(f"FAIL: height/width {ratio:.3f} is not within 0.02 of {TARGET_RATIO:.3f}")

    print("GEN_BUDGET_OK yes")
    print("GEN_RATIO_OK yes")


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
    # GLB rather than GLTF_SEPARATE: one self-contained file, so an import
    # cannot silently lose the accompanying .bin.
    bpy.ops.export_scene.gltf(
        filepath=out_path,
        export_format="GLB",
        use_selection=False,
        export_apply=True,
    )
    print(f"GEN_WROTE {out_path}")


if __name__ == "__main__":
    main()
