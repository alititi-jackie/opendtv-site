"""Smoke-test official embeds with Chromium and retain separate playback evidence."""
import asyncio
import functools
import http.server
import os
import shutil
import threading
from datetime import date
from playwright.async_api import async_playwright
from model import ROOT, DATA, read, write, videos

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):pass

async def main():
    report=ROOT/'health-output/state.json'
    health=read(report) if report.exists() else {}
    today=date.today()
    def days_ago(v):
        old=health.get('video/'+v['stableId'],{}).get('playback',{})
        return (today-date.fromisoformat(old.get('checked','2000-01-01'))).days
    # Retry previously hidden embeds as well so successful checks can restore them.
    queue=sorted((v for v in videos(health,testing=True) if v['embeddable'] and days_ago(v)>=
                  (1 if health.get('video/'+v['stableId'],{}).get('playback',{}).get('failures') else 7)),key=days_ago,reverse=True)[:32]
    if not queue:return
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=ROOT/'dist'))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    async with async_playwright() as p:
        opts={}
        if os.getenv('PLAYER_PROXY'):opts['proxy']={'server':os.environ['PLAYER_PROXY'],'bypass':'127.0.0.1,localhost'}
        browser=await p.chromium.launch(executable_path=os.getenv('CHROME_PATH') or shutil.which('google-chrome'),args=['--autoplay-policy=no-user-gesture-required','--no-sandbox'],**opts)
        sem=asyncio.Semaphore(4)
        async def check(v):
            async with sem:
                key='video/'+v['stableId']
                state=health.setdefault(key,{'result':'review','hidden':False,'checked':str(today),'misses':0})
                if state.get('result') in ('unavailable','external') or state.get('hidden'):return
                pg=await browser.new_page(ignore_https_errors=bool(os.getenv('PLAYER_PROXY')))
                try:
                    # Exercise the shipped click-to-load control.
                    await pg.goto(f'http://127.0.0.1:{server.server_port}/videos/watch/{v["stableId"]}/',wait_until='domcontentloaded')
                    await pg.locator('[data-player]').click(timeout=9000)
                    frame=pg.frame_locator('.frame iframe')
                    if v['platform']=='youtube':
                        await frame.get_by_role('button',name='Play video',exact=True).click(timeout=14000)
                    elif v['platform']=='vimeo':
                        await frame.get_by_role('button',name='Play',exact=True).click(timeout=22000)
                    else:
                        await frame.locator('video').first.evaluate('v=>{v.muted=true;v.play().catch(()=>{})}',timeout=14000)
                    for _ in range(26):
                        await pg.wait_for_timeout(650)
                        if await frame.locator('video').evaluate_all('xs=>xs.some(v=>v.currentTime>.3 && v.readyState>=2 && v.videoWidth>0)'):break
                    else:raise RuntimeError('No decoded frames')
                    state['playback']={'checked':str(today),'result':'played','failures':0}
                except Exception:
                    old=state.get('playback',{})
                    fails=old.get('failures',0)+int(old.get('checked')!=str(today))
                    state['playback']={'checked':str(today),'result':'review','failures':fails}
                finally:await pg.close()
        await asyncio.gather(*(check(v) for v in queue))
        await browser.close()
    server.server_close()
    write(report,health)
    print('Player results:',[(k,s['playback']['result']) for k,s in health.items() if 'playback' in s])
if __name__=='__main__':asyncio.run(main())
