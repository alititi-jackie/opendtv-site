"""Build-time availability report. Temporary failures are recorded for review."""
import argparse
import os
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError
from urllib.request import urlopen, Request
from urllib.parse import urlsplit
from html import unescape
from model import ROOT, DATA, json, read, write, re, player, https
from catalog_ops import api, metadata

today=date.today()
def inspect_url(url,marker=None,image=False):
    https(url)
    try:
        with urlopen(Request(url,headers={'User-Agent':'OpenDTV link check (+https://opendtv.com/about.html)'}),timeout=12) as r:
            raw=r.read(1024 if image else 512000)
            if image:
                return 'ok' if r.headers.get_content_type().startswith('image/') or raw.startswith((bytes.fromhex('ffd8'),b'RIFF',b'\x89PNG')) else 'review'
            text=unescape(raw.decode('utf-8','replace'))
            if marker and marker.casefold() not in text.casefold():return 'review'
            if re.search(r'<title[^>]*>[^<]*(access denied|just a moment|301 moved|page not found|robot check)',text,re.I):return 'review'
            return 'ok'
    except HTTPError as exc:return 'missing' if exc.code in (404,410) else 'review'
    except (OSError,ValueError):return 'review'
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--previous');args=parser.parse_args()
    prev=read(__import__('pathlib').Path(args.previous)) if args.previous else {}
    state={}
    def record(key,result):
        old=prev.get(key,{})
        previous=old.get('checked')!=str(today)
        missing=(old.get('misses',0)+int(previous) if result=='missing' else 0 if result=='ok' else old.get('misses',0))
        hidden=(result=='unavailable' or missing>=2 or (old.get('hidden',False) and result not in ('ok','external')))
        state[key]=dict(old,checked=str(today),result=result,misses=missing,hidden=hidden)
        if result=='unavailable':state[key].pop('metadata',None)
    jobs={}
    records=[read(f) for f in (DATA/'videos').glob('*.json')]
    yt=[v for v in records if v['platform']=='youtube' and v['status']=='approved']
    def due(key):
        return not prev.get(key) or (today-date.fromisoformat(prev[key]['checked'])).days>=7 or prev[key]['result'] not in ('ok','external')
    for v in records:
        if v['status']!='approved':continue
        key='video/'+v['stableId']
        if not due(key):
            state[key]=prev[key];continue
        if v['platform']=='youtube':continue
        def check(v=v):
            if v['platform']=='vimeo':
                metadata_url='https://vimeo.com/api/oembed.json?url='+v['sourceUrl']
                results=[inspect_url(metadata_url,v['videoId']),inspect_url(v['thumbnail'],image=True)]
            else:
                results=[inspect_url(v['sourceUrl'],v['originalTitle'].strip()),inspect_url(v['thumbnail'],image=True)]
            if v['embeddable']:results.append(inspect_url(player(v),'video'))
            return 'missing' if 'missing' in results else 'review' if 'review' in results else 'ok'
        jobs[key]=check
    for c in read(DATA/'live/channels.json'):
        jobs['live/'+c['id']]=lambda c=c:inspect_url(c['url'],c['match'])
    for x in read(DATA/'directory.json'):
        key='directory/'+x['id']
        if not x['url'].startswith('https://'):continue
        if due(key):jobs[key]=lambda x=x:inspect_url(x['url'])
        else:state[key]=prev[key]
    with ThreadPoolExecutor(max_workers=6) as pool:
        for key,result in zip(jobs,pool.map(lambda fn:fn(),jobs.values())):record(key,result)
    waiting=[v for v in yt if due('video/'+v['stableId'])]
    for i in range(0,len(waiting),50):
        chunk=waiting[i:i+50]
        if not os.getenv('YOUTUBE_API_KEY'):
            for v in chunk:record('video/'+v['stableId'],'review')
            continue
        items={x['id']:x for x in api('videos',part='snippet,status,contentDetails',id=','.join(v['videoId'] for v in chunk))}
        for v in chunk:
            key='video/'+v['stableId'];item=items.get(v['videoId'])
            fresh=metadata(item) if item else None
            if not fresh or fresh['channelId']!=v['channelId']:record(key,'unavailable');continue
            record(key,'ok' if fresh['embeddable'] else 'external')
            state[key]['metadata']=fresh
    write(ROOT/'health-output/state.json',state)
    print('Checked',len(jobs),'URLs or groups;',sum(v['hidden'] for v in state.values()),'hidden.')
if __name__=='__main__':main()
