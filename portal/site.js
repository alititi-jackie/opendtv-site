'use strict';
const $ = selector => document.querySelector(selector);
const pagePath = location.pathname;
const keys = { saved: 'opendtv.saved.v1', recent: 'opendtv.opened.v1' };
let toastTimer;
function notify(message) {
  $('#notice').textContent = message;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => $('#notice').textContent = '', 3500);
}
function stored(key) {
  try {
    const data = JSON.parse(localStorage.getItem(key) || '[]');
    return Array.isArray(data) ? data.filter(path => typeof path === 'string') : [];
  } catch { return []; }
}
function remember(key, paths) {
  try { localStorage.setItem(key, JSON.stringify(paths)); return true; }
  catch { notify('浏览器未能保存，请检查本机存储设置。'); return false; }
}
function syncFavorite() {
  const button = $('[data-fav]');
  if (button) {
    const saved = stored(keys.saved).includes(button.dataset.fav);
    button.textContent = saved ? '取消收藏' : '收藏';
    button.setAttribute('aria-pressed', String(saved));
  }
}
function node(tag, text) {
  const el = document.createElement(tag);
  el.textContent = text;
  return el;
}
function showRows(target, rows, removable = false) {
  for (const entry of rows) {
    const row = node('div','');
    row.className = 'result';
    const a = node('a',entry.title);
    a.href = entry.url;
    a.append(node('small',entry.description));
    row.append(a);
    if (removable) {
      const button = node('button','取消收藏');
      button.className = 'remove';
      button.addEventListener('click', () => {
        if (remember(keys.saved,stored(keys.saved).filter(x => x !== entry.url))) renderLists();
      });
      row.append(button);
    }
    target.append(row);
  }
}
let catalog;
async function entries() {
  if (!catalog) {
    const r = await fetch('/search-index.json');
    if (!r.ok) throw Error();
    catalog = await r.json();
  }
  return catalog;
}
async function renderLists() {
  const data = await entries();
  const map = new Map(data.map(row => [row.url,row]));
  for (const [slot,key] of [['saved',keys.saved],['recent',keys.recent]]) {
    const target = document.getElementById(slot);
    target.replaceChildren();
    const rows = stored(key).map(p => map.get(p)).filter(Boolean);
    if (rows.length) showRows(target,rows,slot === 'saved');
    else target.textContent = slot === 'saved' ? '还没有收藏。' : '还没有打开过播放器。';
  }
}
async function search() {
  const q = (new URL(location.href).searchParams.get('q') || '').trim();
  $('[name=q]').value = q;
  const target = $('#results');
  if (!q) {target.textContent = '输入关键词查找内容。'; return;}
  const words = q.toLocaleLowerCase().split(/\s+/);
  const rows = (await entries()).filter(x => {
    const text = [x.title,x.description,x.keywords,x.type].join(' ').toLocaleLowerCase();
    return words.every(w => text.includes(w));
  });
  for (const type of ['视频','直播','导航','指南']) {
    const matches = rows.filter(x => x.type === type);
    if (!matches.length) continue;
    target.append(node('h2',type+' · '+matches.length));
    showRows(target,matches);
  }
  if (!rows.length) target.textContent='没有找到相关内容，可以换用来源、分类或较短的关键词。';
}
async function copyLink() {
  try { await navigator.clipboard.writeText(location.href); notify('链接已复制'); }
  catch { window.prompt('复制此链接', location.href); }
}
document.addEventListener('click',async e => {
  const b = e.target.closest('button');
  if (!b) return;
  if (b.hasAttribute('data-fav')) {
    const p=b.dataset.fav, list=stored(keys.saved);
    if (remember(keys.saved,list.includes(p) ? list.filter(x=>x!==p) : [p,...list])) syncFavorite();
  } else if (b.hasAttribute('data-player')) {
    const u = new URL(b.dataset.player);
    if (!['https://www.nps.gov','https://www.youtube.com','https://player.vimeo.com'].includes(u.origin)) return;
    const wrap=node('div',''), frame=document.createElement('iframe');
    wrap.className='frame'; frame.title=document.querySelector('h1').textContent;
    frame.allowFullscreen=true; frame.allow='encrypted-media; picture-in-picture; fullscreen';
    frame.referrerPolicy='strict-origin-when-cross-origin'; frame.src=u.href;
    b.replaceWith(wrap); wrap.append(frame);
    remember(keys.recent,[pagePath,...stored(keys.recent).filter(x=>x!==pagePath)].slice(0,80));
    $('#player-status').textContent='请在官方播放器内按播放。如播放器受地区或浏览器限制，可使用下方原平台入口。';
  } else if (b.hasAttribute('data-clear')) {
    if (remember(keys.recent,[])) renderLists();
  } else if (b.hasAttribute('data-share')) {
    if (navigator.share) {
      try {await navigator.share({title:document.title,url:location.href});}
      catch (err) {if(err.name!=='AbortError') await copyLink();}
    } else await copyLink();
  } else if (b.hasAttribute('data-copy')) await copyLink();
});
syncFavorite();
addEventListener('storage', () => {syncFavorite(); if ($('#saved')) renderLists();});
if ($('#saved')) renderLists().catch(()=>$('#saved').textContent='暂时无法读取目录，请刷新重试。');
if ($('#results')) search().catch(()=>$('#results').textContent='搜索目录暂时不可用，请刷新重试。');
if (pagePath==='/catalog.html') {
  const type=new URL(location.href).searchParams.get('type');
  const blocks=[...document.querySelectorAll('[data-filter]')];
  if (blocks.some(b=>b.dataset.filter===type)) blocks.forEach(b=>b.hidden=b.dataset.filter!==type);
}
if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js').catch(()=>{});
