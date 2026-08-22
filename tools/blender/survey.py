import bpy, sys, os

argv = sys.argv[sys.argv.index("--")+1:]
paths = argv

for p in paths:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.import_scene.gltf(filepath=p)
    except Exception as e:
        print("FILE", os.path.basename(p), "IMPORT-FAIL", e)
        continue
    tris = 0
    for o in bpy.data.objects:
        if o.type == 'MESH':
            o.data.calc_loop_triangles()
            tris += len(o.data.loop_triangles)
    imgs = []
    for im in bpy.data.images:
        if im.size[0]:
            imgs.append("%s %dx%d" % (im.name, im.size[0], im.size[1]))
    # which principled inputs are actually linked to an image
    slots = set()
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        for n in m.node_tree.nodes:
            if n.type == 'BSDF_PRINCIPLED':
                for inp in n.inputs:
                    if inp.is_linked:
                        src = inp.links[0].from_node
                        # walk one hop through normal-map / separate nodes
                        if src.type == 'TEX_IMAGE':
                            slots.add(inp.name)
                        elif src.type in ('NORMAL_MAP', 'SEPARATE_COLOR', 'SEPRGB'):
                            for i2 in src.inputs:
                                if i2.is_linked and i2.links[0].from_node.type == 'TEX_IMAGE':
                                    slots.add(inp.name)
    print("FILE", os.path.basename(p))
    print("   tris", tris)
    print("   images", imgs)
    print("   textured inputs", sorted(slots))
print("SURVEY-DONE")
