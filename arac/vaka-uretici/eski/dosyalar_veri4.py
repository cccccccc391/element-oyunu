# -*- coding: utf-8 -*-
"""Element Dosyalari: Seviye 4 (Bilimsel Savunma) dosyalari, D16-D20.

Bu seviyede hazir secenekler olabildigince kaldirildi: gorevler yazili cevap, kanit secimi ve
juriye savunma bicimindedir.
"""

from dosyalar_veri import D, G, RSC, S, Y, rsc
from dosyalar_veri2 import ALKALI_TABLO

DOSYALAR = []

DOSYALAR.append(dict(
    id="D16", seviye=4, sira=1, baslik="Dokunmatik Ekranın Görünmez Teli", cevap="In",
    giris="Bir telefon ekranının cam katmanında gözle görülmeyen ama elektriği ileten çok ince bir kaplama var. Kaplamadaki "
          "metalin adı üretici belgesinde silinmiş. Görevin: metali bulmak ve jüriye savunmak. Bu dosyada hazır seçenek yok.",
    kaynakca=[rsc(49, "indium", "İndiyum"), rsc(13, "aluminium", "Alüminyum"), rsc(31, "gallium", "Galyum"),
              rsc(81, "thallium", "Talyum")],
    kanitlar=[
        ("K1", "kullanim", "Üretici belgesi",
         "Kaplama, '... kalay oksit' adlı saydam ve elektriği ileten bir maddeden yapılmış; ilk kelime silinmiş. Madde "
         "cama sıkıca yapışıyor.", "", ""),
        ("K2", "konum", "Analiz raporu", "Kaplamadaki metal 13. grupta ve 5. periyotta.", "", ""),
        ("K3", "erime_kaynama", "Erime noktası ölçümü", "Kaplamadan ayrılan saf metal 156,6 °C'de eriyor.", "", ""),
        ("K4", "fiziksel", "Saf metalin görünüşü", "Yumuşak, gümüşi bir metal; havada ve suda kararlı.", "", ""),
        ("K5", "tarih", "Keşif kaydı",
         "1863'te Ferdinand Reich, bir çinko mineralinde talyum ararken spektroskobunda tanımadığı çizgiler gördü. Reich "
         "renk körü olduğu için spektrumu Hieronymus Richter'e gösterdi; Richter parlak mor-çivit renkli bir çizgi gördü. "
         "Elementin adı bu çizginin renginden gelir.", "", RSC + "49/indium"),
        ("K6", "tablo", "13. grup metallerinden bazıları", "T1", "", "RSC Periyodik Tablo"),
    ],
    tablolar={"T1": [
        ["Metal", "Periyot", "Erime noktası (°C)", "Yoğunluk (g/cm³)"],
        ["Alüminyum", "3", "660,3", "2,70"],
        ["Galyum", "4", "29,8", "5,91"],
        ["İndiyum", "5", "156,6", "7,31"],
        ["Talyum", "6", "304", "11,8"],
    ]},
    gorevler=[
        G("G1", "Çıkarım", "İddia", "yaz", "kimlik", "cikarim",
          "Kaplamadaki metal hangisi? Adını ya da sembolünü yaz.",
          "Analiz raporundaki grup ve periyodu periyodik tabloda bul.",
          "Metal indiyumdur (In): 13. grubun 5. periyottaki elementi. Erime noktası (156,6 °C) da indiyumla uyuşuyor. "
          "Silinmiş kelime 'indiyum'du: indiyum kalay oksit.",
          hata_turu="kanitsiz"),
        G("G2", "Kanıt", "Kanıt", "kanit", "kanit", "kanit",
          "İddianı destekleyen ve diğer 13. grup metallerini eleyen kanıtları seç. Tek başına ayırt edici olmayan kanıtları "
          "seçme.",
          "İki bağımsız kanıt: biri konum, biri ölçülen bir değer.",
          "Analiz raporu (K2) konumu, erime noktası ölçümü (K3) de tabloyla (K6) karşılaştırınca aynı metali gösteriyor: "
          "iki bağımsız kanıt aynı sonuca varıyor. Gümüşi ve yumuşak olmak (K4) birçok metalde görülür; keşif kaydı (K5) "
          "bu örnek hakkında bir ölçüm değildir.",
          dogru="K2 K3 (K6)", hata_turu="kanitsiz"),
        G("G3", "Sonuç", "", "yaz", "sembol", "cikarim",
          "İndiyumun sembolünü yaz.",
          "Sembol iki harfli; ikinci harf küçük.",
          "İndiyumun sembolü In'dir.",
          hata_turu="veri"),
        G("G4", "Sonuç", "", "yaz", "isim", "gozlem",
          "Elementin adı, Richter'in gördüğü çizginin renginden gelir (K5). Bu renk neydi? Tek kelimeyle yaz.",
          "Keşif kaydında rengin adı geçiyor.",
          "RSC'ye göre indiyum adını Latincede 'çivit, mor' anlamına gelen 'indicum' kelimesinden alır; çünkü "
          "spektrumunda parlak mor-çivit renkli bir çizgi vardır. İlginçtir ki onu ilk fark eden Reich renk körüydü.",
          dogru="çivit|çivit mavisi|çivit rengi|mor|menekşe|indigo|lacivert|mor-çivit", hata_turu="veri"),
        G("G5", "Çıkarım", "", "kanit", "ozellik_kullanim", "kanit",
          "Dokunmatik ekranlarda indiyum kalay oksidin kullanılmasını açıklayan özellikleri gösteren kanıtları seç.",
          "Bir dokunmatik ekran kaplamasının hangi üç özelliği olmalı?",
          "RSC'ye göre indiyumun çoğu, dokunmatik ekranlar, düz ekran televizyonlar ve güneş panelleri için indiyum kalay "
          "oksit yapımında kullanılır; çünkü bu madde elektriği iletir, cama sıkıca yapışır ve saydamdır. Bu bilgiler "
          "üretici belgesinde (K1) var.",
          dogru="K1", hata_turu="iliski"),
        G("G6", "Hipotez", "Karşı kanıt", "yaz", "alternatif", "hipotez",
          "Galyum da 13. gruptadır ve erime noktası düşüktür. Galyum hipotezini eleyen bir kanıtın numarasını yaz "
          "(örnek: K4).",
          "Galyum 4. periyotta ve 29,8 °C'de erir.",
          "Galyum iki kanıtla elenir: analiz raporu (K2) metalin 5. periyotta olduğunu söylüyor, galyum ise 4. periyotta; "
          "ölçülen erime noktası (K3) 156,6 °C, galyumunki ise 29,8 °C.",
          dogru="K2|K3", hata_turu="kanitsiz"),
        G("G7", "Sonuç", "Sonuç", "savunma", "gerekce", "gerekce",
          "Jüriye savunmanı yaz: \"Kaplamadaki metalin … olduğunu düşünüyorum çünkü…\" İddianı, kanıtlarını, gerekçeni ve "
          "en güçlü alternatif hipotezi neden reddettiğini yaz.",
          "",
          "Kaplamadaki metalin indiyum olduğunu düşünüyorum çünkü analiz raporu metalin 13. grupta ve 5. periyotta "
          "olduğunu gösteriyor; bu konumdaki tek element indiyum. Bağımsız bir kanıt da aynı sonucu veriyor: ölçülen erime "
          "noktası 156,6 °C ve tabloya göre bu indiyuma ait. En ciddi alternatif galyumdu, çünkü o da 13. grupta ve erime "
          "noktası düşük; ama galyum 4. periyotta ve 29,8 °C'de erir. Ekranda kullanılmasının nedeni, indiyum kalay "
          "oksidin saydam olması, elektriği iletmesi ve cama sıkıca yapışmasıdır."),
    ]))

