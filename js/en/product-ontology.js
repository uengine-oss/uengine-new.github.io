/* Conceptual product relationships, grounded in the product pages.
 * No framework, WebGL dependency, or external asset is required. */
(function () {
  'use strict';
  const root = document.querySelector('.ontology-hero');
  if (!root) return;
  const $ = (s) => root.querySelector(s);
  const svg = $('#ontology-map');
  const ns = 'http://www.w3.org/2000/svg';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const colors = ['#66eee0', '#ad97ff', '#81b5ff', '#ffc383'];
  // The edges describe a solution architecture, not a promise of prebuilt integrations.
  const products = [
    {id:'ontologystudio', name:'Ontology Studio', group:0, tag:'KNOWLEDGE', category:'KNOWLEDGE & CONTEXT', role:'The starting point for connecting enterprise knowledge', pos:[-235,-125,0], icon:'graph', description:'Connects information scattered across documents and databases as entities and relationships. Data stays at its source while we build the enterprise context AI can understand.', vision:'A future where scattered information|becomes your enterprise\'s memory.', future:'Instead of gathering data all over again for every new question, find answers in knowledge that is already connected.'},
    {id:'ontologic', name:'Ontologic Platform', group:0, tag:'INTELLIGENCE', category:'INTELLIGENCE & DECISION', role:'Understand relationships, predict what comes next', pos:[-40,-220,35], icon:'diamond', description:'Connects data, code, and documents through a semantic layer. Natural-language queries, root-cause analysis, and what-if predictions ground your decisions, while monitoring agents catch changes as they happen.', vision:'From what happened,|to what to do next.', future:'We pursue data intelligence where enterprise data goes beyond description to drive prediction and decision-making.'},
    {id:'processgpt', name:'Process GPT', group:1, tag:'AGENTIC EXECUTION', category:'AI-NATIVE ENTERPRISE', role:'The execution engine for organizations where AI and people work together', pos:[170,-160,15], icon:'spark', description:'Define work in natural language and connect the roles of AI agents and people. MCP- and A2A-based agents execute the process, while people review the decisions that matter.', vision:'From an enterprise where AI answers,|to an enterprise where AI works alongside you.', future:'We build the AI-Native Enterprise, where agents that understand your company\'s knowledge and your people work as one team.'},
    {id:'uengine6bpm', name:'uEngine6 BPM', group:1, tag:'ORCHESTRATION', category:'PROCESS & GOVERNANCE', role:'Every execution in a single workflow', pos:[280,0,-25], icon:'flow', description:'Models work on BPMN and manages the execution flow across people, services, and AI. Events, retries, and compensation handling keep complex work\'s state and integrations under control.', vision:'An organization where the structure of work is an asset,|and change is everyday practice.', future:'We pursue an operating model that continuously refines the roles of people, AI, and robots on top of standardized processes.'},
    {id:'uenginerpa', name:'uEngine RPA', group:1, tag:'AUTOMATION', category:'ROBOTIC EXECUTION', role:'Robots that turn repetitive work into real action', pos:[235,163,0], icon:'robot', description:'Describe a repetitive task in words and AI builds the automation; the finished robot then runs it in the defined order. It plugs into human work as a step in a BPM process.', vision:'Repetition goes to robots,|more valuable work goes to people.', future:'Collaborate with AI when designing the work, then carry daily execution forward with reproducible automation.'},
    {id:'roboanalyzer', name:'Robo Analyzer', group:2, tag:'DISCOVERY', category:'LEGACY & UNDERSTANDING', role:'Grounds for new design, drawn from old systems', pos:[-82,82,95], icon:'scan', description:'Analyzes legacy source code and databases together. Explore function calls and data read/write relationships as a graph, all the way down to the original code.', vision:'Legacy that could not be read|becomes an asset that can be redesigned.', future:'By understanding how code and data connect, we turn changes once made on gut feeling into evidence-based modernization.'},
    {id:'roboarchitect', name:'Robo Architect', group:2, tag:'SPEC-DRIVEN DESIGN', category:'AI-DRIVEN DEVELOPMENT', role:'From spec to implementation, software that stays aligned', pos:[-290,65,10], icon:'layers', description:'A Spec-Driven Development platform that runs from natural-language requirements through impact analysis, implementation, verification, and rollout. It keeps spec and implementation aligned on a foundation of DDD and BDD.', vision:'Not the speed of writing code,|but the power of a design everyone understands.', future:'Planners, architects, developers, and AI continuously evolve software against a single shared spec.'},
    {id:'dreamvibe', name:'DreamVibe', group:2, tag:'HUMAN × AI', category:'AI DEVELOPMENT EXPERIENCE', role:'A new development experience for bringing ideas to life', pos:[128,55,-55], icon:'spark', description:'Experience the possibilities of vibe coding, developing in collaboration with AI. Move beyond code-centric work toward a way of building where you shape ideas and implement them together with AI.', vision:'If there is something you want to build,|anyone should be able to start.', future:'Human imagination meets AI\'s ability to build, lowering the barrier to creating software.'},
    {id:'dxez', name:'DX Easy', group:2, tag:'MODEL TO CODE', category:'DIGITAL TRANSFORMATION', role:'From business model to runnable service', pos:[-180,205,0], icon:'cube', description:'Flows from customer journeys, business models, and EventStorming straight into code generation. A digital transformation platform that connects Git-based development, CI, and Kubernetes deployment.', vision:'Business thinking|becomes a runnable service.', future:'We close the gaps between planning, design, development, and deployment so business change carries through to the service.'},
    {id:'uenginecloud', name:'uEngine Cloud', group:3, tag:'CLOUD OPERATIONS', category:'CLOUD-NATIVE FOUNDATION', role:'The foundation for reliably delivering the value you build', pos:[35,237,10], icon:'cloud', description:'An open-source PaaS that deploys and operates Robo Architect\'s output on Kubernetes. Handle app and resource management, staged rollouts, rollbacks, logs, and monitoring from a single portal.', vision:'So that good design never stalls,|and becomes a living service.', future:'On a cloud-native foundation that spans development to operations, we turn enterprise change into sustainable services.'}
  ];
  // Showcase flow: orchestration/agents → ontology → legacy data → development.
  // Keep graph indices stable so changing the tour cannot change its relationships.
  const tourOrder=['processgpt','uengine6bpm','uenginerpa','ontologystudio','ontologic',
    'roboanalyzer','roboarchitect','dreamvibe','dxez','uenginecloud']
    .map(id=>products.findIndex(product=>product.id===id));
  const introduced=new Set();
  let tourComplete=false;
  const showcase=$('#ontology-showcase'),showcaseFrame=$('#ontology-showcase-frame');
  const showcaseLaunch=$('#ontology-showcase-launch'),showcaseClose=$('#ontology-showcase-close');
  const universe=$('#ontology-universe'),stage=$('#ontology-stage');
  let showcaseReturnFocus=null,showcaseState='universe',foldElapsed=0,showcaseReady=false;
  const foldDuration=1500;
  function sendShowcase(command,extra={}) {
    if(showcaseReady)showcaseFrame.contentWindow.postMessage({type:'uengine-showcase-command',command,...extra},location.origin);
  }
  function syncShowcaseVisibility() {sendShowcase('visibility',{suspended:!sceneReady||!visible||document.hidden});}
  function beginShowcase() {
    showcaseState='showcase';universe.hidden=true;
    root.classList.remove('is-folding');root.classList.add('is-showcase');
    stage.style.height=showcase.offsetHeight+'px';
    if(showcaseReady){
      showcase.classList.add('is-ready');$('#ontology-showcase-loading').hidden=true;
      sendShowcase('start',{suspended:!sceneReady||!visible||document.hidden,reduced:reduced.matches});
    }
    if(showcaseReturnFocus)showcaseClose.focus({preventScroll:true});
  }
  function openShowcase(event,immediate=false) {
    if(showcaseState!=='universe')return;
    showcaseReturnFocus=(event||universe.contains(document.activeElement))?document.activeElement:null;
    pause();
    stage.style.height=universe.offsetHeight+'px';
    showcaseState='folding';foldElapsed=0;showcaseReady=false;
    universe.inert=true;showcase.hidden=false;
    if(!immediate)root.classList.add('is-folding');
    showcaseFrame.src='contents/showcase.html?mode=short&inline=1';
    if(immediate||reduced.matches)beginShowcase();else startFrame();
  }
  function closeShowcase() {
    if(showcaseState==='universe')return;
    showcaseState='universe';showcaseReady=false;foldElapsed=0;
    // Unload all scene timers and videos when returning to the product graph.
    showcaseFrame.removeAttribute('src');showcase.hidden=true;showcase.classList.remove('is-ready');
    $('#ontology-showcase-loading').hidden=false;
    universe.hidden=false;universe.inert=false;stage.style.height='';
    root.classList.remove('is-folding','is-showcase');
    render();startFrame();
    const target=showcaseReturnFocus&&showcaseReturnFocus.isConnected?showcaseReturnFocus:showcaseLaunch;
    target.focus({preventScroll:true});
  }
  root.querySelectorAll('[data-showcase-launch]').forEach(button=>button.addEventListener('click',openShowcase));
  showcaseClose.addEventListener('click',closeShowcase);
  root.querySelectorAll('[data-showcase-command]').forEach(button=>button.addEventListener('click',()=>sendShowcase(button.dataset.showcaseCommand)));
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&showcaseState!=='universe'){event.preventDefault();closeShowcase();}});
  window.addEventListener('message',event=>{
    if(event.origin!==location.origin||event.source!==showcaseFrame.contentWindow||showcaseState==='universe')return;
    const data=event.data||{};
    if(data.type==='uengine-showcase-ready'){
      showcaseReady=true;
      if(showcaseState==='showcase')beginShowcase();
    }else if(data.type==='uengine-showcase-return')closeShowcase();
    else if(data.type==='uengine-showcase-state'){
      $('#ontology-showcase-scene').textContent=data.label;
      $('#ontology-showcase-play').textContent=data.paused?'▶':'Ⅱ';
      $('#ontology-showcase-play').setAttribute('aria-label',data.paused?'Play Showcase':'Pause Showcase');
    }
  });
  new ResizeObserver(()=>{if(showcaseState==='showcase')stage.style.height=showcase.offsetHeight+'px';}).observe(showcase);
  function advanceTour(manual) {
    if(!manual){
      introduced.add(selected);
      if(introduced.size===tourOrder.length){tourComplete=true;openShowcase();return;}
    }
    choose(tourOrder[(tourOrder.indexOf(selected)+1)%tourOrder.length],manual);
  }
  const edges = [
    [0,1,'Meaning → Judgment'],[0,2,'Knowledge → Execution'],[1,2,'Judgment → Execution'],[2,3,'Work orchestration'],
    [3,4,'Robot task integration'],[2,4,'Repetitive task automation'],[5,0,'Legacy context'],[5,1,'Code & data understanding'],
    [5,6,'Analysis → Design'],[6,9,'Design → Deployment'],[7,6,'Idea → Spec'],[8,6,'Model-driven design'],
    [8,9,'Development → Operations'],[3,9,'Cloud execution foundation'],[6,3,'Service → Process'],[7,8,'Idea → Model']
  ];
  const icons = {
    graph:'M-9-7L9-7 0 10ZM-9-7L0 0 9-7M0 0V10 M-12-10h6v6h-6z M6-10h6v6H6z M-3 7h6v6h-6z',
    diamond:'M0-13L12 0 0 13-12 0ZM0-6L6 0 0 6-6 0Z',
    spark:'M0-14L4-4 14 0 4 4 0 14-4 4-14 0-4-4Z',
    flow:'M-12-10h8v8h-8z M4 2h8v8H4z M-8-2v8H4 M-4-6h12v8',
    robot:'M-10-7h20v17h-20z M0-12v5 M-5 0h1 M4 0h1 M-4 6h8 M-14-2v7 M14-2v7',
    scan:'M-12-4v-8h8 M4-12h8v8 M12 4v8H4 M-4 12h-8V4 M-6-3l-4 3 4 3 M6-3l4 3-4 3 M2-5l-4 10',
    layers:'M0-12L13-5 0 2-13-5Z M-13 1L0 8 13 1 M-13 7L0 14 13 7',
    cube:'M0-13L12-6V7L0 14-12 7V-6ZM-12-6L0 1 12-6M0 1V14',
    cloud:'M-9 9C-19 8-17-3-10-3C-10-15 9-15 10-3C20-3 19 9 10 9Z M0-4V5 M-4 1L0 5 4 1'
  };
  function make(tag, attrs, parent) {
    const el = document.createElementNS(ns, tag);
    Object.entries(attrs || {}).forEach(([k,v]) => el.setAttribute(k,v));
    if (parent) parent.appendChild(el);
    return el;
  }
  const starGroup = $('.ontology-space');
  // Deterministic stars keep the scene light and visually stable.
  for (let i=0;i<95;i++) {
    make('circle',{cx:(i*137.51)%820,cy:(i*83.17)%590,r:i%7===0?1.15:.6,fill:i%3?'#9baecb':'#78ede4',opacity:.12+(i%5)*.08},starGroup);
  }
  const orbitGroup = $('.ontology-orbits');
  const orbitPaths = [0,1,2].map(() => make('path',{fill:'none',stroke:'#5b97b8','stroke-width':.65,'stroke-opacity':.24},orbitGroup));
  const orbitBeams = [0,1,2].map((_,i) => make('path',{class:'ontology-orbit-beam',stroke:colors[i],opacity:.5,'stroke-dasharray':'55 1100','pathLength':1155},orbitGroup));
  const center = $('.ontology-center');
  const rays=make('g',{class:'ontology-core-rays'},center);
  for(let i=0;i<48;i++){
    const a=i*Math.PI/24;
    make('path',{d:`M${Math.cos(a)*70} ${Math.sin(a)*70}L${Math.cos(a)*(i%4?73:80)} ${Math.sin(a)*(i%4?73:80)}`},rays);
  }
  make('circle',{r:145,fill:'url(#ontology-halo)'},center);
  make('ellipse',{rx:53,ry:53,fill:'none',stroke:'#71cbd5','stroke-opacity':.18},center);
  make('ellipse',{rx:62,ry:62,fill:'none',stroke:'#71cbd5','stroke-opacity':.09,'stroke-dasharray':'2 6'},center);
  make('circle',{cy:-21,r:15,fill:'url(#ontology-core)'},center);
  make('circle',{cy:-21,r:4,fill:'#b9fff0',filter:'url(#ontology-glow)'},center);
  make('text',{y:12,class:'ontology-core-label'},center).textContent='uEngine';
  make('text',{y:28,class:'ontology-core-sub'},center).textContent='CONNECTED INTELLIGENCE';
  const edgeGroup = $('.ontology-edges');
  const edgeViews = edges.map(([a,b,label]) => ({
    a,b,label,
    path:make('path',{class:'ontology-edge'},edgeGroup),
    particle:make('circle',{r:2.2,fill:'#b9fff6'},edgeGroup),
    arrow:make('path',{d:'M-4-3L2 0-4 3',fill:'none','stroke-width':1},edgeGroup),
    text:make('text',{class:'ontology-edge-label','text-anchor':'middle'},edgeGroup)
  }));
  edgeViews.forEach(e => { e.text.textContent=e.label; });
  const nodeGroup = $('.ontology-nodes');
  const nav = $('.ontology-product-nav');
  const nodeViews = products.map((p,i) => {
    const g = make('g',{class:'ontology-node',role:'button',tabindex:'0','aria-label':p.name+' — '+p.role,'aria-pressed':'false','data-product':p.id,style:'--node-color:'+colors[p.group]},nodeGroup);
    make('title',{},g).textContent=p.name+' · '+p.role;
    make('circle',{r:43,class:'ontology-node-hit'},g);
    const aura=make('circle',{r:37,class:'ontology-node-aura'},g);
    const ring=make('circle',{r:33,class:'ontology-node-ring'},g);
    const shell=make('circle',{r:25,class:'ontology-node-shell'},g);
    make('path',{d:icons[p.icon],class:'ontology-node-symbol'},g);
    const name=make('text',{y:47,class:'ontology-node-name'},g);name.textContent=p.name;
    const tag=make('text',{y:61,class:'ontology-node-role'},g);tag.textContent=p.tag;
    g.addEventListener('click',() => { if (!dragged) choose(i,true); });
    g.addEventListener('keydown',e => { if (e.key==='Enter'||e.key===' ') {e.preventDefault();choose(i,true);} });
    const button = document.createElement('button');
    button.type='button'; button.innerHTML='<span>'+String(tourOrder.indexOf(i)+1).padStart(2,'0')+'</span> '+p.name;
    button.setAttribute('aria-pressed','false');button.addEventListener('click',()=>choose(i,true));nav.appendChild(button);
    return {g,aura,ring,shell,name,tag,button};
  });
  tourOrder.forEach(index=>nav.appendChild(nodeViews[index].button));
  let selected=tourOrder[0], playing=!reduced.matches, visible=true, dragging=false, dragged=false;
  const restingPitch=.32, restingYaw=-.12, diagonalTilt=-.18;
  let angleY=restingYaw, angleX=restingPitch, orbitAngle=0;
  let targetZoom=1, zoom=1, focus=0, targetFocus=0;
  let pointer=null, lastX=0, lastY=0, startX=0, startY=0, elapsed=0, lastTime=0, frameId=0;
  let rotationTime=0, frameTime=0;
  const duration=8500;
  const introDuration=5200, introSpeed=4.75, cruisingSpeed=.035;
  let introElapsed=reduced.matches?introDuration:0;
  const pageLoader=document.querySelector('.page-loader');
  let sceneReady=!pageLoader||getComputedStyle(pageLoader).display==='none';
  if(!sceneReady){
    // A Showcase opening also waits for the page loader before its first layer builds.
    const loaderObserver=new MutationObserver(()=>{
      if(getComputedStyle(pageLoader).display!=='none')return;
      sceneReady=true;loaderObserver.disconnect();syncShowcaseVisibility();
    });
    loaderObserver.observe(pageLoader,{attributes:true,attributeFilter:['style','class']});
  }
  function finishIntro() {
    if(introElapsed===introDuration)return;
    introElapsed=introDuration;
    targetZoom=1.13;targetFocus=1;
  }
  function advanceRotation(dt) {
    const before=introElapsed/introDuration;
    const next=Math.min(introDuration,introElapsed+dt);
    const after=next/introDuration;
    // Crossfade the axes over the last 1.2 seconds of the entrance. Integrating
    // smoothstep keeps both angular velocities continuous across the handoff.
    const rampIntegral=t=>{
      const u=Math.max(0,Math.min(1,(t-(introDuration-1200))/1200));
      return 1200*(u*u*u-.5*u*u*u*u);
    };
    const orbitTime=rampIntegral(next)-rampIntegral(introElapsed)+dt-(next-introElapsed);
    const spinTime=dt-orbitTime;
    const delta=cruisingSpeed*spinTime/1000+
      (introSpeed-cruisingSpeed)*introDuration/4000*
      (Math.pow(1-before,4)-Math.pow(1-after,4));
    const previousYaw=angleY;
    // Entrance: the existing mouse-drag axes. Afterwards these angles stay put.
    angleY=(angleY+delta)%(Math.PI*2);
    angleX=Math.max(-.75,Math.min(.75,angleX+.10*(Math.sin(angleY)-Math.sin(previousYaw))));
    // Steady motion: the original slow orbit within the tilted elliptical plane.
    orbitAngle=(orbitAngle+cruisingSpeed*orbitTime/1000)%(Math.PI*2);
    if(before<1&&after===1)finishIntro();
    else introElapsed=next;
  }
  const playButton=$('#ontology-play');
  function updatePlayback() {
    playButton.textContent=playing?'Ⅱ':'▶';
    playButton.setAttribute('aria-label',playing?'Pause auto-tour':'Resume auto-tour');
    $('#ontology-tour-label').textContent=playing?'Auto-touring':'Explore freely';
    root.classList.toggle('is-paused',!playing);
    $('#ontology-announcement').textContent='';
  }
  function pause() {playing=false;finishIntro();updatePlayback();}
  function choose(i,manual) {
    selected=(i+products.length)%products.length;
    const p=products[selected];
    if(manual){pause();introduced.clear();tourComplete=false;}
    elapsed=0;targetFocus=1;targetZoom=1.13;
    root.style.setProperty('--ont-accent',colors[p.group]);
    $('.ontology-detail').style.setProperty('--ont-accent',colors[p.group]);
    $('#ontology-category').textContent=p.category;
    $('#ontology-index').textContent=String(tourOrder.indexOf(selected)+1).padStart(2,'0')+' / '+tourOrder.length;
    $('#ontology-role').textContent=p.role;
    $('#ontology-product').textContent=p.name;
    $('#ontology-description').textContent=p.description;
    $('#ontology-vision-title').replaceChildren();
    p.vision.split('|').forEach((line,j)=>{if(j)$('#ontology-vision-title').appendChild(document.createElement('br'));$('#ontology-vision-title').appendChild(document.createTextNode(line));});
    $('#ontology-vision-body').textContent=p.future;
    $('#ontology-link').href='contents/'+p.id+'.html';
    $('#ontology-link').setAttribute('aria-label',p.name+' View product details');
    const related=$('#ontology-related'); related.replaceChildren();
    edges.filter(e=>e[0]===selected||e[1]===selected).slice(0,2).forEach(([a,b,label])=>{
      const dest=a===selected?b:a;
      const btn=document.createElement('button');btn.type='button';btn.className='ontology-relation';
      const verb=document.createElement('span');verb.textContent=label;
      const arrow=document.createElement('i');arrow.textContent=a===selected?'→':'←';
      const name=document.createElement('span');name.textContent=products[dest].name;
      btn.append(verb,arrow,name);btn.setAttribute('aria-label',label+': '+products[dest].name+' Explore');
      btn.addEventListener('click',()=>choose(dest,true));related.appendChild(btn);
    });
    nodeViews.forEach((v,j)=>{
      const active=j===selected;
      v.g.classList.toggle('is-selected',active);v.g.setAttribute('aria-pressed',String(active));v.button.setAttribute('aria-pressed',String(active));
      v.shell.setAttribute('r',active?40:24);v.ring.setAttribute('r',active?52:31);v.aura.setAttribute('r',active?68:35);
      v.name.setAttribute('y',active?69:45);v.tag.setAttribute('y',active?84:59);
    });
    const content=$('#ontology-detail-content');content.classList.remove('ontology-content-enter');
    // Restart a brief entrance transition without hiding content from assistive technology.
    void content.offsetWidth;content.classList.add('ontology-content-enter');
    if(manual)$('#ontology-announcement').textContent=p.name+' selected. '+p.role;
    if(reduced.matches){zoom=targetZoom;focus=targetFocus;render();}
  }
  function project(pos) {
    const [px,py,z]=pos;
    const co=Math.cos(orbitAngle),so=Math.sin(orbitAngle),aspect=.78;
    const x=px*co-py/aspect*so, y=px*aspect*so+py*co;
    // Mouse dragging still controls the view of this same inclined plane.
    const cy=Math.cos(angleY),sy=Math.sin(angleY),cx=Math.cos(angleX),sx=Math.sin(angleX);
    const rx=x*cy+z*sy, rz=-x*sy+z*cy;
    const ry=y*cx-rz*sx, depth=y*sx+rz*cx;
    const perspective=1000/(1000-depth);
    const cr=Math.cos(diagonalTilt),sr=Math.sin(diagonalTilt);
    return {x:(rx*cr-ry*sr)*perspective,y:(rx*sr+ry*cr)*perspective,z:depth};
  }
  function render() {
    const anchor=project(products[selected].pos);
    // Camera moves toward the chosen product while preserving its surrounding context.
    const shiftX=-anchor.x*.22*focus,shiftY=-anchor.y*.18*focus;
    const fold=showcaseState==='folding'?Math.min(1,foldElapsed/foldDuration):0;
    const collapse=1-(fold*fold*(3-2*fold));
    const sceneScale=(window.innerWidth<=480?.84:1)*collapse;
    orbitGroup.style.opacity=String(collapse*collapse);
    $('.ontology-edges').style.opacity=String(collapse*collapse);
    starGroup.style.opacity=String(collapse);
    center.style.opacity=String(Math.min(1,collapse*3));
    const point = pos => {const p=project(pos);return {x:410+(p.x+shiftX)*zoom*sceneScale,y:284+(p.y+shiftY)*zoom*sceneScale,z:p.z};};
    const points=products.map(p=>point(p.pos));
    const origin=point([0,0,0]);center.setAttribute('transform',`translate(${origin.x} ${origin.y}) scale(${.15+.85*collapse})`);
    orbitPaths.forEach((path,k)=>{
      let d='';
      for(let j=0;j<=90;j++){
        const a=j/90*Math.PI*2,tilt=(k-1)*.6;
        const p=point([Math.cos(a)*(315+k*20),Math.sin(a)*230*Math.cos(tilt),Math.sin(a)*230*Math.sin(tilt)]);
        d+=(j?'L':'M')+p.x.toFixed(1)+' '+p.y.toFixed(1);
      }
      path.setAttribute('d',d+'Z');
      orbitBeams[k].setAttribute('d',d+'Z');
      orbitBeams[k].setAttribute('stroke-dashoffset',-rotationTime*.035-k*370);
    });
    edgeViews.forEach((e,j)=>{
      const a=points[e.a],b=points[e.b],active=e.a===selected||e.b===selected;
      const dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy)||1;
      const insetA=e.a===selected?45:29,insetB=e.b===selected?45:29;
      const ax=a.x+dx/len*insetA,ay=a.y+dy/len*insetA,bx=b.x-dx/len*insetB,by=b.y-dy/len*insetB;
      e.path.setAttribute('d',`M${ax} ${ay}L${bx} ${by}`);
      e.path.setAttribute('stroke',active?colors[products[selected].group]:'#52728e');e.path.setAttribute('opacity',active?.65:.16);
      e.path.setAttribute('stroke-dasharray',active?'none':'3 6');
      const t=(rotationTime/3100+j*.173)%1;
      e.particle.setAttribute('cx',ax+(bx-ax)*t);e.particle.setAttribute('cy',ay+(by-ay)*t);
      e.particle.setAttribute('opacity',active?.9:.13);e.particle.setAttribute('r',active?2.4:1.2);
      e.arrow.setAttribute('transform',`translate(${bx} ${by}) rotate(${Math.atan2(dy,dx)*180/Math.PI})`);
      e.arrow.setAttribute('stroke',active?colors[products[selected].group]:'#52728e');e.arrow.setAttribute('opacity',active?.9:.2);
      e.text.setAttribute('x',(ax+bx)/2);e.text.setAttribute('y',(ay+by)/2-8);
      // Only nearby relation labels are shown, keeping the network readable.
      e.text.setAttribute('opacity',active&&len>135&&introElapsed===introDuration?1:0);
    });
    nodeViews.forEach((v,i)=>{
      const p=points[i];v.g.setAttribute('transform',`translate(${p.x.toFixed(2)} ${p.y.toFixed(2)}) scale(${collapse})`);
      v.g.style.opacity=String(collapse*(i===selected?1:Math.max(.58,Math.min(1,.86+p.z/900))));
    });
    $('.ontology-progress span').style.transform='scaleX('+Math.min(1,elapsed/duration)+')';
  }
  function tick(time) {
    frameId=0;
    if(!visible||document.hidden||showcaseState==='showcase')return;
    const dt=lastTime?Math.min(time-lastTime,64):16;lastTime=time;
    if(showcaseState==='folding'){
      foldElapsed+=dt;render();
      if(foldElapsed>=foldDuration){beginShowcase();return;}
      frameId=requestAnimationFrame(tick);return;
    }
    // Let the entrance begin after the existing page loader has revealed the scene.
    if(!sceneReady)sceneReady=getComputedStyle(pageLoader).display==='none';
    if(playing&&!dragging&&sceneReady){
      if(introElapsed===introDuration)elapsed+=dt;
      if(!reduced.matches){rotationTime+=dt;advanceRotation(dt);}
      if(elapsed>=duration)advanceTour(false);
      if(showcaseState!=='universe')return;
    }
    const blend=reduced.matches?1:1-Math.exp(-dt/550);
    zoom+=(targetZoom-zoom)*blend;focus+=(targetFocus-focus)*blend;
    frameTime+=dt;
    if(frameTime>=32||dragging){render();frameTime=0;}
    if(showcaseState!=='showcase'&&(!reduced.matches||playing||showcaseState==='folding'))frameId=requestAnimationFrame(tick);
  }
  function startFrame(){if(!frameId&&visible&&!document.hidden&&showcaseState!=='showcase'){lastTime=0;frameId=requestAnimationFrame(tick);}}
  function camera(action) {
    pause();
    if(action==='reset'){angleX=restingPitch;angleY=restingYaw;orbitAngle=0;targetZoom=1;targetFocus=0;}
    else targetZoom=Math.max(.72,Math.min(1.8,targetZoom+(action==='in'?.16:-.16)));
    if(reduced.matches){zoom=targetZoom;focus=targetFocus;render();}
  }
  root.querySelectorAll('[data-camera]').forEach(btn=>btn.addEventListener('click',()=>camera(btn.dataset.camera)));
  $('#ontology-prev').addEventListener('click',()=>choose(tourOrder[(tourOrder.indexOf(selected)-1+tourOrder.length)%tourOrder.length],true));
  $('#ontology-next').addEventListener('click',()=>advanceTour(true));
  playButton.addEventListener('click',()=>{
    if(!playing&&tourComplete){introduced.clear();tourComplete=false;choose(tourOrder[0],false);}
    playing=!playing;elapsed=0;if(!playing)finishIntro();updatePlayback();
    startFrame();
  });
  svg.addEventListener('pointerdown',e=>{
    if(e.button!==0||pointer!==null)return;
    pointer=e.pointerId;startX=lastX=e.clientX;startY=lastY=e.clientY;dragged=false;
  });
  svg.addEventListener('pointermove',e=>{
    if(e.pointerId!==pointer)return;
    if(!dragging&&Math.hypot(e.clientX-startX,e.clientY-startY)<5)return;
    if(!dragging){dragging=true;dragged=true;pause();svg.setPointerCapture(e.pointerId);svg.classList.add('is-dragging');}
    angleY+=(e.clientX-lastX)*.005;angleX=Math.max(-.75,Math.min(.75,angleX+(e.clientY-lastY)*.004));
    lastX=e.clientX;lastY=e.clientY;render();
  });
  function endDrag(e){
    if(e.pointerId!==pointer)return;
    if(svg.hasPointerCapture(e.pointerId))svg.releasePointerCapture(e.pointerId);
    dragging=false;pointer=null;svg.classList.remove('is-dragging');
    // A click following a drag must not select a product accidentally.
    setTimeout(()=>{dragged=false;},0);
  }
  svg.addEventListener('pointerup',endDrag);svg.addEventListener('pointercancel',endDrag);
  window.addEventListener('pointerup',endDrag);
  svg.addEventListener('wheel',e=>{
    // Modified wheel zoom leaves ordinary page scrolling intact.
    if(!e.ctrlKey&&!e.metaKey)return;
    e.preventDefault();camera(e.deltaY<0?'in':'out');
  },{passive:false});
  svg.addEventListener('keydown',e=>{
    if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','+','-'].includes(e.key))return;
    e.preventDefault();pause();
    if(e.key==='Home')camera('reset');
    else if(e.key==='+'||e.key==='-')camera(e.key==='+'?'in':'out');
    else {angleY+=e.key==='ArrowLeft'?-.12:e.key==='ArrowRight'?.12:0;angleX+=e.key==='ArrowUp'?-.1:e.key==='ArrowDown'?.1:0;render();}
  });
  const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;syncShowcaseVisibility();if(visible)startFrame();else if(frameId){cancelAnimationFrame(frameId);frameId=0;}},{threshold:.08});
  observer.observe(root);
  window.addEventListener('resize',render);
  document.addEventListener('visibilitychange',()=>{syncShowcaseVisibility();if(document.hidden){cancelAnimationFrame(frameId);frameId=0;}else startFrame();});
  // Keyboard reading pauses the tour so content cannot change under focus.
  $('.ontology-detail').addEventListener('focusin',e=>{if(!e.target.closest('.ontology-tour-buttons'))pause();});
  reduced.addEventListener('change',()=>{if(reduced.matches){if(showcaseState==='folding')beginShowcase();pause();cancelAnimationFrame(frameId);frameId=0;render();}else startFrame();});
  choose(tourOrder[0],false);
  // Reveal the whole universe first, then bring the first product into focus.
  if(!reduced.matches){targetZoom=.96;zoom=.96;targetFocus=0;}
  updatePlayback();render();
  // Choose afresh on each page load; direct Showcase entry skips the folding transition.
  if(Math.random()<.5)openShowcase(null,true);
  else startFrame();
})();
