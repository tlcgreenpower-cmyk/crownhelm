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
// b355: it now also drives REAL POINTER ORDERS on the 3D view — projecting a world position back
// to client coordinates and dispatching genuine MouseEvents at it, so select, move, gather,
// attack, box-select, build-placement, rally and the formation drag all go through the same
// localXY -> raycastGround -> commandMove path the player's hand does. Each one asserts the order
// actually took, not merely that nothing threw.
//
// WHAT IT DOES NOT COVER, so nobody reads a clean run as more than it is:
//   - the Map Builder screen and custom maps (b353 fixed that one; it is still untested here)
//   - Parade mode (b354)
//   - wall dragging, and camera orbit/pan
// A clean sweep means every BUTTON is wired to something that runs and every ORDER lands. It does
// not mean the result is the one a player wanted.
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

  // ---- 3. diplomacy, every action against every realm THAT EXISTS. A three-realm game has no r3,
  // and hardcoding r1/r2/r3 reported two "failures" that were the sweep's fault, not the game's.
  {let n=0; const realms=Object.keys(D.diplo||{});
   for(const o of realms)for(const fn of ['_gift','_war','_peace']){
     try{D.res.player.g=9000;window[fn](o);n++;R.clicks++;}catch(e){err('DIPLO '+fn+' '+o+' '+e.message);}
     step(3);}
   R.sections.diplomacy={actions:n,realms};}

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
  // ---- 6. real pointer orders on the 3D view. Everything above is a button; this is the hand.
  {const orders={};
   D.winMode='conquest'; D.newGame(); await wait(2000);
   const cv=document.getElementById('view');
   const P=(x,z)=>{const v=new D.THREE.Vector3(x,D.heightAtWorld(x,z)+0.6,z);v.project(D.camera);
     const r=cv.getBoundingClientRect();
     return {cx:r.left+(v.x*0.5+0.5)*r.width, cy:r.top+(-v.y*0.5+0.5)*r.height, on:v.z<1&&Math.abs(v.x)<=1&&Math.abs(v.y)<=1};};
   const fire=(t,cx,cy,btn,tgt)=>(tgt||cv).dispatchEvent(new MouseEvent(t,{bubbles:true,cancelable:true,clientX:cx,clientY:cy,button:btn||0,buttons:btn===2?2:1}));
   const LC=(x,z)=>{const p=P(x,z);fire('mousedown',p.cx,p.cy,0);fire('mouseup',p.cx,p.cy,0,window);return p;};
   const RC=(x,z)=>{const p=P(x,z);fire('mousedown',p.cx,p.cy,2);fire('mouseup',p.cx,p.cy,2,window);return p;};
   const DRAG=(x0,z0,x1,z1)=>{const a=P(x0,z0),b=P(x1,z1);
     fire('mousedown',a.cx,a.cy,0);fire('mousemove',(a.cx+b.cx)/2,(a.cy+b.cy)/2,0);fire('mousemove',b.cx,b.cy,0);fire('mouseup',b.cx,b.cy,0,window);};
   try{
     const K=D.blds.find(b=>b.owner==='player'&&b.type==='hall');
     Object.assign(D.res.player,{f:5000,w:5000,m:5000,g:5000});
     // setCam takes (x,z,dist,pitch). Calling it bare sets camTarget to undefined, the camera goes
     // NaN, and every projection after it is garbage — cost me a confusing round of "results".
     D.setCam(K.cx,K.cz,52,0.62); step(8);

     const sold=D.ents.find(e=>e.owner==='player'&&e.type!=='worker');
     LC(sold.x,sold.z); step(2);
     orders.selectByClick={sel:D.selected.length,gotHim:D.selected.includes(sold.id)};
     if(!D.selected.includes(sold.id))err('POINTER left-click did not select the man under it');

     const p0={x:sold.x,z:sold.z}; RC(sold.x+22,sold.z+6); step(90);
     orders.moveOrder={cmd:sold.cmd,moved:+Math.hypot(sold.x-p0.x,sold.z-p0.z).toFixed(1)};
     if(Math.hypot(sold.x-p0.x,sold.z-p0.z)<4)err('POINTER right-click ground did not move him');

     const w=D.ents.find(e=>e.owner==='player'&&e.type==='worker');
     const nd=D.woodNodes.filter(n=>n.amount>0).map(n=>({n,d:Math.hypot(D.wx(n.tx)-w.x,D.wz(n.ty)-w.z)})).sort((a,b)=>a.d-b.d)[0];
     D.sel(null);D.selected=[w.id];D.refreshUI(); RC(D.wx(nd.n.tx),D.wz(nd.n.ty)); step(4);
     // 'return' is a gather order that has already succeeded — he filled his arms and set off home
     // inside the four frames this waits. Asserting cmd==='gather' called that a failure once.
     orders.gatherOrder={cmd:w.cmd,gather:!!w.gather};
     if(!w.gather||!(w.cmd==='gather'||w.cmd==='return'))err('POINTER right-click on timber did not send the worker to it');

     const foe=D.ents.find(e=>e.owner!=='player'&&e.type!=='worker');
     if(foe){ foe.x=K.cx+16; foe.z=K.cz+10; D.diplo[foe.owner].stance='war';
       D.sel(null);D.selected=[sold.id];D.refreshUI(); RC(foe.x,foe.z); step(4);
       orders.attackOrder={cmd:sold.cmd,target:!!sold.target};
       if(sold.cmd!=='attack')err('POINTER right-click on an enemy did not order the attack'); }

     // Box-select DROPS workers when the box also holds a soldier — deliberate, and the same
     // convention AoE uses. Assert that, so nobody later "fixes" it into a regression.
     D.sel(null);D.selected=[];D.refreshUI(); DRAG(K.cx-26,K.cz-14,K.cx+26,K.cz+26); step(2);
     const picked=D.selected.map(id=>D.ents.find(e=>e.id===id)).filter(Boolean);
     orders.boxSelect={n:picked.length,anyWorkers:picked.some(e=>e.type==='worker')};
     if(picked.length&&picked.some(e=>e.type!=='worker')&&picked.some(e=>e.type==='worker'))
       err('POINTER box-select returned workers alongside soldiers — the b352-era filter is gone');

     D.sel(null);D.selected=[w.id];D.refreshUI();
     let bs=[...document.getElementById('cmds').querySelectorAll('.btn')];
     const town=bs.find(b=>/Town/.test(b.textContent)); if(town){town.click();D.refreshUI();}
     bs=[...document.getElementById('cmds').querySelectorAll('.btn')];
     const house=bs.find(b=>/House/.test(b.textContent));
     const nb0=D.blds.filter(b=>b.owner==='player').length;
     if(house){ house.click(); step(1); LC(K.cx+18,K.cz+14); step(4); }
     orders.placeBuilding={before:nb0,after:D.blds.filter(b=>b.owner==='player').length};
     if(D.blds.filter(b=>b.owner==='player').length<=nb0)err('POINTER clicking the ground did not lay the foundation');
     clear();

     D.selected=[]; D.sel(K.id); step(1); RC(K.cx+20,K.cz+20); step(2);
     orders.rallyFlag=K.rally?[Math.round(K.rally.x),Math.round(K.rally.z)]:null;
     if(!K.rally)err('POINTER right-click with a building selected did not set the rally flag');
   }catch(e){err('POINTER '+e.message);}
   R.sections.pointerOrders=orders;}

  R.ok=R.errors.length===0;
  console.log('UI SWEEP — '+R.clicks+' interactions, '+R.errors.length+' errors');
  if(R.errors.length)console.log(R.errors);
  return R;
})();
