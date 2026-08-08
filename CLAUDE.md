# Crownhelm — Lee's personal 3D RTS

Single-file Three.js game: `Crownhelm3D.html`. OPEN-WORLD since 2026-07-27 — the tide mechanic
was REMOVED and must never come back. Big roamable map, 3 AI realms, diplomacy (gift/war/peace),
musket-era factions. Source art in source-art/, assets in assets/.
Test: serve on localhost:8137 and drive with the Chrome extension. Keep building — this is the
owner's fun project; bold ideas welcome, tide stays dead.

Practicals (Lee's Windows PC): no python/node — serve with a PowerShell HttpListener script
(any static server on 8137 works). `index.html` is a deploy MIRROR of `Crownhelm3D.html`:
copy before every commit. Push to origin main works from this machine. Perf gate:
`window.TF.info` in the console (fps/ents/skinned/calls); `window._CHARLIB` inspects character
templates. b92 merged every character to ONE skinned mesh at load (colors baked to vertex
colors) — keep new models going through mergeSkinnedModel/mergeStaticModel.
