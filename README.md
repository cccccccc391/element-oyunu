# Element Dosyaları: Atomun Peşinde

BİLSEM lise öğrencileri için bilimsel akıl yürütme oyunu (TÜBİTAK 2204-A projesi). Oyuncu, Element Araştırma Birimi'ne yeni katılmış bir bilim dedektifidir. Dosyalarda elementin adı yazmaz; öğrenci ölçümlerden, gözlemlerden, veri tablolarından, periyodik tablodaki konumdan ve tarihsel kayıtlardan elementin kimliğini çıkarır ve buna nasıl ulaştığını savunur.

Oyunun asıl sorusu "Bu element hangisi?" değil, **"Bunu nereden biliyorsun?"** sorusudur. Bilim insanı cevabı tahmin etmez; kanıtlar.

Oyun telefonda uygulama gibi çalışan bir web oyunudur. Android'de de iPhone'da da bir bağlantıyla açılır ve bir kez açıldıktan sonra internet olmadan da oynanabilir.

## Oyunun yapısı

- **4 seviye, 20 dosya:** Gözlem (D01–D05), Çıkarım (D06–D10), Kanıt (D11–D15), Bilimsel Savunma (D16–D20). D20 final dosyasıdır: Bilimsel Jüri. Her dosyanın elementi farklıdır.
- **Dosya:** Bir giriş hikâyesi, kanıt kartları ve görevlerden oluşur. Bazı kanıtlar ancak doğru adım atılınca açılır. Görevler bilimsel yöntem zincirini izler: **gözlem → veri → hipotez → kanıt → çıkarım → sonuç**. Dosyanın sonunda **iddia → kanıt → gerekçe → karşı kanıt → sonuç** biçiminde bir bilimsel argüman kurulur.
- **3 bilimsel hata hakkı:** Her yanlış cevap türüyle birlikte gösterilir: kanıta dayanmayan çıkarım, veriyi yanlış yorumlama, birim / ölçüm hatası, kimyasal özelliği yanlış ilişkilendirme. Doğru cevap söylenmez; yalnızca hatanın neden hata olduğu açıklanır.
- **Dosya kilitlenir:** Üç hatada "Araştırma dosyası kilitlendi" yazar ve öğrenci sonraki dosyaya geçemez. Dosyayı yeniden açmak için **bilimsel hata analizi** yapar: her hatası için hangi kanıtı yanlış yorumladığını, hangi varsayımının hatalı olduğunu ve doğru yaklaşımın ne olduğunu bulur.
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
| `icerik/*.csv` | 20 dosyanın içeriği (dosyalar, kanıtlar, veri tabloları, görevler, seçenekler) |
| `manifest.webmanifest`, `sw.js`, `img/` | Ana ekrana ekleme, çevrim dışı çalışma, ikonlar |

## Çalıştırma

**Telefonda:** Oyun GitHub Pages'te yayımlanır. Depodaki dosyalar güncellenince oyun 1–2 dakika içinde kendiliğinden güncellenir. Telefonda tarayıcı menüsündeki "Ana ekrana ekle" ile uygulama gibi açılır.

**Bilgisayarda:** `index.html` dosyasına çift tıklayınca oyun açılmaz, çünkü tarayıcı içerik tablolarını bu şekilde okumaz. Bilgisayarda Python varsa bu klasörde şu komutu çalıştırıp tarayıcıda `http://localhost:8000` adresini açın:

```bash
python -m http.server 8000
```

## Dosya eklemek ya da değiştirmek

Bir dosyanın içeriği beş tabloya dağılır. Tablolar birbirine `dosya` ve `id` sütunlarıyla bağlanır. Var olan 20 dosya düzenlenebilir ya da yenileri eklenebilir; yeni bir dosya hazırlarken var olanların satırlarını örnek alın. `D01` bütün görev türlerini gösteren tanıtım dosyasıdır.

Tablolar Türkçe Excel'de çift tıklayınca doğru açılır. Kaydederken "CSV (noktalı virgülle ayrılmış)" ya da "CSV UTF-8" seçin, ikisi de çalışır. Google E-Tablolar'da **Dosya → İçe aktar** ile açıp **Dosya → İndir → .csv** ile indirebilirsiniz. **İlk satırdaki sütun adlarını değiştirmeyin.** Her kayıttan sonra **Öğretmen paneli**ni açın. Tablolardaki hatalar orada dosya adı ve satır numarasıyla listelenir. Hatalı bir görev atlanır, dosyanın geri kalanı çalışmaya devam eder.

### 1. `dosyalar.csv`: her satır bir dosya

| Sütun | Ne yazılır |
|---|---|
| `id` | Dosya kodu (D01…D20). Değiştirmeyin. |
| `seviye`, `sira` | Seviye (1–4) ve seviye içindeki sıra |
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
- Her dosyada çok görev olmak zorunda değil. Örnek dosyada 18 görev var, çünkü bütün görev türlerini gösteriyor. 8–12 görev çoğu dosya için yeterli.

### Dosyalar

| Seviye | Dosyalar |
|---|---|
| 1 · Gözlem | D01 Gizemli Metal (tanıtım) · D02 Uçan Balon Vakası · D03 Kutu, Folyo ve Uçak · D04 Kurşun Kalem Vakası · D05 Kırık Termometre |
| 2 · Çıkarım | D06 Yırtık Diş Macunu Etiketi · D07 Havai Fişek Gecesi · D08 Kemik ve Alçı · D09 Şişen Batarya · D10 Cips Paketinin Sırrı |
| 3 · Kanıt | D11 Havadaki Gizli Gaz · D12 Sahte Altın · D13 Paslanan Köprü · D14 Havuzdaki Koku · D15 Tavandaki Küçük Kutu |
| 4 · Bilimsel Savunma | D16 Dokunmatik Ekranın Görünmez Teli · D17 Kalça Protezi · D18 Kararan Kaşık · D19 Ampulün Kalbi · D20 Bilimsel Jüri: Yağdaki Metal |

