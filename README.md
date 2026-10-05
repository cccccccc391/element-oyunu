# Element Oyunu (çalışma adı)

Elementlerin **hangi özelliği sayesinde nerede kullanıldığını** öğreten eğitsel bir web oyunu. Oyun telefonda uygulama gibi çalışır ve Android'de de iPhone'da da bir bağlantıyla açılır. TÜBİTAK 2204-A projesi için hazırlanmaktadır.

- 118 element, 6 bölüm (ilk bölüm ilk 20 element).
- Her soruda bir elementin kullanım alanı, o alanda kullanılmasını sağlayan özelliği ya da adının kökeni sorulur. Her cevaptan sonra "Neden?" açıklaması gösterilir.
- 3 can vardır. Canlar biterse bölüm baştan başlar ve sorularla şıkların sırası değişir, böylece cevaplar ezberlenemez.
- Bölüm sonunda bonus tur var: o bölümün elementlerinden oluşan maddeler **gözlem → soru → hipotez → deney → sonuç** basamaklarıyla incelenir.
- Oyun hiçbir kişisel bilgi toplamaz. İlerleme yalnızca o cihazın tarayıcısında tutulur.

Bütün sorular `icerik/` klasöründeki tablolardan **otomatik** üretilir. Öğrenciler kod yazmadan, yalnızca tabloları doldurarak oyunun içeriğini hazırlar.

## Klasördekiler

| Dosya | Görevi |
|---|---|
| `index.html` | Oyunun açılış sayfası |
| `css/stil.css` | Görünüm (renkler, yazılar, düğmeler) |
| `js/ayarlar.js` | Oyunun adı, can sayısı, puanlar: **kuralları buradan değiştirin** |
| `js/oyun.js` | Ekranlar ve oyunun akışı |
| `js/sorular.js` | Tablolardan soru üretimi |
| `js/icerik.js` | Tabloları okuma ve hata kontrolü |
| `js/csv.js` | CSV dosyası okuyucu (Excel ve Google E-Tablolar biçimleri) |
| `js/ilerleme.js` | Açılan bölümleri ve puanları cihazda saklama |
| `icerik/elementler.csv` | 118 elementin bilgileri (**öğrenciler dolduracak**) |
| `icerik/bonus.csv` | Bonus turdaki maddeler, her bölüm için 5 tane (**öğrenciler dolduracak**) |
| `icerik/bolumler.csv` | Bölümlerin adları ve element aralıkları |
| `img/` | Uygulama ikonları |
| `manifest.webmanifest`, `sw.js` | Telefonda ana ekrana eklenebilmesi ve internet yokken de çalışabilmesi için |

## Bilgisayarda çalıştırma

`index.html` dosyasına çift tıklayınca oyun **açılmaz**, çünkü tarayıcı güvenlik nedeniyle tabloları okumaz. Oyun bir web sunucusu üzerinden açılmalı. Bilgisayarda Python varsa bu klasörde şunu çalıştırın:

```bash
python -m http.server 8000
```

Sonra tarayıcıda `http://localhost:8000` adresini açın. (VS Code kullanıyorsanız "Live Server" eklentisi de olur.)

## Telefonda açma (yayınlama)

En kolay yol GitHub Pages:

1. GitHub'da yeni bir depo açın ve bu klasördeki dosyaların hepsini yükleyin.
2. Deponun **Settings → Pages** bölümünde kaynak olarak `main` dalını ve kök klasörü (`/`) seçin.
3. Birkaç dakika sonra verilen adres (`https://kullaniciadi.github.io/depo-adi/`) telefonda da açılır. Bu adresten bir QR kod üretip sınıfta paylaşabilirsiniz.

Telefonda adres açıldıktan sonra tarayıcı menüsündeki **"Ana ekrana ekle"** ile oyun uygulama gibi ikonla açılır. Oyun bir kez açıldıktan sonra internet kesilse bile oynanmaya devam eder.

## İçerik nasıl hazırlanır (öğrenciler için)

