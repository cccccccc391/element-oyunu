// Element Dosyaları: ekranlar ve oyun akışı.
// Dosya panosu -> dosya girişi -> görevler (gözlem, veri, hipotez, kanıt, çıkarım, argüman) -> dosya sonucu.
// Üç bilimsel hatada dosya kilitlenir; bilimsel hata analizi doğru yapılınca dosya yeniden açılır.

import { ARGUMAN_ASAMALARI, ASAMALAR, AYARLAR, BECERILER, HAKKINDA, HATA_TURLERI, HIKAYE, KATEGORILER, SEVIYELER } from './ayarlar.js';
import { icerikYukle } from './icerik.js';
import { elementBul, sadelestir } from './periyodik.js';
import { beceriOzeti, dosyaPuani, gorevKredisi, yuzde } from './puan.js';
import * as kayit from './kayit.js';
import {
  asamaCubugu, baglantiliMetin, duyur, ekranGoster, genisEkran, h, kanitBaglantili, kanitPaneli, karistir, periyodikSecici,
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

function dosyaAcikMi(dosya) {
  if (!dosya.hazir) return false;
  if (ilerleme.ogretmenModu) return true;
  const liste = oynanabilirler();
  const i = liste.indexOf(dosya);
  return i <= 0 || Boolean(ilerleme.cozulen[liste[i - 1].id]);
}

function sonrakiDosya(dosya) {
  const i = icerik.dosyalar.indexOf(dosya);
  return icerik.dosyalar[i + 1] ?? null;
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

function panoEkrani() {
  tur = null;
  const seviyeler = [1, 2, 3, 4].map(no => {
    const dosyalar = icerik.dosyalar.filter(d => d.seviye === no);
    if (!dosyalar.length) return null;
    return h('section', { class: 'seviye', 'aria-labelledby': `seviye-${no}` },
      h('div', { class: 'seviye-ust' },
        h('h2', { id: `seviye-${no}` }, h('span', { class: 'seviye-no' }, `Seviye ${no}`), ' ', SEVIYELER[no].ad),
        h('p', {}, SEVIYELER[no].aciklama)),
      h('div', { class: 'dosya-izgarasi' }, dosyalar.map(dosyaKarti)));
  });
  ekranGoster(
    h('header', { class: 'pano-ust' },
      h('img', { class: 'logo', src: 'img/ikon.svg', alt: '', width: 48, height: 48 }),
      h('div', {}, h('h1', {}, AYARLAR.oyunAdi), h('p', { class: 'alt-baslik' }, AYARLAR.altBaslik)),
      ilerleme.katilimci ? h('span', { class: 'rozet katilimci', title: 'Katılımcı kodu' }, ilerleme.katilimci) : null),
    ilerleme.ogretmenModu ? h('p', { class: 'serit' }, 'Öğretmen modu açık: bütün dosyalar açılabilir.') : null,
    seviyeler,
    h('nav', { class: 'alt-baglantilar', 'aria-label': 'Diğer sayfalar' },
      h('button', { class: 'baglanti', type: 'button', onclick: kurallarEkrani }, 'Nasıl oynanır?'),
      h('button', { class: 'baglanti', type: 'button', onclick: hikayeEkrani }, 'Hikâye'),
      h('button', { class: 'baglanti', type: 'button', onclick: kaynakcaEkrani }, 'Bilimsel kaynakça'),
      h('button', { class: 'baglanti', type: 'button', onclick: hakkindaEkrani }, 'Hakkında'),
      h('button', { class: 'baglanti', type: 'button', onclick: ogretmenGirisi }, 'Öğretmen paneli')));
}

function hakkindaEkrani() {
  ekranGoster(geriButonu(), h('h2', {}, 'Hakkında'), h('section', { class: 'kart' }, HAKKINDA.map(p => h('p', {}, p))));
}

function dosyaKarti(dosya) {
  const cozum = ilerleme.cozulen[dosya.id];
  const kilitli = dosya.hazir && ilerleme.kilitli[dosya.id];
  const acik = dosyaAcikMi(dosya);
  let durum, sinif, dugmeYazisi = null;
  if (!dosya.hazir) { durum = 'Dosya hazırlanıyor'; sinif = 'hazirlaniyor'; }
  else if (kilitli) { durum = 'Kilitli: hata analizi bekliyor'; sinif = 'kilitlendi'; dugmeYazisi = 'Hata analizine git'; }
  else if (cozum) { durum = `Çözüldü · ${cozum.puan}/100`; sinif = 'cozuldu'; dugmeYazisi = 'Yeniden incele'; }
  else if (acik) { durum = 'Soruşturmaya açık'; sinif = 'acik'; dugmeYazisi = 'Dosyayı aç'; }
  else { durum = 'Önce önceki dosyayı çöz'; sinif = 'kapali'; }
  return h('article', { class: `dosya-karti ${sinif}` },
    h('div', { class: 'dosya-sekme' }, dosya.id),
    h('div', { class: 'dosya-govde' },
      h('div', { class: 'rozetler' },
        dosya.ornek ? h('span', { class: 'rozet' }, 'Örnek') : null,
        dosya.final ? h('span', { class: 'rozet final' }, 'Final · Bilimsel jüri') : null),
      h('h3', {}, dosya.baslik || 'Gizli dosya'),
      h('p', { class: 'dosya-durum' }, sinif === 'kapali' ? '🔒 ' : '', durum),
      dugmeYazisi ? h('button', { class: 'buton kucuk', type: 'button', onclick: () => dosyaAc(dosya) }, dugmeYazisi) : null));
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
  ekranGoster(
    geriButonu(),
    h('section', { class: `kart dosya-kapak${dosya.final ? ' final' : ''}` },
      h('p', { class: 'dosya-kod' }, `${dosya.id} · Seviye ${dosya.seviye}: ${SEVIYELER[dosya.seviye].ad}`),
      dosya.final ? h('p', { class: 'juri-serit' }, 'Bilimsel jüri') : null,
      h('h2', {}, dosya.baslik),
      dosya.ornek ? h('p', { class: 'not' }, 'Bu bir örnek dosyadır: oyunun bütün görev türlerini gösterir. Bilgileri öğrenciler kaynaklardan kontrol etmelidir.') : null,
      h('p', {}, dosya.giris),
      h('ul', { class: 'dosya-bilgi' },
        h('li', {}, `${dosya.gorevler.length} görev, ${dosya.kanitlar.length} kanıt`),
        h('li', {}, `${AYARLAR.canSayisi} bilimsel hata hakkın var. Hakların biterse dosya kilitlenir.`),
        h('li', {}, 'Cevabı tahmin etme: kanıtla.'))),
    h('button', { class: 'buton genis', type: 'button', onclick: () => dosyaBaslat(dosya) },
      dosya.final ? 'Jürinin karşısına çık' : 'Soruşturmayı başlat'));
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
      cevapMetni: etkilesim.metin(cevap),
      hataTuru: sonuc.hataTuru,
      hataKaniti: sonuc.hataKaniti ?? '',
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
    alan.replaceChildren(
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
      h('p', { class: 'damga kirmizi' }, 'Araştırma dosyası kilitlendi'),
      h('h2', {}, `${tur.dosya.id} · ${tur.dosya.baslik}`),
      h('p', {}, `${tur.hatalar.length} bilimsel hata yaptın:`),
      h('ul', { class: 'hata-listesi' }, tur.hatalar.map(x => h('li', {}, HATA_TURLERI[x.hataTuru]?.ad ?? 'Bilimsel hata'))),
      h('p', {}, 'Yeni dosyaya geçmeden önce hatalarını bir bilim insanı gibi analiz etmelisin. Doğru cevaplar sana verilmeyecek; hatanın kaynağını sen bulacaksın.'),
      h('button', { class: 'buton genis', type: 'button', onclick: hataAnaliziEkrani }, 'Bilimsel hata analizine başla')),
    geriButonu());
}

// Her hata için: hangi kanıt yanlış yorumlandı, hangi varsayım hatalıydı, doğru yaklaşım ne olmalıydı?
function analizSorulari(hata) {
  const dosya = tur.dosya;
  const gorev = dosya.gorevler.find(g => g.id === hata.gorevId);
  const sorular = [];
  if (hata.hataKaniti && dosya.kanitlar.some(k => k.id === hata.hataKaniti)) {
    sorular.push({
      anahtar: 'kanit',
      soru: 'Bu hatada hangi kanıtı yanlış yorumladın ya da gözden kaçırdın?',
      secenekler: dosya.kanitlar.filter(k => hata.gorunurKanitlar.includes(k.id)).map(k => ({ deger: k.id, metin: `${k.id} · ${k.baslik}` })),
      dogru: hata.hataKaniti,
    });
  }
  const varsayimlar = gorev?.secenekler.filter(s => !s.dogru && s.hataAciklamasi) ?? [];
  if (hata.secenekNo != null && varsayimlar.length >= 2 && varsayimlar.some(s => s.no === hata.secenekNo)) {
    sorular.push({
      anahtar: 'varsayim',
      soru: 'Cevabındaki hatalı varsayımı en iyi hangisi açıklıyor?',
      secenekler: karistir(varsayimlar).map(s => ({ deger: String(s.no), metin: s.hataAciklamasi })),
      dogru: String(hata.secenekNo),
    });
  } else {
    sorular.push({
      anahtar: 'tur',
      soru: 'Bu hata hangi türdendi?',
      secenekler: Object.entries(HATA_TURLERI).map(([k, v]) => ({ deger: k, metin: `${v.ad}: ${v.aciklama}` })),
      dogru: hata.hataTuru,
    });
  }
  sorular.push({
    anahtar: 'yaklasim',
    soru: 'Bu görevi yeniden çözerken hangi bilimsel yaklaşımı izlemelisin?',
    secenekler: karistir(Object.entries(HATA_TURLERI)).map(([k, v]) => ({ deger: k, metin: v.yaklasim })),
    dogru: hata.hataTuru,
  });
  return { gorev, sorular };
}

function hataAnaliziEkrani() {
  const analizler = tur.hatalar.map(analizSorulari);
  const secimler = analizler.map(() => ({}));
  const mesaj = h('p', { class: 'uyari-mesaji', role: 'alert' });
  let deneme = 0;

  const bolumler = analizler.map((analiz, i) => {
    const hata = tur.hatalar[i];
    return h('section', { class: 'kart analiz' },
      h('h3', {}, `Hata ${i + 1} / ${analizler.length}`),
      analiz.gorev ? h('p', { class: 'soluk' }, analiz.gorev.soru) : null,
      h('p', {}, 'Senin cevabın: ', h('strong', {}, hata.cevapMetni)),
      analiz.sorular.map((soru, j) => h('fieldset', { class: 'analiz-sorusu', 'data-hata': i, 'data-soru': soru.anahtar },
        h('legend', {}, `${j + 1}. ${soru.soru}`),
        soru.secenekler.map((s, k) => {
          const id = `analiz-${i}-${soru.anahtar}-${k}`;
          const girdi = h('input', { type: 'radio', name: `analiz-${i}-${soru.anahtar}`, value: s.deger, id });
          girdi.addEventListener('change', () => { secimler[i][soru.anahtar] = s.deger; });
          return h('label', { class: 'radyo', for: id }, girdi, h('span', {}, s.metin));
        }))));
  });

  const gonder = h('button', { class: 'buton genis', type: 'button' }, 'Analizi gönder');
  gonder.addEventListener('click', () => {
    let bos = 0, yanlis = 0;
    document.querySelectorAll('.analiz-sorusu').forEach(alan => {
      const i = Number(alan.dataset.hata), anahtar = alan.dataset.soru;
      const soru = analizler[i].sorular.find(s => s.anahtar === anahtar);
      const secim = secimler[i][anahtar];
      const dogru = secim === soru.dogru;
      if (secim == null) bos++; else if (!dogru) yanlis++;
      alan.classList.toggle('yanlis', secim != null && !dogru);
    });
    if (bos) { mesaj.textContent = `Cevaplanmamış ${bos} soru var.`; return; }
    deneme++;
    kaydet('analiz', null, { deneme, dogru: yanlis === 0, cevap: `${yanlis} yanlış` });
    if (yanlis) {
      mesaj.textContent = `Analizinde ${yanlis} hatalı nokta var (kırmızı çerçeveli). Kanıtları ve cevabını yeniden düşün.`;
      duyur(mesaj.textContent);
      return;
    }
    delete ilerleme.kilitli[tur.dosya.id];
    kayit.ilerlemeYaz(ilerleme);
    const dosya = tur.dosya;
    ekranGoster(h('section', { class: 'kart orta' },
      h('p', { class: 'damga yesil' }, 'Dosya yeniden açıldı'),
      h('h2', {}, 'Analizin doğru'),
      h('p', {}, 'Hatalarının kaynağını buldun. Şimdi dosyayı baştan, kanıtlara dayanarak yeniden incele.'),
      h('button', { class: 'buton genis', type: 'button', onclick: () => dosyaBaslat(dosya) }, 'Dosyayı yeniden incele')));
  });

  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Bilimsel hata analizi'),
    h('p', { class: 'soluk' }, 'Her hata için soruları cevapla. Analizin doğru olduğunda dosya yeniden açılır.'),
    bolumler,
    mesaj,
    gonder);
}

