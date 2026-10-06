# -*- coding: utf-8 -*-
"""Z=1..100 elementlerinin verileri: RSC periyodik tablosundan alınmış sayısal değerler (element_verileri.json)
ile elle yazılmış Türkçe isim kökeni ve keşif notları."""
import json
import pathlib
import re

KOK = pathlib.Path(__file__).resolve().parent
RSC_URL = "https://periodic-table.rsc.org/element/"

SEMBOLLER = (
    "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr "
    "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb "
    "Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm"
).split()

ADLAR = (
    "Hidrojen Helyum Lityum Berilyum Bor Karbon Azot Oksijen Flor Neon Sodyum Magnezyum Alüminyum Silisyum "
    "Fosfor Kükürt Klor Argon Potasyum Kalsiyum Skandiyum Titanyum Vanadyum Krom Mangan Demir Kobalt Nikel "
    "Bakır Çinko Galyum Germanyum Arsenik Selenyum Brom Kripton Rubidyum Stronsiyum İtriyum Zirkonyum "
    "Niyobyum Molibden Teknesyum Rutenyum Rodyum Paladyum Gümüş Kadmiyum İndiyum Kalay Antimon Tellür İyot "
    "Ksenon Sezyum Baryum Lantan Seryum Praseodim Neodim Prometyum Samaryum Evropiyum Gadolinyum Terbiyum "
    "Disprosiyum Holmiyum Erbiyum Tulyum İterbiyum Lutesyum Hafniyum Tantal Tungsten Renyum Osmiyum İridyum "
    "Platin Altın Cıva Talyum Kurşun Bizmut Polonyum Astatin Radon Fransiyum Radyum Aktinyum Toryum "
    "Protaktinyum Uranyum Neptünyum Plütonyum Amerikyum Küriyum Berkelyum Kaliforniyum Aynştaynyum Fermiyum"
).split()

