"""Bruce Bowman clean-up.

blender --background --python bruce_fix.py -- <src_rigged.glb> <out.glb> [report|apply]

Two faults the owner reported, both in the SOURCE model rather than the engine:
  1. a bright lipstick-red mouth with a smear beside it, painted into texture_diffuse
  2. a bow modelled as a closed floating hoop, unattached to his hand - and the game already
     gives every archer a proper bow through ARMS/armUnit, so he was carrying two.
"""
import bpy, sys, os, json, math

argv = sys.argv[sys.argv.index("--")+1:]
SRC, OUT = argv[0], argv[1]
MODE = argv[2] if len(argv) > 2 else "report"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
me = obj.data

# ---- island survey: walk the edge graph to find connected components
adj = {}
for e in me.edges:
    a, b = e.vertices
    adj.setdefault(a, []).append(b)
    adj.setdefault(b, []).append(a)

seen = set()
islands = []
for v in range(len(me.vertices)):
    if v in seen:
        continue
    stack, comp = [v], []
    seen.add(v)
    while stack:
        c = stack.pop()
        comp.append(c)
        for n in adj.get(c, []):
            if n not in seen:
                seen.add(n)
                stack.append(n)
    islands.append(comp)

info = []
for i, comp in enumerate(islands):
    xs = [me.vertices[v].co.x for v in comp]
    ys = [me.vertices[v].co.y for v in comp]
    zs = [me.vertices[v].co.z for v in comp]
    info.append({
        "i": i, "verts": len(comp),
        "x": [round(min(xs), 3), round(max(xs), 3)],
        "y": [round(min(ys), 3), round(max(ys), 3)],
        "z": [round(min(zs), 3), round(max(zs), 3)],
    })
info.sort(key=lambda d: -d["verts"])
print("ISLANDS_JSON_START")
print(json.dumps({"count": len(islands), "top": info[:14]}, indent=1))
print("ISLANDS_JSON_END")

# The mesh is thousands of disconnected shards (these generated models always are), so the bow
# cannot be picked out as one island. Find it by SHAPE instead: histogram the vertices across each
# axis and look for the detached lobe sitting off to one side of the body.
if MODE in ("report", "hist"):
    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    zs = [v.co.z for v in me.vertices]
    for nm, arr in (("x", xs), ("y", ys), ("z", zs)):
        lo, hi = min(arr), max(arr)
        B = 24
        bins = [0]*B
        for a in arr:
            k = min(B-1, int((a-lo)/max(1e-9, hi-lo)*B))
            bins[k] += 1
        print("HIST", nm, round(lo, 3), round(hi, 3), bins)
    print("REPORT-ONLY")
    raise SystemExit

# region delete: "xmin,xmax,ymin,ymax,zmin,zmax" — everything inside the box goes
BOX = None
if len(argv) > 4 and argv[4]:
    BOX = [float(t) for t in argv[4].split(",")]

# ---- 1. soften the mouth in texture_diffuse
img = None
for im in bpy.data.images:
    if "diffuse" in im.name.lower() and im.size[0]:
        img = im
        break
touched = 0
if img:
    px = list(img.pixels)
    n = img.size[0] * img.size[1]
    for i in range(n):
        o = i * 4
        r, g, b = px[o], px[o+1], px[o+2]
        # lipstick red: bright, and far redder than it is anything else. Skin never gets here.
        if r > 0.34 and r > g * 1.75 and r > b * 1.65:
            lum = 0.2126*r + 0.7152*g + 0.0722*b
            # a natural lip is a desaturated rose that sits only a little darker than the face
            px[o]   = min(1.0, lum * 1.42 + 0.10)
            px[o+1] = min(1.0, lum * 0.92 + 0.045)
            px[o+2] = min(1.0, lum * 0.86 + 0.045)
            touched += 1
    img.pixels[:] = px
    img.pack()
print("MOUTH_PIXELS", touched)

# ---- 2. delete the floating bow island (passed in as an index list)
if BOX:
    import bmesh
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(me)
    bm.verts.ensure_lookup_table()
    n = 0
    for v in bm.verts:
        c = v.co
        inside = (BOX[0] <= c.x <= BOX[1] and BOX[2] <= c.y <= BOX[3] and BOX[4] <= c.z <= BOX[5])
        v.select = inside
        if inside:
            n += 1
    bmesh.update_edit_mesh(me)
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    print("DELETED_VERTS", n)

bpy.ops.export_scene.gltf(
    filepath=OUT, export_format='GLB',
    export_animations=True, export_animation_mode='ACTIONS',
    export_force_sampling=True, export_frame_range=False,
    export_apply=False, export_skins=True, export_all_influences=False,
    export_yup=True, export_image_quality=97, export_tangents=True,
)
print("WROTE", OUT, os.path.getsize(OUT))
