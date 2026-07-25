"""Renders an orthographic preview of an exported exhibit GLB, so it can be
looked at rather than merely measured.

    blender --background --factory-startup --python art/tools/preview.py \
        -- --glb <in.glb> --out <out.png> [--axis front|side]

This exists because generator asserts check dimensions, triangle counts and
envelope fit -- and every one of those can pass on an object that is visibly
wrong. It has already caught a parallel-motion linkage attached to nothing, a
governor buried behind its own frame, an accretion disk shaped like a funnel,
and a photon ring lying flat. None of those were expressible as an assert.

Imports the EXPORTED file, not the live scene, so it also verifies the export
survived the round trip.
"""
import sys
import math
import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
glb = argv[argv.index("--glb") + 1]
out = argv[argv.index("--out") + 1]
axis = argv[argv.index("--axis") + 1] if "--axis" in argv else "front"

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=glb)

objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
lo = [min(( o.matrix_world @ v.co)[i] for o in objs for v in o.data.vertices) for i in range(3)]
hi = [max(( o.matrix_world @ v.co)[i] for o in objs for v in o.data.vertices) for i in range(3)]
ctr = [(lo[i] + hi[i]) / 2 for i in range(3)]
span = max(hi[i] - lo[i] for i in range(3))

bpy.ops.object.camera_add()
cam = bpy.context.active_object
cam.data.type = "ORTHO"
cam.data.ortho_scale = span * 1.15
if axis == "front":
    cam.location = (ctr[0], ctr[1] - span * 3, ctr[2])
    cam.rotation_euler = (math.radians(90), 0, 0)
else:
    cam.location = (ctr[0] + span * 3, ctr[1], ctr[2])
    cam.rotation_euler = (math.radians(90), 0, math.radians(90))
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type="SUN", location=(ctr[0] - span, ctr[1] - span * 2, ctr[2] + span))
bpy.context.active_object.data.energy = 4.0
bpy.ops.object.light_add(type="SUN", location=(ctr[0] + span, ctr[1] - span, ctr[2]))
bpy.context.active_object.data.energy = 2.0

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.show_cavity = True
sc.render.resolution_x = 900
sc.render.resolution_y = 900
sc.render.film_transparent = False
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print(f"PREVIEW_WROTE {out}")
