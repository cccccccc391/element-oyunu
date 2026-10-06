// Element Dosyaları v2: periyodik tablo, içerik doğrulama ve puanlama testleri (Node ile)
import { readFile } from 'node:fs/promises';
import assert from 'node:assert/strict';

const KOK = new URL('../../', import.meta.url).pathname.replace(/^\/(\w:)/, '$1');
const mod = yol => import(new URL(yol, 'file:///' + KOK).href);
const { ELEMENTLER, elementBul, sembolle, sadelestir } = await mod('js/periyodik.js');
const { icerikYukle, icerikKur, kod } = await mod('js/icerik.js');
const { dosyaPuani, gorevKredisi, beceriOzeti } = await mod('js/puan.js');
const { kayitlardanCsv } = await mod('js/kayit.js');
const { csvCoz } = await mod('js/csv.js');

let gecen = 0;
async function test(ad, fn) {
  try { await fn(); gecen++; console.log('ok  ', ad); }
  catch (e) { console.log('FAIL', ad, '\n   ', e.message); process.exitCode = 1; }
}

globalThis.fetch = async yol => {
  try { return new Response(await readFile(KOK + yol)); }
  catch { return new Response('yok', { status: 404 }); }
};

await test('periyodik tablo: 118 element ve doğru konumlar', () => {
  assert.equal(ELEMENTLER.length, 118);
  const k = s => { const e = sembolle(s); return [e.periyot, e.grup, e.blok, e.satir, e.sutun]; };
  assert.deepEqual(k('H'), [1, 1, 's', 1, 1]);
  assert.deepEqual(k('He'), [1, 18, 's', 1, 18]);
  assert.deepEqual(k('B'), [2, 13, 'p', 2, 13]);
  assert.deepEqual(k('Cu'), [4, 11, 'd', 4, 11]);
  assert.deepEqual(k('Zn'), [4, 12, 'd', 4, 12]);
  assert.deepEqual(k('Ga'), [4, 13, 'p', 4, 13]);
  assert.deepEqual(k('Ag'), [5, 11, 'd', 5, 11]);
  assert.deepEqual(k('La'), [6, null, 'f', 9, 3]);
  assert.deepEqual(k('Lu'), [6, null, 'f', 9, 17]);
  assert.deepEqual(k('Hf'), [6, 4, 'd', 6, 4]);
  assert.deepEqual(k('Hg'), [6, 12, 'd', 6, 12]);
  assert.deepEqual(k('Rn'), [6, 18, 'p', 6, 18]);
  assert.deepEqual(k('Ac'), [7, null, 'f', 10, 3]);
  assert.deepEqual(k('Lr'), [7, null, 'f', 10, 17]);
  assert.deepEqual(k('Rf'), [7, 4, 'd', 7, 4]);
  assert.deepEqual(k('Og'), [7, 18, 'p', 7, 18]);
  // Her hücre tek bir elemente ait olmalı
  const hucreler = new Set(ELEMENTLER.map(e => `${e.satir}-${e.sutun}`));
  assert.equal(hucreler.size, 118);
  // 4. periyot d bloğu: Sc..Zn
  assert.deepEqual(ELEMENTLER.filter(e => e.periyot === 4 && e.blok === 'd').map(e => e.sembol).join(' '), 'Sc Ti V Cr Mn Fe Co Ni Cu Zn');
});

await test('element adı / sembolü tanıma (Türkçe harf ve büyük-küçük harf farkı)', () => {
  assert.equal(elementBul('bakir').sembol, 'Cu');
  assert.equal(elementBul(' BAKIR ').sembol, 'Cu');
  assert.equal(elementBul('cu').sembol, 'Cu');
  assert.equal(elementBul('İyot').sembol, 'I');
  assert.equal(elementBul('iyot').sembol, 'I');
  assert.equal(elementBul('Nitrojen').sembol, 'N');
  assert.equal(elementBul('Volfram').sembol, 'W');
  assert.equal(elementBul('kıbrıs'), null);
  assert.equal(sadelestir('Çinko!'), 'cinko');
  assert.equal(kod('KARŞI KANIT'), 'karsi_kanit');
  assert.equal(kod('Özellik-Kullanım'), 'ozellik_kullanim');
  assert.equal(kod('ÇIKARIM'), 'cikarim');
});

