// İçerik denetimi: oyunun kendi içerik kurucusuyla (js/icerik.js) tabloları okur ve uyarıları yazar.
// Kullanım: node denetle.mjs <icerik klasörünün bulunduğu kök>
import { readFile } from 'node:fs/promises';

const OYUN = new URL('../../', import.meta.url).pathname.replace(/^\/(\w:)/, '$1');
const KOK = (process.argv[2] ?? OYUN).split('\\').join('/').replace(/\/?$/, '/');
globalThis.fetch = async yol => {
  try { return new Response(await readFile(KOK + yol)); } catch { return new Response('yok', { status: 404 }); }
};
const { icerikYukle } = await import(new URL('js/icerik.js', 'file:///' + OYUN).href);
const icerik = await icerikYukle();
console.log('hazır:', icerik.dosyalar.filter(d => d.hazir).length, '/', icerik.dosyalar.length);
console.log('uyarı sayısı:', icerik.uyarilar.length);
for (const u of icerik.uyarilar.slice(0, 60)) console.log(' -', u.dosya, u.satir ?? '', u.mesaj);
const say = f => {
  const s = {};
  for (const d of icerik.dosyalar) for (const g of d.gorevler) { const k = f(g, d); s[k] = (s[k] ?? 0) + 1; }
  return s;
};
console.log('türler', say(g => g.tur));
console.log('kategoriler', say(g => g.kategori));
console.log('beceriler', say(g => g.beceri));
const temalar = {};
for (const d of icerik.dosyalar) temalar[d.tema || '(yok)'] = (temalar[d.tema || '(yok)'] ?? 0) + 1;
console.log('temalar', temalar);
