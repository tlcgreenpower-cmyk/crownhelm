"""What colour is a model actually carrying?

blender --background --python matsurvey.py -- <files...>

The history pack renders as blank white dolls in-game and the survey says "no texture". That is
only half a diagnosis: a low-poly model can carry its colour in per-material base colours or in
vertex colours instead, and either would look perfectly right in this game's style. This prints
which of the three it is, so the decision to bin a model is made on evidence.
"""
import bpy, sys, os

for p in sys.argv[sys.argv.index("--")+1:]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.import_scene.gltf(filepath=p)
    except Exception as e:
        print("FILE", os.path.basename(p), "IMPORT-FAIL", e); continue
    tris = 0; vcol = set(); meshes = 0
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        meshes += 1
        o.data.calc_loop_triangles(); tris += len(o.data.loop_triangles)
        for a in o.data.color_attributes: vcol.add(a.name)
    cols = []
    for m in bpy.data.materials:
        c = None
        if m.use_nodes:
            for n in m.node_tree.nodes:
                if n.type == 'BSDF_PRINCIPLED':
                    bc = n.inputs.get('Base Color')
                    if bc and not bc.is_linked:
                        v = bc.default_value
                        c = "#%02x%02x%02x" % (int(v[0]*255), int(v[1]*255), int(v[2]*255))
                    elif bc and bc.is_linked:
                        c = "TEX:" + bc.links[0].from_node.type
        cols.append("%s=%s" % (m.name[:22], c))
    print("FILE", os.path.basename(p))
    print("   tris", tris, "meshes", meshes, "vertexcolours", sorted(vcol) or "NONE")
    print("   materials(%d)" % len(cols), "; ".join(cols[:14]))
