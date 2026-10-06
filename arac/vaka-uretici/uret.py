# -*- coding: utf-8 -*-
"""Element Dosyaları: 200 vakanın içerik tablolarını (CSV) ve öğretmen için cevap listesini üretir.

Kullanım:  python uret.py            (oyunun klasörüne yazar: icerik/*.csv ve VAKALAR.md)
           python uret.py <klasör>   (başka bir klasöre yazar; denemek için)
- Eski 20 dosya (D01–D20) eski/ klasöründeki üreticilerden olduğu gibi alınır, yeni numara ve tema verilir.
- Yeni 180 vaka s1*.py, s2*.py, s3*.py, s4*.py dosyalarında tanımlıdır; sablon.py ile kurulur.
- Tablolar Türkçe Excel'de doğru açılsın diye UTF-8 BOM'lu ve noktalı virgül ayırıcılı yazılır.
"""
import collections
import re
import csv
import importlib
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "eski"))

from elementler import E  # noqa: E402
from sablon import Kurucu  # noqa: E402

HEDEF = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else KOK.parents[1]
ICERIK = HEDEF / "icerik"

DOSYA_SUTUNLARI = ["id", "seviye", "sira", "tema", "baslik", "giris", "cevap", "final", "ornek", "kaynakca"]
KANIT_SUTUNLARI = ["dosya", "id", "tur", "baslik", "metin", "goster", "kaynak"]
TABLO_SUTUNLARI = ["dosya", "tablo", "h1", "h2", "h3", "h4", "h5", "h6"]
GOREV_SUTUNLARI = ["dosya", "id", "asama", "arguman", "tur", "kategori", "beceri", "soru", "ipucu", "aciklama",
                   "dogru", "hata_turu"]
SECENEK_SUTUNLARI = ["dosya", "gorev", "metin", "dogru", "hata_turu", "hata_kaniti", "hata_aciklamasi"]

ESKI_TEMALAR = {"D01": "teknoloji", "D02": "ev", "D03": "ev", "D04": "ev", "D05": "saglik", "D06": "saglik",
                "D07": "sanat", "D08": "saglik", "D09": "teknoloji", "D10": "ev", "D11": "tarih", "D12": "adli",
                "D13": "sanayi", "D14": "saglik", "D15": "ev", "D16": "teknoloji", "D17": "saglik", "D18": "sanat",
                "D19": "teknoloji", "D20": "adli"}


def eski_dosyalar():
    sys.argv = [sys.argv[0], str(ICERIK)]       # eski D01 üreticisi hedefi komut satırından okur
    d01 = importlib.import_module("dosya_sablonu_uret")
    bilgi = d01.DOSYALAR[0]
    dosyalar = [dict(
        id="D01", seviye=1, baslik=bilgi["baslik"], giris=bilgi["giris"], cevap=bilgi["cevap"], ornek=True,
        kaynakca=bilgi["kaynakca"].split(" | "), kanitlar=d01.KANITLAR, tablolar={"T1": d01.TABLO},
        gorevler=[(*g[:11], list(g[11])) for g in d01.GOREVLER])]
    for ad in ("dosyalar_veri", "dosyalar_veri2", "dosyalar_veri3", "dosyalar_veri4"):
        dosyalar += importlib.import_module(ad).DOSYALAR
    assert [d["id"] for d in dosyalar] == [f"D{n:02d}" for n in range(1, 21)]
    for d in dosyalar:
        d["tema"] = ESKI_TEMALAR[d["id"]]
        d["eski_id"] = d["id"]
    return dosyalar


def yeni_vakalar():
    vakalar = {1: [], 2: [], 3: [], 4: []}
    for yol in sorted(KOK.glob("s[1-4]*.py")):
        if not re.fullmatch(r"s[1-4][a-z]?", yol.stem):
            continue
        modul = importlib.import_module(yol.stem)
        for v in modul.VAKALAR:
            assert v["seviye"] == int(yol.stem[1]), (yol.stem, v["sembol"], v["baslik"])
            vakalar[v["seviye"]].append(v)
    return vakalar


