# -*- coding: utf-8 -*-
"""Element Dosyalari: D02-D20 icerigi.

Sayisal veriler ve isim kokenleri RSC Periodic Table (periodic-table.rsc.org) element
sayfalarindan 2026-10-06 tarihinde dogrulandi. RSC disindaki bilgiler icin kaynak
dosyanin kaynakcasinda ayrica belirtilir (CDC, EPA, geology.com).
"""

RSC = "https://periodic-table.rsc.org/element/"


def rsc(z, ad, tr):
    return f"Royal Society of Chemistry, Periyodik Tablo: {tr} — {RSC}{z}/{ad}"


def D(metin):
    """Dogru secenek."""
    return (metin, "evet", "", "", "")


def Y(metin, hata, kanit, aciklama):
    """Yanlis secenek: hata turu, hatayi fark ettirecek kanit ve neden yanlis oldugu."""
    return (metin, "", hata, kanit, aciklama)


def S(metin, sira):
    """Siralama secenegi."""
    return (metin, str(sira), "", "", "")


def G(id, asama, arguman, tur, kategori, beceri, soru, ipucu, aciklama, dogru="", hata_turu="", secenekler=()):
    return (id, asama, arguman, tur, kategori, beceri, soru, ipucu, aciklama, dogru, hata_turu, list(secenekler))


DOSYALAR = []

# ---------------------------------------------------------------- SEVIYE 1: GOZLEM

