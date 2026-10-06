// Görünürlük kontrolü: bir görevde henüz açılmamış bir kanıt istenirse içerik denetimi uyarı vermeli
import assert from 'node:assert/strict';

const KOK = new URL('../../', import.meta.url).pathname.replace(/^\/(\w:)/, '$1');
const mod = yol => import(new URL(yol, 'file:///' + KOK).href);
const { icerikKur } = await mod('js/icerik.js');
const { csvCoz } = await mod('js/csv.js');

const veri = {
  dosyalar: csvCoz('id;seviye;sira;baslik;giris;cevap;final;ornek;kaynakca\nX1;1;1;Deneme;g;Fe;;;k'),
  kanitlar: csvCoz('dosya;id;tur;baslik;metin;goster;kaynak\nX1;K1;yogunluk;Y;7,87;;\nX1;K2;deney;M;mıknatıs;G2;'),
  tablolar: csvCoz('dosya;tablo;h1'),
  gorevler: csvCoz([
    'dosya;id;asama;arguman;tur;kategori;beceri;soru;ipucu;aciklama;dogru;hata_turu',
    'X1;G1;Kanıt;;kanit;kanit;kanit;Soru;;;K1 K2;',
    'X1;G2;Veri;;tekli;kanit;veri;Soru2;;;;',
    'X1;G3;Kanıt;;kanit;kanit;kanit;Soru3;;;K1 K2;',
  ].join('\n')),
  secenekler: csvCoz('dosya;gorev;metin;dogru;hata_turu;hata_kaniti;hata_aciklamasi\nX1;G2;A;evet;;;\nX1;G2;B;;veri;K2;b'),
};

const { uyarilar } = icerikKur(veri);
const m = uyarilar.map(u => `${u.dosya}:${u.satir}: ${u.mesaj}`);
assert.ok(m.some(x => x.includes('gorevler.csv:2: X1 G1: K2 kanıtı bu görev sorulduğunda henüz açılmamış')), m.join('\n'));
assert.ok(m.some(x => x.includes('secenekler.csv:3: X1 G2: hata_kaniti K2 bu görev sorulduğunda henüz açılmamış')), m.join('\n'));
assert.ok(!m.some(x => x.includes('X1 G3')), 'G2 çözüldükten sonra K2 açık olmalı');
console.log('ok   görünürlük kontrolü: açılmamış kanıt uyarısı doğru satırlarda, açıldıktan sonra uyarı yok');
