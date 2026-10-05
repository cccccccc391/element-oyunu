// Çevrim dışı çalışma yardımcısı (service worker).
// Her dosya önce internetten istenir; internet yoksa daha önce saklanan kopyası kullanılır.
// Böylece içerik dosyaları değişince oyun hep en güncel hâli gösterir, sınıfta bağlantı
// kopsa bile bir kez açılmış oyun oynanmaya devam eder.

const ONBELLEK = 'element-oyunu-v1';

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', olay => olay.waitUntil(self.clients.claim()));

self.addEventListener('fetch', olay => {
  const istek = olay.request;
  if (istek.method !== 'GET' || new URL(istek.url).origin !== self.location.origin) return;
  olay.respondWith(
    fetch(istek)
      .then(yanit => {
        if (yanit.ok) {
          const kopya = yanit.clone();
          caches.open(ONBELLEK).then(onbellek => onbellek.put(istek, kopya));
        }
        return yanit;
      })
      .catch(() => caches.match(istek, { ignoreSearch: true }))
  );
});
