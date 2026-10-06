# -*- coding: utf-8 -*-
"""Element Dosyalari: Seviye 3 (Kanit) dosyalari, D11-D15."""

from dosyalar_veri import D, G, RSC, S, Y, rsc

CDC = "https://www.cdc.gov/healthy-swimming/prevention/preventing-eye-irritation-from-pool-chemicals.html"
EPA = "https://www.epa.gov/radtown/americium-ionization-smoke-detectors"
PIRIT = "https://geology.com/gold/fools-gold/"

DOSYALAR = []

DOSYALAR.append(dict(
    id="D11", seviye=3, sira=1, baslik="Havadaki Gizli Gaz", cevap="Ar",
    giris="Yıl 1894. Lord Rayleigh, havadan elde ettiği 'azotun', amonyaktan elde ettiği azottan biraz daha ağır "
          "olduğunu fark ediyor. Fark çok küçük, ama ölçümler her seferinde aynı sonucu veriyor. Birim, Rayleigh'nin "
          "deneyini kendi laboratuvarında yineledi ve sonuçları sana verdi. Görevin: bu farkın nedenini kanıtlarla bulmak.",
    kaynakca=[rsc(18, "argon", "Argon"), rsc(7, "nitrogen", "Azot"), rsc(2, "helium", "Helyum"),
              "Ölçüm tablosu: birimin yinelediği deney; değerler azot ve argonun bilinen yoğunluklarıyla (0 °C, 1 atm) "
              "uyumludur"],
    kanitlar=[
        ("K1", "tablo", "Birimin ölçümleri (0 °C, 1 atm)", "T1", "", ""),
        ("K2", "tarih", "Cavendish'in notu (1785)",
         "Henry Cavendish havadaki azotu en zorlu koşullarda bile tepkimeye sokmaya çalıştı; havanın yaklaşık %1'i "
         "hiçbir şekilde tepkimeye girmedi.", "", RSC + "18/argon"),
        ("K3", "deney", "Ramsay'in deneyi",
         "'Havadan elde edilen azot' sıcak magnezyumun üzerinden geçirildi. Azot magnezyumla tepkimeye girip katı "
         "magnezyum nitrür oluşturdu, ama geriye tepkimeye girmeyen bir gaz kaldı.", "G3", RSC + "18/argon"),
        ("K4", "deney", "Kalan gazın spektrumu",
         "Kalan gazın spektrumunda daha önce hiçbir elementte görülmemiş kırmızı ve yeşil çizgi grupları görüldü.",
         "G4", RSC + "18/argon"),
        ("K5", "yogunluk", "Kalan gazın yoğunluğu", "Kalan gazın yoğunluğu azotunkinin yaklaşık 1,4 katı.", "G4", ""),
        ("K6", "isim", "Arşiv notu",
         "Rayleigh ve Ramsay yeni elemente Yunanca 'tembel, işsiz' anlamına gelen 'argos' kelimesinden 'argon' adını "
         "verdiler, çünkü hiçbir maddeyle tepkimeye girmiyordu.", "G6", RSC + "18/argon"),
        ("K7", "kullanim", "RSC kaydı",
         "Bugün bu gaz eski tip akkor ampullerde, kaynak işlerinde ve çift camlı pencerelerin camları arasında kullanılır.",
         "G6", RSC + "18/argon"),
    ],
    tablolar={"T1": [
        ["Ölçüm", "Havadan elde edilen 'azot' (g/L)", "Amonyaktan elde edilen azot (g/L)"],
        ["1. ölçüm", "1,2568", "1,2504"],
        ["2. ölçüm", "1,2572", "1,2507"],
        ["3. ölçüm", "1,2570", "1,2506"],
        ["Ortalama", "1,2570", "1,2506"],
    ]},
    gorevler=[
        G("G1", "Veri", "", "tekli", "kanit", "veri",
          "Tablodaki (K1) ölçümlere bak. İki tür azot arasındaki fark gerçek mi, yoksa ölçüm hatası mı?",
          "Aynı türün ölçümleri kendi aralarında ne kadar farklı? İki türün ortalamaları ne kadar farklı?",
          "Bir farkın gerçek olup olmadığına, farkı ölçümlerin kendi saçılmasıyla karşılaştırarak karar veririz. Her türün "
          "üç ölçümü birbirine çok yakın (en fazla 0,0004 g/L fark); iki tür arasındaki fark ise 0,0064 g/L, yani bunun "
          "yaklaşık 16 katı. Bu fark ölçüm hatasıyla açıklanamaz.",
          secenekler=[
              D("Gerçek bir fark: her türün ölçümleri birbirine çok yakın, ama iki tür arasındaki fark bu saçılmadan çok "
                "daha büyük."),
              Y("Ölçüm hatası: fark binde 5 gibi çok küçük bir değer.", "birim", "K1",
                "Bir farkın küçük olması önemsiz olduğunu göstermez; önemli olan farkın ölçümlerin kendi saçılmasıyla "
                "karşılaştırılmasıdır."),
              Y("Gerçek bir fark, çünkü amonyaktan elde edilen azot kirlidir.", "kanitsiz", "K1",
                "Ölçümler bir fark olduğunu gösteriyor, ama nedenini göstermiyor. Bu iddiayı destekleyen bir kanıt yok."),
              Y("Karar verilemez; yoğunluk g/L ile değil g/cm³ ile ölçülmeliydi.", "birim", "K1",
                "g/L de geçerli bir yoğunluk birimidir; gazlar için daha kullanışlıdır."),
          ]),
        G("G2", "Hipotez", "", "coklu", "alternatif", "hipotez",
          "Havadan elde edilen 'azotun' daha ağır olmasını hangi hipotezler açıklayabilir? Test edilebilir olanların "
          "hepsini seç.",
          "Bir hipotez, deneyle sınanabilecek bir açıklamadır.",
          "İki hipotez de test edilebilir: havadan elde edilen gazda ya bilinen bir gaz tam temizlenmemiştir ya da "
          "bilinmeyen, daha ağır bir gaz vardır. Bilim insanları önce basit açıklamayı dikkatle sınar.",
          hata_turu="kanitsiz", secenekler=[
              D("Havadan elde edilen gaza azottan daha ağır, bilinmeyen bir gaz karışmış olabilir."),
              D("Havadan elde edilen gazda oksijen ya da karbondioksit gibi bilinen bir gaz tam temizlenmemiş olabilir."),
              Y("Rayleigh şanssız bir günde ölçüm yapmıştır.", "kanitsiz", "K1",
                "Ölçümler tekrarlandı ve her seferinde aynı sonuç çıktı; şans bir açıklama değildir."),
              Y("Havadan elde edilen gaz daha soğuk olduğu için daha ağırdır.", "birim", "K1",
                "Bütün ölçümler aynı koşullarda (0 °C, 1 atm) yapıldı."),
          ]),
        G("G3", "Hipotez", "", "tekli", "kanit", "cikarim",
          "Cavendish'in yüz yıl önceki notu (K2) bu hipotezlerden hangisini destekler?",
          "Cavendish'in kalıntısı neye benziyor: bir temizleme hatasına mı, yeni bir maddeye mi?",
          "Cavendish en zorlu koşullarda bile tepkimeye girmeyen bir kalıntı buldu; bu basit bir temizleme hatasına "
          "benzemiyor. Not, havada azot gibi davranmayan bir gaz olduğunu destekliyor. Yeni kanıt açıldı: Ramsay'in "
          "deneyi (K3).",
          secenekler=[
              D("Havada azot gibi davranmayan, hiç tepkimeye girmeyen bilinmeyen bir gaz olduğunu."),
              Y("Bir temizleme hatası olduğunu.", "veri", "K2",
                "Cavendish'in kalıntısı en zorlu koşullarda bile tepkimeye girmedi; bu bir temizleme hatasına benzemiyor."),
              Y("Havanın tamamen azottan oluştuğunu.", "veri", "K2",
                "Not, havanın yaklaşık %1'inin tepkimeye girmediğini söylüyor."),
              Y("Cavendish'in ölçümlerinin yanlış olduğunu.", "kanitsiz", "K2",
                "Bu iddiayı destekleyen bir kanıt yok."),
          ]),
        G("G4", "Kanıt", "", "tekli", "kanit", "kanit",
          "Ramsay'in deneyi (K3) neden önemli bir kanıttır?",
          "Azotun tamamı tepkimeye girip ayrıldıktan sonra geriye ne kaldı?",
          "Azotun tamamı magnezyumla tepkimeye girip ayrıldığı hâlde geriye bir gaz kaldı. Demek ki 'havadan elde edilen "
          "azot' saf azot değildi. Yeni kanıtlar açıldı: kalan gazın spektrumu (K4) ve yoğunluğu (K5).",
          secenekler=[
              D("Azotun tamamı ayrıldığı hâlde geriye bir gaz kaldı; demek ki havadan elde edilen azot saf değildi."),
              Y("Magnezyumun azotu ağırlaştırdığını gösterir.", "iliski", "K3",
                "Magnezyum azotla katı bir bileşik oluşturup onu gazdan ayırdı; azotu ağırlaştırmadı."),
              Y("Kalan gazın oksijen olduğunu kanıtlar.", "kanitsiz", "K3",
                "Oksijen de sıcak magnezyumla hemen tepkimeye girerdi; kalan gaz ise hiçbir şeyle tepkimeye girmiyor."),
              Y("Deney gereksizdir; yoğunluk farkı zaten her şeyi açıklar.", "kanitsiz", "K1",
                "Yoğunluk farkı bir şey olduğunu gösterir, ama ne olduğunu göstermez."),
          ]),
        G("G5", "Çıkarım", "", "tekli", "kanit", "cikarim",
          "Spektrumdaki yeni çizgiler (K4) ve yoğunluk (K5) birlikte hangi sonucu destekler?",
          "Her elementin spektrumu kendine özgüdür.",
          "Her elementin spektrumu kendine özgüdür ve bu çizgiler bilinen hiçbir elemente uymuyor. Gaz azottan yaklaşık "
          "1,4 kat yoğun. Bu, havadan elde edilen azotun neden biraz daha ağır olduğunu açıklar: içine azottan ağır yeni "
          "bir element karışmıştı.",
          secenekler=[
              D("Kalan gaz azottan ağır, yeni bir elementtir; bu da havadan elde edilen azotun neden daha ağır olduğunu açıklar."),
              Y("Kalan gaz bir azot bileşiğidir.", "kanitsiz", "K3",
                "Ramsay azotu tamamen ayırmıştı; ayrıca bu gaz hiçbir şeyle tepkimeye girmiyor."),
              Y("Yeni çizgiler cihazın arızasından kaynaklanır.", "kanitsiz", "K4",
                "Bu iddiayı destekleyen bir kanıt yok; çizgiler yalnızca bu gazda görüldü."),
              Y("Kalan gaz helyumdur.", "veri", "K5", "Helyum azottan çok daha hafiftir; bu gaz ise azottan ağır."),
          ]),
        G("G6", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Bu yeni element hangisi? Adını ya da sembolünü yaz.",
          "Havanın yaklaşık %1'ini oluşturan, tepkimeye girmeyen gaz...",
          "Element argondur (Ar). Havanın yaklaşık %0,9'unu oluşturur; tepkimeye girmediği için yüz yıl boyunca fark "
          "edilmedi.",
          hata_turu="kanitsiz"),
        G("G7", "Sonuç", "", "tekli", "isim", "gozlem",
          "Argonun adı neden 'tembel' anlamına gelir? (K6)",
          "Argonun en belirgin kimyasal davranışı nedir?",
          "RSC'ye göre argon adı Yunanca 'işsiz, tembel' anlamındaki 'argos' kelimesinden gelir; çünkü argon hiçbir "
          "maddeyle tepkimeye girmez.",
          secenekler=[
              D("Hiçbir maddeyle tepkimeye girmediği için"),
              Y("Havada yavaş hareket ettiği için", "iliski", "K6", "Ad gazın hızıyla değil, tepkimeye girmemesiyle ilgili."),
              Y("Keşfi çok uzun sürdüğü için", "iliski", "K6",
                "Keşfi gerçekten yüz yıldan fazla sürdü, ama ad gazın tepkimeye girmemesinden geliyor."),
              Y("Havada çok az bulunduğu için", "veri", "K6", "Ad gazın miktarıyla ilgili değil."),
          ]),
        G("G8", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Eski tip akkor ampullerin içine argon doldurulmasının nedeni nedir?",
          "Akkor hâldeki tel havadaki hangi gazla tepkimeye girip bozulur?",
          "RSC'ye göre argon, akkor ampullerde telin oksijenle tepkimeye girip bozulmasını önlemek için kullanılır. Argon "
          "tepkimeye girmediği için kızgın telin çevresinde koruyucu bir ortam oluşturur.",
          secenekler=[
              D("Argon tepkimeye girmez; akkor hâldeki telin oksijenle tepkimeye girip bozulmasını önler."),
              Y("Ampulün ışığı argondan gelir.", "iliski", "K7",
                "Akkor ampulde ışığı kızgın tel verir; argon telin bozulmasını önler."),
              Y("Argon ampulü soğutur.", "kanitsiz", "K7", "Bu iddiayı destekleyen bir kanıt yok."),
              Y("Argon havadan hafif olduğu için ampulü hafifletir.", "veri", "K5",
                "Argon azottan, dolayısıyla havadan daha yoğundur."),
          ]),
        G("G9", "Çıkarım", "Karşı kanıt", "tekli", "alternatif", "hipotez",
          "Bir eleştirmen 'Rayleigh'nin bulduğu fark ölçüm hatasıydı' diyor. En güçlü karşı kanıt hangisi?",
          "Hangi kanıt farkın kaynağını doğrudan gösterdi?",
          "En güçlü karşı kanıt, farkın kaynağını doğrudan ortaya koyan deneydir: Ramsay azotu tamamen ayırınca geriye "
          "tepkimeye girmeyen bir gaz kaldı ve spektrumu yeni çizgiler gösterdi.",
          secenekler=[
              D("Ramsay, havadan elde edilen azottan azotu tamamen ayırınca geriye tepkimeye girmeyen bir gaz kaldı ve bu "
                "gazın spektrumu yeni çizgiler gösterdi."),
              Y("Rayleigh ünlü bir bilim insanıdır, hata yapmaz.", "kanitsiz", "",
                "Bir iddianın doğruluğu onu söyleyenin ününe değil, kanıtlara bağlıdır."),
              Y("Fark çok küçük olduğu için önemsizdir.", "birim", "K1",
                "Bu, eleştirmeni destekleyen bir ifade; üstelik farkın küçük olması önemsiz olduğu anlamına gelmez."),
              Y("Cavendish de aynı yoğunluk ölçümünü yapmıştı.", "veri", "K2",
                "Cavendish yoğunluk ölçmedi; tepkimeye girmeyen bir kalıntı buldu."),
          ]),
    ]))

