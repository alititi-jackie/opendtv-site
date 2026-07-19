const items=[
{id:'netflix',type:'streaming',icon:'N',name:'Netflix',desc:'覆盖电影、剧集、纪录片与原创内容的订阅流媒体平台。',tags:['订阅','多设备'],url:'https://www.netflix.com/'},
{id:'disney',type:'streaming',icon:'D+',name:'Disney+',desc:'迪士尼、皮克斯、漫威、星球大战等品牌内容平台。',tags:['订阅','家庭'],url:'https://www.disneyplus.com/'},
{id:'prime-video',type:'streaming',icon:'P',name:'Prime Video',desc:'Amazon 旗下影视服务，提供订阅内容及单片租购。',tags:['订阅','租购'],url:'https://www.primevideo.com/'},
{id:'max',type:'streaming',icon:'M',name:'Max',desc:'电影、剧集、纪录片和品牌原创内容平台。',tags:['订阅','影视'],url:'https://www.max.com/'},
{id:'hulu',type:'streaming',icon:'H',name:'Hulu',desc:'以美国剧集、电视节目和点播影视为主的流媒体服务。',tags:['订阅','美国'],url:'https://www.hulu.com/'},
{id:'tubi',type:'streaming',icon:'T',name:'Tubi',desc:'由广告支持的免费电影和电视剧点播平台。',tags:['免费','广告支持'],url:'https://tubitv.com/'},
{id:'youtube',type:'streaming',icon:'▶',name:'YouTube',desc:'视频、直播、频道与电视端应用覆盖广泛。',tags:['免费','多设备'],url:'https://www.youtube.com/'},
{id:'iqiyi',type:'streaming',icon:'爱',name:'爱奇艺国际版',desc:'面向海外用户的华语影视与综艺平台。',tags:['华语','海外版'],url:'https://www.iq.com/'},
{id:'pluto',type:'livetv',icon:'P',name:'Pluto TV',desc:'提供广告支持的免费直播频道和点播内容。',tags:['免费','直播频道'],url:'https://pluto.tv/'},
{id:'plex',type:'livetv',icon:'P',name:'Plex Live TV',desc:'Plex 提供的免费直播频道与点播内容入口。',tags:['免费','电视'],url:'https://www.plex.tv/watch-free-tv/'},
{id:'sling-freestream',type:'livetv',icon:'S',name:'Sling Freestream',desc:'Sling 提供的免费频道与点播内容服务。',tags:['免费','美国'],url:'https://www.sling.com/freestream'},
{id:'roku-channel',type:'livetv',icon:'R',name:'The Roku Channel',desc:'Roku 的免费影视与直播频道服务，地区可用性不同。',tags:['免费','Roku'],url:'https://therokuchannel.roku.com/'},
{id:'youtube-tv',type:'livetv',icon:'YT',name:'YouTube TV',desc:'美国市场的付费网络电视服务，包含多个直播频道。',tags:['付费','美国'],url:'https://tv.youtube.com/'},
{id:'fubo',type:'livetv',icon:'F',name:'Fubo',desc:'以体育和电视直播为重点的订阅服务。',tags:['付费','体育'],url:'https://www.fubo.tv/'},
{id:'directv-stream',type:'livetv',icon:'D',name:'DIRECTV STREAM',desc:'提供多种电视直播套餐的网络电视服务。',tags:['付费','电视'],url:'https://streamtv.directv.com/'},
{id:'pbs',type:'livetv',icon:'PBS',name:'PBS',desc:'美国公共电视内容及部分地区直播入口。',tags:['公共电视','美国'],url:'https://www.pbs.org/'},
{id:'kodi',type:'apps',icon:'K',name:'Kodi',desc:'开源媒体中心，可管理本地媒体及合法插件。',tags:['开源','播放器'],url:'https://kodi.tv/'},
{id:'vlc',type:'apps',icon:'V',name:'VLC',desc:'跨平台开源媒体播放器，支持多种音视频格式。',tags:['开源','播放器'],url:'https://www.videolan.org/vlc/'},
{id:'plex-app',type:'apps',icon:'P',name:'Plex',desc:'整理个人媒体库并在电视、手机和电脑间播放。',tags:['媒体库','多设备'],url:'https://www.plex.tv/'},
{id:'jellyfin',type:'apps',icon:'J',name:'Jellyfin',desc:'开源自建媒体服务器与客户端方案。',tags:['开源','自建'],url:'https://jellyfin.org/'},
{id:'air-screen',type:'apps',icon:'A',name:'AirScreen',desc:'电视端无线投屏接收工具，支持多种投屏协议。',tags:['投屏','电视端'],url:'https://airscreen.app/'},
{id:'smarttube',type:'apps',icon:'ST',name:'SmartTube',desc:'第三方 Android TV 客户端；安装前应核对项目来源与风险。',tags:['Android TV','第三方'],url:'https://github.com/yuliskov/SmartTube'},
{id:'apple-tv-app',type:'apps',icon:'',name:'Apple TV App',desc:'Apple 的影视内容入口，可用于订阅、租购及频道服务。',tags:['官方','Apple'],url:'https://www.apple.com/apple-tv-app/'},
{id:'google-tv-app',type:'apps',icon:'G',name:'Google TV',desc:'Google 的影视聚合与设备管理体验。',tags:['官方','Google'],url:'https://tv.google/'},
{id:'fire-tv-stick',type:'devices',icon:'F',name:'Fire TV Stick',desc:'适合日常流媒体观看，应用生态丰富，安装和使用简单。',tags:['入门','Amazon'],url:'https://www.amazon.com/firetv/'},
{id:'apple-tv-4k',type:'devices',icon:'',name:'Apple TV 4K',desc:'性能流畅，适合 Apple 生态及重视体验的用户。',tags:['高端','Apple'],url:'https://www.apple.com/apple-tv-4k/'},
{id:'google-tv-streamer',type:'devices',icon:'G',name:'Google TV Streamer',desc:'Google TV 生态设备，适合使用 Google 服务的家庭。',tags:['Google TV','家庭'],url:'https://store.google.com/category/streaming'},
{id:'roku',type:'devices',icon:'R',name:'Roku',desc:'界面简单、频道生态成熟，适合美国电视用户。',tags:['易用','美国'],url:'https://www.roku.com/products/players'},
{id:'onn',type:'devices',icon:'O',name:'onn. Google TV',desc:'主打性价比的 Google TV 设备系列。',tags:['性价比','Google TV'],url:'https://www.walmart.com/browse/electronics/onn-streaming-devices/3944_1229875_4536_3315120'},
{id:'shield',type:'devices',icon:'N',name:'NVIDIA SHIELD TV',desc:'性能较强，适合本地媒体、串流和高级用户。',tags:['高性能','Android TV'],url:'https://www.nvidia.com/en-us/shield/'},
{id:'smart-tv',type:'devices',icon:'TV',name:'智能电视内置系统',desc:'无需额外盒子，但应用更新与性能取决于电视品牌和年份。',tags:['一体化','新手'],url:'guides.html#choose-device'},
{id:'ethernet',type:'devices',icon:'↔',name:'网络与 HDMI 配件',desc:'稳定网络、合适的 HDMI 规格和供电可改善大屏体验。',tags:['配件','网络'],url:'guides.html#network'}
];

