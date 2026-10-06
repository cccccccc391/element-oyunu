# Element Dosyaları: Atomun Peşinde

BİLSEM lise öğrencileri için bilimsel akıl yürütme oyunu (TÜBİTAK 2204-A projesi). Oyuncu, Element Araştırma Birimi'ne yeni katılmış bir bilim dedektifidir. Dosyalarda elementin adı yazmaz; öğrenci ölçümlerden, gözlemlerden, veri tablolarından, periyodik tablodaki konumdan ve tarihsel kayıtlardan elementin kimliğini çıkarır ve buna nasıl ulaştığını savunur.

Oyunun asıl sorusu "Bu element hangisi?" değil, **"Bunu nereden biliyorsun?"** sorusudur. Bilim insanı cevabı tahmin etmez; kanıtlar.

Oyun telefonda uygulama gibi çalışan bir web oyunudur. Android'de de iPhone'da da bir bağlantıyla açılır ve bir kez açıldıktan sonra internet olmadan da oynanabilir.

## Oyunun yapısı

- **200 vaka, 4 seviye, 100 element:** Her seviyede 50 vaka var: Gözlem (V001–V050), Çıkarım (V051–V100), Kanıt (V101–V150), Bilimsel Savunma (V151–V200). Vakalar doğada bulunan ve kullanılan 100 elementi kapsar: atom numarası 1–100. Bunlar doğada bulunan elementlerin hepsi ve kullanım alanı olan ilk yapay elementlerdir. Çok kullanılan elementlerin birden fazla vakası var (hidrojen, karbon ve demir gibi elementlerde 4–5 vaka), nadir elementlerin birer vakası. V001 bütün görev türlerini gösteren tanıtım dosyası, V200 final dosyasıdır (Bilimsel Jüri). Cevap anahtarı `VAKALAR.md` dosyasındadır.
- **Pano:** Seviye sekmeleri, 10 tema (sağlık, teknoloji, enerji, ev ve günlük hayat, sanayi ve ulaşım, uzay, doğa ve çevre, bilim tarihi, sanat-kültür-spor, adli bilim ve güvenlik) ve "çözülmeyenler / çözülenler" süzgeci var. Seviye 1 baştan açıktır. Bir sonraki seviye, önceki seviyeden 5 dosya çözülünce açılır (`js/ayarlar.js` içindeki `seviyeAcmaEsigi`). Bir seviyedeki dosyalar istenen sırayla çözülebilir.
- **Keşif tablosu:** Bir elementin en az bir vakası çözülünce o element periyodik tabloda yanar. Öğrenci bir elemente dokununca o elementin kaç vakası olduğunu ve çözdüğü vakaları görür.
- **Raporum:** Çözülen dosya sayısı, puan ortalaması, keşfedilen element sayısı ve bilimsel beceri profili.
- **Vaka:** Bir giriş hikâyesi, kanıt kartları ve görevlerden oluşur. Bazı kanıtlar ancak doğru adım atılınca açılır. Görevler bilimsel yöntem zincirini izler: **gözlem → veri → hipotez → kanıt → çıkarım → sonuç**. Kanıt seçimi ve savunma görevlerinde **iddia → kanıt → gerekçe → karşı kanıt → sonuç** zinciri gösterilir. Yeni vakalarda 4–5 görev var.
- **Seviyeler neyi ölçer:**
  - *Gözlem:* Element periyodik tablodaki yerinden ya da atom numarasından bulunur. Görevler gözlemi yorumlama, özellik–kullanım ilişkisi, isim kökeni ya da elementin sınıfıdır (metal, ametal, yarı metal, soy gaz).
  - *Çıkarım:* Elementin yeri hesaplanarak bulunur: elektron diziliminden (ilk 36 element), izotopun kütle ve nötron sayısından ya da iyonun elektron sayısından. Sonuç bir laboratuvar ölçümüyle doğrulanır, ardından elementi gösteren kanıtlar seçilir.
  - *Kanıt:* Önce gruptaki adaylar işaretlenir, sonra ölçüm ve veri tablosuyla aday seçilir. Ardından bir stajyerin yanlış iddiasını hangi kanıtın çürüttüğü bulunur.
  - *Bilimsel Savunma:* Element seçenek olmadan yazılır. Kanıtlar seçilir ve jüriye yazılı bir savunma yapılır.
