# -*- coding: utf-8 -*-
"""Element Dosyalari: Seviye 2 (Cikarim) dosyalari, D06-D10."""

from dosyalar_veri import D, G, RSC, S, Y, rsc

DOSYALAR = []

ALKALI_TABLO = [
    ["Metal", "Periyot", "Yoğunluk (g/cm³)", "Erime noktası (°C)", "Alev rengi"],
    ["Lityum", "2", "0,534", "180,5", "Kızıl"],
    ["Sodyum", "3", "0,97", "97,8", "Sarı-turuncu"],
    ["Potasyum", "4", "0,89", "63,5", "Leylak"],
    ["Rubidyum", "5", "1,53", "39,3", "Kırmızımsı mor"],
    ["Sezyum", "6", "1,87", "28,5", "Mavi-mor"],
]

DOSYALAR.append(dict(
    id="D06", seviye=2, sira=1, baslik="Yırtık Diş Macunu Etiketi", cevap="F",
    giris="Bir diş macunu tüpünün etiketi yırtılmış; yalnızca '...ür içerir' yazısı okunabiliyor. Üretici, macundaki "
          "etken maddenin bir elementin iyonu olduğunu söylüyor. Birimin elinde bu elementle ilgili bir laboratuvar "
          "dosyası var. Görevin: elementi bulmak ve macunda neden saf hâlde değil de bileşik olarak bulunduğunu açıklamak.",
    kaynakca=[rsc(9, "fluorine", "Flor"), rsc(17, "chlorine", "Klor"), rsc(35, "bromine", "Brom"),
              rsc(53, "iodine", "İyot")],
    kanitlar=[
        ("K1", "konum", "Laboratuvar raporu", "Element periyodik tablonun 17. grubunda (halojenler) yer alıyor.", "", ""),
        ("K2", "fiziksel", "Saf hâlinin görünüşü", "Saf hâli oda sıcaklığında çok soluk sarı-yeşil bir gazdır.", "", ""),
        ("K3", "elektron_dizilimi", "Elektron dizilimi", "1s² 2s² 2p⁵", "", ""),
        ("K4", "reaktivite", "Tepkime notu",
         "Saf hâli bilinen en tepkimeye yatkın elementtir: bütün metallere hızla saldırır, çelik yünü bu gazla "
         "karşılaşınca alev alır.", "", RSC + "9/fluorine"),
        ("K5", "iyon", "İyon notu",
         "Bileşiklerinde bir elektron alarak −1 yüklü iyon oluşturur. Türkçede bu tür iyonlar elementin adına '-ür' "
         "eki getirilerek adlandırılır (örneğin klor → klorür).", "", ""),
        ("K6", "tablo", "17. grup elementleri", "T1", "", "RSC Periyodik Tablo"),
        ("K7", "isim", "Arşiv notu",
         "Bu elementin adı Latincede 'akmak' anlamına gelen 'fluere' kelimesinden gelir. Elementi içeren florit "
         "minerali, metal eritmede erimeyi kolaylaştırmak için kullanılıyordu. Element 1886'da Henri Moissan "
         "tarafından elde edildi; ondan önce elde etmeye çalışan Humphry Davy denemeleri sırasında hastalandı.",
         "G4", RSC + "9/fluorine"),
    ],
    tablolar={"T1": [
        ["Element", "Periyot", "Oda sıcaklığındaki hâli", "Görünüşü"],
        ["Flor", "2", "Gaz", "Çok soluk sarı-yeşil"],
        ["Klor", "3", "Gaz", "Sarı-yeşil, boğucu kokulu"],
        ["Brom", "4", "Sıvı", "Koyu kırmızı, yağımsı"],
        ["İyot", "5", "Katı", "Siyah, parlak kristaller"],
    ]},
    gorevler=[
        G("G1", "Veri", "", "tablo", "kanit", "veri",
          "Laboratuvar raporuna (K1) göre aday olabilecek bütün elementleri periyodik tabloda işaretle.",
          "17. grubun bütün elementlerini, yedinci periyoda kadar işaretle.",
          "17. grupta altı element var: flor, klor, brom, iyot, astatin ve tennesin. Astatin ve tennesin radyoaktiftir; "
          "çok az miktarda bulunur ya da laboratuvarda üretilir.",
          dogru="F Cl Br I At Ts", hata_turu="veri"),
        G("G2", "Veri", "", "coklu", "kanit", "veri",
          "Saf hâlin oda sıcaklığında gaz olması (K2), tablodaki (K6) hangi adayları eler? Elenenlerin hepsini seç.",
          "Tablonun 'hâli' sütununa bak.",
          "Tabloya göre brom sıvı, iyot katıdır; ikisi de elenir. Flor ve klor gazdır; bu kanıt onları birbirinden ayırmaz.",
          hata_turu="veri", secenekler=[
              D("Brom"), D("İyot"),
              Y("Flor", "veri", "K6", "Flor gazdır; gaz olma kanıtı onu elemez."),
              Y("Klor", "veri", "K6", "Klor gazdır; gaz olma kanıtı onu elemez."),
          ]),
        G("G3", "Çıkarım", "", "tekli", "kanit", "cikarim",
          "Elektron dizilimi (K3) flor ile kloru nasıl ayırır?",
          "Dizilimdeki en büyük katman numarası periyodu gösterir.",
          "1s² 2s² 2p⁵ diziliminde toplam 9 elektron var: atom numarası 9. En dış katman 2. katman olduğu için element "
          "2. periyotta; bu katmanda 7 elektron olduğu için de 17. grupta. 2. periyottaki halojen flordur.",
          secenekler=[
              D("En dış elektronlar 2. katmanda (2s² 2p⁵); yani element 2. periyotta. 2. periyottaki halojen flordur."),
              Y("Dizilimdeki 7 elektron elementin 7. periyotta olduğunu gösterir.", "veri", "K3",
                "Son katmandaki elektron sayısı grubu, katman numarası periyodu gösterir; buradaki son katman 2. katman."),
              Y("Dizilim iki elementte de aynıdır; onları ayırmaz.", "veri", "K3",
                "Klorun dizilimi 1s² 2s² 2p⁶ 3s² 3p⁵'tir; üçüncü katmanda biter."),
              Y("Toplam 9 elektron olduğu için element 9. gruptadır.", "iliski", "K3",
                "Toplam elektron sayısı atom numarasını verir; grubu en dış katmandaki elektronlar belirler."),
          ]),
        G("G4", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Element hangisi? Adını ya da sembolünü yaz.",
          "17. grup ve 2. periyot...",
          "Element flordur (F): 17. grupta (K1), saf hâli gaz (K2) ve elektron dizilimi 2. periyodu gösteriyor (K3). "
          "Etiketteki silinmiş kelime 'florür'dü.",
          hata_turu="kanitsiz"),
        G("G5", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Diş macununda saf flor değil de florür iyonu içeren bileşikler kullanılır. Bunun nedeni nedir?",
          "Saf florun tepkime notunu (K4) ve iyon notunu (K5) karşılaştır.",
          "RSC'ye göre flor bütün elementler içinde en tepkimeye yatkın olanıdır ve bütün metallere hızla saldırır. "
          "Flor bir elektron alıp florür iyonuna (F⁻) dönüşünce kararlı hâle gelir. Diş macunlarında sodyum florür gibi "
          "bileşikler bulunur; florür diş minesini asitlere karşı daha dayanıklı yapar.",
          secenekler=[
              D("Saf flor bilinen en tepkimeye yatkın ve tehlikeli elementtir; bileşiklerindeki florür iyonu ise "
                "kararlıdır ve diş minesini güçlendirir."),
              Y("Saf flor gaz olduğu için tüpe sığmaz.", "iliski", "K2",
                "Gazlar sıkıştırılarak kaplarda saklanabilir; asıl sorun florun aşırı tepkimeye yatkın olması."),
              Y("Florür iyonu flor atomundan daha tepkimeye yatkındır.", "veri", "K5",
                "Florür iyonu elektron alarak kararlı hâle gelmiştir; saf flor çok daha tepkimeye yatkındır."),
              Y("Saf flor dişleri beyazlatır ama tadı kötüdür.", "kanitsiz", "K4",
                "Bu iddiayı destekleyen bir kanıt yok; saf flor çok tehlikeli bir gazdır."),
          ]),
        G("G6", "Sonuç", "", "coklu", "kullanim", "gozlem",
          "Flor ve bileşiklerinin günlük hayattaki kullanımları hangileri? Doğru olanların hepsini seç.",
          "Yapışmaz tavaların kaplamasını düşün.",
          "RSC'ye göre flor, yapışmaz tavalarda kullanılan teflon gibi plastiklerin ve su geçirmez kumaşların yapımında "
          "kullanılır. Florür bileşikleri diş macunlarına eklenir.",
          hata_turu="iliski", secenekler=[
              D("Yapışmaz tava kaplaması"),
              D("Diş macunu"),
              D("Su geçirmez giysi kumaşları"),
              Y("Süs balonlarını doldurmak", "iliski", "K4",
                "Balonlarda helyum kullanılır; flor zehirli ve aşırı tepkimeye yatkın bir gazdır."),
              Y("Kurşun kalem ucu", "iliski", "K2", "Kalem ucunda grafit (karbon) vardır."),
          ]),
        G("G7", "Sonuç", "", "tekli", "isim", "gozlem",
          "Arşiv notuna (K7) göre florun adı nereden gelir?",
          "Notta bir Latince fiil geçiyor.",
          "RSC'ye göre flor adı Latince 'fluere' (akmak) kelimesinden gelir: florit minerali, metal eritmede erimeyi "
          "kolaylaştırıyordu. 'Floresan' kelimesi de florit mineralinden türetilmiştir.",
          secenekler=[
              D("Latincede 'akmak' anlamına gelen 'fluere' kelimesinden; florit minerali metal eritmede kullanılıyordu."),
              Y("Işık saçan 'floresan' lambalardan", "iliski", "K7",
                "Tersine: 'floresan' kelimesi florit mineralinden türetilmiştir. Element adını lambalardan almadı."),
              Y("Onu elde eden Moissan'ın memleketinden", "kanitsiz", "K7", "Arşiv notunda böyle bir bilgi yok."),
              Y("Latincede 'sarı' anlamına gelen bir kelimeden", "iliski", "K2",
                "Flor soluk sarı-yeşil bir gaz olduğu için bu açıklama akla yatkın görünebilir, ama arşiv notunda böyle "
                "yazmıyor."),
          ]),
        G("G8", "Kanıt", "Kanıt", "kanit", "kanit", "kanit",
          "İddian: Macundaki etken maddenin elementi flordur. Adayları tek bir elemente indiren kanıtları seç. Tek "
          "başına ayırt edici olmayan kanıtları seçme.",
          "Hangi iki kanıt birlikte tek bir hücreyi gösteriyor?",
          "17. grup (K1) ve 2. periyot (K3) birlikte tek bir element gösterir: flor. Saf hâlinin gaz olması (K2) ve 'en "
          "tepkimeye yatkın element' olması (K4) bu sonucu destekler. −1 yüklü iyon oluşturmak (K5) bütün halojenlerde "
          "görülür; ayırt edici değildir.",
          dogru="K1 K3 (K2) (K4) (K6)", hata_turu="kanitsiz"),
    ]))

