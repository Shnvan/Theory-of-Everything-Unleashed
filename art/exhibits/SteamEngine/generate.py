"""Generates the Boulton and Watt rotative beam engine exhibit mesh.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/SteamEngine/generate.py \
        -- --out art/exhibits/SteamEngine/build/SteamEngine.glb

Structure follows Science Museum Group object 1861-46, the Lap Engine, built by
Boulton and Watt in 1788 and used at the Soho Manufactory to drive 43 lapping
machines for seventy years. It is the oldest essentially unaltered rotative
engine in the world.

THIS REPLACES A LOCOMOTIVE. The prototype it supersedes was built from a boiler,
firebox, chimney stack and wheels -- the wrong class of engine entirely. A
rotative beam engine is a stationary machine: a rocking beam on a raised pivot,
a vertical cylinder at one end, and a sun-and-planet gear driving a flywheel at
the other. No boiler, no chimney, no wheels.

MATERIALS ARE AN ART CHOICE. See README.md -- the factual museum card must not
claim material accuracy.
"""

import math
import os
import sys

import bpy

# --- what the sources actually fix --------------------------------------------

# Cylinder bore 18.75 in (476 mm) and stroke 4 ft (1219 mm). These are the only
# hard dimensions found for 1861-46, so they set the cylinder's proportions and
# everything else scales from the exhibit envelope. The dossier says so.
BORE_MM = 476.0
STROKE_MM = 1219.0
CYLINDER_ASPECT = STROKE_MM / BORE_MM  # ~2.56, height to diameter

# --- envelope -----------------------------------------------------------------

# The exhibit spans 70.66 x 68.00 x 70.21 with the plinth top at Y 8.16, and the
# collision shell is 43.20 x 54.00 x 35.00. The SHELL is the binding constraint,
# not the exhibit extents: geometry wider than the shell is walked through rather
# than walked around. The first run cleared the extents at 54.66 wide and still
# overhung the shell by 11 studs.
SHELL_WIDTH = 43.20
SHELL_DEPTH = 35.00
ENVELOPE_HEIGHT = 63.00  # plinth top Y 8.16 to the exhibit ceiling at 71.16

TOTAL_WIDTH = 30.0
BED_DEPTH = 18.0

STUDS_TO_BLENDER = 1.0

# Explicit layout rather than ratios of ratios. The beam ends have to sit above
# the cylinder and the connecting rod respectively, so those three X positions
# are one decision, and deriving them separately let them drift apart.
BEAM_LENGTH = 24.5
BEAM_Z = 54.0
CYLINDER_X = -11.0
FLYWHEEL_X = 10.5

CYLINDER_DIAMETER = 9.5
CYLINDER_HEIGHT = CYLINDER_DIAMETER * CYLINDER_ASPECT  # keeps the real bore:stroke
FLYWHEEL_DIAMETER = 24.0

SEGMENTS = 24
RING_SEGMENTS = 40


def clear_scene() -> None:
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


def torus(name, major, minor, x=0.0, y=0.0, z=0.0, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major, minor_radius=minor, major_segments=RING_SEGMENTS, minor_segments=8,
        location=(x, y, z), rotation=rot,
    )
    o = bpy.context.active_object
    o.name = name
    return o


def build_bedplate(parts) -> None:
    parts.append(box("Bedplate", TOTAL_WIDTH * 0.92, BED_DEPTH, 1.8, 0.0, 0.0, 0.9))
    for sx in (-1.0, 1.0):
        parts.append(box("BedRail", TOTAL_WIDTH * 0.9, 1.4, 0.9, 0.0, sx * BED_DEPTH * 0.38, 2.2))


def build_entablature(parts) -> None:
    """The cast-iron frame carrying the beam pivot.

    Four fluted columns and a capping entablature. This engine class was sold as
    a finished architectural object, not a bare mechanism, which is why the
    columns matter to the silhouette.
    """
    column_h = BEAM_Z - 3.0
    # Spread wider than the first pass, which clustered them near the centreline
    # and made the frame read as a single mast rather than a portal.
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            parts.append(cyl("Column", 1.35, column_h, sx * 5.0, sy * BED_DEPTH * 0.33, 1.8 + column_h / 2))
            parts.append(cyl("ColumnCap", 1.75, 0.9, sx * 5.0, sy * BED_DEPTH * 0.33, 1.8 + column_h))
    parts.append(box("Entablature", 16.0, BED_DEPTH * 0.80, 1.6, 0.0, 0.0, BEAM_Z - 1.6))