DOSYALAR.append(dict(
    id="D02", seviye=1, sira=2, baslik="Uçan Balon Vakası", cevap="He",
    giris="Bir doğum günü partisinden sonra tavana yapışıp kalan balonlardan biri birimimize getirildi. Balon üç "
          "gündür havada duruyor. Parti şirketi balonları hangi gazla doldurduğunu söylemiyor, yalnızca 'tamamen "
          "güvenli' olduğunu iddia ediyor. Görevin: balondaki gazın hangi element olduğunu kanıtlarla bulmak.",
    kaynakca=[rsc(2, "helium", "Helyum"), rsc(1, "hydrogen", "Hidrojen"), rsc(10, "neon", "Neon"),
              rsc(18, "argon", "Argon"), "Havanın yoğunluğu: 20 °C ve deniz seviyesinde yaklaşık değer"],
    kanitlar=[
        ("K1", "fiziksel", "Balonun davranışı",
         "Bırakılan balon tavana kadar yükseldi ve üç gündür orada duruyor.", "", ""),
        ("K2", "deney", "Kıvılcım testi",
         "Balondan alınan küçük bir gaz örneğine kıvılcım yaklaştırıldı: gaz yanmadı, patlama olmadı.", "", ""),
        ("K3", "fiziksel", "Renk ve koku", "Gaz renksiz ve kokusuz.", "", ""),
        ("K4", "tablo", "Bazı gazların özellikleri", "T1", "", "RSC Periyodik Tablo; hava için yaklaşık değer"),
        ("K5", "deney", "Spektrum analizi",
         "Gazdan elektrik geçirilince yayılan ışığın spektrumunda parlak sarı bir çizgi görüldü. Neonun "
         "spektrumuna rengini veren parlak kırmızı-turuncu çizgiler görülmedi.", "G4", ""),
        ("K6", "tarih", "Arşiv kaydı: Hindenburg",
         "1937'de hidrojenle doldurulmuş Hindenburg zeplini iniş sırasında alev alıp yandı. Bu kaza, hidrojenle "
         "dolu yolcu zeplinleri döneminin sonu oldu.", "", ""),
        ("K7", "isim", "Arşiv notu",
         "Bu gaz Dünya'da bulunmadan 27 yıl önce, 1868'deki bir Güneş tutulması sırasında Güneş'in ışığında fark "
         "edildi. Adını Yunanca 'Güneş' anlamındaki kelimeden aldı.", "G5", RSC + "2/helium"),
    ],
    tablolar={"T1": [
        ["Gaz", "Yoğunluk (g/cm³, oda sıcaklığı)", "Yanıcı mı?"],
        ["Hava (karışım)", "0,0012", "Hayır"],
        ["Hidrojen", "0,000082", "Evet"],
        ["Helyum", "0,000164", "Hayır"],
        ["Neon", "0,000825", "Hayır"],
        ["Argon", "0,001633", "Hayır"],
    ]},
    gorevler=[
        G("G1", "Gözlem", "", "tekli", "kanit", "gozlem",
          "Balonun tavana yükselip orada kalması (K1) içindeki gaz hakkında neyi gösterir?",
          "Bir balon hangi durumda havada yükselir?",
          "Bir balon, içindeki gaz aynı hacimdeki havadan daha hafifse yükselir. Bu kanıt gazın yoğunluğunun "
          "havanınkinden küçük olduğunu gösterir; ama hangi gaz olduğunu söylemez.",
          secenekler=[
              D("Gaz, aynı hacimdeki havadan daha hafiftir."),
              Y("Gaz yanıcıdır.", "iliski", "K1",
                "Yükselmek yoğunlukla ilgilidir; bir gazın yanıcı olup olmadığı hakkında bilgi vermez."),
              Y("Gaz kesinlikle helyumdur.", "kanitsiz", "K4",
                "Havadan hafif tek gaz helyum değildir; tabloda başka gazlar da var."),
              Y("Gazın sıcaklığı havanınkinden yüksektir.", "veri", "K1",
                "Sıcak hava balonları bu yüzden yükselir; ama bu balon üç gündür oda sıcaklığında havada duruyor. "
                "İçindeki gaz çoktan oda sıcaklığına inmiş olmalı."),
          ]),
        G("G2", "Veri", "", "coklu", "kanit", "veri",
          "Tabloya (K4) göre havadan hafif olan gazlar hangileri? Hepsini seç.",
          "Her gazın yoğunluğunu havanınkiyle (0,0012) karşılaştır.",
          "Hidrojen (0,000082), helyum (0,000164) ve neon (0,000825 g/cm³) havadan (0,0012 g/cm³) hafiftir. "
          "Argon ise havadan ağırdır.",
          hata_turu="veri", secenekler=[
              D("Hidrojen"), D("Helyum"), D("Neon"),
              Y("Argon", "veri", "K4",
                "Argonun yoğunluğu (0,001633) havanınkinden (0,0012) büyük; argonla dolu bir balon yere düşer."),
          ]),
        G("G3", "Veri", "", "tekli", "kanit", "cikarim",
          "Kıvılcım testi (K2) hidrojen, helyum ve neondan hangisini eler?",
          "Tabloda hangi gaz yanıcı olarak görünüyor?",
          "Hidrojen havadaki oksijenle hızla yanar; 1937'deki Hindenburg kazası (K6) bunun tarihsel bir örneğidir. "
          "Örnek yanmadığına göre hidrojen elenir. Geriye helyum ve neon kalır.",
          secenekler=[
              D("Hidrojeni: hidrojen yanıcıdır, ama örnek yanmadı."),
              Y("Neonu: neon yanıcıdır.", "veri", "K4", "Tabloya göre neon yanıcı değildir."),
              Y("Hiçbirini: üç gaz da yanmaz.", "veri", "K4",
                "Tabloda hidrojenin yanıcı olduğu yazıyor; Hindenburg kaydı da bunu gösteriyor."),
              Y("Helyumu: yanmayan bir gaz balonda kullanılamaz.", "iliski", "K2",
                "Yanmamak bir gazın balonda kullanılmasını engellemez; tam tersine onu güvenli yapar."),
          ]),
        G("G4", "Hipotez", "", "tekli", "alternatif", "hipotez",
          "Adaylar helyum ve neon. İkisi de havadan hafif ve yanmıyor. Bu ikisini ayırmak için hangi inceleme en "
          "uygun olur?",
          "Her elementin kendine özgü bir 'parmak izi' var mı?",
          "Her element, içinden elektrik geçince ya da ısıtılınca kendine özgü renklerde ışık yayar. Bu ışığın "
          "spektrumu elementin parmak izi gibidir; helyumu neondan kesin olarak ayırır.",
          secenekler=[
              D("Gazdan elektrik geçirip yaydığı ışığın spektrumuna bakmak"),
              Y("Gazın kokusuna bakmak", "kanitsiz", "K3", "İki gaz da kokusuzdur; koku testi onları ayırmaz."),
              Y("Kıvılcım testini yeniden yapmak", "veri", "K2",
                "Bu test zaten yapıldı; iki aday da yanmaz. Testi yinelemek yeni bilgi vermez."),
              Y("Balonun rengine bakmak", "iliski", "K1",
                "Balonun rengi lastikten gelir; içindeki gaz hakkında bilgi vermez."),
          ]),
        G("G5", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Kanıtlara göre balondaki gaz hangi elementtir? Adını ya da sembolünü yaz.",
          "Spektrumda neonun kırmızı-turuncu çizgileri yok (K5).",
          "Gaz helyumdur (He): havadan hafif (K1), yanmıyor (K2) ve spektrumu neonunkinden farklı (K5). Bu sarı "
          "çizgi, 1868'de Güneş'in ışığında görülen ünlü çizgidir.",
          hata_turu="kanitsiz"),
        G("G6", "Sonuç", "", "tekli", "isim", "gozlem",
          "Arşiv notuna (K7) göre helyum adını neden 'Güneş'ten almıştır?",
          "Helyum ilk olarak nerede fark edildi?",
          "RSC'ye göre adı Yunanca 'Güneş' anlamındaki 'helios' kelimesinden gelir. 1868'de Pierre Janssen bir Güneş "
          "tutulmasında Güneş'in ışığında yeni bir sarı çizgi gördü; Joseph Lockyer bu yeni elemente helyum adını "
          "verdi. Helyum Dünya'da ancak 1895'te bulundu.",
          secenekler=[
              D("Dünya'da bulunmadan önce Güneş'in ışığındaki sarı bir çizgiden fark edildi."),
              Y("Güneş ışığında ısınınca balonları yükselttiği için.", "iliski", "K1",
                "Balonlar ısındıkları için değil, helyum havadan hafif olduğu için yükselir. Ad keşfin hikâyesinden gelir."),
              Y("Rengi Güneş gibi sarı olduğu için.", "veri", "K3",
                "Helyum renksizdir; sarı olan, yaydığı ışığın spektrumundaki bir çizgidir."),
              Y("Onu bulan bilim insanının adı Helios olduğu için.", "kanitsiz", "K7",
                "Arşiv notunda böyle bir kişiden söz edilmiyor."),
          ]),
        G("G7", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Süs balonlarında ve hava balonlarında hidrojen yerine neden helyum tercih edilir?",
          "İki gazın tablodaki 'Yanıcı mı?' sütununa bak.",
          "RSC'ye göre helyum düşük yoğunluğu nedeniyle süs balonlarında, hava balonlarında ve zeplinlerde kullanılır. "
          "Hidrojen de bir zamanlar balonlarda kullanılıyordu ama tehlikeli derecede tepkimeye yatkındır. Helyumun "
          "hiçbir maddeyle tepkimeye girmemesi onu güvenli yapar.",
          secenekler=[
              D("Helyum hidrojen kadar olmasa da havadan çok hafiftir ve hiç yanmaz; bu yüzden çok daha güvenlidir."),
              Y("Helyum hidrojenden daha hafiftir.", "veri", "K4",
                "Tabloya göre hidrojen (0,000082) helyumdan (0,000164) daha hafiftir."),
              Y("Helyum oksijenle birleşip balonu soğutur.", "kanitsiz", "K2",
                "Helyum hiçbir maddeyle tepkimeye girmez; bu iddiayı destekleyen bir kanıt yok."),
              Y("Helyum renksiz olduğu için balonun rengini bozmaz.", "iliski", "K3",
                "Hidrojen de renksizdir; renk bu seçimin nedeni olamaz."),
          ]),
        G("G8", "Kanıt", "Kanıt", "kanit", "kanit", "kanit",
          "İddian: Balondaki gaz helyumdur. Bu iddiayı destekleyen ve diğer adayları eleyen kanıtları seç. Tek "
          "başına ayırt edici olmayan kanıtları seçme.",
          "Her kanıt için sor: Bu kanıt bir adayı eliyor mu?",
          "Havadan hafif olması (K1) argonu, yanmaması (K2) hidrojeni, spektrumu (K5) da neonu eledi. Renk ve koku "
          "(K3) ayırt edici değil: adayların hepsi renksiz ve kokusuz. İsmin hikâyesi (K7) bu balondaki gaz hakkında "
          "bir kanıt değildir.",
          dogru="K1 K2 K5 (K4) (K6)", hata_turu="kanitsiz"),
    ]))

