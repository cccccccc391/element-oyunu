// İçerik dosyalarını (icerik/*.csv) okur, kontrol eder ve oyunun kullanacağı hâle getirir.
// Bulunan sorunlar "uyarilar" listesine eklenir ve "İçerik durumu" ekranında gösterilir.

import { csvYukle } from './csv.js';

export async function icerikYukle() {
  const [bolumSatirlari, elementSatirlari, bonusSatirlari] = await Promise.all([
    csvYukle('icerik/bolumler.csv'),
    csvYukle('icerik/elementler.csv'),
    csvYukle('icerik/bonus.csv'),
  ]);
  const uyarilar = [];
  const elementler = elementleriHazirla(elementSatirlari, uyarilar);
  const bolumler = bolumleriHazirla(bolumSatirlari, elementler, uyarilar);
  const bonuslar = bonuslariHazirla(bonusSatirlari, bolumler, uyarilar);
  return { elementler, bolumler, bonuslar, uyarilar };
}

// Her elementin bir kaydı olur. Aynı atom numarasıyla yeni satır eklenirse
// o satır, elemente ikinci (üçüncü...) bir kullanım alanı olarak eklenir.
function elementleriHazirla(satirlar, uyarilar) {
  const dosya = 'elementler.csv';
  const elementler = new Map();
  for (const s of satirlar) {
    const no = Number(s.no);
    if (!Number.isInteger(no) || no < 1 || no > 118) {
      uyarilar.push({ dosya, satir: s._satir, mesaj: `Atom numarası geçersiz: "${s.no ?? ''}"` });
      continue;
    }
    let element = elementler.get(no);
    if (!element) {
      element = { no, sembol: s.sembol ?? '', ad: s.ad ?? '', kullanimlar: [], isimKoken: '', kaynaklar: [] };
      elementler.set(no, element);
      if (!element.sembol || !element.ad) {
        uyarilar.push({ dosya, satir: s._satir, mesaj: `${no} numaralı elementin sembolü ya da adı boş` });
      }
    } else if ((s.sembol && s.sembol !== element.sembol) || (s.ad && s.ad !== element.ad)) {
      uyarilar.push({ dosya, satir: s._satir, mesaj: `${no} numara daha önce "${element.ad} (${element.sembol})" olarak yazılmış` });
    }

    const kullanim = {
      kullanim: s.kullanim ?? '',
      ozellik: s.ozellik ?? '',
      neden: s.neden ?? '',
      celdiriciler: [s.celdirici1, s.celdirici2, s.celdirici3].filter(Boolean),
      kaynak: s.kaynak ?? '',
    };
    const doluSayisi = [kullanim.kullanim, kullanim.ozellik, kullanim.neden].filter(Boolean).length;
    if (doluSayisi === 3) {
      element.kullanimlar.push(kullanim);
    } else if (doluSayisi > 0) {
      uyarilar.push({ dosya, satir: s._satir, mesaj: `${element.ad}: "kullanim", "ozellik" ve "neden" sütunlarının üçü de dolu olmalı. Bu satır şimdilik kullanılmıyor.` });
    }
    if (s.isim_koken && !element.isimKoken) element.isimKoken = s.isim_koken;
    if (s.kaynak) element.kaynaklar.push(s.kaynak);
    if ((doluSayisi === 3 || s.isim_koken) && !s.kaynak) {
      uyarilar.push({ dosya, satir: s._satir, mesaj: `${element.ad}: kaynak yazılmamış` });
    }
  }
  for (let no = 1; no <= 118; no++) {
    if (!elementler.has(no)) uyarilar.push({ dosya, mesaj: `${no} numaralı element tabloda yok` });
  }
  return elementler;
}

function bolumleriHazirla(satirlar, elementler, uyarilar) {
  const bolumler = [];
  for (const s of satirlar) {
    const no = Number(s.bolum), baslangic = Number(s.baslangic), bitis = Number(s.bitis);
    if (![no, baslangic, bitis].every(Number.isInteger) || baslangic > bitis) {
      uyarilar.push({ dosya: 'bolumler.csv', satir: s._satir, mesaj: 'Bölüm numarası ya da element aralığı geçersiz' });
      continue;
    }
    const uyeler = [];
    for (let n = baslangic; n <= bitis; n++) if (elementler.has(n)) uyeler.push(elementler.get(n));
    bolumler.push({ no, ad: s.ad || `${no}. Bölüm`, baslangic, bitis, elementler: uyeler });
  }
  return bolumler.sort((a, b) => a.no - b.no);
}

function bonuslariHazirla(satirlar, bolumler, uyarilar) {
  const dosya = 'bonus.csv';
  const bonuslar = new Map(bolumler.map(b => [b.no, []]));
  const alanlar = ['madde', 'gozlem', 'soru', 'dogru', 'yanlis1', 'yanlis2', 'yanlis3', 'deney', 'sonuc', 'kaynak'];
  for (const s of satirlar) {
    if (alanlar.every(a => !s[a])) continue;   // boş şablon satırı
    const bolumNo = Number(s.bolum);
    if (!bonuslar.has(bolumNo)) {
      uyarilar.push({ dosya, satir: s._satir, mesaj: `Bölüm numarası geçersiz: "${s.bolum ?? ''}"` });
      continue;
    }
    const yanlislar = [s.yanlis1, s.yanlis2, s.yanlis3].filter(Boolean);
    const eksikler = ['madde', 'soru', 'dogru', 'sonuc'].filter(a => !s[a]);
    if (!yanlislar.length) eksikler.push('en az bir yanlış şık');
    if (eksikler.length) {
      uyarilar.push({ dosya, satir: s._satir, mesaj: `${s.madde || 'Bonus madde'}: eksik bilgi (${eksikler.join(', ')}). Bu satır şimdilik kullanılmıyor.` });
      continue;
    }
    if (!s.kaynak) uyarilar.push({ dosya, satir: s._satir, mesaj: `${s.madde}: kaynak yazılmamış` });
    bonuslar.get(bolumNo).push({
      madde: s.madde, gozlem: s.gozlem ?? '', soru: s.soru, dogru: s.dogru, yanlislar,
      deney: s.deney ?? '', sonuc: s.sonuc, kaynak: s.kaynak ?? '',
    });
  }
  return bonuslar;
}
