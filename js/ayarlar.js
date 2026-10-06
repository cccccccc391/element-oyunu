// Oyunun kuralları, puanlama ağırlıkları ve sabit yazıları.
// Puanları, can sayısını ya da yazıları değiştirmek için yalnızca bu dosyayı düzenlemek yeterli.

export const AYARLAR = {
  oyunAdi: 'Element Dosyaları',
  altBaslik: 'Atomun Peşinde',
  birimAdi: 'Element Araştırma Birimi',
  canSayisi: 3,                 // Bu kadar bilimsel hatada dosya kilitlenir
  ipucuKatsayisi: 0.5,          // İpucu alınan görevden alınabilecek puan oranı
  savunmaEnAzKarakter: 80,      // Savunma metninin en kısa uzunluğu
  seviyeAcmaEsigi: 5,           // Bir seviye, önceki seviyeden bu kadar dosya çözülünce açılır
  ogretmenSifresi: '2204',      // Öğretmen panelinin şifresi (öğrencilerle paylaşmayın)
};

export const HIKAYE = [
  'Element Araştırma Birimi\'ne hoş geldin. Bugünden itibaren bir bilim dedektifisin.',
  'Masanda günlük hayattaki nesnelerden gelen dosyalar var. Hiçbir dosyada elementin adı yazmıyor. Elinde yalnızca kanıtlar var: ölçümler, gözlemler, periyodik tablodaki konum, deney sonuçları ve tarihsel kayıtlar.',
  'Görevin, kanıtları inceleyip elementin kimliğini ortaya çıkarmak ve bu sonuca nasıl ulaştığını savunmak. Her dosyada sana sorulacak asıl soru "Bu element hangisi?" değil, "Bunu nereden biliyorsun?" olacak.',
  'Birimin tek bir kuralı var: Bilim insanı cevabı tahmin etmez; kanıtlar.',
];

export const HAKKINDA = [
  'Bu oyun bir TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projesi kapsamında hazırlanmaktadır.',
  'Oyunun yazılım altyapısı ve 200 vaka dosyasının içeriği (hikâyeler, kanıtlar, veri tabloları, görevler ve açıklamalar) üretken yapay zekâ aracı Claude (Anthropic) ile hazırlanmıştır. Oyunun tasarım ilkeleri, danışman öğretmenin üretken yapay zekâ yardımıyla hazırladığı bir tasarım metnine dayanır.',
  'Vakalar, doğada bulunan ve kullanılan 100 elementi (atom numarası 1–100) kapsar. Sayısal veriler ve isim kökenleri başta Royal Society of Chemistry olmak üzere güvenilir kaynaklardan alınmıştır. Gerçek olaylara dayanan vakaların kaynakları ayrıca gösterilmiştir. Kaynaklar "Bilimsel kaynakça" sayfasında, her dosya için ayrı ayrı listelenir.',
  'Bazı vakalar gerçek olaylara dayanır. Diğer vakaların hikâyeleri ve bütün vakalardaki laboratuvar ölçüm sonuçları kurgudur; bilinen değerlerle uyumlu olacak biçimde hazırlanmıştır.',
  'Oyun kişisel bilgi toplamaz. Cevaplar ve puanlar yalnızca bu cihazda, öğretmenin verdiği bir katılımcı koduyla saklanır.',
];

export const SEVIYELER = {
  1: { ad: 'Gözlem', aciklama: 'Temel özelliklerden element tanımlama.' },
  2: { ad: 'Çıkarım', aciklama: 'Birden fazla veriyi birleştirerek element tanımlama.' },
  3: { ad: 'Kanıt', aciklama: 'Rakip hipotezleri karşılaştırma ve kanıtın yeterliliğini değerlendirme.' },
  4: { ad: 'Bilimsel Savunma', aciklama: 'Hazır seçenekler olmadan, veriye dayalı argüman kurma ve savunma.' },
};

// Vaka temaları (dosyalar tablosunun "tema" sütunu). Panodaki filtre düğmelerinde görünür.
export const TEMALAR = {
  saglik: { ad: 'Sağlık', simge: '🩺' },
  teknoloji: { ad: 'Teknoloji', simge: '📱' },
  enerji: { ad: 'Enerji', simge: '⚡' },
  ev: { ad: 'Ev ve günlük hayat', simge: '🏠' },
  sanayi: { ad: 'Sanayi ve ulaşım', simge: '🏭' },
  uzay: { ad: 'Uzay', simge: '🚀' },
  cevre: { ad: 'Doğa ve çevre', simge: '🌿' },
  tarih: { ad: 'Bilim tarihi', simge: '📜' },
  sanat: { ad: 'Sanat, kültür ve spor', simge: '🎨' },
  adli: { ad: 'Adli bilim ve güvenlik', simge: '🔍' },
};

// Bilimsel yöntem zinciri ve bilimsel argüman zinciri (görevlerin "asama" ve "arguman" sütunları)
export const ASAMALAR = [
  ['gozlem', 'Gözlem'], ['veri', 'Veri'], ['hipotez', 'Hipotez'],
  ['kanit', 'Kanıt'], ['cikarim', 'Çıkarım'], ['sonuc', 'Sonuç'],
];
export const ARGUMAN_ASAMALARI = [
  ['iddia', 'İddia'], ['kanit', 'Kanıt'], ['gerekce', 'Gerekçe'],
  ['karsi_kanit', 'Karşı kanıt'], ['sonuc', 'Sonuç'],
];