def main():
    from kaynaklar import EK_KAYNAK
    eskiler = eski_dosyalar()
    yeniler = yeni_vakalar()
    basliklar = {v["baslik"]: v for liste in yeniler.values() for v in liste}
    assert len(basliklar) == sum(len(x) for x in yeniler.values()), "aynı başlıklı iki vaka var"
    for baslik, kaynaklar in EK_KAYNAK.items():
        assert baslik in basliklar, f"kaynaklar.py: '{baslik}' başlıklı vaka yok"
        v = basliklar[baslik]
        v["ayar"]["kaynak"] = list(v["ayar"].get("kaynak", [])) + [k for k in kaynaklar if k not in v["ayar"].get("kaynak", [])]
    # İsim kökeni sorusu her element için yalnızca bir kez sorulur (eski dosyalarda sorulanlar dahil)
    isim_soruldu = {d["cevap"] for d in eskiler if any(g[4] == "isim" for g in d["gorevler"])}

    sirali = []
    for seviye in (1, 2, 3, 4):
        eski = [d for d in eskiler if d["seviye"] == seviye and not d.get("final")]
        final = [d for d in eskiler if d["seviye"] == seviye and d.get("final")]
        sirali += [("eski", d) for d in eski] + [("yeni", v) for v in yeniler[seviye]] + [("eski", d) for d in final]

    dosyalar = []
    for no, (tur, x) in enumerate(sirali, start=1):
        vaka_id = f"V{no:03d}"
        if tur == "eski":
            d = dict(x)
            d["id"] = vaka_id
        else:
            ilk = x["sembol"] not in isim_soruldu
            d = Kurucu(x, vaka_id, no, ilk).kur()
            if any(g[4] == "isim" for g in d["gorevler"]):
                isim_soruldu.add(x["sembol"])
        d["sira"] = no
        dosyalar.append(d)

    d_satir, k_satir, t_satir, g_satir, s_satir = [], [], [], [], []
    for d in dosyalar:
        d_satir.append([d["id"], d["seviye"], d["sira"], d["tema"], d["baslik"], d["giris"], d["cevap"],
                        "evet" if d.get("final") else "", "evet" if d.get("ornek") else "", " | ".join(d["kaynakca"])])
        for k in d["kanitlar"]:
            k_satir.append([d["id"], *k])
        for tablo_id, satirlar in d["tablolar"].items():
            for satir in satirlar:
                assert len(satir) <= 6, (d["id"], tablo_id, satir)
                t_satir.append([d["id"], tablo_id, *satir])
        for g in d["gorevler"]:
            g_satir.append([d["id"], *g[:11]])
            for s in g[11]:
                s_satir.append([d["id"], g[0], *s])

    ICERIK.mkdir(parents=True, exist_ok=True)
    for ad, sutunlar, satirlar in (("dosyalar.csv", DOSYA_SUTUNLARI, d_satir), ("kanitlar.csv", KANIT_SUTUNLARI, k_satir),
                                   ("tablolar.csv", TABLO_SUTUNLARI, t_satir), ("gorevler.csv", GOREV_SUTUNLARI, g_satir),
                                   ("secenekler.csv", SECENEK_SUTUNLARI, s_satir)):
        with open(ICERIK / ad, "w", encoding="utf-8-sig", newline="") as f:
            yazici = csv.writer(f, delimiter=";", lineterminator="\r\n")
            yazici.writerow(sutunlar)
            yazici.writerows(satirlar)

    sizintilar = [m for d in dosyalar if "eski_id" not in d for m in sizinti_kontrolu(d)]
    for m in sizintilar:
        print("SIZINTI", m)
    cevap_listesi_yaz(dosyalar)
    sayac = collections.Counter(d["cevap"] for d in dosyalar)
    print(f"{len(d_satir)} dosya, {len(k_satir)} kanıt, {len(g_satir)} görev, {len(s_satir)} seçenek; "
          f"{len(sayac)} farklı element")
    for seviye in (1, 2, 3, 4):
        print(f"  Seviye {seviye}: {sum(1 for d in dosyalar if d['seviye'] == seviye)} dosya")


def kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()