# (kısa köken: seçenek metni, arşiv notu: isim kökeni ve keşif)
ISIM = {
    "H": ("Yunanca 'su oluşturan' anlamına gelen sözcükler",
          "Adı Yunanca 'hydro' (su) ve 'genes' (oluşturan) sözcüklerinden gelir, çünkü yandığında su oluşur. 1766'da Henry Cavendish tarafından keşfedildi."),
    "He": ("Yunanca 'Güneş' anlamına gelen helios",
           "Adı Yunanca 'Güneş' anlamına gelen 'helios' kelimesinden gelir, çünkü ilk kez Güneş'in ışığında fark edildi. Dünya'da 1895'te William Ramsay tarafından bulundu."),
    "Li": ("Yunanca 'taş' anlamına gelen lithos",
           "Adı Yunanca 'taş' anlamına gelen 'lithos' kelimesinden gelir, çünkü bir mineralin içinde bulundu. 1817'de Johan August Arfvedson tarafından keşfedildi."),
    "Be": ("Beril mineralinin Yunanca adı",
           "Adı, içinde bulunduğu beril mineralinin Yunanca adı 'beryllo'dan gelir. 1797'de Nicolas Louis Vauquelin tarafından keşfedildi."),
    "B": ("Boraks mineralinin Arapça adı 'buraq'",
          "Adı, boraks mineralinin Arapça adı 'buraq'tan gelir. 1808'de Paris'te Gay-Lussac ile Thénard ve Londra'da Humphry Davy tarafından birbirlerinden bağımsız olarak elde edildi."),
    "C": ("Latince 'odun kömürü' anlamına gelen carbo",
          "Adı Latince 'odun kömürü' anlamına gelen 'carbo' kelimesinden gelir. Tarih öncesi çağlardan beri kömür ve is olarak bilinir."),
    "N": ("Yunanca 'güherçile oluşturan' anlamına gelen sözcükler",
          "Uluslararası adı 'nitrogen', Yunanca 'güherçile oluşturan' demektir; sembolü N buradan gelir. Türkçedeki 'azot' adı ise Lavoisier'nin verdiği ve 'cansız' anlamına gelen Fransızca 'azote' adından gelir. 1772'de Daniel Rutherford tarafından keşfedildi."),
    "O": ("Yunanca 'asit oluşturan' anlamına gelen sözcükler",
          "Adı Yunanca 'asit oluşturan' anlamına gelen 'oxy genes' sözünden gelir. 1774'te Joseph Priestley ve ondan bağımsız olarak Carl Wilhelm Scheele tarafından keşfedildi."),
    "F": ("Latince 'akmak' anlamına gelen fluere",
          "Adı Latince 'akmak' anlamına gelen 'fluere' kelimesinden gelir; flüorit minerali metal eritilirken akışkanlaştırıcı olarak kullanılırdı. Element 1886'da Henri Moissan tarafından elde edildi."),
    "Ne": ("Yunanca 'yeni' anlamına gelen neos",
           "Adı Yunanca 'yeni' anlamına gelen 'neos' kelimesinden gelir. 1898'de William Ramsay ve Morris Travers tarafından havadan ayrıldı."),
    "Na": ("'Soda' kelimesi; sembolü Latince natrium",
           "Adı 'soda' kelimesinden gelir; sembolü Na ise Latince adı 'natrium'dan. 1807'de Humphry Davy tarafından elektrik akımıyla elde edildi."),
    "Mg": ("Yunanistan'daki Magnesia bölgesi",
           "Adı Yunanistan'ın Teselya bölgesindeki Magnesia'dan gelir. 1755'te Joseph Black tarafından element olarak tanındı."),
    "Al": ("Latince 'şap' anlamına gelen alumen",
           "Adı Latince 'şap' anlamına gelen 'alumen' kelimesinden gelir. 1825'te Hans Christian Ørsted tarafından elde edildi."),
    "Si": ("Latince 'çakmaktaşı' anlamına gelen silex",
           "Adı Latince 'çakmaktaşı' anlamına gelen 'silex' kelimesinden gelir. 1824'te Jöns Jacob Berzelius tarafından elde edildi."),
    "P": ("Yunanca 'ışık getiren' anlamına gelen phosphoros",
          "Adı Yunanca 'ışık getiren' anlamına gelen 'phosphoros' kelimesinden gelir, çünkü beyaz fosfor karanlıkta parlar. 1669'da Hennig Brandt tarafından keşfedildi."),
    "S": ("Latince sulfur",
          "Uluslararası adı Latince 'sulfur' kelimesinden gelir. Tarih öncesi çağlardan beri bilinir; yanardağların çevresinde saf hâlde bulunur."),
    "Cl": ("Yunanca 'sarımsı yeşil' anlamına gelen chloros",
           "Adı Yunanca 'sarımsı yeşil' anlamına gelen 'chloros' kelimesinden gelir; gazın rengini anlatır. 1774'te Carl Wilhelm Scheele tarafından keşfedildi."),
    "Ar": ("Yunanca 'tembel' anlamına gelen argos",
           "Adı Yunanca 'tembel, işsiz' anlamına gelen 'argos' kelimesinden gelir, çünkü neredeyse hiçbir maddeyle tepkimeye girmez. 1894'te Lord Rayleigh ve William Ramsay tarafından keşfedildi."),
    "K": ("'Potas' (bitki külü) kelimesi; sembolü Latince kalium",
          "Adı bitki külünden elde edilen 'potas' (potash) kelimesinden gelir; sembolü K ise Latince adı 'kalium'dan. 1807'de Humphry Davy tarafından elektrik akımıyla elde edildi."),
    "Ca": ("Latince 'kireç' anlamına gelen calx",
           "Adı Latince 'kireç' anlamına gelen 'calx' kelimesinden gelir. 1808'de Humphry Davy tarafından elde edildi."),
    "Sc": ("İskandinavya'nın Latince adı Scandia",
           "Adı İskandinavya'nın Latince adı 'Scandia'dan gelir. 1879'da Lars Fredrik Nilson tarafından keşfedildi; Mendeleyev bu elementin varlığını önceden tahmin etmişti."),
    "Ti": ("Yunan mitolojisindeki Titanlar",
           "Adı Yunan mitolojisinde Yeryüzü tanrıçasının oğulları olan Titanlardan gelir. 1791'de William Gregor tarafından keşfedildi."),
    "V": ("İskandinav tanrıçası Vanadis",
          "Adı İskandinav güzellik tanrıçası Freyja'nın eski adı 'Vanadis'ten gelir; bileşiklerinin renkleri çok güzeldir. 1801'de Andrés Manuel del Río tarafından keşfedildi."),
    "Cr": ("Yunanca 'renk' anlamına gelen chroma",
           "Adı Yunanca 'renk' anlamına gelen 'chroma' kelimesinden gelir, çünkü bileşikleri çok renklidir. 1798'de Nicolas Louis Vauquelin tarafından keşfedildi."),
    "Mn": ("Latince 'mıknatıs' ya da 'kara magnezya' minerali",
           "Adı ya Latince 'mıknatıs' anlamına gelen 'magnes' kelimesinden ya da 'kara magnezya' denilen siyah bir mineralden gelir. 1774'te Johan Gottlieb Gahn tarafından elde edildi."),
    "Fe": ("Türkçe 'demir'; sembolü Latince ferrum",
           "Demir eski bir Türkçe kelimedir; sembolü Fe ise Latince adı 'ferrum'dan gelir. Yaklaşık MÖ 3500'den beri kullanılıyor."),
    "Co": ("Almanca 'cin, kötü ruh' anlamına gelen kobald",
           "Adı Almanca 'cin, kötü ruh' anlamına gelen 'kobald' kelimesinden gelir; madenciler bu cevherin başlarına iş açtığını düşünürdü. 1739'da Georg Brandt tarafından keşfedildi."),
    "Ni": ("Almanca 'şeytanın bakırı' (kupfernickel)",
           "Adı Almanca 'kupfernickel' (şeytanın bakırı) sözünün kısaltmasıdır; madenciler bakıra benzeyen ama bakır vermeyen bu cevheri böyle adlandırdı. 1751'de Axel Fredrik Cronstedt tarafından keşfedildi."),
    "Cu": ("'Kıbrıs metali' anlamına gelen Cyprium aes",
           "Bakır eski bir Türkçe kelimedir. Sembolü Cu Latince 'cuprum'dan gelir; o da 'Kıbrıs metali' anlamına gelen 'Cyprium aes' sözünden türemiştir. Tarih öncesi çağlardan beri kullanılıyor."),
    "Zn": ("Almanca zink (belki Farsça 'taş' anlamına gelen sing)",
           "Adı Almanca 'zink' kelimesinden gelir; bu kelime belki de Farsça 'taş' anlamına gelen 'sing'den türemiştir. 1746'da Andreas Marggraf tarafından element olarak tanındı; eski Yunanlar ve Romalılar da onu biliyordu."),
    "Ga": ("Fransa'nın Latince adı Gallia",
           "Adı Fransa'nın Latince adı 'Gallia'dan gelir. 1875'te Paul-Émile Lecoq de Boisbaudran tarafından keşfedildi; Mendeleyev bu elementi önceden tahmin etmişti."),
    "Ge": ("Almanya'nın Latince adı Germania",
           "Adı Almanya'nın Latince adı 'Germania'dan gelir. 1886'da Clemens Winkler tarafından keşfedildi; Mendeleyev onu 'eka-silisyum' adıyla önceden tahmin etmişti."),
    "As": ("Sarı boya orpimentin Yunanca adı arsenikon",
           "Adı sarı bir boya olan orpiment mineralinin Yunanca adı 'arsenikon'dan gelir. Yaklaşık 1250'de Albertus Magnus tarafından elde edildiği düşünülür."),
    "Se": ("Yunanca 'Ay' anlamına gelen selene",
           "Adı Yunanca 'Ay' anlamına gelen 'selene' kelimesinden gelir. 1817'de Jöns Jacob Berzelius tarafından keşfedildi; adı 'Dünya'dan gelen tellüre benzediği için ona Ay'ın adı verildi."),
    "Br": ("Yunanca 'pis koku' anlamına gelen bromos",
           "Adı Yunanca 'pis koku' anlamına gelen 'bromos' kelimesinden gelir. 1826'da Antoine-Jérôme Balard ve ondan bağımsız olarak Carl Löwig tarafından keşfedildi."),
    "Kr": ("Yunanca 'gizli' anlamına gelen kryptos",
           "Adı Yunanca 'gizli' anlamına gelen 'kryptos' kelimesinden gelir. 1898'de William Ramsay ve Morris Travers tarafından sıvı havadan ayrıldı."),
    "Rb": ("Latince 'en koyu kırmızı' anlamına gelen rubidius",
           "Adı Latince 'en koyu kırmızı' anlamına gelen 'rubidius' kelimesinden gelir; spektrumundaki kırmızı çizgiler nedeniyle. 1861'de Gustav Kirchhoff ve Robert Bunsen tarafından spektroskopla keşfedildi."),
    "Sr": ("İskoçya'daki Strontian kasabası",
           "Adı İskoçya'daki küçük Strontian kasabasından gelir; element oradan çıkan bir mineralde fark edildi. 1790'da Adair Crawford tarafından tanındı."),
    "Y": ("İsveç'teki Ytterby köyü",
          "Adı İsveç'teki Ytterby köyünden gelir; bu köyün madeninden çıkan minerallerden dört element (itriyum, terbiyum, erbiyum, iterbiyum) adını aldı. 1794'te Johan Gadolin tarafından keşfedildi."),
    "Zr": ("Farsça 'altın renkli' anlamına gelen zargun",
           "Adı Farsça 'altın renkli' anlamına gelen 'zargun' kelimesinden (zirkon taşı) gelir. 1789'da Martin Heinrich Klaproth tarafından keşfedildi."),
    "Nb": ("Kral Tantalos'un kızı Niobe",
           "Adı Yunan mitolojisinde Kral Tantalos'un kızı Niobe'den gelir, çünkü kimyasal olarak tantala çok benzer. 1801'de Charles Hatchett tarafından keşfedildi."),
    "Mo": ("Yunanca 'kurşun' anlamına gelen molybdos",
           "Adı Yunanca 'kurşun' anlamına gelen 'molybdos' kelimesinden gelir; cevheri uzun süre kurşun cevheriyle ve grafitle karıştırıldı. 1781'de Peter Jacob Hjelm tarafından elde edildi."),
    "Tc": ("Yunanca 'yapay' anlamına gelen tekhnetos",
           "Adı Yunanca 'yapay' anlamına gelen 'tekhnetos' kelimesinden gelir; yapay yolla elde edilen ilk elementtir. 1937'de Carlo Perrier ve Emilio Segrè tarafından keşfedildi."),
    "Ru": ("Rusya'nın Latince adı Ruthenia",
           "Adı Rusya'nın Latince adı 'Ruthenia'dan gelir. 1844'te Karl Karlovich Klaus tarafından keşfedildi."),
    "Rh": ("Yunanca 'gül' anlamına gelen rhodon",
           "Adı Yunanca 'gül' anlamına gelen 'rhodon' kelimesinden gelir; tuzlarının çözeltileri gül rengindedir. 1803'te William Hyde Wollaston tarafından keşfedildi."),
    "Pd": ("Pallas asteroidi",
           "Adı, keşfinden kısa süre önce bulunan Pallas asteroidinden gelir; asteroit de adını Yunan bilgelik tanrıçası Pallas'tan almıştı. 1803'te William Hyde Wollaston tarafından keşfedildi."),
    "Ag": ("Türkçe 'gümüş'; sembolü Latince argentum",
           "Gümüş eski bir Türkçe kelimedir; sembolü Ag ise Latince adı 'argentum'dan gelir. Yaklaşık MÖ 3000'den beri kullanılıyor."),
    "Cd": ("Kalamin mineralinin Latince adı cadmia",
           "Adı, kalamin (bir çinko cevheri) mineralinin Latince adı 'cadmia'dan gelir; element bu cevherin içinde fark edildi. 1817'de Friedrich Stromeyer tarafından keşfedildi."),
    "In": ("Spektrumundaki çivit mavisi (indigo) çizgi",
           "Adı, spektrumundaki parlak çivit mavisi (indigo) çizgiden gelir. 1863'te Ferdinand Reich ve Hieronymus Richter tarafından spektroskopla keşfedildi."),
    "Sn": ("Sembolü Latince stannum",
           "Sembolü Sn, Latince adı 'stannum'dan gelir. Yaklaşık MÖ 2100'den beri kullanılıyor; bakırla karıştırılarak tunç yapıldı."),
    "Sb": ("Yunanca 'yalnız değil' (anti-monos); sembolü stibium",
           "Adının Yunanca 'yalnız değil' anlamına gelen 'anti-monos' sözünden geldiği düşünülür; sembolü Sb ise Latince 'stibium'dan gelir. Yaklaşık MÖ 1600'den beri bilinir."),
    "Te": ("Latince 'Dünya' anlamına gelen tellus",
           "Adı Latince 'Dünya, toprak' anlamına gelen 'tellus' kelimesinden gelir. 1783'te Franz-Joseph Müller von Reichenstein tarafından keşfedildi."),
    "I": ("Yunanca 'mor' anlamına gelen iodes",
          "Adı Yunanca 'mor' anlamına gelen 'iodes' kelimesinden gelir; ısıtılınca mor bir buhar çıkarır. 1811'de Bernard Courtois tarafından deniz yosunu külünden elde edildi."),
    "Xe": ("Yunanca 'yabancı' anlamına gelen xenos",
           "Adı Yunanca 'yabancı' anlamına gelen 'xenos' kelimesinden gelir. 1898'de William Ramsay ve Morris Travers tarafından sıvı havadan ayrıldı."),
    "Cs": ("Latince 'gök mavisi' anlamına gelen caesius",
           "Adı Latince 'gök mavisi' anlamına gelen 'caesius' kelimesinden gelir; spektrumundaki mavi çizgiler nedeniyle. 1860'ta Robert Bunsen ve Gustav Kirchhoff tarafından maden suyunda spektroskopla keşfedildi."),
    "Ba": ("Yunanca 'ağır' anlamına gelen barys",
           "Adı Yunanca 'ağır' anlamına gelen 'barys' kelimesinden gelir; cevheri barit çok ağırdır. 1808'de Humphry Davy tarafından elde edildi."),
    "La": ("Yunanca 'gizli kalmak' anlamına gelen lanthanein",
           "Adı Yunanca 'gizli kalmak' anlamına gelen 'lanthanein' kelimesinden gelir; seryum mineralinin içinde gizlenmişti. 1839'da Carl Gustav Mosander tarafından keşfedildi."),
    "Ce": ("Ceres asteroidi",
           "Adı, birkaç yıl önce keşfedilen Ceres asteroidinden gelir; Ceres, Roma tarım tanrıçasının adıdır. 1803'te Jöns Jacob Berzelius ve Wilhelm Hisinger tarafından keşfedildi."),
    "Pr": ("Yunanca 'yeşil ikiz' (prasios didymos)",
           "Adı Yunanca 'yeşil ikiz' anlamına gelen 'prasios didymos' sözünden gelir; tuzları yeşildir ve neodimle birlikte tek bir madde sanılan bir karışımdan ayrıldı. 1885'te Carl Auer von Welsbach tarafından keşfedildi."),
    "Nd": ("Yunanca 'yeni ikiz' (neos didymos)",
           "Adı Yunanca 'yeni ikiz' anlamına gelen 'neos didymos' sözünden gelir; praseodimle birlikte tek bir madde sanılan bir karışımdan ayrıldı. 1885'te Carl Auer von Welsbach tarafından keşfedildi."),
    "Pm": ("Tanrılardan ateşi çalan Prometheus",
           "Adı, Yunan mitolojisinde tanrılardan ateşi çalıp insanlara veren Prometheus'tan gelir. 1945'te Jacob Marinsky, Lawrence Glendenin ve Charles Coryell tarafından nükleer reaktör ürünlerinde bulundu."),
    "Sm": ("Samarskit minerali",
           "Adı, ilk kez elde edildiği samarskit mineralinden gelir; mineral de adını Rus maden yetkilisi Samarsky-Bykhovets'ten almıştı. 1879'da Paul-Émile Lecoq de Boisbaudran tarafından keşfedildi."),
    "Eu": ("Avrupa kıtası",
           "Adı Avrupa kıtasından gelir. 1901'de Eugène-Anatole Demarçay tarafından keşfedildi."),
    "Gd": ("Fin kimyacı Johan Gadolin",
           "Adı Fin kimyacı Johan Gadolin'in onuruna verildi. 1880'de Jean Charles Galissard de Marignac tarafından keşfedildi."),
    "Tb": ("İsveç'teki Ytterby köyü",
           "Adı İsveç'teki Ytterby köyünden gelir. 1843'te Carl Gustav Mosander tarafından keşfedildi."),
    "Dy": ("Yunanca 'elde edilmesi zor' anlamına gelen dysprositos",
           "Adı Yunanca 'elde edilmesi zor' anlamına gelen 'dysprositos' kelimesinden gelir; ayrılması çok uğraş gerektirdi. 1886'da Paul-Émile Lecoq de Boisbaudran tarafından keşfedildi."),
    "Ho": ("Stockholm'ün Latince adı Holmia",
           "Adı Stockholm'ün Latince adı 'Holmia'dan gelir. 1878'de Per Teodor Cleve ve ondan bağımsız olarak Marc Delafontaine ile Louis Soret tarafından keşfedildi."),
    "Er": ("İsveç'teki Ytterby köyü",
           "Adı İsveç'teki Ytterby köyünden gelir. 1843'te Carl Gustav Mosander tarafından keşfedildi."),
    "Tm": ("İskandinavya'nın eski adı Thule",
           "Adı İskandinavya'nın eski adı 'Thule'den gelir. 1879'da Per Teodor Cleve tarafından keşfedildi."),
    "Yb": ("İsveç'teki Ytterby köyü",
           "Adı İsveç'teki Ytterby köyünden gelir. 1878'de Jean Charles Galissard de Marignac tarafından keşfedildi."),
    "Lu": ("Paris'in Roma dönemindeki adı Lutetia",
           "Adı Paris'in Roma dönemindeki adı 'Lutetia'dan gelir. 1907'de Georges Urbain ve ondan bağımsız olarak Charles James tarafından keşfedildi."),
    "Hf": ("Kopenhag'ın Latince adı Hafnia",
           "Adı Kopenhag'ın Latince adı 'Hafnia'dan gelir. 1923'te George de Hevesy ve Dirk Coster tarafından keşfedildi."),
    "Ta": ("Yunan mitolojisindeki Kral Tantalos",
           "Adı Yunan mitolojisindeki Kral Tantalos'tan gelir: Tantalos'un önündeki suyu içememesi gibi, bu metal de asit içine konulunca asidi 'içmez', yani asitten etkilenmez. 1802'de Anders Gustaf Ekeberg tarafından keşfedildi."),
    "W": ("İsveççe 'ağır taş' (tung sten); sembolü wolfram",
          "Adı İsveççe 'ağır taş' anlamına gelen 'tung sten' sözünden gelir; sembolü W ise 'wolfram' adından. 1783'te Juan José ve Fausto Elhuyar kardeşler tarafından elde edildi."),
    "Re": ("Ren Nehri'nin Latince adı Rhenus",
           "Adı Ren Nehri'nin Latince adı 'Rhenus'tan gelir. 1925'te Walter Noddack, Ida Tacke ve Otto Berg tarafından keşfedildi; kararlı izotopu olan elementler arasında en son keşfedilenidir."),
    "Os": ("Yunanca 'koku' anlamına gelen osme",
           "Adı Yunanca 'koku' anlamına gelen 'osme' kelimesinden gelir; oksidi keskin kokuludur. 1803'te Smithson Tennant tarafından keşfedildi."),
    "Ir": ("Yunan gökkuşağı tanrıçası İris",
           "Adı Yunan gökkuşağı tanrıçası İris'ten gelir; tuzları çok renklidir. 1803'te Smithson Tennant tarafından keşfedildi."),
    "Pt": ("İspanyolca 'küçük gümüş' anlamına gelen platina",
           "Adı İspanyolca 'küçük gümüş' anlamına gelen 'platina' kelimesinden gelir. Güney Amerika yerlileri onu Kolomb'dan önce biliyordu; Avrupa'ya 1750 dolaylarında getirildi."),
    "Au": ("Türkçe 'altın'; sembolü Latince aurum",
           "Altın eski bir Türkçe kelimedir; sembolü Au ise Latince adı 'aurum'dan gelir. Yaklaşık MÖ 3000'den beri kullanılıyor."),
    "Hg": ("Merkür gezegeni; sembolü 'sıvı gümüş' anlamına gelen hydrargyrum",
           "Uluslararası adı Merkür gezegeninden gelir; sembolü Hg ise Latince 'sıvı gümüş' anlamına gelen 'hydrargyrum'dan. Yaklaşık MÖ 1500'den beri bilinir."),
    "Tl": ("Yunanca 'yeşil filiz' anlamına gelen thallos",
           "Adı Yunanca 'taze yeşil filiz' anlamına gelen 'thallos' kelimesinden gelir; spektrumunda parlak yeşil bir çizgi vardır. 1861'de William Crookes tarafından spektroskopla keşfedildi."),
    "Pb": ("Türkçe 'kurşun'; sembolü Latince plumbum",
           "Kurşun eski bir Türkçe kelimedir; sembolü Pb ise Latince adı 'plumbum'dan gelir. İngilizcedeki 'plumber' (tesisatçı) kelimesi de buradan gelir, çünkü Romalılar su borularını kurşundan yapardı."),
    "Bi": ("Almanca 'beyaz kütle' sözünün bozulmuş hâli",
           "Adı, Almanca 'beyaz kütle' anlamına gelen 'weisse Masse' sözünün bozulmasıyla oluşan 'bisemutum'dan gelir. 1500'ler dolaylarında biliniyordu."),
    "Po": ("Marie Curie'nin vatanı Polonya",
           "Adı Marie Curie'nin vatanı Polonya'dan gelir. 1898'de Marie Curie ve eşi Pierre Curie tarafından keşfedildi."),
    "At": ("Yunanca 'kararsız' anlamına gelen astatos",
           "Adı Yunanca 'kararsız' anlamına gelen 'astatos' kelimesinden gelir, çünkü bütün izotopları hızla bozunur. 1940'ta Dale Corson, Kenneth MacKenzie ve Emilio Segrè tarafından yapay olarak üretildi."),
    "Rn": ("Radyumdan çıkan gaz olduğu için 'radyum'",
           "Adı radyumdan gelir, çünkü ilk kez radyumun bozunurken çıkardığı gaz olarak fark edildi. 1900'de Friedrich Ernst Dorn tarafından keşfedildi."),
    "Fr": ("Fransa",
           "Adı Fransa'dan gelir. 1939'da Paris'teki Curie Enstitüsü'nde Marguerite Perey tarafından keşfedildi; doğada keşfedilen son element olarak bilinir."),
    "Ra": ("Latince 'ışın' anlamına gelen radius",
           "Adı Latince 'ışın' anlamına gelen 'radius' kelimesinden gelir. 1898'de Marie ve Pierre Curie tarafından uranyum cevherinde keşfedildi."),
    "Ac": ("Yunanca 'ışın' anlamına gelen aktinos",
           "Adı Yunanca 'ışın' anlamına gelen 'aktinos' kelimesinden gelir. 1899'da André Debierne tarafından keşfedildi."),
    "Th": ("İskandinav tanrısı Thor",
           "Adı İskandinav savaş ve gök gürültüsü tanrısı Thor'dan gelir. 1829'da Jöns Jacob Berzelius tarafından keşfedildi."),
    "Pa": ("'Aktinyumdan önce gelen' anlamı (protos + aktinyum)",
           "Adı Yunanca 'ilk' anlamına gelen 'protos' ile 'aktinyum'un birleşiminden gelir, çünkü bozunarak aktinyuma dönüşür. 1913'te Kasimir Fajans ve Otto Göhring tarafından keşfedildi."),
    "U": ("Uranüs gezegeni",
          "Adı, birkaç yıl önce keşfedilen Uranüs gezegeninden gelir. 1789'da Martin Heinrich Klaproth tarafından keşfedildi."),
    "Np": ("Neptün gezegeni",
           "Adı Neptün gezegeninden gelir: periyodik tabloda uranyumdan sonra gelir, tıpkı Neptün'ün Güneş Sistemi'nde Uranüs'ten sonra gelmesi gibi. 1940'ta Edwin McMillan ve Philip Abelson tarafından üretildi."),
    "Pu": ("O dönemde gezegen sayılan Plüton",
           "Adı, o dönemde gezegen sayılan Plüton'dan gelir; uranyum ve neptünyumdan sonra gelen bir gök cismi olarak. 1940'ta Glenn Seaborg ve ekibi tarafından üretildi."),
    "Am": ("Amerika kıtası",
           "Adı, ilk kez üretildiği Amerika kıtasından gelir. 1944'te Glenn Seaborg ve ekibi tarafından üretildi."),
    "Cm": ("Marie ve Pierre Curie",
           "Adı Marie ve Pierre Curie'nin onuruna verildi. 1944'te Glenn Seaborg ve ekibi tarafından üretildi."),
    "Bk": ("Kaliforniya'daki Berkeley şehri",
           "Adı, ilk kez üretildiği Kaliforniya'daki Berkeley şehrinden gelir. 1949'da Stanley Thompson, Albert Ghiorso ve Glenn Seaborg tarafından üretildi."),
    "Cf": ("Kaliforniya eyaleti ve üniversitesi",
           "Adı, ilk kez üretildiği Kaliforniya eyaletinden ve üniversitesinden gelir. 1950'de Stanley Thompson, Kenneth Street, Albert Ghiorso ve Glenn Seaborg tarafından üretildi."),
    "Es": ("Fizikçi Albert Einstein",
           "Adı fizikçi Albert Einstein'ın onuruna verildi. 1952'de Albert Ghiorso ve ekibi tarafından, ilk hidrojen bombası denemesinin kalıntılarında bulundu."),
    "Fm": ("Fizikçi Enrico Fermi",
           "Adı nükleer fizikçi Enrico Fermi'nin onuruna verildi. 1953'te Albert Ghiorso ve ekibi tarafından, ilk hidrojen bombası denemesinin kalıntılarında bulundu."),
}