- **3 bilimsel hata hakkı:** Her yanlış cevap türüyle birlikte gösterilir: kanıta dayanmayan çıkarım, veriyi yanlış yorumlama, birim / ölçüm hatası, kimyasal özelliği yanlış ilişkilendirme. Doğru cevap söylenmez; yalnızca hatanın neden hata olduğu açıklanır.
- **Dosya kilitlenir:** Üç hatada dosya kilitlenir. Dosyayı yeniden açmak için **bilimsel hata analizi** yapılır. Hatalar tek tek gösterilir: soru, öğrencinin cevabı, cevabın neden yanlış olduğu, ilgili kanıt kartı, ipucu ve hata türünün kısa açıklaması. Öğrenci her hata için tek bir soruyu cevaplar: "Bu hatayı bir dahaki sefere nasıl önlersin?" Üç kısa seçenek vardır; yanlış seçimin cezası yoktur, öğrenci açıklamayı yeniden okuyup tekrar dener. Bütün hatalar incelenince dosya yeniden açılır.
- **İpucu:** Görevlerde ipucu alınabilir. İpucu alınan görevden puanın yarısı alınır.
- **Puanlama (100 puan):** Doğru element 20, doğru sembol 10, isim kökeni 10, günlük kullanım 15, özellik–kullanım ilişkisi 15, kanıt kullanımı 15, alternatif hipotezler 5, bilimsel gerekçelendirme 10. Sonuç ekranında "bilgi puanı" ile "bilimsel akıl yürütme puanı" ayrı gösterilir. Bir görevin puanı ilk denemede doğru çözülürse alınır. Dosyada hangi kategoriden görev yoksa onun payı diğerlerine dağıtılır. Savunma metni otomatik puanlanmaz; öğretmen değerlendirir.

### Görev türleri

| Tür | Öğrenci ne yapar | Örnek |
|---|---|---|
| `tekli` | Tek doğru seçeneği seçer | "Yalnızca yoğunlukla kesin sonuca ulaşılabilir mi?" |
| `coklu` | Doğru seçeneklerin hepsini seçer | "Mıknatıs testi hangi adayları eler?" |
| `sirala` | Öğeleri sıraya dizer | "İletkenliğe göre büyükten küçüğe sırala" |
| `tablo` | Periyodik tabloda aday elementleri işaretler | "4. periyot, d bloğundaki adayları işaretle" |
| `kanit` | Dosyadaki kanıt kartlarından iddiayı destekleyenleri seçer | "Adayları eleyen kanıtları seç" |
| `yaz` | Cevabı yazar; seçenek yoktur | "Element hangisi? Adını ya da sembolünü yaz" |
| `savunma` | Jüriye argümanını yazar, örnek savunmayla karşılaştırıp kendini değerlendirir | "Elementin … olduğunu düşünüyorum çünkü…" |

Son seviyede hazır seçenekleri azaltmak için `yaz`, `kanit` ve `savunma` türleri kullanılmalıdır.

## Klasördekiler

| Dosya | Görevi |
|---|---|
| `index.html`, `css/stil.css` | Açılış sayfası ve görünüm |
| `js/ayarlar.js` | Kurallar, puan ağırlıkları, hikâye, hata türleri, öğretmen şifresi: **oyunu buradan ayarlayın** |
| `js/oyun.js` | Ekranlar ve oyunun akışı |
| `js/arayuz.js` | Kanıt kartı, veri tablosu, periyodik tablo seçici gibi ekran parçaları |
| `js/icerik.js` | İçerik tablolarını okuma, birbirine bağlama ve hata kontrolü |
| `js/puan.js` | Puanlama ve beceri özetleri |
| `js/kayit.js` | İlerleme ve araştırma kayıtları, CSV dışa aktarma |
| `js/periyodik.js` | 118 elementin sembolü, Türkçe adı ve periyodik tablodaki yeri |
| `js/csv.js` | CSV okuyucu (Excel ve Google E-Tablolar biçimleri) |
| `icerik/*.csv` | 200 vakanın içeriği (dosyalar, kanıtlar, veri tabloları, görevler, seçenekler) |
| `VAKALAR.md` | Öğretmen için vaka listesi ve cevap anahtarı |
| `MAARIF_MODELI_UYUMU.md` | Oyunun Türkiye Yüzyılı Maarif Modeli 9. sınıf kimya programıyla ilişkisi |
| `arac/` | İçerik tablolarını üreten program ve testler (oyunun çalışması için gerekmez) |
| `manifest.webmanifest`, `sw.js`, `img/` | Ana ekrana ekleme, çevrim dışı çalışma, ikonlar |