def sizinti_kontrolu(d):
    """Element bulunmadan önce görünen metinlerde elementin adı geçiyor mu?"""
    from sablon import ad
    adi = kucuk(ad(d["cevap"]))
    kok = adi[:-1] if len(adi) > 4 else adi          # 'kükürt' -> 'kükür' (kükürdün gibi ekli hâller)
    sorunlar = []

    desen = re.compile(r"(?<![a-zçğıöşüâîû])" + re.escape(kok))     # kelime başında ('periyot' içindeki 'iyot' sayılmaz)

    def bak(yer, metin):
        bulunan = desen.search(kucuk(metin)) if metin else None
        if bulunan:
            sorunlar.append(f"{d['id']} {d['cevap']} {yer}: …{metin[max(0, bulunan.start() - 30):][:90]}…")

    bak("giris", d["giris"])
    kimlik_gorevleri = [g for g in d["gorevler"] if g[4] in ("kimlik",) or (g[3] == "tekli" and g[4] == "kanit" and g[5] == "veri")]
    ilk_kimlik = d["gorevler"].index(kimlik_gorevleri[0]) if kimlik_gorevleri else len(d["gorevler"])
    acilan = {k[0] for k in d["kanitlar"] if not k[4]}
    for k in d["kanitlar"]:
        if not k[4] and k[1] != "tablo":
            bak(f"kanıt {k[0]}", k[3])
    for g in d["gorevler"][:ilk_kimlik + 1]:
        son = g is d["gorevler"][ilk_kimlik] if ilk_kimlik < len(d["gorevler"]) else False
        bak(f"{g[0]} soru", g[6])
        bak(f"{g[0]} ipucu", g[7])
        aday_gorevi = g[3] == "tablo" and g[5] == "hipotez"      # açıklaması bütün adayları sayar
        if not son and not aday_gorevi:
            bak(f"{g[0]} açıklama", g[8])
        for sec in g[11]:
            if sec[1] != "evet" or not son:
                bak(f"{g[0]} seçenek", sec[0])
            bak(f"{g[0]} hata açıklaması", sec[4])
    return sorunlar


def cevap_listesi_yaz(dosyalar):
    """Öğretmen için cevap anahtarı: VAKALAR.md"""
    from elementler import ADLAR, SEMBOLLER
    adlar = dict(zip(SEMBOLLER, ADLAR))
    temalar = {"saglik": "Sağlık", "teknoloji": "Teknoloji", "enerji": "Enerji", "ev": "Ev ve günlük hayat",
               "sanayi": "Sanayi ve ulaşım", "uzay": "Uzay", "cevre": "Doğa ve çevre", "tarih": "Bilim tarihi",
               "sanat": "Sanat, kültür ve spor", "adli": "Adli bilim ve güvenlik"}
    seviye_adlari = {1: "Gözlem", 2: "Çıkarım", 3: "Kanıt", 4: "Bilimsel Savunma"}
    satirlar = ["# Vaka listesi ve cevap anahtarı", "",
                "Bu dosya öğretmen içindir: her vakanın cevabı olan elementi gösterir. Öğrencilerle paylaşmayın.", "",
                "Dosyalar `icerik/` klasöründeki tablolardan oluşur. Bu liste o tablolar üretilirken otomatik yazıldı.", ""]
    for seviye in (1, 2, 3, 4):
        grup = [d for d in dosyalar if d["seviye"] == seviye]
        satirlar += [f"## Seviye {seviye}: {seviye_adlari[seviye]} ({len(grup)} vaka)", "",
                     "| Vaka | Başlık | Tema | Cevap | Görev |", "|---|---|---|---|---|"]
        for d in grup:
            ek = " (tanıtım)" if d.get("ornek") else " (final)" if d.get("final") else ""
            satirlar.append(f"| {d['id']} | {d['baslik']}{ek} | {temalar[d['tema']]} | {adlar[d['cevap']]} ({d['cevap']}) | {len(d['gorevler'])} |")
        satirlar.append("")
    sayac = collections.Counter(d["cevap"] for d in dosyalar)
    satirlar += ["## Elementlere göre vaka sayısı", "",
                 ", ".join(f"{adlar[s]} {sayac[s]}" for s in sorted(sayac, key=lambda s: E[s]["z"])), ""]
    (HEDEF / "VAKALAR.md").write_text("\n".join(satirlar), encoding="utf-8")


if __name__ == "__main__":
    main()