DOSYALAR.append(dict(
    id="D17", seviye=4, sira=2, baslik="Kalça Protezi", cevap="Ti",
    giris="Bir ortopedi kliniği, kalça protezinde kullanılan metalin hangi element olduğunu ve neden seçildiğini öğrencilere "
          "anlatmak istiyor. Birim, protezden alınan bir örnek üzerinde ölçümler yaptı. Hazır seçenek yok; kanıtları sen "
          "değerlendireceksin.",
    kaynakca=[rsc(22, "titanium", "Titanyum"), rsc(13, "aluminium", "Alüminyum"), rsc(26, "iron", "Demir"),
              rsc(28, "nickel", "Nikel"), rsc(29, "copper", "Bakır")],
    kanitlar=[
        ("K1", "yogunluk", "Yoğunluk ölçümü", "4,5 ± 0,1 g/cm³", "", ""),
        ("K2", "fiziksel", "Görünüş ve davranış", "Sert, parlak ve çok güçlü bir metal; mıknatısa çekilmiyor.", "", ""),
        ("K3", "kimyasal", "Korozyon testi",
         "Örnek, deniz suyuna benzeyen tuzlu bir suda bir ay bekletildi; yüzeyinde hiçbir bozulma olmadı.", "", ""),
        ("K4", "tablo", "Bazı yapı metalleri", "T1", "", "RSC Periyodik Tablo"),
        ("K5", "kullanim", "RSC kaydı",
         "Bu metal çelik kadar güçlüdür ama çok daha az yoğundur. Deniz suyunda korozyona çok dayanıklıdır. Kemikle iyi "
         "kaynaştığı için kalça eklemlerinde ve diş implantlarında kullanılır.", "G1", RSC + "22/titanium"),
        ("K6", "isim", "Arşiv notu",
         "Element 1791'de William Gregor tarafından Cornwall'daki siyah bir kumda fark edildi. 1795'te Martin Heinrich "
         "Klaproth, Yunan mitolojisinde Toprak Ana'nın oğulları olan Titanlar'dan esinlenerek ona adını verdi.", "G1",
         RSC + "22/titanium"),
    ],
    tablolar={"T1": [
        ["Metal", "Yoğunluk (g/cm³)", "Erime noktası (°C)", "Mıknatısa çekilir mi?"],
        ["Alüminyum", "2,70", "660", "Hayır"],
        ["Titanyum", "4,506", "1670", "Hayır"],
        ["Demir", "7,87", "1538", "Evet"],
        ["Nikel", "8,90", "1455", "Evet"],
        ["Bakır", "8,96", "1085", "Hayır"],
    ]},
    gorevler=[
        G("G1", "Çıkarım", "İddia", "yaz", "kimlik", "cikarim",
          "Protezin metali hangisi? Adını ya da sembolünü yaz.",
          "Ölçülen yoğunluğu tablodaki değerlerle karşılaştır.",
          "Metal titanyumdur (Ti): yoğunluğu (4,5 ± 0,1) tablodaki metallerden yalnızca titanyumla (4,506) uyuşuyor ve "
          "mıknatısa çekilmiyor.",
          hata_turu="kanitsiz"),
        G("G2", "Kanıt", "Kanıt", "kanit", "kanit", "kanit",
          "İddianı destekleyen ve diğer adayları eleyen kanıtları seç.",
          "Hangi ölçüm tablodaki tek bir metalle uyuşuyor?",
          "Yoğunluk ölçümü (K1) tablodaki (K4) değerlerle karşılaştırılınca yalnızca titanyumu gösteriyor. Mıknatısa "
          "çekilmemesi (K2) demiri ve nikeli eler, korozyon testi (K3) de sonuçla uyumludur. RSC kaydı (K5) ve arşiv notu "
          "(K6) bu örnek üzerinde yapılmış ölçümler değildir.",
          dogru="K1 K4 (K2) (K3)", hata_turu="kanitsiz"),
        G("G3", "Çıkarım", "", "kanit", "ozellik_kullanim", "kanit",
          "Titanyumun kalça protezinde kullanılmasını açıklayan özellikleri gösteren kanıtları seç.",
          "Vücut sıvıları tuzludur. Protez kemiğe tutunmalı ve sağlam olmalı.",
          "Vücut sıvıları tuzludur; protezin korozyona dayanıklı olması gerekir (K3). RSC'ye göre titanyum kemikle iyi "
          "kaynaşır, çelik kadar güçlü ama çok daha hafiftir (K5). Sağlamlığı (K2) ve hafifliği (K1) de bu seçimi destekler.",
          dogru="K3 K5 (K1) (K2)", hata_turu="iliski"),
        G("G4", "Veri", "", "yaz", "kanit", "veri",
          "Tablodaki (K4) yoğunluklara göre aynı boyuttaki bir demir parça, titanyum parçadan kaç kat ağırdır? Sonucu bir "
          "ondalık basamakla yaz (örnek: 2,3).",
          "Demirin yoğunluğunu titanyumunkine böl.",
          "7,87 ÷ 4,506 ≈ 1,75. Aynı boyuttaki bir demir parça titanyumdan yaklaşık 1,7 kat ağırdır. Bu hafiflik hem "
          "uçaklarda hem de vücutta taşınan protezlerde önemli bir avantajdır.",
          dogru="1,7|1.7|1,75|1.75|1,8|1.8", hata_turu="birim"),
        G("G5", "Sonuç", "", "yaz", "isim", "gozlem",
          "Titanyum adını Yunan mitolojisindeki hangi varlıklardan alır? (K6)",
          "Arşiv notunu oku.",
          "RSC'ye göre titanyum adını Yunan mitolojisinde Toprak Ana'nın oğulları olan Titanlar'dan alır. Güçlü bir "
          "metale yakışan bir ad.",
          dogru="Titanlar|Titan|Titanlardan|Titanlar'dan", hata_turu="veri"),
        G("G6", "Sonuç", "Sonuç", "savunma", "gerekce", "gerekce",
          "Jüriye savunmanı yaz: protezdeki metalin ne olduğunu, bunu hangi kanıtlarla bildiğini ve neden protez için "
          "uygun olduğunu açıkla.",
          "",
          "Protezdeki metalin titanyum olduğunu düşünüyorum çünkü ölçtüğümüz yoğunluk 4,5 ± 0,1 g/cm³ ve tablodaki "
          "metallerden yalnızca titanyum (4,506) bu aralıkta. Mıknatısa çekilmemesi demiri ve nikeli eliyor. Alüminyum da "
          "mıknatısa çekilmez ama yoğunluğu 2,70 g/cm³; ölçümümüzle uyuşmuyor. Titanyum protez için uygun, çünkü tuzlu suda "
          "bir ay bozulmadı (vücut sıvıları da tuzludur), kemikle iyi kaynaşır ve çelik kadar güçlü olduğu hâlde demirden "
          "yaklaşık 1,7 kat hafiftir."),
    ]))

