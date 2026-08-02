const CACHE_NAME = 'dealshub-v1';
const ASSETS = [
  './',
  './index.html',
  './deals.json',
  './manifest.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => {
    return Promise.all(keys.map((k) => {
      if (k !== CACHE_NAME) return caches.delete(k);
    }));
  }));
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  if (e.request.url.includes('deals.json')) {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
  } else {
    e.respondWith(
      caches.match(e.request).then((res) => res || fetch(e.request))
    );
  }
});
