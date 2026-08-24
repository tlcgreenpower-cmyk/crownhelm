# Crownhelm — Work Log (time & cost tracking)

**Method:** every deploy is a git commit with a timestamp. Work is clustered into stretches (a gap of 45+ minutes ends a stretch). Each stretch is credited +15 min lead-in for the coding done before its first commit — conservative; real time is slightly higher. Repo history begins Fri 31 Jul 12:44 (site launch). Design/build work on 26–30 Jul happened before the repo existed and is NOT counted below.

## RUNNING TOTAL: 15h 37m of tracked build time (102 deploys)

| Stretch start | End | Deploys | Duration | Running total |
|---|---|---|---|---|
| Fri 31 Jul 12:44 | 13:37 | 4 | 1h 07m | 1h 07m |
| Fri 31 Jul 14:22 | 17:18 | 17 | 3h 11m | 4h 19m |
| Sat 01 Aug 04:01 | 06:35 | 37 | 2h 49m | 7h 08m |
| Sat 01 Aug 16:39 | 17:54 | 7 | 1h 30m | 8h 38m |
| Sat 01 Aug 18:46 | 18:58 | 2 | 0h 26m | 9h 05m |
| Sun 02 Aug 04:32 | 07:11 | 13 | 2h 54m | 12h 00m |
| Sun 02 Aug 13:11 | 14:15 | 7 | 1h 19m | 13h 19m |
| Sun 02 Aug 16:00 | 18:02 | 15 | 2h 17m | 15h 37m |

## Going forward
- A START/STOP line is appended here every time work begins or halts, any reason.
- Idle gaps are recorded when discovered (e.g. Sun 2 Aug 18:02 -> Mon 3 Aug 02:41, 8h39m: session-bound loop did not fire; PC was on).
- New: the 'tidefall-improve' scheduled task runs every 30 min while the app is open and logs its own timestamps here.

## Live log
- Mon 3 Aug 02:41 START (owner check-in; time-tracking setup + scheduled worker created)
- Mon 3 Aug 02:54 START (interactive: KayKit wall/tower art hunt + wiring)
- Mon 3 Aug 03:34 STOP (b72 shipped: KayKit stone walls+gates; stretch 40m)
- Mon 3 Aug 03:52 STOP (b73: straight staircase walls; stretch 10m)
- Mon 3 Aug 04:04 STOP (b74: middle-mouse pan + building bars visible on select; stretch 12m)
- Mon 3 Aug 04:16 STOP (b75: cannon facing + aim-before-fire; stretch 10m)
- Mon 3 Aug 04:26 STOP (b76: order-facing + siege pivot; stretch 8m)
- Mon 3 Aug 04:40 STOP (b77: L-walls + demolish; stretch 12m)
- Mon 3 Aug 04:56 STOP (b78: true diagonal walls; stretch 14m)
- Mon 3 Aug 05:10 STOP (b79: ruler-straight walls; stretch 13m)
- Mon 3 Aug 05:14 START (b80: real cavalry horses)
- Mon 3 Aug 05:34 STOP (b80: real cavalry horses; server restarted; stretch 20m)
- Mon 3 Aug 05:52 START (b81: Chinese Imperial Army faction)
- Mon 3 Aug 06:04 STOP (b81: Chinese Imperial Army in jade green; stretch 12m)
- Mon 3 Aug 06:22 STOP (b82: named save slots; stretch 18m)
- Mon 3 Aug 06:26 START (b83: Sacred Band of Thebes faction)
- Mon 3 Aug 06:38 STOP (b83: Sacred Band of Thebes, pink + rainbow banners; stretch 12m)
- Mon 3 Aug 07:12 STOP (b84: medieval start screen redesign; stretch 34m)
- Mon 3 Aug 07:22 STOP (b85: edge scrolling; stretch 8m)
- Mon 3 Aug 07:34 STOP (b86: auto graphics tuning for slow machines; stretch 10m)
- Mon 3 Aug 07:44 STOP (b87: auto attack-chaining; stretch 8m)
- Mon 3 Aug 07:58 STOP (b88: scan stagger; PERF GATE reading: 294 ents / 200 blds / 1990 skinned on owner save; stretch 10m)
- Mon 3 Aug 08:08 STOP (b89: freeze fix - pathfind thrash cooldowns; stretch 8m)
- Mon 3 Aug 08:14 STOP (b90: chain radius leash; stretch 5m)
- Mon 3 Aug 08:30 STOP (b91: AI town planning + ability; stretch 14m)
- Wed 6 Aug: woodcutter_hut.glb integrated as the Storehouse visual (b92, LOCAL ONLY - not deployed). Measured: 59,988 tris/hut, 1 draw call, 3x2048 PNG (11MB encoded / ~64MB VRAM), 17.4MB file. Replaces KayKit lumbermill (3,170 tris / 170KB).
- Wed 6 Aug: worker-Meiya_pbr.glb wired as the King (b93, LOCAL ONLY). 499,998 tris, 1 draw call, 3x2048 PNG (9.1MB / ~64MB VRAM), 34.4MB file. NO RIG (skins:0 animations:0) -> routed through procedural bob/lean; no walk/attack/death animation. Replaces Knight_Golden_Male (2,964 tris, 17 anims).

- Wed 6 Aug: RENAMED Tidefall -> CROWNHELM. Folder Desktop\Flooded Britain Game -> Desktop\Crownhelm; Tidefall3D.html -> Crownhelm3D.html; Play Tidefall.bat -> Play Crownhelm.bat; localStorage tidefall_* -> crownhelm_* WITH one-time auto-migration so existing kingdoms survive. GitHub repo still 'tidefall' (public URL unchanged - awaiting owner call).

- Wed 6 Aug (session end): Ported onto the REAL b215 line after discovering this clone was 128 builds stale (local b91 vs remote b215). Force-push avoided; stale code branch parked at 'crownhelm-rig-and-rename'. Ported forward ONLY the durable work: rigged Meiya as the King, optimised Woodcutter Hut as the Storehouse visual, and the Crownhelm rename (incl. tidefall_* -> crownhelm_* save migration).

- Sat 8 Aug: AoE ORDER SET — four builds, all live on the crownhelm repo.
  - b216 TOWN BELL (B). Every villager runs for the nearest tower/keep/castle with room; ring again and each one resumes the EXACT job it dropped (same tree, same wall, same farm). Release also frees any villager left in a garrison by an older save.
  - b217 PATROL (R). Walk the line between here and a clicked point, weapons free, for ever; return to the line after each fight. Reuses the attack-march leg so it inherits formation + acquisition. X / move / attack call it off.
  - b218 STANCES (Z). Aggressive (default, unchanged) / Defensive (fights what comes, walks back to post) / Stand Ground (shoots what is in reach, never moves). Also killed the dead-and-wrong 'hold' bail-out in autoAcq that made a man standing his ground stop looking.
  - b219 HOTFIX. b218 shipped a live crash: spawnUnit has always written stance:'aggr', the STANCE table is keyed 'aggro' — every unit would have thrown inside autoAcq. Found by reading spawnUnit, not by testing. All reads now go through stOf() with an Aggressive fallback, so pre-b218 saves load.
  VERIFIED in a live world via TF._dbg() (drives update() directly, so it works in a throttled tab where rAF does not): foe 9 tiles off -> Aggressive charges 5.3, Defensive and Stand Ground do not move and never acquire; no throw for aggro/defend/hold/legacy 'aggr'/undefined. Patrol flips legs cleanly and keeps marching (4 legs, ~1.3s each over 14 units).
  NOT verified at runtime: the Town Bell, which needs a started game — synthetic clicks are blocked in this browser and the pane is not displayed. Code-reviewed only.
  Also: scheduled task 'tidefall-improve' repointed at the Crownhelm folder/file/repo (it would have failed on its next run after the rename) and given a git fetch/pull step first, so no session can work a stale clone again.

- Sat 8 Aug 21:30-22:36: FOUR MORE, all live.
  - b220 MONK CONVERSION. Right-click an enemy with a Monk/Priest/Cardinal; progress lives on the MONK so breaking off loses it; faith spent for 26s after. Monk 7s@8, Priest 6s@9, Cardinal 5s@11. King immune. VERIFIED: flipped at exactly 7.00s, mesh rebuilt in player colours, spent monk blocked at 39% faith, King refused, out-of-range progress bled at the intended rate.
  - b221 MARKET PRICES MOVE. Sell -3.5%/100, buy +3.5%/100, floor 30% ceiling 250%, drift back to par (half-life ~2min, unlike AoE2 - an hours-long game would leave it dead). Saved with the kingdom. VERIFIED: sells paid 50/48/47/45/43, buys cost 70/72/75, guards hold, 0.825 -> 0.878 over a minute.
  - b222 VILLAGERS REPAIR (did not exist at all - every raid was permanent). Right-click a damaged building with workers, or the new Repair button on its panel. Costs half the pro-rata build cost. VERIFIED: Barracks 50% -> full in 27.7s for 27.4 wood against the 27.5 the rule specifies.
  - b223 THE AI MENDS AND PREACHES. Rivals repair their worst building (2 masons max, gives up if the barn is empty) and their monks convert. VERIFIED: rival Keep at 35% had a mason on it 14.4s later and came back to full.
  TOWN BELL (b216) FINALLY VERIFIED once newGame went on the harness: 4 villagers on wood -> bell -> all 4 in the Keep (hall 4/8) -> all clear -> all 4 out, none stranded, all 4 back on the same wood.
  HARNESS: TF._dbg() now also exposes newGame, trade/mkt*, repairOrder/repairTime, convertOrder/convertUnit, setStance, commandPatrol, townBell, COST/BLD/UNIT. NOTE: _dbg() captures blds/ents BY REFERENCE - call TF._dbg() AGAIN after newGame() or you are reading the old arrays.

