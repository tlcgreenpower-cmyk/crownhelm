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
