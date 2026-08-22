# tools

Two small scripts that make Crownhelm testable without a visible browser.

## Why they exist

The browser pane doesn't composite frames in a headless session, so `requestAnimationFrame` never
fires and screenshots time out. The simulation can be driven around that — `TF._dbg()` then
`__D.update(1/30)` in a loop — but that only ever gives you *numbers*.

Numbers are not enough. On the night of 9 Aug 2026, three visual faults shipped or nearly shipped
while every measurement said the code was correct:

- rocks that read as bread rolls
- a stone texture that read as camouflage on the castle walls
- a farmhand standing in the sky

and later, a scatter fix that left half the map bare while reporting all 14,000 instances placed.

**When a count agrees and the frame disagrees, the frame is right.**

## shotsink.py

`TFshot()` in the game renders the scene to an offscreen target and returns a JPEG data URL — no
pane, no rAF, no compositing. But a 60,000-character data URL costs more to pull back through a
tool result than it's worth.

This listens on `127.0.0.1:8138`, takes a POST of that data URL, and writes a real `.jpg` next to
itself that can be opened directly.

```bash
python tools/shotsink.py
```

Then from the page console:

```js
fetch('http://127.0.0.1:8138/myshot', {method:'POST', body: TFshot({x, z, dist:40, pitch:0.55, yaw:0.6, w:960, h:540, q:0.75})})
```

`TFshot` is also just a good screenshot tool for a human — it takes a clean frame from any angle
with no HUD in the way.

## syncheck.py

Extracts the `<script type="module">` body from `Crownhelm3D.html`, stubs the Three.js import and
runs `node --check` on it. Catches syntax errors without a browser or a CDN round trip.

```bash
python tools/syncheck.py
```

## The one check this does NOT cover

A broken **shader** throws no JS error and leaves the on-screen error box empty. It has to be forced:

```js
renderer.compile(scene, camera);
renderer.render(scene, camera);
renderer.info.programs.filter(p => p.diagnostics && p.diagnostics.runnable === false)
```

Run that after any shader change. It has caught a failure that nothing else would have.

## The Blender character pipeline (`tools/blender/`)

These were living in a session scratchpad, which is wiped when the session ends — and one of the
things that pipeline knows is worth roughly the whole look of the game, so they belong in git.

Lee's PC has no Python and no Node. Blender ships its own Python, so everything here runs through
`blender.exe --background --python <script> -- <args>`:

    "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python tools\blender\rig_pipeline.py -- "<src_pbr.glb>" "<out.glb>" rigged SwordSlash

**`rig_pipeline.py`** turns a generated `*_pbr.glb` into something the game can use: cleans the
mesh, decimates to ~20k triangles, builds a humanoid rig, weights it, authors Idle / Walk /
Death / Victory / attack clips, and exports.

Two hard-won rules live in it, and breaking either one costs you the look of every character:

1. **Keep the normal map.** An early version deleted every map but base colour on the reasoning
   that "this engine never reads them". That was wrong, and it is the entire reason Meiya looked
   better than everyone else for weeks — she came in by another route and kept her full PBR set,
   while Bruce, the Pikeman, the Rider and Lisa rendered as flat painted plastic with no surface
   relief at all. Colour keeps its native 2048; relief drops to 1024 and gloss to 512, which is
   invisible to the eye and keeps the file around 6.5MB instead of 11.6MB.
2. **Metallic stays out.** `metalness` with no environment map turns a character into a black
   silhouette (b320), which is why `liftCharacterTone` pins it to zero.

Bone weighting uses `ARMATURE_ENVELOPE`, not `ARMATURE_AUTO`. These generated meshes are thousands
of disconnected shards, and bone-heat weighting needs connectivity — it fails outright, weighting
literally zero vertices of 7,968.

**`survey.py`** — prints triangle count, image sizes and which shader inputs are actually textured
for any list of .glb files. Run it before and after a pipeline change; it is how the dropped normal
maps were found.

**`bruce_fix.py`** — one-off clean-up for a generated model: remaps lipstick-red mouth pixels in the
diffuse sheet to a natural lip tone, and can delete a region of vertices by bounding box. Kept as a
worked example of both jobs.

## Serving and screenshots on Windows (`serve-8137.ps1`, `shotsink.ps1`)

PowerShell HttpListener versions of the Python tools above, for the machine that has no Python.
`serve-8137.ps1` serves the repo on 8137 with no-cache headers and the right MIME type for `.glb`.
`shotsink.ps1` is `shotsink.py` in PowerShell: POST a data URL to `http://localhost:8139/<name>`
and it writes a real `.jpg` you can open.
