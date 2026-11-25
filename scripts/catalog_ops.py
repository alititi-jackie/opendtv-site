"""Manual candidate import, editorial review and bounded YouTube uploads discovery."""
import argparse
import os
from datetime import date, datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from model import DATA, ROOT, json, sources, read, write, videos, re

def api(resource, **params):
    key = os.getenv('YOUTUBE_API_KEY')
    if not key:
        raise SystemExit('YOUTUBE_API_KEY is absent; use manual import.')
    url = 'https://www.googleapis.com/youtube/v3/'+resource+'?'+urlencode(params)
    # Keep the credential out of URLs, error text and logs.
    req = Request(url, headers={'X-Goog-Api-Key':key})
    with urlopen(req,timeout=15) as response:
        return json.load(response)['items']

def metadata(item):
    s,details,status=item['snippet'],item['contentDetails'],item['status']
    if status['privacyStatus']!='public' or status.get('uploadStatus')!='processed' or s['channelId'] not in sources:
        return None
    h,m,sec = re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',details['duration']).groups()
    seconds = int(h or 0)*3600+int(m or 0)*60+int(sec or 0)
    if not seconds or s.get('liveBroadcastContent','none')!='none':return None
    vid=item['id']
    return dict(videoId=vid,platform='youtube',originalTitle=s['title'],sourceName=s['channelTitle'],
                sourceUrl='https://www.youtube.com/watch?v='+vid,channelId=s['channelId'],
                thumbnail=s['thumbnails'].get('high',s['thumbnails']['default'])['url'],
                publishedAt=s['publishedAt'],duration=seconds,embeddable=status['embeddable'],
                regionRestriction=details.get('regionRestriction',{}),lastCheckedAt=str(date.today()))

def fetch():
    if not os.getenv('YOUTUBE_API_KEY'):
        print('SKIPPED: YouTube credential not configured; no candidates fetched.')
        return
    channels=[s for s in sources.values() if s['platform']=='youtube'][:10]
    known={(v['platform'],v['videoId']) for v in (read(f) for f in (DATA/'videos').glob('*.json'))}
    result=[]
    for channel in channels:
        info=api('channels',part='contentDetails',id=channel['id'])
        if not info:continue
        uploads=info[0]['contentDetails']['relatedPlaylists']['uploads']
        batch=api('playlistItems',part='contentDetails',playlistId=uploads,maxResults=10)
        ids=[i['contentDetails']['videoId'] for i in batch if ('youtube',i['contentDetails']['videoId']) not in known]
        if not ids:continue
        for item in api('videos',part='snippet,status,contentDetails',id=','.join(ids)):
            v=metadata(item)
            if v and v['channelId']==channel['id'] and v['embeddable']:
                v.update(category=channel['category'],status='review',title='',description='',tags=[],featured=False)
                result.append(v)
                if len(result)==10:break
        if len(result)==10:break
    write(ROOT/'review-output/candidates.json',result)
    print(f'{len(result)} unapproved candidates; no publication.')
def edit(action,path):
    v=read(path)
    dest=DATA/'videos'/(v['stableId']+'.json')
    if not re.fullmatch(r'[a-z0-9-]+',v['stableId']):raise ValueError('Invalid stable ID')
    if action=='import' and dest.exists():raise ValueError('ID already exists')
    if action=='approve':
        if not dest.exists() or read(dest)['status']!='review':raise ValueError('Import for review first')
        if read(dest)['videoId']!=v['videoId']:raise ValueError('Candidate identity changed')
        if not v.get('playbackCheckedAt') or not v.get('description') or not v.get('title'):raise ValueError('Editorial review and playback evidence required')
    before=dest.read_bytes() if dest.exists() else None
    v['status']='review' if action=='import' else 'approved'
    write(dest,v)
    try: videos()
    except BaseException:
        if before is None:dest.unlink()
        else:dest.write_bytes(before)
        raise
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['fetch','import','approve']);parser.add_argument('file',nargs='?',type=__import__('pathlib').Path)
    args=parser.parse_args()
    if args.action=='fetch':fetch()
    elif args.file:edit(args.action,args.file)
    else:parser.error('Supply one completed JSON object')