# IUPAC grup numarası -> Türkiye'de de kullanılan harfli adlandırma
HARFLI_GRUP = {1: "1A", 2: "2A", 3: "3B", 4: "4B", 5: "5B", 6: "6B", 7: "7B", 8: "8B", 9: "8B", 10: "8B",
               11: "1B", 12: "2B", 13: "3A", 14: "4A", 15: "5A", 16: "6A", 17: "7A", 18: "8A"}
GRUP_ADI = {1: "alkali metaller", 2: "toprak alkali metaller", 13: "toprak metalleri", 17: "halojenler", 18: "soy gazlar"}

METAL_OLMAYAN = {"H", "He", "C", "N", "O", "F", "Ne", "P", "S", "Cl", "Ar", "Se", "Br", "Kr", "I", "Xe", "Rn"}
YARI_METAL = {"B", "Si", "Ge", "As", "Sb", "Te", "At"}
# Bütün izotopları radyoaktif olan elementler
RADYOAKTIF = {"Tc", "Pm", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm"}


def _sayi(metin):
    if not metin or metin.startswith("Unknown"):
        return None
    m = re.search(r"−?-?\d+(?:\.\d+)?", metin)
    return float(m.group().replace("−", "-")) if m else None


def _yukle():
    veri = json.loads((KOK / "element_verileri.json").read_text(encoding="utf-8"))
    sozluk = {}
    for v in veri:
        z = v["z"]
        sembol = SEMBOLLER[z - 1]
        grup = int(v["grup"]) if v["grup"] and v["grup"].isdigit() else None
        yogunluk = _sayi(v.get("yogunluk"))
        if sembol == "C":
            yogunluk = None          # elmas ve grafit farklı
        erime = None if (v["erime"] or "").startswith("Sublimes") else _sayi(v["erime"])
        kaynama = None if (v["kaynama"] or "").startswith("Sublimes") else _sayi(v["kaynama"])
        hal = {"Solid": "katı", "Liquid": "sıvı", "Gas": "gaz"}.get(v["hal"], "katı")
        sozluk[sembol] = dict(
            z=z, sembol=sembol, ad=ADLAR[z - 1], ad_en=v["ad_en"], grup=grup, periyot=int(v["periyot"]), blok=v["blok"],
            hal=hal, yogunluk=yogunluk, erime=erime, kaynama=kaynama, dizilim_rsc=v["dizilim"],
            kutle=_sayi(v["kutle"]), izotoplar=v["izotoplar"], yukseltgenme=v.get("yukseltgenme"),
            kisa_koken=ISIM[sembol][0], arsiv=ISIM[sembol][1],
            rsc=f"{RSC_URL}{z}/{v['ad_en']}",
            tur="ametal" if sembol in METAL_OLMAYAN else "yarı metal" if sembol in YARI_METAL else "metal",
            radyoaktif=sembol in RADYOAKTIF,
        )
    return sozluk


E = _yukle()
assert len(E) == 100 and set(ISIM) == set(E)


def lantanit_mi(e):
    return 57 <= e["z"] <= 71


def aktinit_mi(e):
    return 89 <= e["z"] <= 103


# Aufbau sırasıyla elektron dizilimi (ilk 36 element için; Cr ve Cu istisnaları RSC'ye göre)
_ORBITALLER = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p"]
_KAPASITE = {"s": 2, "p": 6, "d": 10}
_UST = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def dizilim(z):
    assert z <= 36
    kalan, parcalar = z, []
    for o in _ORBITALLER:
        if not kalan:
            break
        n = min(kalan, _KAPASITE[o[-1]])
        parcalar.append([o, n])
        kalan -= n
    if z in (24, 29):              # Cr: 3d⁵ 4s¹, Cu: 3d¹⁰ 4s¹
        for p in parcalar:
            if p[0] == "4s":
                p[1] = 1
            if p[0] == "3d":
                p[1] += 1
    return " ".join(f"{o}{str(n).translate(_UST)}" for o, n in parcalar)


def sayi_tr(x, basamak=None):
    """Türkçe ondalık: 7.874 -> '7,874'"""
    if basamak is not None:
        metin = f"{x:.{basamak}f}"
    else:
        metin = f"{x:g}" if abs(x) < 1e6 else f"{x:.0f}"
    return metin.replace("-", "−").replace(".", ",")