DOSYALAR.append(dict(
    id="D18", seviye=4, sira=3, baslik="Kararan Kaşık", cevap="Ag",
    giris="Bir müzeye bağışlanan eski bir kaşık ve bir ayna zamanla kararmış. Müze, ikisinin de aynı değerli metali "
          "içerdiğini düşünüyor. Görevin: metali bulmak ve kararmanın nedenini jüriye açıklamak. Hazır seçenek yok.",
    kaynakca=[rsc(47, "silver", "Gümüş"), rsc(29, "copper", "Bakır"), rsc(79, "gold", "Altın")],
    kanitlar=[
        ("K1", "konum", "Analiz raporu", "Kaşıktaki ana metal 11. grupta.", "", ""),
        ("K2", "yogunluk", "Kaşığın yoğunluğu", "10,4 ± 0,1 g/cm³", "", ""),
        ("K3", "kimyasal", "Kararma analizi",
         "Kaşığın üzerindeki siyah tabaka bir sülfür bileşiği; havadaki kükürtlü bileşiklerle tepkimeden oluşmuş.", "", ""),
        ("K4", "tablo", "11. grup metalleri", "T1", "", "RSC Periyodik Tablo"),
        ("K5", "fiziksel", "Aynanın arka yüzü",
         "Aynanın arkasındaki yansıtıcı tabaka da aynı metalden; bu metal bilinen en iyi görünür ışık yansıtıcısıdır.", "", ""),
        ("K6", "kullanim", "RSC kaydı",
         "Çatal-kaşık yapımında kullanılan 'sterling' gümüş %92,5 gümüş içerir; geri kalanı bakır ya da başka bir "
         "metaldir. Gümüş bromür ve iyodür ışığa duyarlı oldukları için fotoğrafçılığın tarihinde çok önemliydi.", "G1",
         RSC + "47/silver"),
        ("K7", "isim", "Arşiv notu",
         "Sembol Ag, Latince 'argentum' (gümüş) kelimesinden gelir; Arjantin'in adı da bu kelimeden türemiştir. RSC'ye "
         "göre gümüş madenciliği MÖ 3000 civarında bugünkü Türkiye ve Yunanistan topraklarında başladı.", "G1",
         RSC + "47/silver"),
    ],
    tablolar={"T1": [
        ["Metal", "Yoğunluk (g/cm³)", "Rengi", "Havada kararır mı?"],
        ["Bakır", "8,96", "Kırmızımsı", "Zamanla yeşil bir tabaka oluşturabilir"],
        ["Gümüş", "10,5", "Parlak beyaz", "Kükürtlü bileşiklerle yavaşça siyahlaşır"],
        ["Altın", "19,3", "Sarı", "Kararmaz"],
        ["Röntgenyum", "—", "—", "Laboratuvarda yalnızca birkaç atom üretildi"],
    ]},
    gorevler=[
        G("G1", "Çıkarım", "İddia", "yaz", "kimlik", "cikarim",
          "Kaşığın ana metali hangisi? Adını ya da sembolünü yaz.",
          "Ölçülen yoğunluğa ve kararmanın biçimine bak.",
          "Metal gümüştür (Ag): 11. grupta, yoğunluğu gümüşünkine çok yakın ve kükürtlü bileşiklerle siyahlaşıyor.",
          hata_turu="kanitsiz"),
        G("G2", "Sonuç", "", "yaz", "sembol", "cikarim",
          "Gümüşün sembolünü yaz.",
          "Sembol Latince bir kelimeden gelir.",
          "Gümüşün sembolü Ag'dir; Latince 'argentum' kelimesinden gelir.",
          hata_turu="veri"),
        G("G3", "Kanıt", "Kanıt", "kanit", "kanit", "kanit",
          "Bakır ve altın hipotezlerini eleyen kanıtları seç.",
          "Yoğunluk ölçümünü tabloyla karşılaştır.",
          "Yoğunluk ölçümü (K2) tablodaki (K4) değerlerle karşılaştırılınca bakırı (8,96) ve altını (19,3) eler. Kararmanın "
          "siyah bir sülfürle olması (K3) da gümüşe uyar: altın kararmaz, bakır ise yeşil bir tabaka oluşturur. 11. grupta "
          "olmak (K1) üç metal için de geçerli olduğundan ayırt edici değildir.",
          dogru="K2 K4 (K3)", hata_turu="kanitsiz"),
        G("G4", "Veri", "", "yaz", "kanit", "veri",
          "RSC kaydına (K6) göre sterling gümüşte gümüşün oranı yüzde kaçtır? Yalnızca sayıyı yaz.",
          "Kayıtta bir yüzde değeri geçiyor.",
          "Sterling gümüş %92,5 gümüş içerir; geri kalanı çoğunlukla bakırdır. Bakır (8,96) gümüşten (10,5) daha az "
          "yoğun olduğu için, kaşığın yoğunluğu (10,4) saf gümüşünkinden biraz düşük çıkıyor.",
          dogru="92,5|92.5|%92,5|yüzde 92,5", hata_turu="veri"),
        G("G5", "Çıkarım", "", "kanit", "ozellik_kullanim", "kanit",
          "Kaşığın kararmasını açıklayan kanıtları seç.",
          "Kararmanın kimyasal nedeni hangi kanıtta yazıyor?",
          "RSC'ye göre gümüş, havadaki kükürtlü bileşiklerin yüzeyiyle tepkimeye girip siyah gümüş sülfür oluşturmasıyla "
          "yavaşça kararır (K3). Tablo (K4) da gümüşün bu davranışını gösteriyor.",
          dogru="K3 (K4)", hata_turu="iliski"),
        G("G6", "Sonuç", "Sonuç", "savunma", "gerekce", "gerekce",
          "Jüriye savunmanı yaz: kaşıktaki metalin ne olduğunu, bunu hangi kanıtlarla bildiğini ve kaşığın neden "
          "karardığını açıkla.",
          "",
          "Kaşıktaki metalin gümüş olduğunu düşünüyorum çünkü analiz metalin 11. grupta olduğunu gösteriyor ve bu gruptaki "
          "adaylar bakır, gümüş ve altın. Ölçtüğümüz yoğunluk 10,4 g/cm³; bakırın (8,96) ve altının (19,3) çok uzağında, "
          "gümüşünkine (10,5) ise çok yakın. Fark, kaşığın büyük olasılıkla %92,5 gümüş ve biraz bakır içeren sterling "
          "gümüş olmasından kaynaklanıyor. Kaşık karardı, çünkü gümüş havadaki kükürtlü bileşiklerle tepkimeye girip siyah "
          "bir sülfür oluşturur; altın kararmaz, bakır ise yeşil bir tabaka oluşturur."),
    ]))