DOSYALAR.append(dict(
    id="D03", seviye=1, sira=3, baslik="Kutu, Folyo ve Uçak", cevap="Al",
    giris="Bir içecek kutusu, bir parça mutfak folyosu ve bir uçak modelinin gövde parçası aynı laboratuvar masasında. "
          "Tedarikçi üçünün de 'aynı metalden' yapıldığını söylüyor. Görevin: bu metalin hangi element olduğunu ve "
          "neden bu kadar farklı yerlerde kullanıldığını bulmak.",
    kaynakca=[rsc(13, "aluminium", "Alüminyum"), rsc(12, "magnesium", "Magnezyum"), rsc(22, "titanium", "Titanyum"),
              rsc(26, "iron", "Demir"), rsc(29, "copper", "Bakır"),
              "Elektrik iletkenliği değerleri (20 °C): Serway, R. A., Principles of Physics; aktaran: "
              "https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity"],
    kanitlar=[
        ("K1", "yogunluk", "Yoğunluk ölçümü", "2,7 ± 0,1 g/cm³ (üç eşyadan alınan örneklerin ortalaması)", "", ""),
        ("K2", "fiziksel", "Görünüş ve işlenebilirlik",
         "Gümüşi beyaz ve parlak. Folyo hâlinde kâğıttan ince yapraklara dönüştürülebiliyor, kolayca bükülüyor.", "", ""),
        ("K3", "deney", "Mıknatıs testi", "Üç eşya da mıknatısa çekilmiyor.", "", ""),
        ("K4", "iletkenlik", "Isı iletkenliği",
         "Folyoya sarılan sıcak bir yemek kabının dışı kısa sürede ısınıyor: metal ısıyı iyi iletiyor.", "", ""),
        ("K5", "kimyasal", "Paslanma gözlemi",
         "Aylarca nemli bir ortamda kalan kutuda kırmızı pas oluşmadı; yüzey biraz matlaştı ama sağlam kaldı.", "", ""),
        ("K6", "tablo", "Bazı metallerin özellikleri", "T1", "", "RSC Periyodik Tablo"),
        ("K7", "isim", "Arşiv notu",
         "Bu metalin adı, Latincede 'acı tuz' anlamına gelen 'alumen' (şap) kelimesinden gelir. Metal ilk kez 1825'te "
         "Hans Christian Ørsted tarafından, saf olmayan bir hâlde elde edildi.", "G3", RSC + "13/aluminium"),
        ("K8", "tarih", "RSC kaydı",
         "Bu metal yer kabuğunda en bol bulunan metaldir (yaklaşık %8,1), ama doğada nadiren saf hâlde bulunur. "
         "1700'lerin sonunda bilim insanları onu bileşiklerinden ayırmayı başaramıyordu.", "G3", RSC + "13/aluminium"),
    ],
    tablolar={"T1": [
        ["Metal", "Yoğunluk (g/cm³)", "Mıknatısa çekilir mi?", "Elektrik iletkenliği (MS/m, 20 °C)"],
        ["Magnezyum", "1,74", "Hayır", "—"],
        ["Alüminyum", "2,70", "Hayır", "35,5"],
        ["Titanyum", "4,506", "Hayır", "—"],
        ["Demir", "7,87", "Evet", "10,3"],
        ["Bakır", "8,96", "Hayır", "59,6"],
    ]},
    gorevler=[
        G("G1", "Gözlem", "", "tekli", "kanit", "gozlem",
          "Eşyaların mıknatısa çekilmemesi (K3) hangi sonucu destekler?",
          "Tabloda mıknatısa çekilen kaç metal var?",
          "Tablodaki metallerden yalnızca demir mıknatısa çekiliyor. Mıknatıs testi demiri eler ama kalan dört metali "
          "birbirinden ayırmaz.",
          secenekler=[
              D("Metal demir değildir; ama bu kanıt tek başına hangi metal olduğunu söylemez."),
              Y("Metal alüminyumdur, çünkü alüminyum mıknatısa çekilmez.", "kanitsiz", "K6",
                "Mıknatısa çekilmeyen başka metaller de var: bakır, magnezyum, titanyum. Bu kanıt tek başına yetmez."),
              Y("Metal elektriği iletmez.", "iliski", "K6",
                "Mıknatısa çekilmek ile elektriği iletmek farklı özelliklerdir; bakır mıknatısa çekilmez ama elektriği "
                "çok iyi iletir."),
              Y("Metal çok hafiftir.", "iliski", "K6",
                "Mıknatısa çekilmemek ile yoğunluk arasında bir bağ yok: tablodaki bakır hem yoğun hem de mıknatısa "
                "çekilmiyor."),
          ]),
        G("G2", "Veri", "", "tekli", "kanit", "veri",
          "Ölçülen yoğunluk 2,7 ± 0,1 g/cm³ (K1). Tabloya (K6) göre hangi metal bu ölçümle uyumlu?",
          "Belirsizliği hesaba kat: hangi değerler 2,6 ile 2,8 arasında?",
          "Ölçüm 2,6 ile 2,8 g/cm³ arasındaki değerlerle uyumlu. Tablodaki metallerden yalnızca alüminyum (2,70) bu "
          "aralıkta; diğerlerinin yoğunlukları çok farklı.",
          secenekler=[
              D("Yalnızca alüminyum (2,70 g/cm³)"),
              Y("Magnezyum (1,74 g/cm³), çünkü o da hafif bir metal", "veri", "K1",
                "1,74 g/cm³, ölçümün belirsizlik aralığının (2,6–2,8) çok dışında."),
              Y("Titanyum (4,506 g/cm³), çünkü uçaklarda kullanılır", "iliski", "K1",
                "Bir kullanım alanı kimlik kanıtı değildir; titanyumun yoğunluğu ölçümle uyuşmuyor."),
              Y("Hiçbiri; yoğunluk g/cm³ ile değil kilogram ile ölçülmeliydi", "birim", "K1",
                "Yoğunluğun birimi g/cm³ ya da kg/m³ olur; kilogram yalnızca kütle birimidir."),
          ]),
        G("G3", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Kanıtlara göre üç eşyanın metali hangi elementtir? Adını ya da sembolünü yaz.",
          "Yoğunluğu ölçümle uyuşan tek metal hangisiydi?",
          "Metal alüminyumdur (Al): yoğunluğu 2,70 g/cm³, mıknatısa çekilmiyor, gümüşi beyaz ve kolayca işlenebiliyor.",
          hata_turu="kanitsiz"),
        G("G4", "Gözlem", "", "coklu", "kullanim", "gozlem",
          "Kanıtlara göre alüminyum aşağıdaki kullanımlardan hangileri için uygundur? Hepsini seç.",
          "Hafif, işlenebilir, ısıyı ve elektriği ileten, paslanmayan bir metal nerelerde işe yarar?",
          "RSC'ye göre alüminyum içecek kutularında, folyoda, mutfak eşyalarında, pencere çerçevelerinde ve uçak "
          "parçalarında kullanılır. Elektriği iyi ilettiği için elektrik iletim hatlarında da sık kullanılır.",
          hata_turu="iliski", secenekler=[
              D("İçecek kutuları"),
              D("Uçak gövdesi parçaları (alaşım olarak)"),
              D("Elektrik iletim hatlarındaki teller"),
              Y("Kalıcı mıknatıs yapımı", "iliski", "K3",
                "Alüminyum mıknatısa çekilmez; mıknatıs yapımında kullanılamaz."),
              Y("Dalgıçların beline taktığı ağırlıklar", "iliski", "K1",
                "Dalgıç ağırlıkları için çok yoğun bir metal gerekir; alüminyum çok hafiftir."),
          ]),
        G("G5", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Uzun elektrik iletim hatlarında bakır yerine sıkça alüminyum kullanılır. Tablodaki (K6) verilere göre bunun "
          "en iyi açıklaması hangisi?",
          "İletkenlik sütununu ve yoğunluk sütununu birlikte düşün.",
          "Aynı hacimde bakır alüminyumdan daha iyi iletir (59,6'ya karşı 35,5 MS/m). Ama alüminyum bakırdan üç kattan "
          "fazla hafiftir. RSC'ye göre alüminyum bakırdan ucuzdur ve kütle bakımından neredeyse iki kat daha iyi bir "
          "iletkendir. Direkler arasında asılı duran uzun tellerde hafiflik çok önemlidir.",
          secenekler=[
              D("Alüminyum bakırdan daha az iletir ama çok daha hafif ve ucuzdur; aynı kütleyle neredeyse iki kat "
                "iletkenlik sağlar."),
              Y("Alüminyum elektriği bakırdan daha iyi iletir.", "veri", "K6",
                "Tabloya göre aynı koşullarda bakır (59,6) alüminyumdan (35,5) daha iyi iletir."),
              Y("Alüminyum mıknatısa çekilmediği için elektriği daha iyi iletir.", "kanitsiz", "K3",
                "Mıknatısa çekilmemek ile iletkenlik arasında bir neden-sonuç ilişkisi yok."),
              Y("Alüminyum paslanmadığı için içinden daha çok akım geçer.", "iliski", "K5",
                "Korozyona dayanıklılık telin uzun ömürlü olmasını sağlar ama iletkenliğin nedeni değildir."),
          ]),
        G("G6", "Sonuç", "", "tekli", "isim", "gozlem",
          "Arşiv notuna (K7) göre alüminyumun adı nereden gelir?",
          "Notta bir Latince kelime geçiyor.",
          "RSC'ye göre alüminyumun adı, şap için kullanılan Latince 'alumen' (acı tuz) kelimesinden gelir. Şap, "
          "alüminyum içeren ve çok eskiden beri bilinen bir tuzdur.",
          secenekler=[
              D("Latincede 'acı tuz' anlamına gelen 'alumen' (şap) kelimesinden"),
              Y("Onu ilk elde eden bilim insanının adından", "kanitsiz", "K7",
                "Ørsted alüminyumu ilk elde eden kişidir ama ad onun adından gelmez."),
              Y("Mutfak folyosunun icadından", "iliski", "K7", "Ad, folyonun icadından çok önce verildi."),
              Y("Latincede 'hafif' anlamına gelen bir kelimeden", "iliski", "K7",
                "Alüminyum hafif olduğu için bu açıklama akla yatkın görünebilir, ama arşiv notunda böyle yazmıyor."),
          ]),
        G("G7", "Çıkarım", "Gerekçe", "tekli", "gerekce", "gerekce",
          "İddian: Kutu, folyo ve uçak parçası alüminyumdan yapılmıştır. En güçlü gerekçe hangisi?",
          "Güçlü bir gerekçe ölçülen bir değeri bilinen değerlerle karşılaştırır.",
          "Güçlü bir gerekçe, sayısal bir ölçümü bilinen değerlerle karşılaştırır ve diğer kanıtların bu sonuçla "
          "uyumlu olduğunu gösterir.",
          secenekler=[
              D("Ölçülen yoğunluk (2,7 ± 0,1 g/cm³) tablodaki metallerden yalnızca alüminyumla uyuşuyor; mıknatısa "
                "çekilmemesi ve gümüşi beyaz rengi de bununla uyumlu."),
              Y("Üç eşya da hafif olduğu için alüminyum olmalı.", "kanitsiz", "K6",
                "Magnezyum da hafiftir; 'hafif' demek yetmez, ölçülen değer gerekir."),
              Y("Mıknatısa çekilmedikleri için alüminyumdurlar.", "kanitsiz", "K3",
                "Mıknatısa çekilmeyen birçok metal var; bu kanıt tek başına yetmez."),
              Y("Tedarikçi 'aynı metal' dediği için üçü de alüminyumdur.", "kanitsiz", "",
                "Tedarikçinin sözü bir kanıt değildir; iddia ölçümlerle sınanmalı."),
          ]),
    ]))

