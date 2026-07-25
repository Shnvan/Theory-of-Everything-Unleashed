"""Generates the black-hole accretion-disk visualisation exhibit meshes.

Run headless from the repository root:

    blender --background --factory-startup \
        --python art/exhibits/BlackHoleGenerator/generate.py \
        -- --out art/exhibits/BlackHoleGenerator/build/BlackHoleGenerator.glb

Follows NASA Scientific Visualization Studio depictions of a Schwarzschild black
hole with a thin accretion disk, viewed near edge-on.

THIS IS NOT A REPLICA OF AN OBJECT. It is a visualisation of a physical model,
so "accurate" means the physics reads correctly, not that it matches a museum
catalogue entry. The four features that make it a black hole rather than a
glowing hoop:

  1. The black disc is the SHADOW, not the event horizon. Light bending makes
     the horizon appear about 2.6x its true radius, so the dark region a viewer
     sees is much larger than the horizon itself. Frequently conflated; worth
     getting right on an exhibit that exists to teach.
  2. A photon ring hugs the shadow's edge -- light that orbited at least once
     before escaping.
  3. Gravitational lensing bends the disk. The far side's top arcs OVER the
     shadow and its underside arcs UNDER, so the disk is not a flat annulus.
     This is the defining visual and the reason a torus primitive will not do.
  4. Doppler beaming brightens the approaching side. Geometry cannot express
     brightness, so the disk exports as two halves for separate materials.

Unlike the beam engine this exports FOUR objects, giving four MeshParts. The
split is what makes Doppler asymmetry and the black/emissive contrast possible
at all -- it is not a triangle-budget workaround.
"""

import math
import os
import sys

import bpy

# --- envelope -----------------------------------------------------------------

# Exhibit extents 95.09 x 68.00 x 76.08, plinth top Y 8.16, collision shell
# 43.20 x 54.00 x 36.00. As with the beam engine the SHELL binds, not the
# extents: a disk rim overhanging the shell is geometry players walk through.
SHELL_WIDTH = 43.20
SHELL_DEPTH = 36.00
ENVELOPE_HEIGHT = 63.00

STUDS_TO_BLENDER = 1.0

# --- the physics --------------------------------------------------------------

# Apparent shadow radius = sqrt(27)/2 x the Schwarzschild radius, ~2.598.
SHADOW_FACTOR = math.sqrt(27.0) / 2.0

R_SHADOW = 6.5
R_HORIZON = R_SHADOW / SHADOW_FACTOR  # the true horizon, ~2.5 -- reported, not drawn
R_PHOTON = R_SHADOW * 1.045           # the ring sits just outside the shadow edge

# Innermost stable circular orbit, lensed outward. Sits well clear of the
# shadow: the gap between them is where the photon ring reads, and it also sets
# how high the lensed arc rises, since the arc peaks at DISK_INNER * sin(bend).
DISK_INNER = 9.5
DISK_OUTER = 17.5  # set by the collision shell, and disclosed as such
DISK_THICKNESS = 0.32

# Lensing bend. The disk is rotated about the viewing axis by an angle that
# decays with radius: near the shadow it stands past vertical and wraps over the
# top and under the bottom, while the outer rim stays nearly flat.
#
# The falloff must be SHORT. A long falloff tilts every ring a little, and the
# disk becomes a smooth funnel -- which is what the first run produced. In the
# real image the disk is flat almost everywhere and the lensed arc is a narrow
# band hugging the shadow, so the bend has to die off within a few studs.
BEND_MAX_DEG = 112.0
BEND_FALLOFF = 1.25

DISK_TILT_DEG = 9.0  # a few degrees off edge-on, so the disk plane is readable

U_SEGMENTS = 72
V_SEGMENTS = 16


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.objects):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def bend_angle(r: float) -> float:
    """Lensing bend at radius r, in radians. Maximal at the inner edge."""
    return math.radians(BEND_MAX_DEG) * math.exp(-(r - DISK_INNER) / BEND_FALLOFF)


