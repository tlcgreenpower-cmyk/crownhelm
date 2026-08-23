"""Give the history pack its colours back, so the game gets seven new distinct soldiers.

blender --background --python recolour_troops.py -- <outdir>

WHY THIS EXISTS
The nine history-pack characters (Soldier, BlueSoldier, Knight, GoldKnight, Viking, Ninja,
Kimono, the two Workers) have been in the asset folder since the start and every attempt to use
them has ended the same way: the owner reports "a blank white doll". b327 concluded they were
untextured and moved every combat unit off them.

Untextured was only half the diagnosis. They carry no image, but they DO carry named per-material
colours - Skin, Face, Main, Helmet, Armor, Armor_Dark, Detail, Red, Hair, Pants, Band, Clothes -
which is exactly how this game's own low-poly art works and would look perfectly right. The fault
is the VALUES. Read out of the glTF, every one of them is nearly black:

    Soldier_Male   Skin 0.0134  Main (0.063,0.091,0.040)  Black 0.0204   Face 1.0
    Knight_Male    Armor 0.067  Armor_Dark 0.027          Red 0.126      Skin 0.0134
    Ninja_Male     Main 0.008   Details 0.055             Grey 0.067     Face 1.0

Skin and Face are byte-identical across all nine files, and Face is pure white in every one. That
is the signature of a colour-space conversion applied one time too many on export: white survives
it unchanged and everything else is crushed toward black. Put through this engine's b172
black-point lift the body comes up to a flat mid-grey and the face stays at pure white, which is
precisely "a blank white doll".

So the geometry, the rig and the five animation clips are all fine, and only the paint is lost.
This repaints them by material NAME and writes a clean GLB per model. That turns a bin of
unusable assets into seven distinct 2,500-6,300-triangle soldiers - cheap enough to field a
hundred of, and the thing the owner actually asked for: new men for the different units.

PRE-COMPENSATION
Do not read the palette below as raw material values. The engine lifts every character palette
once at load (b172):

    displayed_srgb = CHAR_BLACK + (1 - CHAR_BLACK) * authored_srgb ** CHAR_GAMMA

with CHAR_BLACK 0.26 and CHAR_GAMMA 0.78. Authoring the colour you want gets you something much
paler than you wanted. So the palette here is written as the colour the unit should APPEAR on the
field, and every channel is put through the inverse of that lift before it is stored. Change the
two constants here if they ever change in the game and the palette keeps meaning what it says.
"""
import bpy, sys, os, math

OUT = (sys.argv[sys.argv.index("--")+1:] or ["assets/troops"])[0]
SRC = "assets/history/glTF"
CHAR_BLACK, CHAR_GAMMA = 0.26, 0.78

def srgb2lin(c):
    return 0.0 if c <= 0 else (1.0 if c >= 1 else (c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4))

def unlift(t):
    """The authored sRGB value that the engine's b172 lift will raise to `t`."""
    if t <= CHAR_BLACK:
        return 0.0
    return min(1.0, ((t - CHAR_BLACK) / (1.0 - CHAR_BLACK)) ** (1.0 / CHAR_GAMMA))

def factor(hexstr):
    """#rrggbb, meaning the colour as it should APPEAR in game -> linear baseColorFactor."""
    h = hexstr.lstrip("#")
    return [srgb2lin(unlift(int(h[i:i+2], 16) / 255.0)) for i in (0, 2, 4)] + [1.0]

WHICH_PART_IS_WHICH = """
The material names in this pack do NOT mean what they say, so nothing below is guessed. Every
material in every model was set to a distinct vivid hue, the models were reloaded into the running
game and each unit was photographed, and the parts were read off the pictures:

  Soldier / BlueSoldier   Black  = the COAT BODY (the biggest surface on the man)
                          Main   = sleeves, shoulders and belt
                          DarkGreen / Grey = the trousers
                          Helmet = the bowl over the head — cap or hair, it reads as either
                          Skin   = face, hands, forearms, lower legs
  Knight / GoldKnight     Armor  = nearly the whole suit;  Armor_Dark = helm detail
                          Red    = the helmet plume;       Detail = the belt
  Viking                  Skin   = head AND bare torso AND arms (he is a bare-armed raider)
                          Pants  = trousers;  Main = belt and shoulder strap;  Hair = hair+beard
  Ninja                   Main   = the whole suit and hood;  Details = sash and straps
                          Grey   = the shoulder strap
  Samurai                 Clothes = the whole kimono;  Band = headband and obi;  Skin = head+hands

And the one that matters most: **Face is the narrow band across the EYES, not the face.** It is
pure white in all nine source files, which is why these men read as blank-faced dolls — a white
slot where the eyes should be, on a body the lift had flattened to grey. Painting it dark is what
gives every one of them a face.

One floor to know about: the b172 lift maps everything to CHAR_BLACK + (1-CHAR_BLACK)*x**GAMMA,
so nothing can appear darker than 0.26 however black it is authored. Deep black comes out as a
dark grey by design; do not chase it.
"""