// ------------------------------------------------------------------ dosya sonucu ve oyun sonu

function dosyaSonuEkrani() {
  const dosya = tur.dosya;
  const puan = dosyaPuani(dosya, tur.krediler);
  const onceki = ilerleme.cozulen[dosya.id];
  ilerleme.cozulen[dosya.id] = { puan: Math.max(onceki?.puan ?? 0, puan.toplam), son: puan.toplam, tarih: new Date().toISOString() };
  delete ilerleme.kilitli[dosya.id];
  kayit.ilerlemeYaz(ilerleme);
  kaydet('dosya_bitti', null, { puan: puan.toplam, sure_sn: Math.round((Date.now() - tur.baslangic) / 1000) });

  const sonraki = sonrakiDosya(dosya);
  const hepsiCozuldu = icerik.dosyalar.every(d => d.hazir && ilerleme.cozulen[d.id]);
  const dugmeler = [];
  if (hepsiCozuldu) dugmeler.push(h('button', { class: 'buton', type: 'button', onclick: oyunSonuEkrani }, 'Araştırmayı tamamla'));
  else if (sonraki?.hazir && dosyaAcikMi(sonraki)) dugmeler.push(h('button', { class: 'buton', type: 'button', onclick: () => dosyaGirisEkrani(sonraki) }, 'Sonraki dosya'));
  dugmeler.push(h('button', { class: 'buton ikincil', type: 'button', onclick: panoEkrani }, 'Dosya panosu'));

  ekranGoster(h('section', { class: 'kart sonuc-karti' },
    h('p', { class: 'damga yesil' }, 'Dosya çözüldü'),
    h('h2', {}, `${dosya.id} · ${dosya.baslik}`),
    h('p', { class: 'buyuk-puan' }, h('span', {}, String(puan.toplam)), ' / 100'),
    h('div', { class: 'grup-puanlari' }, Object.values(puan.gruplar).map(g =>
      h('div', {}, h('span', {}, g.ad), h('strong', {}, `${Math.round(g.alinan)} / ${Math.round(g.en)}`)))),
    h('ul', { class: 'cubuklar' }, puan.kategoriler.map(k => h('li', {},
      h('span', { class: 'cubuk-ad' }, k.ad),
      h('span', { class: 'cubuk' }, h('span', { style: `width:${k.en ? (100 * k.alinan) / k.en : 0}%` })),
      h('span', { class: 'cubuk-deger' }, `${Math.round(k.alinan)}/${Math.round(k.en)}`)))),
    h('p', { class: 'soluk' }, `Kalan hata hakkı: ${tur.can} · Alınan ipucu: ${tur.ipucuSayisi}`),
    sonraki && !sonraki.hazir ? h('p', { class: 'soluk' }, 'Sıradaki dosya henüz hazırlanıyor.') : null,
    h('div', { class: 'butonlar orta' }, dugmeler)));
}