DOSYALAR.append(dict(
    id="D07", seviye=2, sira=2, baslik="Havai Fişek Gecesi", cevap="Sr",
    giris="Bir kutlamada atılan havai fişeklerden biri gökyüzünde parlak kızıl bir ışık saçtı. Patlamayan bir fişeğin "
          "içindeki tuz birime getirildi. Görevin: kızıl rengi veren metali bulmak.",
    kaynakca=[rsc(38, "strontium", "Stronsiyum"), rsc(3, "lithium", "Lityum"), rsc(20, "calcium", "Kalsiyum"),
              rsc(56, "barium", "Baryum"), rsc(37, "rubidium", "Rubidyum")],
    kanitlar=[
        ("K1", "deney", "Alev testi", "Tuzdan bir tutam alevin üzerine serpilince alev parlak kızıl renge döndü.", "", ""),
        ("K2", "tablo", "Alev testinde bazı metallerin renkleri", "T1", "", "Standart alev testi renkleri"),
        ("K3", "konum", "Elementel analiz", "Metal, periyodik tablonun 2. grubunda (toprak alkali metaller) yer alıyor.",
         "G2", ""),
        ("K4", "yogunluk", "Saf metalin yoğunluğu", "Tuzdan elde edilen saf metalin yoğunluğu 2,6 ± 0,1 g/cm³.", "G2", ""),
        ("K5", "kimyasal", "Saf metalin davranışı", "Saf metal havada kolayca yanıyor ve suyla tepkimeye giriyor.", "", ""),
        ("K6", "isim", "Arşiv notu",
         "Bu element, 1787'de İskoçya'daki küçük Strontian kasabası yakınındaki bir kurşun madeninde bulunan bir "
         "mineralden adını aldı. 1791'de Thomas Charles Hope, bu mineralin bir mumun alevini kırmızı yaktığını not etti.",
         "G4", RSC + "38/strontium"),
        ("K7", "kullanim", "RSC kaydı",
         "Bu elementin bileşikleri karanlıkta parlayan boya ve plastiklerde de kullanılır: gün boyunca ışığı soğurur, "
         "saatlerce yavaşça geri verirler.", "G4", RSC + "38/strontium"),
    ],
    tablolar={"T1": [
        ["Metal", "Grup", "Periyot", "Alev rengi"],
        ["Lityum", "1", "2", "Kızıl"],
        ["Sodyum", "1", "3", "Sarı-turuncu"],
        ["Potasyum", "1", "4", "Leylak"],
        ["Kalsiyum", "2", "4", "Turuncu-kırmızı (tuğla kırmızısı)"],
        ["Stronsiyum", "2", "5", "Kızıl"],
        ["Baryum", "2", "6", "Yeşil"],
        ["Bakır", "11", "4", "Mavi-yeşil"],
    ]},
    gorevler=[
        G("G1", "Gözlem", "", "coklu", "kanit", "veri",
          "Alev testine (K1) ve tabloya (K2) göre hangi metaller kızıl alev verir? Hepsini seç.",
          "Tablonun 'Alev rengi' sütununda 'Kızıl' yazan satırları bul.",
          "Tabloya göre lityum ve stronsiyumun ikisi de kızıl alev verir. Alev testi adayları ikiye indirdi, ama tek "
          "başına kesin bir sonuç vermiyor.",
          hata_turu="veri", secenekler=[
              D("Lityum"), D("Stronsiyum"),
              Y("Kalsiyum", "veri", "K2", "Kalsiyumun alevi turuncu-kırmızıdır (tuğla kırmızısı), kızıl değildir."),
              Y("Baryum", "veri", "K2", "Baryum yeşil alev verir."),
              Y("Sodyum", "veri", "K2", "Sodyum sarı-turuncu alev verir."),
          ]),
        G("G2", "Hipotez", "", "tekli", "alternatif", "hipotez",
          "Adaylar lityum ve stronsiyum. Bu iki hipotezi ayırmak için hangi bilgi en işe yarar?",
          "İki aday tabloda hangi sütunda farklılaşıyor?",
          "Lityum 1. grupta, stronsiyum 2. grupta. Metalin hangi grupta olduğunu gösteren bir analiz, iki hipotezden birini "
          "kesin olarak eler. Yeni kanıtlar açıldı: elementel analiz (K3) ve yoğunluk (K4).",
          secenekler=[
              D("Metalin periyodik tablodaki grubunu gösteren bir elementel analiz"),
              Y("Alev testini bir kez daha yapmak", "veri", "K2",
                "İki aday da kızıl alev verir; testi yinelemek onları ayırmaz."),
              Y("Tuzun suda çözünüp çözünmediğine bakmak", "kanitsiz", "",
                "Bu konuda bir kanıt yok; ayrıca birçok tuz suda çözünür."),
              Y("Fişeğin patlama sesinin şiddetini ölçmek", "iliski", "K1",
                "Patlama sesi fişeğin barutuna bağlıdır; rengi veren metal hakkında bilgi vermez."),
          ]),
        G("G3", "Veri", "", "tekli", "kanit", "veri",
          "Analize (K3) ve yoğunluğa (K4) göre ne söylenebilir? (Kalsiyum 1,54; stronsiyum 2,64; baryum 3,62; lityum "
          "0,534 g/cm³)",
          "2,6 ± 0,1 aralığına hangi değer giriyor?",
          "Metal 2. grupta olduğu için lityum (1. grup) elenir. Yoğunluk 2,6 ± 0,1 g/cm³ ise 2. grup metallerinden yalnızca "
          "stronsiyumla (2,64) uyumlu.",
          secenekler=[
              D("Metal 2. grupta olduğu için lityum elenir; yoğunluk da yalnızca stronsiyumla uyumlu."),
              Y("Yoğunluk baryumla da uyumlu.", "veri", "K4", "3,62, ölçüm aralığının (2,5–2,7) dışında."),
              Y("2. gruptaki bütün metallerin yoğunluğu aynıdır.", "veri", "K4",
                "Verilen değerler 1,54 ile 3,62 arasında değişiyor."),
              Y("Karar verilemez; yoğunluk g/cm³ ile değil gram ile ölçülür.", "birim", "K4",
                "Gram kütle birimidir; yoğunluğun birimi g/cm³'tür."),
          ]),
        G("G4", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Fişeğe kızıl rengi veren metal hangisi? Adını ya da sembolünü yaz.",
          "Kızıl alev veren, 2. gruptaki metal...",
          "Metal stronsiyumdur (Sr): kızıl alev veriyor, 2. grupta ve yoğunluğu stronsiyumla uyuşuyor.",
          hata_turu="kanitsiz"),
        G("G5", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Havai fişeklerde farklı renkler nasıl elde edilir?",
          "Tablodaki her metalin alev rengi neden farklı?",
          "Alevde metal atomları ısıyla enerji kazanır ve bu enerjiyi belirli renklerde ışık olarak geri verir. RSC'ye "
          "göre stronsiyum, tuzlarının havai fişeklere ve işaret fişeklerine verdiği parlak kırmızı renkle bilinir. Yeşil "
          "için baryum, mavi-yeşil için bakır tuzları kullanılabilir.",
          secenekler=[
              D("Her metal ısıtılınca kendine özgü renklerde ışık yayar; fişeklere farklı metallerin tuzları konarak "
                "farklı renkler elde edilir."),
              Y("Fişeklere boya katılır; boyanın rengi alevde görünür.", "iliski", "K2",
                "Renk boyadan değil, metal atomlarının yaydığı ışıktan gelir; tablo her metalin kendi rengini gösteriyor."),
              Y("Renk, fişeğin ne kadar yükseğe çıktığına bağlıdır.", "kanitsiz", "",
                "Bu iddiayı destekleyen bir kanıt yok."),
              Y("Bütün metaller aynı rengi verir; renk farkı sıcaklıktan gelir.", "veri", "K2",
                "Tablo, farklı metallerin farklı renkler verdiğini gösteriyor."),
          ]),
        G("G6", "Sonuç", "", "tekli", "isim", "gozlem",
          "Stronsiyum adını nereden alır? (K6)",
          "Notta bir yer adı geçiyor.",
          "RSC'ye göre stronsiyum, adını İskoçya'daki küçük Strontian kasabasından alır. Adını kırmızı renkten alan "
          "element ise rubidyumdur (Latince 'rubidius': en koyu kırmızı).",
          secenekler=[
              D("İskoçya'daki Strontian kasabası yakınındaki bir madende bulunan mineralden"),
              Y("İngilizce 'strong' (güçlü) kelimesinden; patlayıcı olduğu için", "iliski", "K6",
                "Element adını bir yer adından alır; patlayıcılıkla ilgisi yok."),
              Y("Onu bulan kimyagerin adından", "kanitsiz", "K6", "Arşiv notunda bir yer adından söz ediliyor."),
              Y("Latincede 'kırmızı' anlamına gelen bir kelimeden", "iliski", "K6",
                "Kırmızı alev verdiği için akla yatkın görünebilir, ama arşiv notunda bir yer adından söz ediliyor."),
          ]),
        G("G7", "Çıkarım", "Gerekçe", "tekli", "gerekce", "gerekce",
          "İddian: Fişekteki metal stronsiyumdur. En güçlü gerekçe hangisi?",
          "Güçlü gerekçe, her adımda hangi adayın neden elendiğini gösterir.",
          "Güçlü bir gerekçe kanıtları birleştirir: alev testi adayları ikiye indirdi, analiz grubu belirledi, yoğunluk da "
          "sonucu doğruladı.",
          secenekler=[
              D("Alev testi adayları kızıl alev veren lityum ve stronsiyuma indirdi; analiz metalin 2. grupta olduğunu "
                "gösterdi ve yoğunluk da stronsiyumla uyuşuyor."),
              Y("Havai fişeklerde hep stronsiyum kullanıldığı için.", "kanitsiz", "",
                "Genel bir bilgi bu örneğin kanıtı olamaz; fişeklerde başka metaller de kullanılır."),
              Y("Kızıl alev verdiği için.", "kanitsiz", "K1", "Lityum da kızıl alev verir; bu kanıt tek başına yetmez."),
              Y("2. grupta olduğu için.", "kanitsiz", "K3", "2. grupta altı element var."),
          ]),
        G("G8", "Çıkarım", "Karşı kanıt", "tekli", "alternatif", "hipotez",
          "En ciddi alternatif hipotez hangisiydi ve neden reddedildi?",
          "Hangi aday ilk testi de geçmişti?",
          "Lityum en ciddi alternatifti: o da kızıl alev verir. Ama 1. gruptadır ve yoğunluğu (0,534 g/cm³) ölçümle "
          "uyuşmaz. Güçlü bir argüman en güçlü rakibi açıkça ele alır.",
          secenekler=[
              D("Lityum: o da kızıl alev verir, ama 1. gruptadır ve yoğunluğu (0,534 g/cm³) ölçümle uyuşmaz."),
              Y("Baryum: o da 2. gruptadır, ama alevi yeşildir.", "veri", "K2",
                "Bu doğru bir ifade, ama baryum alev testiyle hemen elendi; en ciddi alternatif değildi."),
              Y("Kalsiyum: alevi stronsiyumunkiyle aynıdır.", "veri", "K2",
                "Tabloya göre kalsiyumun alevi turuncu-kırmızıdır; kızıl değildir."),
              Y("Sodyum: en parlak alevi verir.", "iliski", "K2",
                "Alevin parlaklığı değil rengi önemli; sodyumun alevi sarı-turuncudur."),
          ]),
    ]))

