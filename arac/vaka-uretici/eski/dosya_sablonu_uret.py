"""Element Dosyalari icin icerik tablolarini (CSV) uretir.

D01 "Gizemli Metal" tam bir ornek dosyadir: oyunun butun gorev turlerini gosterir.
D02-D20 yalnizca bos satirlardir; icerigi ogrenciler yazacak.
Dosyalar Turkce Excel'de cift tiklayinca dogru acilsin diye UTF-8 BOM'lu ve
noktali virgul ayiricili yazilir.

Sayisal veriler:
- Yogunluk ve erime noktalari: RSC Periodic Table element sayfalari (periodic-table.rsc.org)
- Elektrik iletkenligi (20 C, MS/m): Serway, Principles of Physics; Wikipedia
  "Electrical resistivity and conductivity" tablosundan aktarildi.
"""
import csv
import pathlib
import sys

HEDEF = pathlib.Path(sys.argv[1])

RSC_BAKIR = "https://periodic-table.rsc.org/element/29/copper"
KAYNAKCA_D01 = " | ".join([
    "Royal Society of Chemistry, Periyodik Tablo: Bakır — " + RSC_BAKIR,
    "Royal Society of Chemistry, Periyodik Tablo: Nikel — https://periodic-table.rsc.org/element/28/nickel",
    "Royal Society of Chemistry, Periyodik Tablo: Kobalt — https://periodic-table.rsc.org/element/27/cobalt",
    "Royal Society of Chemistry, Periyodik Tablo: Demir, Alüminyum, Gümüş — https://periodic-table.rsc.org",
    "Elektrik iletkenliği değerleri (20 °C): Serway, R. A., Principles of Physics; aktaran: "
    "https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity",
])

DOSYALAR = [{
    "id": "D01", "seviye": "1", "sira": "1", "baslik": "Gizemli Metal",
    "giris": "Eski bir binanın elektrik tesisatından çıkarılan bir tel parçası birimimize getirildi. "
             "Telin etiketi silinmiş, yüzeyi kirli. Analiz cihazı arızalı olduğu için yalnızca kısmi bir rapor "
             "verebildi. Görevin: kanıtları inceleyerek telin hangi elementten yapıldığını bulmak ve bu sonuca "
             "nasıl ulaştığını kanıtlarla savunmak.",
    "cevap": "Cu", "final": "", "ornek": "evet", "kaynakca": KAYNAKCA_D01,
}]
for no in range(2, 21):
    seviye = (no - 1) // 5 + 1
    DOSYALAR.append({"id": f"D{no:02d}", "seviye": str(seviye), "sira": str((no - 1) % 5 + 1),
                     "final": "evet" if no == 20 else ""})

KANITLAR = [
    ("K1", "yogunluk", "Yoğunluk ölçümü",
     "8,9 ± 0,1 g/cm³ (okul laboratuvarında ölçüldü; ölçümün belirsizliği ±0,1 g/cm³)", "", ""),
    ("K2", "iletkenlik", "Elektrik iletkenliği",
     "Telin iki ucu arasındaki direnç çok düşük ölçüldü: madde elektriği çok iyi iletiyor.", "", ""),
    ("K3", "iletkenlik", "Isı iletkenliği",
     "Telin bir ucu sıcak suya daldırılınca diğer ucu kısa sürede ısındı.", "", ""),
    ("K4", "konum", "Analiz cihazının kısmi raporu",
     "Element 4. periyotta ve d bloğunda yer alıyor. Cihaz daha fazla bilgi veremeden arızalandı.", "", ""),
    ("K5", "sembol", "Envanter kaydı",
     "Eski bir envanter defterinde bu metalin sembolünün iki harfli olduğu ve ikinci harfin küçük yazıldığı not edilmiş.",
     "", ""),
    ("K6", "kullanim", "Günlük kullanım",
     "Bu metal ev ve binaların elektrik kablolarında yaygın olarak kullanılıyor.", "", ""),
    ("K7", "tablo", "Aday metallerin bilinen özellikleri", "T1", "",
     "Yoğunluk ve erime noktası: RSC Periyodik Tablo; iletkenlik: Serway, Principles of Physics"),
    ("K8", "deney", "Mıknatıs testi",
     "Tel, güçlü bir mıknatısa yaklaştırıldığında çekilmedi.", "G4", ""),
    ("K9", "fiziksel", "Temizlenen yüzey",
     "Zımparalanan yüzey kırmızımsı-turuncu renkte ve metalik parlaklıkta.", "G5", ""),
    ("K10", "isim", "Arşiv notu",
     "Eski kayıtlara göre bu metalin Latince adı 'cuprum'. Romalılar ona 'Cyprium aes', yani 'Kıbrıs metali' "
     "derdi. İngilizce adı 'copper' da Eski İngilizce 'coper' kelimesi üzerinden bu Latince addan türemiştir.",
     "G6", RSC_BAKIR),
]

