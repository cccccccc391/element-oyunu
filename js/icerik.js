// İçerik tablolarını (icerik/*.csv) okur, birbirine bağlar ve kontrol eder.
// Bulunan sorunlar "uyarilar" listesine eklenir; Öğretmen panelinde satır numarasıyla gösterilir.
// Hatalı bir görev atlanır, dosyanın geri kalanı oynanabilir kalır.

import { csvYukle } from './csv.js';
import { ASAMALAR, ARGUMAN_ASAMALARI, BECERILER, GOREV_TURLERI, HATA_TURLERI, KANIT_TURLERI, KATEGORILER } from './ayarlar.js';
import { elementBul, sadelestir, sembolle } from './periyodik.js';

const TABLOLAR = ['dosyalar', 'kanitlar', 'tablolar', 'gorevler', 'secenekler'];

export async function icerikYukle() {
  const okunanlar = await Promise.all(TABLOLAR.map(ad => csvYukle(`icerik/${ad}.csv`)));
  return icerikKur(Object.fromEntries(TABLOLAR.map((ad, i) => [ad, okunanlar[i]])));
}

// Tablodaki değerleri karşılaştırılabilir kodlara çevirir: "KARŞI KANIT" -> "karsi_kanit"
export function kod(metin) {
  const harfler = { ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u' };
  return String(metin ?? '').trim().toLocaleLowerCase('tr-TR')
    .replace(/[çğıöşü]/g, harf => harfler[harf])
    .replace(/[\s-]+/g, '_');
}

const evetMi = deger => ['evet', 'e', 'x', '1', 'dogru', 'true'].includes(kod(deger));
const ASAMA_KODLARI = new Set(ASAMALAR.map(([k]) => k));
const ARGUMAN_KODLARI = new Set(ARGUMAN_ASAMALARI.map(([k]) => k));

function grupla(satirlar, anahtar) {
  const gruplar = new Map();
  for (const s of satirlar) {
    const k = (s[anahtar] ?? '').trim();
    if (!gruplar.has(k)) gruplar.set(k, []);
    gruplar.get(k).push(s);
  }
  return gruplar;
}

export function icerikKur(veri) {
  const uyarilar = [];
  const uyar = (tablo, satir, mesaj, dosyaId = null) => uyarilar.push({ dosya: `${tablo}.csv`, satir, mesaj, dosyaId });

  const kanitGruplari = grupla(veri.kanitlar, 'dosya');
  const tabloGruplari = grupla(veri.tablolar, 'dosya');
  const gorevGruplari = grupla(veri.gorevler, 'dosya');
  const secenekGruplari = grupla(veri.secenekler, 'dosya');

  const dosyalar = [];
  const gorulenIdler = new Set();
  veri.dosyalar.forEach((s, sira) => {
    const id = (s.id ?? '').trim();
    if (!id) { uyar('dosyalar', s._satir, 'Dosyanın "id" sütunu boş'); return; }
    if (gorulenIdler.has(id)) { uyar('dosyalar', s._satir, `${id} birden fazla kez yazılmış`, id); return; }
    gorulenIdler.add(id);
    const seviye = Number(s.seviye);
    const dosya = {
      id,
      seviye: [1, 2, 3, 4].includes(seviye) ? seviye : 1,
      sira: Number(s.sira) || sira + 1,
      baslik: s.baslik ?? '',
      giris: s.giris ?? '',
      cevap: null,
      final: evetMi(s.final),
      ornek: evetMi(s.ornek),
      kaynakca: (s.kaynakca ?? '').split('|').map(k => k.trim()).filter(Boolean),
      kanitlar: [],
      gorevler: [],
      hazir: false,
    };
    dosyalar.push(dosya);
    if (![1, 2, 3, 4].includes(seviye)) uyar('dosyalar', s._satir, `${id}: seviye 1, 2, 3 ya da 4 olmalı`, id);
    if (!dosya.baslik) return;   // henüz yazılmamış dosya

    dosya.cevap = sembolle(s.cevap) ?? elementBul(s.cevap);
    if (!dosya.cevap) uyar('dosyalar', s._satir, `${id}: "cevap" sütununa geçerli bir element sembolü yazılmalı (örnek: Cu)`, id);
    if (!dosya.kaynakca.length) uyar('dosyalar', s._satir, `${id}: kaynakça yazılmamış`, id);

    dosya.kanitlar = kanitlariKur(dosya, kanitGruplari.get(id) ?? [], tabloGruplari.get(id) ?? [], uyar);
    dosya.gorevler = gorevleriKur(dosya, gorevGruplari.get(id) ?? [], secenekGruplari.get(id) ?? [], uyar);

    // Görev çözülünce açılan kanıtlar var olan bir göreve bağlı olmalı
    const gorevIdleri = new Set(dosya.gorevler.map(g => g.id));
    for (const k of dosya.kanitlar) {
      if (k.goster && !gorevIdleri.has(k.goster)) {
        uyar('kanitlar', k.satir, `${id} ${k.id}: "goster" sütunundaki ${k.goster} görevi bulunamadı; kanıt baştan gösterilecek`, id);
        k.goster = '';
      }
    }
    gorunurlukKontrolu(dosya, uyar);
    dosya.hazir = Boolean(dosya.cevap) && dosya.gorevler.length > 0;
  });

  for (const [tablo, gruplar] of [['kanitlar', kanitGruplari], ['gorevler', gorevGruplari], ['secenekler', secenekGruplari]]) {
    for (const [dosyaId, satirlar] of gruplar) {
      if (dosyaId && !gorulenIdler.has(dosyaId)) uyar(tablo, satirlar[0]._satir, `${dosyaId} adlı bir dosya dosyalar.csv'de yok`);
    }
  }

  dosyalar.sort((a, b) => a.seviye - b.seviye || a.sira - b.sira || a.id.localeCompare(b.id));
  return { dosyalar, uyarilar };
}

// Bir görevde istenen ya da hata açıklamasında gösterilen kanıt, o görev sorulduğunda açılmış olmalı
function gorunurlukKontrolu(dosya, uyar) {
  const acik = new Set(dosya.kanitlar.filter(k => !k.goster).map(k => k.id));
  for (const gorev of dosya.gorevler) {
    if (gorev.tur === 'kanit') {
      const kapali = [...gorev.gerekli, ...gorev.serbest].filter(k => !acik.has(k));
      if (kapali.length) {
        uyar('gorevler', gorev.satir, `${dosya.id} ${gorev.id}: ${kapali.join(', ')} kanıtı bu görev sorulduğunda henüz açılmamış olacak`, dosya.id);
      }
    }
    for (const s of gorev.secenekler) {
      if (s.hataKaniti && !acik.has(s.hataKaniti)) {
        uyar('secenekler', s.satir, `${dosya.id} ${gorev.id}: hata_kaniti ${s.hataKaniti} bu görev sorulduğunda henüz açılmamış olacak`, dosya.id);
      }
    }
    dosya.kanitlar.filter(k => k.goster === gorev.id).forEach(k => acik.add(k.id));
  }
}

function kanitlariKur(dosya, satirlar, tabloSatirlari, uyar) {
  const tablolar = grupla(tabloSatirlari, 'tablo');
  const kanitlar = [];
  for (const s of satirlar) {
    const id = (s.id ?? '').trim();
    if (!id) { uyar('kanitlar', s._satir, `${dosya.id}: kanıtın "id" sütunu boş`, dosya.id); continue; }
    if (kanitlar.some(k => k.id === id)) { uyar('kanitlar', s._satir, `${dosya.id}: ${id} birden fazla kez yazılmış`, dosya.id); continue; }
    const tur = kod(s.tur);
    if (!KANIT_TURLERI[tur]) uyar('kanitlar', s._satir, `${dosya.id} ${id}: bilinmeyen kanıt türü "${s.tur ?? ''}"`, dosya.id);
    const kanit = {
      id, tur, turAdi: KANIT_TURLERI[tur] ?? (s.tur || 'Kanıt'),
      baslik: s.baslik ?? '', metin: s.metin ?? '', goster: (s.goster ?? '').trim(),
      kaynak: s.kaynak ?? '', tablo: null, satir: s._satir,
    };
    if (tur === 'tablo') {
      const tabloSatirlari = tablolar.get(kanit.metin.trim());
      if (!tabloSatirlari?.length) {
        uyar('kanitlar', s._satir, `${dosya.id} ${id}: tablolar.csv'de "${kanit.metin}" adlı tablo bulunamadı`, dosya.id);
        continue;
      }
      const hucreler = r => ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].map(k => r[k] ?? '');
      const basliklar = hucreler(tabloSatirlari[0]);
      let sutunSayisi = basliklar.length;
      while (sutunSayisi > 1 && !basliklar[sutunSayisi - 1]) sutunSayisi--;
      kanit.tablo = {
        basliklar: basliklar.slice(0, sutunSayisi),
        satirlar: tabloSatirlari.slice(1).map(r => hucreler(r).slice(0, sutunSayisi)),
      };
    }
    kanitlar.push(kanit);
  }
  return kanitlar;
}

