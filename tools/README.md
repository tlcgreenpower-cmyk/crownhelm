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