## Çalıştırma

**Telefonda:** Oyun GitHub Pages'te yayımlanır. Depodaki dosyalar güncellenince oyun 1–2 dakika içinde kendiliğinden güncellenir. Telefonda tarayıcı menüsündeki "Ana ekrana ekle" ile uygulama gibi açılır.

**Bilgisayarda:** `index.html` dosyasına çift tıklayınca oyun açılmaz, çünkü tarayıcı içerik tablolarını bu şekilde okumaz. Bilgisayarda Python varsa bu klasörde şu komutu çalıştırıp tarayıcıda `http://localhost:8000` adresini açın:

```bash
python -m http.server 8000
```

## Dosya eklemek ya da değiştirmek

Bir dosyanın içeriği beş tabloya dağılır. Tablolar birbirine `dosya` ve `id` sütunlarıyla bağlanır. Var olan 200 vaka düzenlenebilir ya da yenileri eklenebilir; yeni bir dosya hazırlarken var olanların satırlarını örnek alın. `V001` bütün görev türlerini gösteren tanıtım dosyasıdır.

Tablolar `arac/vaka-uretici` klasöründeki programla üretildi (ayrıntılar `arac/README.md` dosyasında). Tabloları elle düzenlerseniz üreticiyi yeniden çalıştırmayın.

Tablolar Türkçe Excel'de çift tıklayınca doğru açılır. Kaydederken "CSV (noktalı virgülle ayrılmış)" ya da "CSV UTF-8" seçin, ikisi de çalışır. Google E-Tablolar'da **Dosya → İçe aktar** ile açıp **Dosya → İndir → .csv** ile indirebilirsiniz. **İlk satırdaki sütun adlarını değiştirmeyin.** Her kayıttan sonra **Öğretmen paneli**ni açın. Tablolardaki hatalar orada dosya adı ve satır numarasıyla listelenir. Hatalı bir görev atlanır, dosyanın geri kalanı çalışmaya devam eder.

### 1. `dosyalar.csv`: her satır bir dosya

| Sütun | Ne yazılır |
|---|---|
| `id` | Dosya kodu (V001…V200). Değiştirmeyin; öğrencilerin ilerlemesi bu koda bağlıdır. |
| `seviye`, `sira` | Seviye (1–4) ve panodaki sıra |
| `tema` | Panodaki tema süzgeci için: `saglik`, `teknoloji`, `enerji`, `ev`, `sanayi`, `uzay`, `cevre`, `tarih`, `sanat`, `adli` |
| `baslik` | Dosyanın adı ("Gizemli Metal"). **Boş bırakılan dosya "hazırlanıyor" görünür.** |
| `giris` | Dosyanın hikâyesi: hangi nesne, nereden geldi, görev ne? |
| `cevap` | Elementin sembolü (Cu) |
| `final` | Final (bilimsel jüri) dosyasıysa `evet` |
| `ornek` | Tanıtım dosyasıysa `evet` (panoda "Tanıtım" etiketi ve kısa bir not gösterilir) |
| `kaynakca` | Kaynaklar; birden fazlaysa aralarına `\|` koyun |

### 2. `kanitlar.csv`: dosyadaki kanıt kartları

