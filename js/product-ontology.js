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
    {id:'ontologystudio', name:'Ontology Studio', group:0, tag:'KNOWLEDGE', category:'KNOWLEDGE & CONTEXT', role:'기업의 지식을 연결하는 시작점', pos:[-235,-125,0], icon:'graph', description:'문서와 데이터베이스에 흩어진 정보를 엔티티와 관계로 연결합니다. 데이터는 원본에 두고, AI가 이해할 수 있는 기업의 맥락을 만듭니다.', vision:'흩어진 정보가|기업의 기억이 되는 미래.', future:'새로운 질문이 생길 때마다 데이터를 다시 모으는 대신, 이미 연결된 지식에서 답을 찾습니다.'},
    {id:'ontologic', name:'Ontologic Platform', group:0, tag:'INTELLIGENCE', category:'INTELLIGENCE & DECISION', role:'관계를 이해하고, 다음을 예측하다', pos:[-40,-220,35], icon:'diamond', description:'데이터·코드·문서를 시맨틱 레이어로 연결합니다. 자연어 질의와 원인 분석, What-if 예측으로 판단의 근거를 찾고 감시 에이전트로 변화를 포착합니다.', vision:'무슨 일이 일어났는지에서,|무엇을 할 것인지로.', future:'기업의 데이터가 설명을 넘어 예측과 의사결정으로 이어지는 데이터 인텔리전스를 지향합니다.'},
    {id:'processgpt', name:'Process GPT', group:1, tag:'AGENTIC EXECUTION', category:'AI-NATIVE ENTERPRISE', role:'AI와 사람이 함께 일하는 조직의 실행 엔진', pos:[170,-160,15], icon:'spark', description:'자연어로 업무를 정의하고 AI 에이전트와 사람의 역할을 연결합니다. MCP·A2A 기반의 에이전트가 프로세스를 실행하고, 중요한 판단은 사람이 검토합니다.', vision:'AI가 답하는 기업에서,|AI와 함께 일하는 기업으로.', future:'기업의 지식을 이해하는 에이전트와 사람이 하나의 팀으로 일하는 AI-Native Enterprise를 만듭니다.'},
    {id:'uengine6bpm', name:'uEngine6 BPM', group:1, tag:'ORCHESTRATION', category:'PROCESS & GOVERNANCE', role:'모든 실행을 하나의 업무 흐름으로', pos:[280,0,-25], icon:'flow', description:'BPMN 기반으로 업무를 모델링하고 사람·서비스·AI의 실행 흐름을 관리합니다. 이벤트와 재시도, 보상 처리를 통해 복잡한 업무의 상태와 연동을 다룹니다.', vision:'일의 구조가 자산이 되고,|변화가 일상이 되는 조직.', future:'표준화된 프로세스 위에서 사람과 AI, 로봇의 역할을 계속 개선하는 운영 체계를 지향합니다.'},
    {id:'uenginerpa', name:'uEngine RPA', group:1, tag:'AUTOMATION', category:'ROBOTIC EXECUTION', role:'반복 업무를 실제 행동으로 바꾸는 로봇', pos:[235,163,0], icon:'robot', description:'반복 업무를 말로 설명하면 AI가 자동화를 만들고, 완성된 로봇이 정해진 순서대로 실행합니다. BPM 프로세스의 한 단계로 사람의 업무와 연결됩니다.', vision:'반복은 로봇에게,|사람에게는 더 가치 있는 일.', future:'업무를 설계할 때는 AI와 협업하고, 매일의 실행은 재현 가능한 자동화로 이어갑니다.'},
    {id:'roboanalyzer', name:'Robo Analyzer', group:2, tag:'DISCOVERY', category:'LEGACY & UNDERSTANDING', role:'오래된 시스템에서 새로운 설계의 근거를', pos:[-82,82,95], icon:'scan', description:'레거시 소스 코드와 데이터베이스를 함께 분석합니다. 함수 호출과 데이터 읽기·쓰기 관계를 그래프로 탐색하고 실제 코드 원문까지 확인합니다.', vision:'읽을 수 없던 레거시가|다시 설계할 수 있는 자산으로.', future:'코드와 데이터의 연결을 이해해, 감에 의존하던 변경을 근거 있는 현대화로 바꿉니다.'},
    {id:'roboarchitect', name:'Robo Architect', group:2, tag:'SPEC-DRIVEN DESIGN', category:'AI-DRIVEN DEVELOPMENT', role:'명세에서 구현까지, 일치하는 소프트웨어', pos:[-290,65,10], icon:'layers', description:'자연어 요구사항에서 영향도 분석·구현·검증·반영으로 이어지는 Spec-Driven Development 플랫폼입니다. DDD와 BDD를 바탕으로 명세와 구현을 맞춥니다.', vision:'코드를 작성하는 속도보다,|함께 이해하는 설계의 힘.', future:'기획자·아키텍트·개발자와 AI가 하나의 명세를 기준으로 소프트웨어를 지속적으로 발전시킵니다.'},
    {id:'dreamvibe', name:'DreamVibe', group:2, tag:'HUMAN × AI', category:'AI DEVELOPMENT EXPERIENCE', role:'아이디어를 구현하는 새로운 개발 경험', pos:[128,55,-55], icon:'spark', description:'AI와의 협업으로 개발하는 바이브 코딩의 가능성을 경험합니다. 코드 작성 중심에서 벗어나, 아이디어를 구체화하고 AI와 함께 구현하는 개발 방식으로 나아갑니다.', vision:'만들고 싶은 것이 있다면,|누구나 시작할 수 있도록.', future:'사람의 상상력과 AI의 구현 역량이 만나 소프트웨어를 만드는 경험의 문턱을 낮춥니다.'},
    {id:'dxez', name:'DX Easy', group:2, tag:'MODEL TO CODE', category:'DIGITAL TRANSFORMATION', role:'비즈니스 모델에서 실행 가능한 서비스까지', pos:[-180,205,0], icon:'cube', description:'고객 여정과 비즈니스 모델, 이벤트 스토밍에서 코드 생성으로 이어집니다. Git 기반 개발과 CI, Kubernetes 배포를 연결하는 디지털 전환 플랫폼입니다.', vision:'비즈니스의 생각이|실행 가능한 서비스가 되다.', future:'기획과 설계, 개발과 배포 사이의 간극을 줄여 비즈니스 변화가 서비스에 이어지도록 합니다.'},
    {id:'uenginecloud', name:'uEngine Cloud', group:3, tag:'CLOUD OPERATIONS', category:'CLOUD-NATIVE FOUNDATION', role:'만들어진 가치를 안정적으로 전달하는 기반', pos:[35,237,10], icon:'cloud', description:'Robo Architect의 산출물을 Kubernetes에 배포하고 운영하는 오픈소스 PaaS입니다. 앱·자원 관리부터 단계적 배포, 롤백, 로그와 모니터링을 하나의 포털에서 다룹니다.', vision:'좋은 설계가 멈추지 않고,|살아 있는 서비스가 되도록.', future:'개발에서 운영까지 이어지는 클라우드 네이티브 기반으로 기업의 변화를 지속 가능한 서비스로 만듭니다.'}
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
      $('#ontology-showcase-play').setAttribute('aria-label',data.paused?'Showcase 재생':'Showcase 일시정지');
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
    [0,1,'의미 → 판단'],[0,2,'지식 → 실행'],[1,2,'판단 → 실행'],[2,3,'업무 오케스트레이션'],
    [3,4,'로봇 업무 연결'],[2,4,'반복 업무 자동화'],[5,0,'레거시 맥락'],[5,1,'코드·데이터 이해'],
    [5,6,'분석 → 설계'],[6,9,'설계 → 배포'],[7,6,'아이디어 → 명세'],[8,6,'모델 기반 설계'],
    [8,9,'개발 → 운영'],[3,9,'클라우드 실행 기반'],[6,3,'서비스 → 프로세스'],[7,8,'아이디어 → 모델']
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
    playButton.setAttribute('aria-label',playing?'자동 탐색 일시정지':'자동 탐색 재생');
    $('#ontology-tour-label').textContent=playing?'자동 탐색 중':'자유롭게 탐색하세요';
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
    $('#ontology-link').setAttribute('aria-label',p.name+' 제품 자세히 보기');
    const related=$('#ontology-related'); related.replaceChildren();
    edges.filter(e=>e[0]===selected||e[1]===selected).slice(0,2).forEach(([a,b,label])=>{
      const dest=a===selected?b:a;
      const btn=document.createElement('button');btn.type='button';btn.className='ontology-relation';
      const verb=document.createElement('span');verb.textContent=label;
      const arrow=document.createElement('i');arrow.textContent=a===selected?'→':'←';
      const name=document.createElement('span');name.textContent=products[dest].name;
      btn.append(verb,arrow,name);btn.setAttribute('aria-label',label+': '+products[dest].name+' 살펴보기');
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
    if(manual)$('#ontology-announcement').textContent=p.name+' 선택됨. '+p.role;
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