// 100 puanlık dosya puanının dağılımı. Bir dosyada hangi kategorilerden görev varsa
// puan o kategoriler arasında bu oranlarla paylaştırılır.
export const KATEGORILER = {
  kimlik: { ad: 'Doğru element', agirlik: 20, grup: 'bilgi' },
  sembol: { ad: 'Doğru sembol', agirlik: 10, grup: 'bilgi' },
  isim: { ad: 'İsim kökeni', agirlik: 10, grup: 'bilgi' },
  kullanim: { ad: 'Günlük kullanım', agirlik: 15, grup: 'bilgi' },
  ozellik_kullanim: { ad: 'Özellik–kullanım ilişkisi', agirlik: 15, grup: 'akil' },
  kanit: { ad: 'Kanıt kullanımı', agirlik: 15, grup: 'akil' },
  alternatif: { ad: 'Alternatif hipotezler', agirlik: 5, grup: 'akil' },
  gerekce: { ad: 'Bilimsel gerekçelendirme', agirlik: 10, grup: 'akil' },
};
export const PUAN_GRUPLARI = {
  bilgi: 'Bilgi puanı',
  akil: 'Bilimsel akıl yürütme puanı',
};

// Araştırmada ölçülen beceriler (görevlerin "beceri" sütunu)
export const BECERILER = {
  gozlem: 'Gözlem yapma',
  veri: 'Veri yorumlama',
  hipotez: 'Hipotez oluşturma',
  kanit: 'Kanıt kullanma',
  cikarim: 'Bilimsel çıkarım',
  gerekce: 'Gerekçeli karar verme',
};

// Becerilerin Türkiye Yüzyılı Maarif Modeli (2024 Kimya Dersi Öğretim Programı) karşılıkları.
// Öğretmen panelindeki beceri tablosunda gösterilir.
export const BECERI_TYMM = {
  gozlem: 'FBAB1 Bilimsel Gözlem',
  veri: 'OB7 Veri Okuryazarlığı, KB2.14 Yorumlama',
  hipotez: 'FBAB6 Hipotez Oluşturma',
  kanit: 'FBAB12 Kanıt Kullanma',
  cikarim: 'FBAB8 Bilimsel Çıkarım Yapma, FBAB10 Tümevarımsal Akıl Yürütme',
  gerekce: 'FBAB13 Bilimsel Sorgulama, E3.10 Eleştirel Bakma',
};

// Yanlış cevapların türleri (seçeneklerin ve görevlerin "hata_turu" sütunu).
// Bilimsel hata analizinde öğrenciye hatanın türü "aciklama" ile anlatılır ve
// "Bu hatayı nasıl önlersin?" sorusunun doğru cevabı olarak "yaklasim" sorulur.
export const HATA_TURLERI = {
  kanitsiz: {
    ad: 'Kanıta dayanmayan çıkarım',
    aciklama: 'Kanıt yetmediği hâlde kesin bir sonuca atladın.',
    yaklasim: 'Karar vermeden önce kanıtın diğer adayları da eleyip elemediğine bakmak.',
  },
  veri: {
    ad: 'Veriyi yanlış yorumlama',
    aciklama: 'Bir ölçümü, tabloyu ya da gözlemi yanlış okudun ya da bir veriyi gözden kaçırdın.',
    yaklasim: 'Tabloyu ve ölçümleri satır satır, dikkatle yeniden okumak.',
  },
  birim: {
    ad: 'Birim / ölçüm hatası',
    aciklama: 'Birimleri karıştırdın ya da ölçümdeki ± payını hesaba katmadın.',
    yaklasim: 'Birimlere ve ölçümün ± payına (hangi değerlerin aralığa girdiğine) bakmak.',
  },
  iliski: {
    ad: 'Kimyasal özelliği yanlış ilişkilendirme',
    aciklama: 'Bir özelliği, onunla gerçekte ilgisi olmayan bir kullanıma ya da sonuca bağladın.',
    yaklasim: 'Özellik ile kullanım arasında gerçek bir neden-sonuç bağı olup olmadığını sormak.',
  },
};

// Kanıt türleri (kanıtlar tablosunun "tur" sütunu) ve ekranda görünen adları
export const KANIT_TURLERI = {
  atom_numarasi: 'Atom numarası',
  sembol: 'Sembol',
  konum: 'Periyodik tablodaki konum',
  elektron_dizilimi: 'Elektron dizilimi',
  fiziksel: 'Fiziksel özellik',
  kimyasal: 'Kimyasal özellik',
  iyon: 'İyon oluşturma',
  iletkenlik: 'İletkenlik',
  yogunluk: 'Yoğunluk',
  erime_kaynama: 'Erime / kaynama noktası',
  yukseltgenme: 'Yükseltgenme basamakları',
  reaktivite: 'Reaktiflik',
  alasim: 'Alaşım',
  kullanim: 'Günlük kullanım',
  isim: 'İsim kökeni',
  tarih: 'Tarihsel kayıt',
  deney: 'Deney gözlemi',
  tablo: 'Veri tablosu',
};

export const GOREV_TURLERI = ['tekli', 'coklu', 'sirala', 'tablo', 'kanit', 'yaz', 'savunma'];