| Sütun | Ne yazılır |
|---|---|
| `dosya`, `id` | Dosya kodu ve kanıt kodu (K1, K2…) |
| `tur` | `atom_numarasi`, `sembol`, `konum`, `elektron_dizilimi`, `fiziksel`, `kimyasal`, `iyon`, `iletkenlik`, `yogunluk`, `erime_kaynama`, `yukseltgenme`, `reaktivite`, `alasim`, `kullanim`, `isim`, `tarih`, `deney`, `tablo` |
| `baslik`, `metin` | Kartın başlığı ve içeriği. `tablo` türünde `metin` sütununa tablonun kodu (T1) yazılır. |
| `goster` | Boşsa kanıt baştan görünür. Bir görev kodu yazılırsa (G4) kanıt o görev çözülünce açılır. Bir görevde istenen ya da bir hata açıklamasında gösterilen kanıt o görevden önce açılmış olmalı; değilse öğretmen paneli uyarır. |
| `kaynak` | Bilginin kaynağı |

### 3. `tablolar.csv`: veri tabloları

Her satır tablonun bir satırıdır (`h1`–`h6` en fazla altı sütun). Aynı tablonun ilk satırı başlık satırıdır. Tablo, `kanitlar.csv`'de `tur` sütunu `tablo` olan bir kanıtla dosyaya eklenir.

### 4. `gorevler.csv`: görevler (dosyadaki sırasıyla sorulur)

| Sütun | Ne yazılır |
|---|---|
| `dosya`, `id` | Dosya kodu ve görev kodu (G1, G2…) |
| `asama` | Bilimsel yöntem aşaması: `Gözlem`, `Veri`, `Hipotez`, `Kanıt`, `Çıkarım`, `Sonuç` |
| `arguman` | Argüman bölümündeki görevler için: `İddia`, `Kanıt`, `Gerekçe`, `Karşı kanıt`, `Sonuç`. Dolu olunca ekranda argüman aşamaları gösterilir. |
| `tur` | `tekli`, `coklu`, `sirala`, `tablo`, `kanit`, `yaz`, `savunma` |
| `kategori` | Puan kategorisi: `kimlik`, `sembol`, `isim`, `kullanim`, `ozellik_kullanim`, `kanit`, `alternatif`, `gerekce` |
| `beceri` | Araştırmada ölçülen beceri: `gozlem`, `veri`, `hipotez`, `kanit`, `cikarim`, `gerekce` |
| `soru` | Görev metni. Metinde geçen K3 gibi kanıt kodları ekranda o kanıta götüren düğmelere dönüşür. |
| `ipucu` | İsteğe bağlı ipucu |
| `aciklama` | Doğru cevaptan sonra gösterilen bilimsel açıklama. `savunma` türünde jürinin örnek savunmasıdır. |
| `dogru` | `tablo`: işaretlenecek semboller (`Sc Ti V`). `kanit`: seçilmesi gereken kanıtlar; parantez içindekiler seçilse de olur (`K1 K4 K8 (K7)`). `yaz`: kabul edilen cevaplar `\|` ile (boşsa `kimlik` ve `sembol` görevlerinde dosyanın cevabı kullanılır). |
| `hata_turu` | Seçeneksiz görevlerde yanlış cevabın hata türü: `kanitsiz`, `veri`, `birim`, `iliski` |

### 5. `secenekler.csv`: `tekli`, `coklu` ve `sirala` görevlerinin seçenekleri

| Sütun | Ne yazılır |
|---|---|
| `dosya`, `gorev` | Dosya ve görev kodu |
| `metin` | Seçenek |
| `dogru` | Doğru seçenek için `evet`. `sirala` görevinde doğru sıra numarası (1, 2, 3…). |
| `hata_turu` | Yanlış seçenekse hatanın türü: `kanitsiz`, `veri`, `birim`, `iliski` |
| `hata_kaniti` | Bu yanlışı fark ettirecek kanıtın kodu (hata analizinde sorulur) |
| `hata_aciklamasi` | Bu seçeneğin neden yanlış olduğu. **Doğru cevabı söylememeli**, yalnızca hatayı açıklamalı. |

### İyi bir dosya için

