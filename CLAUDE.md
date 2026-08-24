# Crownhelm — Lee's personal 3D RTS

Single-file Three.js game: `Crownhelm3D.html`. OPEN-WORLD since 2026-07-27 — the tide mechanic
was REMOVED and must never come back. Big roamable map, 3 AI realms, diplomacy (gift/war/peace),
musket-era factions. Source art in source-art/, assets in assets/.
Keep building — this is the owner's fun project; bold ideas welcome, tide stays dead.

## Practicals (Lee's Windows PC)

No Python and no Node. Serve with `tools/serve-8137.ps1` (PowerShell HttpListener, no-cache
headers, `.glb` MIME). `index.html` is a deploy MIRROR of `Crownhelm3D.html` — copy before every
commit. Push to origin main works from this machine.

## Testing without a visible browser

The browser pane does not composite, so `requestAnimationFrame` never fires and normal
screenshots time out. Drive and photograph it instead:

- `window.TF._dbg()` fills `window.__D` with the internals. Then `__D.update(1/30)` steps the
  simulation and `__D.frame(1/30)` steps everything living on the render side (animation, LOD,
  parapets, the King's legs, herds). **Both** are needed; `update` alone misses half the game.
- `window.TFshot({x,z,dist,pitch,yaw,w,h,q})` renders offscreen and returns a JPEG data URL.
  POST it to `tools/shotsink.ps1` on port 8139 — the FILE NAME is the URL path and the raw data
  URL is the whole body (`fetch('http://localhost:8139/myshot',{method:'POST',body:dataUrl})`),
  not JSON. **pitch and yaw are RADIANS.** Passing degrees puts the camera at a random angle,
  usually underground, and you get a picture of the sky full of black silhouettes — that is the
  underside of the terrain, not a bug. Useful values: `pitch:0.6, dist:40` for a gameplay view,
  `pitch:0.2, dist:4.5` for one character.
- Buildings carry `cx`/`cz` (world) and `tx`/`ty` (tile); units carry `x`/`z`. A check written
  against `b.x` silently compares `undefined` and passes every time.
- `window.TF.info` for fps/ents/skinned/calls; `window._CHARLIB` for character templates;
  `renderer.info.render` after a TFshot for real draw calls and triangles.
- **A unit photographed away from the camera shows its BIND POSE, not its animation.** TFshot
  renders from its own throwaway camera, but `updateUnitLOD` decides who gets skinned using the
  REAL one — off-screen men are deliberately never animated. So a unit posed for a photograph is
  frozen at frame 0, which on these rigs is a T-pose, and it looks exactly like a broken model.
  Drive it by hand before the shot: `for(let k=0;k<40;k++)e.mesh.userData.mixer.update(1/30)`.

**The hands-off soak only ever tests the AI.** Spinning up a game and stepping it for twenty
minutes exercises `realmBrain` and nothing the PLAYER does — which is the half the owner actually
operates, and where b351's ReferenceError hid for twenty-five builds. `tools/uisweep.js` pastes
into the console and clicks every command button, stance, panel, diplomacy action and menu item,
round-trips all four win modes through save/load, and (b355) drives REAL POINTER ORDERS on the 3D
view — projecting a world point back to client coordinates and firing genuine MouseEvents, so
select, move, gather, attack, box-select, build placement and the rally flag all go through the
same `localXY` → `raycastGround` → `commandMove` path a hand does. Each asserts the order actually
landed. ~225 interactions. Run it before calling a UI change done. Still NOT covered: the Map
Builder, Parade mode, wall dragging, camera orbit/pan.

Two things it has caught being written wrongly, both in the sweep rather than the game: hardcoding
`r1/r2/r3` (a three-realm game has no r3) and asserting `cmd==='gather'` after a gather order (by
the time you look he may already be `'return'`, which means it worked).

Two containers, and this catches people out: a soldier's commands live in `#formBar` and its
`#cmds` is empty. A worker is the other way round. Neither is a bug.

**Numbers can agree while the picture disagrees, and the picture is right.** But looking is not
enough on its own either — when characters "look bad", SURVEY the assets (`tools/blender/survey.py`)
before touching lights or materials. Three separate rounds of that complaint turned out to be
different unit types still pointing at untextured 2,500-tri models, and every render was a
faithful picture of a bad asset.

## Character pipeline

`tools/blender/rig_pipeline.py`, run through Blender's own Python (there is no other). Two rules
in it are worth the look of the whole game: **keep the normal map** (dropping it is what made
every character but Meiya render as flat plastic) and **leave metallic out** (metalness with no
environment map turns a character black — b320). Bone weighting must be `ARMATURE_ENVELOPE`;
these generated meshes are thousands of disconnected shards and bone-heat weights zero verts.

b92 merged every character to ONE skinned mesh at load (colours baked to vertex colours) — keep
new models going through `mergeSkinnedModel` / `mergeStaticModel`.

### The roster, and the trap in it

Three tiers: Lee's own five (LeeRider, LeePikeman, BruceBowman, Lisa, Meiya — 20k tris, real PBR
maps), the bought packs (Barbarian/Knight/Mage/Rogue_Hooded/Privateer and the pirates — 6-15k,
one colour atlas), and the **history pack**, which carries no image at all and paints from named
per-material colours instead. It was written off twice as "untextured"; it is not broken, its
colour VALUES were crushed to near-black on export while `Face` stayed pure white, which is the
blank-white-doll look reported three times. `tools/blender/recolour_troops.py` repaints them into
`assets/troops/` and they are now the infantry, grenadier, hoplite, Chu-Ko-Nu, viking and samurai.
Two things to know before touching it:

