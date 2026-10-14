// Önbellek temizleyici: eski çevrim dışı kopyayı siler ve kendini kaldırır.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', olay => olay.waitUntil((async () => {
  for (const ad of await caches.keys()) await caches.delete(ad);
  await self.registration.unregister();
  for (const istemci of await self.clients.matchAll({ type: 'window' })) istemci.navigate(istemci.url);
})()));
