// Element Dosyaları: ekranlar ve oyun akışı.
// Dosya panosu -> dosya girişi -> görevler (gözlem, veri, hipotez, kanıt, çıkarım, argüman) -> dosya sonucu.
// Üç bilimsel hatada dosya kilitlenir; bilimsel hata analizi doğru yapılınca dosya yeniden açılır.

import { ARGUMAN_ASAMALARI, ASAMALAR, AYARLAR, BECERI_TYMM, BECERILER, HAKKINDA, HATA_TURLERI, HIKAYE, KATEGORILER, SEVIYELER, TEMALAR } from './ayarlar.js';
import { icerikYukle } from './icerik.js';
import { ELEMENTLER, elementBul, sadelestir } from './periyodik.js';
import { beceriOzeti, dosyaPuani, gorevKredisi, yuzde } from './puan.js';
import * as kayit from './kayit.js';
import {
  asamaCubugu, baglantiliMetin, duyur, ekranGoster, genisEkran, h, kanitBaglantili, kanitKarti, kanitPaneli, karistir, periyodikSecici,
} from './arayuz.js';

let icerik = null;                  // icerik/*.csv tablolarından kurulan dosyalar
let ilerleme = kayit.ilerlemeOku(); // çözülen dosyalar, kilitli dosyalar, katılımcı kodu
let tur = null;                     // açık dosya oturumu
let kanitPaneliAcik = true;

const HARFLER = 'ABCDEFGH';

// ------------------------------------------------------------------ yardımcılar

function geriButonu(hedef = panoEkrani, yazi = '← Dosya panosu') {
  return h('button', { class: 'baglanti geri', type: 'button', onclick: hedef }, yazi);
}

// replaceChildren gibi, ama boş (null/false) parçaları atlar
function doldur(dugum, ...cocuklar) {
  dugum.replaceChildren(...cocuklar.flat(Infinity).filter(c => c != null && c !== false));
}

function aciklama(baslik, metin) {
  return h('div', { class: 'aciklama' }, h('h3', {}, baslik), h('p', {}, metin));
}

function kalpler() {
  return h('span', { class: 'kalpler', role: 'img', 'aria-label': `${tur.can} hata hakkı kaldı` },
    Array.from({ length: AYARLAR.canSayisi }, (_, i) => h('span', { class: i < tur.can ? 'kalp' : 'kalp bos' }, '♥')));
}

function kaydet(olay, gorev, ek = {}) {
  kayit.kayitEkle({
    katilimci: ilerleme.katilimci || '',
    oturum: tur?.oturum ?? '',
    dosya: tur?.dosya.id ?? '',
    seviye: tur?.dosya.seviye ?? '',
    gorev: gorev?.id ?? '',
    asama: gorev?.asama ?? '',
    arguman: gorev?.arguman ?? '',
    tur: gorev?.tur ?? '',
    kategori: gorev?.kategori ?? '',
    beceri: gorev?.beceri ?? '',
    olay,
    ...ek,
  });
}

const oynanabilirler = () => icerik.dosyalar.filter(d => d.hazir);
const cozulduMu = dosya => Boolean(ilerleme.cozulen[dosya.id]);

// Seviye 1 hep açıktır. Diğer seviyeler, önceki seviyeden AYARLAR.seviyeAcmaEsigi kadar dosya çözülünce açılır.
function seviyeAcikMi(no) {
  if (no <= 1 || ilerleme.ogretmenModu) return true;
  const onceki = oynanabilirler().filter(d => d.seviye === no - 1);
  const esik = Math.min(AYARLAR.seviyeAcmaEsigi, onceki.length);
  return seviyeAcikMi(no - 1) && onceki.filter(cozulduMu).length >= esik;
}

function dosyaAcikMi(dosya) {
  return dosya.hazir && seviyeAcikMi(dosya.seviye);
}

// Aynı seviyede bu dosyadan sonra gelen ilk çözülmemiş dosya (sona gelinirse seviyenin başından aranır)
function sonrakiDosya(dosya) {
  const liste = oynanabilirler().filter(d => d.seviye === dosya.seviye);
  const i = liste.indexOf(dosya);
  return [...liste.slice(i + 1), ...liste.slice(0, i)].find(d => !cozulduMu(d) && !ilerleme.kilitli[d.id]) ?? null;
}

// ------------------------------------------------------------------ başlangıç