- **Çeldiriciler güçlü olmalı.** Saçma, kolay elenen seçenekler yazmayın. En iyi çeldiriciler doğru cevapla ortak bir özelliği paylaşır ("ikisi de elektriği iyi iletir") ve ancak birden fazla kanıt birlikte değerlendirilince elenir.
- **En az beş farklı kanıt türü kullanın.** Sayısal ölçümler için birim ve belirsizlik verin (8,9 ± 0,1 g/cm³ gibi). Böylece birim ve ölçüm hataları da sorulabilir.
- **Bilimsel tuzaklar kurun.** Bazı kanıtlar tek başına yetersiz olmalı (birçok metal elektriği iletir; çoğu sembol iki harflidir). Öğrenci "bu kanıt yeterli değil" diyebilmeli.
- **Her elementi en az üç günlük kullanım bağlamında ele alın** ve kullanımı özelliğe bağlayın: kullanım → özellik → bu özelliğin nedeni → neden tercih edildiği.
- **İsim ve sembolün hikâyesini dedektiflik ipucu yapın:** etimolojik köken, keşif tarihi ve koşulları, sembolün neden o harflerden oluştuğu (Fe: ferrum, Ag: argentum…).
- **Bir veri tablosu ekleyin.** Sıralama, sınıflandırma, aykırı değer bulma ya da "ilişki neden-sonuç değildir" görevleri sorulabilir.
- **Her bilgi için kaynak yazın.** IUPAC, Royal Society of Chemistry (periodic-table.rsc.org), NIST, Encyclopaedia Britannica gibi güvenilir kaynaklar kullanın. Kaynaklar oyundaki "Bilimsel kaynakça" sayfasında listelenir.
- Her dosyada çok görev olmak zorunda değil. Tanıtım dosyasında 18 görev var, çünkü bütün görev türlerini gösteriyor. Yeni vakalarda 4–5 görev var; ilk 20 dosyada 7–9 görev.
- **Elementin adı, öğrenci onu bulmadan önce görünmemeli:** hikâyede, ilk kanıtlarda ve ilk görevin açıklamasında elementin adını yazmayın.

### Vakalar

Bütün vakaların listesi, temaları ve cevapları `VAKALAR.md` dosyasındadır. **Bu dosya cevap anahtarıdır; öğrencilerle paylaşmayın.** Temalara göre vaka sayıları: sağlık 34, bilim tarihi 29, ev ve günlük hayat 27, teknoloji 22, sanat-kültür-spor 19, enerji 17, sanayi ve ulaşım 17, doğa ve çevre 14, adli bilim ve güvenlik 11, uzay 10.

Bilgilerin kaynakları:

- Yoğunluklar, erime ve kaynama noktaları, elektron dizilimleri, izotoplar, keşif tarihleri, isim kökenleri ve kullanım alanları Royal Society of Chemistry periyodik tablosundan (periodic-table.rsc.org) alındı.
- Gerçek olaylara dayanan vakaların (Apollo 13, Minamata, Goiânia, Alvarez'lerin iridyum tabakası, Radyum Kızları, kilogram prototipi gibi) kaynakları vakanın kaynakçasında ayrıca gösterildi. Bu kaynaklar 7 Ekim 2026'da açılıp ilgili bilginin sayfada geçtiği denetlendi.
- Elektrik iletkenlikleri Serway'in *Principles of Physics* kitabındaki değerlerdir (Wikipedia tablosu üzerinden). Havuz kokusu için CDC, duman dedektörleri için EPA, pirit için geology.com kullanıldı.
- Vakalardaki laboratuvar ölçümleri kurgudur ama bilinen değerlerle uyumludur: ölçülen değer elementin gerçek değeridir, ± payı da tablodaki öteki adayları dışarıda bırakacak biçimde seçilmiştir. Gerçek olaylara dayanmayan vakaların hikâyeleri de kurgudur.
- Her dosyanın kaynakları oyundaki "Bilimsel kaynakça" sayfasında listelenir. Öğretmenin ve öğrencilerin bilgileri kaynaklardan bir kez daha kontrol etmesi önerilir.

## Öğretmen paneli ve araştırma verileri

Panoda **Öğretmen paneli**ne girilir. Şifre `js/ayarlar.js` dosyasındaki `ogretmenSifresi` değeridir (başlangıçta `2204`). **Uygulamadan önce bu şifreyi değiştirin.**

- **Katılımcı kodu:** Uygulamada her öğrenciye ad yerine bir kod verin (D07, K12 gibi) ve cihaza girin. Kod her kayda eklenir. Ad soyad kullanmayın.
- **Öğretmen modu:** Bütün seviyeler beklemeden açılır. İçerik denerken işe yarar.
- **İçerik uyarıları:** Tablolardaki hatalar satır numarasıyla listelenir.
- **Beceri tablosu:** Her becerideki görevleri ilk denemede doğru çözme oranı, seviyelere göre. Öğrencinin oyun içinde gelişimini gösterir. Her becerinin altında Maarif Modeli'ndeki karşılığı yazar (örneğin kanıt kullanma: FBAB12).
- **Verileri indir (CSV):** Bu cihazdaki bütün kayıtları Excel'de açılabilen bir dosya olarak indirir. Her satır bir olaydır (cevap, ipucu, kilit, hata analizi, savunma, dosya sonu). Satırlarda katılımcı kodu, dosya, görev, aşama, beceri, deneme sayısı, doğruluk, süre, hata türü, verilen cevap ve dosya puanı bulunur. Savunma metinleri ve öğrencinin kendi değerlendirmesi de bu dosyadadır; öğretmen bunları bir rubrikle puanlayabilir.

Araştırma için notlar:

- Kayıtlar yalnızca o cihazdaki tarayıcıda tutulur, hiçbir yere gönderilmez. Uygulama bitince her cihazdan verileri indirin.
- Oyun öğrencilerden veri topladığı için bir **veri toplama aracıdır**. MEB araştırma uygulama izni başvurusunda oyun da veri toplama araçları arasında anlatılmalıdır. Veli onam ve gönüllü katılım formları gerekir.
- Oyun içi veriler, oyunun dışında uygulanan geçerliliği gösterilmiş bir ön test / son test ile birlikte kullanılmalıdır.
- Savunma metinlerini puanlamak için yayımlanmış bir iddia–kanıt–gerekçe rubriği uyarlanabilir (örneğin McNeill ve Krajcik'in "Claim, Evidence, and Reasoning" çerçevesi). Uyarlanan rubriğin kaynağı raporda belirtilmelidir.
- Uygulamadan önce `icerik/` klasörünün bir kopyasını tarihle saklayın. Uygulama sırasında içerik değişmemeli.

## Türkiye Yüzyılı Maarif Modeli ile ilişkisi

Oyunun 9. sınıf kimya programındaki öğrenme çıktıları, beceriler ve öğretim yöntemleriyle ilişkisi `MAARIF_MODELI_UYUMU.md` dosyasında, programın resmî metnine dayanılarak anlatılmıştır.

## Yapay zekâ kullanım beyanı (taslak)

TÜBİTAK, üretken yapay zekânın kod üretmek gibi amaçlarla kullanılmasının başvuru sisteminde beyan edilmesini istiyor. Aşağıdaki metin, kullanımın gerçek hâline göre güncellenerek kullanılabilir:

> Oyunun yazılım altyapısı (ekranlar, görev türleri, kanıt ve hata analizi akışı, puanlama, araştırma kayıtları, içerik tablolarının okunması ve denetimi) ile 200 vakanın içeriği (hikâyeler, kanıtlar, veri tabloları, görevler, çeldiriciler, açıklamalar ve kaynaklar) ve bu içeriği üreten program, teknik destek veren bir gönüllü tarafından üretken yapay zekâ aracı Claude (Anthropic, Claude Opus 5.5 modeli) kullanılarak hazırlanmıştır. Oyunun tasarım ilkeleri, danışman öğretmenin üretken yapay zekâ aracı ChatGPT yardımıyla hazırladığı bir tasarım metnine dayanmaktadır. Proje öğrencileri şunları yapmıştır: [buraya öğrencilerin gerçekten yaptıklarını yazın; örneğin içeriğin kaynaklardan kontrolü, araştırma sorusunun ve ölçme araçlarının hazırlanması, uygulama, verilerin analizi ve rapor].

Beyan gerçeği yansıtmalıdır: öğrenciler yapay zekâyı başka işlerde de kullanırsa bunu da eklemelidir. Oyunun hem yazılımı hem içeriği yapay zekâ ile hazırlandığı için projede öğrencilerin özgün katkısı, oyunun etkisini ölçen araştırmanın kendisi olmalıdır: araştırma sorusu, ölçme araçları, uygulama, analiz ve yorum.