await test('içerik: 200 vakanın hepsi hazır, uyarı yok, V001 tanıtım dosyası 18 görev, 100 farklı element', async () => {
  const icerik = await icerikYukle();
  assert.deepEqual(icerik.uyarilar, []);
  assert.equal(icerik.dosyalar.length, 200);
  assert.deepEqual(icerik.dosyalar.map(d => d.id), Array.from({ length: 200 }, (_, i) => `V${String(i + 1).padStart(3, '0')}`));
  const v001 = icerik.dosyalar[0];
  assert.ok(v001.hazir && v001.ornek && !v001.final);
  assert.equal(v001.cevap.sembol, 'Cu');
  assert.equal(v001.gorevler.length, 18);
  assert.equal(v001.kanitlar.length, 10);
  assert.ok(icerik.dosyalar[199].final && icerik.dosyalar[199].hazir && icerik.dosyalar[199].cevap.sembol === 'Na');
  assert.equal(icerik.dosyalar.filter(d => d.hazir).length, 200);
  const elementler = new Set(icerik.dosyalar.map(d => d.cevap.z));
  assert.equal(elementler.size, 100, 'atom numarası 1–100 arasındaki her element en az bir vakada');
  assert.ok([...elementler].every(z => z >= 1 && z <= 100));
  assert.ok(icerik.dosyalar.every(d => d.tema), 'her vakanın teması var');
  assert.deepEqual([1, 2, 3, 4].map(s => icerik.dosyalar.filter(d => d.seviye === s).length), [50, 50, 50, 50]);
  const d01 = v001;
  const tablo = d01.kanitlar.find(k => k.id === 'K7').tablo;
  assert.equal(tablo.basliklar.length, 5);
  assert.equal(tablo.satirlar.length, 6);
  assert.deepEqual(tablo.satirlar[4], ['Bakır', '8,96', '59,6', '1085', 'Hayır']);
  const g = id => d01.gorevler.find(x => x.id === id);
  assert.deepEqual([...g('G15').gerekli], ['K1', 'K4', 'K8']);
  assert.deepEqual([...g('G15').serbest], ['K7', 'K9']);
  assert.equal(g('G2').dogruSemboller.size, 10);
  assert.deepEqual(g('G6').kabul, ['Cu']);
  assert.ok(g('G6').elementCevabi);
  assert.equal(g('G8').secenekler.map(s => s.sira).join(','), '1,2,3,4');
  assert.equal(g('G5').secenekler.filter(s => s.dogru).length, 2);
  assert.equal(g('G16').arguman, 'gerekce');
  assert.equal(g('G17').arguman, 'karsi_kanit');
  for (const gorev of d01.gorevler.filter(x => x.tur === 'tekli')) {
    assert.equal(gorev.secenekler.filter(s => s.dogru).length, 1, gorev.id);
    for (const s of gorev.secenekler.filter(s => !s.dogru)) assert.ok(s.hataAciklamasi, `${gorev.id} çeldirici açıklaması`);
  }
  // Kanıt açılma zinciri
  assert.deepEqual(d01.kanitlar.filter(k => k.goster).map(k => `${k.id}<${k.goster}`), ['K8<G4', 'K9<G5', 'K10<G6']);
});