def warped_disk(name: str, u_start: float, u_end: float):
    """Builds half the lensed accretion disk as a warped grid.

    A flat annulus is swept, then each ring of it is rotated about the X axis
    (the viewing axis) by `bend_angle(r)`. Because the rotation is applied to
    y = r*sin(u), the far half (y > 0) lifts above the shadow and the near half
    (y < 0) drops below it, continuously and with no seam at y = 0. That is the
    arc-over-the-top signature, produced by construction rather than sculpted.
    """
    verts = []
    for i in range(U_SEGMENTS + 1):
        u = u_start + (u_end - u_start) * i / U_SEGMENTS
        for j in range(V_SEGMENTS + 1):
            # Radial samples bunched toward the inner edge, because that is where
            # the bend lives. Spacing them evenly spends resolution on the flat
            # outer disk and renders the arc as facets.
            t = (j / V_SEGMENTS) ** 2.0
            r = DISK_INNER + (DISK_OUTER - DISK_INNER) * t
            beta = bend_angle(r)
            x = r * math.cos(u)
            y_flat = r * math.sin(u)
            verts.append((x, y_flat * math.cos(beta), y_flat * math.sin(beta)))

    faces = []
    stride = V_SEGMENTS + 1
    for i in range(U_SEGMENTS):
        for j in range(V_SEGMENTS):
            a = i * stride + j
            faces.append((a, a + stride, a + stride + 1, a + 1))

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    # Give the surface thickness so it is not invisible edge-on or from behind.
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new("Solidify", "SOLIDIFY")
    mod.thickness = DISK_THICKNESS
    mod.offset = 0.0
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return obj


def build_shadow():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R_SHADOW, segments=32, ring_count=18, location=(0, 0, 0))
    o = bpy.context.active_object
    o.name = "BlackHole_Shadow"
    bpy.ops.object.shade_smooth()
    return o


def build_photon_ring():
    """Bright ring just outside the shadow.

    Oriented to face the exhibit's primary approach direction. The photon ring
    is a projection effect -- in reality it always faces the observer -- so a
    fixed ring only reads correctly from the front. That limitation is real and
    the dossier states it rather than papering over it.
    """
    bpy.ops.mesh.primitive_torus_add(
        major_radius=R_PHOTON, minor_radius=0.16,
        major_segments=84, minor_segments=6,
        location=(0, 0, 0), rotation=(math.radians(90.0), 0.0, 0.0),
    )
    o = bpy.context.active_object
    o.name = "BlackHole_PhotonRing"
    bpy.ops.object.shade_smooth()
    # Bake the 90 degree orientation into mesh data. Leaving it on the object
    # let a later blanket rotation_euler assignment overwrite it, which laid the
    # ring flat -- it read as a belt around the shadow's waist instead of a ring
    # outlining its edge.
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    return o


def build() -> list:
    clear_scene()

    # Approaching side is where orbital velocity points at the viewer. With the
    # viewer down -Y and the disk turning about Z, that is cos(u) < 0: the x < 0
    # half. It exports separately so it can carry the brighter material.
    approaching = warped_disk("BlackHole_DiskApproaching", math.pi / 2, 3 * math.pi / 2)
    receding = warped_disk("BlackHole_DiskReceding", -math.pi / 2, math.pi / 2)
    objs = [build_shadow(), build_photon_ring(), approaching, receding]

    for o in objs:
        # The importer names each MeshPart from the mesh DATA, not the object.
        o.data.name = o.name
        o.rotation_euler = (math.radians(DISK_TILT_DEG), 0.0, 0.0)

    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    return objs


def report(objs) -> None:
    total_tris = 0
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3

    for o in objs:
        tris = sum(max(len(p.vertices) - 2, 0) for p in o.data.polygons)
        total_tris += tris
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
    print(f"GEN_HORIZON_RADIUS {R_HORIZON:.2f} (shadow {R_SHADOW:.2f} = {SHADOW_FACTOR:.3f}x)")

    # The lensing arc must actually clear the shadow, or the disk is just a
    # tilted annulus and the exhibit teaches nothing. Assert it rather than
    # trusting the bend constants to stay sane through future edits.
    beta_in = bend_angle(DISK_INNER)
    arc_peak = DISK_INNER * math.sin(beta_in)
    if arc_peak <= R_SHADOW:
        raise SystemExit(
            f"FAIL: lensed arc peaks at {arc_peak:.2f}, inside the {R_SHADOW:.2f} shadow -- no visible arc-over"
        )
    print(f"GEN_ARC_PEAK {arc_peak:.2f} vs shadow {R_SHADOW:.2f}")

    if size[2] > ENVELOPE_HEIGHT:
        raise SystemExit(f"FAIL: height {size[2]:.2f} exceeds the {ENVELOPE_HEIGHT:.2f} stud envelope")
    if size[0] > SHELL_WIDTH:
        raise SystemExit(f"FAIL: width {size[0]:.2f} overhangs the {SHELL_WIDTH:.2f} stud collision shell")
    if size[1] > SHELL_DEPTH:
        raise SystemExit(f"FAIL: depth {size[1]:.2f} overhangs the {SHELL_DEPTH:.2f} stud collision shell")

    print(f"GEN_SHELL_MARGIN {SHELL_WIDTH - size[0]:.2f} x {SHELL_DEPTH - size[1]:.2f} studs")
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

    objs = build()
    report(objs)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=out_path, export_format="GLB", use_selection=False, export_apply=True)
    print(f"GEN_WROTE {out_path}")


if __name__ == "__main__":
    main()