DOSYALAR.append(dict(
    id="D12", seviye=3, sira=2, baslik="Sahte Altın", cevap="Au",
    giris="Bir kuyumcuya üç parça getirildi: A) parlak sarı bir taş parçası, B) sarı bir külçe, C) sarı bir madalyon. "
          "Satıcı üçünün de saf altın olduğunu söylüyor. Kuyumcu şüphelenip parçaları birime gönderdi. Görevin: hangisinin "
          "gerçekten altın olduğuna kanıtlarla karar vermek. Dikkat: bu dosyada bazı kanıtlar yanıltıcı olabilir.",
    kaynakca=[rsc(79, "gold", "Altın"), rsc(74, "tungsten", "Tungsten"),
              "Pirit ve altını ayırma (yoğunluk, çizgi rengi, kırılganlık): geology.com — " + PIRIT,
              "Pirinç (bakır-çinko alaşımı) yoğunluğu: yaklaşık değer"],
    kanitlar=[
        ("K1", "tablo", "Üç parçanın ölçümleri", "T1", "", ""),
        ("K2", "tablo", "Referans değerler", "T2", "", "RSC Periyodik Tablo; geology.com"),
        ("K3", "kimyasal", "Asit testi",
         "Kuyumcunun nitrik asit damlası A'yı ve C'yi etkiledi; B'nin yüzeyinde hiçbir değişiklik olmadı.", "", ""),
        ("K4", "tarih", "Arşiv kaydı: Arşimet",
         "Anlatılan hikâyeye göre Arşimet, kralın tacının saf altından yapılıp yapılmadığını anlamak için tacın yerinden "
         "ettiği suyun hacmini ölçerek tacın yoğunluğunu buldu.", "", ""),
        ("K5", "deney", "Külçenin içi",
         "Külçeye ince bir delik açıldı. İçten çıkan talaş da sarı renkte ve iğneyle kolayca eziliyor.", "G3", ""),
        ("K6", "isim", "Arşiv notu",
         "Altının sembolü Au, Latince 'aurum' kelimesinden gelir. RSC'ye göre ilk saf altın sikkeler, bugün Türkiye "
         "sınırları içinde kalan Lidya Krallığı'nda Kral Kroisos (Karun) döneminde (MÖ 561–547) basıldı.", "G5",
         RSC + "79/gold"),
    ],
    tablolar={
        "T1": [
            ["Parça", "Yoğunluk (g/cm³)", "Porselene sürtününce bıraktığı çizgi", "İğneyle bastırınca"],
            ["A (taş)", "5,0", "Yeşilimsi siyah", "Kırılıyor"],
            ["B (külçe)", "19,3", "Altın sarısı", "Eziliyor, iz kalıyor"],
            ["C (madalyon)", "8,5", "Denenmedi", "Hafif iz kalıyor"],
        ],
        "T2": [
            ["Madde", "Yoğunluk (g/cm³)", "Not"],
            ["Altın (Au)", "19,3", "Çok yumuşak, dövülebilir; sarı çizgi bırakır"],
            ["Tungsten (W)", "19,3", "Sert, gümüşi beyaz metal"],
            ["Pirit (FeS₂, 'aptal altını')", "4,9–5,2", "Kırılgan; yeşilimsi siyah çizgi bırakır"],
            ["Pirinç (bakır–çinko alaşımı)", "8,4–8,7", "Sarı renkli alaşım"],
        ],
    },
    gorevler=[
        G("G1", "Gözlem", "", "tekli", "kanit", "gozlem",
          "Üç parçanın da sarı ve parlak olması 'üçü de altın' iddiasını destekler mi?",
          "Referans tablosundaki (K2) maddelerin renklerine bak.",
          "Renk tek başına yetersiz bir kanıttır: pirit ve pirinç de sarı ve parlaktır. Pirite 'aptal altını' denmesinin "
          "nedeni de budur.",
          secenekler=[
              D("Hayır; pirit ve pirinç gibi başka maddeler de sarı ve parlaktır. Renk tek başına yetersiz bir kanıttır."),
              Y("Evet; altının rengi taklit edilemez.", "kanitsiz", "K2",
                "Referans tablosunda altına benzeyen sarı maddeler var."),
              Y("Evet; parlak olan her metal değerlidir.", "iliski", "K2",
                "Parlaklık bir metalin değeri hakkında bilgi vermez; pirinç de parlaktır."),
              Y("Hayır; altın aslında gümüş renklidir.", "veri", "K2", "Altın karakteristik sarı renktedir."),
          ]),
        G("G2", "Veri", "", "coklu", "kanit", "veri",
          "Ölçümlere (K1) ve referans değerlere (K2) göre hangi parçalar altın OLAMAZ? Hepsini seç.",
          "Her parçanın yoğunluğunu ve davranışını referans tablosuyla karşılaştır.",
          "A'nın yoğunluğu (5,0), yeşilimsi siyah çizgisi ve kırılganlığı piritle uyuşuyor; C'nin yoğunluğu (8,5) pirinçle "
          "uyuşuyor. İkisi de altın olamaz. B'nin ölçümleri ise altınla uyumlu; şimdilik elenemez.",
          hata_turu="veri", secenekler=[
              D("A (taş parçası)"),
              D("C (madalyon)"),
              Y("B (külçe)", "veri", "K1",
                "B'nin yoğunluğu ve çizgi rengi altınla uyumlu; bu kanıtlarla elenemez."),
          ]),
        G("G3", "Hipotez", "", "tekli", "alternatif", "hipotez",
          "B'nin yoğunluğu 19,3 g/cm³. Bu, B'nin altın olduğunu kesin olarak kanıtlar mı?",
          "Referans tablosunda yoğunluğu 19,3 olan başka bir metal var mı?",
          "Hayır. Tungstenin yoğunluğu da 19,3 g/cm³; yoğunluk ikisini ayırmaz. B, içi tungstenle doldurulup altınla "
          "kaplanmış bir külçe de olabilir. Bu yüzden külçenin içi incelendi (K5).",
          secenekler=[
              D("Hayır; tungstenin yoğunluğu da 19,3 g/cm³. B'nin içi tungsten, dışı altın olabilir; içini incelemek gerekir."),
              Y("Evet; 19,3 g/cm³ yalnızca altına aittir.", "veri", "K2", "Referans tablosuna göre tungstenin yoğunluğu da 19,3."),
              Y("Evet; yoğunluk en güçlü kanıttır, başka teste gerek yok.", "kanitsiz", "K2",
                "Yoğunluk güçlü bir kanıttır ama aynı yoğunlukta iki metal olduğunda yetmez."),
              Y("Hayır; çünkü yoğunluk g/cm³ ile değil ayar (karat) ile ölçülür.", "birim", "K1",
                "Ayar (karat) altının saflığını gösterir; yoğunluğun birimi g/cm³'tür."),
          ]),
        G("G4", "Kanıt", "", "tekli", "kanit", "cikarim",
          "Külçenin içinden alınan örnek (K5) ve asit testi (K3) birlikte değerlendirildiğinde hangi sonuca varılır?",
          "Tungsten nasıl bir metal? İçten çıkan talaş nasıl?",
          "İçten çıkan talaş da sarı ve yumuşak; sert ve gümüşi beyaz olan tungsten bununla uyuşmuyor. Asit testi de "
          "altınla uyumlu, ama tek başına yetmezdi: tungsten de birçok asitten pek etkilenmez. Ayırt edici kanıt iç kısmın "
          "sarı ve yumuşak olmasıdır.",
          secenekler=[
              D("İç kısım da sarı ve yumuşak; sert ve gümüşi beyaz tungsten bununla uyuşmuyor. Külçe altındır."),
              Y("Asitten etkilenmemesi tek başına külçenin altın olduğunu kanıtlar.", "kanitsiz", "K3",
                "Tungsten de birçok asitten pek etkilenmez; asit testi altını tungstenden ayırmaz."),
              Y("İç kısmın yumuşak olması külçenin kurşun olduğunu gösterir.", "veri", "K1",
                "Kurşunun yoğunluğu 11,3 g/cm³; külçeninki 19,3."),
              Y("Delik açmak külçeyi bozar; bu yüzden kanıt geçersizdir.", "kanitsiz", "K5",
                "Örneği biraz bozmak kanıtı geçersiz yapmaz; bazen tek kesin yol budur."),
          ]),
        G("G5", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "B'nin elementi hangisi? Adını ya da sembolünü yaz.",
          "Yoğunluğu 19,3, içi de dışı da sarı ve yumuşak...",
          "B altındır (Au). A pirit, C ise pirinç gibi bir alaşım.",
          hata_turu="kanitsiz"),
        G("G6", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Altının elektronik devrelerdeki bağlantı uçlarında kullanılmasının nedeni nedir?",
          "Asit testinde (K3) B'ye ne oldu?",
          "RSC'ye göre altın, bakır parçaları korumak için idealdir: elektriği iyi iletir ve korozyona uğramaz, bu yüzden "
          "temas noktası zamanla bozulmaz.",
          secenekler=[
              D("Elektriği iyi iletir ve korozyona uğramaz; bu yüzden temas noktası zamanla bozulmaz."),
              Y("En iyi elektrik iletkeni altındır.", "veri", "",
                "En iyi elektrik iletkeni gümüştür; ardından bakır gelir. Altın paslanmadığı için seçilir."),
              Y("Altın ağır olduğu için bağlantıyı sabit tutar.", "iliski", "K1",
                "Bağlantı uçlarındaki altın çok ince bir kaplamadır; ağırlığı bir işe yaramaz."),
              Y("Altın mıknatısa çekildiği için bağlantıyı tutar.", "veri", "",
                "Altın mıknatısa çekilmez."),
          ]),
        G("G7", "Sonuç", "", "tekli", "sembol", "cikarim",
          "Altının sembolü neden 'A' değil de 'Au'? (K6)",
          "Arşiv notunda Latince bir kelime geçiyor.",
          "Altının sembolü Au, Latince 'aurum' kelimesinden gelir. Tek harfli 'A' sembolü hiçbir elemente ait değildir.",
          secenekler=[
              D("Latince adı 'aurum'dan gelir."),
              Y("'Altın' kelimesinin ilk ve son harflerinden gelir.", "kanitsiz", "K6",
                "Arşiv notuna göre sembol Latince bir kelimeden gelir."),
              Y("'A' başka bir elementin sembolü olduğu için.", "kanitsiz", "K6",
                "Tek harfli 'A' sembolü hiçbir elemente ait değildir."),
              Y("İngilizce 'gold' adından gelir.", "veri", "K6", "'gold' kelimesinde a ya da u harfi yok."),
          ]),
        G("G8", "Sonuç", "", "tekli", "isim", "gozlem",
          "'Karun kadar zengin' deyimi altının tarihiyle nasıl ilişkilidir? (K6)",
          "Karun hangi krallığın kralıydı?",
          "Karun (Kroisos), RSC'ye göre ilk saf altın sikkelerin basıldığı Lidya Krallığı'nın kralıydı ve servetiyle "
          "ünlüydü. Lidya bugün Türkiye sınırları içindedir.",
          secenekler=[
              D("Karun (Kroisos), ilk saf altın sikkelerin basıldığı Lidya Krallığı'nın kralıydı; servetiyle ünlüydü."),
              Y("Altını ilk keşfeden kişi Karun'dur.", "veri", "K6", "RSC'ye göre altın tarih öncesi çağlardan beri bilinir."),
              Y("Karun, altının sembolünü bulan bir kimyagerdir.", "kanitsiz", "K6", "Arşiv notunda böyle bir bilgi yok."),
              Y("Deyim altının yoğunluğundan gelir.", "iliski", "K6", "Deyim bir kralın servetinden gelir."),
          ]),
        G("G9", "Çıkarım", "Gerekçe", "tekli", "gerekce", "gerekce",
          "Kuyumcuya yazacağın raporda en güçlü gerekçe hangisi?",
          "Güçlü gerekçe her parçayı ve en tehlikeli tuzağı ele alır.",
          "Güçlü bir rapor her parçayı kanıtlarla ele alır ve en güçlü alternatifi (aynı yoğunluktaki tungsten) açıkça eler.",
          secenekler=[
              D("A'nın yoğunluğu, çizgisi ve kırılganlığı piritle; C'nin yoğunluğu pirinçle uyuşuyor. B'nin yoğunluğu "
                "altınla uyuşuyor; içten alınan örneğin sarı ve yumuşak olması, aynı yoğunluktaki tungsten ihtimalini eledi."),
              Y("B en ağır parça olduğu için altındır.", "birim", "K1",
                "Ağırlık parçanın büyüklüğüne de bağlıdır; karşılaştırılması gereken, yoğunluktur."),
              Y("B asitten etkilenmediği için altındır.", "kanitsiz", "K3",
                "Tungsten de birçok asitten pek etkilenmez; bu kanıt tek başına yetmez."),
              Y("Satıcı güvenilir biri olduğu için B altındır.", "kanitsiz", "",
                "Bir kişinin güvenilirliği bilimsel bir kanıt değildir."),
          ]),
    ]))

