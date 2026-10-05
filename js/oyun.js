// Oyunun ekranları ve akışı.
// Ana sayfa -> bölüm soruları -> bonus tur (bilimsel basamaklar) -> bölüm sonu

import { AYARLAR, HAKKINDA } from './ayarlar.js';
import { icerikYukle } from './icerik.js';
import { bolumSorulari, bonusMaddeleri, hazirSoruSayisi, karistir } from './sorular.js';
import { ilerlemeOku, ilerlemeSifirla, ilerlemeYaz } from './ilerleme.js';

const kok = document.getElementById('uygulama');
const duyuruAlani = document.getElementById('duyuru');
let icerik = null;              // icerik/*.csv dosyalarından okunanlar
let ilerleme = ilerlemeOku();   // açılan bölümler ve en iyi puanlar
let tur = null;                 // şu an oynanan bölüm turu

const HARFLER = 'ABCDEF';
const ADIMLAR = ['Gözlem', 'Soru', 'Hipotez', 'Deney', 'Sonuç'];

// ------------------------------------------------------------------ yardımcılar

// HTML öğesi oluşturur. Örnek: h('p', { class: 'not' }, 'Merhaba')
function h(etiket, ozellikler, ...cocuklar) {
  const dugum = document.createElement(etiket);
  for (const [ad, deger] of Object.entries(ozellikler ?? {})) {
    if (deger == null || deger === false) continue;
    if (ad.startsWith('on')) dugum.addEventListener(ad.slice(2), deger);
    else if (ad === 'class') dugum.className = deger;
    else dugum.setAttribute(ad, deger === true ? '' : deger);
  }
  for (const cocuk of cocuklar.flat(Infinity)) {
    if (cocuk == null || cocuk === false) continue;
    dugum.append(cocuk);
  }
  return dugum;
}

// Ekranı değiştirir ve odağı başlığa taşır (ekran okuyucular yeni ekranı fark etsin)
function ekranGoster(...parcalar) {
  kok.replaceChildren(...parcalar.flat(Infinity).filter(Boolean));
  window.scrollTo(0, 0);
  const baslik = kok.querySelector('h1, h2');
  if (baslik) {
    baslik.setAttribute('tabindex', '-1');
    baslik.focus({ preventScroll: true });
  }
}

// Ekran okuyuculara kısa bir duyuru yapar ("Doğru!" gibi)
function duyur(metin) {
  if (!duyuruAlani) return;
  duyuruAlani.textContent = '';
  setTimeout(() => { duyuruAlani.textContent = metin; }, 50);
}

const bolumRengi = no => `b${((no - 1) % 6) + 1}`;
const toplamPuan = () => tur.puan + tur.bonusPuani;

function aciklama(baslik, metin) {
  return h('div', { class: 'aciklama' }, h('h3', {}, baslik), h('p', {}, metin));
}

function kaynakSatiri(kaynak) {
  if (!kaynak) return null;
  const icerigi = /^https?:\/\//i.test(kaynak)
    ? h('a', { href: kaynak, target: '_blank', rel: 'noopener' }, kaynak)
    : kaynak;
  return h('p', { class: 'kaynak' }, 'Kaynak: ', icerigi);
}

function geriButonu() {
  return h('button', { class: 'baglanti geri', type: 'button', onclick: anaEkran }, '← Ana sayfa');
}

// ------------------------------------------------------------------ başlangıç

async function baslat() {
  document.title = AYARLAR.oyunAdi;
  try {
    icerik = await icerikYukle();
    anaEkran();
  } catch (hata) {
    hataEkrani(hata);
  }
}

function hataEkrani(hata) {
  ekranGoster(h('section', { class: 'kart' },
    h('h2', {}, 'Oyun açılamadı'),
    h('p', {}, hata.message),
    h('p', { class: 'soluk' }, 'Oyun bir web adresi üzerinden açılmalı ve icerik klasöründeki dosyalar yerinde olmalı. Ayrıntılar README dosyasında.'),
    h('div', { class: 'butonlar' },
      h('button', { class: 'buton', type: 'button', onclick: () => location.reload() }, 'Yeniden dene'))));
}