async function baslat() {
  document.title = `${AYARLAR.oyunAdi}: ${AYARLAR.altBaslik}`;
  try {
    icerik = await icerikYukle();
    if (ilerleme.hikayeGoruldu) panoEkrani(); else hikayeEkrani();
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

function hikayeEkrani() {
  ekranGoster(
    h('header', { class: 'kapak' },
      h('p', { class: 'birim' }, AYARLAR.birimAdi),
      h('img', { class: 'logo', src: 'img/ikon.svg', alt: '', width: 76, height: 76 }),
      h('h1', {}, AYARLAR.oyunAdi),
      h('p', { class: 'alt-baslik' }, AYARLAR.altBaslik)),
    h('section', { class: 'kart hikaye' },
      HIKAYE.map((paragraf, i) => h('p', { class: i === HIKAYE.length - 1 ? 'slogan' : null }, paragraf))),
    h('button', {
      class: 'buton genis', type: 'button',
      onclick: () => { ilerleme.hikayeGoruldu = true; kayit.ilerlemeYaz(ilerleme); panoEkrani(); },
    }, 'Göreve başla'));
}

// ------------------------------------------------------------------ dosya panosu

// Pano seçimleri (seviye sekmesi, tema ve durum filtresi) cihazda hatırlanır
function panoSecimi() {
  ilerleme.pano = { seviye: 1, tema: '', durum: '', ...(ilerleme.pano ?? {}) };
  return ilerleme.pano;
}

function kilitMesaji(no) {
  const onceki = oynanabilirler().filter(d => d.seviye === no - 1);
  const esik = Math.min(AYARLAR.seviyeAcmaEsigi, onceki.length);
  const cozulen = onceki.filter(cozulduMu).length;
  if (!seviyeAcikMi(no - 1)) return `Bu seviye kilitli. Önce Seviye ${no - 1}'i açmalısın.`;
  return `Bu seviye, Seviye ${no - 1}'den ${esik} dosya çözünce açılır. Şu an: ${Math.min(cozulen, esik)} / ${esik}.`;
}

function cip(yazi, secili, tiklaninca) {
  return h('button', { class: `cip${secili ? ' secili' : ''}`, type: 'button', 'aria-pressed': String(secili), onclick: tiklaninca }, yazi);
}

function panoEkrani() {
  tur = null;
  const secim = panoSecimi();
  const hazirlar = oynanabilirler();
  const cozulenler = hazirlar.filter(cozulduMu);
  const elementler = new Set(hazirlar.map(d => d.cevap.sembol));
  const kesfedilen = new Set(cozulenler.map(d => d.cevap.sembol));

  const sekmeAlani = h('div', { class: 'seviye-sekmeleri', role: 'group', 'aria-label': 'Seviyeler' });
  const seviyeBilgisi = h('div', { class: 'seviye-bilgisi' });
  const temaAlani = h('div', { class: 'cipler kaydir', role: 'group', 'aria-label': 'Temaya göre süz' });
  const durumAlani = h('div', { class: 'cipler', role: 'group', 'aria-label': 'Duruma göre süz' });
  const sayac = h('p', { class: 'liste-sayaci', role: 'status' });
  const izgara = h('div', { class: 'dosya-izgarasi' });

  const sec = (alan, deger) => { secim[alan] = deger; kayit.ilerlemeYaz(ilerleme); ciz(); };

  function ciz() {
    doldur(sekmeAlani, [1, 2, 3, 4].map(no => {
      const dosyalar = hazirlar.filter(d => d.seviye === no);
      if (!dosyalar.length) return null;
      const acik = seviyeAcikMi(no);
      return h('button', {
        class: `sekme${secim.seviye === no ? ' secili' : ''}${acik ? '' : ' kilitli'}`, type: 'button',
        'aria-pressed': String(secim.seviye === no), onclick: () => { secim.tema = ''; sec('seviye', no); },
      },
      h('span', { class: 'sekme-no' }, `${acik ? '' : '🔒 '}Seviye ${no}`),
      h('span', { class: 'sekme-ad' }, SEVIYELER[no].ad),
      h('span', { class: 'sekme-sayi' }, `${dosyalar.filter(cozulduMu).length}/${dosyalar.length}`));
    }));

    const seviyeDosyalari = hazirlar.filter(d => d.seviye === secim.seviye);
    doldur(seviyeBilgisi,
      h('h2', {}, h('span', { class: 'seviye-no' }, `Seviye ${secim.seviye}`), ' ', SEVIYELER[secim.seviye].ad),
      h('p', {}, SEVIYELER[secim.seviye].aciklama),
      seviyeAcikMi(secim.seviye) ? null : h('p', { class: 'serit' }, kilitMesaji(secim.seviye)));

    const temalar = Object.keys(TEMALAR).filter(t => seviyeDosyalari.some(d => d.tema === t));
    if (secim.tema && !temalar.includes(secim.tema)) secim.tema = '';
    temaAlani.replaceChildren(
      cip('Bütün temalar', !secim.tema, () => sec('tema', '')),
      ...temalar.map(t => cip(`${TEMALAR[t].simge} ${TEMALAR[t].ad}`, secim.tema === t, () => sec('tema', t))));
    durumAlani.replaceChildren(...[['', 'Hepsi'], ['acik', 'Çözülmeyenler'], ['cozuldu', 'Çözülenler']]
      .map(([k, yazi]) => cip(yazi, secim.durum === k, () => sec('durum', k))));

    const gorunen = seviyeDosyalari.filter(d => (!secim.tema || d.tema === secim.tema)
      && (secim.durum !== 'acik' || !cozulduMu(d))
      && (secim.durum !== 'cozuldu' || cozulduMu(d)));
    izgara.replaceChildren(...gorunen.map(dosyaKarti));
    sayac.textContent = gorunen.length ? `${gorunen.length} dosya` : 'Bu seçime uyan dosya yok.';
  }

  ekranGoster(
    h('header', { class: 'pano-ust' },
      h('img', { class: 'logo', src: 'img/ikon.svg', alt: '', width: 48, height: 48 }),
      h('div', {}, h('h1', {}, AYARLAR.oyunAdi), h('p', { class: 'alt-baslik' }, AYARLAR.altBaslik)),
      ilerleme.katilimci ? h('span', { class: 'rozet katilimci', title: 'Katılımcı kodu' }, ilerleme.katilimci) : null),
    ilerleme.ogretmenModu ? h('p', { class: 'serit' }, 'Öğretmen modu açık: bütün seviyeler açık.') : null,
    h('section', { class: 'kart ozet-karti' },
      h('div', { class: 'ozet-sayilar' },
        h('p', {}, h('strong', {}, String(cozulenler.length)), ` / ${hazirlar.length} vaka çözüldü`),
        h('p', {}, h('strong', {}, String(kesfedilen.size)), ` / ${elementler.size} element keşfedildi`)),
      h('div', { class: 'ozet-dugmeleri' },
        h('button', { class: 'buton kucuk', type: 'button', onclick: kesifEkrani }, 'Keşif tablosu'),
        h('button', { class: 'buton kucuk ikincil', type: 'button', onclick: raporEkrani }, 'Raporum'))),
    sekmeAlani,
    seviyeBilgisi,
    temaAlani,
    durumAlani,
    sayac,
    izgara,
    h('nav', { class: 'alt-baglantilar', 'aria-label': 'Diğer sayfalar' },
      h('button', { class: 'baglanti', type: 'button', onclick: kurallarEkrani }, 'Nasıl oynanır?'),
      h('button', { class: 'baglanti', type: 'button', onclick: hikayeEkrani }, 'Hikâye'),
      h('button', { class: 'baglanti', type: 'button', onclick: kaynakcaEkrani }, 'Bilimsel kaynakça'),
      h('button', { class: 'baglanti', type: 'button', onclick: hakkindaEkrani }, 'Hakkında'),
      h('button', { class: 'baglanti', type: 'button', onclick: ogretmenGirisi }, 'Öğretmen paneli')));
  ciz();
}

function hakkindaEkrani() {
  ekranGoster(geriButonu(), h('h2', {}, 'Hakkında'), h('section', { class: 'kart' }, HAKKINDA.map(p => h('p', {}, p))));
}

function dosyaKarti(dosya) {
  const cozum = ilerleme.cozulen[dosya.id];
  const kilitli = ilerleme.kilitli[dosya.id];
  const acik = dosyaAcikMi(dosya);
  let durum, sinif;
  if (kilitli) { durum = 'Kilitli: hata analizi bekliyor'; sinif = 'kilitlendi'; }
  else if (cozum) { durum = `Çözüldü · ${dosya.cevap.sembol} · ${cozum.puan}/100`; sinif = 'cozuldu'; }
  else if (acik) { durum = 'Soruşturmaya açık'; sinif = 'acik'; }
  else { durum = 'Seviye kilitli'; sinif = 'kapali'; }
  const tema = TEMALAR[dosya.tema];
  const ic = [
    h('span', { class: 'dosya-sekme' }, dosya.id),
    h('span', { class: 'dosya-govde' },
      tema ? h('span', { class: 'dosya-tema' }, `${tema.simge} ${tema.ad}`) : null,
      dosya.ornek ? h('span', { class: 'rozet' }, 'Tanıtım: önce bunu oyna') : null,
      dosya.final ? h('span', { class: 'rozet final' }, 'Final · Bilimsel jüri') : null,
      h('span', { class: 'dosya-baslik' }, dosya.baslik),
      h('span', { class: 'dosya-durum' }, sinif === 'kapali' ? '🔒 ' : '', durum)),
  ];
  return acik || kilitli
    ? h('button', { class: `dosya-karti ${sinif}`, type: 'button', onclick: () => dosyaAc(dosya) }, ic)
    : h('div', { class: `dosya-karti ${sinif}` }, ic);
}

function dosyaAc(dosya) {
  const kilitliHatalar = ilerleme.kilitli[dosya.id];
  if (kilitliHatalar) {
    yeniOturum(dosya);
    tur.hatalar = kilitliHatalar;
    tur.can = 0;
    kilitEkrani();
  } else {
    dosyaGirisEkrani(dosya);
  }
}

function dosyaGirisEkrani(dosya) {
  const tema = TEMALAR[dosya.tema];
  ekranGoster(
    geriButonu(),
    h('section', { class: `kart dosya-kapak${dosya.final ? ' final' : ''}` },
      h('p', { class: 'dosya-kod' }, `${dosya.id} · Seviye ${dosya.seviye}: ${SEVIYELER[dosya.seviye].ad}${tema ? ` · ${tema.simge} ${tema.ad}` : ''}`),
      dosya.final ? h('p', { class: 'juri-serit' }, 'Bilimsel jüri') : null,
      h('h2', {}, dosya.baslik),
      dosya.ornek ? h('p', { class: 'not' }, 'Bu tanıtım dosyası oyunun bütün görev türlerini gösterir; bu yüzden diğer dosyalardan daha uzundur.') : null,
      h('p', {}, dosya.giris),
      h('ul', { class: 'dosya-bilgi' },
        h('li', {}, `${dosya.gorevler.length} görev, ${dosya.kanitlar.length} kanıt`),
        h('li', {}, `${AYARLAR.canSayisi} bilimsel hata hakkın var. Hakların biterse dosya kilitlenir.`),
        h('li', {}, 'Cevabı tahmin etme: kanıtla.'))),
    h('button', { class: 'buton genis', type: 'button', onclick: () => dosyaBaslat(dosya) },
      dosya.final ? 'Jürinin karşısına çık' : 'Soruşturmayı başlat'));
}

// Keşif tablosu: en az bir vakası çözülen elementler periyodik tabloda yanar
function kesifEkrani() {
  const hazirlar = oynanabilirler();
  const vakalar = new Map();
  for (const d of hazirlar) {
    if (!vakalar.has(d.cevap.sembol)) vakalar.set(d.cevap.sembol, []);
    vakalar.get(d.cevap.sembol).push(d);
  }
  const kesfedilen = new Set(hazirlar.filter(cozulduMu).map(d => d.cevap.sembol));
  const bilgi = h('div', { class: 'kart kesif-bilgi', role: 'status' },
    h('p', { class: 'soluk' }, 'Bir elemente dokun: kaç vakası olduğunu ve çözdüğün vakaları gör.'));

  function goster(e) {
    const liste = vakalar.get(e.sembol) ?? [];
    const cozulen = liste.filter(cozulduMu);
    if (!liste.length) {
      bilgi.replaceChildren(h('h3', {}, `${e.ad} (${e.sembol}) · atom numarası ${e.z}`), h('p', { class: 'soluk' }, 'Bu element için vaka yok.'));
      return;
    }
    doldur(bilgi,
      h('h3', {}, `${e.ad} (${e.sembol}) · atom numarası ${e.z}`),
      h('p', {}, `Bu elementin ${liste.length} vakası var. ${cozulen.length ? `${cozulen.length} tanesini çözdün.` : 'Henüz hiçbirini çözmedin.'}`),
      cozulen.length
        ? h('div', { class: 'butonlar' }, cozulen.map(d => h('button', { class: 'buton kucuk ikincil', type: 'button', onclick: () => dosyaGirisEkrani(d) }, `${d.id} · ${d.baslik}`)))
        : null);
  }

  const izgara = h('div', { class: 'pt-izgara', role: 'group', 'aria-label': 'Keşif tablosu' });
  for (let grup = 1; grup <= 18; grup++) izgara.append(h('span', { class: 'pt-etiket', style: `grid-row:1;grid-column:${grup + 1}`, 'aria-hidden': 'true' }, String(grup)));
  for (let periyot = 1; periyot <= 7; periyot++) izgara.append(h('span', { class: 'pt-etiket', style: `grid-row:${periyot + 1};grid-column:1`, 'aria-hidden': 'true' }, String(periyot)));
  izgara.append(h('span', { class: 'pt-yer', style: 'grid-row:7;grid-column:4', 'aria-hidden': 'true' }, '57–71'));
  izgara.append(h('span', { class: 'pt-yer', style: 'grid-row:8;grid-column:4', 'aria-hidden': 'true' }, '89–103'));
  for (const e of ELEMENTLER) {
    const sayi = vakalar.get(e.sembol)?.length ?? 0;
    const kesif = kesfedilen.has(e.sembol);
    const durum = kesif ? 'keşfedildi' : sayi ? `${sayi} vaka, keşfedilmedi` : 'vaka yok';
    izgara.append(h('button', {
      type: 'button',
      class: `pt-hucre blok-${e.blok}${kesif ? ' kesfedildi' : sayi ? '' : ' vakasiz'}`,
      style: `grid-row:${e.satir + 1};grid-column:${e.sutun + 1}`,
      'aria-label': `${e.ad}, ${e.sembol}, atom numarası ${e.z}: ${durum}`,
      onclick: () => goster(e),
    }, h('span', { class: 'pt-z' }, String(e.z)), h('span', { class: 'pt-sembol' }, e.sembol)));
  }

  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Keşif tablosu'),
    h('p', { class: 'soluk' }, `Bir elementin en az bir vakasını çözünce o element tabloda yanar. Keşfedilen element: ${kesfedilen.size} / ${vakalar.size}`),
    h('div', { class: 'pt-kutusu' }, izgara),
    h('p', { class: 'kesif-anahtar' }, h('span', { class: 'ornek-hucre kesfedildi' }), ' keşfedildi  ', h('span', { class: 'ornek-hucre' }), ' vakası var  ', h('span', { class: 'ornek-hucre vakasiz' }), ' vaka yok'),
    bilgi);
}

// ------------------------------------------------------------------ dosya oturumu ve görevler

function yeniOturum(dosya) {
  tur = {
    dosya,
    oturum: `${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`,
    sira: 0,
    can: AYARLAR.canSayisi,
    krediler: new Map(),
    hatalar: [],
    acikKanitlar: new Set(dosya.kanitlar.filter(k => !k.goster).map(k => k.id)),
    yeniKanitlar: new Set(),
    ipucuSayisi: 0,
    baslangic: Date.now(),
  };
}

function dosyaBaslat(dosya) {
  yeniOturum(dosya);
  kanitPaneliAcik = true;
  kaydet('dosya_basladi', null);
  gorevEkrani();
}

function dosyadanCik() {
  if (!confirm('Dosyadan çıkmak istiyor musun? Bu incelemedeki ilerlemen kaybolur.')) return;
  kaydet('cikis', tur.dosya.gorevler[tur.sira]);
  panoEkrani();
}

function gorevEkrani() {
  const dosya = tur.dosya;
  const gorev = dosya.gorevler[tur.sira];
  const durum = { yanlisSayisi: 0, ipucu: false, baslangic: Date.now() };
  const gorunurKanitlar = dosya.kanitlar.filter(k => tur.acikKanitlar.has(k.id));
  const kanitIdleri = new Set(gorunurKanitlar.map(k => k.id));

  const kalpKutusu = h('span', {}, kalpler());
  const geriBildirimAlani = h('div', { class: 'geri-bildirim-alani' });
  const ipucuAlani = h('div');
  const eylemler = h('div', { class: 'eylemler' });

  let etkilesim;
  if (gorev.tur === 'savunma') etkilesim = savunmaEtkilesimi(gorev, () => sonrakiGorev(new Set()));
  else etkilesim = etkilesimOlustur(gorev, gorunurKanitlar, () => { gonder.disabled = etkilesim.cevap() == null; });

  const gonder = h('button', { class: 'buton', type: 'submit', disabled: true }, 'Gönder');
  if (gorev.tur !== 'savunma') {
    if (gorev.ipucu) {
      const ipucuDugmesi = h('button', { class: 'buton ikincil', type: 'button' }, 'İpucu al');
      ipucuDugmesi.addEventListener('click', () => {
        durum.ipucu = true;
        tur.ipucuSayisi++;
        kaydet('ipucu', gorev);
        ipucuDugmesi.remove();
        ipucuAlani.replaceChildren(h('div', { class: 'ipucu' }, h('h3', {}, 'İpucu'), h('p', {}, gorev.ipucu),
          h('p', { class: 'soluk' }, 'İpucu alınan görevden puanın yarısı alınabilir.')));
      });
      eylemler.append(ipucuDugmesi);
    }
    eylemler.append(gonder);
  }

  const kart = h('form', { class: 'kart gorev-karti', novalidate: true },
    h('div', { class: 'gorev-etiketleri' },
      h('span', { class: 'etiket' }, (gorev.arguman
        ? ARGUMAN_ASAMALARI.find(([k]) => k === gorev.arguman)?.[1]
        : ASAMALAR.find(([k]) => k === gorev.asama)?.[1]) ?? 'Görev'),
      h('span', { class: 'etiket soluk' }, KATEGORILER[gorev.kategori].ad)),
    h('h2', { class: 'gorev-sorusu' }, kanitBaglantili(gorev.soru, kanitIdleri)),
    etkilesim.dugum,
    ipucuAlani,
    eylemler,
    geriBildirimAlani);
  kart.addEventListener('submit', olay => { olay.preventDefault(); cevabiGonder(); });

  function cevabiGonder() {
    const cevap = etkilesim.cevap();
    if (cevap == null || gonder.disabled) return;
    const sonuc = degerlendir(gorev, cevap);
    if (sonuc.gecersiz) {
      geriBildirimAlani.replaceChildren(h('p', { class: 'uyari-mesaji' }, sonuc.gecersiz));
      duyur(sonuc.gecersiz);
      return;
    }
    kaydet('cevap', gorev, {
      deneme: durum.yanlisSayisi + 1,
      dogru: sonuc.dogru,
      ipucu: durum.ipucu,
      sure_sn: Math.round((Date.now() - durum.baslangic) / 1000),
      hata_turu: sonuc.dogru ? '' : sonuc.hataTuru,
      cevap: etkilesim.metin(cevap),
    });
    if (sonuc.dogru) dogruCevap(sonuc); else yanlisCevap(sonuc, cevap);
  }

  function dogruCevap(sonuc) {
    etkilesim.isaretle(true);
    etkilesim.kilitle();
    eylemler.remove();
    tur.krediler.set(gorev.id, gorevKredisi(durum));
    const acilanlar = dosya.kanitlar.filter(k => k.goster === gorev.id);
    acilanlar.forEach(k => tur.acikKanitlar.add(k.id));
    const son = tur.sira === dosya.gorevler.length - 1;
    const devam = h('button', { class: 'buton genis', type: 'button' }, son ? 'Dosyayı tamamla' : 'Sonraki görev');
    devam.addEventListener('click', () => sonrakiGorev(new Set(acilanlar.map(k => k.id))));
    geriBildirimAlani.replaceChildren(
      h('section', { class: 'geri-bildirim iyi' },
        h('p', { class: 'sonuc-baslik' }, '✓ Doğru'),
        sonuc.not ? h('p', {}, sonuc.not) : null,
        gorev.aciklama ? aciklama('Bilimsel açıklama', gorev.aciklama) : null,
        acilanlar.length
          ? h('p', { class: 'yeni-kanit' }, `Yeni kanıt açıldı: ${acilanlar.map(k => `${k.id} · ${k.baslik}`).join(', ')}`)
          : null),
      devam);
    duyur('Doğru.');
    devam.focus({ preventScroll: true });
    geriBildirimAlani.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function yanlisCevap(sonuc, cevap) {
    etkilesim.isaretle(false);
    durum.yanlisSayisi++;
    tur.can--;
    tur.hatalar.push({
      gorevId: gorev.id,
      soru: gorev.soru,
      cevapMetni: etkilesim.metin(cevap),
      hataTuru: sonuc.hataTuru,
      hataKaniti: sonuc.hataKaniti ?? '',
      aciklama: [sonuc.aciklama, sonuc.ek].filter(Boolean).join(' '),
      secenekNo: sonuc.secenekNo ?? null,
      gorunurKanitlar: [...tur.acikKanitlar],
    });
    kalpKutusu.replaceChildren(kalpler());
    kart.classList.remove('salla');
    void kart.offsetWidth;
    kart.classList.add('salla');
    const hata = HATA_TURLERI[sonuc.hataTuru] ?? HATA_TURLERI.veri;
    const kilitlendi = tur.can <= 0;
    const parcalar = [
      h('p', { class: 'sonuc-baslik' }, `✗ Bilimsel hata: ${hata.ad}`),
      sonuc.aciklama ? h('p', {}, sonuc.aciklama) : null,
      sonuc.ek ? h('p', {}, sonuc.ek) : null,
      h('p', { class: 'soluk' }, kilitlendi ? 'Hata hakkın kalmadı.' : `Kalan hata hakkın: ${tur.can}. Kanıtları yeniden incele ve tekrar dene.`),
    ];
    if (kilitlendi) {
      etkilesim.kilitle();
      eylemler.remove();
      const ileri = h('button', { class: 'buton genis tehlike', type: 'button' }, 'Dosya kilitlendi: devam et');
      ileri.addEventListener('click', dosyayiKilitle);
      geriBildirimAlani.replaceChildren(h('section', { class: 'geri-bildirim kotu' }, parcalar), ileri);
      ileri.focus({ preventScroll: true });
    } else {
      geriBildirimAlani.replaceChildren(h('section', { class: 'geri-bildirim kotu' }, parcalar));
      gonder.disabled = etkilesim.cevap() == null;
    }
    duyur(`Bilimsel hata: ${hata.ad}. Kalan hata hakkı: ${tur.can}.`);
    geriBildirimAlani.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  ekranGoster(
    h('div', { class: 'ust-cubuk' },
      h('button', { class: 'cik', type: 'button', 'aria-label': 'Dosyadan çık', onclick: dosyadanCik }, '✕'),
      h('span', { class: 'dosya-adi' }, `${dosya.id} · ${dosya.baslik}`),
      kalpKutusu),
    h('div', { class: 'ilerleme', role: 'progressbar', 'aria-label': 'Dosya ilerlemesi', 'aria-valuemin': 0, 'aria-valuemax': dosya.gorevler.length, 'aria-valuenow': tur.sira },
      h('span', { style: `width:${Math.round((100 * tur.sira) / dosya.gorevler.length)}%` })),
    h('p', { class: 'sayac' }, `Görev ${tur.sira + 1} / ${dosya.gorevler.length}`),
    asamaCubugu(gorev),
    h('div', { class: 'dosya-duzeni' },
      kart,
      kanitPaneli(gorunurKanitlar, tur.yeniKanitlar, kanitPaneliAcik || tur.yeniKanitlar.size > 0, acik => { kanitPaneliAcik = acik; })));
  genisEkran();
}

function sonrakiGorev(yeniKanitlar) {
  tur.yeniKanitlar = yeniKanitlar;
  tur.sira++;
  if (tur.sira < tur.dosya.gorevler.length) gorevEkrani(); else dosyaSonuEkrani();
}

// ------------------------------------------------------------------ görev türleri

// Her etkileşim şunları verir: dugum (ekrandaki öğe), cevap() (seçim tamamlanmadıysa null),
// metin(cevap) (kayıt için), isaretle(dogruMu) ve kilitle().
function etkilesimOlustur(gorev, gorunurKanitlar, degisince) {
  switch (gorev.tur) {
    case 'tekli': return tekliSecim(gorev, degisince);
    case 'coklu': return cokluSecim({
      ogeler: gorev.secenekler, anahtar: s => s.no, yazi: s => s.metin, kayitYazisi: s => s.metin, degisince,
    });
    case 'kanit': return cokluSecim({
      ogeler: gorunurKanitlar,
      anahtar: k => k.id,
      yazi: k => `${k.id} · ${k.baslik}${k.tablo ? ' (veri tablosu)' : `: ${k.metin}`}`,
      kayitYazisi: k => k.id,
      degisince,
      ekSinif: 'kanit-secimi',
    });
    case 'sirala': return siralama(gorev, degisince);
    case 'tablo': return tabloSecimi(degisince);
    case 'yaz': return yaziCevabi(degisince);
    default: throw new Error(`Bilinmeyen görev türü: ${gorev.tur}`);
  }
}

function secenekDugmesi(i, metin) {
  return h('button', { class: 'secenek', type: 'button', 'aria-pressed': 'false' },
    h('span', { class: 'harf', 'aria-hidden': 'true' }, HARFLER[i] ?? '•'),
    h('span', { class: 'secenek-metin' }, metin));
}

function tekliSecim(gorev, degisince) {
  const secenekler = karistir(gorev.secenekler);
  let secim = null;
  const dugmeler = secenekler.map((s, i) => {
    const d = secenekDugmesi(i, s.metin);
    d.addEventListener('click', () => {
      secim = s;
      dugmeler.forEach((x, j) => {
        x.classList.toggle('secili', secenekler[j] === s);
        x.setAttribute('aria-pressed', String(secenekler[j] === s));
      });
      degisince();
    });
    return d;
  });
  return {
    dugum: h('div', { class: 'secenekler', role: 'group', 'aria-label': 'Seçenekler' }, dugmeler),
    cevap: () => secim,
    metin: c => c.metin,
    isaretle(dogru) {
      const d = dugmeler[secenekler.indexOf(secim)];
      d.classList.remove('secili');
      d.classList.add(dogru ? 'dogru' : 'yanlis');
      if (!dogru) { d.disabled = true; secim = null; }
    },
    kilitle: () => dugmeler.forEach(d => { d.disabled = true; }),
  };
}

// ogeler: seçenekler ya da kanıtlar; anahtar: cevapta tutulan değer (seçenek no'su ya da kanıt id'si)
function cokluSecim({ ogeler, anahtar, yazi, kayitYazisi, degisince, ekSinif = '' }) {
  const secilenler = new Set();
  const dugmeler = ogeler.map((oge, i) => {
    const d = secenekDugmesi(i, yazi(oge));
    d.classList.add('coklu');
    d.addEventListener('click', () => {
      if (secilenler.has(oge)) secilenler.delete(oge); else secilenler.add(oge);
      d.classList.toggle('secili', secilenler.has(oge));
      d.setAttribute('aria-pressed', String(secilenler.has(oge)));
      degisince();
    });
    return d;
  });
  return {
    dugum: h('div', { class: `secenekler ${ekSinif}`, role: 'group', 'aria-label': 'Birden fazla seçilebilir' },
      h('p', { class: 'yonerge' }, 'Birden fazla seçebilirsin.'), dugmeler),
    cevap: () => (secilenler.size ? new Set([...secilenler].map(anahtar)) : null),
    metin: c => ogeler.filter(o => c.has(anahtar(o))).map(kayitYazisi).join(' | '),
    isaretle(dogru) {
      if (dogru) dugmeler.forEach((d, i) => { if (secilenler.has(ogeler[i])) d.classList.add('dogru'); });
    },
    kilitle: () => dugmeler.forEach(d => { d.disabled = true; }),
  };
}

function siralama(gorev, degisince) {
  const ogeler = karistir(gorev.secenekler);
  const sira = [];
  const liste = h('div', { class: 'secenekler siralama', role: 'group', 'aria-label': 'Sıralanacak öğeler' });
  const ciz = () => {
    liste.replaceChildren(...ogeler.map(oge => {
      const yer = sira.indexOf(oge);
      const d = h('button', { class: `secenek${yer >= 0 ? ' secili' : ''}`, type: 'button', 'aria-label': `${oge.metin}${yer >= 0 ? `, ${yer + 1}. sırada` : ''}` },
        h('span', { class: 'harf', 'aria-hidden': 'true' }, yer >= 0 ? String(yer + 1) : '·'),
        h('span', { class: 'secenek-metin' }, oge.metin));
      d.addEventListener('click', () => {
        if (yer >= 0) sira.splice(yer); else sira.push(oge);
        ciz();
        degisince();
      });
      return d;
    }));
  };
  ciz();
  const sifirla = h('button', { class: 'baglanti', type: 'button' }, 'Sıralamayı sıfırla');
  sifirla.addEventListener('click', () => { sira.length = 0; ciz(); degisince(); });
  let kilitli = false;
  return {
    dugum: h('div', {}, h('p', { class: 'yonerge' }, 'Öğelere sırayla dokun: ilk dokunduğun 1. sıraya yerleşir. Bir öğeye yeniden dokunursan o ve sonrası silinir.'), liste, sifirla),
    cevap: () => (sira.length === ogeler.length ? [...sira] : null),
    metin: c => c.map(o => o.metin).join(' > '),
    isaretle(dogru) {
      if (dogru) liste.querySelectorAll('.secenek').forEach(d => d.classList.add('dogru'));
    },
    kilitle() {
      kilitli = true;
      liste.querySelectorAll('button').forEach(d => { d.disabled = true; });
      sifirla.remove();
    },
    get kilitli() { return kilitli; },
  };
}

function tabloSecimi(degisince) {
  const secili = new Set();
  const sayac = h('p', { class: 'secim-sayaci' }, 'Seçilen: 0');
  const tablo = periyodikSecici(secili, () => { sayac.textContent = `Seçilen: ${secili.size}`; degisince(); });
  return {
    dugum: h('div', {}, h('p', { class: 'yonerge' }, 'Aday elementlere dokunarak işaretle. Tablo yana kaydırılabilir.'), tablo.dugum, sayac),
    cevap: () => (secili.size ? new Set(secili) : null),
    metin: c => [...c].join(' '),
    isaretle() {},
    kilitle: tablo.kilitle,
  };
}

function yaziCevabi(degisince) {
  const girdi = h('input', {
    type: 'text', class: 'yazi-girdisi', autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false',
    'aria-label': 'Cevabın', placeholder: 'Element adı ya da sembolü',
  });
  girdi.addEventListener('input', () => { girdi.classList.remove('yanlis'); degisince(); });
  return {
    dugum: girdi,
    cevap: () => girdi.value.trim() || null,
    metin: c => c,
    isaretle(dogru) { girdi.classList.toggle('dogru', dogru); girdi.classList.toggle('yanlis', !dogru); },
    kilitle: () => { girdi.disabled = true; },
  };
}

// Savunma: öğrenci jüriye argümanını yazar. Otomatik puanlanmaz; öğretmen rubrikle değerlendirir.
function savunmaEtkilesimi(gorev, bitince) {
  const kutu = h('textarea', {
    class: 'savunma-kutusu', rows: '9', 'aria-label': 'Savunman',
    placeholder: 'Elementin … olduğunu düşünüyorum çünkü…',
  });
  const sayac = h('p', { class: 'secim-sayaci' }, `0 karakter (en az ${AYARLAR.savunmaEnAzKarakter})`);
  const sun = h('button', { class: 'buton', type: 'button', disabled: true }, 'Savunmamı sun');
  const alan = h('div');
  kutu.addEventListener('input', () => {
    const uzunluk = kutu.value.trim().length;
    sayac.textContent = `${uzunluk} karakter (en az ${AYARLAR.savunmaEnAzKarakter})`;
    sun.disabled = uzunluk < AYARLAR.savunmaEnAzKarakter;
  });
  sun.addEventListener('click', () => {
    kutu.readOnly = true;
    sun.remove();
    const kutular = ARGUMAN_ASAMALARI.map(([k, ad]) => {
      const girdi = h('input', { type: 'checkbox', value: k, id: `oz-${k}` });
      return { girdi, etiket: h('label', { class: 'anahtar', for: `oz-${k}` }, girdi, h('span', {}, ad)) };
    });
    const kaydetDugmesi = h('button', { class: 'buton genis', type: 'button' }, 'Değerlendirmemi kaydet ve devam et');
    kaydetDugmesi.addEventListener('click', () => {
      kaydet('savunma', gorev, {
        cevap: kutu.value.trim(),
        oz_degerlendirme: kutular.filter(k => k.girdi.checked).map(k => k.girdi.value).join(' '),
        sure_sn: Math.round((Date.now() - baslangic) / 1000),
      });
      bitince();
    });
    doldur(alan,
      gorev.aciklama ? h('section', { class: 'geri-bildirim notr' }, h('h3', {}, 'Jüri notu: örnek bir savunma'), h('p', {}, gorev.aciklama)) : null,
      h('fieldset', { class: 'oz-degerlendirme' },
        h('legend', {}, 'Kendini değerlendir: Savunmanda bunlar var mıydı?'),
        kutular.map(k => k.etiket)),
      kaydetDugmesi);
    duyur('Savunman kaydedildi. Örnek savunmayı oku ve kendini değerlendir.');
  });
  const baslangic = Date.now();
  return {
    dugum: h('div', {},
      h('p', { class: 'not' }, 'Savunmana adını ya da kişisel bilgilerini yazma. Bu metin otomatik puanlanmaz; öğretmenin değerlendirir.'),
      kutu, sayac, sun, alan),
    cevap: () => null,
    metin: c => c,
    isaretle() {},
    kilitle() {},
  };
}

// Cevabı değerlendirir. Yanlışsa hata türünü ve cevabı ele vermeyen bir açıklama döndürür.
function degerlendir(gorev, cevap) {
  switch (gorev.tur) {
    case 'tekli':
      return cevap.dogru
        ? { dogru: true }
        : { dogru: false, hataTuru: cevap.hataTuru, hataKaniti: cevap.hataKaniti, aciklama: cevap.hataAciklamasi, secenekNo: cevap.no };
    case 'coklu': {
      const secilenler = gorev.secenekler.filter(s => cevap.has(s.no));
      const fazla = secilenler.filter(s => !s.dogru);
      const eksik = gorev.secenekler.filter(s => s.dogru && !cevap.has(s.no));
      if (!fazla.length && !eksik.length) return { dogru: true };
      if (fazla.length) {
        return {
          dogru: false, hataTuru: fazla[0].hataTuru, hataKaniti: fazla[0].hataKaniti, secenekNo: fazla[0].no,
          aciklama: `“${fazla[0].metin}”: ${fazla[0].hataAciklamasi || 'Bu seçim kanıtlarla uyuşmuyor.'}`,
          ek: eksik.length ? `Ayrıca kanıtlara uyan ${eksik.length} seçenek daha var.` : '',
        };
      }
      return { dogru: false, hataTuru: gorev.hataTuru, aciklama: `Seçimlerin doğru ama eksik: kanıtlara uyan ${eksik.length} seçenek daha var.` };
    }
    case 'kanit': {
      const eksik = [...gorev.gerekli].filter(k => !cevap.has(k));
      const fazla = [...cevap].filter(k => !gorev.gerekli.has(k) && !gorev.serbest.has(k));
      if (!eksik.length && !fazla.length) return { dogru: true };
      const parcalar = [];
      if (fazla.length) parcalar.push(`Seçtiğin kanıtlardan ${fazla.length} tanesi tek başına ayırt edici değil: adayları elemiyor.`);
      if (eksik.length) parcalar.push(`Adayları eleyen ${eksik.length} kanıt daha var.`);
      return { dogru: false, hataTuru: gorev.hataTuru, hataKaniti: fazla[0] ?? eksik[0] ?? '', aciklama: parcalar.join(' ') };
    }
    case 'sirala': {
      const yanlisYer = cevap.filter((s, i) => s.sira !== i + 1).length;
      return yanlisYer
        ? { dogru: false, hataTuru: gorev.hataTuru, aciklama: `Sıralamada ${yanlisYer} öğe yanlış yerde. Verileri yeniden karşılaştır.` }
        : { dogru: true };
    }
    case 'tablo': {
      const eksik = [...gorev.dogruSemboller].filter(s => !cevap.has(s)).length;
      const fazla = [...cevap].filter(s => !gorev.dogruSemboller.has(s)).length;
      if (!eksik && !fazla) return { dogru: true };
      const parcalar = [];
      if (fazla) parcalar.push(`İşaretlediğin ${fazla} element ipuçlarına uymuyor.`);
      if (eksik) parcalar.push(`İpuçlarına uyan ${eksik} aday daha var.`);
      return { dogru: false, hataTuru: gorev.hataTuru, aciklama: parcalar.join(' ') };
    }
    case 'yaz': {
      if (gorev.elementCevabi) {
        const element = elementBul(cevap);
        if (!element) return { gecersiz: 'Bu bir element adı ya da sembolü değil. Yazımını kontrol et; bu deneme hata sayılmadı.' };
        if (gorev.kabul.some(k => elementBul(k) === element)) {
          const not = gorev.kategori === 'sembol' && cevap !== element.sembol ? `Sembolün doğru yazılışı: ${element.sembol}` : '';
          return { dogru: true, not };
        }
        return { dogru: false, hataTuru: gorev.hataTuru, aciklama: `${element.ad} (${element.sembol}) dosyadaki kanıtlarla uyuşmuyor.` };
      }
      return gorev.kabulSade.has(sadelestir(cevap))
        ? { dogru: true }
        : { dogru: false, hataTuru: gorev.hataTuru, aciklama: 'Bu cevap dosyadaki kanıtlarla uyuşmuyor.' };
    }
    default:
      return { dogru: false, hataTuru: 'veri' };
  }
}

// ------------------------------------------------------------------ kilit ve bilimsel hata analizi

function dosyayiKilitle() {
  ilerleme.kilitli[tur.dosya.id] = tur.hatalar;
  kayit.ilerlemeYaz(ilerleme);
  kaydet('kilit', null, { cevap: tur.hatalar.map(x => `${x.gorevId}:${x.hataTuru}`).join(' ') });
  kilitEkrani();
}

function kilitEkrani() {
  ekranGoster(
    h('section', { class: 'kart kilit-karti' },
      h('p', { class: 'damga kirmizi' }, 'Dosya kilitlendi'),
      h('h2', {}, `${tur.dosya.id} · ${tur.dosya.baslik}`),
      h('p', {}, `${tur.hatalar.length} bilimsel hata yaptın. Kilidi açmak için hatalarına birlikte bakacağız. Her hata için:`),
      h('ol', { class: 'adimlar' },
        h('li', {}, 'Cevabının neden yanlış olduğunu okuyacaksın.'),
        h('li', {}, 'Bu hatayı nasıl önleyeceğini seçeceksin.')),
      h('p', { class: 'soluk' }, 'Burada yanlış seçimin cezası yok: açıklamayı yeniden okuyup tekrar deneyebilirsin.'),
      h('button', { class: 'buton genis', type: 'button', onclick: () => hataAnaliziEkrani(0) }, 'Hatalarımı incele')),
    geriButonu());
}

// Hatanın nedenini anlatan metin: önce cevap verildiği anda gösterilen açıklama,
// o yoksa (eski kayıtlar) seçeneğin hata açıklaması, o da yoksa hata türünün açıklaması.
function hataNedeni(hata, gorev) {
  if (hata.aciklama) return hata.aciklama;
  const secenek = gorev?.secenekler.find(s => s.no === hata.secenekNo);
  return secenek?.hataAciklamasi || (HATA_TURLERI[hata.hataTuru] ?? HATA_TURLERI.veri).aciklama;
}

// Bilimsel hata analizi: hatalar tek tek gösterilir. Her hatada önce neden yanlış olduğu açıklanır,
// sonra tek bir soru sorulur: "Bu hatayı nasıl önlersin?" Doğru seçilince sıradaki hataya geçilir.
function hataAnaliziEkrani(sira) {
  const dosya = tur.dosya;
  const hata = tur.hatalar[sira];
  const gorev = dosya.gorevler.find(g => g.id === hata.gorevId);
  const hataTuru = HATA_TURLERI[hata.hataTuru] ? hata.hataTuru : 'veri';
  const tanim = HATA_TURLERI[hataTuru];
  const kanit = hata.hataKaniti && hata.gorunurKanitlar?.includes(hata.hataKaniti)
    ? dosya.kanitlar.find(k => k.id === hata.hataKaniti) : null;
  const sonHata = sira === tur.hatalar.length - 1;

  const digerleri = karistir(Object.keys(HATA_TURLERI).filter(k => k !== hataTuru)).slice(0, 2);
  const secenekler = karistir([hataTuru, ...digerleri]);
  const geriBildirim = h('div', { class: 'geri-bildirim-alani' });
  let deneme = 0;
  const dugmeler = secenekler.map((k, i) => {
    const dugme = secenekDugmesi(i, HATA_TURLERI[k].yaklasim);
    dugme.addEventListener('click', () => {
      deneme++;
      const dogru = k === hataTuru;
      kaydet('analiz', gorev, { deneme, dogru, hata_turu: hataTuru, cevap: k });
      if (!dogru) {
        dugme.classList.add('yanlis');
        dugme.disabled = true;
        geriBildirim.replaceChildren(h('section', { class: 'geri-bildirim kotu' },
          h('p', {}, `Bu, "${HATA_TURLERI[k].ad}" hatasını önler. Senin hatan "${tanim.ad}" türündeydi. Yukarıdaki açıklamayı yeniden oku ve tekrar dene.`)));
        duyur('Bu seçim senin hatana uymuyor. Tekrar dene.');
        return;
      }
      dugme.classList.add('dogru');
      dugmeler.forEach(d => { d.disabled = true; });
      const ileri = h('button', { class: 'buton genis', type: 'button' }, sonHata ? 'Analizi bitir' : 'Sonraki hata');
      ileri.addEventListener('click', () => (sonHata ? analizBitti() : hataAnaliziEkrani(sira + 1)));
      geriBildirim.replaceChildren(
        h('section', { class: 'geri-bildirim iyi' },
          h('p', { class: 'sonuc-baslik' }, '✓ Doğru'),
          h('p', {}, `Bir dahaki sefere: ${tanim.yaklasim.charAt(0).toLocaleLowerCase('tr-TR')}${tanim.yaklasim.slice(1)}`)),
        ileri);
      duyur('Doğru.');
      ileri.focus({ preventScroll: true });
      geriBildirim.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
    return dugme;
  });

  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Bilimsel hata analizi'),
    h('div', { class: 'ilerleme', role: 'progressbar', 'aria-label': 'Analiz ilerlemesi', 'aria-valuemin': 0, 'aria-valuemax': tur.hatalar.length, 'aria-valuenow': sira },
      h('span', { style: `width:${Math.round((100 * sira) / tur.hatalar.length)}%` })),
    h('p', { class: 'sayac' }, `Hata ${sira + 1} / ${tur.hatalar.length}`),
    h('section', { class: 'kart analiz' },
      h('h3', {}, 'Soru'),
      h('p', {}, gorev?.soru ?? hata.soru ?? ''),
      h('h3', {}, 'Senin cevabın'),
      h('p', { class: 'verilen-cevap' }, hata.cevapMetni),
      h('h3', {}, 'Neden yanlış?'),
      h('p', {}, hataNedeni(hata, gorev)),
      kanit ? [h('p', { class: 'soluk' }, 'Bu kanıta yeniden bak:'), kanitKarti(kanit)] : null,
      gorev?.ipucu ? h('div', { class: 'ipucu' }, h('h3', {}, 'İpucu'), h('p', {}, gorev.ipucu)) : null,
      h('div', { class: 'hata-turu' },
        h('h3', {}, `Hata türü: ${tanim.ad}`),
        h('p', {}, tanim.aciklama))),
    h('section', { class: 'kart' },
      h('h3', {}, 'Bu hatayı bir dahaki sefere nasıl önlersin?'),
      h('div', { class: 'secenekler', role: 'group', 'aria-label': 'Hatayı önleme yolları' }, dugmeler),
      geriBildirim));
}

function analizBitti() {
  const dosya = tur.dosya;
  delete ilerleme.kilitli[dosya.id];
  kayit.ilerlemeYaz(ilerleme);
  kaydet('analiz_bitti', null, { cevap: tur.hatalar.map(x => `${x.gorevId}:${x.hataTuru}`).join(' ') });
  ekranGoster(h('section', { class: 'kart orta' },
    h('p', { class: 'damga yesil' }, 'Dosya yeniden açıldı'),
    h('h2', {}, 'Hata analizini tamamladın'),
    h('p', {}, 'Hatalarının nedenini artık biliyorsun. Dosyayı baştan, kanıtlara dayanarak yeniden incele.'),
    h('div', { class: 'butonlar orta' },
      h('button', { class: 'buton', type: 'button', onclick: () => dosyaBaslat(dosya) }, 'Dosyayı yeniden incele'),
      h('button', { class: 'buton ikincil', type: 'button', onclick: panoEkrani }, 'Dosya panosu'))));
}

// ------------------------------------------------------------------ dosya sonucu ve rapor

function dosyaSonuEkrani() {
  const dosya = tur.dosya;
  const puan = dosyaPuani(dosya, tur.krediler);
  const sonrakiSeviye = dosya.seviye + 1;
  const seviyeOnceAcikti = sonrakiSeviye > 4 || seviyeAcikMi(sonrakiSeviye);
  const elementOnceKesfedildi = oynanabilirler().some(d => d.cevap === dosya.cevap && cozulduMu(d));
  const onceki = ilerleme.cozulen[dosya.id];
  ilerleme.cozulen[dosya.id] = { puan: Math.max(onceki?.puan ?? 0, puan.toplam), son: puan.toplam, tarih: new Date().toISOString() };
  delete ilerleme.kilitli[dosya.id];
  kayit.ilerlemeYaz(ilerleme);
  kaydet('dosya_bitti', null, { puan: puan.toplam, sure_sn: Math.round((Date.now() - tur.baslangic) / 1000) });

  const yeniSeviye = !seviyeOnceAcikti && seviyeAcikMi(sonrakiSeviye) && oynanabilirler().some(d => d.seviye === sonrakiSeviye);
  const sonraki = sonrakiDosya(dosya);
  const dugmeler = [];
  if (yeniSeviye) {
    dugmeler.push(h('button', {
      class: 'buton', type: 'button',
      onclick: () => { panoSecimi().seviye = sonrakiSeviye; panoSecimi().tema = ''; kayit.ilerlemeYaz(ilerleme); panoEkrani(); },
    }, `Seviye ${sonrakiSeviye}'ye geç`));
  }
  if (sonraki) dugmeler.push(h('button', { class: yeniSeviye ? 'buton ikincil' : 'buton', type: 'button', onclick: () => dosyaGirisEkrani(sonraki) }, `Sonraki dosya: ${sonraki.id}`));
  dugmeler.push(h('button', { class: 'buton ikincil', type: 'button', onclick: panoEkrani }, 'Dosya panosu'));

  ekranGoster(h('section', { class: 'kart sonuc-karti' },
    h('p', { class: 'damga yesil' }, 'Dosya çözüldü'),
    h('h2', {}, `${dosya.id} · ${dosya.baslik}`),
    h('p', { class: 'kesif-rozeti' }, elementOnceKesfedildi ? 'Element: ' : 'Yeni element keşfedildi: ',
      h('strong', {}, `${dosya.cevap.ad} (${dosya.cevap.sembol})`)),
    h('p', { class: 'buyuk-puan' }, h('span', {}, String(puan.toplam)), ' / 100'),
    h('div', { class: 'grup-puanlari' }, Object.values(puan.gruplar).map(g =>
      h('div', {}, h('span', {}, g.ad), h('strong', {}, `${Math.round(g.alinan)} / ${Math.round(g.en)}`)))),
    h('ul', { class: 'cubuklar' }, puan.kategoriler.map(k => h('li', {},
      h('span', { class: 'cubuk-ad' }, k.ad),
      h('span', { class: 'cubuk' }, h('span', { style: `width:${k.en ? (100 * k.alinan) / k.en : 0}%` })),
      h('span', { class: 'cubuk-deger' }, `${Math.round(k.alinan)}/${Math.round(k.en)}`)))),
    h('p', { class: 'soluk' }, `Kalan hata hakkı: ${tur.can} · Alınan ipucu: ${tur.ipucuSayisi}`),
    yeniSeviye ? h('p', { class: 'serit' }, `Tebrikler! Seviye ${sonrakiSeviye} (${SEVIYELER[sonrakiSeviye].ad}) açıldı.`) : null,
    h('div', { class: 'butonlar orta' }, dugmeler)));
}

function beceriTablosu(kayitlar, tymm = false) {
  const ozet = beceriOzeti(kayitlar);
  const hucre = o => (o?.sayi ? `%${yuzde(o)} (${o.sayi})` : '—');
  return h('div', { class: 'tablo-kutusu', tabindex: '0', role: 'region', 'aria-label': 'Beceri özeti' },
    h('table', { class: 'veri-tablosu' },
      h('thead', {}, h('tr', {}, h('th', { scope: 'col' }, 'Beceri'), [1, 2, 3, 4].map(s => h('th', { scope: 'col' }, `Seviye ${s}`)), h('th', { scope: 'col' }, 'Toplam'))),
      h('tbody', {}, Object.entries(BECERILER).map(([b, ad]) => h('tr', {},
        h('th', { scope: 'row' }, ad, tymm ? h('span', { class: 'tymm-kodu' }, BECERI_TYMM[b]) : null),
        [1, 2, 3, 4].map(s => h('td', {}, hucre(ozet[b].seviyeler[s]))),
        h('td', {}, hucre(ozet[b].toplam)))))));
}

// Öğrencinin kendi ilerlemesi: çözülen dosyalar, puan ortalaması, keşfedilen elementler ve beceri profili
function raporEkrani() {
  const benim = kayit.kayitlariOku().filter(k => (k.katilimci || '') === (ilerleme.katilimci || ''));
  const hazirlar = oynanabilirler();
  const cozulenler = hazirlar.filter(cozulduMu);
  const puanlar = cozulenler.map(d => ilerleme.cozulen[d.id].puan);
  const ortalama = puanlar.length ? Math.round(puanlar.reduce((a, b) => a + b, 0) / puanlar.length) : 0;
  const elementler = new Set(hazirlar.map(d => d.cevap.sembol));
  const kesfedilen = new Set(cozulenler.map(d => d.cevap.sembol));
  const kutu = (ad, deger) => h('div', {}, h('span', {}, ad), h('strong', {}, deger));
  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Raporum'),
    h('section', { class: 'kart' },
      h('div', { class: 'grup-puanlari' },
        kutu('Çözülen dosya', `${cozulenler.length} / ${hazirlar.length}`),
        kutu('Puan ortalaması', puanlar.length ? `${ortalama} / 100` : '—'),
        kutu('Keşfedilen element', `${kesfedilen.size} / ${elementler.size}`),
        kutu('Kilitli dosya', String(Object.keys(ilerleme.kilitli).length))),
      h('ul', { class: 'seviye-ozeti' }, [1, 2, 3, 4].map(no => {
        const dosyalar = hazirlar.filter(d => d.seviye === no);
        return dosyalar.length
          ? h('li', {}, h('span', {}, `Seviye ${no} · ${SEVIYELER[no].ad}`), h('strong', {}, `${dosyalar.filter(cozulduMu).length} / ${dosyalar.length}`))
          : null;
      })),
      cozulenler.length && cozulenler.length === hazirlar.length ? h('p', { class: 'slogan' }, 'Bütün dosyaları çözdün. Bilim insanı cevabı tahmin etmez; kanıtlar.') : null),
    h('section', { class: 'kart' },
      h('h3', {}, 'Bilimsel beceri profilin'),
      h('p', { class: 'soluk' }, 'Her becerideki görevleri ilk denemede doğru çözme oranın (parantez içinde görev sayısı).'),
      beceriTablosu(benim)),
    h('div', { class: 'butonlar orta' },
      h('button', { class: 'buton', type: 'button', onclick: kesifEkrani }, 'Keşif tablosu'),
      h('button', { class: 'buton ikincil', type: 'button', onclick: panoEkrani }, 'Dosya panosu')));
}

// ------------------------------------------------------------------ bilgi sayfaları

function kaynakcaEkrani() {
  const seviyeler = [1, 2, 3, 4].map(no => {
    const dosyalar = oynanabilirler().filter(d => d.seviye === no);
    if (!dosyalar.length) return null;
    return h('details', { class: 'kart kaynak-seviyesi' },
      h('summary', {}, `Seviye ${no} · ${SEVIYELER[no].ad} (${dosyalar.length} dosya)`),
      dosyalar.map(d => {
        const kaynaklar = [...new Set([...d.kaynakca, ...d.kanitlar.map(k => k.kaynak).filter(Boolean)])];
        return h('section', { class: 'kaynak-dosyasi' },
          h('h3', {}, `${d.id} · ${d.baslik}`),
          kaynaklar.length ? h('ol', { class: 'kaynak-listesi' }, kaynaklar.map(k => h('li', {}, baglantiliMetin(k)))) : h('p', { class: 'soluk' }, 'Kaynak yazılmamış.'));
      }));
  });
  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Bilimsel kaynakça'),
    h('p', { class: 'soluk' }, 'Oyundaki bilgilerin dayandığı kaynaklar, dosyalara göre. Bir seviyenin kaynaklarını görmek için başlığına dokun.'),
    seviyeler);
}

function kurallarEkrani() {
  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Nasıl oynanır?'),
    h('section', { class: 'kart' },
      h('h3', {}, 'Dosyalar ve kanıtlar'),
      h('p', {}, 'Her dosyada bir elementin kimliğini kanıtlardan çıkarırsın. Kanıtlar ölçümler, gözlemler, veri tabloları, periyodik tablodaki konum ve tarihsel kayıtlardır. Bazı kanıtlar ancak doğru adımı attığında açılır.'),
      h('p', {}, 'Görevler bilimsel yöntemin aşamalarını izler: gözlem, veri, hipotez, kanıt, çıkarım ve sonuç. Dosyanın sonunda iddia, kanıt, gerekçe, karşı kanıt ve sonuçtan oluşan bir bilimsel argüman kurarsın.')),
    h('section', { class: 'kart' },
      h('h3', {}, `${AYARLAR.canSayisi} bilimsel hata hakkı`),
      h('p', {}, 'Her yanlış cevap bir bilimsel hata sayılır ve türü sana söylenir:'),
      h('ul', {}, Object.values(HATA_TURLERI).map(t => h('li', {}, h('strong', {}, t.ad), `: ${t.aciklama}`))),
      h('p', {}, 'Hata hakların biterse dosya kilitlenir. Dosyayı yeniden açmak için bilimsel hata analizi yaparsın: her hatanın neden yanlış olduğunu okur ve o hatayı nasıl önleyeceğini seçersin.')),
    h('section', { class: 'kart' },
      h('h3', {}, 'Puanlama'),
      h('p', {}, 'Her dosya 100 puan üzerinden değerlendirilir. Puan yalnızca doğru elementi bulmaya değil, bilimsel akıl yürütmene göre verilir:'),
      h('ul', {}, Object.values(KATEGORILER).map(k => h('li', {}, `${k.ad}: ${k.agirlik} puan`))),
      h('p', {}, 'Bir görevi ilk denemede doğru çözersen puanın tamamını alırsın. İpucu alırsan yarısını, yanlış deneme yaparsan hiç alamazsın ama dosyaya devam edersin. Savunma metnini öğretmenin değerlendirir.')),
    h('section', { class: 'kart' },
      h('h3', {}, 'Seviyeler'),
      h('ul', {}, Object.entries(SEVIYELER).map(([no, s]) => h('li', {}, h('strong', {}, `Seviye ${no}: ${s.ad}`), ` · ${s.aciklama}`))),
      h('p', {}, `Seviye 1 baştan açıktır. Bir sonraki seviye, önceki seviyeden ${AYARLAR.seviyeAcmaEsigi} dosya çözünce açılır. Bir seviyedeki dosyaları istediğin sırayla çözebilirsin; panodaki tema düğmeleriyle ilgini çeken konuları seçebilirsin.`)),
    h('section', { class: 'kart' },
      h('h3', {}, 'Keşif tablosu'),
      h('p', {}, 'Her dosyanın cevabı bir elementtir. Bir elementin en az bir dosyasını çözünce o element Keşif tablosunda yanar. Amacın, periyodik tablonun mümkün olduğu kadar çok elementini keşfetmek.')));
}

// ------------------------------------------------------------------ öğretmen paneli

function ogretmenGirisi() {
  const girdi = h('input', { type: 'password', id: 'sifre', class: 'yazi-girdisi', inputmode: 'numeric', autocomplete: 'off' });
  const mesaj = h('p', { class: 'uyari-mesaji', role: 'alert' });
  const form = h('form', { class: 'kart' },
    h('label', { for: 'sifre' }, 'Öğretmen şifresi'), girdi, mesaj,
    h('button', { class: 'buton', type: 'submit' }, 'Giriş'));
  form.addEventListener('submit', olay => {
    olay.preventDefault();
    if (girdi.value === AYARLAR.ogretmenSifresi) ogretmenPaneli();
    else { mesaj.textContent = 'Şifre yanlış.'; girdi.select(); }
  });
  ekranGoster(geriButonu(), h('h2', {}, 'Öğretmen paneli'),
    h('p', { class: 'soluk' }, 'Katılımcı kodları, içerik kontrolü ve araştırma verileri.'), form);
}

function ogretmenPaneli() {
  const kayitlar = kayit.kayitlariOku();

  const kodGirdisi = h('input', { type: 'text', id: 'katilimci', class: 'yazi-girdisi', maxlength: '12', autocomplete: 'off', value: ilerleme.katilimci });
  const kodMesaji = h('p', { class: 'soluk', role: 'status' });
  const kodFormu = h('form', {},
    h('label', { for: 'katilimci' }, 'Bu cihazı kullanacak öğrencinin katılımcı kodu'),
    h('div', { class: 'satir' }, kodGirdisi, h('button', { class: 'buton', type: 'submit' }, 'Kaydet')),
    h('p', { class: 'not' }, 'Ad soyad yazmayın. Yalnızca harf ve rakamdan oluşan bir kod kullanın (örnek: D07, K12). Kod her kayda eklenir.'),
    kodMesaji);
  kodFormu.addEventListener('submit', olay => {
    olay.preventDefault();
    const kod = kodGirdisi.value.trim();
    if (kod && !/^[A-Za-z0-9_-]{1,12}$/.test(kod)) { kodMesaji.textContent = 'Kod yalnızca harf, rakam, - ve _ içerebilir.'; return; }
    ilerleme.katilimci = kod;
    kayit.ilerlemeYaz(ilerleme);
    kodMesaji.textContent = kod ? `Kod kaydedildi: ${kod}` : 'Kod silindi.';
  });

  const mod = h('input', { type: 'checkbox', id: 'ogretmen-modu' });
  mod.checked = ilerleme.ogretmenModu;
  mod.addEventListener('change', () => { ilerleme.ogretmenModu = mod.checked; kayit.ilerlemeYaz(ilerleme); });

  const icerikSatirlari = icerik.dosyalar.map(d => h('tr', {},
    h('th', { scope: 'row' }, d.id),
    h('td', {}, String(d.seviye)),
    h('td', {}, d.baslik || '—'),
    h('td', {}, d.hazir ? `Hazır · ${d.gorevler.length} görev, ${d.kanitlar.length} kanıt` : d.baslik ? 'Hatalı' : 'Hazırlanıyor')));

  const katilimcilar = new Set(kayitlar.map(k => k.katilimci).filter(Boolean));
  const tarih = new Date().toISOString().slice(0, 10);

  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Öğretmen paneli'),
    h('section', { class: 'kart' }, h('h3', {}, 'Katılımcı'), kodFormu),
    h('section', { class: 'kart' },
      h('h3', {}, 'Dosyalar'),
      h('label', { class: 'anahtar', for: 'ogretmen-modu' }, mod, h('span', {}, 'Öğretmen modu: bütün seviyeler beklemeden açılsın')),
      h('div', { class: 'tablo-kutusu', tabindex: '0', role: 'region', 'aria-label': 'Dosyaların durumu' },
        h('table', { class: 'veri-tablosu' },
          h('thead', {}, h('tr', {}, ['Dosya', 'Seviye', 'Başlık', 'Durum'].map(b => h('th', { scope: 'col' }, b)))),
          h('tbody', {}, icerikSatirlari))),
      h('h3', {}, `İçerik tablolarındaki uyarılar (${icerik.uyarilar.length})`),
      icerik.uyarilar.length
        ? h('ul', { class: 'uyarilar' }, icerik.uyarilar.map(u => h('li', {}, h('strong', {}, u.satir ? `${u.dosya}, satır ${u.satir}` : u.dosya), `: ${u.mesaj}`)))
        : h('p', {}, 'Uyarı yok.'),
      h('div', { class: 'butonlar' }, h('button', { class: 'buton ikincil', type: 'button', onclick: icerigiYenile }, 'İçeriği yeniden yükle'))),
    h('section', { class: 'kart' },
      h('h3', {}, 'Araştırma verileri'),
      h('p', { class: 'soluk' }, `Bu cihazda ${kayitlar.length} kayıt var (${katilimcilar.size} katılımcı kodu). Tablo, becerilere göre ilk denemede doğru çözme oranını gösterir. Becerilerin altında, Türkiye Yüzyılı Maarif Modeli Kimya Dersi Öğretim Programı'ndaki karşılıkları yazar.`),
      beceriTablosu(kayitlar, true),
      h('div', { class: 'butonlar' },
        h('button', {
          class: 'buton', type: 'button', disabled: !kayitlar.length,
          onclick: () => kayit.dosyaIndir(`element-dosyalari-veriler-${tarih}.csv`, kayit.kayitlardanCsv(kayitlar)),
        }, 'Verileri indir (CSV)'),
        h('button', {
          class: 'buton ikincil', type: 'button',
          onclick: () => {
            if (!confirm('Bu cihazdaki ilerleme (çözülen ve kilitli dosyalar) silinsin mi? Araştırma kayıtları silinmez.')) return;
            ilerleme = kayit.ilerlemeSifirla(ilerleme);
            ogretmenPaneli();
          },
        }, 'İlerlemeyi sıfırla'),
        h('button', {
          class: 'buton ikincil tehlike', type: 'button', disabled: !kayitlar.length,
          onclick: () => {
            if (!confirm(`Bu cihazdaki ${kayitlar.length} araştırma kaydı kalıcı olarak silinsin mi? Önce verileri indirdiğinizden emin olun.`)) return;
            kayit.kayitlariSil();
            ogretmenPaneli();
          },
        }, 'Araştırma kayıtlarını sil'))));
}

async function icerigiYenile() {
  try {
    icerik = await icerikYukle();
    ogretmenPaneli();
  } catch (hata) {
    hataEkrani(hata);
  }
}

// ------------------------------------------------------------------ çalıştır

// İnternet bağlantısı gidince de oynanabilsin diye dosyaları tarayıcıda saklayan yardımcı
if ('serviceWorker' in navigator && location.protocol !== 'file:') {
  navigator.serviceWorker.register('sw.js').catch(() => { /* çevrim dışı çalışma isteğe bağlı */ });
}

baslat();