const labels={streaming:['影视平台','订阅、免费点播与华语内容'],livetv:['电视服务','合法直播频道与网络电视服务'],apps:['TV 应用','播放器、媒体库、投屏与官方应用'],devices:['电视设备','流媒体盒子、智能电视与配件'],all:['全部内容','浏览 OpenDTV 收录的所有条目']};

function isExternal(url){return /^https?:\/\//.test(url)}
function card(i){const external=isExternal(i.url);return `<article class="card" id="${i.id}"><div class="card-icon">${i.icon}</div><h3>${i.name}</h3><p>${i.desc}</p><div class="tags">${i.tags.map(t=>`<span class="tag">${t}</span>`).join('')}</div><a class="button" href="${i.url}" ${external?'target="_blank" rel="noopener noreferrer"':''}>${external?'访问官方网站 ↗':'查看使用指南 →'}</a></article>`}

function renderHome(){const el=document.querySelector('#featuredGrid');if(el)el.innerHTML=['tubi','pluto','iqiyi','fire-tv-stick','apple-tv-4k','kodi','plex','roku'].map(id=>card(items.find(i=>i.id===id))).join('')}

function updateCatalogHeading(type){const title=document.querySelector('#catalogTitle'),intro=document.querySelector('#catalogIntro');if(title)title.textContent=labels[type][0];if(intro)intro.textContent=labels[type][1];document.title=`${labels[type][0]}｜OpenDTV`;setActiveNav(type)}

function highlightHashTarget(){const id=decodeURIComponent(location.hash.slice(1));if(!id)return;requestAnimationFrame(()=>{const target=document.getElementById(id);if(!target)return;target.scrollIntoView({behavior:'smooth',block:'center'});target.classList.add('card-highlight');setTimeout(()=>target.classList.remove('card-highlight'),2200)})}

function renderCatalog(){const grid=document.querySelector('#catalogGrid');if(!grid)return;const q=new URLSearchParams(location.search);let type=q.get('type')||'all';if(!labels[type])type='all';const types=['all','streaming','livetv','apps','devices'];const filters=document.querySelector('#filters');filters.innerHTML=types.map(t=>`<button class="filter ${t===type?'active':''}" data-type="${t}">${labels[t][0]}</button>`).join('');const draw=t=>{grid.innerHTML=(t==='all'?items:items.filter(i=>i.type===t)).map(card).join('')||'<div class="empty">没有找到内容</div>';updateCatalogHeading(t);highlightHashTarget()};draw(type);filters.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;document.querySelectorAll('.filter').forEach(x=>x.classList.remove('active'));b.classList.add('active');history.replaceState(null,'',`?type=${b.dataset.type}`);draw(b.dataset.type)})}

