"""Build the public Pages artifact. Run from any working directory."""
import html
import re
import shutil
from pathlib import Path
from urllib.parse import quote
from model import ROOT, DATA, categories, videos, read, write, https, player, json

out = ROOT / 'dist'
if out.exists():
    shutil.rmtree(out)
out.mkdir()
for name in ('assets','portal'):
    shutil.copytree(ROOT/name,out/name)
for name in ('style-v2.css','manifest.webmanifest','robots.txt','sw.js'):
    shutil.copy(ROOT/name,out/name)
base = 'https://opendtv.com'
site_desc = '汇聚全球优质视频、电视直播、影视资讯与观看指南，让精彩内容触手可及。'
nav = [('/','首页'),('/videos/','视频'),('/live/','直播'),('/movies/','影视'),('/directory/','导航'),('/guides/','指南')]
statefile = ROOT/'health-output/state.json'
health = read(statefile) if statefile.exists() else {}
directory = read(DATA/'directory.json')
live = [c for c in read(DATA/'live/channels.json') if c.get('status','approved')=='approved' and not health.get('live/'+c['id'],{}).get('hidden')]
import os
video = videos(health,testing=os.getenv('TEST_PLAYERS')=='1')
types = dict(streaming='影视平台',livetv='电视服务',apps='TV 应用',devices='电视设备')
index, sitemap = [], []
def esc(s):
    return html.escape(str(s),quote=True)
def link(url,title):
    return f'<a href="{esc(url)}">{esc(title)}</a>'
def save(url,content):
    path = out/(url.lstrip('/')+('index.html' if url.endswith('/') else ''))
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content)
def wurl(v):
    return '/videos/watch/'+v['stableId']+'/'
def curl(c):
    return '/videos/category/'+c+'/'
def lurl(c):
    return '/live/'+c['id']+'/'
def section(title,body,more=''):
    if not body: return ''
    return '<section class="shelf"><div class="shelf-head"><h2>'+esc(title)+'</h2>'+(link(more,'查看全部 →') if more else '')+'</div>'+body+'</section>'
def grid(cards):
    cards=''.join(cards)
    return '<div class="tiles">'+cards+'</div>' if cards else ''
def tile(url,title,desc):
    return f'<a class="texttile" href="{esc(url)}"><strong>{esc(title)}</strong><small>{esc(desc)}</small></a>'
def listrow(title,desc,url,kind,keywords=''):
    index.append(dict(title=title,description=desc,url=url,type=kind,keywords=keywords))
def duration(v):
    m,s=divmod(v['duration'],60)
    return f'{m}:{s:02d}'
def card(v,large=False):
    return f'<a class="{"lead" if large else "film"}" href="{wurl(v)}"><div class="cover"><img src="{esc(v["thumbnail"])}" alt="" loading="{"eager" if large else "lazy"}"><span>{duration(v)}</span></div><div class="caption"><small>{esc(categories[v["category"]])} · {esc(v["publishedAt"][:10])}</small><h3>{esc(v["title"])}</h3>{("<p>"+esc(v["description"])+"</p>") if large else ""}<small>{esc(v["sourceName"])}</small></div></a>'
def category_nav(current=''):
    return '<nav class="chips" aria-label="视频分类">'+link('/videos/','全部视频')+''.join(f'<a {"aria-current=page" if k==current else ""} href="{curl(k)}">{esc(n)}</a>' for k,n in categories.items())+'</nav>'
def actions(url='',fav=False):
    return '<div class="controls">'+(f'<button data-fav="{esc(url)}">收藏</button>' if fav else '')+'<button data-share>分享</button><button data-copy>复制链接</button></div>'