- Sat 8 Aug 22:50-23:20: camera + scale block.
  - b224 resource hover names the thing (Forest/Gold vein/Iron seam/Carcass + live game), amount of original, % bar, and why men cannot reach a tree.
  - b225 THE AGE OF EMPIRES CAMERA. Measured AoE2 at 1280x720: tile ~96px, TC ~287px, ~19 tiles across. Old default (dist 80/pitch 53deg) = 37px tile, 146px Keep, 35 tiles across - hence "cannot see anything". New default dist 45 / pitch 0.62 = 66px tile, 259px Keep, 19.5 across. C snaps back. Loads force it too (every save holds the old camera).
  - b226 MEN AT AoE PROPORTIONS. b197 measured a soldier at 2.28 vs a 4-unit tile = 0.57 tile; AoE villager is 0.42. MAN_SCALE 0.75 -> 0.43 tile. Applied to foot/horse/rider/guns/procedural/holy orders/weapons; health bars ride down; buildings + ships untouched. M toggles, remembered in crownhelm_manscale. Verified ratio 0.751.
  - b227 followed the men: instanced far-rank imposters and regimental standards were left at the old size (both hang off the unit GROUP, the same trap the weapons were in).
  - b228 idle-SOLDIER round-up (topbar + backslash), mirroring the b41 idle-worker button.
  CORRECTION LOGGED: the "94px vs AoE 40px" figure I gave the owner in b225 was measured off a Box3 that included the health bar and banner. Real gap was ~1.36x, not 2.4x. Box3.setFromObject is NOT a reliable ruler on skinned characters here - read the normalised target heights in makeUnitMesh instead (2.4 foot, 3.0 hero).

- Sat 8 Aug 23:20-23:45: b229 rings/parade follow the man scale. b230+b231 TRADE CARTS - Market, Age 2, 100w/60g; shuttles to the farthest non-hostile realm's Market; pay = distance x 0.11 per run; war closes the route; own ox-cart mesh. b231 fixed the arrival tolerance (cart parked 16 units out against a 9.6 reach and waited for ever) - wide dock + 8s stall-counts-as-arrived. Verified 33g/run on a 296 route, ~105s round trip.
  HARNESS NOTE: render-side systems (team rings, unit imposters, HUD counts) do NOT populate under TF._dbg() because they run off rAF, which never fires in a backgrounded tab. Sim-side behaviour verifies fine; anything visual has to be checked by eye in a real window.

- Sat 8 Aug 23:45-00:10: b232 AI town bell (radius 70; 40 was measured useless) + Market as a trainer.
  AI TRADE CARTS ABANDONED. Rule read correctly, every gate measured green (market up, at peace, 33k gold, 56 pop spare, empty queue, partner 296 away) and no realm ever built one, filed low in realmBrain or at the very top. Root cause not found in budget; pulled rather than shipped as a silent no-op.
  *** SELF-INFLICTED BREAK + RECOVERY: moving blocks inside realmBrain by text surgery, my cut used an end-anchor that matched a block far below the start and deleted a large part of the function ("r is not defined" at runtime). Caught it on localhost, never deployed. Recovered with `git checkout -- Crownhelm3D.html` back to b231 and re-applied only the wanted change with single-anchor asserts. LESSON: never cut a RANGE between two independently-moving anchors in this file - insert-before-anchor only, one assert each.

- Sun 9 Aug 00:10-00:30: b233 SAVE FORMAT CAUGHT UP. None of tonight's orders were being written down - a reloaded kingdom came back all-Aggressive, patrols forgotten, monk faith free, trade carts parked for good. Stance/patrol/faith saved; carts re-route on load; old saves load unchanged. Verified over a real save/load: holds held, patrol came back on the same line (ax -114 bx -90 leg 1), monk 40% -> 40%, cart already routed.
- b234 cancel-from-queue with full refund (verified 2 -> 1 and exactly 50 food back). Trade cart icon added.

- Sun 9 Aug 12:00-12:40: VISUAL UPGRADE, owner brief + Image 2 reference (premium stylised medieval RTS).
  b235 STAGE 1 lighting + grass palette. Sun 1.85->2.10 warmer, hemi fill down, ground bounce warmed, exposure 1.30->1.38, seven terrain stops warmed. NOTE: all lighting must go through updateDayNight(), which rewrites it every frame - editing the declarations does nothing.
  b236 STAGE 1b THE BIG ONE: every scatter setHSL wrote into LINEAR working space and was displayed as sRGB, so grass intended mid-green rendered #c6daae (pale sage). Same fault b172 fixed in the terrain canvas; the instanced scatter never got it. Nine colour tables fixed -> #87ae59. Turf 9k->14k, flowers 1.6k->3.2k.
  b237 STAGE 2 three tree archetypes (oak broad crown + underskirt / birch slim / fir four tiers) inside the existing instancing. 48/48/47 on a fresh map, felling intact.
  b238 STAGE 3 rock + gold formations from angular slabs + rubble; gold is an ochre outcrop with seams, not a butter ball. Contract kept: Group scale 2, shrink verified exact (0.81 at 30%), hides when empty.
  b239 STAGE 4 sea colour lifted from near-black. VERIFY TRICK: renderer.compile(scene,camera)+render(scene,camera) forces shader compilation in the headless tab - check renderer.info.programs for diagnostics.runnable===false. 38 programs, 0 failures.
  STILL TO DO: building surrounds/props, path blending, shoreline rocks+reeds, fog-of-war reads as a black void (gameplay - left alone, owner asked).

- Sun 9 Aug 13:40-14:10: b240 ground detail texture (AoE4 approach - injected via onBeforeCompile; FIRST CUT FAILED, it guessed the UV varying by regex but #includes are unexpanded at that point, so neither vUv nor vMapUv is in the source yet - caught only by renderer.compile + checking info.programs diagnostics). b241 grass cones -> alpha cards (4 tris vs 8, 731k->620k). b242 UNDID MY OWN b238 ROCK REGRESSION - dodecahedra piled six deep read as bread rolls; boxes+octahedra, 3 masses, footprint >3 tiles -> 1.5. b243 procedural texture library (stone/bark/leaf, grey-centred so material colours survive) + walked back dropping flatShading.
  STANDING TECHNIQUE: any shader change MUST be verified with renderer.compile(scene,camera)+render then checking renderer.info.programs for diagnostics.runnable===false. A broken shader throws NO JS error and #err stays empty.
  OWNER IS TAKING BUILDINGS; I have the environment.

- Sun 9 Aug 20:15-20:40: PLAYED AND TESTED THE GAME THROUGH (b253-b257, NOT COMMITTED - awaiting say-so).
  THE HARNESS WAS LYING. ents is reassigned (`ents=ents.filter`) EVERY time anything dies, and res/tech
  are reassigned by initRealms() and loadGame(). _dbg handed all three out by value, so from the first
  casualty onward I was reading a corpse of the game. That is what produced "entity count frozen at 114
  while the field was really 188", and it is very likely what killed the b230 AI trade-cart hunt -
  every gate measured green because I was measuring the wrong object. b253+b257 put them behind getters.
  MEASURE THE HARNESS BEFORE BELIEVING THE MEASUREMENT.
  SHADOWS WERE MISSING - two separate bugs, both found only by LOOKING at a rendered frame:
   1. b254 the shadow CAMERA was stretched to the whole map (504x376 on a 2048 map = a quarter of a
      unit per texel; a 1.7-unit man got a 4-texel shadow which PCFSoft then blurred away. On the
      168x112 maps half the world sat outside the far plane entirely). Now follows the view, texel-
      snapped, ~0.06 units/texel. Light DIRECTION untouched - position and target move together.
   2. b256 the shadow CONTRAST. Measured at the exact ground point a test cube's shadow lands on:
      only 17% darker than open grass, because hemi ran 1.07 against a sun of 2.10 and ACES then
      compressed what was left. Traded fill for key (0.46/2.80): 28% and clearly readable. Open-ground
      brightness unchanged (113.8 -> 110.9), so b235's warm daylight survives.
  b255 GRASS: my own b241 cards were the worst thing in frame - up to 1.6 units tall against a 1.71-unit
  man, and coloured DARKER than the ground they stood on, so they read as torn green paper. Now a third
  of a man and lighter than the field. Flowers were 0.1 spheres in full-strength hues - candy on a lawn;
  smaller and pastel now.
  SEEING IT AT LAST: shotsink.py (scratchpad) listens on 8138, takes a POST of a TFshot() data URL and
  writes a real .jpg the Read tool can open. THAT is the missing half of b252 - the game could take a
  photograph but had nowhere to put it. Every fix above was found by looking, not by numbers.
  WHAT TESTED CLEAN: 25+ game-minutes driven headlessly, zero JS errors, zero broken shaders. Save/load
  round-trips EXACTLY (deep-compared units, buildings, resources, age, elapsed) and the game runs on
  afterwards. Defeat fires correctly ("Your Kingdom Has Fallen", running=false). Three-front war resolves.
  FAIRNESS PROVEN: gave the player realm the rivals' own realmBrain - it kept pace and led (59 units /
  32 buildings / Age 2 at t=600 vs 29-63 for the rivals). The game is symmetric; my earlier wipeouts
  were my scripted player being bad, not a balance fault.
  PERFORMANCE IS FINE: 4.5-5.3 ms a frame (~200fps headroom) on Intel integrated graphics, 908k tris,
  365 draw calls. An early reading of 18fps was shader RECOMPILATION on first frames, not steady state -
  do not benchmark the first frames after touching materials.
  FOR THE OWNER: idle starting workers only ever chop wood - 3 minutes untouched gives 1,437 wood and
  still exactly the 200 food and 80 metal you started with. In AoE the first villagers auto-gather food.
  That is nextJob, i.e. gameplay, so I have NOT touched it - his call.
  STILL TO DO: building surrounds/props, path blending, shoreline rocks+reeds, terrain still reads as
  one flat green at distance. Fog-of-war black void left alone (owner asked for it, b141).

