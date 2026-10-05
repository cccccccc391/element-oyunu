// Puanlama ve araştırma özetleri.
// Bir görevin kredisi: ilk denemede ipucusuz doğru = 1, ilk denemede ipucuyla doğru = ipucu katsayısı,
// en az bir yanlış deneme = 0. Savunma metinleri otomatik puanlanmaz; öğretmen rubrikle değerlendirir.

import { AYARLAR, BECERILER, KATEGORILER, PUAN_GRUPLARI } from './ayarlar.js';

export function gorevKredisi({ yanlisSayisi, ipucu }) {
  if (yanlisSayisi > 0) return 0;
  return ipucu ? AYARLAR.ipucuKatsayisi : 1;
}

// 100 üzerinden dosya puanı. Dosyada görevi olmayan kategorilerin payı diğerlerine dağıtılır.
export function dosyaPuani(dosya, krediler) {
  const puanli = dosya.gorevler.filter(g => g.tur !== 'savunma');
  const sayilar = {};
  for (const g of puanli) sayilar[g.kategori] = (sayilar[g.kategori] ?? 0) + 1;
  const toplamAgirlik = Object.keys(sayilar).reduce((t, k) => t + KATEGORILER[k].agirlik, 0);
  const kategoriler = Object.keys(KATEGORILER).filter(k => sayilar[k]).map(k => ({
    kategori: k,
    ad: KATEGORILER[k].ad,
    grup: KATEGORILER[k].grup,
    en: toplamAgirlik ? (100 * KATEGORILER[k].agirlik) / toplamAgirlik : 0,
    alinan: 0,
  }));
  for (const g of puanli) {
    const k = kategoriler.find(x => x.kategori === g.kategori);
    k.alinan += (k.en / sayilar[g.kategori]) * (krediler.get(g.id) ?? 0);
  }
  const gruplar = {};
  for (const k of kategoriler) {
    gruplar[k.grup] ??= { ad: PUAN_GRUPLARI[k.grup], en: 0, alinan: 0 };
    gruplar[k.grup].en += k.en;
    gruplar[k.grup].alinan += k.alinan;
  }
  return { toplam: Math.round(kategoriler.reduce((t, k) => t + k.alinan, 0)), kategoriler, gruplar };
}

// Becerilere göre ilk deneme başarısı. Her dosya oturumunda her görevin yalnızca ilk denemesi sayılır.
// Sonuç: { beceri: { toplam: {dogru, sayi}, seviyeler: { 1: {dogru, sayi}, ... } } }
export function beceriOzeti(kayitlar) {
  const ozet = Object.fromEntries(Object.keys(BECERILER).map(b => [b, { toplam: { dogru: 0, sayi: 0 }, seviyeler: {} }]));
  for (const k of kayitlar) {
    if (k.olay !== 'cevap' || k.deneme !== 1 || !ozet[k.beceri]) continue;
    const hedefler = [ozet[k.beceri].toplam, (ozet[k.beceri].seviyeler[k.seviye] ??= { dogru: 0, sayi: 0 })];
    for (const h of hedefler) {
      h.sayi++;
      if (k.dogru) h.dogru++;
    }
  }
  return ozet;
}

export const yuzde = ({ dogru, sayi }) => (sayi ? Math.round((100 * dogru) / sayi) : null);
