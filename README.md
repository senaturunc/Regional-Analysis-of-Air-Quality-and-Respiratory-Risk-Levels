# Hava Kalitesi ve Solunum Risk Duzeylerinin Bolgesel Analizi

Bu proje, hava kalitesi verilerini kullanarak solunum risk duzeyini tahmin eden bir Python uygulamasidir. Projede veri analizi, makine ogrenmesi, SQLite veritabani ve Tkinter tabanli masaustu arayuzu birlikte kullanilmistir.

## Projenin Amaci

Projenin amaci; PM2.5, NO2, SO2, CO, O3, sicaklik, nem ve ruzgar hizi gibi hava kalitesi verilerinden kisiler icin solunum risk seviyesini tahmin etmektir. Risk seviyesi uc kategori olarak gosterilir:

- Dusuk risk
- Orta risk
- Yuksek risk

Ayrica uygulama, girilen sehre gore veri setindeki ortalama bolgesel risk seviyesini de gosterir.

## Kullanilan Teknolojiler

- Python
- Tkinter
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- SQLite
- Joblib

## Dosya Yapisi

```text
.
├── proje.py
├── train_model.py
├── global_air_quality_data_10000.csv
├── air_quality.db
├── risk_model.pkl
├── scaler.pkl
├── data.pkl
└── README.md
```

## Dosyalarin Gorevleri

`proje.py`: Tkinter ile hazirlanan ana masaustu uygulamasidir. Kullanici degerleri girer, model tahmin yapar ve risk sonucu ekranda gosterilir.

`train_model.py`: Veri setini okuyup makine ogrenmesi modelini egitir. Egitim sonunda `risk_model.pkl`, `scaler.pkl` ve `data.pkl` dosyalarini olusturur.

`global_air_quality_data_10000.csv`: Hava kalitesi veri setidir. Sehir, ulke, tarih, hava kirleticileri ve meteorolojik degerleri icerir.

`air_quality.db`: CSV verilerinden olusturulan SQLite veritabanidir. Sehir bazli ortalama risk hesaplamalari icin kullanilir.

`risk_model.pkl`: Egitilmis makine ogrenmesi modelidir.

`scaler.pkl`: Model egitiminde kullanilan olceklendiricidir. Girilen degerleri modelin bekledigi formata donusturur.

`data.pkl`: Islenmis veri setinin kaydedilmis halidir.

## Kurulum

Gerekli Python kutuphanelerini yuklemek icin:

```bash
pip install pandas numpy scikit-learn matplotlib joblib
```

## Modeli Egitme

Model dosyalari yoksa veya modeli yeniden egitmek isterseniz:

```bash
python train_model.py
```

Bu komut su dosyalari olusturur:

- `risk_model.pkl`
- `scaler.pkl`
- `data.pkl`

## Uygulamayi Calistirma

```bash
python proje.py
```

Uygulama acildiktan sonra kullanici asagidaki degerleri girer:

- PM2.5
- NO2
- SO2
- CO
- O3
- Sicaklik
- Nem
- Ruzgar
- Sehir

Ardindan `Tahmin Et` butonuna basilarak risk seviyesi hesaplanir.

## Arayuz Ozellikleri

- Kullanici girdilerine gore kisisel risk tahmini yapar.
- Sehir bazli ortalama risk seviyesini gosterir.
- Son 7 tahmini grafik uzerinde gosterir.
- `Ornek Doldur` butonu ile test verileri otomatik doldurulabilir.
- `Temizle` butonu ile giris alanlari temizlenebilir.

## Risk Siniflandirmasi

Model egitiminde PM2.5 degeri temel alinarak risk siniflari olusturulmustur:

```text
PM2.5 <= 12       -> Dusuk risk
12 < PM2.5 <= 35.4 -> Orta risk
PM2.5 > 35.4      -> Yuksek risk
```

Uygulamada ek olarak basit bir kural motoru bulunur. Bu kural motoru, PM2.5 ve nem degerlerine gore tahmin sonucunu gerektiğinde yukseltebilir.

## Notlar

- `__pycache__` ve `.pyc` dosyalari projeye dahil edilmemistir.
- `air_quality.db` dosyasi yoksa uygulama, CSV dosyasindan veritabani olusturmaya calisir.
- Model dosyalari yoksa once `train_model.py` calistirilmalidir.
