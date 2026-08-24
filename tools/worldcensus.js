// Crownhelm world census — is every scatter actually putting anything on the map?
//
// WHY THIS EXISTS
// b358. b353 fixed rocks hanging in mid-air over the sea by making the skirt height honest, and in
// the same line it silently reduced the sea stacks from a scattering to ZERO — because the height
// band it was tested against had been written for the old, dishonest number. Nothing noticed for a
// build, and it only surfaced because I kept photographing the same stretch of coast and kept
// feeling something was missing.
//
// That is the shape of the problem: the world's decoration is nineteen separate scatters, each one
// a pile of conditions on elevation, water depth, distance from the border and a hash roll, and
// NOTHING counts them. Any one of them can fall to zero and the game still runs, still soaks
// clean, still reports no errors. The only symptom is that the world quietly gets emptier.
//
// HOW TO RUN
//   await census()        // one map
//   await census(6)       // six fresh maps, so a one-map fluke cannot pass
// Returns a table and a verdict. Anything placing nothing, or almost nothing against its cap, is
// flagged by name.
//
// READING IT
// A zero is not automatically a bug — lilies want still water and a map with no lake will have
// none, foam wants a shore. That is why it runs several maps and reports how many of them each
// scatter was empty on. Empty on ONE map is terrain; empty on ALL of them is a broken condition.
window.census = async function(maps){
  maps = maps || 4;
  const R = { runs: [], scale: [], byName: {}, verdict: null };
  window.__CENSUS = R;
  if(!window.TF || !window.TF._dbg) throw new Error('TF._dbg missing — is the game loaded?');
  window.TF._dbg();
  const D = window.__D;
  const wait = ms => new Promise(r => setTimeout(r, ms));

  // The world is DETERMINISTIC: calling newGame() again rebuilds the identical map, so repeating it
  // proves nothing. Real variation comes from a different map, and the honest way to get one is the
  // selector the player uses. 'custom' is skipped — it depends on whatever is in the Map Builder.
  const sel = document.getElementById('mapSel');
  const ids = sel ? [...sel.options].map(o => o.value).filter(v => v !== 'custom') : [];
  R.mapsUsed = [];

  for(let m = 0; m < maps; m++){
    if(sel && ids.length){ sel.value = ids[m % ids.length];
      sel.dispatchEvent(new Event('change', {bubbles:true})); await wait(60); }
    R.mapsUsed.push(sel ? sel.value : '(only map)');
    D.newGame(); await wait(1100);
    // Every scatter is SPLIT into a grid of chunk meshes for culling (b281), all carrying the same
    // name (b359). Reading one chunk's count is meaningless — that mistake is what produced the
    // "exactly 1 sea stack on every map" figure in b358, when the real answer was 65 across
    // twenty-two chunks. Sum them.
    const row = {};
    D.scene.traverse(o => {
      if(!o.isInstancedMesh || !o.name || o.name.indexOf('scatter:') !== 0) return;
      const key = o.name.slice(8);
      const r = row[key] || (row[key] = { count:0, cap:0, chunks:0 });
      r.count += o.count; r.cap += o.instanceMatrix.count; r.chunks++;
    });
    R.runs.push(row);

    // the scale-sensitive simulation quantities, alongside the scenery
    {const nn = pts => { if(pts.length < 2) return null; let s = 0;
       for(const a of pts){ let best = 1e9;
         for(const b of pts){ if(a===b) continue; const d = Math.hypot(a.x-b.x, a.z-b.z); if(d < best) best = d; }
         s += best; }
       return Math.round(s / pts.length); };
     let land = 0, claimed = 0;
     for(let y = 0; y < D.MAP_H; y += 2) for(let x = 0; x < D.MAP_W; x += 2){
       if(D.elev[D.ti(x,y)] < D.SEA) continue; land++;
       if(D.territoryAt(D.wx(x), D.wz(y))) claimed++; }
     R.scale.push({ tiles: D.MAP_W * D.MAP_H,
       treasures: D.treasures.length, tradePosts: D.tradeSites.length,
       tradeSpacing: nn(D.tradeSites.map(t => ({x:t.x, z:t.z}))),
       claimedPct: land ? +(100 * claimed / land).toFixed(1) : 0 }); }
    for(const k in row){
      const b = R.byName[k] || (R.byName[k] = { name:k, counts:[], cap:row[k].cap, emptyOn:0 });
      b.counts.push(row[k].count);
      if(row[k].count === 0) b.emptyOn++;
    }
  }

  // No "percentage of cap" here on purpose: the chunker sizes each piece to its contents, so after
  // b281 the summed capacity always equals the summed count and a fill ratio is a tautology. What
  // actually carries information is the absolute count and whether it ever reaches zero.
  const list = Object.values(R.byName).map(b => {
    const tot = b.counts.reduce((s,v) => s+v, 0);
    return { name:b.name, mean:Math.round(tot/b.counts.length),
             min:Math.min(...b.counts), max:Math.max(...b.counts),
             perMap:b.counts.join(' / '), emptyOnMaps:b.emptyOn+'/'+b.counts.length };
  }).sort((a,b) => a.mean - b.mean);

  const notes = [];
  for(const s of list){
    const [empty, of] = s.emptyOnMaps.split('/').map(Number);
    if(empty === of) notes.push(s.name + ' placed NOTHING on any of ' + of + ' maps');
    else if(empty > 0) notes.push(s.name + ' empty on ' + empty + ' of ' + of + ' maps — check that is terrain, not a broken condition');
    else if(s.mean < 4) notes.push(s.name + ' averages only ' + s.mean + ' across the map (' + s.perMap + ')');
  }
  const missing = ['grass','flowers','bushes','reeds','pebbles','shingle','boulders','driftwood','wrack',
                   'stumps','logs','mushrooms','saplings','deadTrees','foam','lilies','seaStacks']
                  .filter(n => !R.byName[n]);
  if(missing.length) notes.push('never found in the scene at all: ' + missing.join(', ') + ' — has a scatter been renamed or removed?');

  // ---- SCALE AUDIT. b361 and b362 both found the same kind of bug: a number tuned on Heartlands
  // (96x64) and never revisited, quietly wrong on the four 168x112 maps that are most of the menu.
  // Minimap markers drawn bigger than your own castle; eleven treasures spread over three times the
  // country; half the trade road beyond any realm's reach. Each was found by eye and then measured.
  // This measures them without needing the eye. A quantity that fills an AREA should hold its
  // per-area density; one that follows a LINE should hold its spacing.
  {const per = R.runs.map((row, i) => {
     const s = R.scale[i];
     return { map:R.mapsUsed[i], tiles:s.tiles,
              hoardsPerMTile:+(s.treasures / s.tiles * 1000).toFixed(2),
              tradeSpacing:s.tradeSpacing,
              landClaimedPct:s.claimedPct };
   });
   // landClaimedPct is REPORTED but never flagged. Measured, Heartlands has 31 per cent of its
   // land inside somebody's borders and the big maps about 10 — because BORDER_R is a fixed world
   // radius and a bigger map simply has more frontier between the same four realms. Checked how it
   // plays before deciding: on the Broadwood the nearest rival claims sit 248 units apart against
   // Heartlands' 48, and over seven minutes that gap closes 248 -> 224 -> 208 as towns expand. So
   // the system is quieter out there, not dead, and more wilderness on a bigger country is a fair
   // reading of the design rather than a bug. Left alone deliberately; the number is here so the
   // next person can form their own view instead of rediscovering it.
   // Villages are deliberately NOT measured: `villages` is not on the debug surface, and a metric
   // that silently reads zero on every map is exactly the lying instrument b358 and b360 cost a
   // pass each to. Export it first, then measure it.
   R.scaleTable = per;
   // Heartlands is the reference because every constant in this game was tuned on it.
   const ref = per[0];
   if(ref) for(const p of per.slice(1)){
     const off = (a,b) => b && Math.abs(a-b)/b > 0.35;
     if(off(p.hoardsPerMTile, ref.hoardsPerMTile))
       notes.push(p.map+': hoard density '+p.hoardsPerMTile+' per 1000 tiles against '+ref.map+"'s "+ref.hoardsPerMTile+' — a count that does not scale with area');
     if(off(p.tradeSpacing, ref.tradeSpacing))
       notes.push(p.map+': trade posts '+p.tradeSpacing+' apart against '+ref.map+"'s "+ref.tradeSpacing+' — a line whose spacing does not hold');
   }}

  R.table = list;
  R.verdict = { maps, healthy: notes.length === 0, notes };
  console.log('WORLD CENSUS over ' + maps + ' maps'); console.table && console.table(list);
  console.log('VERDICT', R.verdict);
  return R;
};
console.log('census() ready — call: await census()   (or await census(6) for more maps)');