def build_beam(parts) -> None:
    """The rocking beam and its pivot.

    Held level. The real beam rocks, but D-016 keeps every exhibit static, and
    a frozen mid-stroke pose reads as broken rather than paused.
    """
    parts.append(cyl("BeamPivot", 1.7, TOTAL_WIDTH * 0.20, 0.0, 0.0, BEAM_Z, rot=(math.radians(90.0), 0.0, 0.0)))

    # Lozenge profile: deep at the pivot, tapering to the ends, which is how
    # these beams were cast to carry bending load.
    for sx in (-1.0, 1.0):
        parts.append(box("BeamInner", BEAM_LENGTH * 0.26, 1.8, 5.2, sx * BEAM_LENGTH * 0.13, 0.0, BEAM_Z))
        parts.append(box("BeamOuter", BEAM_LENGTH * 0.24, 1.8, 3.4, sx * BEAM_LENGTH * 0.37, 0.0, BEAM_Z))
        parts.append(cyl("BeamEndBoss", 1.5, 1.9, sx * BEAM_LENGTH * 0.49, 0.0, BEAM_Z, rot=(math.radians(90.0), 0.0, 0.0)))


def build_cylinder(parts) -> None:
    """Steam cylinder, with the real 4 ft : 18.75 in stroke-to-bore proportion."""
    base_z = 2.8
    parts.append(cyl("SteamCylinder", CYLINDER_DIAMETER / 2, CYLINDER_HEIGHT, CYLINDER_X, 0.0, base_z + CYLINDER_HEIGHT / 2))
    parts.append(cyl("CylinderTopFlange", CYLINDER_DIAMETER / 2 + 0.7, 1.0, CYLINDER_X, 0.0, base_z + CYLINDER_HEIGHT))
    parts.append(cyl("CylinderBaseFlange", CYLINDER_DIAMETER / 2 + 0.7, 1.0, CYLINDER_X, 0.0, base_z))
    parts.append(cyl("PistonRod", 0.55, BEAM_Z - (base_z + CYLINDER_HEIGHT), CYLINDER_X, 0.0, (base_z + CYLINDER_HEIGHT + BEAM_Z) / 2))

    # Parallel motion: Watt's linkage, which keeps the piston rod travelling in a
    # straight line while the beam end swings on an arc. It has to READ as a
    # closed parallelogram hung under the beam end -- the first pass placed two
    # angled bars that touched nothing and looked like damage.
    top_z = BEAM_Z - 1.2
    bot_z = BEAM_Z - 8.0
    outer_x = CYLINDER_X - 4.6
    for z in (top_z, bot_z):
        parts.append(box("ParallelMotionLink", abs(CYLINDER_X - outer_x), 0.55, 0.55, (CYLINDER_X + outer_x) / 2, 0.0, z))
    parts.append(box("ParallelMotionBar", 0.6, 0.6, top_z - bot_z, outer_x, 0.0, (top_z + bot_z) / 2))
    # Radius rod back to its fixed pivot on the entablature.
    parts.append(
        box("RadiusRod", 7.4, 0.5, 0.5, outer_x + 3.4, 0.0, bot_z + 1.6, rot=(0.0, math.radians(-14.0), 0.0))
    )


def build_sun_and_planet(parts) -> None:
    """Flywheel driven by sun-and-planet gearing.

    Murdoch's mechanism, patented by Watt in 1781 to avoid the crank patent, and
    the reason this engine matters historically. The planet wheel is fixed to
    the connecting rod and rolls around the sun wheel on the flywheel shaft, so
    the flywheel turns twice per beam stroke.
    """
    shaft_z = FLYWHEEL_DIAMETER / 2 + 3.0

    parts.append(cyl("FlywheelShaft", 0.9, TOTAL_WIDTH * 0.30, FLYWHEEL_X, 0.0, shaft_z, rot=(math.radians(90.0), 0.0, 0.0)))
    parts.append(torus("FlywheelRim", FLYWHEEL_DIAMETER / 2, 1.15, FLYWHEEL_X, TOTAL_WIDTH * 0.13, shaft_z, rot=(math.radians(90.0), 0.0, 0.0)))
    parts.append(cyl("FlywheelHub", 1.9, 1.4, FLYWHEEL_X, TOTAL_WIDTH * 0.13, shaft_z, rot=(math.radians(90.0), 0.0, 0.0)))
    for i in range(6):
        a = math.radians(i * 60.0)
        parts.append(
            box(
                "FlywheelSpoke", FLYWHEEL_DIAMETER * 0.46, 0.55, 0.55,
                FLYWHEEL_X, TOTAL_WIDTH * 0.13, shaft_z,
                rot=(0.0, a, 0.0),
            )
        )

    # Sun wheel on the shaft, planet wheel on the connecting rod beside it.
    parts.append(cyl("SunWheel", 2.6, 1.0, FLYWHEEL_X, TOTAL_WIDTH * 0.05, shaft_z, rot=(math.radians(90.0), 0.0, 0.0)))
    parts.append(cyl("PlanetWheel", 2.6, 1.0, FLYWHEEL_X, TOTAL_WIDTH * 0.02, shaft_z + 5.2, rot=(math.radians(90.0), 0.0, 0.0)))
    parts.append(
        box("ConnectingRod", 0.75, 0.75, BEAM_Z - shaft_z - 5.2, FLYWHEEL_X, TOTAL_WIDTH * 0.02, (BEAM_Z + shaft_z + 5.2) / 2)
    )


