// 118 elementin sembolü, Türkçe adı ve periyodik tablodaki yeri.
// Periyot, grup ve blok bilgisi atom numarasından hesaplanır. Lantanitler (57–71) ve
// aktinitler (89–103) f bloğu olarak tablonun altındaki iki ayrı satırda gösterilir.

const SEMBOLLER = (
  'H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr ' +
  'Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb ' +
  'Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr ' +
  'Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og'
).split(' ');

const ADLAR = (
  'Hidrojen Helyum Lityum Berilyum Bor Karbon Azot Oksijen Flor Neon Sodyum Magnezyum Alüminyum Silisyum ' +
  'Fosfor Kükürt Klor Argon Potasyum Kalsiyum Skandiyum Titanyum Vanadyum Krom Mangan Demir Kobalt Nikel ' +
  'Bakır Çinko Galyum Germanyum Arsenik Selenyum Brom Kripton Rubidyum Stronsiyum İtriyum Zirkonyum ' +
  'Niyobyum Molibden Teknesyum Rutenyum Rodyum Paladyum Gümüş Kadmiyum İndiyum Kalay Antimon Tellür İyot ' +
  'Ksenon Sezyum Baryum Lantan Seryum Praseodim Neodim Prometyum Samaryum Evropiyum Gadolinyum Terbiyum ' +
  'Disprosiyum Holmiyum Erbiyum Tulyum İterbiyum Lutesyum Hafniyum Tantal Tungsten Renyum Osmiyum İridyum ' +
  'Platin Altın Cıva Talyum Kurşun Bizmut Polonyum Astatin Radon Fransiyum Radyum Aktinyum Toryum ' +
  'Protaktinyum Uranyum Neptünyum Plütonyum Amerikyum Küriyum Berkelyum Kaliforniyum Aynştaynyum Fermiyum ' +
  'Mendelevyum Nobelyum Lavrensiyum Rutherfordiyum Dubniyum Seaborgiyum Bohriyum Hassiyum Meitneriyum ' +
  'Darmstadtiyum Röntgenyum Kopernikyum Nihonyum Flerovyum Moskovyum Livermoryum Tennesin Oganesson'
).split(' ');

// Yazılı cevaplarda kabul edilen başka adlar
const DIGER_ADLAR = { N: ['Nitrojen'], W: ['Volfram', 'Wolfram'], I: ['İyod'] };

const PERIYOT_BASLARI = [1, 3, 11, 19, 37, 55, 87];

function konumBul(z) {
  let periyot = 7;
  while (PERIYOT_BASLARI[periyot - 1] > z) periyot--;
  const sira = z - PERIYOT_BASLARI[periyot - 1];   // periyot içindeki sıra (0'dan başlar)
  let grup;
  if (periyot === 1) grup = z === 1 ? 1 : 18;
  else if (periyot <= 3) grup = sira < 2 ? sira + 1 : sira + 11;
  else if (periyot <= 5) grup = sira + 1;
  else if (sira < 2) grup = sira + 1;
  else if (sira < 17) grup = null;                 // lantanit ya da aktinit
  else grup = sira - 13;

  let blok;
  if (grup === null) blok = 'f';
  else if (grup <= 2 || z === 2) blok = 's';
  else if (grup >= 13) blok = 'p';
  else blok = 'd';

  // Ekrandaki tablo yerleşimi: f bloğu 9. ve 10. satırlara alınır
  const satir = grup === null ? periyot + 3 : periyot;
  const sutun = grup === null ? sira + 1 : grup;
  return { periyot, grup, blok, satir, sutun };
}

export const ELEMENTLER = SEMBOLLER.map((sembol, i) => ({ z: i + 1, sembol, ad: ADLAR[i], ...konumBul(i + 1) }));

const sembolHaritasi = new Map(ELEMENTLER.map(e => [e.sembol, e]));

// Cevap karşılaştırmak için metni sadeleştirir: "Bakır" -> "bakir", "  Cu " -> "cu"
export function sadelestir(metin) {
  const harfler = { ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u', â: 'a', î: 'i', û: 'u' };
  return String(metin ?? '').toLocaleLowerCase('tr-TR')
    .replace(/[çğıöşüâîû]/g, h => harfler[h])
    .replace(/[^a-z0-9]/g, '');
}

const aramaHaritasi = new Map();
for (const e of ELEMENTLER) {
  for (const anahtar of [e.sembol, e.ad, ...(DIGER_ADLAR[e.sembol] ?? [])]) aramaHaritasi.set(sadelestir(anahtar), e);
}

// Sembolü ya da adı yazılan elementi bulur (büyük-küçük harf ve Türkçe karakter farkını önemsemez)
export function elementBul(metin) {
  return aramaHaritasi.get(sadelestir(metin)) ?? null;
}

export function sembolle(sembol) {
  return sembolHaritasi.get(String(sembol ?? '').trim()) ?? null;
}
