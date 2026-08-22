"""Parameterised character pipeline.

blender --background --python rig_pipeline.py -- <src.glb> <out.glb> <rigged|static> <attackClipName>

b321: re-run of the b316/b318 exports with the texture left at its native 2048 and the JPEG
quality raised. The first pass shrank base colour to 1024 at quality 85 to keep the file small,
which is exactly why faces went soft next to Meiya - she never went through that step and kept
her full 2048 sheet. Tri budget also raised 16k -> 20k to match hers.
"""
import bpy, math, json, mathutils, os, sys

argv = sys.argv[sys.argv.index("--")+1:]
SRC, OUT, MODE = argv[0], argv[1], argv[2]
ATTACK = argv[3] if len(argv) > 3 else "SwordSlash"

TARGET_TRIS = 20000
TEX_MAX = 2048          # leave native 2048 alone
IMG_QUALITY = 97

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)

obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')

polys_before = len(obj.data.polygons)
ratio = min(1.0, TARGET_TRIS / max(1, polys_before))
mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
mod.ratio = ratio
bpy.ops.object.modifier_apply(modifier=mod.name)
polys_after = len(obj.data.polygons)

bone_count = 0
unweighted = None

if MODE == 'rigged':
    minv = mathutils.Vector((1e9,1e9,1e9)); maxv = mathutils.Vector((-1e9,-1e9,-1e9))
    for corner in obj.bound_box:
        wc = obj.matrix_world @ mathutils.Vector(corner)
        minv.x=min(minv.x,wc.x); minv.y=min(minv.y,wc.y); minv.z=min(minv.z,wc.z)
        maxv.x=max(maxv.x,wc.x); maxv.y=max(maxv.y,wc.y); maxv.z=max(maxv.z,wc.z)
    H = maxv.z - minv.z; BASEZ = minv.z; CX = (minv.x+maxv.x)/2

    hip_h=BASEZ+H*0.500; waist_h=BASEZ+H*0.595; chest_h=BASEZ+H*0.760
    neck_h=BASEZ+H*0.845; head_h=BASEZ+H*0.930; top_h=BASEZ+H*1.000
    knee_h=BASEZ+H*0.270; shoulder_h=BASEZ+H*0.800
    shoulder_x=(maxv.x-minv.x)*0.19; elbow_h=BASEZ+H*0.590
    hand_h=BASEZ+H*0.470; hip_x=(maxv.x-minv.x)*0.11

    bpy.ops.object.armature_add(enter_editmode=True, location=(CX, 0, 0))
    arm_obj = bpy.context.object
    arm_obj.name = "CharArmature"
    eb = arm_obj.data.edit_bones
    eb.remove(eb[0])

    def mkbone(name, head, tail, parent=None, connect=False):
        b = eb.new(name); b.head=head; b.tail=tail
        if parent: b.parent = eb[parent]; b.use_connect = connect
        return b

    mkbone("Bone",(CX,0,BASEZ),(CX,0,hip_h))
    mkbone("Hips",(CX,0,hip_h),(CX,0,waist_h),"Bone")
    mkbone("Abdomen",(CX,0,waist_h),(CX,0,chest_h),"Hips",True)
    mkbone("Torso",(CX,0,chest_h),(CX,0,neck_h),"Abdomen",True)
    mkbone("Neck",(CX,0,neck_h),(CX,0,head_h),"Torso",True)
    mkbone("Head",(CX,0,head_h),(CX,0,top_h),"Neck",True)
    for side, sx in (("L",-1),("R",1)):
        sxv = CX + sx*shoulder_x
        mkbone(f"Shoulder{side}",(CX,0,shoulder_h),(sxv,0,shoulder_h),"Torso")
        mkbone(f"UpperArm{side}",(sxv,0,shoulder_h),(sxv,0,elbow_h),f"Shoulder{side}",True)
        mkbone(f"LowerArm{side}",(sxv,0,elbow_h),(sxv,0,hand_h),f"UpperArm{side}",True)
        mkbone(f"Fist{side}",(sxv,0,hand_h),(sxv,0,hand_h-H*0.06),f"LowerArm{side}",True)
        hxv = CX + sx*hip_x
        mkbone(f"UpperLeg{side}",(hxv,0,hip_h),(hxv,0,knee_h),"Hips")
        mkbone(f"LowerLeg{side}",(hxv,0,knee_h),(hxv,0,BASEZ),f"UpperLeg{side}",True)
        mkbone(f"Foot{side}",(hxv,0,BASEZ),(hxv,0-H*0.11,BASEZ),f"LowerLeg{side}",True)

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = None
    obj.select_set(True); arm_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')

    bone_count = len(arm_obj.data.bones)
    unweighted = sum(1 for v in obj.data.vertices if not any(g.weight>0.001 for g in v.groups))

    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.scene.render.fps = 24
    for pb in arm_obj.pose.bones: pb.rotation_mode = 'XYZ'

    def key(name, frame, deg=(0,0,0), loc=None):
        pb = arm_obj.pose.bones[name]
        pb.rotation_euler = tuple(math.radians(d) for d in deg)
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)
        if loc is not None:
            pb.location = loc; pb.keyframe_insert(data_path="location", frame=frame)

    def new_action(name):
        arm_obj.animation_data_create()
        act = bpy.data.actions.new(name); act.use_fake_user = True
        arm_obj.animation_data.action = act; return act

    def rest_pose(frame):
        for b in arm_obj.pose.bones: key(b.name, frame, (0,0,0))

    new_action("Walk")
    SWING=28; ARMSW=22
    for f, ph in ((1,0.0),(7,0.25),(13,0.5),(19,0.75),(25,1.0)):
        a = math.sin(ph*2*math.pi)*SWING
        key("UpperLegL",f,(a,0,0)); key("UpperLegR",f,(-a,0,0))
        key("LowerLegL",f,(max(0,-a*0.7),0,0)); key("LowerLegR",f,(max(0,a*0.7),0,0))
        key("UpperArmR",f,(a*ARMSW/SWING,0,0)); key("UpperArmL",f,(-a*ARMSW/SWING,0,0))
        key("Hips",f,(0,0,0),loc=(0,0,abs(math.sin(ph*2*math.pi))*0.02))
        key("Abdomen",f,(math.sin(ph*4*math.pi)*3,0,0))

    new_action("Idle")
    for f, ph in ((1,0.0),(25,0.5),(49,1.0)):
        key("Torso",f,(math.sin(ph*2*math.pi)*1.2,0,0))
        key("Head",f,(math.sin(ph*2*math.pi+0.6)*1.5, math.sin(ph*2*math.pi)*2,0))
        key("UpperArmL",f,(1.5+math.sin(ph*2*math.pi)*0.8,0,0))
        key("UpperArmR",f,(1.5+math.sin(ph*2*math.pi+math.pi)*0.8,0,0))

    new_action(ATTACK)
    if ATTACK == "2H_Ranged_Shooting":
        key("UpperArmL",1,(-70,0,10)); key("LowerArmL",1,(0,0,0))
        key("UpperArmR",1,(-40,0,-25)); key("LowerArmR",1,(-90,0,0))
        key("UpperArmL",6,(-75,0,10)); key("LowerArmL",6,(0,0,0))
        key("UpperArmR",6,(-55,0,-35)); key("LowerArmR",6,(-115,0,0))
        key("Abdomen",6,(0,0,6))
        key("UpperArmL",10,(-70,0,10)); key("LowerArmL",10,(0,0,0))
        key("UpperArmR",10,(-20,0,-10)); key("LowerArmR",10,(-30,0,0))
        key("Abdomen",10,(0,0,0))
        key("UpperArmL",14,(-70,0,10)); key("LowerArmL",14,(0,0,0))
        key("UpperArmR",14,(-40,0,-25)); key("LowerArmR",14,(-90,0,0))
    else:
        key("UpperArmR",1,(-25,0,-8)); key("LowerArmR",1,(-15,0,0))
        key("UpperArmL",1,(-15,0,8));  key("LowerArmL",1,(-10,0,0))
        key("UpperArmR",5,(-25,0,-8)); key("LowerArmR",5,(-15,0,0))
        key("UpperArmL",5,(-15,0,8));  key("LowerArmL",5,(-10,0,0))
        key("UpperArmR",9,(35,0,-4));  key("LowerArmR",9,(5,0,0))
        key("UpperArmL",9,(30,0,4));   key("LowerArmL",9,(5,0,0))
        key("Abdomen",9,(0,0,-6))
        key("UpperArmR",13,(5,0,-6));  key("LowerArmR",13,(0,0,0))
        key("UpperArmL",13,(5,0,6));   key("LowerArmL",13,(0,0,0))
        key("Abdomen",13,(0,0,0))

    new_action("Death")
    rest_pose(1)
    key("Hips",10,(70,0,10),loc=(0,0,-0.35)); key("Abdomen",10,(20,0,0)); key("Torso",10,(15,0,0))
    key("UpperArmL",10,(20,0,-30)); key("UpperArmR",10,(20,0,30))
    key("Hips",20,(85,5,15),loc=(0,0,-0.62)); key("Abdomen",20,(25,0,0)); key("Torso",20,(18,0,0))
    key("UpperArmL",20,(15,0,-40)); key("UpperArmR",20,(15,0,40))

    new_action("Victory")
    for f, ph in ((1,0.0),(13,0.5),(25,1.0)):
        lift = 5+abs(math.sin(ph*2*math.pi))*8
        key("UpperArmL",f,(-140,0,-20-lift)); key("UpperArmR",f,(-140,0,20+lift))
        key("LowerArmL",f,(-20,0,0)); key("LowerArmR",f,(-20,0,0))
        key("Head",f,(0,math.sin(ph*2*math.pi)*4,0))

    arm_obj.animation_data.action = None
    bpy.ops.object.mode_set(mode='OBJECT')