Tablolar Türkçe Excel'de çift tıklayınca doğru açılır. Google E-Tablolar'da da **Dosya → İçe aktar** ile açılabilir. Kaydederken:

- **Excel:** "CSV (noktalı virgülle ayrılmış)" ya da "CSV UTF-8" seçin, ikisi de çalışır.
- **Google E-Tablolar:** **Dosya → İndir → Virgülle ayrılmış değerler (.csv)** seçin ve dosyayı `icerik/` klasöründeki eski dosyanın yerine koyun.
- **İlk satırdaki sütun adlarını değiştirmeyin.**

Her kayıttan sonra oyunun ana sayfasındaki **İçerik durumu** ekranını açın. Bu ekran hangi bölümde kaç sorunun hazır olduğunu ve tablolardaki hataları satır numarasıyla gösterir. Henüz bitmemiş bölümleri denemek için aynı ekrandaki **öğretmen modu** bütün bölümlerin kilidini açar.

### `elementler.csv`

| Sütun | Ne yazılır | Örnek (Helyum) |
|---|---|---|
| `no`, `sembol`, `ad` | Hazır, değiştirmeyin | 2, He, Helyum |
| `kullanim` | Günlük hayatta nerede kullanıldığı | Uçan balonlar ve zeplinler |
| `ozellik` | Orada kullanılmasını sağlayan özelliği | Havadan hafiftir ve yanmaz |
| `neden` | Özelliğin o kullanımı nasıl mümkün kıldığı (cevaptan sonra gösterilir) | Havadan hafif olduğu için balonu yukarı taşır… |
| `celdirici1`–`celdirici3` | Bu element için **yanlış** ama akla yatkın üç özellik | Elektriği çok iyi iletir |
| `isim_koken` | Adının nereden geldiği | Yunanca 'helios' (Güneş) kelimesinden… |
| `kaynak` | Bilginin alındığı güvenilir kaynak | Ders kitabı, ansiklopedi ya da bilimsel site adresi |

Kurallar:

- `kullanim`, `ozellik` ve `neden` sütunlarının **üçü birden** dolu olmalı. Biri eksik olan satır kullanılmaz ve İçerik durumu ekranında uyarı olarak görünür.
- Bir elementin ikinci bir kullanımını yazmak için **aynı atom numarasıyla yeni bir satır** ekleyin. Bu satırda `sembol` ve `ad` boş kalabilir.
- Çeldiricileri mutlaka yazın. Yazılmazsa oyun aynı bölümdeki başka elementlerin özelliklerini kullanır ve bu bazen iki doğru cevabı olan soru çıkarabilir.
- `isim_koken` yazarken elementin adını kullanmamaya çalışın. Oyun adı soruda zaten `___` ile gizler.
- Her bilgi için kaynak yazın. Jüri bilgilerin nereden alındığını soracaktır.
- Helyum, Neon ve Silisyum satırlarındaki bilgiler **yalnızca biçimi göstermek için konmuş örneklerdir**. Öğrenciler bunları kontrol edip kendi araştırdıkları bilgilerle değiştirmelidir. Element adlarını da ders kitabındaki yazımlarla karşılaştırın.

### `bonus.csv`

Her bölüm için 5 madde yazılır. Sütunlar bilimsel yöntemin basamaklarına karşılık gelir:

| Sütun | Basamak | Örnek (Sofra tuzu) |
|---|---|---|
| `bolum` | Hangi bölümden sonra sorulacağı | 1 |
| `madde` | Maddenin adı | Sofra tuzu |
| `gozlem` | **Gözlem**: maddenin gözle görülen özellikleri | Beyaz, küp biçimli kristaller… |
| `soru` | **Soru** | Sofra tuzu hangi elementlerden oluşur? |
| `dogru`, `yanlis1`–`yanlis3` | **Hipotez**: öğrencinin seçeceği şıklar | Sodyum ve klor / Kalsiyum ve karbon… |
| `deney` | **Deney**: hipotezi sınayan bir deney ya da gözlemin sonucu | Tuz alevde sarı renk verir… |
| `sonuc` | **Sonuç**: açıklama | Sofra tuzu sodyum klorürdür (NaCl)… |
| `kaynak` | Kaynak | |