DOSYALAR.append(dict(
    id="D19", seviye=4, sira=4, baslik="Ampulün Kalbi", cevap="W",
    giris="Eski bir akkor ampulün içindeki ince ve kıvrık tel, çalışırken 2000 °C'nin çok üzerinde ısındığı hâlde erimiyordu. "
          "Birim tel üzerinde ölçümler yaptı. Görevin: telin metalini bulmak ve sembolünün neden adına benzemediğini "
          "açıklamak. Hazır seçenek yok.",
    kaynakca=[rsc(74, "tungsten", "Tungsten"), rsc(75, "rhenium", "Renyum"), rsc(73, "tantalum", "Tantal"),
              rsc(42, "molybdenum", "Molibden"), rsc(79, "gold", "Altın")],
    kanitlar=[
        ("K1", "erime_kaynama", "Erime noktası ölçümü", "Tel ancak 3400 °C'nin üzerinde eriyor.", "", ""),
        ("K2", "yogunluk", "Yoğunluk ölçümü", "19,3 ± 0,1 g/cm³", "", ""),
        ("K3", "tablo", "Erime noktası yüksek bazı metaller", "T1", "", "RSC Periyodik Tablo"),
        ("K4", "fiziksel", "Görünüş", "Parlak, gümüşi beyaz bir metal.", "", ""),
        ("K5", "isim", "Arşiv notu",
         "Elementin adı İsveççe 'ağır taş' anlamına gelen 'tung sten' sözünden gelir. Sembolü W ise elementin diğer adı "
         "olan 'wolfram'dan gelir; bu ad, elementin elde edildiği wolframit mineraliyle ilgilidir. Element 1783'te "
         "İspanya'da Elhuyar kardeşler tarafından metal hâlinde elde edildi.", "G1", RSC + "74/tungsten"),
        ("K6", "kullanim", "RSC kaydı",
         "Bu metal eski tip akkor ampullerin telinde yaygın olarak kullanılıyordu; ama bu ampuller ışıktan çok ısı "
         "ürettikleri için birçok ülkede kullanımdan kaldırıldı. Bütün metaller içinde erime noktası en yüksek olanıdır; "
         "karbürü çok serttir ve kesici-delici aletlerde kullanılır.", "G1", RSC + "74/tungsten"),
    ],
    tablolar={"T1": [
        ["Metal", "Erime noktası (°C)", "Yoğunluk (g/cm³)"],
        ["Tungsten", "3414", "19,3"],
        ["Renyum", "3185", "20,8"],
        ["Tantal", "3017", "16,4"],
        ["Molibden", "2622", "10,2"],
    ]},
    gorevler=[
        G("G1", "Çıkarım", "İddia", "yaz", "kimlik", "cikarim",
          "Telin metali hangisi? Adını ya da sembolünü yaz.",
          "Tablodaki metallerden hangisi ancak 3400 °C'nin üzerinde erir?",
          "Metal tungstendir (W): tablodaki metallerden yalnızca tungsten 3400 °C'nin üzerinde erir (3414 °C). Yoğunluğu "
          "da (19,3) ölçümle uyuşuyor.",
          hata_turu="kanitsiz"),
        G("G2", "Hipotez", "Karşı kanıt", "yaz", "alternatif", "hipotez",
          "Yoğunluğu da 19,3 g/cm³ olan değerli bir metal daha var; Sahte Altın dosyasını hatırla. Bu metalin adını yaz.",
          "Kuyumcunun külçesi...",
          "Altının yoğunluğu da 19,3 g/cm³. Yoğunluk tek başına teli altından ayırmaz. Ama altın 1064 °C'de erir; ampul "
          "telinin sıcaklığında çoktan erirdi. Rengi de sarıdır, tel ise gümüşi beyaz.",
          dogru="Altın", hata_turu="veri"),
        G("G3", "Kanıt", "Kanıt", "kanit", "kanit", "kanit",
          "Teli altından ayıran kanıtları seç. Altınla ortak olan kanıtı seçme.",
          "Hangi ölçüm altın için de aynı sonucu verirdi?",
          "Erime noktası (K1) ve gümüşi beyaz renk (K4) teli altından ayırır: altın 1064 °C'de erir ve sarıdır. Yoğunluk "
          "(K2) ise altınla aynı olduğu için ayırt edici değildir; bu dosyanın tuzağı buydu.",
          dogru="K1 K4 (K3)", hata_turu="veri"),
        G("G4", "Sonuç", "", "yaz", "sembol", "cikarim",
          "Tungstenin sembolünü yaz.",
          "Sembol, adın baş harfi değil.",
          "Tungstenin sembolü W'dir; elementin diğer adı olan 'wolfram'dan gelir.",
          hata_turu="veri"),
        G("G5", "Sonuç", "", "yaz", "isim", "gozlem",
          "W sembolünün geldiği 'wolfram' adı, elementin elde edildiği bir mineralle ilgilidir. Bu mineralin adını yaz (K5).",
          "Arşiv notunda mineralin adı geçiyor.",
          "Mineralin adı wolframittir. Sembol W, 'wolfram' adından gelir; 'tungsten' adı ise İsveççe 'ağır taş' anlamındadır. "
          "Aynı elementin iki adı olması, sembolünün İngilizce ve Türkçe adına benzememesinin nedenidir.",
          dogru="wolframit|volframit", hata_turu="veri"),
        G("G6", "Çıkarım", "", "kanit", "ozellik_kullanim", "kanit",
          "Ampul telinde tungsten kullanılmasını açıklayan özelliği gösteren kanıtı seç.",
          "Akkor bir tel çalışırken hangi sıcaklığa dayanmalı?",
          "Akkor ampulün teli ışık verecek kadar ısınır; bu sıcaklıkta erimemesi gerekir. Tungsten bütün metaller içinde "
          "erime noktası en yüksek olanıdır (K1, K6).",
          dogru="K1 (K3) (K6)", hata_turu="iliski"),
        G("G7", "Sonuç", "Sonuç", "savunma", "gerekce", "gerekce",
          "Jüriye savunmanı yaz: telin metalini, kanıtlarını, altın hipotezini neden reddettiğini ve sembolünün neden W "
          "olduğunu açıkla.",
          "",
          "Ampul telinin tungsten olduğunu düşünüyorum çünkü tel ancak 3400 °C'nin üzerinde eriyor ve tablodaki metallerden "
          "yalnızca tungsten (3414 °C) bu koşulu sağlıyor; yoğunluğu da (19,3) tungstenle uyuşuyor. Yoğunluğu aynı olan "
          "altını eledim, çünkü altın 1064 °C'de erir ve sarıdır; tel ise gümüşi beyaz. Telde tungsten kullanılır, çünkü "
          "akkor hâlde erimeden dayanabilir. Sembolü W'dir, çünkü elementin diğer adı wolframdır; bu ad wolframit "
          "mineralinden gelir."),
    ]))

