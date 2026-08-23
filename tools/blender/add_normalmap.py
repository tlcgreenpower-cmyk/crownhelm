"""Derive a normal map for a model that shipped without one, and bake it in.

blender --background --python add_normalmap.py -- <in.glb> <out.glb> [strength]

WHY THIS EXISTS
The bought character pack (Knight, Mage, Barbarian, Rogue_Hooded and the pirates) carries a
diffuse texture and nothing else — no normal map at all. That is the exact fault that made every
one of Lee's own characters render as flat painted plastic until b326 put their normal maps back,
and it is why those pack models still look softer than his do.

There is no ground truth to recover here, so this SYNTHESISES one: it reads the diffuse sheet's
luminance as a height field and takes its gradient. That is a lie in the strict sense — dark paint
is not the same thing as a dent — but on stylised low-poly characters the dark parts of the sheet
are overwhelmingly the places the artist drew a crease, a seam, a strap or a shadowed fold, so the
lie lands almost everywhere it matters. Strength is kept deliberately low for that reason.

Verify by rendering before and after and LOOKING, never by trusting the idea.
"""
import bpy, sys, os, math

argv = sys.argv[sys.argv.index("--")+1:]
SRC, OUT = argv[0], argv[1]
STRENGTH = float(argv[2]) if len(argv) > 2 else 1.6
NRM_MAX = 1024          # relief is low-frequency; a smaller sheet is invisible and much lighter

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

# find the diffuse image actually wired to Base Color
diffuse = None
mat = None
for m in bpy.data.materials:
    if not m.use_nodes:
        continue
    for n in m.node_tree.nodes:
        if n.type != 'BSDF_PRINCIPLED':
            continue
        inp = n.inputs.get('Base Color')
        if inp and inp.is_linked and inp.links[0].from_node.type == 'TEX_IMAGE':
            diffuse = inp.links[0].from_node.image
            mat = m
            break
    if diffuse:
        break

if not diffuse:
    print("NO_DIFFUSE"); raise SystemExit
# already has one? then leave it entirely alone
for n in mat.node_tree.nodes:
    if n.type == 'NORMAL_MAP':
        print("ALREADY_HAS_NORMAL"); raise SystemExit

W, H = diffuse.size
px = list(diffuse.pixels)

# downsample the luminance to NRM_MAX so the gradient is taken at the scale we will ship
step = max(1, W // NRM_MAX)
NW, NH = W // step, H // step

lum = [0.0] * (NW * NH)
for y in range(NH):
    sy = y * step
    row = sy * W
    for x in range(NW):
        o = (row + x * step) * 4
        lum[y * NW + x] = 0.2126 * px[o] + 0.7152 * px[o+1] + 0.0722 * px[o+2]

# central-difference gradient -> tangent-space normal, packed to 0..1
out = [0.0] * (NW * NH * 4)
for y in range(NH):
    ym, yp = max(0, y-1), min(NH-1, y+1)
    for x in range(NW):
        xm, xp = max(0, x-1), min(NW-1, x+1)
        dx = (lum[y*NW+xp] - lum[y*NW+xm]) * STRENGTH
        dy = (lum[yp*NW+x] - lum[ym*NW+x]) * STRENGTH
        nx, ny, nz = -dx, -dy, 1.0
        inv = 1.0 / math.sqrt(nx*nx + ny*ny + 1.0)
        o = (y*NW + x) * 4
        out[o]   = nx*inv*0.5 + 0.5
        out[o+1] = ny*inv*0.5 + 0.5
        out[o+2] = nz*inv*0.5 + 0.5
        out[o+3] = 1.0

nrm = bpy.data.images.new("texture_normal_derived", NW, NH, alpha=False, float_buffer=False)
nrm.colorspace_settings.name = 'Non-Color'
nrm.pixels[:] = out
nrm.pack()

nt = mat.node_tree
tex = nt.nodes.new('ShaderNodeTexImage')
tex.image = nrm
tex.image.colorspace_settings.name = 'Non-Color'
nmap = nt.nodes.new('ShaderNodeNormalMap')
nmap.inputs['Strength'].default_value = 1.0
nt.links.new(tex.outputs['Color'], nmap.inputs['Color'])
for n in nt.nodes:
    if n.type == 'BSDF_PRINCIPLED':
        nt.links.new(nmap.outputs['Normal'], n.inputs['Normal'])

bpy.ops.export_scene.gltf(
    filepath=OUT, export_format='GLB',
    export_animations=True, export_animation_mode='ACTIONS',
    export_force_sampling=True, export_frame_range=False,
    export_apply=False, export_skins=True, export_all_influences=False,
    export_yup=True, export_image_quality=92, export_tangents=True,
)
print("DERIVED_NORMAL %dx%d strength %.2f -> %s (%d bytes)" % (NW, NH, STRENGTH, OUT, os.path.getsize(OUT)))

# ---------------------------------------------------------------------------
# RESULT ON THIS PROJECT'S PACK MODELS: NO VISIBLE CHANGE. Do not roll it out.
#
# Tried it on Knight.glb (b343), rendered the mounted Knight before and after at
# identical camera and lighting, and the two frames are indistinguishable.
#
# The reason is worth writing down, because the idea is sound and will look
# tempting again: this technique reads painted luminance as height, and these
# pack models have almost no painted luminance to read. Their detail lives in
# the GEOMETRY — faceted plates, a hard-edged helm, chunky pauldrons — over
# large areas of nearly flat colour. There is nothing in the sheet to take a
# gradient of, so the derived map comes out almost uniformly (0.5, 0.5, 1.0),
# which is exactly "no bump at all".
#
# It would work on a model whose texture carries the detail — Lee's own
# characters do, which is precisely why losing their real normal maps hurt so
# much. Kept for that case, and as a record that this avenue is closed for the
# bought pack: those models need more polygons or a hand-authored map, not a
# derived one.