// ------------------------------------------------------------------ ana sayfa

function bolumAcikMi(bolum) {
  return ilerleme.ogretmenModu || bolum.no <= ilerleme.acikBolum;
}

function anaEkran() {
  tur = null;
  ekranGoster(
    h('header', { class: 'kapak' },
      h('img', { class: 'logo', src: 'img/ikon.svg', alt: '', width: 64, height: 64 }),
      h('h1', {}, AYARLAR.oyunAdi),
      h('p', { class: 'alt-baslik' }, AYARLAR.altBaslik)),
    ilerleme.ogretmenModu ? h('p', { class: 'serit' }, 'Öğretmen modu açık: bütün bölümler oynanabilir.') : null,
    h('section', { class: 'bolumler', 'aria-label': 'Bölümler' }, icerik.bolumler.map(bolumKarti)),
    h('nav', { class: 'alt-baglantilar', 'aria-label': 'Diğer sayfalar' },
      h('button', { class: 'baglanti', type: 'button', onclick: nasilOynanir }, 'Nasıl oynanır?'),
      h('button', { class: 'baglanti', type: 'button', onclick: icerikDurumu }, 'İçerik durumu'),
      h('button', { class: 'baglanti', type: 'button', onclick: hakkinda }, 'Hakkında')));
}

function bolumKarti(bolum) {
  const soruSayisi = hazirSoruSayisi(bolum);
  const acik = bolumAcikMi(bolum);
  const enIyi = ilerleme.enIyi[bolum.no];
  let bilgi = soruSayisi ? `${soruSayisi} soru hazır` : 'İçerik hazırlanıyor';
  if (soruSayisi && enIyi != null) bilgi += ` · En iyi: ${enIyi} puan`;
  return h('article', { class: `bolum-karti ${bolumRengi(bolum.no)}${acik ? '' : ' kilitli'}` },
    h('div', { class: 'bolum-ust' },
      h('span', { class: 'bolum-no' }, `${bolum.no}. Bölüm`),
      ilerleme.tamamlanan[bolum.no] ? h('span', { class: 'rozet' }, '✓ Tamamlandı') : null),
    h('h2', {}, bolum.ad),
    h('p', { class: 'aralik' }, `${bolum.baslangic}–${bolum.bitis} arası ${bolum.elementler.length} element`),
    h('div', { class: 'cipler', 'aria-hidden': 'true' }, bolum.elementler.map(e => h('span', { class: 'cip' }, e.sembol))),
    h('div', { class: 'bolum-alt' },
      h('span', { class: 'bilgi' }, bilgi),
      acik
        ? h('button', { class: 'buton', type: 'button', disabled: soruSayisi === 0, onclick: () => bolumBaslat(bolum) }, 'Başla')
        : h('span', { class: 'kilit' }, '🔒 Önceki bölümü bitir')));
}

// ------------------------------------------------------------------ sorular

function bolumBaslat(bolum) {
  const sorular = bolumSorulari(bolum);
  if (!sorular.length) return anaEkran();
  tur = { bolum, sorular, sira: 0, can: AYARLAR.canSayisi, dogruSayisi: 0, puan: 0, bonusPuani: 0, bonus: null, yeniAcilan: null };
  soruEkrani();
}

function ustCubuk(baslik, kalplerGorunsun, cikis) {
  return h('div', { class: 'ust-cubuk' },
    h('button', { class: 'cik', type: 'button', 'aria-label': 'Çık', onclick: cikis }, '✕'),
    h('span', { class: 'bolum-adi' }, baslik),
    kalplerGorunsun ? kalpler() : null,
    h('span', { class: 'puan' }, `${toplamPuan()} puan`));
}

function kalpler() {
  return h('span', { class: 'kalpler', role: 'img', 'aria-label': `${tur.can} can kaldı` },
    Array.from({ length: AYARLAR.canSayisi }, (_, i) => h('span', { class: i < tur.can ? 'kalp' : 'kalp bos' }, '♥')));
}

function bolumdenCik() {
  if (confirm('Bölümden çıkmak istiyor musun? Bu turdaki ilerlemen kaybolur.')) anaEkran();
}