TABLO = [
    ["Metal", "Yoğunluk (g/cm³)", "Elektrik iletkenliği (MS/m, 20 °C)", "Erime noktası (°C)", "Mıknatısa çekilir mi?"],
    ["Alüminyum", "2,70", "35,5", "660", "Hayır"],
    ["Demir", "7,87", "10,3", "1538", "Evet"],
    ["Kobalt", "8,86", "16,0", "1495", "Evet"],
    ["Nikel", "8,90", "14,3", "1455", "Evet"],
    ["Bakır", "8,96", "59,6", "1085", "Hayır"],
    ["Gümüş", "10,5", "63,0", "962", "Hayır"],
]

# (id, asama, arguman, tur, kategori, beceri, soru, ipucu, aciklama, dogru, hata_turu, secenekler)
# secenek: (metin, dogru, hata_turu, hata_kaniti, hata_aciklamasi)
GOREVLER = [
    ("G1", "Gözlem", "", "tekli", "kanit", "gozlem",
     "İlk kanıtlara (K2 ve K3) göre bu madde hakkında hangi sonuca güvenle varabilirsin?",
     "Elektriği ve ısıyı iyi iletmek hangi madde sınıfının ortak özelliği? Bu özellik kaç farklı maddede görülür?",
     "Elektriği ve ısıyı iyi iletmek metallerin ortak özelliğidir. Bu kanıt maddenin bir metal olduğunu gösterir ama "
     "hangi metal olduğunu söylemez, çünkü pek çok metal elektriği ve ısıyı iyi iletir.",
     "", "", [
         ("Madde bir metaldir.", "evet", "", "", ""),
         ("Madde bakırdır, çünkü elektriği çok iyi iletiyor.", "", "kanitsiz", "K2",
          "Elektriği çok iyi ileten birçok metal var: gümüş, alüminyum, altın... Bu kanıt tek başına bakırı göstermez."),
         ("Maddenin yoğunluğu yüksektir, çünkü ısıyı iyi iletiyor.", "", "iliski", "K3",
          "Isı iletkenliği ile yoğunluk farklı özelliklerdir; birinden diğeri çıkarılamaz. Alüminyum ısıyı iyi iletir "
          "ama yoğunluğu düşüktür."),
         ("Madde bir yarı metaldir, çünkü elektriği iletiyor.", "", "iliski", "K2",
          "Yarı metaller elektriği metaller kadar iyi iletmez. Telin direncinin çok düşük olması metalik iletkenliğe işaret eder."),
     ]),
    ("G2", "Veri", "", "tablo", "kanit", "veri",
     "Analiz cihazının kısmi raporuna (K4) göre aday olabilecek bütün elementleri periyodik tabloda işaretle.",
     "4. periyot potasyumla (19) başlar. d bloğu 3. gruptan 12. gruba kadar uzanır.",
     "4. periyodun d bloğunda 10 element var: skandiyumdan (21) çinkoya (30) kadar. Kısmi rapor adayları 118 "
     "elementten 10 elemente indirdi ama henüz tek bir sonuç yok.",
     "Sc Ti V Cr Mn Fe Co Ni Cu Zn", "veri", []),
    ("G3", "Veri", "", "tekli", "kanit", "veri",
     "Ölçülen yoğunluk 8,9 ± 0,1 g/cm³ (K1). Tablodaki verilere (K7) göre yalnızca yoğunluk bilgisiyle kesin "
     "sonuca ulaşılabilir mi?",
     "Ölçümün belirsizliğini hesaba kat: 8,8 ile 9,0 g/cm³ arasındaki bütün değerler ölçümle uyumludur.",
     "Hayır. 8,8–9,0 g/cm³ aralığına tablodaki üç metal giriyor: kobalt (8,86), nikel (8,90) ve bakır (8,96). "
     "Bu ölçüm, bu üç metali birbirinden ayırmaya yetmez; başka bir kanıt gerekir. Demir (7,87) ise bu kanıtla elenir.",
     "", "", [
         ("Hayır; tablodaki kobalt, nikel ve bakırın yoğunlukları ölçümün belirsizlik aralığına giriyor.", "evet", "", "", ""),
         ("Evet; 8,96 g/cm³ yalnızca bakıra aittir ve ölçüm 8,9'a çok yakındır.", "", "veri", "K1",
          "Ölçüm 8,9 ± 0,1 g/cm³; yani 8,8 ile 9,0 arasındaki her değer olabilir. Tabloda bu aralığa giren birden "
          "fazla metal var."),
         ("Evet; yoğunluk bir maddeyi tek başına tanımlayan bir özelliktir.", "", "kanitsiz", "K7",
          "Yoğunluk ayırt edici bir özelliktir ama farklı maddelerin yoğunlukları birbirine çok yakın olabilir. "
          "Tablo bunun bir örneğini gösteriyor."),
         ("Hayır; çünkü yoğunluk g/cm³ ile değil kilogram ile ölçülür.", "", "birim", "K1",
          "Yoğunluk kütlenin hacme oranıdır; birimi g/cm³ ya da kg/m³ olur. Kilogram yalnızca kütle birimidir."),
     ]),
    ("G4", "Hipotez", "", "tekli", "alternatif", "hipotez",
     "Adaylar kobalt, nikel ve bakır. Tablodaki sütunlara bakarak, örneği bozmadan bu üç adayı birbirinden "
     "ayırabilecek en uygun test hangisidir?",
     "Tabloda bu üç metal arasında 'evet / hayır' gibi açık bir fark gösteren sütun var mı?",
     "Mıknatıs testi örneği bozmaz. Tabloya göre kobalt ve nikel mıknatısa çekilir, bakır çekilmez; bu yüzden "
     "adayları ayırmak için en uygun test budur. Erime noktaları da farklıdır ama ölçmek için örneği eritmek gerekir.",
     "", "", [
         ("Mıknatıs testi", "evet", "", "", ""),
         ("Erime noktasını ölçmek", "", "veri", "K7",
          "Erime noktaları gerçekten farklı, ama bu ölçüm örneği eritmeyi gerektirir. Soru örneği bozmadan "
          "yapılabilecek testi soruyor."),
         ("Yoğunluğu aynı yöntemle bir kez daha ölçmek", "", "birim", "K1",
          "Aynı yöntemle yapılan yeni ölçümün belirsizliği yine ±0,1 g/cm³ olur. Bu belirsizlik, yoğunlukları "
          "birbirine 0,1 g/cm³'ten daha yakın olan metalleri ayırmaya yetmez."),
         ("Elektriği iletip iletmediğini denemek", "", "kanitsiz", "K2",
          "Üç aday da metaldir ve elektriği iletir. 'İletiyor mu?' sorusunun cevabı üçü için de 'evet' olacağından "
          "bu test adayları ayırmaz."),
     ]),
    ("G5", "Kanıt", "", "coklu", "kanit", "cikarim",
     "Mıknatıs testinin sonucu (K8) kobalt, nikel ve bakırdan hangilerini eler? Elenenlerin hepsini seç.",
     "Tabloda mıknatısa çekilen metaller hangileri? Örnek mıknatısa çekildi mi?",
     "Örnek mıknatısa çekilmedi. Tabloya göre kobalt ve nikel mıknatısa çekilir, bu yüzden ikisi de elenir. "
     "Geriye bakır kalır.",
     "", "veri", [
         ("Kobalt", "evet", "", "", ""),
         ("Nikel", "evet", "", "", ""),
         ("Bakır", "", "veri", "K7",
          "Tabloya göre bakır mıknatısa çekilmez; yani örnekle aynı davranıyor. Mıknatıs testi bakırı elemez."),
         ("Hiçbirini; mıknatıs testi metalleri birbirinden ayırmaz.", "", "kanitsiz", "K7",
          "Tablodaki 'Mıknatısa çekilir mi?' sütunu metallerin bu testte farklı davrandığını gösteriyor."),
     ]),
    ("G6", "Çıkarım", "", "yaz", "kimlik", "cikarim",
     "Kanıtlara göre tel hangi elementten yapılmıştır? Adını ya da sembolünü yaz.",
     "Adaylardan hangisi mıknatısa çekilmiyor? Yüzeyin rengi (K9) sonucunu destekliyor mu?",
     "Tel bakırdır (Cu). Kısmi rapor 4. periyodun d bloğunu, yoğunluk kobalt–nikel–bakır üçlüsünü, mıknatıs testi de "
     "bakırı gösteriyor. Kırmızımsı renk bu sonucu destekliyor.",
     "", "kanitsiz", []),
    ("G7", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
     "Bakırın ev elektrik kablolarında yaygın kullanılmasının bilimsel nedeni nedir?",
     "Bir kablo malzemesinde iki şey gerekir: akımı iyi taşımak ve ...?",
     "Metallerde elektronların bir kısmı tek bir atoma bağlı değildir; metal yapı içinde serbestçe hareket edebilir. "
     "Bu yüzden bakır elektriği çok iyi iletir. Ayrıca kolayca işlenip ince tel hâline getirilebilir. RSC'ye göre "
     "bakırın büyük kısmı bu iki özellik nedeniyle kablolarda ve elektrik motorlarında kullanılır.",
     "", "", [
         ("Elektriği çok iyi iletir ve kolayca ince tel hâline getirilebilir.", "evet", "", "", ""),
         ("Yoğunluğu yüksek olduğu için akımı daha hızlı taşır.", "", "iliski", "K7",
          "Yoğunluk iletkenliği belirlemez: tablodaki nikel bakırla neredeyse aynı yoğunlukta ama çok daha az iletir."),
         ("Mıknatısa çekilmediği için elektriği iletir.", "", "kanitsiz", "K8",
          "Mıknatısa çekilmemek ile elektriği iletmek farklı özelliklerdir. Tablodaki demir mıknatısa çekildiği hâlde "
          "elektriği iletir."),
         ("Erime noktası yüksek olduğu için içinden akım geçerken hiç ısınmaz.", "", "veri", "K7",
          "Akım geçen her tel bir miktar ısınır. Erime noktası telin ne kadar ısıya dayanabileceğiyle ilgilidir; "
          "iletkenliğin nedeni değildir."),
     ]),
    ("G8", "Veri", "", "sirala", "kanit", "veri",
     "Tabloya (K7) göre şu metalleri elektrik iletkenliği en yüksek olandan en düşük olana doğru sırala.",
     "İletkenlik sütununda büyük sayı daha iyi iletkenlik demektir.",
     "Gümüş (63,0) > bakır (59,6) > alüminyum (35,5) > demir (10,3 MS/m). Gümüş elektriği en iyi ileten metaldir; "
     "bakır onu çok yakından izler.",
     "", "veri", [
         ("Gümüş", "1", "", "", ""),
         ("Bakır", "2", "", "", ""),
         ("Alüminyum", "3", "", "", ""),
         ("Demir", "4", "", "", ""),
     ]),
    ("G9", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
     "Gümüş elektriği bakırdan da iyi iletiyor. Buna rağmen ev kablolarında neden gümüş değil de bakır kullanılır?",
     "Bir malzeme seçilirken yalnızca bilimsel özelliklerine mi bakılır?",
     "Malzeme seçiminde tek ölçüt en iyi özellik değildir; ne kadar bulunduğu ve maliyeti de önemlidir. Gümüş en iyi "
     "iletken olsa da çok daha az bulunur ve pahalıdır. Bakır hem çok iyi iletir hem de çok daha boldur; RSC bakırın "
     "bakır, gümüş ve altın arasında en yaygın, bu yüzden en ucuz olanı olduğunu belirtir.",
     "", "", [
         ("Gümüş çok daha az bulunur ve pahalıdır; bakır hem çok iyi iletir hem de daha bol ve ucuzdur.", "evet", "", "", ""),
         ("Gümüş tel hâline getirilemez.", "", "iliski", "",
          "Gümüş de kolayca işlenip tel hâline getirilebilen bir metaldir. Bu seçenek gerçeği yansıtmıyor."),
         ("Tablo yanlıştır; aslında bakır gümüşten daha iyi iletir.", "", "veri", "K7",
          "Tablodaki değerler güvenilir bir kaynaktan alınmıştır. Bir veriyi reddetmek için onunla çelişen başka bir "
          "kanıt gerekir."),
         ("Gümüş mıknatısa çekildiği için kablolarda tehlikelidir.", "", "veri", "K7",
          "Tabloya göre gümüş mıknatısa çekilmez."),
     ]),
    ("G10", "Çıkarım", "", "tekli", "kanit", "veri",
     "Bir öğrenci tablodan yalnızca alüminyum, bakır ve gümüşü seçip şöyle diyor: \"Yoğunluk arttıkça iletkenlik de "
     "artıyor. Demek ki yüksek yoğunluk iyi iletkenliğe neden oluyor.\" Bu çıkarım hakkında ne söylenebilir?",
     "Tablonun tamamına bak: Bu eğilime uymayan metal var mı?",
     "Korelasyon (birlikte değişme) nedensellik değildir. Seçilen üç metalin aynı eğilimi göstermesi bir neden-sonuç "
     "ilişkisini kanıtlamaz; üstelik tablonun tamamı bu eğilimi desteklemiyor. Nikel, bakırla neredeyse aynı "
     "yoğunlukta olduğu hâlde çok daha az iletir.",
     "", "", [
         ("Geçersizdir; birlikte artmaları birinin diğerine neden olduğunu göstermez. Üstelik nikel bakırla neredeyse "
          "aynı yoğunlukta ama çok daha az iletiyor.", "evet", "", "", ""),
         ("Geçerlidir; üç örnekte de aynı eğilim görülüyor.", "", "kanitsiz", "K7",
          "Seçilmiş üç örnek bir eğilimi kanıtlamaya yetmez. Tablonun tamamına bakınca bu eğilime uymayan metaller "
          "görülüyor."),
         ("Geçerlidir; yoğun metallerde daha çok atom olduğu için daha çok elektron akar.", "", "iliski", "K7",
          "Bu açıklama kulağa mantıklı geliyor ama verilerle çelişiyor: tablodaki demir, kobalt ve nikel yoğun "
          "oldukları hâlde iletkenlikleri düşük."),
         ("Geçersizdir; çünkü yoğunluk ile iletkenliğin birimleri farklı olduğu için karşılaştırılamazlar.", "",
          "birim", "K7",
          "Birimleri farklı iki nicelik arasında da ilişki aranabilir. Sorun birimler değil, bir ilişkiden "
          "neden-sonuç çıkarılmasıdır."),
     ]),
    ("G11", "Gözlem", "", "coklu", "kullanim", "gozlem",
     "Elektrik kabloları dışında bakır ve alaşımları günlük hayatta nerelerde kullanılır? Doğru olanların hepsini seç.",
     "Bakırın kolay işlenmesi ve dayanıklılığı hangi yapı işlerinde işe yarar?",
     "RSC'ye göre bakır, elektrik donanımlarının yanı sıra çatı kaplaması ve su tesisatı gibi yapı işlerinde "
     "kullanılır. Madeni paraların birçoğu da bakır alaşımlarından yapılır.",
     "", "iliski", [
         ("Su tesisatı boruları", "evet", "", "", ""),
         ("Çatı kaplamaları", "evet", "", "", ""),
         ("Madeni paralar (bakır alaşımları)", "evet", "", "", ""),
         ("Uçak gövdeleri", "", "iliski", "K7",
          "Uçak gövdelerinde hafif metaller (örneğin alüminyum alaşımları) tercih edilir. Bakırın yoğunluğu "
          "alüminyumun üç katından fazla."),
         ("Termometrelerdeki parlak sıvı metal", "", "iliski", "K7",
          "Oda sıcaklığında sıvı olan metal cıvadır. Bakır ancak yaklaşık 1085 °C'de erir."),
     ]),
    ("G12", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
     "Musluk, kapı kolu ve bazı madeni paralarda saf bakır yerine çoğunlukla bakır alaşımları (örneğin bakır ve "
     "çinkodan oluşan pirinç) kullanılır. Bunun en olası bilimsel nedeni nedir?",
     "Sık dokunulan, sürekli kullanılan bir eşyadan hangi özellik beklenir?",
     "Saf metale başka bir element katılınca atomların düzenli dizilişi bozulur ve metal katmanlarının birbiri "
     "üzerinden kayması zorlaşır. Bu yüzden alaşımlar çoğu zaman saf metalden daha serttir. RSC'ye göre bakıra biraz "
     "kalay katılarak sertleştirilmesiyle elde edilen bronz, Tunç Çağı'na adını vermiştir.",
     "", "", [
         ("Alaşım saf bakırdan daha sert ve dayanıklıdır; sürekli kullanılan eşyalarda daha az aşınır.", "evet", "", "", ""),
         ("Alaşım elektriği saf bakırdan daha iyi iletir.", "", "iliski", "",
          "Alaşımlar genellikle elektriği saf metalden daha az iletir. Üstelik musluk ve kapı kolunda iletkenlik "
          "aranan bir özellik değildir."),
         ("Çinko eklenince metal mıknatısa çekilir hâle gelir, böylece eşyalar kolay tutturulur.", "", "kanitsiz", "",
          "Bu iddiayı destekleyen bir kanıt yok; pirinç mıknatısa çekilmez."),
         ("Alaşımın erime noktası saf bakırınkinden çok daha yüksektir.", "", "veri", "",
          "Pirincin erime noktası saf bakırınkinden düşüktür. Ayrıca musluk ve kapı kolunun erime noktasıyla ilgili "
          "bir ihtiyacı yoktur."),
     ]),
    ("G13", "Sonuç", "", "tekli", "sembol", "cikarim",
     "Bu metalin sembolü Cu. Türkçe adı 'bakır', İngilizce adı 'copper' olduğu hâlde sembolü neden 'B' ya da 'Co' "
     "değil? Arşiv notunu (K10) incele.",
     "Uluslararası semboller hangi dildeki adlardan gelir? Arşiv notunda geçen eski adı bul.",
     "Sembol, metalin Latince adı 'cuprum'dan gelir. Uluslararası semboller çoğu zaman elementin Latince adına "
     "dayanır: demir Fe (ferrum), gümüş Ag (argentum), altın Au (aurum), kurşun Pb (plumbum) gibi.",
     "", "", [
         ("Sembol, metalin Latince adı 'cuprum'dan gelir.", "evet", "", "", ""),
         ("Sembol, İngilizce adı 'copper'ın ilk iki harfinden gelir.", "", "veri", "K10",
          "'copper' kelimesinin ilk iki harfi 'Co' olurdu; bu da kobaltın sembolüdür. Arşiv notunu yeniden oku."),
         ("'B' sembolü bora ait olduğu için rastgele başka harfler seçilmiştir.", "", "kanitsiz", "K10",
          "Element sembolleri rastgele seçilmez; çoğu, elementin Latince ya da Yunanca adından gelir."),
         ("Sembol, bu metali ilk bulan bilim insanının adından gelir.", "", "kanitsiz", "K10",
          "Bakır tarih öncesi çağlardan beri kullanılıyor; onu ilk bulan bilinen bir bilim insanı yok."),
     ]),
    ("G14", "Sonuç", "", "tekli", "isim", "gozlem",
     "Latince 'Cyprium aes' ifadesi bu metalin adı hakkında bize ne anlatıyor?",
     "Arşiv notunda 'Cyprium aes' ifadesinin Türkçe karşılığı yazıyor.",
     "RSC'ye göre bakırın adı, 'Kıbrıs'tan gelen metal' anlamındaki Latince 'Cyprium aes' ifadesinden gelir; Antik "
     "Çağ'da Kıbrıs önemli bir bakır kaynağıydı. Bakır insanların işlediği ilk metaldir: Kuzey Irak'ta bulunan bakır "
     "boncuklar on bin yıldan daha eskidir.",
     "", "", [
         ("Antik Çağ'da bu metalin önemli bir kaynağı Kıbrıs adasıydı; metal adını oradan aldı.", "evet", "", "", ""),
         ("Latincede 'kırmızı metal' anlamına gelir; metal adını renginden alır.", "", "iliski", "K10",
          "Bakır kırmızımsı renkte olduğu için bu açıklama akla yatkın görünebilir, ama arşiv notunda renkten söz "
          "edilmiyor. K10'u yeniden oku."),
         ("Onu ilk işleyen Romalı ustanın adından gelir.", "", "kanitsiz", "K10",
          "Arşiv notunda bir kişi adından söz edilmiyor; bu iddiayı destekleyen kanıt yok."),
         ("'Kablo' anlamına gelen bir kelimeden gelir, çünkü en çok kablolarda kullanılır.", "", "iliski", "K10",
          "Bakırın adı, elektrik kablolarının icadından binlerce yıl önce verilmişti."),
     ]),
    ("G15", "Kanıt", "Kanıt", "kanit", "kanit", "kanit",
     "İddian: Tel bakırdır. Bu iddiayı destekleyen ve diğer adayları eleyen kanıtları seç. Tek başına ayırt edici "
     "olmayan kanıtları seçme.",
     "Her kanıt için sor: Bu kanıt aday sayısını azaltıyor mu?",
     "Ayırt edici kanıtlar şunlar: kısmi analiz raporu (K4) adayları 10 elemente, yoğunluk (K1) kobalt–nikel–bakır "
     "üçlüsüne, mıknatıs testi (K8) de bakıra indirdi. Tablo (K7) bu ölçümleri yorumlamamızı sağladı, renk (K9) "
     "sonucu destekledi. Elektrik ve ısı iletkenliği (K2, K3), sembolün iki harfli olması (K5) ve kablolarda "
     "kullanılması (K6) birçok metal için geçerli olduğundan tek başına ayırt edici değil.",
     "K1 K4 K8 (K7) (K9)", "kanitsiz", []),
    ("G16", "Çıkarım", "Gerekçe", "tekli", "gerekce", "gerekce",
     "Bu kanıtlar neden bakırı işaret ediyor? En güçlü gerekçeyi seç.",
     "Güçlü bir gerekçe, kanıtların adayları adım adım nasıl azalttığını gösterir.",
     "Güçlü bir gerekçe, kanıtların adayları nasıl tek bir sonuca indirdiğini adım adım gösterir: konum (10 aday) → "
     "yoğunluk (3 aday) → mıknatıs testi (1 aday).",
     "", "", [
         ("4. periyodun d bloğunda yoğunluğu ölçümle uyumlu üç metal var (kobalt, nikel, bakır); bunlardan mıknatısa "
          "çekilmeyen tek metal bakır.", "evet", "", "", ""),
         ("Elektriği iyi ilettiği ve kablolarda kullanıldığı için kesinlikle bakırdır.", "", "kanitsiz", "K6",
          "Elektriği iyi ileten ve kablolarda kullanılan başka metaller de var (örneğin alüminyum). Bu kanıtlar ayırt "
          "edici değil."),
         ("Yoğunluğu 8,96 g/cm³ olduğu için başka bir metal olamaz.", "", "birim", "K1",
          "Ölçülen yoğunluk 8,96 değil, 8,9 ± 0,1 g/cm³. Ölçümün belirsizliği içinde birden fazla metal var."),
         ("Sembolü iki harfli olduğu için bakırdır.", "", "kanitsiz", "K5",
          "Elementlerin çoğunun sembolü iki harflidir; bu kanıt neredeyse hiçbir adayı elemez."),
     ]),
    ("G17", "Çıkarım", "Karşı kanıt", "tekli", "alternatif", "hipotez",
     "Hangi alternatif hipotez en ciddi biçimde düşünülmeliydi ve neden reddedildi?",
     "Elemesi en zor olan aday hangisiydi?",
     "En ciddi alternatifler nikel ve kobalttı, çünkü yoğunlukları ölçümle uyumlu. Onları eleyen kanıt mıknatıs "
     "testidir. Güçlü bir argüman, en güçlü rakip hipotezi açıkça ele alır ve neden reddedildiğini gösterir.",
     "", "", [
         ("Nikel: yoğunluğu ölçümle uyumlu (8,90 g/cm³), ama mıknatısa çekilir; örnek ise çekilmedi.", "evet", "", "", ""),
         ("Alüminyum: kablolarda kullanılır, ama yoğunluğu 2,70 g/cm³ olduğu için hemen elenir.", "", "veri", "K7",
          "Bu ifade doğru, ama alüminyum ölçülen yoğunluktan çok uzak olduğu için en ciddi alternatif değildi. Soru, "
          "elenmesi en zor adayı soruyor."),
         ("Gümüş: elektriği bakırdan iyi iletir, bu yüzden tel gümüş olabilir.", "", "kanitsiz", "K4",
          "Gümüş 5. periyottadır; kısmi analiz raporu onu baştan eler. Daha iyi iletken olması bu teli gümüş yapmaz."),
         ("Kobalt: yoğunluğu ölçümle uyumludur ve mıknatısa çekilmez.", "", "veri", "K7",
          "Tabloya göre kobalt mıknatısa çekilir."),
     ]),
    ("G18", "Sonuç", "Sonuç", "savunma", "gerekce", "gerekce",
     "Bilimsel jüriye savunmanı yaz. \"Telin bakır olduğunu düşünüyorum çünkü…\" diye başla. İddianı, kanıtlarını, "
     "gerekçeni ve en güçlü alternatif hipotezi neden reddettiğini yaz.",
     "",
     "Telin bakır olduğunu düşünüyorum çünkü kısmi analiz raporu elementin 4. periyodun d bloğunda olduğunu "
     "gösteriyor; bu, adayları 10 elemente indiriyor. Ölçtüğümüz yoğunluk 8,9 ± 0,1 g/cm³ ve tabloya göre bu aralıkta "
     "yalnızca kobalt, nikel ve bakır var. Örnek mıknatısa çekilmedi; kobalt ve nikel mıknatısa çekildiği için "
     "elendi. Temizlenen yüzeyin kırmızımsı rengi de bakırla uyumlu. En ciddi alternatif nikeldi, çünkü yoğunluğu "
     "ölçümümüzle neredeyse aynı; ama mıknatıs testi onu eledi. Elektriği iyi iletmesi ve kablolarda kullanılması tek "
     "başına yeterli kanıt değildi, çünkü bu özellikler birçok metalde var.",
     "", "", []),
]