- **`Face` is the narrow band across the EYES, not the face.** Paint it dark or the man has none.
- **Nothing can appear darker than `CHAR_BLACK` (0.26).** `liftCharacterTone` maps every character
  palette through `0.26 + 0.74*x**0.78` at load, so the script authors the INVERSE of that lift
  and its palette means "how this should look on the field". Don't chase true black.

Material names lie about which part they paint (`Black` is the coat body; `Helmet` is the hair).
The mapping is written out at the top of the recolour script — it was read off debug renders with
every material set to a different hue, not guessed.

## Systems worth knowing before you change things

Twelve borrowed mechanics went in over b326–b330 and they touch a lot:

- **Popularity** (`mood`) — 0-100 per realm off food variety, the tax dial, entertainment,
  crowding and war; drives worker immigration and emigration. Top bar meter, tax at the Keep.
- **Borders** (`territoryAt`, `BORDER_R`) — claims radiate from Keeps, Castles, Forts and towers.
  You cannot build inside a rival's; buildings on hostile ground take 3× damage (`bldExposure`).
- **Attrition** — a fraction of max HP per second in hostile territory, floored at 20%, cancelled
  by a Caravan in the column.
- **Regiments** (`regiments`, `regOf`, `regBonus`) — 8+ under an officer; Stand Ground entrenches
  them and then they refuse move orders at the door in `commandMove`.
- **Battle order** (`battleOrder`, `classOf`) — the player sets who stands in the front rank.
  Classify by REACH, not the `ranged` flag: the Skirmisher has range 17 and no flag.
- **Treasures / trade road** (`treasures`, `tradeSites`) — placed in `newGame` after the keeps,
  saved and restored explicitly.
- **Downed commanders** — heroes go to `downed` instead of dying; only the capture timer finishes
  them. The death filter in `update` must keep letting them through.

**Anything new that holds state must go in `saveGame`/`loadGame`.** Four of these were silently
lost on reload until they were tested; test the round trip, do not assume it.

`placeAI` carries a `BAND` table of which ring each building belongs in — a type missing from it
is silently never sited, however well the rest of the brain works.