Öğrenci, deneyden önce kurduğu hipotez doğruysa 20, deneyi okuduktan sonra doğru cevaba geçerse 10 bonus puan alır. "Sofra tuzu" ve "Kemik" satırları örnektir.

### `bolumler.csv`

Bölümlerin adları ve hangi atom numaralarını kapsadığı. Bölümlere öğrencilerin seçeceği adlar verilebilir.

## Oyunun kurallarını değiştirmek

`js/ayarlar.js` dosyasındaki değerler değiştirilerek oyunun adı, can sayısı, puanlar ve soru türlerinin ne sıklıkla çıkacağı ayarlanabilir. **Oyunun adını öğrenciler koymalı.**

## Öğrencilerin ekleyebileceği özellikler

Aşağıdakiler oyunda bilerek yapılmadı, öğrencilerin geliştirmesi için bırakıldı:

- **Mucit görevi:** Oyunun sonunda bir ihtiyaç verilir ("hafif ve paslanmayan bir bisiklet kadrosu") ve öğrenci uygun elementleri seçip gerekçesini yazar.
- **6. bölüme özel tasarım:** 101–118 arasındaki elementler yalnızca laboratuvarda, çok az miktarda üretilir ve günlük hayatta kullanılmaz. Bu bölümün soruları isimlerin hikâyesine (bilim insanları, şehirler, ülkeler) ve "neden kullanılamıyor?" sorusuna yönelebilir.
- **Periyodik tablo ekranı:** Doğru cevaplanan elementlerin periyodik tabloda yanması.
- Element ve madde fotoğrafları, ses efektleri, telefonun geri tuşuyla önceki ekrana dönme.

## Araştırma için notlar

- **Kontrol grubu için bilgi kartları:** Deney grubu oyunu oynarken kontrol grubu aynı bilgileri kâğıt üzerinde çalışacaksa, kartlar aynı `elementler.csv` dosyasından hazırlanmalı. Böylece iki grubun aldığı bilgi aynı olur ve fark yalnızca oyundan kaynaklanır.
- **İçeriği dondurun:** Uygulamadan önce `icerik/` klasörünün bir kopyasını tarihle saklayın. Uygulama sırasında içerik değişmemeli.
- **Ön test ve son test oyunun dışında yapılır** (kâğıt ya da çevrim içi form). Oyun kişisel veri toplamaz. Öğrencilerle yapılacak uygulama için MEB Araştırma Uygulama İzni ve veli onam formları gereklidir.

## Yapay zekâ kullanım beyanı (taslak)

TÜBİTAK, üretken yapay zekânın kod üretmek gibi amaçlarla kullanılmasının başvuru sisteminde beyan edilmesini istiyor. Aşağıdaki metin, kullanımın gerçek hâline göre güncellenerek kullanılabilir:

> Oyunun yazılım altyapısı (ekranlar, sorulara ait tablolardan otomatik soru üretimi, puanlama, bonus turu akışı ve içerik dosyalarının okunması), teknik destek veren bir gönüllü tarafından üretken yapay zekâ aracı Claude (Anthropic, Claude Opus 5.5 modeli) kullanılarak geliştirilmiştir. Elementlerin kullanım alanları, bu kullanımları sağlayan özellikler, açıklamalar, çeldiriciler, isim kökenleri, bonus turundaki maddeler ve kaynakları; başarı testi, uygulama, verilerin analizi ve rapor; oyuna sonradan eklenen özellikler proje öğrencileri tarafından hazırlanmıştır.

Öğrenciler oyuna kendi ekledikleri özellikleri ve yapay zekâyı başka işlerde kullandılarsa bunu da beyana eklemelidir.
