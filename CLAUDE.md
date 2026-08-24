# Crownhelm — Lee's personal 3D RTS

Single-file Three.js game: `Crownhelm3D.html`. OPEN-WORLD since 2026-07-27 — the tide mechanic
was REMOVED and must never come back. Big roamable map, 3 AI realms, diplomacy (gift/war/peace),
musket-era factions. Source art in source-art/, assets in assets/.
Keep building — this is the owner's fun project; bold ideas welcome, tide stays dead.

## Practicals (Lee's Windows PC)

**Node and Python both exist on this machine** — `node` v24.19.0 with npm 11.17, and `python`
3.13.15 (`py` works too; `python3` hits the Windows Store alias and fails). This file said "No
Python and no Node" for a long time and it is simply out of date, which cost real time: the game is
one 780KB HTML file and `node --check` on an extracted script, or on anything in `tools/`, catches
a syntax slip in a second instead of a browser reload and a blank screen. b363 checked and corrected
it. The PowerShell servers still work and there is no reason to replace them.

Serve with `tools/serve-8137.ps1` (PowerShell HttpListener, no-cache headers, `.glb` MIME).
`index.html` is a deploy MIRROR of `Crownhelm3D.html` — copy before every commit. Push to origin
main works from this machine.

**The browser caches the module script through `location.reload()`.** After editing the game, load
it with a changed query string (`Crownhelm3D.html?bust=1`) or you will spend a while measuring the
build you already replaced.

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
- **The maps are not all the same size, and the biggest are not in the menu.** Heartlands is 96×64;
  the other four are 168×112, three times the area. The **Map Builder** goes further — Large
  224×144 and Epic 256×176 (**7.33×** Heartlands, 45k tiles) with up to **8 realms** against the
  menu's four. Anything sized against "the biggest map" must mean Epic, not Broadwood: b367 found
  every area-scaled ceiling in the game cut to fit 168×112, so on an Epic map treasures, villages,
  relics, herds, sheep and leaves all bind at once and the world arrives at roughly a third of its
  intended density. Epic itself plays fine (1.2–3.0ms a step, 8 realms, save 133KB).
  **Before lifting one of those ceilings, check how the thing is DRAWN** (b368). The falling leaves
  are a single `InstancedMesh` — one draw call at 60 or at 440 — so that ceiling was free to lift.
  The sheep are 3,821 separate meshes at their cap and would be ~14,000 at the count the rule wants,
  so theirs stays. Two of these were mislabelled in b367's own table: `min(120,60*A)` is leaves, not
  sheep; `min(16,8*A)` is sheep flocks, not birds.
  **Render TIME cannot be measured in this harness** — the pane does not composite, and a far TFshot
  clocked 441ms, which is the harness, not the game. Argue render cost from
  `renderer.info.render.calls` and `.triangles`, which are exact and machine-independent. Anything you compare between maps has to be per-tile or it is meaningless.
  `MAP_W`, `MAP_H`, `WORLD_W`, `WORLD_H` and `HALF_W/H` are GETTERS in `_dbg` for this reason
  (b360) — they used to be captured values, frozen at the moment `_dbg()` ran, so a 168×112 map
  still reported 96×64 and every measurement taken after a map change was quietly wrong. It
  produced a confident "the default map has a third the scenery of every other" that was pure
  artefact. If you add a map-dependent value to the debug surface, make it a getter.
- `window.TF.info` for fps/ents/skinned/calls; `window.TF.weather` for the live front (name, cloud,
  fog, mist, rain, sun, wind and seconds to the next change); `window._CHARLIB` for character
  templates; `renderer.info.render` after a TFshot for real draw calls and triangles.
  **Some of the debug surface hangs off `TF` and some off `TF._dbg()`'s `__D`, and they are not the
  same object** — `weather` is on `TF`, so listing `Object.keys(__D)` says it does not exist. Check
  both before concluding a thing cannot be measured (b366 nearly re-derived the weather state by
  hand for want of looking one level up).
- **`setCam` takes (x,z,dist,pitch) and NO yaw** (b375). The real camera — the one `updateUnitLOD`
  reads to decide who gets skinned — therefore keeps whatever yaw it had, which is usually not the
  yaw you pass to TFshot. Every man in your shot but outside the REAL camera's view is left in bind
  pose, so you photograph a field of T-poses and conclude the rig is broken. Read the yaw back off
  the camera and pass THAT to the shot:
  `const yaw=Math.atan2(camera.position.x-camTarget.x, camera.position.z-camTarget.z)`.
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
landed. ~238 interactions. Run it before calling a UI change done. Still NOT covered: wall dragging
and camera orbit/pan. The **Map Builder** round-trip was verified by hand in b367 (it is sound, and
its Epic size is 7.33× Heartlands — see above); **Parade mode** in b369.