function gorevleriKur(dosya, satirlar, secenekSatirlari, uyar) {
  const secenekGruplari = grupla(secenekSatirlari, 'gorev');
  const kanitIdleri = new Set(dosya.kanitlar.map(k => k.id));
  const gorevler = [];
  for (const s of satirlar) {
    const id = (s.id ?? '').trim();
    const yer = `${dosya.id} ${id || '?'}`;
    const sorun = mesaj => uyar('gorevler', s._satir, `${yer}: ${mesaj}. Bu görev şimdilik atlanıyor.`, dosya.id);
    if (!id) { sorun('görevin "id" sütunu boş'); continue; }
    if (gorevler.some(g => g.id === id)) { sorun('aynı id ile ikinci kez yazılmış'); continue; }

    const gorev = {
      id,
      asama: kod(s.asama),
      arguman: kod(s.arguman),
      tur: kod(s.tur),
      kategori: kod(s.kategori),
      beceri: kod(s.beceri),
      soru: s.soru ?? '',
      ipucu: s.ipucu ?? '',
      aciklama: s.aciklama ?? '',
      hataTuru: HATA_TURLERI[kod(s.hata_turu)] ? kod(s.hata_turu) : 'veri',
      secenekler: [],
      satir: s._satir,
    };
    if (!GOREV_TURLERI.includes(gorev.tur)) { sorun(`bilinmeyen görev türü "${s.tur ?? ''}" (geçerli türler: ${GOREV_TURLERI.join(', ')})`); continue; }
    if (!gorev.soru) { sorun('soru yazılmamış'); continue; }
    if (!KATEGORILER[gorev.kategori]) { sorun(`kategori geçersiz: "${s.kategori ?? ''}"`); continue; }
    if (!ASAMA_KODLARI.has(gorev.asama)) uyar('gorevler', s._satir, `${yer}: aşama geçersiz: "${s.asama ?? ''}"`, dosya.id);
    if (gorev.arguman && !ARGUMAN_KODLARI.has(gorev.arguman)) {
      uyar('gorevler', s._satir, `${yer}: argüman aşaması geçersiz: "${s.arguman}"`, dosya.id);
      gorev.arguman = '';
    }
    if (!BECERILER[gorev.beceri]) uyar('gorevler', s._satir, `${yer}: beceri geçersiz: "${s.beceri ?? ''}"`, dosya.id);
    if (s.hata_turu && !HATA_TURLERI[kod(s.hata_turu)]) uyar('gorevler', s._satir, `${yer}: hata türü geçersiz: "${s.hata_turu}"`, dosya.id);

    const dogru = (s.dogru ?? '').trim();
    const secenekler = (secenekGruplari.get(id) ?? []).map((o, i) => ({
      no: i,
      metin: o.metin ?? '',
      dogru: evetMi(o.dogru),
      sira: Number(o.dogru) || null,
      hataTuru: HATA_TURLERI[kod(o.hata_turu)] ? kod(o.hata_turu) : gorev.hataTuru,
      hataKaniti: kanitIdleri.has((o.hata_kaniti ?? '').trim()) ? o.hata_kaniti.trim() : '',
      hataAciklamasi: o.hata_aciklamasi ?? '',
      satir: o._satir,
    })).filter(o => o.metin);
    for (const o of secenekGruplari.get(id) ?? []) {
      if (o.hata_kaniti && !kanitIdleri.has(o.hata_kaniti.trim())) {
        uyar('secenekler', o._satir, `${yer}: hata_kaniti sütunundaki ${o.hata_kaniti} kanıtı bulunamadı`, dosya.id);
      }
    }

    if (gorev.tur === 'tekli' || gorev.tur === 'coklu') {
      const dogrular = secenekler.filter(o => o.dogru).length;
      if (secenekler.length < 2) { sorun('en az iki seçenek gerekli'); continue; }
      if (gorev.tur === 'tekli' && dogrular !== 1) { sorun(`tek doğru seçenek olmalı, ${dogrular} tane işaretlenmiş`); continue; }
      if (gorev.tur === 'coklu' && dogrular < 1) { sorun('en az bir seçenek doğru olarak işaretlenmeli'); continue; }
      gorev.secenekler = secenekler;
    } else if (gorev.tur === 'sirala') {
      const siralar = secenekler.map(o => o.sira).sort((a, b) => a - b);
      if (secenekler.length < 2 || siralar.some((n, i) => n !== i + 1)) {
        sorun('sıralama seçeneklerinin "dogru" sütununa 1, 2, 3... diye birer kez sıra numarası yazılmalı'); continue;
      }
      gorev.secenekler = secenekler;
    } else if (gorev.tur === 'tablo') {
      const parcalar = dogru.split(/[\s,;]+/).filter(Boolean);
      const gecersiz = parcalar.filter(p => !sembolle(p));
      if (!parcalar.length || gecersiz.length) {
        sorun(gecersiz.length ? `geçersiz sembol: ${gecersiz.join(', ')}` : '"dogru" sütununa işaretlenmesi gereken sembolleri yazın'); continue;
      }
      gorev.dogruSemboller = new Set(parcalar);
    } else if (gorev.tur === 'kanit') {
      gorev.gerekli = new Set();
      gorev.serbest = new Set();
      for (const parca of dogru.split(/[\s,;]+/).filter(Boolean)) {
        const serbest = /^\(.*\)$/.test(parca);
        const kanitId = parca.replace(/[()]/g, '');
        if (!kanitIdleri.has(kanitId)) uyar('gorevler', s._satir, `${yer}: ${kanitId} kanıtı bulunamadı`, dosya.id);
        else (serbest ? gorev.serbest : gorev.gerekli).add(kanitId);
      }
      if (!gorev.gerekli.size) { sorun('"dogru" sütununa seçilmesi gereken kanıtları yazın (örnek: K1 K4 (K7))'); continue; }
    } else if (gorev.tur === 'yaz') {
      gorev.kabul = dogru.split('|').map(k => k.trim()).filter(Boolean);
      if (!gorev.kabul.length && (gorev.kategori === 'kimlik' || gorev.kategori === 'sembol') && dosya.cevap) {
        gorev.kabul = [dosya.cevap.sembol];
      }
      if (!gorev.kabul.length) { sorun('"dogru" sütununa kabul edilecek cevapları | ile ayırarak yazın'); continue; }
      // Cevapların hepsi element ise öğrencinin yazdığı da element adı/sembolü olarak yorumlanır
      gorev.elementCevabi = gorev.kabul.every(k => elementBul(k));
      gorev.kabulSade = new Set(gorev.kabul.map(sadelestir));
    }
    gorevler.push(gorev);
  }
  return gorevler;
}