def page(url,title,desc,body,parent=None,photo='',schema=None,searchable=True,legacy=False):
    active=next((p for p,_ in nav[1:] if url.startswith(p)), '/')
    if parent and parent[0] in dict(nav):active=parent[0]
    with_crumb = url!='/'
    crumbs=[('/','首页')]+([parent] if parent and parent[0]!=url else [])+([(url,title)] if with_crumb else [])
    bread='<nav class="crumb" aria-label="面包屑">'+' <span>›</span> '.join(link(p,t) if p!=url else esc(t) for p,t in crumbs)+'</nav>' if with_crumb else ''
    structured=[{'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i,'name':t,'item':base+p} for i,(p,t) in enumerate(crumbs,1)]}] if with_crumb else []
    if schema:structured.append(schema)
    meta=''.join(f'<meta property="og:{k}" content="{esc(v)}">' for k,v in dict(title=title+'｜OpenDTV',description=desc,url=base+url,image=photo or base+'/assets/social-card.svg',type='video.other' if schema else 'website').items())
    logo='<a class="wordmark" href="/" aria-label="OpenDTV 首页"><img src="/assets/logo.svg" alt="OpenDTV"></a>'
    header='<header class="mast"><div class="mastin">'+logo+'<nav class="primary" aria-label="主导航">'+''.join(f'<a href="{p}" {"aria-current=page" if active==p else ""}>{n}</a>' for p,n in nav)+'</nav><nav class="tools">'+link('/search/','搜索')+link('/favorites/','收藏')+'<a href="https://go.openaa.com/"><b>Go.</b>OpenAA</a></nav></div></header>'
    footer='<footer class="foot"><div><strong>OpenDTV · 开放视界，发现精彩。</strong><p>全球精选视频与电视门户 · opendtv.com</p><nav>'+ '　'.join(link(p,t) for p,t in [('/about.html','关于本站'),('/legal.html#copyright','版权声明'),('/legal.html#privacy','隐私政策'),('/about.html#contact','联系我们')])+'</nav><small>本站主要提供合法视频嵌入、内容整理及官方观看入口。第三方视频的版权归原权利人所有，播放服务由相应平台提供。</small></div></footer>'
    ld=json.dumps(structured,ensure_ascii=False).replace('<',r'\u003c')
    save(url,f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}｜OpenDTV</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{base+url}">{meta}<meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/favicon.svg"><link rel="manifest" href="/manifest.webmanifest"><link rel="stylesheet" href="/style-v2.css"><link rel="stylesheet" href="/portal/site.css">'+('' if searchable else '<meta name="robots" content="noindex,follow">')+f'<script type="application/ld+json">{ld}</script><script defer src="/portal/site.js"></script></head><body>{header}<main class="shell">{bread}{body}</main>{footer}<div id="notice" role="status"></div></body></html>')
    if searchable:sitemap.append(url)
def intro(title,desc=''):
    return '<div class="intro"><h1>'+esc(title)+'</h1>'+('<p>'+esc(desc)+'</p>' if desc else '')+'</div>'
def searchform():
    return '<form class="query" action="/search/"><input type="search" name="q" aria-label="搜索关键词" placeholder="搜索视频、频道、平台或指南"><button>搜索</button></form>'
def livetiles(seq):
    return grid(tile(lurl(c),c['title'],c['category']+' · 官方观看入口') for c in seq)
def platformlist(seq,anchors=False):
    return grid(tile('/directory/'+x['id']+'/',x['name'],x['desc']).replace('<a ', '<a id="'+esc(x['id'])+'" ',1) if anchors else tile('/directory/'+x['id']+'/',x['name'],x['desc']) for x in seq)
guides=[]
def from_legacy(f):
    s=f.read_text()
    title=html.unescape(re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S)[1]).strip()
    match=re.search(r'<meta name="description" content="([^"]*)"',s); desc=html.unescape(match[1]) if match else title
    body=re.search(r'<main[^>]*>(.*?)</main>',s,re.S)[1]
    return title,desc,body
for f in sorted((ROOT/'guides').glob('*.html')):
    t,d,body=from_legacy(f);p='/guides/'+f.name;guides.append((p,t,d))
    listrow(t,d,p,'指南')
    page(p,t,d,body+actions()+section('继续浏览',grid([tile('/live/','电视直播','各频道官方观看入口'),tile('/directory/','平台导航','查找电视服务、播放器及设备')])),('/guides/','指南'))
for item in read(DATA/'guides.json'):
    p='/guides/'+item['id']+'/';t=item['title'];d=item['description']
    body=intro(t,d)+'<article class="reading">'+''.join('<h2>'+esc(h)+'</h2><p>'+esc(text)+'</p>' for h,text in item['sections'])+'</article>'
    page(p,t,d,body+actions()+section('继续阅读',grid(tile(url,name,'') for url,name in item['related'])),('/guides/','指南'))
    guides.append((p,t,d));listrow(t,d,p,'指南')
def guidetiles(seq):
    return grid(tile(p,t,d) for p,t,d in seq)
page('/guides/','实用观看指南','从选择正版平台到排查电视播放问题。',intro('实用观看指南')+guidetiles(guides))
for v in video:
    p=wurl(v);cat=v['category'];t=v['title'];d=v['description'];src=player(v)
    listrow(t,d,p,'视频',' '.join([v['originalTitle'],v['sourceName'],categories[cat],*v['tags']]))
    play=f'<button class="poster" data-player="{esc(src)}" data-platform="{v["platform"]}" aria-label="加载官方播放器"><img src="{esc(v["thumbnail"])}" alt=""><span>▶　加载官方播放器</span></button>' if v['embeddable'] else '<p>该视频需在原平台观看。</p>'
    other=[x for x in video if x!=v];same=[x for x in other if x['category']==cat]
    related=[x for x in other if x not in same][:4]
    schema=dict({'@context':'https://schema.org','@type':'VideoObject'},name=t,description=d,thumbnailUrl=v['thumbnail'],uploadDate=v['publishedAt'],duration='PT'+str(v['duration'])+'S')
    if v.get('regionRestriction'):
        rules=v['regionRestriction'];body_regions='；'.join(('仅限' if k=='allowed' else '不适用')+'地区代码 '+', '.join(codes) for k,codes in rules.items())
        play += '<p>'+esc(body_regions)+'</p>'
    if v['embeddable']:schema['embedUrl']=src
    body=intro(t)+f'<p class="meta">{link(curl(cat),categories[cat])}　·　{esc(v["sourceName"])}　·　原片发布 {esc(v["publishedAt"][:10])}　·　{duration(v)}</p>'+play+'<p id="player-status" role="status"></p>'+actions(p,True)+f'<article class="reading"><h2>关于这段视频</h2><p>{esc(d)}</p><dl><dt>原标题</dt><dd>{esc(v["originalTitle"])}</dd><dt>发布者与署名</dt><dd>{esc(v["sourceName"])} · {esc(v.get("credit",v["platform"].upper()))}</dd><dt>标签</dt><dd>{esc("、".join(v["tags"]))}</dd></dl>'+link(v['sourceUrl'],'前往原平台观看 ↗')+'　'+link('/about.html#contact','反馈播放问题')+'</article>'
    page(p,t,d,body+section('同分类视频',grid(card(x) for x in same[:4]))+section('相关推荐',grid(card(x) for x in related))+section('观看指南',guidetiles([next(g for g in guides if 'buffering' in g[0])])),(curl(cat),categories[cat]),v['thumbnail'],schema)
# Preserve a usable landing page for formerly published items under review.
for f in (DATA/'videos').glob('*.json'):
    record=read(f); path=wurl(record)
    if path not in sitemap and record['status']!='review':
        page(path,'视频暂不可用','这段视频已归档或正在复查。',intro('视频暂不可用','这段视频已归档或正在复查。')+link('/videos/','查看其他精选视频 →'),('/videos/','视频'),searchable=False)
def paged(url,title,desc,seq,body,parent=None):
    size=24
    count=max(1,(len(seq)+size-1)//size)
    for number in range(1,count+1):
        path=url if number==1 else url+'page/'+str(number)+'/'
        def dest(n):return url if n==1 else url+'page/'+str(n)+'/'
        paging='<nav class="chips" aria-label="分页">'+''.join(link(dest(n),str(n)) for n in range(1,count+1))+'</nav>' if count>1 else ''
        heading=title if number==1 else title+' · 第 '+str(number)+' 页'
        page(path,heading,desc,intro(heading)+body+grid(card(v) for v in seq[(number-1)*size:number*size])+paging,parent)
for k,n in categories.items():
    seq=sorted((v for v in video if v['category']==k),key=lambda v:v['publishedAt'],reverse=True)
    if seq:
        paged(curl(k),n,n+'精选视频与官方来源。',seq,category_nav(k),('/videos/','视频'))
    else:
        page(curl(k),n,n+'精选视频与官方来源。',intro(n)+category_nav(k)+'<p class="emptybox">这个分类暂时没有通过审核的视频。'+link('/videos/','浏览其他精选视频 →')+'</p>',('/videos/','视频'),searchable=False)
latest=sorted(video,key=lambda x:(x['publishedAt'],x['stableId']),reverse=True)
paged('/videos/','精选视频','按主题探索经过审核的精选视频。',latest,category_nav())
for c in live:
    p=lurl(c);https(c['url']);listrow(c['title'],c['description'],p,'直播',c['category'])
    page(p,c['title'],c['description'],intro(c['title'],c['description'])+f'<div class="official"><p>{esc(c["category"])} · 官方观看入口</p>{link(c["url"],"打开频道官网 ↗")}</div>'+actions(p,True)+section('相关频道',livetiles([x for x in live if x!=c and x['category']==c['category']][:4]))+section('观看指南',guidetiles([next(g for g in guides if 'free-tv' in g[0])])),('/live/','直播'))
page('/live/','电视直播','按地区与节目类型浏览官方电视直播入口。',intro('电视直播','选择频道后前往电视台官网，节目与可用地区以官方播放器为准。')+''.join(section(c,livetiles([x for x in live if x['category']==c])) for c in dict.fromkeys(x['category'] for x in live)))
for x in directory:
    p='/directory/'+x['id']+'/';u=x['url'];u=https(u) if u.startswith('https:') else '/'+u
    listrow(x['name'],x['desc'],p,'导航',' '.join([types[x['type']],*x['tags']]))
    page(p,x['name'],x['desc'],intro(x['name'],x['desc'])+'<div class="official"><p>'+esc(' · '.join(x['tags']))+'</p>'+link(u,'访问官方网站 ↗' if u.startswith('https:') else '查看使用指南 →')+'</div>'+actions(p,True)+section('相关平台与设备',platformlist([z for z in directory if z!=x and z['type']==x['type']][:4])),('/directory/','导航'))
def dirbody():
    return ''.join(section(n,platformlist(x for x in directory if x['type']==k),'/'+k+'.html') for k,n in types.items())
page('/directory/','平台导航','浏览影视平台、电视服务、播放器、投屏工具及电视设备。',intro('平台导航')+dirbody())
page('/movies/','影视天地','官方电影预告、正版免费影视与观看指南。',intro('影视天地')+section('官方预告',grid(card(v) for v in video if v['category']=='trailers'))+section('正版免费影视',platformlist(x for x in directory if x['id'] in ('tubi','plex','roku-channel','pluto')))+section('观看指南',guidetiles([g for g in guides if 'free-tv' in g[0] or 'watch-chinese' in g[0]])))
# Retain the original article bodies, IDs, relative links and parameterized catalog.
for f in sorted(ROOT.glob('*.html')):
    if f.name=='index.html':continue
    t,d,body=from_legacy(f);p='/'+f.name;parent=('/directory/','导航') if f.stem in [*types,'catalog'] else None
    if f.name=='404.html':body=intro('页面不存在')+searchform()+link('/','返回首页')
    if f.name=='guides.html':body+=section('所有指南',guidetiles(guides))
    if f.name=='catalog.html':
        body=intro(t,d)+'<nav class="chips">'+link('?type=all','全部内容')+''.join(link('?type='+k,n) for k,n in types.items())+'</nav>'+''.join('<section data-filter="'+k+'">'+section(n,platformlist((x for x in directory if x['type']==k),anchors=True))+'</section>' for k,n in types.items())
    if f.name=='about.html':
        body=body.replace('帮助海外华人更容易找到合法、公开且适合电视大屏使用的娱乐服务。',site_desc)+ '<section id="contact" class="reading"><h2>反馈与联系</h2><p>请附上页面地址、设备和问题出现的时间。公开反馈请勿填写私人资料。</p>'+link('https://github.com/alititi-jackie/opendtv-site/issues','在 GitHub 提交站点反馈 ↗')+'</section>'
    if f.name=='legal.html':
        body=body.replace('当前网站以静态内容为主','收藏与最近打开记录保存在当前浏览器，清除网站数据后会丢失。封面由来源网站提供；点击加载播放器后，第三方平台会收到播放请求。当前网站以静态内容为主')+link('https://policies.google.com/privacy','Google 隐私政策')+'　'+link('https://www.youtube.com/t/terms','YouTube 服务条款')
    page(p,t,d,body+actions(),parent,searchable=f.name!='404.html')
featured=sorted((v for v in video if v['featured']),key=lambda x:x.get('featuredOrder',100))
hero=''
if featured:
    v=featured[0]
    hero='<section class="spotlight"><div class="hero-copy"><p class="kicker">全球精选视频与电视门户</p><h1>开放视界，<br>发现精彩。</h1><p>'+site_desc+'</p>'+link('/videos/','浏览全部视频 →')+'</div>'+card(v,True)+'</section>'
home=(hero or intro('开放视界，发现精彩。',site_desc))+category_nav()+section('编辑精选',grid(card(v) for v in featured[1:5]),'/videos/')+section('最新视频',grid(card(v) for v in latest[:8]),'/videos/')+section('电视直播入口',livetiles([next((c for c in live if c['id']==i),live[0]) for i in ('cctv4','cbs','sky','cctv10')]) if live else '', '/live/')
for name,cats in [('科技与纪录片',['science','nature']),('中国风光',['china']),('世界风光',['world']),('影视预告',['trailers'])]:
    home+=section(name,grid(card(v) for v in [v for v in video if v['category'] in cats][:4]),curl(cats[0]))
home+=section('实用观看指南',guidetiles(guides[:4]),'/guides/')+section('影视平台导航',platformlist(directory[:4]),'/directory/')
old=from_legacy(ROOT/'index.html')[2]
# The original bundles live with the platforms.
if '推荐组合' in old:
    bundles=next((s for s in re.findall(r'<section\b.*?</section>',old,re.S) if '推荐组合' in s),'')
    dest=out/'directory/index.html';dest.write_text(dest.read_text().replace('</main>',bundles+'</main>'))
page('/','OpenDTV 全球精选视频与电视门户',site_desc,home or intro('开放视界，发现精彩。'))
page('/search/','站内搜索','查找视频、直播、平台和指南。',intro('站内搜索')+searchform()+'<div id="results" aria-live="polite"></div>',searchable=False)
page('/favorites/','我的收藏','本机收藏及最近打开的播放器。',intro('我的收藏','收藏和记录仅保存在当前浏览器。清除网站数据或更换设备后无法恢复。')+'<div id="saved"></div><h2>最近观看</h2><p>仅列出官方播放器已确认开始播放的视频。</p><button data-clear-watched>清除观看记录</button><div id="watched"></div><h2>最近打开的播放器</h2><p>按点击加载播放器的时间排列。</p><button data-clear>清除最近记录</button><div id="recent"></div>',searchable=False)
write(out/'search-index.json',index)
(out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+base+p+'</loc></url>' for p in sitemap)+'</urlset>')
import hashlib
stamp=hashlib.sha256(b''.join(f.read_bytes() for f in sorted(out.rglob('*')) if f.is_file())).hexdigest()[:12]
sw=out/'sw.js';sw.write_text(sw.read_text().replace('BUILD_ID',stamp))
(out/'.nojekyll').touch()
print(f'{len(video)} videos, {len(live)} channels, {len(index)} index entries, {len(sitemap)} sitemap URLs')
