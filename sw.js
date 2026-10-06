/* OpenDTV service worker: offline support + installability.
 * Bump CACHE_VERSION when shipping changes that must reach users immediately. */
const CACHE_VERSION = 'opendtv-v2';
const PAGE_CACHE = `${CACHE_VERSION}-pages`;
const STATIC_CACHE = `${CACHE_VERSION}-static`;

const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/streaming.html',
  '/livetv.html',
  '/apps.html',
  '/devices.html',
  '/catalog.html',
  '/guides.html',
  '/about.html',
  '/legal.html',
  '/404.html',
  '/guides/choose-streaming-device.html',
  '/guides/watch-free-tv.html',
  '/guides/install-tv-apps-safely.html',
  '/guides/fix-tv-buffering.html',
  '/style-v2.css',
  '/app-v2.js',
  '/manifest.webmanifest',
  '/assets/favicon.svg',
  '/assets/logo.svg',
  '/assets/icons/icon-192.png',
  '/assets/icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(PAGE_CACHE);
      // Cache each URL independently: one 404 must not fail the whole install.
      await Promise.all(
        PRECACHE_URLS.map((url) =>
          cache.add(url).catch(() => console.warn('[sw] precache skip:', url)),
        ),
      );
      await self.skipWaiting();
    })(),
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(
        keys
          .filter((key) => key.startsWith('opendtv-') && key !== PAGE_CACHE && key !== STATIC_CACHE)
          .map((key) => caches.delete(key)),
      );
      await self.clients.claim();
    })(),
  );
});

// Page navigations: network-first, fall back to cache, then to the offline home page.
async function networkFirst(request, cacheName, fallbackUrl) {
  const cache = await caches.open(cacheName);
  try {
    const response = await fetch(request);
    if (response && response.ok) cache.put(request, response.clone());
    return response;
  } catch (error) {
    const cached = await cache.match(request);
    if (cached) return cached;
    if (fallbackUrl) {
      const fallback = await cache.match(fallbackUrl);
      if (fallback) return fallback;
    }
    throw error;
  }
}

// Everything else same-origin: stale-while-revalidate.
// No .catch() here on purpose: with no cached copy and the network down,
// the promise rejects so the browser handles it as a normal network error.
async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const network = fetch(request).then((response) => {
    if (response && response.ok) cache.put(request, response.clone());
    return response;
  });
  return cached || network;
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (request.mode === 'navigate') {
    event.respondWith(networkFirst(request, PAGE_CACHE, '/'));
    return;
  }

  if (
    /\.(css|js|svg|png|ico|webmanifest)$/i.test(url.pathname) ||
    url.pathname.startsWith('/assets/')
  ) {
    event.respondWith(staleWhileRevalidate(request, STATIC_CACHE));
    return;
  }

  event.respondWith(staleWhileRevalidate(request, PAGE_CACHE));
});