DOSYALAR.append(dict(
    id="D13", seviye=3, sira=3, baslik="Paslanan Köprü", cevap="Fe",
    giris="Bir köprünün metal korkuluklarında pas lekeleri görüldü. Belediye 'Pas yağmurdan oluşur; tek neden sudur' "
          "diyor. Birim, paslanmanın gerçek nedenini kontrollü bir deneyle araştırıyor. Görevin: korkulukların metalini "
          "kanıtlamak ve deneyi yorumlamak.",
    kaynakca=[rsc(26, "iron", "Demir"), rsc(27, "cobalt", "Kobalt"), rsc(28, "nickel", "Nikel")],
    kanitlar=[
        ("K1", "deney", "Mıknatıs testi", "Korkuluk metali mıknatısa güçlü biçimde çekiliyor.", "", ""),
        ("K2", "yogunluk", "Yoğunluk ölçümü", "7,9 ± 0,1 g/cm³", "", ""),
        ("K3", "tablo", "Mıknatısa güçlü biçimde çekilen metaller", "T1", "", "RSC Periyodik Tablo"),
        ("K4", "tablo", "Paslanma deneyi: bir hafta sonra çiviler", "T2", "", ""),
        ("K5", "kimyasal", "Pas analizi", "Kırmızı-kahverengi pasın, su içeren bir demir oksit olduğu bulundu.", "", ""),
        ("K6", "tarih", "RSC kaydı",
         "Demiri cevherinden ilk eriterek elde edenler, MÖ 1500 civarında Anadolu'daki Hititlerdi; bu, Demir Çağı'nın "
         "başlangıcıydı. Mısır'da bulunan MÖ 3500'den kalma demir eşyalar ise yaklaşık %7,5 nikel içeriyor; bu da "
         "onların göktaşından geldiğini gösteriyor. Sembol Fe, Latince 'ferrum' adından gelir.", "G3", RSC + "26/iron"),
    ],
    tablolar={
        "T1": [
            ["Metal", "Yoğunluk (g/cm³)"],
            ["Demir", "7,87"],
            ["Kobalt", "8,86"],
            ["Nikel", "8,90"],
        ],
        "T2": [
            ["Tüp", "Koşullar", "Bir hafta sonra"],
            ["1", "Yalnızca kuru hava (tüpte nem çeken madde var)", "Paslanmadı"],
            ["2", "Kaynatılıp üzeri yağla kapatılmış su (havasız su)", "Paslanmadı"],
            ["3", "Su ve hava", "Paslandı"],
            ["4", "Tuzlu su ve hava", "Çok paslandı"],
        ],
    },
    gorevler=[
        G("G1", "Veri", "", "tekli", "kanit", "veri",
          "Mıknatıs testi (K1) ve yoğunluk (K2) birlikte tablodaki (K3) hangi metali gösteriyor?",
          "7,8 ile 8,0 arasına hangi değer giriyor?",
          "Mıknatısa güçlü biçimde çekilen üç metalden yalnızca demirin yoğunluğu (7,87) ölçümle uyumlu. Kobalt ve nikel "
          "birbirine çok yakın (8,86 ve 8,90) ama ikisi de aralığın dışında.",
          secenekler=[
              D("Demir (7,87 g/cm³)"),
              Y("Kobalt (8,86 g/cm³)", "veri", "K2", "8,86, ölçüm aralığının (7,8–8,0) dışında."),
              Y("Nikel (8,90 g/cm³)", "veri", "K2", "8,90, ölçüm aralığının dışında."),
              Y("Üçü de; yoğunlukları neredeyse aynı", "veri", "K3",
                "Kobalt ve nikel birbirine çok yakın, ama demir onlardan belirgin biçimde farklı."),
          ]),
        G("G2", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Korkulukların metali hangi elementtir? Adını ya da sembolünü yaz.",
          "Mıknatısa çekilen ve yoğunluğu 7,87 g/cm³ olan metal...",
          "Metal demirdir (Fe). Pas analizi (K5) de bunu destekliyor: pas bir demir oksittir.",
          hata_turu="kanitsiz"),
        G("G3", "Hipotez", "", "tekli", "kanit", "hipotez",
          "Deneyde (K4) tüp 1 ile tüp 3'ü karşılaştıran bir öğrenci hangi değişkenin etkisini sınayabilir?",
          "İki tüp arasında yalnızca tek bir koşul farklı olmalı.",
          "Kontrollü bir deneyde karşılaştırılan iki düzenek arasında yalnızca tek bir değişken farklı olmalıdır. Tüp 1 ile "
          "tüp 3'te hava var; yalnızca birinde su var. Bu karşılaştırma suyun etkisini gösterir.",
          secenekler=[
              D("Suyun etkisini: iki tüpte de hava var, yalnızca birinde su var."),
              Y("Havanın etkisini", "veri", "K4", "İki tüpte de hava var; hava değişmiyor."),
              Y("Tuzun etkisini", "veri", "K4", "Tuz yalnızca 4. tüpte var."),
              Y("Sıcaklığın etkisini", "kanitsiz", "K4", "Sıcaklık bütün tüplerde aynı; deney onu değiştirmiyor."),
          ]),
        G("G4", "Kanıt", "", "tekli", "kanit", "cikarim",
          "Tüp 2'nin sonucu (K4) belediyenin 'tek neden sudur' iddiası hakkında ne söyler?",
          "Tüp 2'de su var mı? Hava var mı? Çivi paslandı mı?",
          "Tüp 2'de su var ama hava (oksijen) yok ve çivi paslanmadı. Tüp 1'de hava var ama su yok ve yine paslanma yok. "
          "Paslanma için su ve oksijen birlikte gerekir; belediyenin iddiası çürür.",
          secenekler=[
              D("İddiayı çürütür: tüp 2'de su var ama hava yok ve çivi paslanmadı. Paslanma için su ve oksijen birlikte gerekir."),
              Y("İddiayı destekler: suyun olduğu her tüpte pas var.", "veri", "K4", "Tüp 2'de su var ama pas yok."),
              Y("Hiçbir şey söylemez; tüp 2 yanlış kurulmuştur.", "kanitsiz", "K4",
                "Tüp 2'nin yanlış kurulduğunu gösteren bir kanıt yok."),
              Y("Paslanma için yalnızca oksijen gerekir.", "veri", "K4",
                "Tüp 1'de oksijen var ama su yok ve paslanma olmadı."),
          ]),
        G("G5", "Çıkarım", "", "tekli", "kanit", "cikarim",
          "Tüp 3 ile tüp 4'ün karşılaştırması deniz kıyısındaki köprüler için ne öngörür?",
          "İki tüp arasındaki tek fark nedir?",
          "Tüp 3 ile 4 arasındaki tek fark tuzdur ve tuzlu sudaki çivi çok daha fazla paslandı. Kontrollü deneyler gerçek "
          "durumlar için öngörü yapmamızı sağlar: deniz kıyısındaki ya da kışın yollarına tuz dökülen köprüler daha hızlı "
          "paslanır.",
          secenekler=[
              D("Tuz paslanmayı hızlandırır; deniz kıyısındaki ya da kışın yollarına tuz dökülen köprüler daha hızlı paslanır."),
              Y("Tuz demiri korur.", "veri", "K4", "Tuzlu sudaki çivi daha çok paslandı."),
              Y("Tuz paslanmayı etkilemez; yalnızca suyu tuzlu yapar.", "veri", "K4",
                "Tüp 3 ile 4'ün sonuçları farklı; tek fark tuz."),
              Y("Deney yalnızca çiviler için geçerlidir; köprüler için bir şey söylenemez.", "kanitsiz", "K4",
                "Köprü de aynı metalden yapılmış; kontrollü deneyler bu tür öngörüler için yapılır."),
          ]),
        G("G6", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Demir kolay paslandığı hâlde neden hâlâ en çok kullanılan metaldir?",
          "Demiri güçlendirmek ve paslanmaya karşı korumak mümkün mü?",
          "RSC'ye göre bugün arıtılan metalin %90'ı demirdir. Demir bol bulunur ve ucuzdur; karbonla ve başka metallerle "
          "karıştırılarak çok güçlü çelikler yapılır. En az %10,5 krom içeren paslanmaz çelik korozyona çok dayanıklıdır; "
          "boya ve kaplama da demiri korur.",
          secenekler=[
              D("Bol ve ucuzdur; karbon ve başka metallerle çok güçlü çelikler yapılır. Boya, kaplama ya da paslanmaz çelik "
                "paslanmayı önler."),
              Y("Demir aslında paslanmaz; pas yalnızca kirdir.", "veri", "K5", "Pas analizi pasın bir demir oksit olduğunu gösterdi."),
              Y("Demir en hafif metal olduğu için.", "veri", "K3", "Demirin yoğunluğu 7,87 g/cm³; hafif bir metal değildir."),
              Y("Demir mıknatısa çekildiği için köprüleri sağlam tutar.", "iliski", "K1",
                "Mıknatısa çekilmek dayanıklılığın nedeni değildir."),
          ]),
        G("G7", "Sonuç", "", "tekli", "isim", "gozlem",
          "RSC kaydına (K6) göre hangisi doğrudur?",
          "Kayıtta Anadolu'dan söz ediliyor.",
          "RSC'ye göre demiri cevherinden ilk eritenler, MÖ 1500 civarında Anadolu'daki Hititlerdi ve bu yeni, daha güçlü "
          "metal onlara ekonomik ve siyasi güç verdi. Daha eski demir eşyalar ise göktaşı demirinden yapılmıştı.",
          secenekler=[
              D("Demiri cevherinden ilk eritenler Anadolu'daki Hititlerdi (MÖ 1500 civarı)."),
              Y("Demir ilk kez 1800'lerde laboratuvarda bulundu.", "veri", "K6", "Kayda göre demir binlerce yıldır kullanılıyor."),
              Y("Mısır'daki en eski demir eşyalar Hititlerden satın alındı.", "kanitsiz", "K6",
                "Kayıt bu eşyaların nikel içerdiğini, yani göktaşından geldiğini söylüyor."),
              Y("Demir Çağı, demirin paslanmasının keşfiyle başladı.", "iliski", "K6",
                "Demir Çağı, demirin cevherden eritilmeye başlanmasıyla başladı."),
          ]),
        G("G8", "Çıkarım", "Karşı kanıt", "tekli", "alternatif", "hipotez",
          "Belediye bu kez 'Tüp 1'de de hava var ve çivi paslanmadı; demek ki hava önemsiz' diyor. Bu çıkarımdaki hata nedir?",
          "Tüp 1'de neyin eksik olduğuna bak.",
          "Tüp 1'de su yok. Paslanma için su ve oksijen birlikte gerekir; havanın tek başına yetmemesi, havanın önemsiz "
          "olduğunu göstermez. Tüp 2 de havanın gerekli olduğunu gösteriyor.",
          secenekler=[
              D("Tüp 1'de su yok. Paslanma için su ve oksijen birlikte gerekir; havanın tek başına yetmemesi önemsiz olduğunu "
                "göstermez."),
              Y("Hata yok; hava gerçekten önemsizdir.", "veri", "K4", "Tüp 2'de hava yok ve çivi paslanmadı."),
              Y("Tüp 1'deki hava kirli olduğu için sonuç geçersizdir.", "kanitsiz", "K4",
                "Havanın kirli olduğunu gösteren bir kanıt yok."),
              Y("Tüp 1 ile tüp 4 karşılaştırılmalıydı.", "veri", "K4",
                "Tüp 1 ile 4 arasında hem su hem tuz farkı var; iki değişken birden değiştiği için hangisinin etkili "
                "olduğu anlaşılmaz."),
          ]),
    ]))