DOSYALAR.append(dict(
    id="D04", seviye=1, sira=4, baslik="Kurşun Kalem Vakası", cevap="C",
    giris="Bir öğrenci endişeli: 'Kurşun kalem kullanmak tehlikeli mi? Adı üstünde, içinde kurşun var!' Birim, bir "
          "kalemin ucunu laboratuvara gönderdi. Görevin: uçtaki siyah maddenin hangi element olduğunu kanıtlarla "
          "bulmak ve öğrencinin endişesinin yerinde olup olmadığına karar vermek.",
    kaynakca=[rsc(6, "carbon", "Karbon"), rsc(82, "lead", "Kurşun")],
    kanitlar=[
        ("K1", "fiziksel", "Görünüş",
         "Siyah, hafif parlak ve çok yumuşak. Kâğıda sürtünce iz bırakıyor, parmakları kayganlaştırıyor.", "", ""),
        ("K2", "iletkenlik", "Elektrik testi",
         "Kalem ucu bir pil ve küçük bir lambayla devreye bağlanınca lamba yandı: uç elektriği iletiyor.", "", ""),
        ("K3", "yogunluk", "Yoğunluk ölçümü", "2,2 ± 0,2 g/cm³", "", ""),
        ("K4", "deney", "Yanma deneyi",
         "Uçtan alınan örnek oksijen içinde çok yüksek sıcaklıkta yakıldı. Açığa çıkan gaz kireç suyunu bulandırdı. "
         "Geriye yanmayan, açık renkli bir kalıntı kaldı.", "", ""),
        ("K5", "tablo", "Kurşun ve grafitin özellikleri", "T1", "", "RSC Periyodik Tablo"),
        ("K6", "isim", "Arşiv notu",
         "Grafit 1500'lerde İngiltere'de bulunduğunda insanlar bu siyah, parlak ve yazı yazan maddeyi bir tür kurşun "
         "sandı; 'kurşun kalem' adı bu yanılgıdan kaldı. 'Grafit' adı Yunanca 'yazmak' anlamındaki 'graphein' "
         "kelimesinden, 'karbon' adı ise Latince 'odun kömürü' anlamındaki 'carbo' kelimesinden gelir.", "G4",
         RSC + "6/carbon"),
        ("K7", "tarih", "Elmas deneyi",
         "1796'da İngiliz kimyager Smithson Tennant bir elması yaktı ve yanınca yalnızca karbondioksit oluştuğunu "
         "göstererek elmasın da karbon olduğunu kanıtladı.", "G4", RSC + "6/carbon"),
    ],
    tablolar={"T1": [
        ["Özellik", "Kurşun", "Grafit"],
        ["Yoğunluk (g/cm³)", "11,3", "2,2"],
        ["Renk", "Mavimsi gri metal", "Siyah, parlak"],
        ["Yanınca karbondioksit verir mi?", "Hayır", "Evet"],
        ["Erime noktası (°C)", "327", "Erimez; yaklaşık 3825 °C'de süblimleşir"],
    ]},
    gorevler=[
        G("G1", "Gözlem", "", "tekli", "kanit", "gozlem",
          "Uç yumuşak ve kâğıtta iz bırakıyor (K1). Bu gözlem 'uçta kurşun var' iddiasını kanıtlar mı?",
          "Yumuşak olan ve iz bırakan başka maddeler düşünebiliyor musun?",
          "Yumuşak olmak ve iz bırakmak birçok maddenin özelliğidir. Bu gözlem tek başına uçtaki maddenin kimliğini "
          "kanıtlamaz; ölçüm ve deney gerekir.",
          secenekler=[
              D("Hayır; iz bırakan ve yumuşak olan başka maddeler de var. Bu gözlem tek başına yetmez."),
              Y("Evet; adı 'kurşun kalem' olduğuna göre içinde kurşun vardır.", "kanitsiz", "",
                "Bir eşyanın adı, içeriği hakkında kanıt değildir. Adlar çoğu zaman tarihsel nedenlerle verilir."),
              Y("Evet; kâğıtta yalnızca metaller iz bırakır.", "iliski", "K1",
                "Odun kömürü ve tebeşir gibi metal olmayan maddeler de iz bırakır."),
              Y("Hayır; kurşun sert bir metaldir, iz bırakamaz.", "veri", "K5",
                "Kurşun aslında yumuşak bir metaldir. Doğru cevap 'hayır' ama gerekçe yanlış: asıl sorun bu "
                "kanıtın yetersiz olması."),
          ]),
        G("G2", "Veri", "", "tekli", "kanit", "veri",
          "Yoğunluk ölçümünü (K3) tablodaki (K5) değerlerle karşılaştır. Ne söylenebilir?",
          "11,3'ün 2,2'ye oranı nedir?",
          "11,3 ÷ 2,2 ≈ 5. Ölçülen yoğunluk kurşunla değil grafitle uyumlu.",
          secenekler=[
              D("Ölçülen değer grafitle uyumlu; kurşunun yoğunluğu bunun beş katından fazla."),
              Y("Kurşunla uyumlu; ölçüm hatalı olmalı.", "veri", "K3",
                "Bir ölçümü beklenen sonucu vermediği için hatalı saymak bilimsel değildir. 2,2 ile 11,3 arasındaki "
                "fark ölçüm belirsizliğiyle açıklanamaz."),
              Y("Karar verilemez; çünkü yoğunlukların birimleri farklı.", "birim", "K5",
                "Tablodaki ve ölçümdeki birimler aynı: g/cm³."),
              Y("Kurşun ve grafitin yoğunlukları neredeyse aynı.", "veri", "K5", "Tabloyu yeniden oku."),
          ]),
        G("G3", "Kanıt", "", "coklu", "kanit", "cikarim",
          "Yanma deneyine (K4) göre hangi sonuçlara varılabilir? Doğru olanların hepsini seç.",
          "Kireç suyunu bulandıran gaz hangisidir? Geriye kalan kalıntı ne anlatır?",
          "Kireç suyunu bulandıran gaz karbondioksittir; karbondioksit oluştuğuna göre yanan madde karbon içerir. "
          "Yanmayan açık renkli kalıntı, kalem ucunun grafit ve kil gibi maddelerin karışımı olduğunu gösterir.",
          hata_turu="kanitsiz", secenekler=[
              D("Uçtaki siyah madde karbon içerir, çünkü yanınca karbondioksit oluştu."),
              D("Kalem ucu saf bir madde değil, bir karışımdır, çünkü geriye yanmayan bir kalıntı kaldı."),
              Y("Kalıntı kurşundur.", "kanitsiz", "K4",
                "Kalıntının kurşun olduğunu gösteren bir kanıt yok; kalıntı açık renkli. Kurşun mavimsi gri bir "
                "metaldir (K5)."),
              Y("Karbondioksit oluştuğuna göre uçta oksijen elementi vardır.", "iliski", "K4",
                "Oksijen, yakmak için ortama verildi; karbondioksitteki oksijen buradan gelir."),
          ]),
        G("G4", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Kalem ucundaki siyah, kaygan ve elektriği ileten madde hangi elementtir? Adını ya da sembolünü yaz.",
          "Yanınca karbondioksit veren madde...",
          "Siyah madde karbondur (C); grafit, karbonun bir biçimidir. Yoğunluğu grafitle uyuşuyor ve yanınca "
          "karbondioksit veriyor.",
          hata_turu="kanitsiz"),
        G("G5", "Sonuç", "", "tekli", "isim", "gozlem",
          "Madem uçta kurşun yok, neden 'kurşun kalem' deniyor? (K6)",
          "Arşiv notu bir yanılgıdan söz ediyor.",
          "Grafit bulunduğunda kurşuna benzetildi ve 'kurşun kalem' adı bu yanılgıdan kaldı. Öğrencinin endişesine "
          "gerek yok: kalem ucunda kurşun değil, grafit (karbon) ve kil var.",
          secenekler=[
              D("Grafit bulunduğunda insanlar onu bir tür kurşun sandı; ad bu yanılgıdan kaldı."),
              Y("Kalem uçlarına bugün de az miktarda kurşun katılır.", "kanitsiz", "K3",
                "Bu iddiayı destekleyen bir kanıt yok; ölçümler uçta grafit olduğunu gösteriyor."),
              Y("Grafit, kurşunun bir alaşımıdır.", "iliski", "K5",
                "Grafit bir metal alaşımı değil, karbon elementinin bir biçimidir."),
              Y("Kalemi icat eden kişinin soyadı 'Kurşun'du.", "kanitsiz", "K6",
                "Arşiv notunda böyle bir bilgi yok."),
          ]),
        G("G6", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Grafit kâğıtta neden kolayca iz bırakır ve kaygan hissettirir?",
          "Grafitteki atomların nasıl dizildiğini düşün.",
          "Grafitte karbon atomları düz katmanlar hâlinde dizilir; katmanlar arasındaki bağlar zayıftır. Yazarken "
          "katmanlar kayıp kâğıtta kalır. Aynı yapı grafiti kaygan yapar; katmanlar boyunca hareket edebilen "
          "elektronlar sayesinde grafit elektriği de iletir (K2).",
          secenekler=[
              D("Karbon atomları üst üste dizilmiş katmanlar oluşturur; katmanlar birbirinin üzerinden kolayca kayar "
                "ve kâğıtta kalır."),
              Y("Grafit elektriği ilettiği için kâğıda yapışır.", "iliski", "K2",
                "Elektrik iletkenliği iz bırakmanın nedeni değildir; ikisi de grafitin yapısından kaynaklanır."),
              Y("Grafit sıvı olduğu için kâğıda akar.", "veri", "K1", "Grafit katıdır; oda sıcaklığında erimez."),
              Y("Grafit kurşundan daha ağır olduğu için iz bırakır.", "veri", "K5",
                "Grafit kurşundan çok daha hafiftir (2,2'ye karşı 11,3 g/cm³)."),
          ]),
        G("G7", "Çıkarım", "", "tekli", "alternatif", "hipotez",
          "Elmas da karbondan oluşur (K7). Aynı elementten yapıldıkları hâlde elmas çok sert ve saydam, grafit ise "
          "yumuşak ve siyah. Bu farkı en iyi hangi hipotez açıklar?",
          "İki maddede değişen şey element mi, atomların düzeni mi?",
          "Elmas ve grafit karbonun iki farklı biçimidir. RSC'ye göre elmas bilinen en sert maddedir; grafit ise siyah, "
          "parlak ve yumuşaktır. Farkın nedeni atomların dizilişidir; element aynıdır.",
          secenekler=[
              D("Karbon atomlarının diziliş biçimi farklıdır: elmasta her atom komşularına sıkıca bağlıdır, grafitte "
                "ise kolayca kayan katmanlar vardır."),
              Y("Elmas daha saf karbondur; grafite kurşun karışmıştır.", "kanitsiz", "K4",
                "Grafitte kurşun olduğunu gösteren bir kanıt yok."),
              Y("Elmas ile grafit aslında farklı elementlerdir.", "veri", "K7",
                "Tennant'ın deneyi elmasın yanınca yalnızca karbondioksit verdiğini, yani karbon olduğunu gösterdi."),
              Y("Elmas, grafitin donmuş hâlidir.", "iliski", "K5",
                "Grafit zaten katıdır; donma sıvıdan katıya geçiştir."),
          ]),
    ]))