function bonusVarMi() {
  return (icerik.bonuslar.get(tur.bolum.no) ?? []).length > 0;
}

function soruEkrani() {
  const soru = tur.sorular[tur.sira];
  const sonSoru = tur.sira === tur.sorular.length - 1;
  const cubukKutusu = h('div', {}, ustCubuk(`${tur.bolum.no}. Bölüm`, true, bolumdenCik));
  const geriBildirimAlani = h('div', { class: 'geri-bildirim-alani' });

  const butonlar = soru.secenekler.map((secenek, i) => {
    const buton = h('button', { class: 'secenek', type: 'button' },
      h('span', { class: 'harf', 'aria-hidden': 'true' }, HARFLER[i]),
      h('span', { class: 'secenek-metin' }, secenek.metin));
    buton.addEventListener('click', () => cevapla(secenek, buton));
    return buton;
  });

  const kart = h('section', { class: 'kart soru-karti' },
    h('h2', { class: 'soru-turu' }, soru.etiket),
    h('dl', { class: 'bilgiler' }, soru.bilgiler.map(([baslik, metin]) =>
      h('div', { class: 'bilgi-satiri' }, h('dt', {}, baslik), h('dd', {}, metin)))),
    h('p', { class: 'soru-metni' }, soru.soru),
    h('div', { class: 'secenekler' }, butonlar));

  function cevapla(secenek, buton) {
    butonlar.forEach(b => { b.disabled = true; });
    soru.secenekler.forEach((s, i) => { if (s.dogru) butonlar[i].classList.add('dogru'); });
    if (secenek.dogru) {
      tur.dogruSayisi++;
      tur.puan += AYARLAR.soruPuani;
    } else {
      buton.classList.add('yanlis');
      tur.can--;
      kart.classList.add('salla');
    }
    cubukKutusu.replaceChildren(ustCubuk(`${tur.bolum.no}. Bölüm`, true, bolumdenCik));
    duyur(secenek.dogru ? 'Doğru!' : `Yanlış. Doğru cevap: ${soru.secenekler.find(s => s.dogru).metin}`);

    const canBitti = tur.can <= 0;
    if (sonSoru && !canBitti) bolumuTamamla();
    let devamYazisi = 'Sonraki soru';
    if (canBitti) devamYazisi = 'Devam';
    else if (sonSoru) devamYazisi = bonusVarMi() ? 'Bonus tura geç' : 'Bölümü bitir';
    const devam = h('button', { class: 'buton genis', type: 'button' }, devamYazisi);
    devam.addEventListener('click', () => {
      if (canBitti) canBittiEkrani();
      else if (sonSoru) bonusGiris();
      else { tur.sira++; soruEkrani(); }
    });
    geriBildirimAlani.replaceChildren(geriBildirim(soru, secenek.dogru), devam);
    devam.focus({ preventScroll: true });
    geriBildirimAlani.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  const yuzde = Math.round((tur.sira / tur.sorular.length) * 100);
  ekranGoster(
    cubukKutusu,
    h('div', { class: 'ilerleme', role: 'progressbar', 'aria-label': 'Bölüm ilerlemesi', 'aria-valuemin': 0, 'aria-valuemax': tur.sorular.length, 'aria-valuenow': tur.sira },
      h('span', { style: `width: ${yuzde}%` })),
    h('p', { class: 'sayac' }, `Soru ${tur.sira + 1} / ${tur.sorular.length}`),
    kart,
    geriBildirimAlani);
}

// Cevaptan sonra açıklama: projenin asıl amacı öğrencinin "neden"i okuması
function geriBildirim(soru, dogruMu) {
  const element = soru.element;
  const dogruSecenek = soru.secenekler.find(s => s.dogru);
  const kullanim = soru.kullanim ?? element.kullanimlar[0];
  let kullanimAciklamasi = null;
  if (soru.kullanim) kullanimAciklamasi = aciklama('Neden?', soru.kullanim.neden);
  else if (kullanim) kullanimAciklamasi = aciklama('Nerede kullanılır?', `${kullanim.kullanim}: ${kullanim.neden}`);
  return h('section', { class: `geri-bildirim ${dogruMu ? 'iyi' : 'kotu'}` },
    h('p', { class: 'sonuc-baslik' }, dogruMu ? '✓ Doğru!' : '✗ Yanlış'),
    dogruMu ? null : h('p', { class: 'dogru-cevap' }, 'Doğru cevap: ', h('strong', {}, dogruSecenek.metin)),
    kullanimAciklamasi,
    element.isimKoken ? aciklama('Adı nereden geliyor?', element.isimKoken) : null,
    kaynakSatiri(kullanim?.kaynak || element.kaynaklar[0]));
}

function canBittiEkrani() {
  const bolum = tur.bolum;
  ekranGoster(h('section', { class: 'kart orta' },
    h('div', { class: 'buyuk-simge', 'aria-hidden': 'true' }, '💔'),
    h('h2', {}, 'Canların bitti'),
    h('p', {}, `${AYARLAR.canSayisi} yanlış yaptın, bölüm baştan başlıyor. Sorular ve sıraları değişecek.`),
    h('p', { class: 'soluk' }, `Bu turda ${tur.dogruSayisi} doğru cevap verdin.`),
    h('div', { class: 'butonlar orta' },
      h('button', { class: 'buton', type: 'button', onclick: () => bolumBaslat(bolum) }, 'Bölümü yeniden başlat'),
      h('button', { class: 'buton ikincil', type: 'button', onclick: anaEkran }, 'Ana sayfa'))));
}

// Bütün sorular can bitmeden cevaplanınca bölüm geçilmiş sayılır; bonus tur ek puan içindir.
function bolumuTamamla() {
  const bolum = tur.bolum;
  ilerleme.tamamlanan[bolum.no] = true;
  const sonraki = icerik.bolumler.find(b => b.no > bolum.no);
  if (sonraki && sonraki.no > ilerleme.acikBolum) {
    tur.yeniAcilan = sonraki;
    ilerleme.acikBolum = sonraki.no;
  }
  ilerlemeYaz(ilerleme);
}

// ------------------------------------------------------------------ bonus tur

function bonustanCik() {
  if (confirm('Bonus turu burada bitirmek istiyor musun? Kazandığın puanlar korunur.')) bolumSonu();
}

function adimListesi(simdikiAdim) {
  return h('ol', { class: 'adimlar' }, ADIMLAR.map((ad, i) => h('li', {
    class: i < simdikiAdim ? 'bitti' : i === simdikiAdim ? 'simdi' : null,
    'aria-current': i === simdikiAdim ? 'step' : null,
  }, ad)));
}

function bonusGiris() {
  const maddeler = bonusMaddeleri(icerik.bonuslar, tur.bolum.no);
  if (!maddeler.length) return bolumSonu();
  tur.bonus = { maddeler, sira: 0 };
  ekranGoster(
    ustCubuk(`${tur.bolum.no}. Bölüm · Bonus`, false, bonustanCik),
    h('section', { class: 'kart orta' },
      h('div', { class: 'buyuk-simge', 'aria-hidden': 'true' }, '🔬'),
      h('h2', {}, 'Bonus tur: Madde dedektifi'),
      h('p', {}, `Bu bölümün elementlerinden oluşan ${maddeler.length} madde seni bekliyor. Her maddede bir bilim insanı gibi çalışacaksın:`),
      adimListesi(-1),
      h('p', { class: 'soluk' }, `Deneyden önce kurduğun hipotez doğruysa ${AYARLAR.bonusIlkHipotezPuani}, deneyden sonra doğru cevaba geçersen ${AYARLAR.bonusDuzeltmePuani} bonus puan kazanırsın. Bonus turda can kaybetmezsin.`),
      h('button', { class: 'buton genis', type: 'button', onclick: bonusMaddeEkrani }, 'Başla')));
}

function bonusMaddeEkrani() {
  const madde = tur.bonus.maddeler[tur.bonus.sira];
  const secenekler = karistir([
    { metin: madde.dogru, dogru: true },
    ...madde.yanlislar.map(metin => ({ metin, dogru: false })),
  ]);
  // asama: 'hipotez' (tahmin seçilir) -> 'deney' (deney sonucu okunur, karar verilir) -> 'sonuc'
  const durum = { asama: 'hipotez', hipotez: null, secim: null, kazanilan: 0, mesaj: '' };

  function puanla() {
    const sonDogru = durum.secim.dogru, ilkDogru = durum.hipotez.dogru;
    if (sonDogru && ilkDogru) {
      durum.kazanilan = AYARLAR.bonusIlkHipotezPuani;
      durum.mesaj = madde.deney ? 'Hipotezin deneyle doğrulandı!' : 'Hipotezin doğruydu!';
    } else if (sonDogru) {
      durum.kazanilan = AYARLAR.bonusDuzeltmePuani;
      durum.mesaj = 'Deney sonucuna göre hipotezini düzelttin.';
    } else {
      durum.kazanilan = 0;
      durum.mesaj = ilkDogru ? 'İlk hipotezin doğruydu ama deneyden sonra değiştirdin.' : 'Hipotezin doğrulanmadı.';
    }
    tur.bonusPuani += durum.kazanilan;
    duyur(`${sonDogru ? 'Doğru' : 'Yanlış'}. ${durum.mesaj} ${durum.kazanilan} bonus puan.`);
  }

  function ilerle() {
    if (durum.asama === 'hipotez') {
      durum.hipotez = durum.secim;
      durum.asama = madde.deney ? 'deney' : 'sonuc';
    } else {
      durum.asama = 'sonuc';
    }
    if (durum.asama === 'sonuc') puanla();
    ciz();
  }

  function secenekListesi() {
    const onay = h('button', { class: 'buton genis', type: 'button', disabled: !durum.secim },
      durum.asama === 'hipotez' ? 'Hipotezimi kaydet' : 'Kararımı verdim');
    onay.addEventListener('click', ilerle);
    const butonlar = secenekler.map((secenek, i) => {
      const secili = durum.secim === secenek;
      const buton = h('button', { class: `secenek${secili ? ' secili' : ''}`, type: 'button', 'aria-pressed': String(secili) },
        h('span', { class: 'harf', 'aria-hidden': 'true' }, HARFLER[i]),
        h('span', { class: 'secenek-metin' }, secenek.metin));
      buton.addEventListener('click', () => {
        durum.secim = secenek;
        butonlar.forEach((b, j) => {
          b.classList.toggle('secili', secenekler[j] === secenek);
          b.setAttribute('aria-pressed', String(secenekler[j] === secenek));
        });
        onay.disabled = false;
      });
      return buton;
    });
    const not = durum.asama === 'hipotez'
      ? 'Tahminini seç: bu senin hipotezin.'
      : `Hipotezin: “${durum.hipotez.metin}”. Deney sonucuna göre koruyabilir ya da değiştirebilirsin.`;
    return [
      h('p', { class: 'hipotez-notu' }, not),
      h('div', { class: 'secenekler', role: 'group', 'aria-label': 'Şıklar' }, butonlar),
      onay,
    ];
  }

  function sonucKismi() {
    const sonrakiVar = tur.bonus.sira < tur.bonus.maddeler.length - 1;
    const devam = h('button', { class: 'buton genis', type: 'button' }, sonrakiVar ? 'Sonraki madde' : 'Bölümü bitir');
    devam.addEventListener('click', () => {
      if (sonrakiVar) { tur.bonus.sira++; bonusMaddeEkrani(); } else bolumSonu();
    });
    return [
      h('section', { class: `geri-bildirim ${durum.secim.dogru ? 'iyi' : 'kotu'}` },
        h('p', { class: 'sonuc-baslik' }, durum.secim.dogru ? '✓ Doğru!' : '✗ Yanlış'),
        h('p', {}, `${durum.mesaj} `, h('strong', {}, `+${durum.kazanilan} bonus puan`)),
        durum.secim.dogru ? null : h('p', { class: 'dogru-cevap' }, 'Doğru cevap: ', h('strong', {}, madde.dogru)),
        aciklama('Sonuç', madde.sonuc),
        kaynakSatiri(madde.kaynak)),
      devam,
    ];
  }

  function ciz() {
    const adim = { hipotez: 2, deney: 3, sonuc: 4 }[durum.asama];
    ekranGoster(
      ustCubuk(`${tur.bolum.no}. Bölüm · Bonus`, false, bonustanCik),
      h('p', { class: 'sayac' }, `Madde ${tur.bonus.sira + 1} / ${tur.bonus.maddeler.length}`),
      adimListesi(adim),
      h('section', { class: 'kart' },
        h('h2', { class: 'madde-adi' }, madde.madde),
        madde.gozlem ? aciklama('Gözlem', madde.gozlem) : null,
        aciklama('Soru', madde.soru),
        durum.asama !== 'hipotez' && madde.deney
          ? h('div', { class: 'deney' }, h('h3', {}, 'Deney'), h('p', {}, madde.deney))
          : null,
        durum.asama === 'sonuc' ? null : secenekListesi()),
      durum.asama === 'sonuc' ? sonucKismi() : null);
  }

  ciz();
}

// ------------------------------------------------------------------ bölüm sonu

function puanSatiri(baslik, deger) {
  return h('div', {}, h('dt', {}, baslik), h('dd', {}, String(deger)));
}

function bolumSonu() {
  const bolum = tur.bolum;
  const toplam = toplamPuan();
  const oncekiEnIyi = ilerleme.enIyi[bolum.no];
  const rekor = oncekiEnIyi == null || toplam > oncekiEnIyi;
  if (rekor) {
    ilerleme.enIyi[bolum.no] = toplam;
    ilerlemeYaz(ilerleme);
  }
  const sonraki = icerik.bolumler.find(b => b.no > bolum.no);
  const sonrakiHazir = sonraki && hazirSoruSayisi(sonraki) > 0;
  ekranGoster(h('section', { class: 'kart orta' },
    h('div', { class: 'buyuk-simge', 'aria-hidden': 'true' }, sonraki ? '🎉' : '🏆'),
    h('h2', {}, sonraki ? `${bolum.no}. Bölüm tamamlandı!` : 'Tebrikler, bütün bölümleri bitirdin!'),
    h('dl', { class: 'puan-tablosu' },
      puanSatiri('Doğru cevap', `${tur.dogruSayisi} / ${tur.sorular.length}`),
      puanSatiri('Soru puanı', tur.puan),
      puanSatiri('Bonus puanı', tur.bonusPuani),
      puanSatiri('Toplam', toplam)),
    rekor && oncekiEnIyi != null ? h('p', { class: 'rekor' }, 'Bu bölümdeki en yüksek puanın!') : null,
    tur.yeniAcilan ? h('p', {}, `${tur.yeniAcilan.no}. Bölüm açıldı.`) : null,
    sonraki && !sonrakiHazir ? h('p', { class: 'soluk' }, 'Sonraki bölümün içeriği henüz hazırlanıyor.') : null,
    h('div', { class: 'butonlar orta' },
      sonrakiHazir ? h('button', { class: 'buton', type: 'button', onclick: () => bolumBaslat(sonraki) }, 'Sonraki bölüm') : null,
      h('button', { class: 'buton ikincil', type: 'button', onclick: () => bolumBaslat(bolum) }, 'Tekrar oyna'),
      h('button', { class: 'buton ikincil', type: 'button', onclick: anaEkran }, 'Ana sayfa'))));
}

// ------------------------------------------------------------------ diğer sayfalar

function nasilOynanir() {
  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Nasıl oynanır?'),
    h('section', { class: 'kart' }, h('ol', { class: 'kurallar' },
      h('li', {}, `Oyunda ${icerik.bolumler.length} bölüm var. Her bölümde yaklaşık 20 element bulunur.`),
      h('li', {}, 'Her soruda bir elementin nerede kullanıldığını, hangi özelliği sayesinde orada kullanıldığını ya da adının nereden geldiğini bulursun.'),
      h('li', {}, `Her doğru cevap ${AYARLAR.soruPuani} puan. Cevaptan sonra çıkan "Neden?" açıklamasını mutlaka oku.`),
      h('li', {}, `${AYARLAR.canSayisi} canın var. Canların biterse bölüm baştan başlar; sorular ve sıraları değişir.`),
      h('li', {}, 'Bölümün sonunda bonus tur var: o bölümün elementlerinden oluşan maddeleri bir bilim insanı gibi incelersin (gözlem, soru, hipotez, deney, sonuç).'),
      h('li', {}, 'Bir bölümü bitirince sıradaki bölüm açılır.'))),
    h('button', { class: 'buton genis', type: 'button', onclick: anaEkran }, 'Anladım'));
}