DOSYALAR.append(dict(
    id="D20", seviye=4, sira=5, baslik="Bilimsel Jüri: Yağdaki Metal", cevap="Na", final=True,
    giris="Final dosyası. Bir okul laboratuvarının dolabında, içi gazyağı dolu bir şişede saklanan gümüşi parçalar bulundu. "
          "Etiket yok. Laboratuvar sorumlusu emekli olmuş; geriye yalnızca eski bir deney defteri kalmış. Bilimsel jüri "
          "senden bu elementi kanıtlarla belirlemeni ve savunmanı istiyor. Bu dosyada hazır seçenek yok.",
    kaynakca=[rsc(11, "sodium", "Sodyum"), rsc(3, "lithium", "Lityum"), rsc(19, "potassium", "Potasyum"),
              rsc(37, "rubidium", "Rubidyum"), rsc(55, "caesium", "Sezyum")],
    kanitlar=[
        ("K1", "fiziksel", "Defter notu: görünüş",
         "Parçalar bıçakla kolayca kesiliyor. Kesilen yüzey parlak gümüşi, ama birkaç saniye içinde matlaşıyor.", "", ""),
        ("K2", "deney", "Defter notu: suyla deney",
         "Öğretmen, koruyucu ekranın arkasında bezelye büyüklüğünde bir parçayı suya attı. Parça su üzerinde yüzerek hızla "
         "döndü, cızırdadı ve gaz çıkardı. Deneyden sonra suya fenolftalein damlatılınca su pembeleşti.", "", ""),
        ("K3", "deney", "Defter notu: alev testi", "Parçanın bileşikleri alevi parlak sarı-turuncu renge boyuyor.", "", ""),
        ("K4", "yogunluk", "Defter notu: yoğunluk", "0,97 ± 0,02 g/cm³", "", ""),
        ("K5", "tablo", "1. grup (alkali) metalleri", "T1", "", "RSC Periyodik Tablo; standart alev testi renkleri"),
        ("K6", "isim", "Arşiv notu",
         "Bu elementin İngilizce adı 'soda' kelimesinden gelir; sembolü Na ise Latince 'natrium' adından gelir. Bu ad, "
         "eski Mısır'da Natron Vadisi'nden çıkarılan sodaya (natron) dayanır. Element 1807'de Humphry Davy tarafından, "
         "sodyum hidroksitten elektrik akımı geçirilerek elde edildi.", "G2", RSC + "11/sodium"),
        ("K7", "kullanim", "RSC kaydı",
         "Elementin kendisinden çok bileşikleri kullanılır: sodyum klorür (sofra tuzu) yemeklerde ve kışın yollardaki "
         "buzu çözmekte, sodyum karbonat (çamaşır sodası) su yumuşatıcı olarak kullanılır.", "G2", RSC + "11/sodium"),
    ],
    tablolar={"T1": [row for row in ALKALI_TABLO]},
    gorevler=[
        G("G1", "Gözlem", "", "tablo", "kanit", "veri",
          "Defter notlarına (K1, K2) göre bu madde hangi gruptaki metallerden olabilir? O gruptaki bütün metalleri "
          "periyodik tabloda işaretle.",
          "Bıçakla kesilebilen, havada hemen matlaşan, suyla şiddetle tepkimeye giren ve bu yüzden yağda saklanan metaller...",
          "Bu özellikler alkali metallerin (1. grup) özellikleridir: lityum, sodyum, potasyum, rubidyum, sezyum ve fransiyum. "
          "Hidrojen 1. grupta gösterilir ama metal değildir.",
          dogru="Li Na K Rb Cs Fr", hata_turu="veri"),
        G("G2", "Çıkarım", "İddia", "yaz", "kimlik", "cikarim",
          "Element hangisi? Adını ya da sembolünü yaz.",
          "Alev rengini ve yoğunluğu tabloyla karşılaştır.",
          "Element sodyumdur (Na): alevi sarı-turuncu boyuyor ve yoğunluğu (0,97 ± 0,02) tablodaki alkali metallerden "
          "yalnızca sodyumla uyuşuyor.",
          hata_turu="kanitsiz"),
        G("G3", "Kanıt", "Kanıt", "kanit", "kanit", "kanit",
          "İddianı destekleyen ve diğer alkali metalleri eleyen kanıtları seç.",
          "Hangi iki kanıt adayları tek bir metale indiriyor?",
          "Alev testi (K3) ve yoğunluk (K4), tabloyla (K5) karşılaştırılınca bağımsız olarak aynı metali gösteriyor. "
          "Görünüş (K1) ve suyla deney (K2) adayları alkali metallere indirir; ama hangisi olduğunu söylemez.",
          dogru="K3 K4 (K5) (K1) (K2)", hata_turu="kanitsiz"),
        G("G4", "Hipotez", "Karşı kanıt", "yaz", "alternatif", "hipotez",
          "En ciddi rakip hipotez hangi elementti? Adını yaz.",
          "Yoğunluğu ölçüme en yakın olan diğer alkali metal hangisi?",
          "En ciddi rakip potasyumdu: yoğunluğu (0,89) ölçüme en yakın diğer alkali metal ve o da suyla şiddetle tepkimeye "
          "girer. Ama alevi leylak rengidir; yoğunluğu da ölçüm aralığının (0,95–0,99) dışında kalır.",
          dogru="Potasyum", hata_turu="veri"),
        G("G5", "Kanıt", "Karşı kanıt", "yaz", "kanit", "kanit",
          "Potasyum hipotezini eleyen bir kanıtın numarasını yaz (örnek: K1).",
          "Potasyumun alevi hangi renktir? Yoğunluğu kaçtır?",
          "Potasyum iki kanıtla elenir: alev testi (K3), çünkü potasyumun alevi leylak rengidir; yoğunluk (K4), çünkü "
          "potasyumun yoğunluğu (0,89) ölçüm aralığının dışındadır.",
          dogru="K3|K4", hata_turu="kanitsiz"),
        G("G6", "Sonuç", "", "yaz", "sembol", "cikarim",
          "Elementin sembolünü yaz.",
          "Sembol, elementin Latince adından gelir.",
          "Sodyumun sembolü Na'dır.",
          hata_turu="veri"),
        G("G7", "Sonuç", "", "yaz", "isim", "gozlem",
          "Sembolün geldiği Latince adı yaz (K6).",
          "Arşiv notunda Latince ad geçiyor.",
          "Sembol Na, Latince 'natrium' adından gelir; bu ad eski Mısır'daki Natron Vadisi'nden çıkarılan sodaya dayanır.",
          dogru="natrium", hata_turu="veri"),
        G("G8", "Çıkarım", "", "kanit", "ozellik_kullanim", "kanit",
          "Elementin gazyağı içinde saklanmasını açıklayan kanıtları seç.",
          "Element hava ve suyla karşılaşınca ne oluyor?",
          "Sodyum havayla karşılaşınca saniyeler içinde matlaşır (K1) ve suyla şiddetle tepkimeye girer (K2). Gazyağı "
          "metali hava ve nemden yalıtır.",
          dogru="K1 K2", hata_turu="iliski"),
        G("G9", "Sonuç", "Sonuç", "savunma", "gerekce", "gerekce",
          "Bilimsel jüriye final savunmanı yaz: \"Elementin … olduğunu düşünüyorum çünkü…\" İddianı, kanıtlarını, gerekçeni, "
          "rakip hipotezleri neden reddettiğini, günlük kullanımını ve sembolünün hikâyesini anlat.",
          "",
          "Elementin sodyum olduğunu düşünüyorum çünkü defterdeki gözlemler alkali metalleri gösteriyor: bıçakla kesiliyor, "
          "havada hemen matlaşıyor, suyla şiddetle tepkimeye girip gaz çıkarıyor ve suyu bazik yapıyor. Alkali metaller "
          "arasında iki bağımsız kanıt aynı sonucu veriyor: alev sarı-turuncu ve yoğunluk 0,97 ± 0,02 g/cm³; tabloya göre "
          "ikisi de sodyuma ait. En ciddi rakip potasyumdu, çünkü yoğunluğu ölçüme en yakın ve o da suyla şiddetle tepkimeye "
          "girer; ama alevi leylaktır ve yoğunluğu 0,89 g/cm³'tür. Sodyum, hava ve sudan korumak için gazyağında saklanır. "
          "Bileşikleri günlük hayatta her yerdedir: sofra tuzu sodyum klorürdür. Sembolü Na, Latince 'natrium' adından gelir."),
    ]))