- Sun 9 Aug 20:50-21:10: b258 + b259, brief items 4 and 5 (NOT COMMITTED - awaiting say-so).
  b258 BUILDING SURROUNDS. Worn earth was five soft ellipses of one colour at 0.18 alpha - a smudge
  at play distance. Three passes now: a ragged outer fringe so the patch does not end on an oval,
  the old body at higher alpha, and a darker trodden core, because a yard wears hardest where the
  feet are. PROPS: barrels, crates, sacks, logs, planks, stumps, buckets, stones, kitted BY TRADE -
  sacks at a mill, logs at the woodcutter's, crates at a market, stone at the forge. NOT baked into
  the models, as he asked: a separate merged mesh hung off b.mesh, so it can be re-kitted or pulled
  without re-exporting a GLB, and it dies with the building automatically.
  COST DISCIPLINE: everything merges to ONE geometry and ONE shared material per building - 65
  buildings' worth of props came to 4,928 triangles total. Left as loose meshes it would have been
  ~200 extra draw calls; merged it is one per building.
  TRAP: mergeGeometries silently refuses a mix of indexed and non-indexed geometry, and a
  Dodecahedron is non-indexed while a Box is not - a stone next to a crate would have dropped the
  whole lot. Everything is toNonIndexed() first.
  FARMS ARE EXCLUDED ON PURPOSE - b251 raycasts b.mesh to find the surface the farmhands stand on,
  and hanging props off that mesh would put a man on top of a barrel.
  b259 PATHS. The road system was already good (verge, worn centre, ruts) but each was a SINGLE
  stroke at uniform alpha, so a road ended on a crisp tan edge and read as a ribbon laid on the
  grass. Three graded verge passes now, plus a deterministic scatter along both sides - earth
  spilling out, grass reclaiming the middle - so the boundary wanders. Canvas only, no geometry.
  VERIFIED: 12,600 sim steps, no JS errors, no broken shaders, 830k tris / 317 calls at a built-up
  town. Props on 70 buildings, roads on 67.
  NOT MINE, PRE-EXISTING: the house model carries a SphereGeometry at y=2.1 that reads as a pale
  ball sitting on the roof apex in screenshots. Left alone - it is his building.
  STILL TO DO: shoreline rocks + reeds, terrain still reads as one flat green at distance.

- Sun 9 Aug 22:00-22:20: b260+b261 SHORELINE (brief item 6).
  PHOTOGRAPHED THE COAST BEFORE TOUCHING IT, because b103 and b199 had both already been over this
  ground and I did not want a third scatter on top of two. The BEACH was fine - pebbles, driftwood,
  shingle, the b199 strand band all present and correct. What was missing was the WATER's half of
  the meeting: the old foam fired only below depth 0.16, a sliver a few inches wide on this shelf,
  so the sea just changed colour against the sand with nothing happening at the join.
  b260 put in a proper surf: a drifting two-octave noise edge so the foam wanders in tongues instead
  of ringing the island, a pulse so it advances and retreats, and a lip at the waterline that does
  not depend on the noise (without it the waterline itself can come out dry).
  b261 IS THE ONE THAT MATTERED. b260 still photographed as a soft pale wash. Shallow water is drawn
  at 0.72 alpha so the sand reads through it - correct for water, WRONG FOR FOAM. White at 72% over
  tan sand is pale cyan-tan, which is exactly what I was looking at. `alpha=max(alpha,foam*0.96)` is
  most of the difference; the band widths were secondary.
  LESSON: when a bright thing renders dull, check what it is being composited OVER before retuning it.
  Verified with the standing shader technique: 62 programs, 0 with diagnostics.runnable===false.
  STILL TO DO: terrain reads as one flat green at distance - the last item on my list.

- Sun 9 Aug 22:20-22:40: b262+b263 THE FLAT GREEN - last item on the visual list.
  MEASURED FIRST, on a 300x300 block of the painted ground texture:
    red   mean 133 sd 30.8 | blue mean 88 sd 17.1 | GREEN mean 169 sd 10.7
  90% of the country inside a 40-level green band, 65% inside two eight-level bands. So b196's four
  noise fields ARE working - they are just all working in HUE. The turf shifts straw to lush and
  back at the SAME BRIGHTNESS throughout, and the eye reads shape from value, not hue. That is the
  whole reason the ground looked like a sheet, and no amount of extra colour variation would have
  fixed it. b169's lightness nudge existed but at +/-0.025 linear over a six-unit period it is a
  grain, not a landscape.
  Two broad octaves, ~45 and ~18 world units, gated to grass and eased out down to the sand so the
  shore bands b103/b199 tuned survive. First cut at 0.185 measured as barely a move (sd 10.7->12.2);
  0.285 gives 13.6 and reads as bleached rises and damp hollows in the frame.
  THIRD TIME FOR THE SAME TRAP: groundCv was also exported by value and is null until buildTerrain
  runs, so the measurement above threw on a fresh page. Now a getter, like ents/blds/res/tech.
  ANY module-level binding that gets REASSIGNED must be a getter in _dbg. That is now four of them.
  ALL EIGHT ITEMS OF THE VISUAL BRIEF ARE DONE (terrain, trees, rocks, building ground detail,
  paths, water, lighting, art direction). What is left is polish, not gaps.

- Sun 9 Aug 22:40-23:00: b264+b265 HEADLANDS AND SEA STACKS (terrain silhouette).
  THE CONSTRAINT THAT SHAPED THIS: passable() gates on water, standing forest and buildings and
  NOTHING ELSE - there is no notion of ground too steep to walk. So a decorative rock anywhere on
  the playfield is a rock your men stroll straight through, which is a worse fault than a soft
  horizon. The crags therefore go only where nothing can walk: the SKIRT (b174's sixty units of
  terrain running past the playable border out to sea, where inB() is false) and genuinely
  submerged ground just off the coast. Pure silhouette, zero gameplay cost, and it finally does
  what the skirt was built for - the world ends in headlands instead of trailing off.
  b264 SHIPPED A BUG AND THE PHOTO CAUGHT IT: I gated in-map stacks on elev<=1.0 thinking that
  meant water. SEA is 0.55, so elev 0.55-1.0 is DRY LAND that happens to be low, and a crag came
  out standing on the grass above the beach - the exact wart the rule exists to prevent. b265 tests
  the thing itself (ground below waterY) instead of a proxy. Also lifted them from 0.26 lightness,
  where they photographed as near-black holes, to 0.44-0.62.
  PROVED IT RATHER THAN ASSUMING: walked all 122 instances and ran passable() on each tile.
  0 standing on walkable ground. That check is cheap and should be repeated if the placement rule
  is ever touched.
  NEXT: tree variety at distance (firs read as identical cones); owner's call on idle workers only
  ever chopping wood.

- Sun 9 Aug 23:00-23:15: b266 FIR VARIETY.
  b237 gave the fir four tiers and a good silhouette but the offsets and scales are LITERALS -
  every fir on the map was the same shape at a different size and spin, and a hillside read as a
  row of traffic cones. The oak and birch get away with fixed layouts because their masses pick
  different leaf materials; the fir had nothing to break it.
  h3 already carried unused spread: the archetype gate only fires above 0.68, so 0.68-1.0 was free
  variation nobody was reading. Remapped to 0-1 it drives tier COUNT (3/4/5), tier gap and taper
  rate; h2 drives squat-spruce vs narrow-spire. One code path, three recognisably different trees.
  TRAP AVOIDED: c1 cone base radius is 1.25 and c2's is 0.85, so a continuous taper across the
  switch would pinch every tree in at the waist. Work in real radius/height and divide by each
  cone's own base.
  Placement, felling, shrink-as-harvested, materials and draw-call count all untouched.
  OVERNIGHT RUN SET UP: cron 8e3aa447 every 30 min (13,43) picking one improvement per firing, and
  one-shot d9f844d8 at Mon 11:00 to stop and report. SESSION-ONLY - both die if the app is closed.

- Mon 10 Aug 00:00-00:35: b267 (wrong, never deployed) -> b268 SCATTER STRIPS.
  The tufts ran in faint diagonal bands with bare lanes between them, visible in every screenshot
  this session. Cause: x came from hashN(i*1.7,3) and z from hashN(7,i*2.3) - two hashes of the
  SAME marching integer, and a sin-based hash fed two arithmetic sequences keeps enough correlation
  to draw a lattice. Raising the count would only have made the bands denser.
  b267 REACHED FOR THE TEXTBOOK CURE AND IT WAS WRONG HERE. A jittered grid is the standard fix for
  lattice artefacts, but a grid is traversed IN ORDER and these scatters stop at a cap, so the fill
  ran out partway down the map and everything south of that row got nothing. Every instance count
  was still exactly at cap (14,000 / 3,200 / 850) so the numbers all said it worked. Only the
  photograph said otherwise. THIRD TIME THIS SESSION a count agreed and the picture disagreed.
  b268 is the narrow fix: make the SECOND axis hash the FIRST HASH rather than i again. One
  multiply. Breaks the correlation completely, loop/cap/fill order untouched.
  NEW CHECK WORTH KEEPING: count instances per cell of a 6x6 grid over the world, not just the
  total. b268 gives 0 empty cells, min 159, max 587 (the spread is terrain - water and sand cells
  carry less grass). That check would have caught b267 without needing the photo.
  ALSO CHECKED AND FOUND FINE: team-colour readability. updateTeamRings() already draws a team ring
  under every visible ungarrisoned unit, fog-gated. My premise was wrong - no change made.