await test('puanlama: tam kredi 100, kategoriler ağırlıklara göre, gruplar toplamı tutar', async () => {
  const { dosyalar } = await icerikYukle();
  const d01 = dosyalar[0];
  const hepsi = new Map(d01.gorevler.map(g => [g.id, 1]));
  const tam = dosyaPuani(d01, hepsi);
  assert.equal(tam.toplam, 100);
  const enToplam = tam.kategoriler.reduce((t, k) => t + k.en, 0);
  assert.ok(Math.abs(enToplam - 100) < 1e-9);
  // Örnek dosyada 8 kategorinin hepsi var: ağırlıklar aynen geçerli
  assert.deepEqual(tam.kategoriler.map(k => [k.kategori, Math.round(k.en)]),
    [['kimlik', 20], ['sembol', 10], ['isim', 10], ['kullanim', 15], ['ozellik_kullanim', 15], ['kanit', 15], ['alternatif', 5], ['gerekce', 10]]);
  assert.equal(Math.round(tam.gruplar.bilgi.en), 55);
  assert.equal(Math.round(tam.gruplar.akil.en), 45);
  // Yalnızca element kimliği yanlış denemeyle bulunursa 20 puan gider
  const kimliksiz = new Map(hepsi); kimliksiz.set('G6', 0);
  assert.equal(dosyaPuani(d01, kimliksiz).toplam, 80);
  // İpucu yarım kredi
  assert.equal(gorevKredisi({ yanlisSayisi: 0, ipucu: true }), 0.5);
  assert.equal(gorevKredisi({ yanlisSayisi: 1, ipucu: false }), 0);
  // Kanıt kategorisinde 7 görev var: biri yanlış olursa 15/7 puan gider
  const birKanitYanlis = new Map(hepsi); birKanitYanlis.set('G3', 0);
  assert.equal(dosyaPuani(d01, birKanitYanlis).toplam, Math.round(100 - 15 / 7));
});

await test('doğrulama: bozuk içerik satır numaralarıyla raporlanır, bozuk görev atlanır', () => {
  const veri = {
    dosyalar: csvCoz('id;seviye;sira;baslik;giris;cevap;final;ornek;kaynakca\nX1;1;1;Deneme;giriş;Qq;;;\nX2;5;2;İkinci;g;Fe;;;k\nX2;1;3;Tekrar;g;Fe;;;k\nX3;2;1;Bos;;;;;'),
    kanitlar: csvCoz('dosya;id;tur;baslik;metin;goster;kaynak\nX2;K1;yogunluk;Y;7,87;G9;\nX2;K2;sihir;S;?;;\nX2;K3;tablo;T;T9;;\nX9;K1;deney;D;d;;'),
    tablolar: csvCoz('dosya;tablo;h1;h2\nX2;T1;a;b'),
    gorevler: csvCoz([
      'dosya;id;asama;arguman;tur;kategori;beceri;soru;ipucu;aciklama;dogru;hata_turu',
      'X2;G1;Gözlem;;tekli;kimlik;gozlem;Soru1;;;;',
      'X2;G2;Veri;;tekli;kanit;veri;Soru2;;;;',
      'X2;G3;Veri;;tablo;kanit;veri;Soru3;;;Fe Xx;',
      'X2;G4;Kanıt;Yanlış;kanit;kanit;kanit;Soru4;;;K1 (K5);',
      'X2;G5;Sonuç;;yaz;sembol;cikarim;Soru5;;;;',
      'X2;G6;Sonuç;;sirala;kanit;veri;Soru6;;;;',
      'X2;G7;Hayal;;tekli;uydurma;veri;Soru7;;;;',
    ].join('\n')),
    secenekler: csvCoz([
      'dosya;gorev;metin;dogru;hata_turu;hata_kaniti;hata_aciklamasi',
      'X2;G1;A;evet;;;', 'X2;G1;B;;veri;K7;b',
      'X2;G2;A;evet;;;', 'X2;G2;B;evet;;;',
      'X2;G6;A;1;;;', 'X2;G6;B;1;;;',
    ].join('\n')),
  };
  const { dosyalar, uyarilar } = icerikKur(veri);
  const m = uyarilar.map(u => `${u.dosya}:${u.satir ?? '-'}: ${u.mesaj}`);
  const icerir = parca => assert.ok(m.some(x => x.includes(parca)), `beklenen uyarı yok: ${parca}\n  ${m.join('\n  ')}`);
  icerir('dosyalar.csv:2: X1: "cevap" sütununa geçerli bir element sembolü');
  icerir('dosyalar.csv:2: X1: kaynakça yazılmamış');
  icerir('dosyalar.csv:3: X2: seviye 1, 2, 3 ya da 4 olmalı');
  icerir('dosyalar.csv:4: X2 birden fazla kez yazılmış');
  icerir('kanitlar.csv:3: X2 K2: bilinmeyen kanıt türü "sihir"');
  icerir('kanitlar.csv:4: X2 K3: tablolar.csv\'de "T9" adlı tablo bulunamadı');
  icerir('kanitlar.csv:5: X9 adlı bir dosya');
  icerir('kanitlar.csv:2: X2 K1: "goster" sütunundaki G9 görevi bulunamadı');
  icerir('secenekler.csv:3: X2 G1: hata_kaniti sütunundaki K7 kanıtı bulunamadı');
  icerir('gorevler.csv:3: X2 G2: tek doğru seçenek olmalı, 2 tane');
  icerir('gorevler.csv:4: X2 G3: geçersiz sembol: Xx');
  icerir('gorevler.csv:5: X2 G4: argüman aşaması geçersiz: "Yanlış"');
  icerir('gorevler.csv:5: X2 G4: K5 kanıtı bulunamadı');
  icerir('gorevler.csv:7: X2 G6: sıralama seçeneklerinin');
  icerir('gorevler.csv:8: X2 G7: kategori geçersiz');
  const x2 = dosyalar.find(d => d.id === 'X2');
  assert.deepEqual(x2.gorevler.map(g => g.id), ['G1', 'G4', 'G5'], 'bozuk görevler atlanmalı');
  assert.ok(x2.hazir);
  assert.equal(x2.seviye, 1, 'geçersiz seviye 1 sayılır');
  assert.deepEqual(x2.gorevler[2].kabul, ['Fe'], 'sembol görevinin cevabı dosyanın cevabından alınır');
  assert.equal(x2.kanitlar.find(k => k.id === 'K1').goster, '', 'geçersiz goster baştan gösterilir');
  assert.ok(!dosyalar.find(d => d.id === 'X1').hazir);
  assert.ok(!dosyalar.find(d => d.id === 'X3').hazir);
});

