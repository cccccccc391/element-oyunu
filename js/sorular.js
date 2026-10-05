// Soruları elementler tablosundan otomatik üretir.
// Üç soru türü var:
//   neden        : Element ve kullanım alanı verilir, "hangi özelliği sayesinde?" diye sorulur.
//   hangiElement : Kullanım alanı ve özellik verilir, "hangi element?" diye sorulur.
//   isim         : Adının hikâyesi verilir, "hangi element?" diye sorulur.
// Bölüm her başladığında sorular, soru türleri ve şıkların sırası yeniden karıştırılır;
// böylece bölüm baştan başladığında cevapların sırası ezberlenemez.

import { AYARLAR } from './ayarlar.js';

export function karistir(dizi, rastgele = Math.random) {
  const sonuc = [...dizi];
  for (let i = sonuc.length - 1; i > 0; i--) {
    const j = Math.floor(rastgele() * (i + 1));
    [sonuc[i], sonuc[j]] = [sonuc[j], sonuc[i]];
  }
  return sonuc;
}

export function elementEtiketi(element) {
  return `${element.ad} (${element.sembol})`;
}

// Metinde elementin adı geçiyorsa "___" ile gizler; yoksa soru cevabı ele verir.
// Türkçe büyük-küçük harf farkını (İ/i, I/ı) da dikkate alır.
export function adiGizle(metin, element) {
  if (!element.ad) return metin;
  const kacis = harf => harf.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const desen = [...element.ad].map(harf => {
    const kucuk = harf.toLocaleLowerCase('tr-TR'), buyuk = harf.toLocaleUpperCase('tr-TR');
    return kucuk === buyuk ? kacis(harf) : `[${kacis(kucuk)}${kacis(buyuk)}]`;
  }).join('');
  return metin.replace(new RegExp(desen, 'gu'), '___');
}

const ayniMetin = (a, b) => a.toLocaleLowerCase('tr-TR') === b.toLocaleLowerCase('tr-TR');

// "neden" sorusunun yanlış şıkları: öğrencilerin yazdığı çeldiriciler.
// İkiden az çeldirici yazılmışsa aynı bölümdeki başka elementlerin özellikleriyle tamamlanır.
function nedenCeldiricileri(element, kullanim, bolum, rastgele) {
  const secilenler = [];
  const ekle = metin => {
    if (secilenler.length < 3 && metin && !ayniMetin(metin, kullanim.ozellik)
        && !secilenler.some(s => ayniMetin(s, metin))) secilenler.push(metin);
  };
  kullanim.celdiriciler.forEach(ekle);
  if (secilenler.length < 2) {
    const havuz = bolum.elementler
      .filter(e => e.no !== element.no)
      .flatMap(e => e.kullanimlar.map(k => k.ozellik));
    karistir(havuz, rastgele).forEach(ekle);
  }
  return secilenler;
}

// Doğru element ve aynı bölümden üç yanlış element
function elementSecenekleri(element, bolum, rastgele, haric = () => false) {
  const digerleri = karistir(bolum.elementler.filter(e => e.no !== element.no && !haric(e)), rastgele).slice(0, 3);
  return karistir([element, ...digerleri].map(e => ({ metin: elementEtiketi(e), dogru: e === element })), rastgele);
}

function nedenSorusu(element, kullanim, celdiriciler, rastgele) {
  return {
    tur: 'neden',
    etiket: 'Neden?',
    element, kullanim,
    bilgiler: [['Element', elementEtiketi(element)], ['Kullanım alanı', kullanim.kullanim]],
    soru: 'Bu element hangi özelliği sayesinde burada kullanılır?',
    secenekler: karistir([
      { metin: kullanim.ozellik, dogru: true },
      ...celdiriciler.map(metin => ({ metin, dogru: false })),
    ], rastgele),
  };
}

function hangiElementSorusu(element, kullanim, bolum, rastgele) {
  // Aynı kullanım alanı yazılmış başka bir element yanlış şık olarak çıkmasın
  const ayniKullanim = e => e.kullanimlar.some(k => ayniMetin(k.kullanim, kullanim.kullanim));
  return {
    tur: 'hangiElement',
    etiket: 'Hangi element?',
    element, kullanim,
    bilgiler: [['Kullanım alanı', adiGizle(kullanim.kullanim, element)], ['Özelliği', adiGizle(kullanim.ozellik, element)]],
    soru: 'Bu özelliği sayesinde burada kullanılan element hangisi?',
    secenekler: elementSecenekleri(element, bolum, rastgele, ayniKullanim),
  };
}

function isimSorusu(element, bolum, rastgele) {
  return {
    tur: 'isim',
    etiket: 'Adının hikâyesi',
    element, kullanim: null,
    bilgiler: [['Adı nereden geliyor?', adiGizle(element.isimKoken, element)]],
    soru: 'Bu hikâye hangi elementin?',
    secenekler: elementSecenekleri(element, bolum, rastgele),
  };
}

// Bir element için sorulabilecek bütün soru türleri
function soruAdaylari(element, bolum, rastgele) {
  const adaylar = [];
  const baskaElementVar = bolum.elementler.length >= 2;
  for (const kullanim of element.kullanimlar) {
    const celdiriciler = nedenCeldiricileri(element, kullanim, bolum, rastgele);
    if (celdiriciler.length >= 2) {
      adaylar.push({ tur: 'neden', uret: () => nedenSorusu(element, kullanim, celdiriciler, rastgele) });
    }
    if (baskaElementVar) {
      adaylar.push({ tur: 'hangiElement', uret: () => hangiElementSorusu(element, kullanim, bolum, rastgele) });
    }
  }
  if (element.isimKoken && baskaElementVar) {
    adaylar.push({ tur: 'isim', uret: () => isimSorusu(element, bolum, rastgele) });
  }
  return adaylar;
}

function agirlikliSec(adaylar, rastgele) {
  const agirlik = aday => AYARLAR.soruTuruAgirliklari[aday.tur] ?? 1;
  let kalan = rastgele() * adaylar.reduce((toplam, aday) => toplam + agirlik(aday), 0);
  for (const aday of adaylar) {
    kalan -= agirlik(aday);
    if (kalan < 0) return aday;
  }
  return adaylar[adaylar.length - 1];
}

// Bir bölüm turu için sorular: içeriği hazır her element bir kez, rastgele sırayla sorulur.
export function bolumSorulari(bolum, rastgele = Math.random) {
  return karistir(bolum.elementler, rastgele)
    .map(element => soruAdaylari(element, bolum, rastgele))
    .filter(adaylar => adaylar.length > 0)
    .map(adaylar => agirlikliSec(adaylar, rastgele).uret());
}

// Bölümde içeriği soru sormaya yetecek kadar dolu olan element sayısı
export function hazirSoruSayisi(bolum) {
  return bolum.elementler.filter(element => soruAdaylari(element, bolum, Math.random).length > 0).length;
}

// Bonus tur için bölümün maddelerinden rastgele seçim
export function bonusMaddeleri(bonuslar, bolumNo, rastgele = Math.random) {
  return karistir(bonuslar.get(bolumNo) ?? [], rastgele).slice(0, AYARLAR.bonusMaddeSayisi);
}
