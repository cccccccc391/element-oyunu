# -*- coding: utf-8 -*-
"""Vaka şablonu.

Her vakada elle yazılanlar: başlık, hikâye, gözlem kartları, gözlem sorusu ve özellik-kullanım sorusu.
Şablonun ürettikleri: yapı kanıtı (periyodik tablo konumu, atom numarası, elektron dizilimi, izotop ya da
iyon bilgisi), veri tablosu, laboratuvar ölçümü, arşiv notu ve bunlara dayanan görevler.

Seviye 1 (Gözlem):   gözlem sorusu, konum, özellik-kullanım, isim kökeni ya da sınıf
Seviye 2 (Çıkarım):  gözlem sorusu, hesaplanan konum (dizilim/izotop/iyon), ölçüm, özellik-kullanım, kanıt seçimi
Seviye 3 (Kanıt):    adaylar, ölçüm, rakip hipotez, özellik-kullanım, kanıt seçimi
Seviye 4 (Savunma):  gözlem sorusu, yazılı kimlik, özellik-kullanım, kanıt seçimi, savunma
"""
import math

from elementler import E, GRUP_ADI, HARFLI_GRUP, aktinit_mi, dizilim, lantanit_mi, sayi_tr

RSC_GENEL = "https://periodic-table.rsc.org"

OZELLIK = {
    "yogunluk": dict(ad="yoğunluk", birim="g/cm³", sutun="Yoğunluk (g/cm³)",
                     cumle="Örneğin yoğunluğu {m} ± {u} g/cm³ olarak ölçüldü.", baslik="Yoğunluk ölçümü", tur="yogunluk"),
    "erime": dict(ad="erime noktası", birim="°C", sutun="Erime noktası (°C)",
                  cumle="Örnek {m} ± {u} °C sıcaklıkta erimeye başladı.", baslik="Erime noktası ölçümü", tur="erime_kaynama"),
    "kaynama": dict(ad="kaynama noktası", birim="°C", sutun="Kaynama noktası (°C)",
                    cumle="Sıvılaştırılan örnek {m} ± {u} °C sıcaklıkta kaynadı.", baslik="Kaynama noktası ölçümü", tur="erime_kaynama"),
}
PAYLAR = [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5, 10, 20, 30, 50]

# İzotop bilgisi için radyoaktif elementlerde kullanılan izotoplar (kütle numarası)
RADYOAKTIF_IZOTOP = {"Tc": 99, "Pm": 147, "Po": 210, "At": 211, "Rn": 222, "Fr": 223, "Ra": 226, "Ac": 227, "Th": 232,
                     "Pa": 231, "U": 238, "Np": 237, "Pu": 238, "Am": 241, "Cm": 244, "Bk": 249, "Cf": 252, "Es": 253,
                     "Fm": 255}
# İyon bilgisi: (yük, aynı elektron sayısına sahip soy gaz)
IYON = {"Li": (1, "He"), "Be": (2, "He"), "N": (-3, "Ne"), "O": (-2, "Ne"), "F": (-1, "Ne"), "Na": (1, "Ne"),
        "Mg": (2, "Ne"), "Al": (3, "Ne"), "P": (-3, "Ar"), "S": (-2, "Ar"), "Cl": (-1, "Ar"), "K": (1, "Ar"),
        "Ca": (2, "Ar")}

UST = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")


# ------------------------------------------------------------------ elle yazılan parçalar

def S(soru, dogru, *yanlislar, ipucu="", aciklama="", dogru_kanit=""):
    """Elle yazılan tek doğrulu soru. yanlislar: Y(...) listesi."""
    return dict(soru=soru, dogru=dogru, yanlislar=list(yanlislar), ipucu=ipucu, aciklama=aciklama)


def Y(metin, hata, aciklama, kanit=""):
    """Yanlış seçenek: hata türü (kanitsiz, veri, birim, iliski), neden yanlış olduğu, hatayı gösteren kanıt."""
    assert hata in ("kanitsiz", "veri", "birim", "iliski"), hata
    return (metin, hata, aciklama, kanit)


def V(sembol, seviye, tema, baslik, giris, ipuclari, kullanim, gozlem=None, **ayar):
    """Bir vaka tanımı. ipuclari: (tur, baslik, metin[, rol[, kaynak]]) — rol: genel | serbest | gerekli."""
    assert sembol in E, sembol
    assert seviye in (1, 2, 3, 4)
    return dict(sembol=sembol, seviye=seviye, tema=tema, baslik=baslik, giris=giris, ipuclari=ipuclari,
                kullanim=kullanim, gozlem=gozlem, ayar=ayar)


# ------------------------------------------------------------------ yardımcılar

def kucuk(metin):
    """Türkçe küçük harf: 'İyot' -> 'iyot'"""
    return metin.replace("İ", "i").replace("I", "ı").lower()


def de_eki(kelime):
    """'Demir' -> 'de', 'Berilyum' -> 'da' (ünlü uyumu)"""
    for harf in reversed(kucuk(kelime)):
        if harf in "aıou":
            return "da"
        if harf in "eiöü":
            return "de"
    return "de"


def ad(s):
    return E[s]["ad"]


def adlar(semboller, kucuk_harf=True):
    liste = [kucuk(ad(s)) if kucuk_harf else ad(s) for s in semboller]
    return ", ".join(liste[:-1]) + " ve " + liste[-1] if len(liste) > 1 else liste[0]


def deger_metni(ozellik, v, s=None):
    if s == "C" and ozellik == "yogunluk":
        return "2,2 (grafit)"
    if v is None:
        return "bilinmiyor"
    if ozellik == "yogunluk":
        return sayi_tr(v, 6 if v < 0.01 else 2).rstrip("0").rstrip(",") if v < 0.01 else sayi_tr(v, 2)
    return sayi_tr(v, 0 if abs(v) >= 100 else 1)


def deger(s, ozellik):
    """Tabloda gösterilen (yuvarlanmış) değer; ölçüm karşılaştırmaları da bu değerle yapılır."""
    if s == "C" and ozellik == "yogunluk":
        return 2.2                              # grafit (elmas 3,51)
    v = E[s][ozellik]
    if v is None:
        return None
    return float(deger_metni(ozellik, v).replace(",", ".").replace("−", "-"))


def ondalik(pay):
    return max(0, -int(math.floor(math.log10(pay) + 1e-9))) if pay < 1 else 0


def grup_metni(e):
    return f"{HARFLI_GRUP[e['grup']]} grubunda (IUPAC'a göre {e['grup']}. grup)"