SKIN = "#b08258"          # face, hands and forearms — one tone across the whole roster
EYES = "#2b211b"          # the eye band. Lands at the 0.26 floor, which is exactly right for eyes

# Each entry: source file -> (output name, {material name: colour as it should APPEAR}).
# A material the source has and this table does not is left exactly as it was.
JOBS = {
    # the line infantryman: red coat, buff breeches, black shako
    "Soldier_Male":       ("Soldier", {
        "Skin": SKIN, "Face": EYES, "Black": "#8e3630", "Main": "#6d5638",
        "DarkGreen": "#c3ae87", "Helmet": "#332c24"}),
    # the grenadier: blue coat with brass lace, buff breeches, near-black bearskin
    "BlueSoldier_Male":   ("BlueSoldier", {
        "Skin": SKIN, "Face": EYES, "Black": "#33508f", "Main": "#b39a4f",
        "Grey": "#c3ae87", "Helmet": "#1f1c19"}),
    # the heavy spearman: plain steel, leather belt, a red plume
    "Knight_Male":        ("KnightM", {
        "Skin": SKIN, "Armor": "#a3acb6", "Armor_Dark": "#5f6771",
        "Detail": "#6f4c2d", "Red": "#8d2f2a"}),
    # the household guard: the same plate in the game's gold
    "Knight_Golden_Male": ("GoldKnight", {
        "Skin": SKIN, "Armor": "#c9a44a", "Armor_Dark": "#7e6529",
        "Detail": "#4c3c22", "Red": "#8d2f2a"}),
    # the raider: bare arms, leather trousers, a red beard
    "Viking_Male":        ("Viking", {
        "Skin": SKIN, "Face": EYES, "Pants": "#5a4632", "Main": "#3d3228",
        "Light": "#c5b393", "Hair": "#a85f2a"}),
    # the crossbowman: dark green suit and hood with a red sash
    "Ninja_Male":         ("Ninja", {
        "Skin": SKIN, "Face": EYES, "Main": "#2e3c30", "Details": "#8d2f2a",
        "Grey": "#55575c"}),
    # the swordsman: indigo kimono, red obi
    "Kimono_Male":        ("Samurai", {
        "Skin": SKIN, "Face": EYES, "Clothes": "#3b4b70", "Band": "#8d2f2a"}),
}

os.makedirs(OUT, exist_ok=True)
for src, (name, palette) in JOBS.items():
    path = os.path.join(SRC, src + ".gltf")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.import_scene.gltf(filepath=path)
    except Exception as e:
        print("SKIP", src, e)
        continue
    hit, miss = [], []
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        want = palette.get(m.name)
        for n in m.node_tree.nodes:
            if n.type != 'BSDF_PRINCIPLED':
                continue
            if want:
                n.inputs['Base Color'].default_value = factor(want)
                # b320's rule: no metalness without an environment map, or the man goes black
                if 'Metallic' in n.inputs:
                    n.inputs['Metallic'].default_value = 0.0
                if 'Roughness' in n.inputs:
                    n.inputs['Roughness'].default_value = 0.72
                hit.append(m.name)
            else:
                miss.append(m.name)
    dst = os.path.join(OUT, name + ".glb")
    bpy.ops.export_scene.gltf(
        filepath=dst, export_format='GLB',
        export_animations=True, export_animation_mode='ACTIONS',
        export_force_sampling=True, export_frame_range=False,
        export_apply=False, export_skins=True, export_all_influences=False,
        export_yup=True)
    clips = len(bpy.data.actions)
    print("WROTE %-14s repainted %-52s untouched %-22s clips %d  %d bytes"
          % (name, ",".join(hit), ",".join(miss) or "-", clips, os.path.getsize(dst)))
