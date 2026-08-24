// Crownhelm UI sweep — click every control the player has and report anything that throws.
//
// WHY THIS EXISTS
// The hands-off soak (spin up a game, step it for twenty minutes, watch the error count) only ever
// exercises the AI. Everything the PLAYER does — every command button, every stance, every panel,
// every diplomacy action — is untouched by it, and that is the half of the game the owner actually
// operates. b351 found a ReferenceError that had been silently aborting whole simulation steps
// since b326, and the only reason it surfaced was that a staged battle happened to drive a branch
// the soak never reaches. This makes that kind of poking repeatable instead of lucky.
//
// HOW TO RUN
// Serve the game, open it, and paste this whole file into the console. It returns a summary and
// leaves the detail on window.__SWEEP. It is READ-MOSTLY: it spends resources and queues units,
// but it skips anything that tears a building down or quits to the menu, and it finishes on a
// fresh newGame() so the page is left in a sane state.
//
// WHAT IT DOES NOT COVER, so nobody reads a clean run as more than it is:
//   - the Map Builder screen and custom maps
//   - Parade mode
//   - real mouse work on the 3D view: drag-select, right-click orders, formation drag-aim,
//     wall dragging, rally flags. Those go through pointer maths this cannot fake honestly.
// A clean sweep means every BUTTON is wired to something that runs. It does not mean the button
// does the right thing.
(async function(){
  const R={clicks:0,errors:[],sections:{}};
  window.__SWEEP=R;
  const err=m=>{R.errors.push(m);};
  window.addEventListener('error',e=>err('ERR '+e.message+' @'+(e.filename||'').split('/').pop()+':'+e.lineno));
  window.addEventListener('unhandledrejection',e=>err('REJ '+e.reason));
  const ce=console.error; console.error=function(){err('CE '+[...arguments].map(String).join(' ').slice(0,200));ce.apply(console,arguments);};

  if(!window.TF||!window.TF._dbg){throw new Error('TF._dbg missing — is the game loaded?');}
  window.TF._dbg(); const D=window.__D;
  const step=n=>{for(let f=0;f<n;f++){D.update(1/30);D.frame(1/30);}};
  const clear=()=>{try{D.setPlacing(null);}catch(e){}};
  const wait=ms=>new Promise(r=>setTimeout(r,ms));

  // ---- a kingdom rich enough that every button is affordable and every panel has something in it
  D.newGame(); await wait(2200);
  const ov=document.getElementById('overlay'); if(ov)ov.style.display='none';
  Object.assign(D.res.player,{f:9000,w:9000,m:9000,g:9000});
  D.tech.player.age=2;
  const K=D.blds.find(b=>b.owner==='player'&&b.type==='hall');
  for(const [t,dx,dy] of [['barracks',5,3],['gunshop',8,3],['church',5,7],['castle',11,3],['siege',8,7],
                          ['range',11,7],['stable',14,3],['market',2,7],['dock',-6,2],['armourer',14,7]])
    try{D.addBuilding(t,K.tx+dx,K.ty+dy,'player',true);}catch(e){err('BUILD '+t+' '+e.message);}
  let i=0;
  for(const t of ['spear','infantry','archer','viking','knight','monk','hero','cannon','catapult','worker'])
    for(let k=0;k<3;k++){try{D.spawnUnit(t,'player',K.tx-6+(i%8),K.ty+9+(i/8|0));i++;}catch(e){err('SPAWN '+t+' '+e.message);}}
  step(90);

  // ---- 1. every building's command panel. Buttons here are div.btn, not <button>.
  {const skip=/tear down|demolish|quit/i; let n=0;
   for(const b of D.blds.filter(x=>x.owner==='player')){
     clear(); try{D.sel(b.id);}catch(e){err('SEL '+b.type+' '+e.message);continue;}
     const count=document.getElementById('cmds').querySelectorAll('.btn').length;
     for(let k=0;k<count;k++){
       clear(); try{D.sel(b.id);}catch(e){}
       const el=[...document.getElementById('cmds').querySelectorAll('.btn')][k]; if(!el)break;
       const label=(el.textContent||'').replace(/\s+/g,' ').trim().slice(0,26);
       if(skip.test(label))continue;
       try{el.click();n++;R.clicks++;}catch(e){err('CLICK bld '+b.type+' "'+label+'" '+e.message);}
       step(2); } }
   R.sections.buildingPanels=n;}

  // ---- 2. every unit's bar. Military commands live in #formBar, NOT #cmds — #cmds is empty for
  // a soldier and that is not a bug. Workers are the other way round.
  {let n=0;
   const pick=ids=>{clear();D.sel(null);D.selected=ids;D.refreshUI();};
   for(const t of [...new Set(D.ents.filter(e=>e.owner==='player').map(e=>e.type))]){
     const ids=D.ents.filter(e=>e.owner==='player'&&e.type===t).map(e=>e.id);
     for(const box of ['cmds','formBar']){
       pick(ids);
       const count=document.getElementById(box).querySelectorAll('.btn,button').length;
       for(let k=0;k<count;k++){
         pick(ids);
         const el=[...document.getElementById(box).querySelectorAll('.btn,button')][k]; if(!el)break;
         const label=(el.textContent||'').replace(/\s+/g,' ').trim().slice(0,24);
         try{el.click();n++;R.clicks++;}catch(e){err('CLICK unit '+t+' "'+label+'" '+e.message);}
         step(2); } } }
   clear(); R.sections.unitBars=n;}

  // ---- 3. diplomacy, every action against every realm
  {let n=0;
   for(const o of ['r1','r2','r3'])for(const fn of ['_gift','_war','_peace']){
     try{D.res.player.g=9000;window[fn](o);n++;R.clicks++;}catch(e){err('DIPLO '+fn+' '+o+' '+e.message);}
     step(3);}
   R.sections.diplomacy=n;}

  // ---- 4. the top bar and the game menu. Everything except the one that quits.
  {let n=0;
   for(const id of ['idleBtn','idleMilBtn','forcesBtn','realmsBtn','bellBtn','speedBtn','speedBtn','speedBtn',
                    'pauseBtn','pauseBtn','gmenuBtn','muteBtn','muteBtn','qualBtn','qualBtn','qualBtn',
                    'guideBtn','saveBtn','slotsClose','gmResume','demoBtn','demoBtn']){
     const el=document.getElementById(id);
     if(!el){err('MISSING button #'+id);continue;}
     try{el.click();n++;R.clicks++;}catch(e){err('BTN '+id+' '+e.message);}
     step(2);}
   clear(); R.sections.chrome=n;}

  // ---- 5. each win mode through a save and a reload. This is where b350 found the Wonder's clock
  // being dropped, so it is worth doing on every mode rather than the one that broke.
  {const modes={};
   for(const mode of ['conquest','wonder','regicide','relicrace']){
     try{
       D.winMode=mode; D.newGame(); await wait(1800); step(120);
       const before={mode:D.winMode,ents:D.ents.length,blds:D.blds.length};
       D.saveGame(); await wait(250); D.loadGame(); await wait(1600); step(60);
       modes[mode]={before,after:{mode:D.winMode,ents:D.ents.length,blds:D.blds.length},running:D.running};
       if(D.winMode!==mode)err('WINMODE '+mode+' came back as '+D.winMode+' after a reload');
       if(!D.running)err('WINMODE '+mode+' ended the game on load');
     }catch(e){err('WINMODE '+mode+' '+e.message);} }
   R.sections.winModes=modes;}

  D.winMode='conquest'; D.newGame(); await wait(1500);
  R.ok=R.errors.length===0;
  console.log('UI SWEEP — '+R.clicks+' interactions, '+R.errors.length+' errors');
  if(R.errors.length)console.log(R.errors);
  return R;
})();
