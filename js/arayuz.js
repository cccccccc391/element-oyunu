// Ekran parçaları: HTML öğesi oluşturma, kanıt kartları, veri tablosu, periyodik tablo seçici, aşama çubuğu.

import { ARGUMAN_ASAMALARI, ASAMALAR } from './ayarlar.js';
import { ELEMENTLER } from './periyodik.js';

const kok = document.getElementById('uygulama');
const duyuruAlani = document.getElementById('duyuru');

// HTML öğesi oluşturur. Örnek: h('p', { class: 'not' }, 'Merhaba')
export function h(etiket, ozellikler, ...cocuklar) {
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
export function ekranGoster(...parcalar) {
  kok.className = '';
  kok.replaceChildren(...parcalar.flat(Infinity).filter(Boolean));
  window.scrollTo(0, 0);
  const baslik = kok.querySelector('h1, h2');
  if (baslik) {
    baslik.setAttribute('tabindex', '-1');
    baslik.focus({ preventScroll: true });
  }
}

export function genisEkran() {
  kok.classList.add('genis');
}

// Ekran okuyuculara kısa bir duyuru yapar ("Doğru" gibi)
export function duyur(metin) {
  if (!duyuruAlani) return;
  duyuruAlani.textContent = '';
  setTimeout(() => { duyuruAlani.textContent = metin; }, 50);
}

export function karistir(dizi, rastgele = Math.random) {
  const sonuc = [...dizi];
  for (let i = sonuc.length - 1; i > 0; i--) {
    const j = Math.floor(rastgele() * (i + 1));
    [sonuc[i], sonuc[j]] = [sonuc[j], sonuc[i]];
  }
  return sonuc;
}

// Metindeki web adreslerini tıklanabilir bağlantıya çevirir
export function baglantiliMetin(metin) {
  return String(metin).split(/(https?:\/\/[^\s|]+)/g)
    .map((parca, i) => (i % 2 ? h('a', { href: parca, target: '_blank', rel: 'noopener' }, parca) : parca));
}

// Görev metnindeki "K3" gibi kanıt numaralarını, o kanıt kartına götüren düğmelere çevirir
export function kanitBaglantili(metin, kanitIdleri) {
  return String(metin).split(/\b(K\d+)\b/g).map((parca, i) => {
    if (i % 2 === 0 || !kanitIdleri.has(parca)) return parca;
    return h('button', { type: 'button', class: 'kanit-baglantisi', onclick: () => kanidaGit(parca) }, parca);
  });
}

function kanidaGit(id) {
  const kart = document.getElementById(`kanit-${id}`);
  if (!kart) return;
  const panel = kart.closest('details');
  if (panel) panel.open = true;
  kart.scrollIntoView({ behavior: 'smooth', block: 'center' });
  kart.classList.remove('vurgulu');
  void kart.offsetWidth;
  kart.classList.add('vurgulu');
}

export function veriTablosu(tablo) {
  return h('div', { class: 'tablo-kutusu', tabindex: '0', role: 'region', 'aria-label': 'Veri tablosu' },
    h('table', { class: 'veri-tablosu' },
      h('thead', {}, h('tr', {}, tablo.basliklar.map(b => h('th', { scope: 'col' }, b)))),
      h('tbody', {}, tablo.satirlar.map(satir => h('tr', {},
        satir.map((hucre, i) => (i === 0 ? h('th', { scope: 'row' }, hucre) : h('td', {}, hucre))))))));
}

export function kanitKarti(kanit, yeni = false) {
  return h('article', { class: `kanit${yeni ? ' yeni' : ''}`, id: `kanit-${kanit.id}` },
    h('div', { class: 'kanit-ust' },
      h('span', { class: 'kanit-kod' }, kanit.id),
      h('span', { class: 'kanit-tur' }, kanit.turAdi),
      yeni ? h('span', { class: 'rozet yeni-rozet' }, 'Yeni') : null),
    h('h3', { class: 'kanit-baslik' }, kanit.baslik),
    kanit.tablo ? veriTablosu(kanit.tablo) : h('p', {}, kanit.metin),
    kanit.kaynak ? h('p', { class: 'kaynak' }, 'Kaynak: ', baglantiliMetin(kanit.kaynak)) : null);
}

export function kanitPaneli(kanitlar, yeniler, acik, degisince) {
  const panel = h('details', { class: 'kanit-paneli', open: acik },
    h('summary', {}, h('span', {}, 'Dosyadaki kanıtlar'), h('span', { class: 'sayi' }, String(kanitlar.length))),
    h('div', { class: 'kanitlar' }, kanitlar.map(k => kanitKarti(k, yeniler.has(k.id)))));
  panel.addEventListener('toggle', () => degisince?.(panel.open));
  return panel;
}

// Bilimsel yöntem ya da bilimsel argüman zinciri; görevin bulunduğu aşama vurgulanır
export function asamaCubugu(gorev) {
  const argumanda = Boolean(gorev.arguman);
  const zincir = argumanda ? ARGUMAN_ASAMALARI : ASAMALAR;
  const simdiki = zincir.findIndex(([kod]) => kod === (argumanda ? gorev.arguman : gorev.asama));
  return h('nav', { class: `asamalar${argumanda ? ' arguman' : ''}`, 'aria-label': argumanda ? 'Bilimsel argüman' : 'Bilimsel yöntem' },
    h('p', { class: 'asama-baslik' }, argumanda ? 'Bilimsel argüman' : 'Bilimsel yöntem'),
    h('ol', {}, zincir.map(([, ad], i) => h('li', {
      class: i === simdiki ? 'simdi' : argumanda && i < simdiki ? 'bitti' : null,
      'aria-current': i === simdiki ? 'step' : null,
    }, ad))));
}

// Dokunarak aday element seçilen periyodik tablo
export function periyodikSecici(secili, degisince) {
  const izgara = h('div', { class: 'pt-izgara', role: 'group', 'aria-label': 'Periyodik tablo: aday elementleri seç' });
  for (let grup = 1; grup <= 18; grup++) izgara.append(h('span', { class: 'pt-etiket', style: `grid-row:1;grid-column:${grup + 1}`, 'aria-hidden': 'true' }, String(grup)));
  for (let periyot = 1; periyot <= 7; periyot++) izgara.append(h('span', { class: 'pt-etiket', style: `grid-row:${periyot + 1};grid-column:1`, 'aria-hidden': 'true' }, String(periyot)));
  izgara.append(h('span', { class: 'pt-yer', style: 'grid-row:7;grid-column:4', 'aria-hidden': 'true' }, '57–71'));
  izgara.append(h('span', { class: 'pt-yer', style: 'grid-row:8;grid-column:4', 'aria-hidden': 'true' }, '89–103'));
  const dugmeler = ELEMENTLER.map(e => {
    const dugme = h('button', {
      type: 'button',
      class: `pt-hucre blok-${e.blok}${secili.has(e.sembol) ? ' secili' : ''}`,
      style: `grid-row:${e.satir + 1};grid-column:${e.sutun + 1}`,
      'aria-pressed': String(secili.has(e.sembol)),
      'aria-label': `${e.ad}, ${e.sembol}, atom numarası ${e.z}`,
    }, h('span', { class: 'pt-z' }, String(e.z)), h('span', { class: 'pt-sembol' }, e.sembol));
    dugme.addEventListener('click', () => {
      if (secili.has(e.sembol)) secili.delete(e.sembol); else secili.add(e.sembol);
      dugme.classList.toggle('secili', secili.has(e.sembol));
      dugme.setAttribute('aria-pressed', String(secili.has(e.sembol)));
      degisince?.();
    });
    return dugme;
  });
  izgara.append(...dugmeler);
  return {
    dugum: h('div', { class: 'pt-kutusu' }, izgara),
    kilitle: () => dugmeler.forEach(d => { d.disabled = true; }),
  };
}
