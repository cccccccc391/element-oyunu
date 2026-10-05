// CSV dosyalarını okur.
// Google E-Tablolar'dan inen dosyalar (virgüllü, UTF-8) de, Türkçe Excel'in kaydettiği
// dosyalar (noktalı virgüllü, Windows-1254) de okunabilir.

export async function csvYukle(yol) {
  const yanit = await fetch(yol, { cache: 'no-store' });
  if (!yanit.ok) throw new Error(`${yol} dosyası okunamadı (hata ${yanit.status}).`);
  return csvCoz(metneCevir(new Uint8Array(await yanit.arrayBuffer())));
}

export function metneCevir(baytlar) {
  try {
    return new TextDecoder('utf-8', { fatal: true }).decode(baytlar).replace(/^﻿/, '');
  } catch {
    // UTF-8 değilse Türkçe Windows kodlamasıyla oku (Excel'in varsayılan kaydı)
    return new TextDecoder('windows-1254').decode(baytlar);
  }
}

// Sütun adlarını sadeleştirir: "İsim_Köken" -> "isim_koken", "Özellik" -> "ozellik"
export function sutunAdi(ad) {
  const harfler = { ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u' };
  return ad.trim().toLocaleLowerCase('tr-TR')
    .replace(/[çğıöşü]/g, harf => harfler[harf])
    .replace(/\s+/g, '_');
}

// Metni satırlara ve hücrelere ayırır. İlk satır sütun adlarıdır.
// Her kayıt, hata mesajlarında kullanmak için dosyadaki satır numarasını (_satir) da taşır.
export function csvCoz(metin) {
  metin = metin.replace(/\r\n?/g, '\n');
  const ilkSatir = metin.split('\n', 1)[0];
  const ayirici = say(ilkSatir, ';') > say(ilkSatir, ',') ? ';' : ',';

  const satirlar = [];
  let hucreler = [], hucre = '', tirnakIcinde = false;
  let satirNo = 1, baslangic = 1;
  for (let i = 0; i < metin.length; i++) {
    const harf = metin[i];
    if (tirnakIcinde) {
      if (harf === '"' && metin[i + 1] === '"') { hucre += '"'; i++; }
      else if (harf === '"') tirnakIcinde = false;
      else { if (harf === '\n') satirNo++; hucre += harf; }
    } else if (harf === '"') {
      tirnakIcinde = true;
    } else if (harf === ayirici) {
      hucreler.push(hucre); hucre = '';
    } else if (harf === '\n') {
      hucreler.push(hucre);
      satirlar.push({ no: baslangic, hucreler });
      hucreler = []; hucre = '';
      satirNo++; baslangic = satirNo;
    } else {
      hucre += harf;
    }
  }
  if (hucre !== '' || hucreler.length) {
    hucreler.push(hucre);
    satirlar.push({ no: baslangic, hucreler });
  }

  const doluSatirlar = satirlar.filter(s => s.hucreler.some(h => h.trim() !== ''));
  if (!doluSatirlar.length) return [];
  const sutunlar = doluSatirlar[0].hucreler.map(sutunAdi);
  return doluSatirlar.slice(1).map(s => {
    const kayit = { _satir: s.no };
    sutunlar.forEach((sutun, j) => { if (sutun) kayit[sutun] = (s.hucreler[j] ?? '').trim(); });
    return kayit;
  });
}

function say(metin, aranan) {
  return metin.split(aranan).length - 1;
}
