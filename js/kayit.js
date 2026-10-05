// İlerleme ve araştırma kayıtları yalnızca bu cihazdaki tarayıcıda saklanır.
// Kişisel bilgi tutulmaz: öğrenciler ad yerine öğretmenin verdiği bir katılımcı kodu kullanır.
// Tarayıcı depolamayı engellerse oyun yine çalışır, yalnızca ilerleme hatırlanmaz.

const ILERLEME = 'element-dosyalari-ilerleme';
const KAYITLAR = 'element-dosyalari-kayitlar';

const bosIlerleme = () => ({ cozulen: {}, kilitli: {}, ogretmenModu: false, katilimci: '', hikayeGoruldu: false });

export function ilerlemeOku() {
  try {
    const kayit = JSON.parse(localStorage.getItem(ILERLEME));
    if (kayit && typeof kayit === 'object') return { ...bosIlerleme(), ...kayit };
  } catch { /* depolama kapalı ya da kayıt bozuk */ }
  return bosIlerleme();
}

export function ilerlemeYaz(ilerleme) {
  try { localStorage.setItem(ILERLEME, JSON.stringify(ilerleme)); } catch { /* depolama kapalı */ }
}

export function ilerlemeSifirla(eski) {
  const yeni = bosIlerleme();
  yeni.katilimci = eski?.katilimci ?? '';
  ilerlemeYaz(yeni);
  return yeni;
}

export function kayitlariOku() {
  try {
    const liste = JSON.parse(localStorage.getItem(KAYITLAR));
    return Array.isArray(liste) ? liste : [];
  } catch { return []; }
}

export function kayitEkle(kayit) {
  try {
    const liste = kayitlariOku();
    // Cihazın yerel saatiyle, Excel'in tanıdığı biçimde: 2026-10-06 14:05:09
    liste.push({ zaman: new Date().toLocaleString('sv-SE'), ...kayit });
    localStorage.setItem(KAYITLAR, JSON.stringify(liste));
  } catch { /* depolama kapalı */ }
}

export function kayitlariSil() {
  try { localStorage.removeItem(KAYITLAR); } catch { /* depolama kapalı */ }
}

export const KAYIT_SUTUNLARI = ['katilimci', 'zaman', 'oturum', 'dosya', 'seviye', 'gorev', 'asama', 'arguman', 'tur',
  'kategori', 'beceri', 'olay', 'deneme', 'dogru', 'ipucu', 'sure_sn', 'hata_turu', 'cevap', 'puan', 'oz_degerlendirme'];

// Türkçe Excel'de doğrudan açılan CSV (noktalı virgüllü, UTF-8 BOM'lu)
export function kayitlardanCsv(kayitlar) {
  const hucre = deger => {
    if (deger == null) return '';
    const metin = typeof deger === 'boolean' ? (deger ? '1' : '0') : String(deger);
    return /[;"\n\r]/.test(metin) ? `"${metin.replace(/"/g, '""')}"` : metin;
  };
  const satirlar = [KAYIT_SUTUNLARI.join(';'), ...kayitlar.map(k => KAYIT_SUTUNLARI.map(s => hucre(k[s])).join(';'))];
  return '﻿' + satirlar.join('\r\n');
}

export function dosyaIndir(ad, icerik, tur = 'text/csv;charset=utf-8') {
  const adres = URL.createObjectURL(new Blob([icerik], { type: tur }));
  const baglanti = Object.assign(document.createElement('a'), { href: adres, download: ad });
  document.body.append(baglanti);
  baglanti.click();
  baglanti.remove();
  setTimeout(() => URL.revokeObjectURL(adres), 1000);
}