DOSYALAR.append(dict(
    id="D08", seviye=2, sira=3, baslik="Kemik ve Alçı", cevap="Ca",
    giris="Kolu kırılan bir öğrencinin röntgeninde kemikler beyaz görünüyor; kolu alçıya alınmış. Doktor 'kemiğinin ve "
          "alçının ortak bir elementi var' diyor. Görevin: bu elementi bulmak.",
    kaynakca=[rsc(20, "calcium", "Kalsiyum"), rsc(4, "beryllium", "Berilyum"), rsc(12, "magnesium", "Magnezyum"),
              rsc(38, "strontium", "Stronsiyum"), rsc(56, "barium", "Baryum"), rsc(88, "radium", "Radyum")],
    kanitlar=[
        ("K1", "konum", "Analiz raporu", "Element periyodik tablonun 2. grubunda (toprak alkali metaller).", "", ""),
        ("K2", "kimyasal", "Saf metalin davranışı",
         "Saf metal gümüşi beyaz ve yumuşak; havada hızla matlaşıyor, suya atılınca yavaşça gaz çıkararak tepkimeye "
         "giriyor.", "", ""),
        ("K3", "yogunluk", "Yoğunluk ölçümü", "Saf metalin yoğunluğu 1,5 ± 0,1 g/cm³.", "", ""),
        ("K4", "tablo", "2. grup metalleri", "T1", "", "RSC Periyodik Tablo"),
        ("K5", "deney", "Kemik deneyi",
         "Bir tavuk kemiği birkaç gün sirkede bekletilince lastik gibi bükülebilir hâle geldi. Sirkede çözünen mineral, "
         "aranan elementi içeriyor.", "", ""),
        ("K6", "kullanim", "Yapı malzemeleri",
         "Kireçtaşı, mermer ve alçı (kalsiyum sülfat) bu elementin bileşiklerini içerir. RSC'ye göre alçı, kırık "
         "kemikleri sabitlemek için de kullanılır.", "G4", RSC + "20/calcium"),
        ("K7", "isim", "Arşiv notu",
         "Bu elementin adı Latincede 'kireç' anlamına gelen 'calx' kelimesinden gelir. Element ilk kez 1808'de Humphry "
         "Davy tarafından elde edildi: Davy kireci cıva oksitle karıştırıp elektrik akımı verdi, oluşan alaşımdan "
         "cıvayı damıtarak ayırdı.", "G4", RSC + "20/calcium"),
    ],
    tablolar={"T1": [
        ["Metal", "Periyot", "Yoğunluk (g/cm³)", "Erime noktası (°C)"],
        ["Berilyum", "2", "1,85", "1287"],
        ["Magnezyum", "3", "1,74", "650"],
        ["Kalsiyum", "4", "1,54", "842"],
        ["Stronsiyum", "5", "2,64", "777"],
        ["Baryum", "6", "3,62", "727"],
        ["Radyum", "7", "5", "696"],
    ]},
    gorevler=[
        G("G1", "Gözlem", "", "tekli", "kanit", "gozlem",
          "Kemiğin röntgende beyaz görünmesi ve alçının da beyaz olması 'ikisi aynı elementi içerir' iddiasını kanıtlar mı?",
          "Aynı renkte olan iki madde aynı elementleri mi içerir?",
          "Kemiklerin röntgende beyaz görünmesinin nedeni, X ışınlarını yumuşak dokulardan daha çok soğurmalarıdır. "
          "Bu bir ipucu olabilir ama tek başına kanıt değildir; alçının renginin ise bununla hiçbir ilgisi yoktur. "
          "Kimyasal analiz gerekir.",
          secenekler=[
              D("Hayır; renk benzerliği ortak bir element içerdiklerini göstermez. Kimyasal analiz gerekir."),
              Y("Evet; beyaz olan bütün maddeler aynı elementi içerir.", "iliski", "",
                "Tuz, şeker ve kâğıt da beyazdır ama farklı elementlerden oluşur."),
              Y("Evet; röntgen her zaman hangi element olduğunu gösterir.", "kanitsiz", "",
                "Röntgen yalnızca X ışınlarının ne kadar soğurulduğunu gösterir; elementin adını söylemez."),
              Y("Hayır; kemikte hiçbir element yoktur.", "veri", "K5",
                "Kemik deneyi kemikte asitte çözünen bir mineral olduğunu gösteriyor."),
          ]),
        G("G2", "Veri", "", "tablo", "kanit", "veri",
          "Analiz raporuna (K1) göre adayları periyodik tabloda işaretle.",
          "2. grubun bütün elementlerini, yedinci periyoda kadar işaretle.",
          "2. grupta altı element var: berilyum, magnezyum, kalsiyum, stronsiyum, baryum ve radyum.",
          dogru="Be Mg Ca Sr Ba Ra", hata_turu="veri"),
        G("G3", "Veri", "", "tekli", "kanit", "veri",
          "Ölçülen yoğunluk 1,5 ± 0,1 g/cm³ (K3). Tabloya (K4) göre hangi aday uyumlu?",
          "1,4 ile 1,6 arasına hangi değer giriyor?",
          "Ölçüm 1,4–1,6 g/cm³ aralığıyla uyumlu. Tablodaki adaylardan yalnızca kalsiyum (1,54) bu aralıkta. Magnezyum "
          "(1,74) ve berilyum (1,85) yakın ama aralığın dışında.",
          secenekler=[
              D("Yalnızca kalsiyum (1,54 g/cm³)"),
              Y("Magnezyum (1,74 g/cm³); en yakın değer o", "veri", "K3",
                "1,74, 1,4–1,6 aralığının dışında; aralıktaki tek değer kalsiyumunki (1,54)."),
              Y("Berilyum (1,85 g/cm³)", "veri", "K3", "1,85, ölçüm aralığının dışında."),
              Y("Hiçbiri; metallerin yoğunluğu 2 g/cm³'ten küçük olamaz.", "iliski", "K4",
                "Tabloda yoğunluğu 2 g/cm³'ten küçük üç metal var; lityum gibi bazı metaller sudan bile hafiftir."),
          ]),
        G("G4", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Kemiğin ve alçının ortak elementi hangisi? Adını ya da sembolünü yaz.",
          "2. grupta, yoğunluğu 1,54 g/cm³ olan metal...",
          "Element kalsiyumdur (Ca): 2. grupta, yoğunluğu ölçümle uyuşuyor ve suyla tepkimesi kalsiyuma uyuyor.",
          hata_turu="kanitsiz"),
        G("G5", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Sirkede bekletilen kemiğin bükülebilir hâle gelmesi (K5) kemiğin yapısı hakkında ne söyler?",
          "Sirke asittir. Asit kemikten neyi çözmüş olabilir?",
          "Kemiğin sertliği kalsiyum ve fosfat içeren bir mineralden (hidroksiapatit) gelir. Sirkedeki asit bu minerali "
          "çözer; geriye esnek bir protein olan kolajen kalır ve kemik bükülebilir.",
          secenekler=[
              D("Kemiğin sertliği kalsiyum içeren bir mineralden gelir; asit bu minerali çözünce geriye esnek kısım kalır."),
              Y("Sirke kemiğe kalsiyum ekleyerek onu yumuşatır.", "iliski", "K5",
                "Sirke kemiğe bir şey eklemedi; kemikteki minerali çözdü."),
              Y("Kemik sirkeyi emip şişer, bu yüzden bükülür.", "kanitsiz", "K5",
                "Kemiğin şiştiğini gösteren bir kanıt yok; kanıt bir mineralin çözündüğünü söylüyor."),
              Y("Kemikte hiç mineral yoktur; bükülmek kemiğin doğal hâlidir.", "veri", "K5",
                "Deneyden önce kemik serttir; bükülebilir hâle gelmesi bir şeyin çözüldüğünü gösteriyor."),
          ]),
        G("G6", "Sonuç", "", "coklu", "kullanim", "gozlem",
          "Kalsiyum bileşikleri günlük hayatta nerelerde bulunur? Doğru olanların hepsini seç.",
          "Yapı malzemeleri kaydına (K6) bak.",
          "RSC'ye göre kireçtaşı (kalsiyum karbonat) yapı taşı olarak ve çimento yapımında kullanılır; alçı (kalsiyum "
          "sülfat) hem inşaatta hem de kırık kemiklerin sabitlenmesinde kullanılır.",
          hata_turu="iliski", secenekler=[
              D("Kireçtaşı ve mermer"),
              D("Çimento ve harç"),
              D("Kırık kemikler için alçı"),
              Y("Uçan balonları doldurmak", "iliski", "K2",
                "Kalsiyum katı bir metaldir; balonlarda helyum gibi havadan hafif gazlar kullanılır."),
              Y("Termometre sıvısı", "iliski", "K4",
                "Kalsiyum 842 °C'de erir; oda sıcaklığında sıvı olan metal cıvadır."),
          ]),
        G("G7", "Sonuç", "", "tekli", "isim", "gozlem",
          "Kalsiyumun adı nereden gelir? (K7)",
          "Notta Latince bir kelime geçiyor.",
          "RSC'ye göre kalsiyumun adı Latince 'kireç' anlamındaki 'calx' kelimesinden gelir. Kireç (kalsiyum oksit), "
          "kireçtaşı ısıtılarak elde edilir ve yüzyıllardır sıva ve harç yapımında kullanılır.",
          secenekler=[
              D("Latincede 'kireç' anlamına gelen 'calx' kelimesinden"),
              Y("Onu elde eden Davy'nin memleketinden", "kanitsiz", "K7", "Arşiv notunda böyle bir bilgi yok."),
              Y("'Kalori' kelimesinden; vücuda enerji verdiği için", "iliski", "K7",
                "Kalsiyum besinlerde enerji kaynağı değildir; ad 'kireç' anlamındaki 'calx'tan gelir."),
              Y("Kemik anlamına gelen Yunanca bir kelimeden", "iliski", "K7",
                "Kalsiyum kemikte bulunduğu için akla yatkın görünebilir, ama notta böyle yazmıyor."),
          ]),
        G("G8", "Çıkarım", "Karşı kanıt", "tekli", "alternatif", "hipotez",
          "Kemikte fosfor da bulunur. 'Kemiğin ve alçının ortak elementi fosfordur' hipotezi neden reddedilir?",
          "Fosfor periyodik tablonun neresinde? Alçının formülünü düşün.",
          "Fosfor 15. gruptadır, analiz ise 2. grubu gösteriyor. Ayrıca alçı (kalsiyum sülfat) fosfor içermez. Kemik "
          "mineralinde fosfor vardır ama kemik ile alçının ortak elementi kalsiyumdur.",
          secenekler=[
              D("Fosfor 2. grupta değil 15. gruptadır; ayrıca alçı (kalsiyum sülfat) fosfor içermez."),
              Y("Fosfor kemikte hiç bulunmaz.", "veri", "K5",
                "Kemik minerali kalsiyum fosfattır; fosfor içerir. Hipotezin reddedilme nedeni bu değil."),
              Y("Fosfor bir gazdır.", "veri", "",
                "Fosfor oda sıcaklığında katıdır."),
              Y("Fosfor kemikte bulunduğu için hipotez reddedilemez.", "kanitsiz", "K1",
                "Bir elementin kemikte bulunması, alçıda da bulunduğunu göstermez; analiz de 2. grubu gösteriyor."),
          ]),
    ]))