def yaz(dosya, sutunlar, satirlar):
    with open(HEDEF / dosya, "w", encoding="utf-8-sig", newline="") as f:
        yazici = csv.writer(f, delimiter=";", lineterminator="\r\n")
        yazici.writerow(sutunlar)
        for satir in satirlar:
            yazici.writerow(satir)


def main():
    HEDEF.mkdir(parents=True, exist_ok=True)
    d_sutun = ["id", "seviye", "sira", "baslik", "giris", "cevap", "final", "ornek", "kaynakca"]
    yaz("dosyalar.csv", d_sutun, [[d.get(s, "") for s in d_sutun] for d in DOSYALAR])
    yaz("kanitlar.csv", ["dosya", "id", "tur", "baslik", "metin", "goster", "kaynak"],
        [["D01", *k] for k in KANITLAR])
    yaz("tablolar.csv", ["dosya", "tablo", "h1", "h2", "h3", "h4", "h5", "h6"],
        [["D01", "T1", *satir] for satir in TABLO])
    yaz("gorevler.csv", ["dosya", "id", "asama", "arguman", "tur", "kategori", "beceri", "soru", "ipucu",
                         "aciklama", "dogru", "hata_turu"],
        [["D01", *g[:11]] for g in GOREVLER])
    secenekler = []
    for g in GOREVLER:
        for s in g[11]:
            secenekler.append(["D01", g[0], *s])
    yaz("secenekler.csv", ["dosya", "gorev", "metin", "dogru", "hata_turu", "hata_kaniti", "hata_aciklamasi"],
        secenekler)
    print("yazildi:", sorted(p.name for p in HEDEF.iterdir()), "| gorev:", len(GOREVLER),
          "| secenek:", len(secenekler))


if __name__ == "__main__":
    main()