# b326: KEEP THE NORMAL MAP. An earlier pass deleted every map but base colour on the reasoning
# that "this engine never reads them" — which was wrong, and is the single reason Meiya looked
# better than everyone else. She came in by a different route and kept her full PBR set; Bruce,
# the Pikeman, the Rider and Lisa all had theirs stripped, so their faces and armour rendered as
# flat painted colour with no surface relief at all. Every source _pbr.glb ships a 2048 normal
# map and a packed metallic/roughness sheet. Normal and roughness go back in.
# METALLIC stays out on purpose: b320 established that metalness with no environment map turns
# a character into a black silhouette, and liftCharacterTone pins metalness to 0 for exactly
# that reason — a metallic map would be multiplied by zero anyway.
# Colour is what the eye reads letter by letter, so it keeps the full 2048. Relief and gloss are
# low-frequency by nature and survive a smaller sheet perfectly well — and at 2048 apiece three
# maps tripled the download for no visible gain (11.6MB a character against 5.2MB).
MAP_MAX = {'normal': 1024, 'metallic': 512, 'roughness': 512}
for img in bpy.data.images:
    lim = TEX_MAX
    low = img.name.lower()
    for k, v in MAP_MAX.items():
        if k in low:
            lim = min(lim, v)
    if img.size[0] > lim:
        img.scale(lim, lim)