DOSYALAR.append(dict(
    id="D09", seviye=2, sira=4, baslik="Şişen Batarya", cevap="Li",
    giris="Bir öğrencinin eski telefonunun bataryası şişmiş. Bataryanın etiketinde '...-iyon' yazıyor; ilk kelime "
          "silinmiş. Birim, bataryadaki elementi araştırıyor. Uyarı: şişmiş bataryalar delinmemeli, ezilmemeli ve "
          "ısıtılmamalıdır.",
    kaynakca=[rsc(3, "lithium", "Lityum"), rsc(11, "sodium", "Sodyum"), rsc(19, "potassium", "Potasyum"),
              rsc(37, "rubidium", "Rubidyum"), rsc(55, "caesium", "Sezyum"), rsc(38, "strontium", "Stronsiyum")],
    kanitlar=[
        ("K1", "konum", "Analiz raporu", "Element periyodik tablonun 1. grubunda; bir alkali metal.", "", ""),
        ("K2", "yogunluk", "Yoğunluk ölçümü", "Saf metalin yoğunluğu 0,53 ± 0,02 g/cm³.", "", ""),
        ("K3", "deney", "Alev testi", "Bileşikleri alevi kızıl renge boyuyor.", "", ""),
        ("K4", "tablo", "1. grup (alkali) metalleri", "T1", "", "RSC Periyodik Tablo; standart alev testi renkleri"),
        ("K5", "kimyasal", "Suyla tepkime",
         "Saf metal suyla tepkimeye girerek hidrojen gazı çıkarıyor, ama sodyum ve potasyuma göre daha sakin.", "", ""),
        ("K6", "kullanim", "RSC kaydı",
         "Bu metalin en önemli kullanımı telefon, dizüstü bilgisayar, fotoğraf makinesi ve elektrikli araçlardaki şarj "
         "edilebilir pillerdir. Bütün metaller içinde yoğunluğu en düşük olanıdır.", "G5", RSC + "3/lithium"),
        ("K7", "isim", "Arşiv notu",
         "Adı Yunanca 'taş' anlamına gelen 'lithos' kelimesinden gelir. Diğer yaygın alkali metaller bitki küllerinden "
         "bulunurken bu metal bir mineralden (petalit) bulundu. 1817'de Johan August Arfvedson tarafından keşfedildi.",
         "G5", RSC + "3/lithium"),
    ],
    tablolar={"T1": [row for row in ALKALI_TABLO]},
    gorevler=[
        G("G1", "Veri", "", "tablo", "kanit", "veri",
          "Analiz raporuna (K1) göre aday olabilecek bütün alkali metalleri periyodik tabloda işaretle.",
          "Hidrojen 1. grupta gösterilir ama bir metal değildir.",
          "Alkali metaller lityum, sodyum, potasyum, rubidyum, sezyum ve fransiyumdur. Hidrojen 1. grupta gösterilir "
          "ama metal değildir.",
          dogru="Li Na K Rb Cs Fr", hata_turu="veri"),
        G("G2", "Veri", "", "tekli", "kanit", "veri",
          "Yoğunluk ölçümü (K2) tablodaki (K4) hangi adayı gösteriyor?",
          "0,51 ile 0,55 arasına hangi değer giriyor?",
          "Ölçülen 0,53 ± 0,02 g/cm³ yalnızca lityumla (0,534) uyumlu. Lityum bütün metallerin en hafifidir; sudan bile "
          "neredeyse iki kat hafiftir.",
          secenekler=[
              D("Lityum (0,534 g/cm³)"),
              Y("Potasyum (0,89 g/cm³), çünkü listedeki en hafif metal o", "veri", "K4",
                "Tabloda lityumun yoğunluğu (0,534) potasyumunkinden (0,89) düşük."),
              Y("Sodyum (0,97 g/cm³)", "veri", "K2", "0,97, ölçüm aralığının (0,51–0,55) dışında."),
              Y("Sezyum; grupta aşağı inildikçe yoğunluk azalır", "veri", "K4",
                "Tabloya göre yoğunluk grupta aşağı inildikçe genel olarak artar."),
          ]),
        G("G3", "Veri", "", "tekli", "kanit", "veri",
          "Tabloya (K4) göre 1. grupta aşağı inildikçe yoğunluk genel olarak artıyor. Bu eğilime uymayan (istisna) "
          "metal hangisi?",
          "Yoğunlukları periyot sırasıyla tek tek karşılaştır.",
          "Genel eğilim yoğunluğun grupta aşağı doğru artmasıdır; ama potasyum (0,89) sodyumdan (0,97) sonra geldiği "
          "hâlde daha hafiftir. Veri analizinde istisnaları fark etmek önemlidir: bir eğilim her zaman bir kural değildir.",
          secenekler=[
              D("Potasyum: sodyumdan sonra geldiği hâlde yoğunluğu (0,89) sodyumunkinden (0,97) düşük."),
              Y("Lityum: en hafif metal olduğu için.", "veri", "K4", "Lityum grubun en üstünde ve en hafifi; eğilime uyuyor."),
              Y("Sezyum: en yoğun olduğu için.", "veri", "K4", "Sezyum grubun en altında ve en yoğunu; eğilime uyuyor."),
              Y("Hiçbiri; eğilim kusursuz.", "veri", "K4", "Sodyum ile potasyumun yoğunluklarını karşılaştır."),
          ]),
        G("G4", "Hipotez", "", "tekli", "alternatif", "hipotez",
          "Bir öğrenci 'Alev testinde kızıl renk verdiğine göre (K3) element stronsiyum olabilir' diyor. Bu hipotez "
          "hakkında ne söylenebilir?",
          "Stronsiyum hangi grupta? Analiz raporu ne diyor?",
          "Stronsiyum da kızıl alev verir; ama 2. gruptadır (toprak alkali metal) ve yoğunluğu 2,64 g/cm³'tür. Analiz "
          "1. grubu, ölçüm de 0,53 g/cm³'ü gösterdiği için bu hipotez reddedilir.",
          secenekler=[
              D("Reddedilir; stronsiyum da kızıl alev verir ama 2. gruptadır ve yoğunluğu 2,64 g/cm³'tür."),
              Y("Kabul edilir; kızıl alev yalnızca stronsiyumda görülür.", "veri", "K4",
                "Tabloya göre lityum da kızıl alev verir."),
              Y("Kabul edilir; stronsiyum da bir alkali metaldir.", "veri", "K1",
                "Stronsiyum toprak alkali metaldir (2. grup); analiz ise 1. grubu gösteriyor."),
              Y("Karar verilemez; alev testi hiçbir şey göstermez.", "kanitsiz", "K3",
                "Alev testi adayları daraltan değerli bir kanıttır; ama tek başına yetmez."),
          ]),
        G("G5", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Bataryadaki element hangisi? Adını ya da sembolünü yaz.",
          "1. grupta, kızıl alev veren ve yoğunluğu 0,534 g/cm³ olan metal...",
          "Element lityumdur (Li). Etiketteki silinmiş kelime 'lityum'du: lityum-iyon batarya.",
          hata_turu="kanitsiz"),
        G("G6", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Taşınabilir cihazların pillerinde lityumun tercih edilmesinin en önemli bilimsel nedeni nedir?",
          "Bir telefon pilinden hangi iki özellik beklenir: hafiflik ve...?",
          "RSC'ye göre lityumun en önemli kullanımı şarj edilebilir pillerdir. Lityum bütün metaller içinde en hafifidir "
          "ve dış katmanındaki tek elektronunu kolayca verir; bu iki özellik hafif ama çok enerji depolayan piller "
          "yapmayı sağlar.",
          secenekler=[
              D("Bütün metaller içinde en hafifidir ve elektronunu kolayca verir; hafif bir pilde çok enerji depolanabilir."),
              Y("Suyla hiç tepkimeye girmediği için güvenlidir.", "veri", "K5", "Lityum suyla tepkimeye girer."),
              Y("Kızıl alev verdiği için pil şarj olurken ışık saçar.", "iliski", "K3",
                "Alev rengi pilin çalışmasıyla ilgili değildir."),
              Y("Erime noktası çok yüksek olduğu için hiç ısınmaz.", "veri", "K4",
                "Lityumun erime noktası 180,5 °C; metaller arasında düşük sayılır."),
          ]),
        G("G7", "Sonuç", "", "tekli", "isim", "gozlem",
          "Lityumun adı neden 'taş' anlamına gelir? (K7)",
          "Lityum nereden bulunmuştu?",
          "RSC'ye göre diğer yaygın alkali metaller bitki maddelerinden bulunurken lityum bir mineralden, yani bir taştan "
          "bulundu; adı da buradan gelir.",
          secenekler=[
              D("Diğer yaygın alkali metaller bitki küllerinden bulunurken lityum bir mineralden (taştan) bulundu."),
              Y("Taş kadar sert olduğu için.", "veri", "K7", "Lityum yumuşak bir metaldir."),
              Y("Pillerde taş gibi uzun ömürlü olduğu için.", "iliski", "K7", "Ad, pillerin icadından çok önce, 1817'de verildi."),
              Y("Onu bulan kişinin adı Lithos olduğu için.", "kanitsiz", "K7", "Arşiv notunda kâşifin adı Arfvedson."),
          ]),
        G("G8", "Sonuç", "Sonuç", "tekli", "gerekce", "gerekce",
          "Şişmiş bir lityum bataryayla ilgili bilimsel olarak doğru uyarı hangisi?",
          "Lityumun suyla davranışını (K5) hatırla.",
          "Lityum tepkimeye yatkın bir metaldir; hasarlı bir pil ısınabilir ve alev alabilir. Şişmiş pil delinmemeli, "
          "ezilmemeli, ısıtılmamalı ve atık pil toplama noktasına verilmelidir.",
          secenekler=[
              D("Delinmemeli, ezilmemeli ve ısıtılmamalı; hasarlı pil alev alabilir. Atık pil toplama noktasına verilmeli."),
              Y("Suya batırılırsa güvenli hâle gelir.", "iliski", "K5", "Lityum suyla tepkimeye girer."),
              Y("Şişmiş pil daha çok enerji depolar; kullanmaya devam edilebilir.", "kanitsiz", "",
                "Bu iddiayı destekleyen bir kanıt yok; şişme bir hasar belirtisidir."),
              Y("Lityum radyoaktif olduğu için pil kurşun kutuda saklanmalı.", "veri", "K1",
                "Lityum radyoaktif değildir."),
          ]),
    ]))