await test('araştırma özeti ve CSV dışa aktarma', () => {
  const kayitlar = [
    { olay: 'cevap', beceri: 'veri', seviye: 1, deneme: 1, dogru: true },
    { olay: 'cevap', beceri: 'veri', seviye: 1, deneme: 1, dogru: false },
    { olay: 'cevap', beceri: 'veri', seviye: 1, deneme: 2, dogru: true },
    { olay: 'cevap', beceri: 'kanit', seviye: 2, deneme: 1, dogru: true },
    { olay: 'savunma', beceri: 'gerekce', seviye: 1, deneme: 1, cevap: 'Telin bakır; "çünkü"\nikinci satır' },
  ];
  const ozet = beceriOzeti(kayitlar);
  assert.deepEqual(ozet.veri.toplam, { dogru: 1, sayi: 2 });
  assert.deepEqual(ozet.veri.seviyeler[1], { dogru: 1, sayi: 2 });
  assert.deepEqual(ozet.kanit.seviyeler[2], { dogru: 1, sayi: 1 });
  assert.deepEqual(ozet.gerekce.toplam, { dogru: 0, sayi: 0 });
  const csv = kayitlardanCsv([{ katilimci: 'D07', olay: 'savunma', dogru: true, cevap: kayitlar[4].cevap }]);
  assert.ok(csv.startsWith('\uFEFFkatilimci;zaman;'));
  const geri = csvCoz(csv.replace(/^\uFEFF/, ''));
  assert.equal(geri[0].cevap, 'Telin bakır; "çünkü"\nikinci satır');
  assert.equal(geri[0].dogru, '1');
  assert.equal(geri[0].katilimci, 'D07');
});

console.log(`\n${gecen} test geçti`);