KEEP_INPUTS = {'Base Color', 'Normal', 'Roughness'}
mat = bpy.data.materials.get("model") or next((m for m in bpy.data.materials if m.use_nodes), None)
dropped = []
kept = []
if mat and mat.use_nodes:
    for n in list(mat.node_tree.nodes):
        if n.type != 'TEX_IMAGE' or not n.image:
            continue
        # a texture node can feed the shader directly, or via a Normal Map / channel-split node
        targets = set()
        for l in n.outputs[0].links:
            if l.to_node.type == 'BSDF_PRINCIPLED':
                targets.add(l.to_socket.name)
            else:
                for l2 in l.to_node.outputs[0].links if l.to_node.outputs else []:
                    if l2.to_node.type == 'BSDF_PRINCIPLED':
                        targets.add(l2.to_socket.name)
                # a Separate Color feeding Roughness/Metallic from one packed sheet
                for out in l.to_node.outputs:
                    for l3 in out.links:
                        if l3.to_node.type == 'BSDF_PRINCIPLED':
                            targets.add(l3.to_socket.name)
        if targets & KEEP_INPUTS:
            kept.append([n.image.name, list(n.image.size), sorted(targets)])
        else:
            dropped.append([n.image.name, sorted(targets)])
            mat.node_tree.nodes.remove(n)

bpy.ops.export_scene.gltf(
    filepath=OUT, export_format='GLB',
    export_animations=(MODE == 'rigged'), export_animation_mode='ACTIONS',
    export_force_sampling=True, export_frame_range=False,
    export_apply=True, export_skins=(MODE == 'rigged'), export_all_influences=False,
    export_yup=True, export_image_quality=IMG_QUALITY,
    export_tangents=True,          # a normal map without tangents is a normal map three.js has to guess at
)

print("REPORT_JSON_START")
print(json.dumps({
    "src": os.path.basename(SRC), "mode": MODE, "attack": ATTACK,
    "polys_before": polys_before, "polys_after": polys_after,
    "bone_count": bone_count, "verts_unweighted": unweighted,
    "kept_map": kept, "dropped_maps": dropped,
    "exported_bytes": os.path.getsize(OUT),
}, indent=2))
print("REPORT_JSON_END")