Bilgilerin kaynakları:

- Yoğunluklar, erime ve kaynama noktaları, keşif tarihleri, isim kökenleri ve kullanım alanları Royal Society of Chemistry periyodik tablosundan (periodic-table.rsc.org) doğrulandı.
- Elektrik iletkenlikleri Serway'in *Principles of Physics* kitabındaki değerlerdir (Wikipedia tablosu üzerinden).
- Havuz kokusu ve kloraminler için ABD Hastalık Kontrol ve Önleme Merkezleri (CDC), duman dedektörleri için ABD Çevre Koruma Ajansı (EPA), pirit için geology.com kullanıldı.
- Vakaların hikâyeleri ve vakalardaki ölçüm sonuçları kurgudur ama bilinen değerlerle uyumludur. Örneğin D11'deki ölçüm tablosu Rayleigh'nin gerçek deneyinin sonucunu, azot ve argonun bilinen yoğunluklarından hesaplanan değerlerle canlandırır.
- Her dosyanın kaynakları oyundaki "Bilimsel kaynakça" sayfasında listelenir. Öğretmenin ve öğrencilerin bilgileri kaynaklardan bir kez daha kontrol etmesi önerilir.

## Öğretmen paneli ve araştırma verileri

Panoda **Öğretmen paneli**ne girilir. Şifre `js/ayarlar.js` dosyasındaki `ogretmenSifresi` değeridir (başlangıçta `2204`). **Uygulamadan önce bu şifreyi değiştirin.**

- **Katılımcı kodu:** Uygulamada her öğrenciye ad yerine bir kod verin (D07, K12 gibi) ve cihaza girin. Kod her kayda eklenir. Ad soyad kullanmayın.
- **Öğretmen modu:** Bütün dosyalar sırayla beklemeden açılır. İçerik denerken işe yarar.
- **İçerik uyarıları:** Tablolardaki hatalar satır numarasıyla listelenir.
- **Beceri tablosu:** Her becerideki görevleri ilk denemede doğru çözme oranı, seviyelere göre. Öğrencinin oyun içinde gelişimini gösterir.
- **Verileri indir (CSV):** Bu cihazdaki bütün kayıtları Excel'de açılabilen bir dosya olarak indirir. Her satır bir olaydır (cevap, ipucu, kilit, hata analizi, savunma, dosya sonu). Satırlarda katılımcı kodu, dosya, görev, aşama, beceri, deneme sayısı, doğruluk, süre, hata türü, verilen cevap ve dosya puanı bulunur. Savunma metinleri ve öğrencinin kendi değerlendirmesi de bu dosyadadır; öğretmen bunları bir rubrikle puanlayabilir.

Araştırma için notlar:

- Kayıtlar yalnızca o cihazdaki tarayıcıda tutulur, hiçbir yere gönderilmez. Uygulama bitince her cihazdan verileri indirin.
- Oyun öğrencilerden veri topladığı için bir **veri toplama aracıdır**. MEB araştırma uygulama izni başvurusunda oyun da veri toplama araçları arasında anlatılmalıdır. Veli onam ve gönüllü katılım formları gerekir.
- Oyun içi veriler, oyunun dışında uygulanan geçerliliği gösterilmiş bir ön test / son test ile birlikte kullanılmalıdır.
- Savunma metinlerini puanlamak için yayımlanmış bir iddia–kanıt–gerekçe rubriği uyarlanabilir (örneğin McNeill ve Krajcik'in "Claim, Evidence, and Reasoning" çerçevesi). Uyarlanan rubriğin kaynağı raporda belirtilmelidir.
- Uygulamadan önce `icerik/` klasörünün bir kopyasını tarihle saklayın. Uygulama sırasında içerik değişmemeli.

## Yapay zekâ kullanım beyanı (taslak)

TÜBİTAK, üretken yapay zekânın kod üretmek gibi amaçlarla kullanılmasının başvuru sisteminde beyan edilmesini istiyor. Aşağıdaki metin, kullanımın gerçek hâline göre güncellenerek kullanılabilir:

> Oyunun yazılım altyapısı (ekranlar, görev türleri, kanıt ve hata analizi akışı, puanlama, araştırma kayıtları, içerik tablolarının okunması ve denetimi) ile 20 dosyanın içeriği (vakalar, kanıtlar, veri tabloları, görevler, çeldiriciler, açıklamalar ve kaynaklar), teknik destek veren bir gönüllü tarafından üretken yapay zekâ aracı Claude (Anthropic, Claude Opus 5.5 modeli) kullanılarak hazırlanmıştır. Oyunun tasarım ilkeleri, danışman öğretmenin üretken yapay zekâ aracı ChatGPT yardımıyla hazırladığı bir tasarım metnine dayanmaktadır. Proje öğrencileri şunları yapmıştır: [buraya öğrencilerin gerçekten yaptıklarını yazın; örneğin içeriğin kaynaklardan kontrolü, araştırma sorusunun ve ölçme araçlarının hazırlanması, uygulama, verilerin analizi ve rapor].

Beyan gerçeği yansıtmalıdır: öğrenciler yapay zekâyı başka işlerde de kullanırsa bunu da eklemelidir. Oyunun hem yazılımı hem içeriği yapay zekâ ile hazırlandığı için projede öğrencilerin özgün katkısı, oyunun etkisini ölçen araştırmanın kendisi olmalıdır: araştırma sorusu, ölçme araçları, uygulama, analiz ve yorum.