DOSYALAR.append(dict(
    id="D10", seviye=2, sira=5, baslik="Cips Paketinin Sırrı", cevap="N",
    giris="Bir cips paketi açıldığında içinin yarısının boş olduğu görüldü. Bir tüketici 'Bize hava satıyorlar!' diye "
          "şikâyet etti. Üretici paketteki gazın 'hava değil' olduğunu söylüyor. Görevin: gazın hangi element "
          "olduğunu ve neden kullanıldığını bulmak.",
    kaynakca=[rsc(7, "nitrogen", "Azot"), rsc(8, "oxygen", "Oksijen"), rsc(18, "argon", "Argon"),
              rsc(2, "helium", "Helyum"), "Karbondioksitin yoğunluğu ve havanın bileşimi: yaklaşık standart değerler"],
    kanitlar=[
        ("K1", "deney", "Mum testi", "Paketten alınan gazla doldurulan bir kaba yanan bir mum indirildi; mum hemen söndü.", "", ""),
        ("K2", "fiziksel", "Renk ve koku", "Gaz renksiz ve kokusuz.", "", ""),
        ("K3", "deney", "Kireç suyu testi", "Gaz kireç suyundan geçirildi; kireç suyu bulanmadı.", "", ""),
        ("K4", "tablo", "Renksiz ve kokusuz bazı gazlar", "T1", "", "RSC Periyodik Tablo; standart değerler"),
        ("K5", "yogunluk", "Yoğunluk ölçümü", "Gazın yoğunluğu 0,00115 ± 0,00002 g/cm³ (oda sıcaklığında).", "", ""),
        ("K6", "isim", "Arşiv notu",
         "Bu gazı 1772'de İskoç öğrenci Daniel Rutherford bir element olarak tanımladı. Daha önce Cavendish ve "
         "Priestley, havadan oksijeni ayırınca geriye kalan gazın mumu söndürdüğünü ve içinde bir farenin "
         "yaşayamadığını görmüştü. Fransız kimyager Lavoisier bu gaza 'cansız' anlamındaki 'azote' adını verdi; Türkçedeki "
         "'azot' adı buradan gelir. Uluslararası sembolü N ise 'nitrogen' adından gelir: Yunanca 'nitron' (güherçile) ve "
         "'genes' (oluşturan).", "G4", RSC + "7/nitrogen"),
        ("K7", "kullanim", "RSC kaydı",
         "Bu gaz tepkimeye girmeyen bir ortam sağlamak için kullanılır; yiyecekleri korumak bunlardan biridir. Sıvı hâli "
         "(−196 °C) hücreleri dondurup saklamak ve yiyecekleri hızla dondurmak için kullanılır.", "G4", RSC + "7/nitrogen"),
    ],
    tablolar={"T1": [
        ["Gaz", "Mumu söndürür mü?", "Kireç suyunu bulandırır mı?", "Yoğunluk (g/cm³)", "Havadaki oranı (hacimce)"],
        ["Azot", "Evet", "Hayır", "0,001145", "Yaklaşık %78"],
        ["Oksijen", "Hayır, mumu daha parlak yakar", "Hayır", "0,001308", "Yaklaşık %21"],
        ["Argon", "Evet", "Hayır", "0,001633", "Yaklaşık %0,9"],
        ["Karbondioksit", "Evet", "Evet", "0,00184", "Yaklaşık %0,04"],
        ["Helyum", "Evet", "Hayır", "0,000164", "Çok az"],
    ]},
    gorevler=[
        G("G1", "Gözlem", "", "tekli", "kanit", "gozlem",
          "Mumun sönmesi (K1) gaz hakkında neyi gösterir?",
          "Tabloda mumu söndüren kaç gaz var?",
          "Mumun sönmesi gazın yanmayı desteklemediğini gösterir. Ama tabloya göre dört gaz mumu söndürür; bu kanıt tek "
          "başına gazın kimliğini göstermez.",
          secenekler=[
              D("Gaz yanmayı desteklemiyor; ama bu özellik birçok gazda var, tek başına kimliği göstermez."),
              Y("Gaz zehirlidir.", "iliski", "K1",
                "Mumun sönmesi yanmayı desteklememekle ilgilidir; zehirlilikle değil."),
              Y("Gaz karbondioksittir.", "kanitsiz", "K4", "Tabloya göre başka gazlar da mumu söndürür."),
              Y("Gaz oksijendir.", "veri", "K4", "Oksijen mumu söndürmez, daha parlak yakar."),
          ]),
        G("G2", "Veri", "", "coklu", "kanit", "veri",
          "Tabloya (K4) göre mum testi ve kireç suyu testi (K1, K3) birlikte hangi gazları aday olarak bırakır? Hepsini seç.",
          "Hem mumu söndüren hem de kireç suyunu bulandırmayan gazlar...",
          "Mumu söndüren ve kireç suyunu bulandırmayan gazlar azot, argon ve helyumdur. Karbondioksit kireç suyunu "
          "bulandırır; oksijen ise mumu söndürmez.",
          hata_turu="veri", secenekler=[
              D("Azot"), D("Argon"), D("Helyum"),
              Y("Karbondioksit", "veri", "K3", "Karbondioksit kireç suyunu bulandırır; test sonucuyla uyuşmuyor."),
              Y("Oksijen", "veri", "K1", "Oksijen mumu söndürmez; mumu daha parlak yakar."),
          ]),
        G("G3", "Veri", "", "tekli", "kanit", "veri",
          "Yoğunluk ölçümü (K5) kalan adaylardan hangisini gösterir?",
          "0,00113 ile 0,00117 arasına hangi değer giriyor?",
          "Ölçülen 0,00115 ± 0,00002 g/cm³ yalnızca azotla (0,001145) uyumlu. Argon (0,001633) daha yoğun, helyum "
          "(0,000164) çok daha hafif.",
          secenekler=[
              D("Azot (0,001145 g/cm³)"),
              Y("Argon (0,001633 g/cm³)", "veri", "K5", "0,001633, ölçüm aralığının dışında."),
              Y("Helyum (0,000164 g/cm³)", "veri", "K5", "0,000164, ölçüm aralığının çok dışında."),
              Y("Hiçbiri; gazların yoğunluğu ölçülemez.", "birim", "K5",
                "Gazların da yoğunluğu vardır. Değerler çok küçük olduğu için çoğu zaman g/cm³ yerine g/L ya da kg/m³ "
                "kullanılır."),
          ]),
        G("G4", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Paketteki gaz hangi elementtir? Adını ya da sembolünü yaz.",
          "Havanın yaklaşık %78'ini oluşturan gaz...",
          "Gaz azottur (N): mumu söndürüyor, kireç suyunu bulandırmıyor ve yoğunluğu azotla uyuşuyor.",
          hata_turu="kanitsiz"),
        G("G5", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Cips paketlerine hava yerine azot doldurulmasının bilimsel nedeni nedir?",
          "Havadaki hangi gaz yağların bozulmasına yol açar?",
          "RSC'ye göre azot, tepkimeye girmeyen bir ortam sağlamak için kullanılır; yiyecekleri korumak bunlardan biridir. "
          "Havadaki oksijen cipslerdeki yağın bozulmasına (acımasına) yol açar; azot dolu pakette cipsler daha uzun süre "
          "taze kalır. Gaz ayrıca cipslerin ezilmesini de önler.",
          secenekler=[
              D("Azot tepkimeye pek girmez; oksijen gibi yağın bozulmasına yol açmaz. Gaz ayrıca cipslerin ezilmesini önler."),
              Y("Azot cipsleri soğutur.", "iliski", "K7",
                "Paketteki azot oda sıcaklığındadır; cipsleri soğutmaz."),
              Y("Azot havadan çok daha ağır olduğu için paketi sabit tutar.", "veri", "K4",
                "Azot havadan biraz hafiftir."),
              Y("Azot mikropları öldüren zehirli bir gazdır.", "veri", "K4",
                "Soluduğumuz havanın yaklaşık %78'i azottur; azot zehirli değildir."),
          ]),
        G("G6", "Sonuç", "", "tekli", "sembol", "cikarim",
          "Türkçede adı 'azot' olduğu hâlde sembolü neden 'A' değil de 'N'? (K6)",
          "Arşiv notunda iki ayrı ad geçiyor.",
          "Uluslararası sembol N, elementin 'nitrogen' adından gelir. Türkçedeki 'azot' adı ise Lavoisier'nin Fransızca "
          "'azote' adından geçmiştir. Bu yüzden Türkçe ad ile sembol farklıdır.",
          secenekler=[
              D("Sembol uluslararası 'nitrogen' adından gelir; Türkçedeki 'azot' adı ise Fransızca 'azote'tan geçmiştir."),
              Y("N, 'nefes' kelimesinden gelir.", "kanitsiz", "K6", "Arşiv notunda böyle bir bilgi yok."),
              Y("A sembolü argona ayrıldığı için N seçilmiştir.", "kanitsiz", "K6",
                "Argonun sembolü Ar'dır; semboller rastgele değil, adlardan gelir."),
              Y("N, azotun 'nötr' (tepkimeye girmeyen) olmasından gelir.", "iliski", "K6",
                "Arşiv notuna göre N, 'nitrogen' adından gelir."),
          ]),
        G("G7", "Sonuç", "", "tekli", "isim", "gozlem",
          "Lavoisier'nin bu gaza 'cansız' anlamındaki 'azote' adını vermesinin nedeni ne olabilir? (K6)",
          "Cavendish ve Priestley ne gözlemlemişti?",
          "Bu gazın içinde mum sönüyor ve canlılar yaşayamıyordu: gaz yanmayı ve solunumu desteklemiyordu. Ama azot "
          "zehirli değildir; havanın %78'ini oluşturur. Saf azotta canlılar oksijensiz kaldıkları için yaşayamaz.",
          secenekler=[
              D("Bu gazda mum sönüyor ve canlılar yaşayamıyordu; gaz yanmayı ve solunumu desteklemiyordu."),
              Y("Gaz zehirli olduğu için canlıları öldürüyordu.", "iliski", "K4",
                "Azot zehirli değildir; havanın %78'ini oluşturur. Saf azotta canlılar oksijensiz kaldıkları için yaşayamaz."),
              Y("Gaz hiçbir zaman canlılar tarafından kullanılmaz.", "veri", "K7",
                "Azot proteinlerin ve DNA'nın temel elementlerinden biridir; bitkiler azotlu bileşikleri gübre olarak kullanır."),
              Y("Gaz yalnızca uzayda bulunduğu için.", "kanitsiz", "K4", "Havanın yaklaşık %78'i azottur."),
          ]),
        G("G8", "Çıkarım", "Gerekçe", "tekli", "gerekce", "gerekce",
          "Tüketicinin 'Bize hava satıyorlar!' şikâyetine bilimsel yanıt hangisi?",
          "Paketteki gaz hava olsaydı mum testinde ne olurdu?",
          "Güçlü bir yanıt kanıtlara dayanır: Gaz mumu söndürüyor (hava söndürmezdi, çünkü %21 oksijen içerir), kireç "
          "suyunu bulandırmıyor ve yoğunluğu azotla uyuşuyor. Azot cipslerin bozulmasını ve ezilmesini önlemek için konur.",
          secenekler=[
              D("Paketteki gaz hava değil azottur: mumu söndürüyor, kireç suyunu bulandırmıyor ve yoğunluğu azotla "
                "uyuşuyor. Azot cipslerin bozulmasını ve ezilmesini önlemek için konur."),
              Y("Paketteki gaz havadır, çünkü havanın çoğu azottur.", "veri", "K1",
                "Havada %21 oksijen de var; paketteki gaz mumu söndürdüğüne göre oksijen içermiyor."),
              Y("Gaz helyumdur, çünkü paketi hafifletir.", "veri", "K5", "Gazın yoğunluğu helyumla uyuşmuyor."),
              Y("Gazın ne olduğu önemli değil; paketteki boşluk her zaman haksızlıktır.", "kanitsiz", "",
                "Bu bir görüş, bilimsel bir yanıt değil; soru gazın ne olduğu ve neden konduğu."),
          ]),
    ]))