- Mon 10 Aug 00:40-01:05: b269 TFshot camera fix + b270 GOLD ORE.
  b269: TFshot put the camera at an ABSOLUTE height of sin(pitch)*dist and aimed at y=0, which is
  only right where the ground is at sea level. Anywhere the land is up - most of it - a close shot
  photographed the inside of a hill. Cost me two wasted shots before I read my own tool. Both the
  camera and its aim point now sit on the terrain. Close-in shots (dist<25) are usable at last.
  b270: photographed the gold node and it read as a stack of flat orange boxes - cheese. The iron
  node forty feet away read correctly, and the difference told me why: iron is grey rock with dark
  crevices, so there is CONTRAST and the eye reads stone; the gold node was solid ochre from the
  ground up and a single-colour lump of flat faces has nothing in it to read as anything. Gold in
  the ground is rock with gold IN it. Body is stone now (same three masses, same b242 footprint),
  gold kept for a struck seam at the peak and nuggets caught on the faces. Also means the node
  visibly gets poorer as it is worked, because the gold sits on the outside.
  CONTRACT CHECKED, not assumed: still a Group at scale 2, 13 children, a0/s0 shrink untouched.
  GITHUB PAGES STUCK: the b268 build sat on "building" for 40+ min on the right SHA (verified via
  gh api pages/builds/latest). Not our fault; this push supersedes it.

- Mon 10 Aug 01:10-01:25: b271 THE WHITE DOTS - owner spotted them, and they were mine.
  He sent a screenshot asking what the white dots all over the map were. VERIFIED rather than
  guessed: enumerated every instanced scatter with >200 instances and read its instance colours
  back out of the buffer. The 3,200 spheres at radius 0.065 carried #f2efe1 - the flowers, from my
  own b255. They had been four saturated hues reading as sweets on a lawn, so I muted them and
  reached for CREAM as the mute. Grass luminance 0.62, cream 0.94: the single highest-contrast
  thing on the map. I swapped candy for confetti.
  SAME LESSON THREE BUILDS RUNNING (grass cards b255, terrain b262, this): VALUE is what makes a
  thing shout, not saturation. Every flower colour now sits within 0.148 luminance of the turf,
  count 3200->2100, head 0.065->0.055. Measured, not eyeballed.
  ALSO IN HIS SHOT, not a fault: the diagonal white streaks are the rain shower (updateRain).

- Mon 10 Aug 01:30-02:15: b275+b276 THE FARMERS, properly this time (4th complaint).
  b248-b251 fixed WHERE he stands and how HIGH. NOBODY HAD EVER MEASURED HOW HE MOVES. Logged one
  farmhand at 30fps: walked 25.9 units to make 7.2 of progress (wander 3.6), 8 reversals in 4s,
  position jumping 5.6 units between samples, x oscillating -104.90/-104.06 with y flicking.
  THREE THINGS WERE MOVING ONE MAN: (1) the tend case ASSIGNED e.x/e.z to a fresh Math.random()
  point every 2.5-5s - he was never walking the rows, he was being cut and pasted round his own
  field; (2) separateUnits shoved him off the bed and b251's clamp yanked him back, every other
  step; (3) an e.path issued while he stood on the bed walked him 1.9 units OUTSIDE the plot and
  the clamp then snapped him back - every 25 frames, exactly.
  b275 fixed (1) and (2) and MADE IT WORSE - wander went 3.6 -> 678 - because my walk became a
  FOURTH thing fighting the path. Instrumenting the individual jumps rather than the summary is
  what found (3): every jump was identical, -112.99 to -111.05, the plot edge.
  b276: while _onDeck, clear e.path every tick. A man on the bed is working, not travelling.
  MEASURED RESULT: biggest single-frame jump 1.963 -> 0.21, frames off the plot -> 0, distance
  26.8/4s -> 12.8/10s. Still on the farm, still tending.
  LESSON: when something jitters, do not fix the movers you can see - COUNT them. Four separate
  pieces of code had write access to this man's position.

## Overnight run, Sat 22–23 Aug 2026 — continuous, unattended

Owner asked for a continuous overnight project: pick the highest-value thing, verify it by
rendering or measuring, fix it, soak it, ship it, no questions. Running note below, newest last.

- **b343 ENEMY GARRISONS SHOWED THROUGH FOG.** My own bug, one build old. Putting the garrison on
  the parapet (b331) meant exempting those men from the LOD's imposter path, which works off
  ground position and would have swapped a man on a battlement for a stand-in in the dirt. I
  exempted them from the FOG test in the same breath — so an enemy garrison lit up on its walls
  across an unexplored map and you could count the men in a castle you had never scouted.
  Fog first, then the wall exemption, and off-screen wall men now get a real frustum test instead
  of being skinned unconditionally. Verified both ways: 3 hidden while fogged, 3 visible the
  moment a scout stands there, own garrison unaffected over two simulated minutes.

- **TRIED AND REJECTED: derived normal maps for the bought character pack.** The pack models
  (Knight, Mage, Barbarian, Rogue, the pirates — about ten unit types including all four cavalry
  riders) carry a diffuse sheet and nothing else, which is exactly the fault that made Lee's own
  characters look flat until b326. Wrote a Blender pass that reads diffuse luminance as height and
  takes its gradient. Rendered the mounted Knight before and after at identical camera and light:
  INDISTINGUISHABLE. Reason worth keeping — these models put their detail in GEOMETRY, faceted
  plates and hard-edged helms over flat colour, so there is no luminance gradient to read and the
  derived map comes out uniformly flat. Knight reverted byte for byte; script and the negative
  result kept in tools/blender/add_normalmap.py so nobody tries it again from scratch.
  Those models need more polygons or a hand-authored map, not a derived one.

- **CHECKED, NO FAULT FOUND: treasure guardians holding their post.** Wolves hunt, so a pack could
  in principle chase a passing worker and leave its hoard open. Measured over six simulated
  minutes: worst drift 9 units from the hoard (from a starting 3), and zero of the eleven
  treasures ended up unguarded. The tether works; no change made.

- **b344 THE TREASURE RACE IS REAL NOW.** Measured the system as shipped and its top tiers were
  decorative: only WORKERS could shoot beasts (1 damage a shot, from the hunting code), soldiers
  could not engage wolves at all, and ten minutes of three AI realms wandering past hoards claimed
  exactly none. Two halves: (1) any fighting man of any realm stood near a guarded hoard now takes
  his weapon to the wolves automatically — no order needed beyond marching him there — and the
  pack bites back exactly as it bites a hunter; (2) an at-ease realm with six spare soldiers
  details a party of three to the nearest unclaimed hoard (boomers keenest, realms at war don't
  bother). Verified: four infantry stood at a hoard clear its guard unaided (110→103hp, claimed),
  and a fresh hands-off game has the realms take 4 of 11 in ten minutes while the big distant
  hoards mostly keep their guards — a race, not a famine.

- **b345 THE COAST WAS A RULED LINE.** Photographed the seaboard and then measured it: the water's
  edge on the east sat between x=182.0 and x=183.0 across 224 units of shore — ONE unit of wander
  over the whole coast, because the rim rule cut the land purely as a function of distance to the
  map rectangle, so the shoreline could not be anything but a straight line parallel to the border.
  b174 had already tried to fix this and could not: its noisy skirt only shapes the mesh OUTSIDE
  the playable rectangle, and the land had gone under water before it ever got there, so every bay
  it cut was drowned and unseen. Moved the noise into the playable grid instead — the DEPTH of the
  waterline is now the noisy quantity and the shore bends by itself. Measured after: the shore now
  runs 11 to 40 units in and the map grows river mouths, bays, headlands and a gulf on the east.
  Two guards on it: the outermost ring always drowns, so the world still ends in sea, and the
  homeland plateaus are raised after the rim, so no realm can start underwater.
  Also fixed the sea stacks while in there. The shallows rule only tested that ground was under
  water AT ALL and then lifted every stack to just under the surface regardless of the depth of
  the bed, so lakes in the middle of the map carried what photographed as a raft of dark rubble
  floating on a pond. A stack now needs a bed within a rock's height of the surface, has to be in
  the coastal ring rather than an inland lake, and stands on its bed instead of on the waterline.
  Ten simulated minutes hands-off after the change: 3 realms, 120 buildings, 293 units, no errors,
  no building underwater and no land unit stranded in water.
  (Also exported SEA/HSCALE/waterY/elev/ti/MAP_W/MAP_H through TF._dbg. The first round of these
  measurements silently compared heights against `undefined` and reported "no land anywhere".)

