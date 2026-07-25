"""Generates the armillary sphere exhibit mesh.

Run headless:

    blender --background --factory-startup \
        --python art/exhibits/GiantArmillarySphere/generate.py \
        -- --out art/exhibits/GiantArmillarySphere/build/GiantArmillarySphere.gltf

Accuracy note, and read this before trusting the output. The *astronomy* here is
real: the obliquity of the ecliptic, the tropics, and the polar circles use their
actual values, and the ring set is the standard Ptolemaic (geocentric)
construction the Della Volpaia sphere belongs to. The *proportions* -- ring
width, thickness, stand shape -- are stylistic and have NOT been verified against
Science Museum Group object 1878-12. See README.md in this directory.

Replaces 71 primitive parts, 48 of which were spheres strung into rings.
"""

import math
import os
import sys

import bpy

# --- parameters ---------------------------------------------------------------

# One Blender unit imports as one stud, so no conversion is applied.
#
# Verified by import on 2026-07-26, not assumed. An earlier version of this file
# scaled by 0.01 on the documented belief that Roblox reads a Blender metre as
# 100 studs. It does not: with the importer's `Scale Unit` set to `Stud`, one
# file unit is one stud, so that conversion made the mesh 100x too small and had
# to be undone by hand with a Scale Factor of 100. Authoring 1:1 means every
# exhibit imports correctly at Scale Factor 1 with nothing to remember.
STUDS_TO_BLENDER = 1.0

# Sized to sit inside the existing exhibit footprint, whose collision shell
# measures 43.20 x 54.00 x 33.92 studs. Verify after import; do not assume.
OUTER_RADIUS = 21.0
RING_THICKNESS = 0.55
BAND_WIDTH_RATIO = 2.6  # rings are flat bands, not round wire

# Real astronomical constants.
OBLIQUITY_DEG = 23.44  # tilt of the ecliptic to the celestial equator
POLAR_CIRCLE_DEG = 90.0 - OBLIQUITY_DEG  # 66.56
LATITUDE_DEG = 45.0  # the whole celestial assembly is tilted to a latitude

# Segment counts. Each torus costs major * minor * 2 triangles, so these drive
# the budget directly. The importer rejects any single mesh above 20,000.
MAJOR_SEGMENTS = 64
MINOR_SEGMENTS = 6
SPHERE_SEGMENTS = 32
SPHERE_RINGS = 16


