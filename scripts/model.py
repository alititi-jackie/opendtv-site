import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
def read(path):
    return json.loads(path.read_text())
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
categories = read(DATA / 'categories.json')
sources = {s['id']: s for s in read(DATA / 'channels/sources.json')}
def https(url, hosts=None):
    p = urlsplit(url)
    if p.scheme != 'https' or not p.hostname or p.username or p.password or (hosts and p.netloc not in hosts):
        raise ValueError(f'Unexpected URL: {url}')
    return url
def player(v):
    vid = v['videoId']
    if v['platform'] == 'youtube' and re.fullmatch(r'[\w-]{11}', vid, re.ASCII):
        return 'https://www.youtube.com/embed/' + vid
    if v['platform'] == 'vimeo' and vid.isascii() and vid.isdigit():
        return 'https://player.vimeo.com/video/'+vid
    if v['platform'] == 'nps' and re.fullmatch(r'[A-F0-9]{8}(?:-[A-F0-9]{4}){2}-[A-F0-9]{4,16}(?:-[A-F0-9]{12})?', vid):
        return 'https://www.nps.gov/media/video/embed.htm?id=' + vid
    raise ValueError('Unsupported player or video ID: ' + vid)
def videos(health=None, testing=False):
    health = health or {}
    result, ids = [], set()
    for f in sorted((DATA/'videos').glob('*.json')):
        v = read(f)
        assert re.fullmatch(r'[a-z0-9-]+', v['stableId']) and f.stem == v['stableId']
        assert v['status'] in ('approved','archived','review') and v['category'] in categories
        assert (v['platform'], v['videoId']) not in ids
        ids.add((v['platform'], v['videoId']))
        state = health.get('video/'+v['stableId'], {})
        if state.get('hidden') or (not testing and state.get('playback',{}).get('failures',0)>=2) or v['status'] != 'approved':
            continue
        if state.get('metadata'):
            v.update(state['metadata'])
        assert sources[v['channelId']]['platform'] == v['platform']
        for field in ('title','originalTitle','sourceName','description','playbackCheckedAt','addedAt','publishedAt','lastCheckedAt'):
            assert v[field], (f, field)
        for field in ('playbackCheckedAt','addedAt','publishedAt','lastCheckedAt'):
            date.fromisoformat(v[field][:10])
        assert type(v['embeddable']) is bool and type(v['duration']) is int and v['duration'] > 0
        src = player(v)
        if v['platform'] == 'youtube':
            assert v['sourceUrl'] == 'https://www.youtube.com/watch?v=' + v['videoId']
            https(v['thumbnail'], ['i.ytimg.com','img.youtube.com'])
            if (date.today()-date.fromisoformat(v['lastCheckedAt'][:10])).days >= 30:
                continue
        elif v['platform']=='vimeo':
            assert v['sourceUrl']=='https://vimeo.com/'+v['videoId']
            https(v['thumbnail'],['i.vimeocdn.com'])
        else:
            assert v['sourceUrl'] == src.replace('/embed.htm','/view.htm')
            https(v['thumbnail'], ['www.nps.gov'])
        result.append(v)
    return result