**Parade mode places its ranks in TILES, not world units** (b369) — `spawnUnit` takes tile
coordinates and `TILE` is 4, so a spacing that reads like "2" on the page is 8 units on the ground.
The game's own formed-up line is **2.0 world units** between neighbours (measured by marching a
company and seeing where it settles), and the widest land unit is the cannon at r=1.7, so 4 units is
the tightest rank that cannot overlap. Anything laying men out by hand should be checked against
those two numbers rather than eyeballed.

Two things it has caught being written wrongly, both in the sweep rather than the game: hardcoding
`r1/r2/r3` (a three-realm game has no r3) and asserting `cmd==='gather'` after a gather order (by
the time you look he may already be `'return'`, which means it worked).

`tools/worldcensus.js` — `await census(5)` counts every world scatter by name across five real
maps and flags any that place nothing. **It audits a saved custom map too (b367)** — build one in
the Map Builder first, or the run silently covers none of the sizes above 168×112 and says so. It exists because of b358: b353 fixed rocks floating over
the sea and in the same line silently took the sea stacks to ZERO, and nothing noticed for a build
because **nothing counts the world's decoration**. A scatter can die and the game still runs,
still soaks clean, still reports no errors — the world just quietly gets emptier.

Two things make counting them possible, and both are easy to undo by accident: each scatter sets
`mesh.name='scatter:<thing>'`, and `chunkGroupInPlace` copies that name onto every piece when it
splits a scatter into a culling grid. **Never read one InstancedMesh's `count`** — a scatter is
tens of chunks, and reading one gave "1 sea stack" when the true figure was 65. Sum by name.

`tools/soak.js` is the other half — `await soak()` runs a long hands-off game and reports whether
entity counts, scene nodes, scene geometry, save size and step time all settle. b356 measured 21.5
minutes: army plateaus at 346, scene nodes and geometry stop growing and tick down again, save
holds at 74KB, step time flat around 2ms, zero errors.

**Give it thirty minutes, not fifteen, and read the army trace before the verdict** (b366). Since
b364 the rivals actually fight, so the army no longer climbs monotonically — a real run reads
24/100/119/181/**117**/175/219/236/236/236, that dip being a war taking sixty-four men off the
board. The settle check looks for the first sample within 95% of peak, so a run cut off mid-rebuild
reports `healthy:false, "army never settled"` when nothing whatever is wrong. Two builds in a row
were nearly mis-reported that way.

**`renderer.info.memory` is not a leak detector here.** It counts what has been UPLOADED to the
GPU, so it only ever rises, and it jumps every time you call **TFshot** — a screenshot renders
parts of the world the play camera never touched. Sampling it alongside screenshots shows a
convincing steady "leak" that is entirely your own measuring; it cost most of a pass before the
penny dropped. The honest figure is the count of distinct geometries reachable from the scene
graph, which falls again when things are disposed. `soak.js` reports both and takes no screenshots.

Two containers, and this catches people out: a soldier's commands live in `#formBar` and its
`#cmds` is empty. A worker is the other way round. Neither is a bug.

**The worker's held tool is NOT the blade on his shoulder** (b375). The worker model has tools,
pouches and a belt knife modelled into the mesh. Hide every `userData.axe`/`pick` in the scene and
re-shoot before blaming the attached prop — that control settles in one render what three passes of
tweaking will not. The attached axe itself is sound: on the `FistR` bone 0.189 out (the designed 0.20
× the rig's 0.947), and of nine grip rotations tried the shipped one puts the blade tip furthest from
the chest. What is still wrong is that the model already carries tools and the attached haft is long
at this scale, so it reads as a second, floating one — an **asset** calibration, not a code one.

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
- **AI-vs-AI wars** (`aiWars`, `warKey`, `aiDiplomacy`) — the value stored against a war key is the
  `elapsed` it was DECLARED at, not `true` (b364), because `aiDiplomacy` rolls to end every war on
  the books every 90–180s and a realm needs ~220s to muster its first host. Without a minimum age
  the rivals declared war, stood still, and made peace before anyone marched — twenty minutes of
  three-way war used to destroy ONE building. It is still always truthy, so `if(aiWars[k])` is
  unaffected; a pre-b364 save holds `true`, which `warAge` reads as "old enough to end".

**Never end a patched line with a `//` comment unless the line really ends there.** Twice in one
day (b370, b372) a comment appended mid-statement swallowed the rest of the line — an object
literal's remaining fields once, a function's closing brace the other time — and the failure
surfaces as `Unexpected end of input` at the LAST line of the file, nowhere near the edit. Use a
`/* ... */` block, or put the comment on its own line. `node --check` on the extracted module
catches it in a second; a browser reload just shows a blank screen.

**Anything new that holds state must go in `saveGame`/`loadGame`.** Four of these were silently
lost on reload until they were tested; test the round trip, do not assume it.

`placeAI` carries a `BAND` table of which ring each building belongs in — a type missing from it
is silently never sited, however well the rest of the brain works.
