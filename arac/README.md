# Araçlar

Bu klasör oyunun çalışması için gerekli değildir. İçerik tablolarını üreten program ve testler buradadır.

## `vaka-uretici/`: 200 vakanın üreticisi

`icerik/*.csv` tabloları ve öğretmen için cevap anahtarı `VAKALAR.md` bu programla üretildi. Çalıştırmak için Python 3 gerekir:

```bash
cd arac/vaka-uretici
python uret.py
```

- `s1a.py` … `s4b.py`: Yeni 180 vakanın elle yazılan bölümleri: başlık, hikâye, gözlem kartları, gözlem sorusu ve özellik-kullanım sorusu. Dosya adındaki rakam seviyedir.
- `sablon.py`: Her vakaya otomatik eklenen bölümleri kurar. Bunlar yapı kanıtı (periyodik tablo konumu, atom numarası, elektron dizilimi, izotop ya da iyon bilgisi), veri tablosu, laboratuvar ölçümü, arşiv notu ve bunlara dayanan görevlerdir. Ölçüm aralığı, tablodaki öteki adayları dışarıda bırakacak biçimde seçilir.
- `elementler.py`: Türkçe element adları, isim kökenleri ve keşif notları. Sayısal değerler `element_verileri.json` dosyasındadır; Royal Society of Chemistry periyodik tablosundan alınmıştır.
- `kaynaklar.py`: Gerçek olaylara dayanan vakaların RSC dışındaki kaynakları.
- `eski/`: İlk 20 dosyanın (bugün V001–V005, V051–V055, V101–V105, V151–V154 ve V200) üreticileri.

Üretici, elementin adını öğrenci elementi bulmadan önce görünen metinlerde (hikâye, ilk kanıtlar, ilk sorunun açıklaması) arar. Bulursa `SIZINTI` diye uyarır.

**Dikkat:** Tabloları Excel'de elle düzenlediyseniz üreticiyi yeniden çalıştırmayın, çünkü elle yaptığınız değişikliklerin üzerine yazar. Ya hep tabloları düzenleyin ya hep üreticiyi.

## `testler/`

```bash
node arac/testler/v2_mantik_testi.mjs
node arac/testler/v2_gorunurluk_testi.mjs
node arac/testler/denetle.mjs
```

İlki periyodik tabloyu, puanlamayı, içerik denetimini ve kayıtları sınar. İkincisi açılmamış kanıt uyarısını sınar. Üçüncüsü içerik tablolarını oyunun kendi denetimiyle okur ve uyarıları listeler. Testler için Node.js 20 ya da üstü gerekir.

`otomatik-cozucu.js` tarayıcıda çalışır. Her vakayı arayüzden açar, görevleri içerik tablolarındaki doğru cevaplarla çözer ve doğru cevabın kabul edilip edilmediğini denetler.
