"""Verify every local navigational link, asset path, canonical and video detail."""
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin, unquote
from xml.etree import ElementTree as ET
from model import ROOT, read
from pathlib import Path

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[];self.ids=set();self.canonical=[];self.h1=0;self.noindex=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='meta' and a.get('name')=='robots' and 'noindex' in a.get('content',''):self.noindex=True
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
        for field in ('href','src'):
            if a.get(field):self.links.append(a[field])
out=ROOT/'dist';pages={}
for f in out.rglob('*.html'):
    p='/'+f.relative_to(out).as_posix()
    if p.endswith('/index.html'):p=p[:-10]
    parser=Page();parser.feed(f.read_text());pages[p]=parser
errors=[]
for p,t in pages.items():
    if t.h1!=1 or t.canonical!=['https://opendtv.com'+p]:errors.append((p,'heading or canonical'))
    for href in t.links:
        u=urlsplit(urljoin('https://opendtv.com'+p,href))
        if u.netloc!='opendtv.com':continue
        path=unquote(u.path)
        if path.endswith('/index.html'):path=path[:-10]
        if path not in pages and not (out/path.lstrip('/')).is_file():errors.append((p,href))
        if u.fragment and path in pages and unquote(u.fragment) not in pages[path].ids:errors.append((p,href))
for f in list(ROOT.glob('*.html'))+list((ROOT/'guides').glob('*.html')):
    if not (out/f.relative_to(ROOT)).exists():errors.append(('legacy',str(f)))
urls={x.text for x in ET.parse(out/'sitemap.xml').findall('.//{*}loc')}
assert urls=={'https://opendtv.com'+p for p,t in pages.items() if not t.noindex}
assert all(row['url'] in pages for row in read(out/'search-index.json'))
if errors:raise SystemExit(str(errors))
print('PASS:',len(pages),'static pages; internal links, anchors, SEO and original routes.')