function beceriTablosu(kayitlar) {
  const ozet = beceriOzeti(kayitlar);
  const hucre = o => (o?.sayi ? `%${yuzde(o)} (${o.sayi})` : '—');
  return h('div', { class: 'tablo-kutusu', tabindex: '0', role: 'region', 'aria-label': 'Beceri özeti' },
    h('table', { class: 'veri-tablosu' },
      h('thead', {}, h('tr', {}, h('th', { scope: 'col' }, 'Beceri'), [1, 2, 3, 4].map(s => h('th', { scope: 'col' }, `Seviye ${s}`)), h('th', { scope: 'col' }, 'Toplam'))),
      h('tbody', {}, Object.entries(BECERILER).map(([b, ad]) => h('tr', {},
        h('th', { scope: 'row' }, ad),
        [1, 2, 3, 4].map(s => h('td', {}, hucre(ozet[b].seviyeler[s]))),
        h('td', {}, hucre(ozet[b].toplam)))))));
}

function oyunSonuEkrani() {
  const benim = kayit.kayitlariOku().filter(k => (k.katilimci || '') === (ilerleme.katilimci || ''));
  const puanlar = Object.values(ilerleme.cozulen).map(c => c.puan);
  const ortalama = puanlar.length ? Math.round(puanlar.reduce((a, b) => a + b, 0) / puanlar.length) : 0;
  ekranGoster(
    h('section', { class: 'kart orta' },
      h('p', { class: 'damga yesil' }, 'Araştırma tamamlandı'),
      h('h2', {}, 'Bütün dosyaları çözdün'),
      h('p', {}, `Dosya puanlarının ortalaması: ${ortalama} / 100`),
      h('p', { class: 'slogan' }, 'Bilim insanı cevabı tahmin etmez; kanıtlar.')),
    h('section', { class: 'kart' },
      h('h3', {}, 'Bilimsel beceri profilin'),
      h('p', { class: 'soluk' }, 'Her becerideki görevleri ilk denemede doğru çözme oranın (parantez içinde görev sayısı).'),
      beceriTablosu(benim)),
    h('div', { class: 'butonlar orta' },
      h('button', { class: 'buton', type: 'button', onclick: kaynakcaEkrani }, 'Bilimsel kaynakça'),
      h('button', { class: 'buton ikincil', type: 'button', onclick: panoEkrani }, 'Dosya panosu')));
}