- **b346 THE BLANK DOLLS WERE STILL IN THE TOWN.** b327 surveyed the character library, found a
  bottom tier carrying NO TEXTURE AT ALL, and moved every combat unit off it — "nothing untextured
  is left on the battlefield". It never touched the townsfolk. Counted on a grown world by walking
  the citizen list and asking each material whether it has a `map`: 8 of 22 citizens — better than
  a third of the town — were untextured (2,524-tri Kimono, 2,720 Ninja, 2,994 Soldier and
  BlueSoldier, 5,856 Viking). Those are the same blank white dolls that drew the owner's
  complaint about the Chu-Ko-Nu, and the town is where the camera spends most of its life.
  Swapped the four untextured entries for Barbarossa, Privateer, Knight and Lisa. Re-counted:
  0 of 22. Costs about 2,500 triangles a citizen; measured at the owner's default zoom afterwards,
  381 draw calls and 408k triangles with 1.7ms of sim per frame against a 33ms budget.

- **RE-VERIFIED b345's building check.** The soak in b345 tested `b.x` for buildings, and
  buildings do not have an `x` — they carry `cx`/`cz`. So that check compared `undefined` and
  passed vacuously. Re-ran it properly against `cx`/`cz` on a fresh 7.5-minute world: 75
  buildings, none underwater. The claim was true, it just had not actually been tested. Noted in
  CLAUDE.md along with the fact that TFshot's pitch and yaw are RADIANS, which cost several
  renders of the underside of the map.

- **FOUND, NOT YET FIXED: twelve unit types share five models.** infantry and grenadier are both
  Meiya; spear and hoplite are both LeePikeman; archer and Chu-Ko-Nu are both BruceBowman; monk,
  priest and cardinal are all Mage; highlander and viking are both Barbarian. On the field you
  cannot tell a grenadier from a line infantryman, which matters in a game that has a whole
  battle-order system built on telling roles apart. The library has textured models going spare
  (Anne, Henry, Mako, Sharky, Barbarossa, Knight, Privateer) but each needs looking at before it
  is assigned. Next job.

- **FOR THE OWNER TO DECIDE: the infantry is a toddler.** Photographed each unit type on its own.
  `infantry` and `grenadier` use Meiya, and Meiya is a barefoot chibi child in a lilac romper and
  a pink cape. It is genuinely the best-finished asset in the game — 20,080 tris, a full 2048
  colour, normal and roughness set, the only model with all of it — which is very likely what the
  owner meant by "the only good looking one is meiya". But it is serving as the line infantry and
  the grenadier of a musket-era army, and the file is still called worker-Meiya. Not changed:
  swapping it out would overturn a preference the owner stated out loud. Flagged instead.

- **b347 NEW MEN FOR THE DIFFERENT UNITS, AND MEIYA IS A WIZARD.** Owner's instruction after
  seeing the b346 note. Two halves.
  (1) THE HISTORY PACK WAS NEVER UNTEXTURED — it was UNPAINTED. Nine models have sat unused since
  the start, written off by b327 for having no texture. They have no image, true, but they carry
  named per-material colours, which is exactly how this game's own art works. The values were the
  fault: every one reads out of the glTF near-black (Soldier Skin 0.0134, Main 0.063/0.091/0.040)
  while Face is pure white in all nine and Skin is byte-identical across all nine — the signature
  of a colour conversion applied once too often, which leaves white alone and crushes the rest.
  Through b172's black-point lift that is a flat grey body under a white face: the blank white
  doll, three separate complaints, explained. Geometry, rig and seventeen clips were always fine.
  tools/blender/recolour_troops.py repaints all seven fighting models by material name into
  assets/troops/. The material names lie about which part they paint, so the mapping was read off
  debug renders with every material a different vivid hue rather than guessed — Black is the coat
  body, Helmet is the hair, and Face is the narrow band across the EYES. That last one is what
  gave these men faces; painting it white is what took them away.
  Infantry is now a redcoat, grenadier a blue-coated bearskin, hoplite a steel man-at-arms with a
  red plume, Chu-Ko-Nu a hooded crossbowman in dark green, viking a bare-armed raider, samurai an
  indigo kimono. Twelve types sharing five models is now twelve sharing eleven.
  (2) MEIYA TAKES THE STAFF. She is the Monk, and a chibi girl with a staff still reads as a girl
  with a stick, so she gets a pointed indigo hat with a gold band parented to her HEAD BONE — it
  rides the walk cycle instead of hovering beside her, the b325 lesson. Sized off the man's
  rendered height divided by the bone's own world scale: the first try used the model-space height
  and the hat came out buried in her hair, because a bone sits after ch.scale, so bone space is
  world space. Her own texture already has a star-patterned cape; with the hat she reads as a
  wizard at a glance. HOLY_TINT now keys on the MODEL, not the unit type — it paints a whole model
  one flat colour, which would have thrown away the only full PBR texture set in the game.
  Cheaper than what it replaced: the new soldiers are 2.5-6.3k tris against Meiya's 20k. Soak of
  12 simulated minutes, 198 units, 94 buildings: no errors, 433 draw calls, 569k triangles, 1.76ms
  of sim per frame. Save/load round trip: every type restored, all six wizards still wearing hats.

- **THIRD TRAP DOCUMENTED.** A unit photographed away from the camera shows its BIND POSE, not its
  animation — TFshot renders from its own camera but updateUnitLOD decides who gets skinned from
  the REAL one, and off-screen men are deliberately never animated. On these rigs frame 0 is a
  T-pose, so it looks exactly like a broken model. Cost most of an hour before it was spotted.
  Drive the mixer by hand before the shot. Now in CLAUDE.md.

- **b348 THE AI COULD NOT TRAIN NINE OF ITS OWN UNIT TYPES.** Counted a hands-off game at 24
  minutes: all three realms fielded 135 pikemen, 39 vikings, 11 archers and 4 infantry — no
  cavalry, no guns, no siege, no King — while sitting on 400-1,600 unspent gold each. Cause: units
  cost food, wood and GOLD (metal is for buildings and research), but every training test in
  realmBrain asked `r.m >= COST.<unit>.m`, and no unit has an `.m`. `>= undefined` is false, so
  knight, dragoon, samurai, cannon, grenadier, catapult, infantry, the King and every faction's
  unique guard were unreachable — permanently, in every game. The four infantry in the census were
  the ones each realm starts with. Same class of fault as the `b.x` trap already in CLAUDE.md: a
  silent comparison against undefined that never throws and never logs.
  Fixed with two helpers that read the real cost object (`canPay`/`payFor`) applied to all fifteen
  training sites including the three that were already right, so there is only one way to do it.
  Also widened three age gates from `===2` to `>=2` — knight, cannon and dragoon were written as
  "exactly Age II", so reaching Age III took them away again.
  Measured at 15 minutes, before -> after: pikemen 135->83, vikings 39->12, archers 11->4,
  infantry 4->36, grenadiers 0->16, knights 0->3, r1 treasury 397->5 gold. Samurai appear by 22
  minutes. Pikemen fall from 68 per cent of the host to about 54. 208 entities, zero errors.
  Still no cannon, and that one is economics not a bug — a cannon wants 100 wood and the realms
  run wood-poor, so it loses the roll to men who cost forty. Left alone.
  JUDGEMENT CALL: this makes the AI materially stronger and I did not soften it to compensate.
  The intent is plain in all fifteen lines; restoring it is a repair, not a difficulty change. If
  it bites too hard that is now a balance decision the owner can make against an opponent that
  works.

- **CHECKED, NO FAULT FOUND: AI personalities.** Three realms in one game all rolled 'turtle',
  which looked like a broken roll. Rolled 14 fresh games and counted: rush 15, turtle 14, boom 13
  out of 42. The roll is fine; it was chance. No change made.

- **b349 THE WOODS COME BACK.** Timber was the one resource that never returned, on a map meant to
  be lived on for an hour. Measured at 18 minutes: 62 of 107 stands were stumps, no realm had a
  living tree within 40 units of its keep (nearest 62/88/79), and the realms sat on 29/14/73 wood
  against 514/214/2,245 metal they could not spend — r2 with SIXTEEN men on a metal seam and five
  in the woods. Not an allocation bug: realmWant asks for wood correctly, but with none in reach
  the b183 fallback sends the man to the nearest work of any kind, and that is always metal.
  Wood gates houses, farms, barracks, the Castle and both Ages, so the map stalls — no AI realm
  had EVER reached Age III in any soak, meaning the whole Age III layer (unique guards, the
  Wonder, tier-3 research) had never appeared in a played game.
  Cleared stumps now seed and grow: 45s bare, then 11 minutes to maturity, a regrown stand worth
  60 per cent of virgin forest, nothing sprouting on or beside built ground.
  TWO WRONG FIRST CUTS, both worth keeping:
  (1) letting the young stand carry timber as it grew did nothing — a sapling with three wood in
  it is the NEAREST wood on the map, so a woodcutter took it back to zero over and over. A young
  stand now carries no `amount` at all until mature, which also means no other system needed a new
  rule: a node with no amount is already invisible to nearestNode, the AI and the player.
  (2) the no-building clearance was ±2 tiles and rejected ALL 38 bare stumps — the woodcutter
  fells the nearest timber and the town then grows over that same ground, so stumps and buildings
  are the same ground by construction. ±1 keeps trees out of doorways and lets copses return
  between the houses.
  RESULT over 31 minutes hands-off — live stands 79/60/56/64/67/70 at 5/10/15/20/25/30 min: the
  forest bottoms out at 56 and recovers, the first rise in any run. Wood goes from single digits
  at 15 minutes to 624/534/1109 by 30. **r2 reached Age III at minute 30 — never seen before.**
  Field carried 3 knights, a dragoon, 28 grenadiers, a samurai and an enemy King. Zero errors.
  Growth is saved (new state, project rule): 16 saplings and total growth 6.70 identical either
  side of a reload, every restored sapling at exactly the height its growth implies.
  Arithmetic trap avoided: maturing to `n.a0*0.6` compounds (220→132→79→47) and would dwindle the
  woods away over a long game. Matures against a fixed FOREST_STAND instead.
  Cost: 0.051ms for a forced full tick, and it really ticks once every two simulated seconds.

