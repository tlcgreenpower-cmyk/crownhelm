// Crownhelm long-run soak — does a game stay healthy for an hour?
//
// WHY THIS EXISTS
// Every soak in this project runs about ten minutes, because that is how long a chunk of console
// stepping takes. The owner plays for far longer. Nothing had ever checked that entity counts
// settle, that the scene stops growing, that the save file stops swelling, or that the step time
// does not drift — the failures that only show up after half an hour and then ruin an evening.
//
// HOW TO RUN
// Serve the game, open it, paste this in. It returns a summary and leaves the full table on
// window.__SOAK. Takes a few minutes of wall clock; it prints each sample as it goes.
//   await soak()          // default, 25 simulated minutes
//   await soak(45)        // longer
//
// THE TRAP THIS EXISTS TO AVOID
// `renderer.info.memory.geometries` and `.textures` count what has been UPLOADED TO THE GPU, not
// what the game is holding. They rise the first time anything new is drawn and never fall while it
// stays resident — and crucially they jump every time you call TFshot, because a screenshot renders
// parts of the world the normal camera never touched. Sampling those numbers alongside screenshots
// shows a beautiful steady "leak" that is entirely your own measuring. This file therefore takes
// NO screenshots, and reports the honest figure as well: the number of distinct geometries actually
// reachable from the scene graph, which goes down again when things are disposed.
window.soak = async function(minutes){
  minutes = minutes || 25;
  const R = {samples:[], errors:[], verdict:null};
  window.__SOAK = R;
  const err = m => R.errors.push(m);
  window.addEventListener('error', e => err('ERR ' + e.message + ' @' + e.lineno));
  window.addEventListener('unhandledrejection', e => err('REJ ' + e.reason));
  const ce = console.error;
  console.error = function(){ err('CE ' + [...arguments].map(String).join(' ').slice(0,200)); ce.apply(console, arguments); };

  if(!window.TF || !window.TF._dbg) throw new Error('TF._dbg missing — is the game loaded?');
  window.TF._dbg();
  const D = window.__D;
  const wait = ms => new Promise(r => setTimeout(r, ms));

  D.newGame(); await wait(2400);

  let steps = 0;
  const sample = () => {
    let nodes = 0; const geo = new Set();
    D.scene.traverse(o => { nodes++; if(o.geometry) geo.add(o.geometry.uuid); });
    let saveKB = 0;
    try { D.saveGame(true); saveKB = Math.round((localStorage.getItem('crownhelm_save')||'').length/1024); } catch(e){}
    const t0 = performance.now();
    for(let i=0;i<60;i++) D.update(1/30);           // sim only — rendering here would poison the counters
    const stepMs = (performance.now()-t0)/60;
    const mem = D.renderer.info.memory;
    return { min:+(steps/1800).toFixed(1), ents:D.ents.length, blds:D.blds.length, cits:D.citizens.length,
             sceneNodes:nodes, sceneGeom:geo.size, gpuGeom:mem.geometries, gpuTex:mem.textures,
             saveKB, stepMs:+stepMs.toFixed(2), errs:R.errors.length };
  };

  const run = ms => { const t0=performance.now();
    while(performance.now()-t0 < ms){ for(let i=0;i<300;i++){ D.update(1/30); D.frame(1/30); steps++; } } };

  R.samples.push(sample());
  console.log('soak 0m', R.samples[0]);
  const targetSteps = minutes*1800;
  while(steps < targetSteps){
    run(22000);
    const s = sample(); R.samples.push(s);
    console.log('soak ' + s.min + 'm', s);
    await wait(0);
  }

  // ---- verdict. Compare the tail against the point the army stopped growing: anything that keeps
  // climbing after the entity count settles is the shape a leak actually has.
  const S = R.samples, last = S[S.length-1];
  const peak = Math.max(...S.map(s => s.ents));
  const settledAt = S.findIndex(s => s.ents >= peak*0.95);
  const tail = S.slice(Math.max(1,settledAt));
  const drift = (k) => tail.length>1 ? +(tail[tail.length-1][k]-tail[0][k]).toFixed(1) : 0;
  const notes = [];
  if(tail.length < 2) notes.push('army never settled inside ' + minutes + ' minutes — run it longer before trusting the rest');
  else {
    if(drift('sceneNodes') > tail[0].sceneNodes*0.15) notes.push('scene nodes still climbing after the army settled: +' + drift('sceneNodes'));
    if(drift('sceneGeom') > tail[0].sceneGeom*0.15) notes.push('scene geometries still climbing after the army settled: +' + drift('sceneGeom'));
    if(drift('saveKB') > Math.max(8, tail[0].saveKB*0.25)) notes.push('save file still swelling after the army settled: +' + drift('saveKB') + 'KB');
    if(drift('stepMs') > Math.max(1.5, tail[0].stepMs*0.6)) notes.push('step time drifting upward: +' + drift('stepMs') + 'ms');
  }
  if(R.errors.length) notes.push(R.errors.length + ' errors — see __SOAK.errors');
  R.verdict = { minutes:last.min, peakEnts:peak, settledAtSample:settledAt, healthy:notes.length===0, notes };
  console.log('SOAK VERDICT', R.verdict);
  console.table && console.table(S);
  return R;
};
console.log('soak() ready — call: await soak()   (or await soak(45) for longer)');