DOSYALAR.append(dict(
    id="D14", seviye=3, sira=4, baslik="Havuzdaki Koku", cevap="Cl",
    giris="Kapalı bir yüzme havuzunda öğrenciler gözlerinin yandığından ve havadaki keskin 'havuz kokusundan' şikâyet "
          "ediyor. Yönetici 'Demek ki suya çok fazla dezenfektan koymuşuz, azaltalım' diyor. Görevin: dezenfektandaki "
          "elementi bulmak ve yöneticinin çıkarımını kanıtlarla değerlendirmek.",
    kaynakca=[rsc(17, "chlorine", "Klor"),
              "ABD Hastalık Kontrol ve Önleme Merkezleri (CDC), havuzlarda göz tahrişi ve kloraminler — " + CDC],
    kanitlar=[
        ("K1", "konum", "Analiz raporu", "Dezenfektanın etken elementi 17. grupta ve 3. periyotta.", "", ""),
        ("K2", "fiziksel", "Saf hâlinin görünüşü", "Saf hâli sarı-yeşil, havadan yoğun ve boğucu kokulu bir gaz.", "", ""),
        ("K3", "tablo", "Havuz suyu ölçümleri (bir hafta)", "T1", "G1", ""),
        ("K4", "kimyasal", "CDC notu",
         "Bu element sudaki ter, idrar ve kirle birleşerek 'kloramin' adı verilen bileşikler oluşturur. Kloraminler zayıf "
         "dezenfektanlardır, havaya karışarak gözleri ve solunum yollarını tahriş eder. CDC'ye göre havuzda 'klor kokusu' "
         "diye algılanan koku çoğunlukla kloraminlerden gelir.", "G1", CDC),
        ("K5", "kullanim", "RSC kaydı",
         "Bu element bakterileri öldürür; içme suyunu ve havuz suyunu dezenfekte etmek için kullanılır. Üretilenin "
         "yaklaşık %20'si PVC plastiğinin yapımında kullanılır.", "G1", RSC + "17/chlorine"),
        ("K6", "isim", "Arşiv notu",
         "Adı Yunanca 'sarımsı yeşil' anlamına gelen 'chloros' kelimesinden gelir. İlk kez 1774'te Carl Wilhelm Scheele "
         "elde etti; Humphry Davy 1810'da onun bir element olduğunu açıkladı.", "G1", RSC + "17/chlorine"),
    ],
    tablolar={"T1": [
        ["Gün", "Serbest dezenfektan (mg/L)", "Kloramin (mg/L)", "Yüzücü sayısı", "Göz yanması şikâyeti"],
        ["Pazartesi", "1,8", "0,1", "40", "0"],
        ["Çarşamba", "1,7", "0,3", "120", "3"],
        ["Cumartesi", "1,2", "0,8", "310", "21"],
        ["Pazar", "0,9", "1,1", "350", "27"],
    ]},
    gorevler=[
        G("G1", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Analize (K1) ve saf hâlinin görünüşüne (K2) göre dezenfektanın etken elementi hangisi? Adını ya da sembolünü yaz.",
          "17. grubun 3. periyottaki elementi...",
          "Element klordur (Cl): 17. grubun 3. periyottaki elementi; saf hâli sarı-yeşil, boğucu kokulu bir gaz. Yeni "
          "kanıtlar açıldı: havuz ölçümleri (K3) ve CDC notu (K4).",
          hata_turu="veri"),
        G("G2", "Veri", "", "tekli", "kanit", "veri",
          "Tabloya (K3) göre hafta boyunca serbest dezenfektan miktarı nasıl değişti?",
          "İkinci sütunu baştan sona oku.",
          "Serbest dezenfektan 1,8 mg/L'den 0,9 mg/L'ye düştü; yani hafta boyunca azaldı.",
          secenekler=[
              D("Azaldı: 1,8 mg/L'den 0,9 mg/L'ye düştü."),
              Y("Arttı.", "veri", "K3", "Değerler 1,8'den 0,9'a iniyor."),
              Y("Değişmedi.", "veri", "K3", "Değerler 1,8'den 0,9'a iniyor."),
              Y("Karşılaştırılamaz, çünkü birim mg/L.", "birim", "K3",
                "Bütün ölçümler aynı birimle yapılmış; karşılaştırılabilir."),
          ]),
        G("G3", "Veri", "", "tekli", "kanit", "veri",
          "Göz yanması şikâyetleri tablodaki (K3) hangi değerlerle birlikte artıyor?",
          "Şikâyet sütunuyla her sütunu ayrı ayrı karşılaştır.",
          "Şikâyetler kloramin ve yüzücü sayısıyla birlikte artıyor; serbest dezenfektan ise azalıyor.",
          secenekler=[
              D("Kloramin ve yüzücü sayısıyla birlikte artıyor; serbest dezenfektan ise azalıyor."),
              Y("Serbest dezenfektanla birlikte artıyor.", "veri", "K3",
                "Şikâyet en çokken (Pazar) serbest dezenfektan en azdı."),
              Y("Hiçbir değerle birlikte değişmiyor.", "veri", "K3", "Şikâyetler hafta boyunca belirgin biçimde arttı."),
              Y("Yalnızca günün adıyla ilgili; hafta sonları gözler daha hassastır.", "kanitsiz", "K3",
                "Bu iddiayı destekleyen bir kanıt yok."),
          ]),
        G("G4", "Hipotez", "", "tekli", "alternatif", "hipotez",
          "Yöneticinin 'çok fazla dezenfektan koymuşuz' hipotezi verilerle uyumlu mu?",
          "Hipotez doğru olsaydı, şikâyetin en çok olduğu gün serbest dezenfektan nasıl olmalıydı?",
          "Hipotez doğru olsaydı şikâyetler serbest dezenfektanla birlikte artardı. Oysa şikâyet en çokken serbest "
          "dezenfektan en azdı. Veriler, şikâyetlerin kloraminlerden kaynaklandığı hipoteziyle uyumlu.",
          secenekler=[
              D("Hayır; şikâyetler arttıkça serbest dezenfektan azalıyor. Veriler kloramin hipoteziyle uyumlu."),
              Y("Evet; koku varsa dezenfektan fazladır.", "kanitsiz", "K4",
                "CDC'ye göre 'klor kokusu' diye algılanan koku çoğunlukla kloraminlerden gelir."),
              Y("Evet; çünkü bu element zehirli bir gazdır.", "iliski", "K2",
                "Saf element gerçekten zehirli bir gazdır, ama havuzda saf gaz değil, suda çözünmüş bileşikleri vardır. "
                "Veriler de fazla dezenfektanı göstermiyor."),
              Y("Karar verilemez; yalnızca dört gün ölçülmüş.", "veri", "K3",
                "Dört gün sınırlı bir veri, ama hipotezle açıkça çelişiyor: şikâyet en çokken dezenfektan en azdı."),
          ]),
        G("G5", "Kanıt", "", "tekli", "kanit", "cikarim",
          "Korelasyon nedensellik değildir. Şikâyetlerin yüzücü sayısıyla birlikte artması 'yüzücüler göz yanmasına neden "
          "oluyor' demek midir?",
          "CDC notu (K4) kloraminlerin nasıl oluştuğunu söylüyor.",
          "Birlikte artmak doğrudan neden olmak değildir. CDC notuna göre yüzücülerin teri ve idrarı dezenfektanla "
          "birleşip kloramin oluşturuyor; yüzücü sayısı kloramin oluşumunu artırarak dolaylı bir etki yapıyor olabilir. "
          "Bunu doğrulamak için kontrollü bir deney gerekir.",
          secenekler=[
              D("Doğrudan değil; yüzücülerin teri ve idrarı kloramin oluşumunu artırarak dolaylı bir etki yapıyor olabilir. "
                "Doğrulamak için kontrollü bir deney gerekir."),
              Y("Evet; yüzücüler gözleri doğrudan yakar.", "kanitsiz", "K4", "Bu iddiayı destekleyen bir kanıt yok."),
              Y("Hayır; yüzücü sayısının hiçbir etkisi olamaz.", "veri", "K4",
                "CDC notu, yüzücülerin terinin ve idrarının kloramin oluşumuna katkı yaptığını söylüyor."),
              Y("Evet; korelasyon her zaman nedenselliği kanıtlar.", "kanitsiz", "K3",
                "İki niceliğin birlikte değişmesi, birinin diğerine neden olduğunu kanıtlamaz."),
          ]),
        G("G6", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Bu verilere göre göz yanmasını azaltmak için en bilimsel öneri hangisi?",
          "Kloraminlerin oluşmasını nasıl azaltabiliriz?",
          "CDC'ye göre teri, kiri ve idrarı sudan uzak tutmak kloramin oluşumunu önler: yüzücüler girmeden önce duş "
          "almalıdır. Kapalı havuzlarda havalandırma, havaya karışan kloraminleri uzaklaştırır. Dezenfektan mikropları "
          "öldürdüğü için azaltılmamalı, önerilen aralıkta tutulmalıdır.",
          secenekler=[
              D("Yüzücülerin girmeden önce duş almasını sağlamak, havalandırmayı artırmak ve dezenfektanı önerilen aralıkta tutmak."),
              Y("Dezenfektanı tamamen kesmek.", "iliski", "K5",
                "Dezenfektan mikropları öldürür; kesilirse su hastalık yayabilir."),
              Y("Suya daha çok tuz atmak.", "kanitsiz", "", "Tuzun kloramini azalttığını gösteren bir kanıt yok."),
              Y("Koku kaybolana kadar havuza parfüm eklemek.", "kanitsiz", "",
                "Parfüm kokuyu örter ama kloraminleri ve göz yanmasını ortadan kaldırmaz."),
          ]),
        G("G7", "Sonuç", "", "tekli", "isim", "gozlem",
          "Klor adını nereden alır? (K6)",
          "Saf gazın rengini hatırla.",
          "RSC'ye göre klor adı Yunanca 'sarımsı yeşil' anlamındaki 'chloros' kelimesinden gelir; saf gazın rengi "
          "nedeniyle. Klorofil de aynı Yunanca kökten (yeşil) adını alır, ama klor içermez.",
          secenekler=[
              D("Yunanca 'sarımsı yeşil' anlamındaki 'chloros' kelimesinden; saf gazın rengi nedeniyle"),
              Y("Bitkilerdeki klorofilden", "iliski", "K6",
                "Klorofil de aynı Yunanca kökten (yeşil) adını alır, ama klorofil klor içermez."),
              Y("Kloramin bileşiklerinden", "veri", "K6", "Kloraminler adını elementten alır, tersi değil."),
              Y("Onu elde eden Scheele'nin memleketinden", "kanitsiz", "K6", "Arşiv notunda böyle bir bilgi yok."),
          ]),
        G("G8", "Çıkarım", "Gerekçe", "tekli", "gerekce", "gerekce",
          "Yöneticiye yazacağın kısa raporda en güçlü gerekçe hangisi?",
          "Güçlü gerekçe hem verilere hem de güvenilir bir kaynağa dayanır.",
          "Güçlü bir rapor ölçümlere ve güvenilir bir kaynağa dayanır, yöneticinin hipotezinin verilerle neden çeliştiğini "
          "açıkça gösterir.",
          secenekler=[
              D("Şikâyetlerin arttığı günlerde serbest dezenfektan azalmış, kloramin artmış. CDC'ye göre 'klor kokusu' "
                "çoğunlukla kloraminlerden gelir. Sorun fazla dezenfektan değil, ter ve idrarla oluşan kloraminler."),
              Y("Koku keskin olduğu için dezenfektan azaltılmalı.", "kanitsiz", "K4",
                "Kokunun kaynağı dezenfektanın kendisi değil, kloraminlerdir."),
              Y("Pazar günü 350 kişi yüzdüğü için havuz kapatılmalı.", "kanitsiz", "K3",
                "Bu bir öneri, gerekçe değil; ayrıca sorunun kaynağını açıklamıyor."),
              Y("Kloramin bir element olduğu için tehlikelidir.", "veri", "K4", "Kloraminler element değil, bileşiktir."),
          ]),
    ]))