function setupSearch(){const form=document.querySelector('#searchForm'),input=document.querySelector('#searchInput'),box=document.querySelector('#searchResults');if(!form)return;form.addEventListener('submit',e=>{e.preventDefault();const k=input.value.trim().toLowerCase();if(!k){box.hidden=true;return}const found=items.filter(i=>[i.name,i.desc,...i.tags].join(' ').toLowerCase().includes(k)).slice(0,8);box.innerHTML=found.length?found.map(i=>`<a href="catalog.html?type=${i.type}#${i.id}"><b>${i.name}</b><br><small>${i.desc}</small></a>`).join(''):'<div class="empty">暂时没有找到相关内容</div>';box.hidden=false})}

function getPageInfo(){const path=location.pathname.toLowerCase();const params=new URLSearchParams(location.search);if(path==='/'||path.endsWith('/index.html'))return {key:'home',label:'首页'};if(path.endsWith('/catalog.html')){const type=params.get('type')||'all';return {key:labels[type]?type:'all',label:labels[type]?.[0]||'全部内容'}}if(path.endsWith('/guides.html'))return {key:'guides',label:'使用指南'};if(path.endsWith('/about.html'))return {key:'about',label:'关于与联系'};if(path.endsWith('/legal.html'))return {key:'legal',label:'法律说明'};return {key:'other',label:'当前页面'}}

function setActiveNav(key=getPageInfo().key){document.querySelectorAll('.header nav a').forEach(a=>{a.classList.remove('active');a.removeAttribute('aria-current')});let selector='';if(key==='home')selector='a[data-nav="home"]';else if(key==='streaming'||key==='livetv'||key==='apps'||key==='devices')selector=`a[href*="type=${key}"]`;else if(key==='guides')selector='a[href="guides.html"]';const active=document.querySelector(`.header nav ${selector}`);if(active){active.classList.add('active');active.setAttribute('aria-current','page')}}

function setupGlobalNavigation(){document.querySelectorAll('a.brand').forEach(a=>{a.href='/';a.title='返回首页'});const nav=document.querySelector('.header nav');if(nav&&!nav.querySelector('[data-nav="home"]'))nav.insertAdjacentHTML('afterbegin','<a href="/" data-nav="home">首页</a>');setActiveNav();const info=getPageInfo();const heroWrap=document.querySelector('.page-hero .wrap');if(heroWrap&&info.key!=='home'&&!heroWrap.querySelector('.breadcrumb'))heroWrap.insertAdjacentHTML('afterbegin',`<nav class="breadcrumb" aria-label="面包屑"><a href="/">首页</a><span>›</span><span aria-current="page">${info.label}</span></nav>`);const footer=document.querySelector('footer');if(footer&&info.key!=='home'&&!document.querySelector('.page-actions'))footer.insertAdjacentHTML('beforebegin','<div class="wrap page-actions"><a href="/">← 返回首页</a><a href="catalog.html?type=all">浏览全部内容 →</a></div>')}

function setupMenu(){const b=document.querySelector('.menu'),n=document.querySelector('.header nav');if(!b||!n)return;b.setAttribute('aria-expanded','false');const close=()=>{n.classList.remove('open');b.textContent='☰';b.setAttribute('aria-expanded','false')};b.addEventListener('click',e=>{e.stopPropagation();const open=n.classList.toggle('open');b.textContent=open?'×':'☰';b.setAttribute('aria-expanded',String(open))});n.addEventListener('click',e=>{if(e.target.closest('a'))close()});document.addEventListener('click',e=>{if(!n.contains(e.target)&&e.target!==b)close()});document.addEventListener('keydown',e=>{if(e.key==='Escape')close()})}

function setupBackToTop(){const button=document.createElement('button');button.className='back-to-top';button.type='button';button.setAttribute('aria-label','返回顶部');button.textContent='↑';document.body.appendChild(button);const update=()=>button.classList.toggle('show',scrollY>500);addEventListener('scroll',update,{passive:true});update();button.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}))}

setupGlobalNavigation();renderHome();renderCatalog();setupSearch();setupMenu();setupBackToTop();
