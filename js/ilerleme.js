// Oyuncunun ilerlemesi (açılan bölümler, en iyi puanlar) yalnızca bu cihazdaki tarayıcıda saklanır.
// Kişisel bilgi tutulmaz. Tarayıcı depolamayı engellerse oyun yine çalışır, sadece ilerleme hatırlanmaz.

const ANAHTAR = 'element-oyunu-ilerleme';

const bosIlerleme = () => ({ acikBolum: 1, enIyi: {}, tamamlanan: {}, ogretmenModu: false });

export function ilerlemeOku() {
  try {
    const kayit = JSON.parse(localStorage.getItem(ANAHTAR));
    if (kayit && typeof kayit === 'object') return { ...bosIlerleme(), ...kayit };
  } catch { /* depolama kapalı ya da kayıt bozuk */ }
  return bosIlerleme();
}

export function ilerlemeYaz(ilerleme) {
  try { localStorage.setItem(ANAHTAR, JSON.stringify(ilerleme)); } catch { /* depolama kapalı */ }
}

export function ilerlemeSifirla() {
  try { localStorage.removeItem(ANAHTAR); } catch { /* depolama kapalı */ }
  return bosIlerleme();
}