def sinif(e):
    if e["grup"] == 18:
        return "soy gaz"
    return e["tur"]


def periyot_bas(p):
    return {1: "H", 2: "Li", 3: "Na", 4: "K", 5: "Rb", 6: "Cs", 7: "Fr"}[p]


# ------------------------------------------------------------------ vaka kurucu

class Kurucu:
    def __init__(self, v, vaka_id, sira, ilk_vaka):
        self.v = v
        self.id = vaka_id
        self.sira = sira
        self.s = v["sembol"]
        self.e = E[self.s]
        self.ayar = v["ayar"]
        self.seviye = v["seviye"]
        self.ilk_vaka = ilk_vaka            # bu element için ilk vaka mı (isim kökeni sorusu)
        self.kanitlar = []
        self.tablolar = {}
        self.gorevler = []
        self.ref = {}                       # yapi, tablo, olcum, olcum2, arsiv -> K numarası
        self.kaynakca = [f"Royal Society of Chemistry, Periyodik Tablo: {self.e['ad']} — {self.e['rsc']}"]
        self.karsilastirma = []

    # -------------------------------------------------------------- kanıtlar

    def kanit_ekle(self, tur, baslik, metin, goster="", kaynak=""):
        kid = f"K{len(self.kanitlar) + 1}"
        self.kanitlar.append([kid, tur, baslik, metin, goster, kaynak])
        return kid

    def yapi_modu(self):
        mod = self.ayar.get("yapi")
        if mod:
            return mod
        e = self.e
        if self.seviye == 1:
            return "z" if e["grup"] is None else "konum"
        if self.seviye == 2:
            return "dizilim" if e["z"] <= 36 else "izotop"
        if self.seviye == 3:
            return "grup"
        return "grup" if e["grup"] not in (None, 3) else ("dizilim" if e["z"] <= 36 else "izotop")

    def periyot_siniri(self):
        """Gruptaki radyoaktif olmayan üyelerin en büyük periyodu (7. periyot ve Po, At, Rn hep radyoaktif)."""
        g = self.e["grup"]
        return max(x["periyot"] for x in E.values() if x["grup"] == g and not x["radyoaktif"])

    def adaylar_grup(self):
        g = self.e["grup"]
        uyeler = [s for s, x in E.items() if x["grup"] == g]
        if not self.e["radyoaktif"]:
            uyeler = [s for s in uyeler if not E[s]["radyoaktif"] and E[s]["periyot"] <= self.periyot_siniri()]
        return sorted(uyeler, key=lambda s: E[s]["z"])

    def yapi_kur(self):
        e, mod = self.e, self.yapi_modu()
        self.mod = mod
        if mod == "konum":
            metin = f"Element periyodik tablonun {e['periyot']}. periyodunda ve {grup_metni(e)} yer alır."
            kid = self.kanit_ekle("konum", "Periyodik tablo kaydı", metin)
        elif mod == "z":
            metin = f"Bu elementin her atomunun çekirdeğinde {e['z']} proton bulunur."
            kid = self.kanit_ekle("atom_numarasi", "Çekirdek analizi", metin)
        elif mod == "dizilim":
            metin = f"Elementin nötr atomunun elektron dizilimi: {dizilim(e['z'])}"
            kid = self.kanit_ekle("elektron_dizilimi", "Elektron dizilimi", metin)
        elif mod == "izotop":
            a = self.ayar.get("izotop") or self.izotop_a()
            self.izotop = a
            n = a - e["z"]
            if e["radyoaktif"]:
                metin = f"Örnekteki atomların kütle numarası {a}; her birinin çekirdeğinde {n} nötron var. Bu atomlar radyoaktif."
            else:
                metin = f"Örnekteki atomların çoğunun kütle numarası {a}; bu atomların çekirdeğinde {n} nötron var."
            kid = self.kanit_ekle("atom_numarasi", "Kütle analizi", metin)
        elif mod == "iyon":
            q, soy = self.ayar.get("iyon") or IYON[self.s]
            self.iyon = (q, soy)
            yuk = f"{'+' if q > 0 else '−'}{abs(q)}"
            metin = (f"Bu elementin atomları {abs(q)} {'elektron vererek' if q > 0 else 'elektron alarak'} {yuk} yüklü iyon "
                     f"oluşturur. Bu iyonun elektron sayısı {kucuk(ad(soy))} atomununkiyle aynıdır.")
            kid = self.kanit_ekle("iyon", "İyon analizi", metin)
        elif mod == "grup":
            self.adaylar = self.ayar.get("adaylar") or self.adaylar_grup()
            if e["grup"] == 7:
                metin = (f"Element periyodik tablonun {grup_metni(e)} yer alır. Bu grubun 5. periyottaki üyesi (teknesyum) "
                         f"radyoaktiftir; örnek ise radyoaktif değil.")
            else:
                metin = f"Element periyodik tablonun {grup_metni(e)} ve ilk {self.periyot_siniri()} periyottan birinde yer alır."
            kid = self.kanit_ekle("konum", "Periyodik tablo kaydı", metin)
        elif mod == "ozel":
            tur, baslik, metin = self.ayar["yapi_ozel"]
            kid = self.kanit_ekle(tur, baslik, metin)
        else:
            raise ValueError(mod)
        self.ref["yapi"] = kid

    def izotop_a(self):
        if self.s in RADYOAKTIF_IZOTOP:
            return RADYOAKTIF_IZOTOP[self.s]
        en, a = -1, None
        for iz in self.e["izotoplar"]:
            try:
                bolluk = float(iz["bilgi"][1])
            except (ValueError, IndexError):
                continue
            if bolluk > en:
                en, a = bolluk, iz["a"]
        assert a, self.s
        return a

    # Ölçüm ve tablo -------------------------------------------------

    def olcum_kur(self):
        """Veri tablosu ve laboratuvar ölçümü. ayar: ozellik, ozellik2, adaylar, olcum=False, tablo_ozel."""
        if self.ayar.get("olcum") is False:
            self.olcumler = []
            return
        if "tablo_ozel" in self.ayar:
            self.ozel_tablo_kur()
            return
        if self.mod == "grup":
            adaylar = self.adaylar
        else:
            adaylar = self.ayar.get("adaylar") or self.komsu_adaylar()
        e = self.e
        oz = self.ayar.get("ozellik") or ("kaynama" if e["hal"] == "gaz" else "yogunluk")
        adaylar = [a for a in adaylar if deger(a, oz) is not None or a == self.s]
        olcumler = []
        pay = self.pay_bul(oz, adaylar)
        oz2 = self.ayar.get("ozellik2")
        if pay is None or oz2:
            # Tek ölçüm adayları ayırmıyor: ikinci bir ölçüm eklenir
            oz2 = oz2 or next(o for o in ("erime", "yogunluk", "kaynama") if o != oz and deger(self.s, o) is not None)
            uyanlar = [a for a in adaylar if self.uyar_mi(a, oz, pay)] if pay else adaylar
            pay1 = pay or self.genis_pay(oz, adaylar)
            olcumler.append((oz, deger(self.s, oz), pay1))
            uyanlar = [a for a in adaylar if self.uyar_mi(a, oz, pay1)]
            pay2 = self.pay_bul(oz2, uyanlar)
            assert pay2, (self.id, self.s, "iki ölçüm de adayları ayırmıyor", adaylar)
            olcumler.append((oz2, deger(self.s, oz2), pay2))
        else:
            olcumler.append((oz, deger(self.s, oz), pay))
        self.olcumler = olcumler
        self.tablo_adaylari = sorted(adaylar, key=lambda s: E[s]["z"])
        sutunlar = [oz] + ([o for o, _, _ in olcumler[1:]] or [self.ikinci_sutun(oz)])
        sutunlar = [s for s in sutunlar if s]
        satirlar = [["Element"] + [OZELLIK[o]["sutun"] for o in sutunlar]]
        for a in self.tablo_adaylari:
            satirlar.append([ad(a)] + [deger_metni(o, deger(a, o), a) for o in sutunlar])
        self.tablolar["T1"] = satirlar
        self.ref["tablo"] = self.kanit_ekle("tablo", "Aday elementlerin verileri", "T1", "", "RSC Periyodik Tablo")
        for i, (o, m, p) in enumerate(olcumler):
            b = ondalik(p)
            metin = OZELLIK[o]["cumle"].format(m=sayi_tr(round(m, b), b), u=sayi_tr(p, b))
            self.ref["olcum" if i == 0 else "olcum2"] = self.kanit_ekle(OZELLIK[o]["tur"], f"Laboratuvar ölçümü: {OZELLIK[o]['ad']}", metin)
        self.karsilastirma = [a for a in self.tablo_adaylari if a != self.s]

    def ozel_tablo_kur(self):
        """Elle verilen tablo ve ölçüm: tablo_ozel=dict(satirlar=[[...]], olcum=(baslik, metin, tur), dogru='satır adı',
        secenekler=[(satır adı, açıklama, hata_turu)], soru=..., ipucu=..., aciklama=...)"""
        t = self.ayar["tablo_ozel"]
        self.tablolar["T1"] = t["satirlar"]
        self.ref["tablo"] = self.kanit_ekle("tablo", t.get("baslik", "Karşılaştırma tablosu"), "T1", "", t.get("kaynak", ""))
        b, m, tur = t["olcum"]
        self.ref["olcum"] = self.kanit_ekle(tur, b, m, "", t.get("olcum_kaynak", ""))
        self.olcumler = ["ozel"]

    def ikinci_sutun(self, oz):
        for o in ("erime", "kaynama", "yogunluk"):
            if o != oz and all(deger(a, o) is not None for a in self.tablo_adaylari if E[a]["hal"] != "gaz" or o != "yogunluk"):
                if o == "yogunluk" and self.e["hal"] == "gaz":
                    continue
                return o
        return None

    def komsu_adaylar(self):
        z = self.e["z"]
        komsular = []
        for dz in (1, -1, 2, -2, 3, -3):
            zz = z + dz
            if 1 <= zz <= 100:
                s = list(E)[zz - 1]
                komsular.append(s)
        return [self.s] + komsular[:3]

    def uyar_mi(self, a, oz, pay):
        v = deger(a, oz)
        m = deger(self.s, oz)
        return v is not None and abs(v - m) <= pay + 1e-9

    def pay_bul(self, oz, adaylar):
        m = deger(self.s, oz)
        if m is None:
            return None
        farklar = [abs(deger(a, oz) - m) for a in adaylar if a != self.s and deger(a, oz) is not None]
        if not farklar:
            return PAYLAR[3]
        en_yakin = min(farklar)
        uygun = [p for p in PAYLAR if p <= 0.4 * en_yakin]
        # Ölçüm, tablodaki değerin hassasiyetinden daha hassas olmasın
        en_kucuk = 0.01 if oz == "yogunluk" else (0.1 if abs(m) < 100 else 1)
        uygun = [p for p in uygun if p >= en_kucuk]
        if oz in ("erime", "kaynama"):
            uygun = [p for p in uygun if m - p > -273]      # mutlak sıfırın altına inen aralık olmaz
        if not uygun:
            return None
        # Çok büyük paylardan kaçın: değerin yaklaşık %5'ini geçmesin
        sinir = max(en_kucuk, abs(m) * 0.05)
        makul = [p for p in uygun if p <= sinir]
        return max(makul) if makul else min(uygun)

    def genis_pay(self, oz, adaylar):
        m = deger(self.s, oz)
        return 0.05 if oz == "yogunluk" and m < 10 else (0.1 if oz == "yogunluk" else 10)

    def arsiv_kur(self, goster):
        self.ref["arsiv"] = self.kanit_ekle("isim", "Arşiv notu", self.e["arsiv"], goster, self.e["rsc"])

    # -------------------------------------------------------------- metin yardımcıları

    def f(self, metin):
        """Elle yazılan metindeki {yapi}, {tablo}, {olcum}, {olcum2}, {arsiv} yer tutucularını doldurur."""
        if not metin:
            return metin

        class Bekleyen(dict):
            def __missing__(self, anahtar):      # henüz numarası bilinmeyen kanıt: sonra doldurulur
                return "{" + anahtar + "}"
        return metin.format_map(Bekleyen(self.ref))

    def gorev(self, asama, arguman, tur, kategori, beceri, soru, ipucu, aciklama, dogru="", hata_turu="", secenekler=()):
        gid = f"G{len(self.gorevler) + 1}"
        self.gorevler.append([gid, asama, arguman, tur, kategori, beceri, soru, ipucu, aciklama, dogru, hata_turu,
                              list(secenekler)])
        return gid

    # -------------------------------------------------------------- otomatik görevler

    def konum_gorevi(self):
        e, mod, k = self.e, self.mod, self.ref["yapi"]
        konum_aciklama = self.konum_aciklamasi()
        if mod == "konum":
            soru = f"Periyodik tablo kaydına ({k}) göre bu element tabloda nerede? Elementi periyodik tabloda bul ve işaretle."
            ipucu = "Periyotlar yatay satırlar, gruplar dikey sütunlardır. Tablonun üstündeki ve solundaki numaralara bak. IUPAC grup numarası, sütunun üstünde yazan sayıdır."
        elif mod == "z":
            soru = f"Çekirdek analizine ({k}) göre bu element hangisi? Elementi periyodik tabloda bul ve işaretle."
            ipucu = "Atom numarası, çekirdekteki proton sayısıdır. Tablodaki her kutunun köşesinde atom numarası yazar."
        elif mod == "dizilim":
            soru = f"Elektron dizilimine ({k}) göre bu element periyodik tabloda nerede? Elementi tabloda bul ve işaretle."
            ipucu = ("En büyük katman numarası periyodu verir. Dizilim s ya da p orbitalinde bitiyorsa son katmandaki elektron "
                     "sayısı A grubunu, d orbitalinde bitiyorsa s ve d elektronlarının toplamı B grubunu gösterir.")
        elif mod == "izotop":
            soru = f"Kütle analizine ({k}) göre elementin atom numarası kaç? Elementi periyodik tabloda bul ve işaretle."
            ipucu = "Kütle numarası = proton sayısı + nötron sayısı. Atom numarası da proton sayısına eşittir."
        elif mod == "iyon":
            soru = f"İyon analizine ({k}) göre elementin atom numarası kaç? Elementi periyodik tabloda bul ve işaretle."
            ipucu = "Nötr atomda elektron sayısı proton sayısına eşittir. Atom elektron verirse pozitif, elektron alırsa negatif yüklü iyon oluşur."
        elif mod == "ozel":
            soru = self.f(self.ayar.get("konum_soru", f"Kanıta ({k}) göre bu element hangisi? Elementi periyodik tabloda bul ve işaretle."))
            ipucu = self.f(self.ayar.get("konum_ipucu", ""))
        else:
            raise ValueError(mod)
        asama = "veri" if self.seviye == 1 else "cikarim"
        beceri = "veri" if self.seviye == 1 else "cikarim"
        return self.gorev(asama, "", "tablo", "kimlik", beceri, soru, ipucu, konum_aciklama, dogru=self.s, hata_turu="veri")

    def konum_aciklamasi(self):
        e, mod = self.e, self.mod
        tanim = f"{kucuk(e['ad'])} ({e['sembol']}, atom numarası {e['z']})"
        if mod == "konum" or mod == "grup":
            return f"{e['periyot']}. periyot ile {HARFLI_GRUP[e['grup']]} grubunun ({e['grup']}. sütun) kesiştiği kutuda {tanim} var."
        if mod == "z":
            yer = ("lantanitler" if lantanit_mi(e) else "aktinitler" if aktinit_mi(e) else None)
            ek = f" Bu element tablonun altındaki {yer} satırında yer alır." if yer else ""
            return f"Atom numarası {e['z']} olan element {kucuk(e['ad'])} ({e['sembol']}).{ek}"
        if mod == "dizilim":
            return self.dizilim_aciklamasi()
        if mod == "izotop":
            a = self.izotop
            return f"Atom numarası = kütle numarası − nötron sayısı = {a} − {a - e['z']} = {e['z']}. {e['z']} numaralı element {kucuk(e['ad'])} ({e['sembol']})."
        if mod == "iyon":
            q, soy = self.iyon
            n = E[soy]["z"]
            if q > 0:
                return (f"{ad(soy)} atomunda {n} elektron var. {q} elektron vermiş iyonda {n} elektron kaldıysa nötr atomda "
                        f"{n + q} elektron, yani {n + q} proton vardır: {kucuk(e['ad'])} ({e['sembol']}).")
            return (f"{ad(soy)} atomunda {n} elektron var. {-q} elektron almış iyonda {n} elektron varsa nötr atomda "
                    f"{n + q} elektron, yani {n + q} proton vardır: {kucuk(e['ad'])} ({e['sembol']}).")
        if mod == "ozel":
            return self.f(self.ayar.get("konum_aciklama", f"Element {e['ad']} ({e['sembol']})."))
        raise ValueError(mod)

    def dizilim_aciklamasi(self):
        e = self.e
        z, p, g = e["z"], e["periyot"], e["grup"]
        d = dizilim(z).split()
        son = d[-1]
        if z == 1:
            return "Tek elektron 1s orbitalinde: 1. periyot, 1A grubu. Bu yer hidrojenin (H, atom numarası 1)."
        if z == 2:
            return "Tek katman (1s²) tamamen dolu: 1. periyot. Helyum, dolu katmanı nedeniyle soy gazlarla birlikte 8A grubundadır (He, atom numarası 2)."
        cevap = f"{kucuk(e['ad'])} ({e['sembol']}, atom numarası {z})"
        if e["blok"] == "s":
            return (f"Dizilim {son} ile bitiyor: en büyük katman numarası {p}, bu yüzden {p}. periyot. Son katmanda {g} elektron var "
                    f"ve dizilim s orbitalinde bitiyor: {HARFLI_GRUP[g]} grubu. Bu yer {cevap}.")
        if e["blok"] == "p":
            s_son = next(x for x in d if x.startswith(f"{p}s"))
            v = g - 10
            return (f"En büyük katman numarası {p}: {p}. periyot. Son katmanda {s_son} ve {son} var, yani {v} değerlik elektronu; "
                    f"dizilim p orbitalinde bittiği için {HARFLI_GRUP[g]} grubu. Bu yer {cevap}.")
        s_son = next(x for x in d if x.startswith(f"{p}s"))
        d_son = next(x for x in d if x.startswith(f"{p - 1}d"))
        toplam = g
        grup_adi = HARFLI_GRUP[g]
        return (f"Dizilim d orbitalinde bitiyor: d bloğu, yani bir geçiş metali. En büyük katman {p}: {p}. periyot. "
                f"{s_son} ve {d_son} elektronlarının toplamı {toplam}: {grup_adi} grubu (IUPAC {g}. grup). Bu yer {cevap}.")

    def olcum_gorevi(self):
        if self.olcumler == ["ozel"]:
            return self.ozel_olcum_gorevi()
        e = self.e
        k_tablo = self.ref["tablo"]
        if len(self.olcumler) == 1:
            oz, m, p = self.olcumler[0]
            b = ondalik(p)
            bilgi = OZELLIK[oz]
            alt, ust = sayi_tr(round(m - p, b), b), sayi_tr(round(m + p, b), b)
            soru = (f"Ölçülen {bilgi['ad']} {sayi_tr(round(m, b), b)} ± {sayi_tr(p, b)} {bilgi['birim']} ({self.ref['olcum']}). "
                    f"Tablodaki ({k_tablo}) adaylardan hangisi bu ölçümle uyumlu?")
            ipucu = f"Ölçüm aralığı {alt} ile {ust} {bilgi['birim']} arasıdır. Tabloda bu aralığa giren değeri ara."
            aciklama = (f"Ölçüm {alt}–{ust} {bilgi['birim']} aralığını gösteriyor. Tablodaki adaylardan bu aralığa yalnızca "
                        f"{kucuk(e['ad'])} ({deger_metni(oz, deger(self.s, oz), self.s)} {bilgi['birim']}) giriyor.")
            secenekler = []
            for a in self.tablo_adaylari:
                if a == self.s:
                    secenekler.append((ad(a), "evet", "", "", ""))
                    continue
                v = deger(a, oz)
                yakin = abs(v - m) <= 3 * p
                secenekler.append((ad(a), "", "birim" if yakin else "veri", self.ref["olcum"],
                                   f"Tabloya göre {kucuk(ad(a))}: {deger_metni(oz, v, a)} {bilgi['birim']}. Bu değer ölçüm aralığının "
                                   f"({alt}–{ust}) dışında kalıyor."
                                   + (" Ölçümün ± payını hesaba kat." if yakin else "")))
        else:
            (o1, m1, p1), (o2, m2, p2) = self.olcumler
            b1, b2 = ondalik(p1), ondalik(p2)
            i1, i2 = OZELLIK[o1], OZELLIK[o2]
            a1, u1 = round(m1 - p1, b1), round(m1 + p1, b1)
            a2, u2 = round(m2 - p2, b2), round(m2 + p2, b2)
            soru = (f"İki ölçüm var: {i1['ad']} {sayi_tr(round(m1, b1), b1)} ± {sayi_tr(p1, b1)} {i1['birim']} ({self.ref['olcum']}) ve "
                    f"{i2['ad']} {sayi_tr(round(m2, b2), b2)} ± {sayi_tr(p2, b2)} {i2['birim']} ({self.ref['olcum2']}). "
                    f"Tablodaki ({k_tablo}) adaylardan hangisi iki ölçümle de uyumlu?")
            ipucu = (f"Önce {i1['ad']} ölçümüne uyan adayları bul ({sayi_tr(a1, b1)}–{sayi_tr(u1, b1)} {i1['birim']}), sonra bunlar "
                     f"arasından {i2['ad']} ölçümüne uyanı seç ({sayi_tr(a2, b2)}–{sayi_tr(u2, b2)} {i2['birim']}).")
            uyan1 = [a for a in self.tablo_adaylari if self.uyar_mi(a, o1, p1)]
            aciklama = (f"{i1['ad'].capitalize()} ölçümüne {adlar(uyan1)} uyuyor; tek başına yetmiyor. Bunlardan {i2['ad']} ölçümüne "
                        f"yalnızca {kucuk(e['ad'])} ({deger_metni(o2, deger(self.s, o2), self.s)} {i2['birim']}) uyuyor.")
            secenekler = []
            for a in self.tablo_adaylari:
                if a == self.s:
                    secenekler.append((ad(a), "evet", "", "", ""))
                    continue
                v1, v2 = deger(a, o1), deger(a, o2)
                if self.uyar_mi(a, o1, p1):
                    acik = (f"Tabloya göre {kucuk(ad(a))}: {i1['ad']} {deger_metni(o1, v1, a)} {i1['birim']} (uyumlu), ama {i2['ad']} "
                            f"{deger_metni(o2, v2, a)} {i2['birim']}; ikinci ölçümle uyuşmuyor. Verilerin hepsini birlikte değerlendir.")
                    secenekler.append((ad(a), "", "veri", self.ref["olcum2"], acik))
                else:
                    acik = (f"Tabloya göre {kucuk(ad(a))}: {i1['ad']} {deger_metni(o1, v1, a)} {i1['birim']}. Bu değer ilk ölçümün aralığının "
                            f"({sayi_tr(a1, b1)}–{sayi_tr(u1, b1)}) dışında.")
                    secenekler.append((ad(a), "", "birim" if abs(v1 - m1) <= 3 * p1 else "veri", self.ref["olcum"], acik))
        return self.gorev("veri", "", "tekli", "kanit", "veri", soru, ipucu, aciklama, hata_turu="veri", secenekler=secenekler)

    def ozel_olcum_gorevi(self):
        t = self.ayar["tablo_ozel"]
        secenekler = []
        for metin, acik, hata in t["secenekler"]:
            if metin == t["dogru"]:
                secenekler.append((metin, "evet", "", "", ""))
            else:
                secenekler.append((metin, "", hata, self.ref["olcum"], self.f(acik)))
        if t["dogru"] not in [m for m, _, _ in t["secenekler"]]:
            secenekler.insert(0, (t["dogru"], "evet", "", "", ""))
        return self.gorev("veri", "", "tekli", "kanit", "veri", self.f(t["soru"]), self.f(t.get("ipucu", "")),
                          self.f(t.get("aciklama", "")), hata_turu="veri", secenekler=secenekler)

    def aday_gorevi(self):
        e = self.e
        k = self.ref["yapi"]
        adaylar = self.adaylar
        harf = HARFLI_GRUP[e["grup"]]
        soru = f"Periyodik tablo kaydına ({k}) göre hangi elementler aday olabilir? Periyodik tabloda bütün adayları işaretle."
        if e["grup"] == 7:
            ipucu = f"{harf} grubu, tablonun {e['grup']}. sütunudur. Teknesyumu ve 7. periyottaki yapay elementi işaretleme."
            kosul = "radyoaktif olmayan"
        else:
            n = self.periyot_siniri()
            ipucu = f"{harf} grubu, tablonun {e['grup']}. sütunudur. Sütunda yukarıdan aşağı, ilk {n} periyottaki elementleri işaretle."
            kosul = f"ilk {n} periyotta"
        aciklama = (f"{harf} grubunda {kosul} {len(adaylar)} element var: {adlar(adaylar)}. "
                    f"Kanıt adayları {len(adaylar)} elemente indirdi ama tek bir sonuca ulaştırmadı; başka bir kanıt gerekiyor.")
        return self.gorev("hipotez", "", "tablo", "kanit", "hipotez", soru, ipucu, aciklama, dogru=" ".join(adaylar), hata_turu="veri")

    def rakip_gorevi(self):
        e = self.e
        rakip = self.ayar.get("rakip") or self.en_yakin_rakip()
        oz, m, p = self.olcumler[0] if self.olcumler != ["ozel"] else (None, None, None)
        k_olcum, k_yapi = self.ref["olcum"], self.ref["yapi"]
        genel = self.ayar.get("rakip_genel", "K1")
        genel_baslik = next(k[2] for k in self.kanitlar if k[0] == genel)
        yapi_baslik = next(k[2] for k in self.kanitlar if k[0] == k_yapi)
        if oz:
            v = deger(rakip, oz)
            b = ondalik(p)
            bilgi = OZELLIK[oz]
            neden = (f"Tabloya göre {kucuk(ad(rakip))}: {deger_metni(oz, v, rakip)} {bilgi['birim']}. Ölçülen {bilgi['ad']} "
                     f"({sayi_tr(round(m, b), b)} ± {sayi_tr(p, b)} {bilgi['birim']}) bu değerle uyuşmuyor; bu yüzden ölçüm iddiayı çürütür.")
            if len(self.olcumler) > 1 and self.uyar_mi(rakip, oz, p):
                o2, m2, p2 = self.olcumler[1]
                b2 = ondalik(p2)
                k_olcum = self.ref["olcum2"]
                neden = (f"Tabloya göre {kucuk(ad(rakip))}: {OZELLIK[o2]['ad']} {deger_metni(o2, deger(rakip, o2), rakip)} {OZELLIK[o2]['birim']}. "
                         f"İkinci ölçüm ({sayi_tr(round(m2, b2), b2)} ± {sayi_tr(p2, b2)} {OZELLIK[o2]['birim']}) bu değerle uyuşmuyor; "
                         f"bu yüzden iddiayı çürüten kanıt budur.")
        else:
            neden = self.f(self.ayar["rakip_neden"])
        olcum_baslik = next(k[2] for k in self.kanitlar if k[0] == k_olcum)
        soru = f"Bir stajyer, elementin {kucuk(ad(rakip))} olduğunu iddia ediyor. Bu iddiayı en açık biçimde hangi kanıt çürütür?"
        ipucu = f"Her kanıt için sor: Bu kanıt {kucuk(ad(rakip))} için de geçerli olabilir mi?"
        secenekler = [
            (f"{k_olcum} · {olcum_baslik}", "evet", "", "", ""),
            (f"{k_yapi} · {yapi_baslik}", "", "kanitsiz", k_yapi,
             self.f(self.ayar.get("rakip_yapi_neden", f"{ad(rakip)} {de_eki(ad(rakip))} aynı grupta yer alıyor; bu kanıt onu elemez."))),
            (f"{genel} · {genel_baslik}", "", "iliski", genel,
             self.f(self.ayar.get("rakip_genel_neden", f"Bu gözlem {kucuk(ad(rakip))} için de geçerli olabilir; tek başına onu elemez."))),
        ]
        self.rakip = rakip
        self.karsilastirma = sorted(set(self.karsilastirma) | {rakip}, key=lambda s: E[s]["z"])
        return self.gorev("kanit", "karsi_kanit", "tekli", "alternatif", "hipotez", soru, ipucu, neden, hata_turu="kanitsiz",
                          secenekler=secenekler)

    def en_yakin_rakip(self):
        oz, m, p = self.olcumler[0]
        digerleri = [a for a in self.tablo_adaylari if a != self.s and deger(a, oz) is not None]
        return min(digerleri, key=lambda a: abs(deger(a, oz) - m))

    def kanit_gorevi(self, asama="kanit"):
        e = self.e
        gerekli = [self.ref["yapi"]]
        if "olcum" in self.ref:
            gerekli.append(self.ref["olcum"])
        if "olcum2" in self.ref:
            gerekli.append(self.ref["olcum2"])
        serbest = [self.ref["tablo"]] if "tablo" in self.ref else []
        genel = []
        for i, ip in enumerate(self.v["ipuclari"]):
            kid = f"K{i + 1}"
            rol = ip[3] if len(ip) > 3 else "genel"
            if rol == "gerekli":
                gerekli.append(kid)
            elif rol == "serbest":
                serbest.append(kid)
            else:
                genel.append(kid)
        if self.ayar.get("kanit_gerekli"):
            gerekli = list(self.ayar["kanit_gerekli"])
        if self.ayar.get("kanit_serbest") is not None:
            serbest = list(self.ayar["kanit_serbest"])
        soru = (f"İddia: Element {kucuk(e['ad'])}. Bu iddiayı destekleyen ve diğer adayları eleyen kanıtları seç. "
                f"Tek başına ayırt edici olmayan kanıtları seçme.")
        ipucu = "Her kanıt için sor: Bu kanıt bir adayı eliyor ya da elementin yerini gösteriyor mu? Elementin adının hikâyesi bir kanıt değildir."
        parcalar = []
        yapi_cumle = {"konum": "elementin periyodik tablodaki yerini gösterir", "z": "atom numarasını gösterir",
                      "dizilim": "elementin periyodunu ve grubunu gösterir", "izotop": "atom numarasını hesaplamayı sağlar",
                      "iyon": "atom numarasını hesaplamayı sağlar", "grup": "adayları tek bir gruba indirir",
                      "ozel": "elementin kimliğini gösterir"}[self.mod]
        parcalar.append(f"{self.ref['yapi']} {yapi_cumle}.")
        if "olcum" in self.ref:
            parcalar.append(f"{self.ref['olcum']}{' ve ' + self.ref['olcum2'] if 'olcum2' in self.ref else ''} ölçümü tablodaki diğer adayları eler.")
        if len(genel) == 1:
            parcalar.append(f"{genel[0]} pek çok element için de geçerli olabilecek bir gözlemdir; tek başına ayırt edici değildir.")
        elif genel:
            parcalar.append(f"{' ve '.join([', '.join(genel[:-1]), genel[-1]])} pek çok element için de geçerli olabilecek gözlemlerdir; tek başına ayırt edici değildir.")
        if "arsiv" in self.ref:
            parcalar.append(f"Arşiv notu ({self.ref['arsiv']}) adın hikâyesini anlatır; bu örneğin kimliği için bir kanıt değildir.")
        dogru = " ".join(gerekli + [f"({k})" for k in serbest])
        return self.gorev(asama, "kanit", "kanit", "kanit", "kanit", soru, ipucu, " ".join(parcalar), dogru=dogru, hata_turu="kanitsiz")

    def yaz_gorevi(self):
        e = self.e
        soru = "Kanıtlara göre bu element hangisi? Adını ya da sembolünü yaz."
        ipucu = {"dizilim": "En büyük katman numarası periyodu, son katmandaki elektronlar grubu gösterir.",
                 "izotop": "Atom numarası = kütle numarası − nötron sayısı.",
                 "iyon": "İyonun elektron sayısına verdiği ya da aldığı elektronları ekle ya da çıkar.",
                 "grup": "Önce gruptaki adayları düşün, sonra ölçümle eşleşeni bul.",
                 "konum": "Periyot ve grubun kesiştiği kutuya bak.",
                 "z": "Atom numarası, çekirdekteki proton sayısıdır.",
                 "ozel": self.f(self.ayar.get("yaz_ipucu", "Kanıtları birlikte değerlendir."))}[self.mod]
        aciklama = self.konum_aciklamasi()
        if self.mod == "grup" and getattr(self, "olcumler", None) and self.olcumler != ["ozel"]:
            oz, m, p = self.olcumler[0]
            aciklama = (f"{self.ref['yapi']} adayları {HARFLI_GRUP[e['grup']]} grubuna indiriyor ({adlar(self.adaylar)}). "
                        f"Ölçümler ({self.ref['olcum']}{', ' + self.ref['olcum2'] if 'olcum2' in self.ref else ''}) yalnızca "
                        f"{kucuk(e['ad'])} ile uyumlu. Element {e['ad']} ({e['sembol']}).")
        return self.gorev("cikarim", "iddia", "yaz", "kimlik", "cikarim", soru, ipucu, aciklama, dogru="", hata_turu="kanitsiz")

    def isim_gorevi(self):
        e = self.e
        diger = self.ayar.get("isim_celdirici") or self.isim_celdiricileri()
        soru = f"Arşiv notuna ({self.ref['arsiv']}) göre bu elementin adı nereden geliyor?"
        secenekler = [(e["kisa_koken"], "evet", "", "", "")]
        for s in diger:
            secenekler.append((E[s]["kisa_koken"], "", "veri", self.ref["arsiv"],
                               f"Bu, {kucuk(ad(s))} elementinin adının kökeni. Arşiv notunu yeniden oku."))
        return self.gorev("sonuc", "", "tekli", "isim", "gozlem", soru, "Arşiv notunun ilk cümlesini oku.", e["arsiv"],
                          hata_turu="veri", secenekler=secenekler)

    def isim_celdiricileri(self):
        # Kökeni farklı türden (yer adı, Yunanca kelime, kişi) iki element seç; aynı kökenleri ele
        z = self.e["z"]
        adaylar = [s for s in E if s != self.s and E[s]["kisa_koken"] != self.e["kisa_koken"]]
        sira = sorted(adaylar, key=lambda s: ((E[s]["z"] * 37 + z * 11) % 101))
        secilen = []
        for s in sira:
            if all(E[s]["kisa_koken"] != E[x]["kisa_koken"] for x in secilen):
                secilen.append(s)
            if len(secilen) == 2:
                break
        return secilen

    def sinif_gorevi(self):
        e = self.e
        dogru = sinif(e)
        yer = "hidrojen" if self.s == "H" else dogru
        bolge = {
            "metal": "tablonun solunda ve ortasında, metaller bölgesinde",
            "hidrojen": "tablonun sol üst köşesinde, 1A grubunun başında",
            "ametal": "tablonun sağ üst bölümünde, ametaller arasında",
            "yarı metal": "metallerle ametalleri ayıran merdiven çizgisi boyunca",
            "soy gaz": "8A grubunda, soy gazlar arasında",
        }
        nerede = {"metal": "Metaller tablonun solunda ve ortasında yer alır.",
                  "ametal": "Ametaller (hidrojen dışında) tablonun sağ üst bölümünde yer alır.",
                  "yarı metal": "Yarı metaller metallerle ametalleri ayıran merdiven çizgisi boyunca dizilir: B, Si, Ge, As, Sb, Te.",
                  "soy gaz": "Soy gazlar 8A grubunda yer alır."}
        secenekler = []
        for snf in ("metal", "ametal", "yarı metal", "soy gaz"):
            metin = snf.capitalize()
            if snf == dogru:
                secenekler.append((metin, "evet", "", "", ""))
            else:
                secenekler.append((metin, "", "veri", self.ref["yapi"],
                                   f"{nerede[snf]} {e['ad']} ise {bolge[yer]} bulunur."))
        soru = f"Periyodik tablodaki yerine ({self.ref['yapi']}) göre bu element hangi sınıfa girer?"
        ek = " Hidrojen 1A grubunda olsa da bir ametaldir." if self.s == "H" else ""
        ek_dir = "dır" if dogru == "soy gaz" else "dir"
        aciklama = f"{e['ad']} bir {dogru}{ek_dir}: {bolge[yer]} bulunur.{ek}"
        return self.gorev("sonuc", "", "tekli", "kanit", "cikarim", soru,
                          "Periyodik tabloda metaller solda ve ortada, ametaller sağ üstte, soy gazlar en sağ sütundadır.",
                          aciklama, hata_turu="veri", secenekler=secenekler)

    def savunma_gorevi(self):
        e = self.e
        k = self.ref["yapi"]
        yapi_kisa = {
            "dizilim": f"elektron dizilimi ({k}) elementi {e['periyot']}. periyot{', ' + HARFLI_GRUP[e['grup']] + ' grubuna' if e['grup'] else 'a'} yerleştiriyor",
            "izotop": f"kütle analizine ({k}) göre atom numarası {getattr(self, 'izotop', 0)} − {getattr(self, 'izotop', 0) - e['z']} = {e['z']}",
            "iyon": f"iyon analizi ({k}) atom numarasının {e['z']} olduğunu gösteriyor",
            "grup": f"periyodik tablo kaydı ({k}) adayları {HARFLI_GRUP[e['grup']] if e['grup'] else ''} grubuna indiriyor",
            "konum": f"periyodik tablo kaydı ({k}) elementin yerini gösteriyor",
            "z": f"çekirdekteki proton sayısı ({k}) {e['z']}",
            "ozel": self.f(self.ayar.get("savunma_yapi", f"kanıt ({k}) elementin kimliğini gösteriyor")),
        }[self.mod]
        parcalar = [f"İddia: Element {kucuk(e['ad'])} ({e['sembol']}).", f"Kanıt: {yapi_kisa}"]
        if getattr(self, "olcumler", None) and self.olcumler != ["ozel"]:
            oz, m, p = self.olcumler[0]
            b = ondalik(p)
            parcalar[-1] += (f"; ölçülen {OZELLIK[oz]['ad']} ({sayi_tr(round(m, b), b)} ± {sayi_tr(p, b)} {OZELLIK[oz]['birim']}, "
                             f"{self.ref['olcum']}) tablodaki adaylardan yalnızca {kucuk(e['ad'])} ile uyumlu.")
        elif self.olcumler == ["ozel"]:
            parcalar[-1] += "; " + self.f(self.ayar["tablo_ozel"].get("savunma", "ölçüm de bu sonucu destekliyor.")).rstrip(".") + "."
        else:
            parcalar[-1] += "."
        gerekce = self.f(self.ayar.get("gerekce") or self.v["kullanim"]["dogru"])
        parcalar.append(f"Gerekçe: {gerekce.rstrip('.')}.")
        if getattr(self, "olcumler", None) and self.olcumler and self.olcumler != ["ozel"]:
            rakip = self.ayar.get("rakip") or self.en_yakin_rakip()
            oz, m, p = self.olcumler[0]
            v = deger(rakip, oz)
            parcalar.append(f"Karşı kanıt: {kucuk(ad(rakip))} adayı da düşünülebilirdi, ama {OZELLIK[oz]['ad']} değeri "
                            f"{deger_metni(oz, v, rakip)} {OZELLIK[oz]['birim']}; ölçümle uyuşmuyor.")
        elif self.ayar.get("karsi_kanit"):
            parcalar.append("Karşı kanıt: " + self.f(self.ayar["karsi_kanit"]))
        parcalar.append(f"Sonuç: Kanıtlar elementin {kucuk(e['ad'])} olduğunu gösteriyor.")
        soru = ("Jüriye savun: Bu element hangisi ve vakadaki işte neden kullanılıyor? İddianı yaz, kanıtlarını numaralarıyla göster "
                "(örneğin K3), gerekçeni açıkla ve bir rakip adayı neden elediğini söyle.")
        return self.gorev("sonuc", "sonuc", "savunma", "gerekce", "gerekce", soru, "", " ".join(parcalar))

    # -------------------------------------------------------------- elle yazılan görevler

    def elle_soru(self, soru, asama, arguman, kategori, beceri):
        secenekler = [(self.f(soru["dogru"]), "evet", "", "", "")]
        for metin, hata, aciklama, kanit in soru["yanlislar"]:
            secenekler.append((self.f(metin), "", hata, self.f(kanit), self.f(aciklama)))
        return self.gorev(asama, arguman, "tekli", kategori, beceri, self.f(soru["soru"]), self.f(soru["ipucu"]),
                          self.f(soru["aciklama"]), hata_turu=soru["yanlislar"][0][1] if soru["yanlislar"] else "veri",
                          secenekler=secenekler)

    # -------------------------------------------------------------- kurulum

    def kur(self):
        v = self.v
        for ip in v["ipuclari"]:
            tur, baslik, metin = ip[:3]
            kaynak = ip[4] if len(ip) > 4 else ""
            self.kanit_ekle(tur, baslik, metin, "", kaynak)
        self.yapi_kur()
        sv = self.seviye
        if sv >= 2:
            self.olcum_kur()
        else:
            self.olcumler = []
        gorevler = self.ayar.get("gorevler") or {
            1: ["gozlem", "konum", "kullanim", "isim" if self.ilk_vaka else "sinif"],
            2: ["gozlem", "konum", "olcum", "kullanim", "kanit"],
            3: ["aday", "olcum", "rakip", "kullanim", "kanit"],
            4: ["gozlem", "yaz", "kullanim", "kanit", "savunma"],
        }[sv]
        if not self.olcumler:
            gorevler = [g for g in gorevler if g not in ("olcum", "rakip")]
        kimlik_gorevi = next(g for g in gorevler if g in ("konum", "olcum", "yaz"))
        arsiv_bekliyor = True
        for g in gorevler:
            if g == "gozlem":
                gid = self.elle_soru(v["gozlem"], "gozlem", "", "kanit", "gozlem")
            elif g == "kullanim":
                gid = self.elle_soru(v["kullanim"], "cikarim", "gerekce" if sv == 4 else "", "ozellik_kullanim",
                                     "gerekce" if sv >= 3 else "cikarim")
            elif g == "ek":
                for ek in self.ayar.get("ek_sorular", []):
                    gid = self.elle_soru(ek, "cikarim", "", ek.get("kategori", "kanit"), ek.get("beceri", "cikarim"))
            elif g == "konum":
                gid = self.konum_gorevi()
            elif g == "olcum":
                gid = self.olcum_gorevi()
            elif g == "aday":
                gid = self.aday_gorevi()
            elif g == "rakip":
                gid = self.rakip_gorevi()
            elif g == "kanit":
                gid = self.kanit_gorevi()
            elif g == "yaz":
                gid = self.yaz_gorevi()
            elif g == "isim":
                gid = self.isim_gorevi()
            elif g == "sinif":
                gid = self.sinif_gorevi()
            elif g == "savunma":
                gid = self.savunma_gorevi()
            else:
                raise ValueError(g)
            if g == kimlik_gorevi and arsiv_bekliyor:
                self.arsiv_kur(gid)
                arsiv_bekliyor = False
        # Yer tutucuları, görevler kurulduktan sonra bilinen numaralarla yeniden doldur
        self.gorevler = [[*g[:6], self.f(g[6]), self.f(g[7]), self.f(g[8]), g[9], g[10],
                          [(self.f(s[0]), s[1], s[2], self.f(s[3]), self.f(s[4])) for s in g[11]]] for g in self.gorevler]
        kaynaklar = list(self.kaynakca)
        if self.karsilastirma:
            kaynaklar.append(f"Royal Society of Chemistry, Periyodik Tablo: {adlar(self.karsilastirma)} (karşılaştırma verileri) — {RSC_GENEL}")
        kaynaklar += self.ayar.get("kaynak", [])
        return dict(
            id=self.id, seviye=sv, sira=self.sira, baslik=v["baslik"], giris=self.f(v["giris"]), cevap=self.s,
            tema=v["tema"], final=False, ornek=False, kaynakca=kaynaklar,
            kanitlar=[tuple(k) for k in self.kanitlar], tablolar=self.tablolar,
            gorevler=[tuple(g) for g in self.gorevler],
        )