DOSYALAR.append(dict(
    id="D15", seviye=3, sira=5, baslik="Tavandaki Küçük Kutu", cevap="Am",
    giris="Bir evin tavanındaki duman dedektörünün içinde küçük bir etiket var: 'Radyoaktif madde içerir.' Ev sahibi panik "
          "içinde birimi aradı: 'Evimde radyoaktif madde mi var? Bu uranyum mu, plütonyum mu?' Görevin: dedektördeki "
          "elementi kanıtlarla bulmak ve tehlikenin gerçek boyutunu bilimsel olarak değerlendirmek.",
    kaynakca=[rsc(95, "americium", "Amerikyum"), rsc(94, "plutonium", "Plütonyum"), rsc(96, "curium", "Küriyum"),
              "ABD Çevre Koruma Ajansı (EPA), iyonlaşmalı duman dedektörlerinde amerikyum — " + EPA,
              "İzotopların yarı ömürleri: yaklaşık standart değerler"],
    kanitlar=[
        ("K1", "deney", "Radyasyon ölçümü",
         "Kaynak alfa parçacıkları yayıyor. Kaynağın önüne bir kâğıt konunca ölçülen alfa radyasyonu neredeyse sıfıra iniyor.",
         "", ""),
        ("K2", "konum", "Element analizi", "Element 7. periyotta ve f bloğunda (aktinitler).", "", ""),
        ("K3", "deney", "Teknik belge",
         "Dedektör üreticisinin belgesine göre kaynak, yarı ömrü yaklaşık 432 yıl olan bir izotop. Doğada bulunmaz; "
         "nükleer reaktörlerde plütonyumun nötronlarla bombardımanıyla üretilir.", "", RSC + "95/americium"),
        ("K4", "tablo", "Bazı aktinit izotoplarının yarı ömürleri", "T1", "", "Standart değerler"),
        ("K5", "isim", "Arşiv notu",
         "Element 1944'te Chicago Üniversitesi'nde Glenn Seaborg ve ekibi tarafından üretildi ve ilk kez üretildiği "
         "kıtanın adını aldı. İlginç bir ayrıntı: periyodik tabloda kendisinden sonra gelen küriyumdan sonra keşfedildi.",
         "G4", RSC + "95/americium"),
        ("K6", "kullanim", "EPA notu",
         "İyonlaşmalı duman dedektörlerinde bu elementin küçük bir kaynağı bulunur. Yaydığı alfa parçacıkları, "
         "dedektördeki iki levha arasındaki havayı iyonlaştırır ve küçük bir akım oluşur. Duman girince akım azalır ve "
         "alarm çalar. Kaynak metal folyo ve seramikle kaplıdır; doğru kullanıldığında radyasyon riski oluşturmaz.",
         "G4", EPA),
    ],
    tablolar={"T1": [
        ["İzotop", "Yarı ömür"],
        ["Uranyum-238", "Yaklaşık 4,5 milyar yıl"],
        ["Plütonyum-239", "Yaklaşık 24 100 yıl"],
        ["Amerikyum-241", "432 yıl"],
        ["Küriyum-244", "Yaklaşık 18 yıl"],
    ]},
    gorevler=[
        G("G1", "Gözlem", "", "tekli", "kanit", "gozlem",
          "'Radyoaktif madde içerir' etiketi tek başına neyi kanıtlar?",
          "Etiket hangi elementin olduğunu ya da ne kadar tehlikeli olduğunu söylüyor mu?",
          "Etiket yalnızca kaynağın radyoaktif olduğunu söyler; hangi element olduğunu ya da ne kadar tehlikeli olduğunu "
          "söylemez. Bunlar için ölçüm ve analiz gerekir.",
          secenekler=[
              D("Yalnızca kaynağın radyoaktif olduğunu; hangi element olduğunu ya da ne kadar tehlikeli olduğunu söylemez."),
              Y("Kaynağın uranyum olduğunu", "kanitsiz", "K2",
                "Radyoaktif elementlerin sayısı çok; etiket hangisi olduğunu söylemiyor."),
              Y("Evin tehlikeli derecede radyasyonlu olduğunu", "kanitsiz", "K1",
                "Etiket radyasyonun ne kadar olduğu hakkında bilgi vermez."),
              Y("Kaynağın patlayıcı olduğunu", "iliski", "K1", "Radyoaktif olmak patlayıcı olmak demek değildir."),
          ]),
        G("G2", "Veri", "", "tablo", "kanit", "veri",
          "Analize (K2) göre aday olabilecek bütün elementleri periyodik tabloda işaretle.",
          "7. periyodun f bloğu, tablonun altındaki ikinci satırdır: 89'dan 103'e.",
          "7. periyodun f bloğunda 15 element var: aktinyumdan (89) lavrensiyuma (103) kadar. Bunlara aktinitler denir.",
          dogru="Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr", hata_turu="veri"),
        G("G3", "Veri", "", "tekli", "kanit", "veri",
          "Teknik belgedeki yarı ömür (K3) ve tablo (K4) hangi elementi gösteriyor?",
          "Tabloda yarı ömrü 432 yıl olan izotop hangisi?",
          "Belgedeki 432 yıllık yarı ömür amerikyum-241'e ait. Belgede plütonyumun adı geçiyor, ama hammadde olarak: "
          "amerikyum, plütonyumun reaktörde nötronlarla bombardımanıyla üretilir.",
          secenekler=[
              D("Amerikyum: amerikyum-241'in yarı ömrü 432 yıl."),
              Y("Uranyum: en bilinen radyoaktif element olduğu için", "kanitsiz", "K4",
                "Bir elementin tanınmış olması kanıt değildir; uranyum-238'in yarı ömrü 4,5 milyar yıl."),
              Y("Plütonyum: belgede plütonyumun adı geçtiği için", "veri", "K3",
                "Belgede plütonyumun hammadde olduğu yazıyor; ürün plütonyum değil."),
              Y("Küriyum: yarı ömrü kısa olduğu için daha güvenli", "veri", "K4",
                "Küriyum-244'ün yarı ömrü yaklaşık 18 yıl; belgedeki 432 yılla uyuşmuyor."),
          ]),
        G("G4", "Çıkarım", "", "yaz", "kimlik", "cikarim",
          "Dedektördeki element hangisi? Adını ya da sembolünü yaz.",
          "Yarı ömrü 432 yıl olan izotopun elementi...",
          "Element amerikyumdur (Am); dedektörde amerikyum-241 kullanılır.",
          hata_turu="kanitsiz"),
        G("G5", "Kanıt", "", "tekli", "kanit", "cikarim",
          "Kâğıt deneyi (K1) ve EPA notu (K6) birlikte değerlendirildiğinde dedektörün tehlikesi hakkında ne söylenebilir?",
          "Alfa parçacıkları ne kadar uzağa gidebiliyor?",
          "Alfa parçacıkları kâğıt gibi ince bir engelle bile durur. EPA'ya göre kaynak metal folyo ve seramikle kaplıdır; "
          "bu yüzden dedektör doğru kullanıldığında radyasyon riski oluşturmaz.",
          secenekler=[
              D("Alfa parçacıkları kâğıt gibi ince bir engelle bile durur; kaynak kaplı olduğu için dedektör doğru "
                "kullanıldığında radyasyon riski oluşturmaz."),
              Y("Radyoaktif olan her şey her durumda tehlikelidir.", "kanitsiz", "K6",
                "Tehlike radyasyonun türüne, miktarına ve korunmaya bağlıdır."),
              Y("Alfa parçacıkları duvarları geçer; dedektör evin her yerini etkiler.", "veri", "K1",
                "Kâğıt deneyi alfa parçacıklarının ince bir kâğıtla bile durduğunu gösteriyor."),
              Y("Dedektör radyasyonla dumanı yok eder.", "iliski", "K6",
                "Dedektör dumanı yok etmez; dumanın akımı azaltmasını algılar."),
          ]),
        G("G6", "Çıkarım", "", "tekli", "ozellik_kullanim", "cikarim",
          "Duman dedektöründe amerikyumun hangi özelliği işe yarar?",
          "EPA notunu (K6) oku.",
          "Amerikyumun yaydığı alfa parçacıkları havayı iyonlaştırır ve iki levha arasında küçük bir akım oluşur. Duman "
          "girince akım azalır ve alarm çalar.",
          secenekler=[
              D("Yaydığı alfa parçacıklarının havayı iyonlaştırıp küçük bir akım oluşturması; duman akımı azaltınca alarm çalar."),
              Y("Amerikyumun dumanı görüp ışık saçması", "iliski", "K6", "Amerikyum dumanı 'görmez'; akımdaki değişim algılanır."),
              Y("Amerikyumun yangında eriyip devreyi kapatması", "veri", "",
                "Amerikyumun erime noktası 1176 °C; dedektör bu şekilde çalışmaz."),
              Y("Amerikyumun mıknatısa çekilmesi", "kanitsiz", "K6", "Notta mıknatıstan söz edilmiyor."),
          ]),
        G("G7", "Sonuç", "", "tekli", "isim", "gozlem",
          "Amerikyumun adı nereden gelir? (K5)",
          "Element ilk kez nerede üretildi?",
          "RSC'ye göre amerikyum, ilk kez üretildiği Amerika'nın adını taşır. Ekibin lideri Glenn Seaborg'un adı ise "
          "106 numaralı element seaborgiyuma verildi.",
          secenekler=[
              D("İlk kez üretildiği kıta olan Amerika'dan"),
              Y("Onu üreten ekibin liderinin adından", "veri", "K5",
                "Ekibin lideri Glenn Seaborg'du ama ad bir kıtadan geliyor."),
              Y("Doğada en çok Amerika'da bulunduğu için", "veri", "K3", "Amerikyum doğada bulunmaz; reaktörde üretilir."),
              Y("Amerika'daki bir madenden çıkarıldığı için", "veri", "K3", "Amerikyum madenden çıkarılmaz; reaktörde üretilir."),
          ]),
        G("G8", "Sonuç", "Sonuç", "tekli", "gerekce", "gerekce",
          "Ev sahibine bilimsel yanıtın hangisi olmalı?",
          "Yanıt hem elementin kimliğini hem de tehlikenin gerçek boyutunu kanıtlarla anlatmalı.",
          "Güçlü bir yanıt kanıtlara dayanır: Dedektördeki kaynak uranyum ya da plütonyum değil, amerikyum-241. Alfa "
          "parçacıkları çok kısa mesafede durur ve kaynak kaplıdır. Dedektör doğru kullanıldığında güvenlidir ve hayat "
          "kurtarır.",
          secenekler=[
              D("Kaynak uranyum ya da plütonyum değil, amerikyum-241. Alfa parçacıkları çok kısa mesafede durur ve kaynak "
                "kaplıdır. Dedektör doğru kullanıldığında güvenlidir; bozulursa açılmamalı, kurallara uygun atılmalı."),
              Y("Dedektör radyoaktif olduğu için hemen sökülüp atılmalı.", "kanitsiz", "K6",
                "Kanıtlar dedektörün doğru kullanıldığında risk oluşturmadığını gösteriyor; dedektör hayat kurtarır."),
              Y("Dedektördeki madde plütonyumdur.", "veri", "K3", "Belgedeki yarı ömür plütonyum-239'a değil, amerikyum-241'e ait."),
              Y("Radyasyon tamamen zararsızdır; kaynağı elle tutmakta da sakınca yok.", "veri", "K6",
                "Kaynak kaplı olduğu için güvenlidir; kaplama açılmamalı ve kaynağa dokunulmamalıdır."),
          ]),
    ]))