function hakkinda() {
  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Hakkında'),
    h('section', { class: 'kart' }, HAKKINDA.map(paragraf => h('p', {}, paragraf))));
}

function icerikDurumu() {
  const ogretmenKutusu = h('input', { type: 'checkbox', id: 'ogretmen-modu' });
  ogretmenKutusu.checked = ilerleme.ogretmenModu;
  ogretmenKutusu.addEventListener('change', () => {
    ilerleme.ogretmenModu = ogretmenKutusu.checked;
    ilerlemeYaz(ilerleme);
  });
  const uyarilar = icerik.uyarilar;
  ekranGoster(
    geriButonu(),
    h('h2', {}, 'İçerik durumu'),
    h('p', { class: 'soluk' }, 'Öğrenciler ve öğretmen için: hangi bölümün içeriğinin hazır olduğunu ve dosyalardaki sorunları gösterir.'),
    h('section', { class: 'kart' },
      h('table', { class: 'durum-tablosu' },
        h('thead', {}, h('tr', {}, ['Bölüm', 'Soru hazır', 'İsim kökeni', 'Bonus'].map(baslik => h('th', { scope: 'col' }, baslik)))),
        h('tbody', {}, icerik.bolumler.map(b => h('tr', {},
          h('th', { scope: 'row' }, String(b.no)),
          h('td', {}, `${hazirSoruSayisi(b)} / ${b.elementler.length}`),
          h('td', {}, `${b.elementler.filter(e => e.isimKoken).length} / ${b.elementler.length}`),
          h('td', {}, `${(icerik.bonuslar.get(b.no) ?? []).length} / ${AYARLAR.bonusMaddeSayisi}`)))))),
    h('section', { class: 'kart' },
      h('h3', {}, `Dosyalardaki uyarılar (${uyarilar.length})`),
      uyarilar.length
        ? h('ul', { class: 'uyarilar' }, uyarilar.map(u =>
          h('li', {}, h('strong', {}, u.satir ? `${u.dosya}, satır ${u.satir}` : u.dosya), `: ${u.mesaj}`)))
        : h('p', {}, 'Uyarı yok.')),
    h('section', { class: 'kart' },
      h('label', { class: 'anahtar', for: 'ogretmen-modu' }, ogretmenKutusu, h('span', {}, 'Öğretmen modu: bütün bölümler kilitsiz olsun')),
      h('div', { class: 'butonlar' },
        h('button', { class: 'buton ikincil', type: 'button', onclick: icerigiYenile }, 'İçeriği yeniden yükle'),
        h('button', { class: 'buton ikincil', type: 'button', onclick: ilerlemeyiSifirla }, 'İlerlemeyi sıfırla'))));
}

async function icerigiYenile() {
  try {
    icerik = await icerikYukle();
    icerikDurumu();
  } catch (hata) {
    hataEkrani(hata);
  }
}

function ilerlemeyiSifirla() {
  if (!confirm('Bu cihazdaki bütün ilerleme ve puanlar silinsin mi?')) return;
  ilerleme = ilerlemeSifirla();
  icerikDurumu();
}

// ------------------------------------------------------------------ çalıştır

// İnternet bağlantısı gidince de oynanabilsin diye dosyaları tarayıcıda saklayan yardımcı
if ('serviceWorker' in navigator && location.protocol !== 'file:') {
  navigator.serviceWorker.register('sw.js').catch(() => { /* çevrim dışı çalışma isteğe bağlı */ });
}

baslat();
