const CACHE_NAME = 'dealshub-v2';
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

/* PUSH NOTIFICATIONS HANDLER */
self.addEventListener('push', (e) => {
  const data = e.data ? e.data.json() : { title: '🔥 New Loot Deal Dropped!', body: 'Check out today\'s biggest price drop on Deals Hub.' };
  e.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: 'https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=192&auto=format&fit=crop',
      badge: 'https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=192&auto=format&fit=crop',
      data: { url: './' }
    })
  );
});

self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  e.waitUntil(clients.openWindow(e.notification.data.url || './'));
});