def build_condenser_and_governor(parts) -> None:
    """Condenser and air pump -- Watt's separate condenser is the invention the
    whole engine family rests on -- plus the centrifugal governor."""
    # Kept inboard of the cylinder rather than standing off it: the real engine
    # sinks the condenser in a cistern beside the cylinder, and hanging it
    # further out was what pushed the first run past the collision shell.
    parts.append(cyl("Condenser", 2.6, 9.0, CYLINDER_X - 4.5, BED_DEPTH * 0.18, 7.0))
    parts.append(cyl("AirPump", 1.7, 7.0, CYLINDER_X - 4.5, -BED_DEPTH * 0.18, 6.0))

    # Stood in front of the columns and belt height from the flywheel shaft --
    # which is where it was actually driven from. Behind the frame it was hidden,
    # and the balls read as two beads floating in the structure.
    gov_x = -3.0
    gov_y = -BED_DEPTH * 0.40
    gov_z = 15.0
    parts.append(cyl("GovernorPedestal", 1.1, 12.0, gov_x, gov_y, gov_z - 5.0))
    parts.append(cyl("GovernorSpindle", 0.5, 9.0, gov_x, gov_y, gov_z + 4.0))
    for sx in (-1.0, 1.0):
        parts.append(
            box("GovernorArm", 5.0, 0.4, 0.4, gov_x + sx * 2.1, gov_y, gov_z + 6.4, rot=(0.0, math.radians(38.0 * sx), 0.0))
        )
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, segments=14, ring_count=10, location=(gov_x + sx * 4.1, gov_y, gov_z + 4.6))
        b = bpy.context.active_object
        b.name = "GovernorBall"
        parts.append(b)


def build() -> None:
    clear_scene()
    parts: list = []
    build_bedplate(parts)
    build_entablature(parts)
    build_beam(parts)
    build_cylinder(parts)
    build_sun_and_planet(parts)
    build_condenser_and_governor(parts)

    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    merged = bpy.context.active_object
    merged.name = "SteamEngine"
    # The importer names the MeshPart from the mesh DATA, not the object.
    merged.data.name = "SteamEngine"
    # join() inherits parts[0]'s transform; bake it so local space matches world
    # and `dimensions` reports the axes it claims to.
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    merged.location = (0.0, 0.0, 0.0)


def report(obj) -> None:
    mesh = obj.data
    tris = sum(max(len(p.vertices) - 2, 0) for p in mesh.polygons)
    d = obj.dimensions

    print(f"GEN_OBJECT {obj.name}")
    print(f"GEN_TRIANGLES {tris}")
    print(f"GEN_VERTICES {len(mesh.vertices)}")
    print(f"GEN_SIZE_STUDS {d.x:.2f} x {d.y:.2f} x {d.z:.2f}")
    print(f"GEN_CYLINDER_ASPECT {CYLINDER_ASPECT:.3f} (real stroke 1219mm / bore 476mm)")

    if tris > 20000:
        raise SystemExit(f"FAIL: {tris} triangles exceeds the 20000 per-mesh importer cap")

    # Assert against the COLLISION SHELL, not the exhibit extents. The exhibit is
    # 70 studs across but only the shell is solid, so a mesh that clears the
    # extents and overhangs the shell is geometry players walk through. The first
    # run did exactly that -- 54.66 wide against a 43.20 shell -- and passed.
    if d.z > ENVELOPE_HEIGHT:
        raise SystemExit(f"FAIL: height {d.z:.2f} exceeds the {ENVELOPE_HEIGHT:.2f} stud envelope")
    if d.x > SHELL_WIDTH:
        raise SystemExit(f"FAIL: width {d.x:.2f} overhangs the {SHELL_WIDTH:.2f} stud collision shell")
    if d.y > SHELL_DEPTH:
        raise SystemExit(f"FAIL: depth {d.y:.2f} overhangs the {SHELL_DEPTH:.2f} stud collision shell")

    print(f"GEN_SHELL_MARGIN {SHELL_WIDTH - d.x:.2f} x {SHELL_DEPTH - d.y:.2f} studs")
    print("GEN_BUDGET_OK yes")
    print("GEN_ENVELOPE_OK yes")


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
    bpy.ops.export_scene.gltf(filepath=out_path, export_format="GLB", use_selection=False, export_apply=True)
    print(f"GEN_WROTE {out_path}")


if __name__ == "__main__":
    main()