DOSYALAR.append(dict(
    id="D05", seviye=1, sira=5, baslik="Kırık Termometre", cevap="Hg",
    giris="Eski bir okul laboratuvarının dolabında kırık bir termometre bulundu. Cam parçalarının arasında gümüş "
          "renkli, yuvarlak damlacıklar var. Hademe damlacıkları süpürmek üzereyken birim olaya el koydu. Görevin: "
          "damlacıkların hangi element olduğunu bulmak ve neden dikkatli olunması gerektiğini açıklamak.",
    kaynakca=[rsc(80, "mercury", "Cıva"), rsc(31, "gallium", "Galyum"), rsc(55, "caesium", "Sezyum"),
              rsc(37, "rubidium", "Rubidyum"), rsc(11, "sodium", "Sodyum")],
    kanitlar=[
        ("K1", "fiziksel", "Görünüş",
         "Oda sıcaklığında (20 °C) sıvı; gümüş renkli, metalik parlak. Yüzeyde yuvarlak damlacıklar oluşturuyor.", "", ""),
        ("K2", "yogunluk", "Yoğunluk ölçümü", "13,5 ± 0,2 g/cm³", "", ""),
        ("K3", "tablo", "Erime noktası düşük bazı metaller", "T1", "", "RSC Periyodik Tablo"),
        ("K4", "iletkenlik", "Elektrik testi", "Damlacıklar elektriği iletiyor.", "", ""),
        ("K5", "isim", "Arşiv notu",
         "Bu metalin sembolü Hg; Latince 'hydrargyrum' adından gelir. Bu ad Yunanca 'su' ve 'gümüş' kelimelerinden "
         "oluşur. Türkçe adı cıva, İngilizce adı ise (mercury) Merkür gezegeninden gelir.", "G4", RSC + "80/mercury"),
        ("K6", "kullanim", "Güvenlik notu",
         "Bu metal ve buharı zehirlidir. RSC'ye göre zehirliliği nedeniyle termometre gibi birçok kullanımı terk "
         "edildi ya da kısıtlandı.", "G4", RSC + "80/mercury"),
    ],
    tablolar={"T1": [
        ["Metal", "Erime noktası (°C)", "Yoğunluk (g/cm³)"],
        ["Cıva", "−38,8", "13,53"],
        ["Sezyum", "28,5", "1,87"],
        ["Galyum", "29,8", "5,91"],
        ["Rubidyum", "39,3", "1,53"],
        ["Sodyum", "97,8", "0,97"],
    ]},
    gorevler=[
        G("G1", "Gözlem", "", "tekli", "kanit", "gozlem",
          "Madde oda sıcaklığında sıvı ve elektriği iletiyor (K1, K4). Bu iki gözlem birlikte neyi gösterir?",
          "Elektriği ileten, metalik parlak bir sıvı...",
          "Elektriği iletmek ve metalik parlaklık maddenin bir metal olduğunu, oda sıcaklığında sıvı olması da erime "
          "noktasının 20 °C'nin altında olduğunu gösterir. Bu, metaller arasında çok nadir görülür.",
          secenekler=[
              D("Oda sıcaklığında sıvı olan bir metaldir; bu, çok nadir görülen bir durumdur."),
              Y("Su bazlı bir sıvıdır, çünkü elektriği iletiyor.", "iliski", "K2",
                "Bu madde gümüş renkli, metalik parlak ve çok yoğun; suyla açıklanamaz."),
              Y("Erimiş hâlde bir metaldir; termometre çok ısınmış olmalı.", "kanitsiz", "K1",
                "Gözlem oda sıcaklığında (20 °C) yapıldı; madde erimek için ısıtılmadı."),
              Y("Bir gazdır, çünkü damlacıklar yuvarlak.", "iliski", "K1",
                "Damlacık oluşturmak sıvıların özelliğidir; gaz damlacık oluşturmaz."),
          ]),
        G("G2", "Veri", "", "coklu", "kanit", "veri",
          "Tabloya (K3) göre 20 °C'de sıvı olan metaller hangileri? Hepsini seç.",
          "Bir madde, sıcaklık erime noktasının üzerindeyse sıvıdır.",
          "Tablodaki metallerden yalnızca cıvanın erime noktası (−38,8 °C) 20 °C'nin altında. Sezyum ve galyum sıcak bir "
          "günde ya da elde eriyebilir, ama 20 °C'de katıdır.",
          hata_turu="veri", secenekler=[
              D("Cıva"),
              Y("Galyum", "veri", "K3",
                "Galyumun erime noktası 29,8 °C; 20 °C'de katıdır. Elde tutulunca eriyebilir ama oda sıcaklığında katıdır."),
              Y("Sezyum", "veri", "K3", "Sezyumun erime noktası 28,5 °C; 20 °C'de katıdır."),
              Y("Rubidyum", "veri", "K3", "Rubidyumun erime noktası 39,3 °C; 20 °C'de katıdır."),
          ]),
        G("G3", "Veri", "", "tekli", "kanit", "veri",
          "Ölçülen yoğunluk (K2) bu sonucu destekliyor mu?",
          "13,5 ± 0,2 aralığına tablodaki hangi değerler giriyor?",
          "Ölçülen 13,5 ± 0,2 g/cm³ yalnızca cıvanın yoğunluğuyla (13,53) uyumlu. Cıva sıvı olduğu hâlde çok yoğundur: "
          "aynı hacimdeki demirden yaklaşık 1,7 kat ağırdır.",
          secenekler=[
              D("Evet; 13,5 ± 0,2 g/cm³ cıvanın yoğunluğuyla (13,53) uyumlu, diğer metallerinkiyle uyumsuz."),
              Y("Hayır; sıvılar katılardan her zaman daha hafiftir.", "iliski", "K3",
                "Bu genelleme yanlış: tablodaki sıvı cıva, katı galyumdan iki kattan daha yoğun."),
              Y("Evet; ama galyum da bu yoğunlukla uyumlu.", "veri", "K3",
                "Galyumun yoğunluğu 5,91 g/cm³; ölçümden çok farklı."),
              Y("Karar verilemez; sıvıların yoğunluğu ölçülemez.", "birim", "K2",
                "Sıvıların da yoğunluğu ölçülür; örneğin suyunki yaklaşık 1 g/cm³'tür."),
          ]),
        G("G4", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Damlacıklar hangi elementtir? Adını ya da sembolünü yaz.",
          "20 °C'de sıvı olan tek metal...",
          "Damlacıklar cıvadır (Hg): oda sıcaklığında sıvı, elektriği iletiyor ve yoğunluğu cıvanınkiyle uyuşuyor.",
          hata_turu="kanitsiz"),
        G("G5", "Sonuç", "", "tekli", "sembol", "cikarim",
          "Cıvanın Türkçe ve İngilizce (mercury) adı H ya da g harfi içermediği hâlde sembolü neden Hg? (K5)",
          "Arşiv notunda hangi dilden bir ad geçiyor?",
          "Cıvanın sembolü Hg, Latince 'hydrargyrum' adından gelir; bu ad Yunanca 'su' ve 'gümüş' kelimelerinden "
          "türemiştir: sıvı ve gümüş renkli bir metal. İngilizce adı ise RSC'ye göre Merkür gezegeninden gelir.",
          secenekler=[
              D("Sembol, Latince 'hydrargyrum' (su gümüşü) adından gelir."),
              Y("Sembol, cıvanın Almanca adından gelir.", "kanitsiz", "K5",
                "Arşiv notunda sembolün Latince addan geldiği yazıyor."),
              Y("H hidrojenden, g gümüşten gelir; cıva bu ikisinin bileşiğidir.", "iliski", "K5",
                "Cıva bir elementtir, bileşik değildir. 'Hydrargyrum' 'su' ve 'gümüş' anlamındaki kelimelerden oluşur; "
                "bu, cıvanın hidrojen ya da gümüş içerdiği anlamına gelmez."),
              Y("Sembol rastgele seçilmiştir.", "kanitsiz", "K5",
                "Element sembolleri rastgele seçilmez; çoğu elementin Latince ya da Yunanca adından gelir."),
          ]),
        G("G6", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Eski termometrelerde cıva kullanılmasının bilimsel nedeni neydi?",
          "Cıva hangi sıcaklıklar arasında sıvıdır?",
          "Cıva −38,8 °C'de donar ve yaklaşık 357 °C'de kaynar; aradaki geniş aralıkta sıvıdır. Isındıkça düzenli "
          "biçimde genleşir ve ince tüpte kolayca okunur. Ama RSC'ye göre zehirliliği nedeniyle termometre gibi "
          "kullanımları terk edilmektedir.",
          secenekler=[
              D("Geniş bir sıcaklık aralığında sıvı kalır ve ısındıkça düzenli genleşir; parlak rengi ince tüpte kolay "
                "okunur."),
              Y("Elektriği iyi ilettiği için sıcaklığı elektrikle ölçer.", "iliski", "K4",
                "Cıvalı termometre elektrikle çalışmaz; sıvının genleşmesiyle ölçer."),
              Y("Çok yoğun olduğu için tüpte yükselmez.", "veri", "K2",
                "Termometrede cıva ısındıkça genleşip yükselir; yoğunluğu bunu engellemez."),
              Y("Zehirli olduğu için mikropları öldürür.", "iliski", "K6",
                "Zehirlilik termometrenin çalışmasıyla ilgili değildir; tam tersine cıvalı termometrelerin terk "
                "edilme nedenidir."),
          ]),
        G("G7", "Sonuç", "Sonuç", "tekli", "gerekce", "gerekce",
          "Hademe damlacıkları süpürgeyle toplamak istiyor. Birimin bilimsel uyarısı ne olmalı?",
          "Güvenlik notunu (K6) oku.",
          "Bilimsel bir karar kanıtlara dayanır: Güvenlik notu cıvanın ve buharının zehirli olduğunu söylüyor. "
          "Süpürmek ya da elektrikli süpürgeyle çekmek damlacıkları dağıtır ve buharlaşmayı artırır. Cıva dökülmelerini "
          "bu konuda eğitimli kişiler temizlemelidir.",
          secenekler=[
              D("Cıva ve buharı zehirlidir; damlacıklara dokunulmamalı, süpürülmemeli ve elektrikli süpürgeyle "
                "çekilmemeli. Ortam havalandırılmalı, temizliği eğitimli kişiler yapmalı."),
              Y("Cıva sıvı olduğu için zararsızdır; süpürülebilir.", "iliski", "K6",
                "Bir maddenin sıvı olması zararsız olduğunu göstermez."),
              Y("Tek tehlike elektrik çarpmasıdır, çünkü cıva elektriği iletir.", "veri", "K6",
                "Güvenlik notu asıl tehlikenin zehirlilik olduğunu söylüyor."),
              Y("Damlacıklar suyla yıkanırsa kendiliğinden yok olur.", "kanitsiz", "",
                "Bu iddiayı destekleyen bir kanıt yok; cıva suyla yok olmaz."),
          ]),
    ]))