- **b350 THE WONDER COUNTDOWN ONLY SPOKE TO ITS OWNER.** b348/b349 made Age III reachable for an
  AI realm for the first time, so this pass checked what that newly-reachable content does. The
  content itself is fine — handed a realm Age III, a Castle and money it raised a Wonder, trained
  three Cuirassiers, fielded cannon and knights and ran its research. The fault is what happens to
  the PLAYER: the five-minute Wonder victory clock had its warnings inside `if(b.owner==='player')`,
  so a rival's Wonder gave one line at completion and then five minutes of silence before the game
  ended. Logged every message shown: at 34 seconds from losing the realm, the last thing the player
  had been told was a weather report. Now warns at 4/3/2/1 minutes and 20 seconds — verified all
  five fired in order and the game ended on schedule.
  Also reveals the ground the Wonder stands on (7 tiles, so the realm around it stays dark — a
  signpost, not free reconnaissance), because "deny them" is not an instruction you can follow
  against something standing in unscouted fog. And gives it a pulsing minimap ring in the owner's
  colour; ordinary building squares are four pixels among forty and that is not how you show a
  countdown to losing. Photographed the minimap to confirm.
  TWO MORE FOUND BY DOING IT:
  (1) `wonderStart` was NEVER SAVED. The victory check skips any Wonder without one, so a save and
  reload silently switched the Wonder win condition off for the rest of the game — for the player
  and the realms alike. Measured 168 seconds left before a reload, "NO COUNTDOWN" after. Stored
  relative to `elapsed` now; re-measured 168 before, 168 after, still ticking. The exact failure
  CLAUDE.md warns about, and it needed testing rather than assuming.
  (2) the wolf warning fired on EVERY BITE — a pack on one worker put the identical line up
  fifteen times in twenty seconds, and the message bar holds one line, so a mauling buried
  everything else. It buried the Wonder countdown in the very run testing the Wonder countdown.
  One per twenty seconds now: same run shows three wolf messages instead of twenty-two.
  Plus a `possess` helper — half the realms are named in the plural, so it was "Blue Coats's".
  Soak: 13 simulated minutes, 154 entities, 106 buildings, zero errors, 9.24ms a step.

- **b351 A CRASH THAT HAS BEEN SILENTLY EATING FRAMES SINCE b326.** Staged a battle to look at
  combat and the console threw `ReferenceError: makePeace is not defined` from `updateLords`,
  called from `update()`. b326 gave lords a RECOVERY state that "sells goods and sues for peace";
  the selling was implemented, the suing calls `makePeace()`, and that function exists NOWHERE in
  the file. Because the call sits inside `update()`, every time a battered lord at war with the
  player rolled his 22 per cent the whole remainder of that simulation step was abandoned —
  combat, movement, building, resources, the win check. Repeating roll, common game state, and
  nothing surfaces it: the browser logs it and the game carries on looking fine. Written now as
  the spending half of the state the comment already describes — he pays up to 120 gold, the
  tribute goes to the player, allied wars end with it, honour rises for asking, and the player is
  told. Verified: war → neutral, message fired, tribute moved, no errors.
  SWEPT FOR MORE: pulled every BARE call site out of the script (not `x.method(`, which is 800
  false positives) and diffed against everything the file defines. 92 survivors, all explainable —
  GLSL builtins in shader strings, THREE addons from dynamic imports, object-literal shorthand
  methods, and the TF._dbg getters. No second one.

- **CHECKED, NO FAULT FOUND — three, recorded so the next pass doesn't re-open them.**
  (1) Health bars looked like huge floating slabs in a battle photo. Measured: a pikeman spans
  10.63–12.83 and his bar sits at 12.73, on his head. What looked like float was the pikes of the
  rank behind him.
  (2) An enemy town looked to be on top of the player's keep in one shot. The four keeps are
  148–296 units apart on a 384×256 map. Camera angle, not map generation.
  (3) A duel of identical armies came out 12–0 to the player with `tech.player.weapon` reading 1
  against the AI's 0. Traced to a save I had loaded earlier in the same page session — a fresh
  game holds at 0 for ten minutes while the AI legitimately researches. My own residue. The rest
  of the asymmetry is terrain: the two sides stood on ground 4.95 and 7.70 high, and elevation is
  meant to matter.
  Soak: 9 simulated minutes with two wars running throughout, 292 entities, 129 buildings, zero
  errors, 6.44ms a step.

- **b352 A SWEEP THAT CLICKS EVERYTHING THE PLAYER CAN CLICK.** b351's crash had been eating
  simulation steps since b326 and only surfaced by luck — a battle staged for another reason
  happened to catch it in the console. The hands-off soak this project leans on only ever
  exercises `realmBrain`; every command button, stance, panel, diplomacy action and menu item is
  untouched by it, and that is the half of the game the owner operates. `tools/uisweep.js` now
  drives all of it from one console paste: builds a rich player kingdom, clicks every button on
  every building panel and every unit bar, runs gift/war/peace against all three realms, works the
  top bar and game menu (everything but Quit), and round-trips all four win modes through
  save/load checking the mode survives and the game still runs.
  RESULT: 226 interactions, four win modes, ZERO errors. Nothing new found — this ships the
  harness and a clean run, not a fix, and the commit says so.
  TWO TRAPS IT TAUGHT ME, both now in CLAUDE.md: a soldier's commands live in `#formBar` and his
  `#cmds` is EMPTY (a worker is the other way round) — my first sweep read `#cmds` only and
  reported "military units have no commands at all", which looked serious for about a minute. And
  the panel is built from `div.btn`, not `<button>` — querying for buttons finds nothing and
  reports a clean pass over zero controls, which is the worst kind of green.
  Caveats written into the file so a clean run is not over-read: it does not cover the Map
  Builder, Parade mode, or real pointer work on the 3D view (drag-select, right-click orders,
  formation drag-aim, wall dragging, rally flags), and a green sweep means every button is wired
  to something that runs, not that it does the right thing.

- **CHECKED, NO FAULT FOUND: Regicide, end to end.** Every realm starts with a King, `_regHad`
  fills correctly, a downed King stays in `ents` so the game does NOT end while he is merely down
  (the b330 design), and removing a King outright ends the game on the spot with `_regDone` set.
  `_regHad` is not in the save, which looked like the same hole b350 found in the Wonder's clock —
  but it self-heals on the first tick after a load, since any realm that still has a King re-marks
  itself. Left alone. All four win modes survive save/reload with the mode intact.

- **b353 THE MAP BUILDER HAS NEVER WORKED SINCE THE RENAME.** Went after the surfaces b352's sweep
  skips. MapBuilder.html writes `tidefall_custom_map` / `tidefall_map` / `tidefall_players`; the
  game reads `crownhelm_*`. Zero overlap. Save a map and the game never sees it; press PLAY TEST
  and it sets two keys nothing reads, then drops you into a generated map. A feature advertised on
  the main menu that cannot deliver a playable map. The game's rename migration DOES copy
  `tidefall_*` across but it is one-shot — it ran once, set `crownhelm_migrated`, and returns early
  forever, while the builder carried on writing where the migration would never look again.
  Builder writes `crownhelm_*` now; the game reads the old key as a fallback when the new one is
  absent, and the builder does the same for its editor state, so stranded maps and half-finished
  designs come back. Verified the whole round trip: 284 painted hills all at elev ≥3.3, 455 painted
  water tiles all below sea level, 4,000 sampled plains all land, resources exactly as saved
  (1,276 forest / 26 iron / 16 gold), and the map plays — 32 buildings, 42 units, zero errors.

- **AND THE FIRST CUSTOM MAP EXPOSED A SECOND FAULT.** Photographed it: boulders hanging in mid-air
  over the sea. `heightAtWorld` clamps to the tile grid, so beyond the playable rectangle it
  returns the map EDGE's height and never changes. Measured west of the border — heightAtWorld says
  11.22 at 4, 10, 20, 35 and 55 units out, while the mesh drops 8.72 / 6.23 / 1.11 / −7.13. An
  18-unit lie, and the b264 skirt crags are placed with it. Always wrong; only visible now because
  b345 drowns a GENERATED map's rim so its edge sits near the waterline and the gap stays small —
  a painted map has no rim and the fault came straight out. The skirt formula lived inline in
  `buildTerrain` so nothing else could ask where the ground was; it is `terrainMeshY(x,z)` now,
  used by the mesh and the crags. Checked the extraction is exact before trusting it: 4,000 sample
  points, 1,908 outside the rectangle, worst difference **0** — terrain byte-identical, only the
  rocks moved. Photographed after: they stand on the shore.

- Also rebranded the builder, which still said TIDEFALL in its title, masthead, back button and its
  "not a Tidefall map" error. Naming only — no tide mechanics remain in it. The one surviving
  mention is a code comment recording where a function was ported from, which is true and stays.
  Soak after: 7 simulated minutes on a generated map, 58 buildings, 76 units, zero errors.