// ------------------------------------------------------------------ bilgi sayfaları

function kaynakcaEkrani() {
  const bolumler = oynanabilirler().map(d => {
    const kaynaklar = [...new Set([...d.kaynakca, ...d.kanitlar.map(k => k.kaynak).filter(Boolean)])];
    return h('section', { class: 'kart' },
      h('h3', {}, `${d.id} · ${d.baslik}`),
      kaynaklar.length ? h('ol', { class: 'kaynak-listesi' }, kaynaklar.map(k => h('li', {}, baglantiliMetin(k)))) : h('p', { class: 'soluk' }, 'Kaynak yazılmamış.'));
  });
  ekranGoster(
    geriButonu(),
    h('h2', {}, 'Bilimsel kaynakça'),
    h('p', { class: 'soluk' }, 'Oyundaki bilgilerin dayandığı kaynaklar, dosyalara göre.'),
    bolumler);
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
      h('p', {}, 'Hata hakların biterse dosya kilitlenir. Dosyayı yeniden açmak için bilimsel hata analizi yaparsın: hangi kanıtı yanlış yorumladığını, hangi varsayımının hatalı olduğunu ve doğru yaklaşımın ne olduğunu bulursun.')),
    h('section', { class: 'kart' },
      h('h3', {}, 'Puanlama'),
      h('p', {}, 'Her dosya 100 puan üzerinden değerlendirilir. Puan yalnızca doğru elementi bulmaya değil, bilimsel akıl yürütmene göre verilir:'),
      h('ul', {}, Object.values(KATEGORILER).map(k => h('li', {}, `${k.ad}: ${k.agirlik} puan`))),
      h('p', {}, 'Bir görevi ilk denemede doğru çözersen puanın tamamını alırsın. İpucu alırsan yarısını, yanlış deneme yaparsan hiç alamazsın ama dosyaya devam edersin. Savunma metnini öğretmenin değerlendirir.')),
    h('section', { class: 'kart' },
      h('h3', {}, 'Seviyeler'),
      h('ul', {}, Object.entries(SEVIYELER).map(([no, s]) => h('li', {}, h('strong', {}, `Seviye ${no}: ${s.ad}`), ` · ${s.aciklama}`)))));
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
      h('label', { class: 'anahtar', for: 'ogretmen-modu' }, mod, h('span', {}, 'Öğretmen modu: bütün dosyalar sırayla beklemeden açılabilsin')),
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
      h('p', { class: 'soluk' }, `Bu cihazda ${kayitlar.length} kayıt var (${katilimcilar.size} katılımcı kodu). Tablo, becerilere göre ilk denemede doğru çözme oranını gösterir.`),
      beceriTablosu(kayitlar),
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
