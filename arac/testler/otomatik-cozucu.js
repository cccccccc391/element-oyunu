// Tarayıcıda çalışan otomatik çözücü (yalnızca yerel test için; yayına girmez).
// Her vakayı arayüzden açar, her görevi içerik tablolarındaki doğru cevapla çözer ve sonucu denetler.
window.otomatikCoz = async function otomatikCoz(seviye, baslangic = 0, adet = 999) {
  const { icerikYukle } = await import('/js/icerik.js');
  const icerik = await icerikYukle();
  const bekle = ms => new Promise(r => setTimeout(r, ms));
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const metniOlanDugme = (secici, metin) => $$(secici).find(b => b.textContent.trim().includes(metin));
  const sorunlar = [];
  const dosyalar = icerik.dosyalar.filter(d => d.seviye === seviye).slice(baslangic, baslangic + adet);

  for (const dosya of dosyalar) {
    try {
      // Panoya dön, seviye sekmesini seç, kartı aç
      const pano = metniOlanDugme('button', 'Dosya panosu');
      if (pano) { pano.click(); await bekle(20); }
      const sekme = $$('.sekme')[seviye - 1];
      if (sekme && !sekme.classList.contains('secili')) { sekme.click(); await bekle(20); }
      const tumu = metniOlanDugme('.cip', 'Bütün temalar'); if (tumu && !tumu.classList.contains('secili')) { tumu.click(); await bekle(10); }
      const hepsi = metniOlanDugme('.cip', 'Hepsi'); if (hepsi && !hepsi.classList.contains('secili')) { hepsi.click(); await bekle(10); }
      const kart = $$('button.dosya-karti').find(b => b.querySelector('.dosya-sekme')?.textContent === dosya.id);
      if (!kart) throw new Error('kart bulunamadı');
      kart.click(); await bekle(20);
      const basla = metniOlanDugme('button', 'Soruşturmayı başlat') || metniOlanDugme('button', 'Jürinin karşısına çık');
      if (!basla) throw new Error('başlat düğmesi yok');
      basla.click(); await bekle(20);

      for (const gorev of dosya.gorevler) {
        const soru = $('.gorev-sorusu')?.textContent ?? '';
        if (!soru.includes(gorev.soru.slice(0, 25).replace(/K\d+/g, '').trim().slice(0, 10))) {
          // soru metnindeki kanıt düğmeleri metni bölebilir; yalnızca uyarı olarak kaydet
        }
        if (gorev.tur === 'savunma') {
          const kutu = $('.savunma-kutusu');
          kutu.value = 'İddia: Element bu vakadaki elementtir. Kanıt: K3 ve ölçüm. Gerekçe: özellik kullanımla uyumlu. Karşı kanıt: rakip aday ölçümle uyuşmuyor.';
          kutu.dispatchEvent(new Event('input', { bubbles: true }));
          metniOlanDugme('button', 'Savunmamı sun').click(); await bekle(10);
          metniOlanDugme('button', 'Değerlendirmemi kaydet').click(); await bekle(20);
          continue;
        }
        if (gorev.tur === 'tekli') {
          const dogru = gorev.secenekler.find(s => s.dogru);
          const d = $$('.secenek').find(b => b.querySelector('.secenek-metin')?.textContent === dogru.metin);
          if (!d) throw new Error(`${gorev.id}: doğru seçenek düğmesi yok`);
          d.click();
        } else if (gorev.tur === 'coklu') {
          for (const s of gorev.secenekler.filter(x => x.dogru)) $$('.secenek').find(b => b.querySelector('.secenek-metin')?.textContent === s.metin).click();
        } else if (gorev.tur === 'kanit') {
          for (const id of gorev.gerekli) {
            const d = $$('.secenek').find(b => b.querySelector('.secenek-metin')?.textContent.startsWith(`${id} · `));
            if (!d) throw new Error(`${gorev.id}: ${id} kanıt düğmesi yok (açılmamış olabilir)`);
            d.click();
          }
        } else if (gorev.tur === 'sirala') {
          for (const s of [...gorev.secenekler].sort((a, b) => a.sira - b.sira)) {
            $$('.siralama .secenek').find(b => b.querySelector('.secenek-metin')?.textContent === s.metin).click();
            await bekle(5);
          }
        } else if (gorev.tur === 'tablo') {
          for (const sembol of gorev.dogruSemboller) {
            const d = $$('.pt-hucre').find(b => b.getAttribute('aria-label').includes(`, ${sembol}, `));
            d.click();
          }
        } else if (gorev.tur === 'yaz') {
          const girdi = $('.yazi-girdisi');
          girdi.value = gorev.kabul[0];
          girdi.dispatchEvent(new Event('input', { bubbles: true }));
        }
        await bekle(5);
        const gonder = $('form.gorev-karti button[type=submit]');
        if (!gonder || gonder.disabled) throw new Error(`${gorev.id}: Gönder düğmesi kapalı`);
        gonder.click(); await bekle(15);
        const iyi = $('.geri-bildirim.iyi');
        if (!iyi) throw new Error(`${gorev.id} (${gorev.tur}): doğru cevap kabul edilmedi: ${$('.geri-bildirim')?.textContent.slice(0, 120)}`);
        const ileri = $$('.geri-bildirim-alani button.buton.genis').pop();
        ileri.click(); await bekle(15);
      }
      const puan = $('.buyuk-puan span')?.textContent;
      const damga = $('.damga')?.textContent;
      if (damga !== 'Dosya çözüldü') throw new Error(`sonuç ekranı yok: ${damga}`);
      if (puan !== '100') sorunlar.push(`${dosya.id}: puan ${puan}`);
    } catch (hata) {
      sorunlar.push(`${dosya.id} ${dosya.cevap?.sembol}: ${hata.message}`);
      const cik = $('.cik'); if (cik) { window.confirm = () => true; cik.click(); await bekle(20); }
    }
  }
  return { seviye, denenen: dosyalar.length, sorunlar };
};