- **b354 THE UNIT PARADE WAS DROWNING ITS BACK RANK.** Second of the surfaces b352's sweep skips.
  The parade laid its ranks out three tiles below the Keep and marched south with nothing checking
  the map went that far. On the Heartlands the Keep sits at ty=49 on a 64-tile map, so the ranks
  land at 55/58/61/64 — and 64 is off the end of a grid whose last row is 63. Measured on the real
  screen: **4 men off the map entirely** (z=130, boundary 128) and **5 standing on water**, four of
  them on skirt ground 6–8 units UNDER the sea. The drowned rank was Hoplite, Privateer, Viking and
  Samurai — four of the six models b347 had just rebuilt, on the one screen whose whole job is to
  show them off.
  Now sizes the block it needs and finds somewhere it fits. Dry alone was not enough: the first
  version allowed anything above the tideline and photographed as half-on-grass, half-on-beach, so
  it wants proper inland ground (1.6, the floor the world's own scatter uses) and near-level, so
  the back rank does not stand over the front rank's heads. Falls back to the old position if the
  map offers nothing, so it cannot be worse than before. Camera frames the block, not the Keep.
  Verified through the menu button rather than by calling anything directly: 37 units, 31 types,
  zero off-map, zero in water, no errors; photographed before and after.
  Soak: 13 simulated minutes of ordinary play after, 179 units, 70 buildings, zero errors, 3.40ms
  a step.

- **b355 THE SWEEP NOW DRIVES THE MOUSE.** Last of the three surfaces b352 listed as out of reach.
  A synthetic click turns out to be honest here after all: project a world point through the camera
  into client coordinates, dispatch a real MouseEvent, and the game's own
  `localXY → raycastGround → commandMove` path runs exactly as under a hand. `tools/uisweep.js`
  now drives seven orders and asserts each one LANDED, not merely that nothing threw — select the
  right man, walk him (measured 21.9 units), send a worker to timber, order an attack, box-select,
  place a foundation by clicking the ground, move a rally flag.
  RESULT: 223 interactions, 7 pointer orders, 4 win modes, ZERO errors. No new defect — the pointer
  surface is sound; b353 and b354 had already taken the two skipped surfaces that were not.

- **THREE THINGS CHECKED RATHER THAN FIXED, which was most of the value.**
  (1) Box-select over the town returned 1 unit while 5 stood inside the box, dropping four workers.
  Looked like a clear bug for a minute. It is deliberate — if the box holds any non-worker, workers
  are filtered out, the same convention AoE uses so dragging over your town gives you the army and
  not the peasants. The sweep now ASSERTS it so nobody "fixes" it into a regression.
  (2) A `computeBoundingSphere(): radius is NaN` during a drag. Reproduced from a clean start: does
  not happen. My own doing — `setCam` takes (x,z,dist,pitch) and I called it bare, which sets
  camTarget to undefined and turns the camera NaN, making every later projection garbage.
  (3) The first full run reported three failures and ALL THREE were the sweep being wrong: it
  hardcoded r1/r2/r3 in a two-AI-realm game, and it asserted `cmd==='gather'` four frames after a
  gather order, by which time the worker had filled his arms and moved to `'return'` — the order
  having worked. Both fixed and both documented at the assertion, because a harness that cries
  wolf is worse than no harness.

- **b356 LONG-RUN STABILITY, AND THE COUNTER THAT LIES ABOUT IT.** Every soak in this project runs
  ~10 minutes; the owner plays far longer, and nothing had ever checked the failures that only
  appear after half an hour. `tools/soak.js` runs a long hands-off game and returns a verdict on
  whether entity counts, scene nodes, scene geometry, save size and step time all settle.
  Measured over 21.5 simulated minutes: army plateaus at 346 and stops; scene nodes and scene
  geometry stop climbing and tick DOWN between samples (disposal working); save holds at 74KB;
  step time flat ~2ms against a 33ms budget; zero errors. Verdict healthy, no notes.

- **THE TRAP, which is most of the value.** `renderer.info.memory.geometries` looked like a textbook
  leak — 484 at 15 min, 597 at 18, 716 at 23, with entities flat at 342 and scene nodes barely
  moving. It is not one. Those counters report what has been UPLOADED TO THE GPU, so they only ever
  rise, and they jump every time you call **TFshot**, because a screenshot renders parts of the
  world the play camera never touched — and I had been screenshotting between samples. Proved it
  with a controlled two-minute interval containing no screenshot: 1406 geometries before, 1406
  after, while the scene churned 44 new geometries in and 38 out. soak.js therefore takes NO
  screenshots and reports the honest figure too — distinct geometries reachable from the scene
  graph, which falls again on disposal. Trap and correct measure both now in CLAUDE.md.

- **CHECKED, NO FAULT FOUND: textures.** Looked like a creep (51→63). Counted distinct textures
  actually referenced by scene materials: 57, against 61 reported. The four spare are render
  targets. The rise tracks character models uploading the first time each unit type appears, and it
  plateaus. Not a leak.

- No defect found this pass — it ships the harness and a clean 21.5-minute result, and the commit
  says so plainly.

- **b357 A STREET OF IDENTICAL HOUSES.** Every soak leaves the PLAYER with bare ground — the AI
  builds, the player doesn't — so in all the photography across these builds nobody had ever looked
  at a BUILT player town, which is the view the owner spends his whole game inside. Built one
  properly: 25 buildings laid out the way a person lays one out, a garrison, a population.
  The housing quarter is six byte-identical objects at the same angle in lockstep. Houses are the
  most numerous building in any settlement (18–45 in a grown game), so that repeat dominates the
  look of every town on the map. b190's twelve degrees breaks the ruled rows but cannot stop every
  roof pointing the same way — twelve degrees is not a different building, it is the same building
  slightly crooked.
  Square-footprint types (house, mill, bakery, storehouse, market, garden, statue, watch,
  tradepost) now take a quarter turn plus a size between 0.95 and 1.05, seeded from the tile like
  b190 — so a saved town returns exactly as it stood with no new save field. Verified: 25 varied
  buildings, every rotation and scale identical across save/reload. Excluded on purpose: Keep and
  Castle (one or two per realm, doors face the road) and everything in NO_JITTER.

- **TWO THINGS CHECKED RATHER THAN ASSUMED.**
  (1) Tinting was the obvious third variation and is NOT safe: 292 distinct materials across 58
  buildings but EIGHTEEN are shared, one by 36 buildings at once. Tinting in place recolours whole
  groups; cloning to avoid it would undo the b92 merge that keeps draw calls down. Left alone.
  (2) Scaling could sink a building into a hill, which b209 exists to prevent. Measured with b209's
  own metric on the same buildings with variation off and on: mean change **0.016** units, worst
  **0.07**. The deep gaps in town (to −6.58 on a scarp) are b209's slope handling, identical either
  way. The variation does not move buildings.
  Soak: 11 simulated minutes, 249 units, 115 buildings of which 68 went up DURING play and carry
  the variation through the build animation, zero errors, 4.20ms a step.

- **b358 b353 QUIETLY EMPTIED THE HEADLANDS.** Kept photographing the coast and kept noticing
  nothing stood off it. b264 built "crags on the skirt and stacks in the shallows"; the shallows
  half survived, the skirt half — the rocks beyond the map edge that make a coastline read as one —
  did not. Instrumented the real placement loop instead of guessing. Identical on 3 maps of 3:
  7000 candidates, 2974 land on the skirt, **0 passed the height band**, 16 pass after the fix.
  Zero. And I caused it in b353 last night: that build made `y` on the skirt the height of the mesh
  actually there rather than the map edge's height (fixing rocks hanging 18 units in the air), and
  silently invalidated the band written against the old value — `y > waterY+16` was a formality
  when `y` was a flat edge height and became a wall once it fell to waterY−9. A fix and a
  regression in one line, and nothing caught it because nothing counts rocks.

- **THE FIRST FIX WAS STILL WRONG.** Widening the band restored 16 stacks; checked them before
  believing it and all 16 were COMPLETELY UNDER WATER. The band only knows the depth of the sea
  floor, not the size of the rock standing on it. The size is known further down the loop, so the
  real question is asked there — does the top clear the tide? Rocks that would not show are not
  placed. After, on 3 maps of 3: 53 crags, 4 on the skirt, **zero floating**, drowned down 16 → 4
  (and those 4 are the pre-existing inside-map branch, where the loop's boundary test and my
  audit's disagree by a tile). Photographed: a stack now stands out of the shallows onto the sand.
  Soak: 11 simulated minutes, 234 units, 110 buildings, zero errors, 4.25ms a step.

- **MEASUREMENT LESSON, cost most of the pass.** I counted crags by finding "the" octahedron
  InstancedMesh via `scene.traverse` and reading its `count`. There are TWENTY-TWO of them and the
  one traverse lands on last is meaningless — that is where the "exactly 1 crag on every map"
  figure came from, and it was nonsense. Sum across all of them, or better, tally inside the loop.

- **b359 SOMETHING TO COUNT THE WORLD WITH.** b358 was a scatter that had fallen to zero and stayed
  there for a build, found only because I kept photographing the same coast and kept feeling
  something was missing. Not a way to find things. The world is nineteen separate scatters, each a
  pile of conditions on elevation, water depth, border distance and a hash roll, and NOTHING counted
  them — one can die and the game still runs, soaks clean and reports no errors.
  Two changes make them countable: every scatter now sets `mesh.name='scatter:<thing>'` (19 of
  them), and **`chunkGroupInPlace` copies that name onto every piece** when b281 splits a scatter
  into a culling grid. That second part is the one that mattered — the pieces were anonymous, which
  is exactly why b358 went badly: I read "the" instanced mesh's count and got 1 when the true
  figure was 65 across twenty-two chunks.
  `tools/worldcensus.js` — `await census(5)` walks the REAL map selector (Heartlands, Greatvale,
  Twinrivers, Ironhigh, Broadwood), because the world is deterministic and calling newGame() again
  just rebuilds the identical map, so repeating it proves nothing. Counts every scatter on each and
  flags anything empty.
  RESULT, five maps, healthy: seaStacks 53/50/59/48/62, deadTrees 12/108/106/53/217, stumps
  18/165/162/78/326, mushrooms 54/495/482/236/987, grass 14000/42875×4. Nothing empty anywhere, and
  the seaStacks 53 matches b358's independent measurement exactly — the cross-check that the census
  reads the right thing.
  Left out on purpose: percentage of cap. The chunker sizes each piece to its contents so summed
  cap always equals summed count; it read 100% for all nineteen on the first run, which is worse
  than useless because it looks like information.
  Soak: 11 simulated minutes, 229 units, 104 buildings, 614 named chunks alive, zero errors, 3.93ms.

- **b360 THE DEBUG SURFACE WAS REPORTING ONE MAP'S SIZE FOR EVERY MAP.** Took b359's census out for
  its first real use and it immediately "found" that Heartlands — the default map, the one every
  photograph in this project is taken on — carried a third the scenery of the other four. Grass
  14,000 vs 42,875, stumps 18 vs 165–326, dead trees 12 vs 217, every map reporting 96×64. It read
  as a clean density bug on the map the owner plays, and would have neatly explained why the ground
  looked bare in b357's town shots.
  It was my own instrument. `MAP_W`, `MAP_H`, `WORLD_W`, `WORLD_H` were exported from `_dbg` as
  PLAIN VALUES, captured when `_dbg()` ran and never updated. Heartlands really is 96×64; the other
  four are **168×112**, three times the area — and the debug surface flatly denied it, so the
  land-tile count I divided by only scanned the first 96×64 tiles of a bigger map. Caught it with
  `elev.length`, which is live: 6144 vs 18816 while `MAP_W` insisted on 96 for all five.
  Getters now, plus HALF_W/HALF_H. Honest numbers, grass per land tile: heartlands 2.97, greatvale
  2.70, twinrivers 2.83, ironhigh 2.62, broadwood 2.77 — the same density everywhere, as it always
  was. **Nothing to fix in the world.**

- **SECOND MEASUREMENT TRAP IN TWO PASSES.** After b358's "read one InstancedMesh and call it the
  total", this is the second instrument that produced a confident wrong conclusion — this one
  within minutes of building the very tool meant to prevent that. An instrument that lies is worse
  than none, because it manufactures work. Both traps now in CLAUDE.md, along with the fact that
  the maps are NOT all the same size, which is what made this one bite.
  Verified after: census clean across all five maps, healthy, nothing empty. Soaked both map sizes
  — Heartlands and the Broadwood at 168×112 — 19 simulated minutes, 163 units, 89 buildings, zero
  errors, 5.02ms a step on the big map. The large-map path had never been soaked before.

- **b361 ON THE BIG MAPS THE LOOT WAS DRAWN BIGGER THAN YOUR CASTLE.** b360 revealed the maps are
  not all one size — Heartlands is 96×64, the other four are 168×112, three times the area and four
  of the five menu choices — and every photograph, soak and measurement this project has ever taken
  was on Heartlands. So this pass went to the big maps.
  MOSTLY IN GOOD ORDER, worth stating: realms land correctly in the corners of the 672×448 world
  (keeps 340–642 apart vs 148–296); pathfinding holds — over a measured minute 36 of 40 moving
  units moved and the four that didn't were three woodcutters at a tree plus one infantryman in a
  crowd; wars cross the map — declared war on all three and r2 marched 31 men and its King 340
  units to the player's gate and pulled the Keep down; and it stays healthy — 21 simulated minutes
  on the Broadwood, entities 24→287, nodes 8,418→21,195, save 37→89KB, step 0.89→2.19ms, zero
  errors, no drift. That path had never been soaked.
  THE MINIMAP IS THE EXCEPTION. Every marker is a FIXED pixel radius tuned on Heartlands (tile =
  2.08 minimap px). On a 168×112 map a tile is 1.19px and the markers don't care. Measured on the
  Broadwood: player's Keep **3.57px**, village dot **4.80**, trade post **5.00**, treasure
  **6.40** — loot and scenery drawn nearly twice the size of your own castle, sixteen villages
  shouting over the terrain. Photographed: a scatter of discs with the country barely visible.
  Markers now scale with tile size, anchored so HEARTLANDS IS UNCHANGED (village 4.81 vs 4.80,
  treasure 6.41 vs 6.40 — rounding). Broadwood comes down to 2.80 / 3.20 / 3.66, all at or below
  the Keep. Floors stop anything vanishing. b350's Wonder ring scales with them.
  Soak: Heartlands to 11 min then Twin Rivers at 168×112 to 16, zero errors, 3.85ms a step.

- **b362 THE ROAMING LAYER NEVER GREW WITH THE MAP.** Same class as b361's minimap markers but in
  the simulation, and worse because it is not decoration — it is the whole reason to leave home.
  Every other world feature already scales: villages min(16,7*A), relics min(7,3+2*A), all nineteen
  scatters, clouds, birds, butterflies, sheep. The roaming layer was `spawnTreasures(11);
  spawnTradeRoute(7);` — flat, however big the country.
  Heartlands: 11 hoards, **111.9 per million sq units**, 52 between neighbours. Broadwood (3.06×
  the area): the SAME 11, **36.5 per million**, 95 apart. A third the density on four of five maps.
  Treasures now scale with AREA (they fill one); the trade road with the SQUARE ROOT of area (a road
  is a line). Measured both ways — full area scaling put 16 posts 33 apart on big maps against
  Heartlands' 43, tighter than the map it was tuned on; sqrt gives 12 at 43–44, matching exactly.
  Bird flocks already make the same 1-D distinction. After: density 111.9/112.9/112.9, trade spacing
  43/43/44. Heartlands untouched at 11 and 7.

- **AND THAT UNCOVERED THE REAL FIND.** With the road properly populated the big map STILL finished
  seven minutes with zero posts claimed. The AI only reaches a signpost within **190 units** of its
  hall, and 190 was measured on a 384×256 world. Counted on the Broadwood at 672×448: only **6 of
  12** posts lay within 190 of ANY keep; the other six sat 210–301 out where no realm would ever go.
  Half the trade road was "a prize with nobody standing in the way of it" — word for word the fault
  b336 was written to cure, back the moment the map outgrew the constant. Reach now scales with
  sqrt(area): 190 on Heartlands unchanged, 333 on big maps, 12 of 12 in contention.
  Played out, not assumed: Broadwood at 7.5 min now has 6 of 12 held and split three ways (r1 2,
  r2 3, r3 1) where the same run before had none.
  Verified: save/reload with 34 hoards and 12 posts round-trips exactly — positions, tiers,
  ownership. Soaks: Broadwood 7.5 min / 184 units / 5.32ms; Heartlands 12.2 min / 184 units /
  3.19ms; zero errors on either.

- **b363 A CHECK FOR THE BUG THAT KEEPS HAPPENING.** b361 and b362 were the same bug twice: a
  number tuned on Heartlands (96×64) and never revisited, quietly wrong on the four 168×112 maps
  that are most of the menu. Both found by eye, then measured; nothing was watching for the class.
  The census now audits it — alongside the nineteen scatters it measures the scale-sensitive
  quantities across every real map and flags any whose density doesn't hold (area things keep their
  per-area count, line things keep their spacing). On this build: hoards/1000 tiles 1.79 / 1.81 ×4,
  trade spacing 44/41/44/42/45, verdict healthy — b362's fix holding, now verifiable in one call.

- **TERRITORY: MEASURED, REPORTED, DELIBERATELY NOT CHANGED.** Heartlands keeps **31.2%** of its
  land inside someone's borders; the big maps about **10%**, because BORDER_R is a fixed world
  radius and a bigger country has more frontier between the same four realms. Tempting to scale it
  like the rest. Checked how it PLAYS first: on the Broadwood the nearest rival claims sit 248 units
  apart against Heartlands' 48, and over seven minutes that gap closes 248 → 224 → 208 as towns
  expand. Quieter out there, not dead — and "a bigger map has more wilderness" is a fair reading of
  the design. Changing a tuned constant on a hunch is how b360 nearly happened. Number left in the
  table so the next person can judge instead of rediscovering it.

- **ALSO CHECKED, LEFT ALONE:** forts and castles absent at 15 minutes on Heartlands looks like the
  "type missing from BAND" trap — it isn't, both are gated behind Age II and most realms are still
  Age I then. The 22-townsfolk cap is a mesh budget, identical on both map sizes, not a scale bug.

- **TWO CORRECTIONS TO CLAUDE.md.** It has said "No Python and no Node" for a long time. **Both are
  installed** — node v24.19.0 + npm 11.17, python 3.13.15 (`py` works; `python3` hits the Windows
  Store alias). Not trivia: the game is one 780KB HTML file and `node --check` on anything in
  `tools/` catches a syntax slip in a second instead of a reload and a blank screen — it caught a
  broken comment while writing this build. And **the browser caches the module script through
  `location.reload()`**, so editing the game and reloading can leave you measuring the build you
  already replaced; load with a changed query string. That cost most of a pass earlier tonight.
  Soak: 12 simulated minutes, 208 units, 102 buildings, zero errors, 3.88ms a step.