def clear_scene() -> None:
    """Removes the factory-startup cube, camera, and light."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.objects):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def add_ring(name: str, radius: float, height: float = 0.0, rotation=(0.0, 0.0, 0.0)):
    """Adds one flat celestial band.

    A torus with a deliberately non-square minor profile, scaled after creation
    so the band reads as a flat brass hoop rather than round wire.
    """
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
    # Widen along the ring's own axis so the band faces outward.
    ring.scale = (1.0, 1.0, BAND_WIDTH_RATIO)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ring


def add_small_circle(name: str, declination_deg: float):
    """A circle of constant declination -- a tropic or a polar circle.

    Radius shrinks with the cosine of the declination and the ring rides up the
    polar axis with the sine, which is what makes these read as latitude circles
    rather than arbitrary hoops.
    """
    d = math.radians(declination_deg)
    return add_ring(name, OUTER_RADIUS * math.cos(d), OUTER_RADIUS * math.sin(d))


def build() -> None:
    clear_scene()

    parts = []

    # Structural rings, fixed to the stand and not part of the celestial sphere.
    parts.append(add_ring("Meridian", OUTER_RADIUS * 1.06, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_ring("Horizon", OUTER_RADIUS * 1.06))

    # The celestial assembly. Built axis-aligned, then tilted as one group.
    celestial = []
    celestial.append(add_ring("Equator", OUTER_RADIUS))
    celestial.append(add_small_circle("TropicOfCancer", OBLIQUITY_DEG))
    celestial.append(add_small_circle("TropicOfCapricorn", -OBLIQUITY_DEG))
    celestial.append(add_small_circle("ArcticCircle", POLAR_CIRCLE_DEG))
    celestial.append(add_small_circle("AntarcticCircle", -POLAR_CIRCLE_DEG))

    # The ecliptic: the sun's apparent yearly path, inclined to the equator by
    # the obliquity. This is the ring that makes an armillary sphere an
    # armillary sphere rather than a wire globe.
    celestial.append(add_ring("Ecliptic", OUTER_RADIUS, rotation=(math.radians(OBLIQUITY_DEG), 0.0, 0.0)))

    # Colures: two great circles through both poles, at right angles.
    celestial.append(add_ring("EquinoctialColure", OUTER_RADIUS, rotation=(math.radians(90.0), 0.0, 0.0)))
    celestial.append(
        add_ring("SolsticialColure", OUTER_RADIUS, rotation=(math.radians(90.0), 0.0, math.radians(90.0)))
    )

    # Polar axis.
    bpy.ops.mesh.primitive_cylinder_add(
        radius=RING_THICKNESS * 0.8,
        depth=OUTER_RADIUS * 2.25,
        vertices=16,
        location=(0.0, 0.0, 0.0),
    )
    axis = bpy.context.active_object
    axis.name = "PolarAxis"
    celestial.append(axis)

    # Earth at the centre. Ptolemaic: geocentric, which is the point.
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=OUTER_RADIUS * 0.17,
        segments=SPHERE_SEGMENTS,
        ring_count=SPHERE_RINGS,
        location=(0.0, 0.0, 0.0),
    )
    earth = bpy.context.active_object
    earth.name = "Earth"
    celestial.append(earth)

    # Tilt the celestial assembly to the working latitude.
    tilt = math.radians(90.0 - LATITUDE_DEG)
    for obj in celestial:
        obj.rotation_euler = (
            obj.rotation_euler[0] + tilt,
            obj.rotation_euler[1],
            obj.rotation_euler[2],
        )
    parts.extend(celestial)

    # Stand: a stepped pedestal, deliberately simple. Its shape is invention.
    bpy.ops.mesh.primitive_cylinder_add(
        radius=OUTER_RADIUS * 0.42,
        depth=OUTER_RADIUS * 0.18,
        vertices=32,
        location=(0.0, 0.0, -OUTER_RADIUS * 1.16),
    )
    base = bpy.context.active_object
    base.name = "StandBase"
    parts.append(base)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=OUTER_RADIUS * 0.13,
        depth=OUTER_RADIUS * 0.30,
        vertices=16,
        location=(0.0, 0.0, -OUTER_RADIUS * 1.02),
    )
    column = bpy.context.active_object
    column.name = "StandColumn"
    parts.append(column)

    # Join into a single object so the importer produces one MeshPart.
    bpy.ops.object.select_all(action="DESELECT")
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    merged = bpy.context.active_object
    merged.name = "GiantArmillarySphere"
    # The importer names the MeshPart from the MESH DATA, not the object, so
    # this must be set too. Without it the part arrives called "Torus", after
    # whichever primitive happened to be active during the join.
    merged.data.name = "GiantArmillarySphere"

    # Recentre on the origin so the importer places it predictably.
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    merged.location = (0.0, 0.0, 0.0)

    # Studs to Blender metres, applied last so every dimension above stays
    # readable as studs.
    merged.scale = (STUDS_TO_BLENDER,) * 3
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


def report(obj) -> int:
    """Prints the numbers the pipeline is judged on."""
    mesh = obj.data
    tris = sum(max(len(p.vertices) - 2, 0) for p in mesh.polygons)
    dims = obj.dimensions
    print(f"GEN_OBJECT {obj.name}")
    print(f"GEN_TRIANGLES {tris}")
    print(f"GEN_VERTICES {len(mesh.vertices)}")
    print(
        "GEN_SIZE_STUDS "
        f"{dims.x / STUDS_TO_BLENDER:.2f} x {dims.y / STUDS_TO_BLENDER:.2f} x {dims.z / STUDS_TO_BLENDER:.2f}"
    )
    print(f"GEN_BUDGET_OK {'yes' if tris <= 20000 else 'NO -- exceeds the 20000 per-mesh importer cap'}")
    return tris


def main() -> None:
    argv = sys.argv
    out_path = None
    if "--" in argv:
        rest = argv[argv.index("--") + 1 :]
        if "--out" in rest:
            out_path = rest[rest.index("--out") + 1]
    if out_path is None:
        raise SystemExit("usage: ... --python generate.py -- --out <path.gltf>")

    build()
    obj = bpy.context.active_object
    report(obj)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    # GLB rather than GLTF_SEPARATE: a single self-contained file. The separate
    # form splits into .gltf plus .bin which must be kept together, and an
    # import that silently loses the .bin is an easy mistake to make.
    bpy.ops.export_scene.gltf(
        filepath=out_path,
        export_format="GLB",
        use_selection=False,
        export_apply=True,
    )
    print(f"GEN_WROTE {out_path}")


if __name__ == "__main__":
    main()
