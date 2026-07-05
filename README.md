# Hava Kalitesi ve Solunum Risk Düzeylerinin Bölgesel Analizi

Bu proje, hava kalitesi verilerini kullanarak solunum risk düzeyini tahmin eden bir Python uygulamasıdır. Projede veri analizi, makine öğrenmesi, SQLite veritabanı ve Tkinter tabanlı masaüstü arayüzü birlikte kullanılmıştır.

## Projenin Amacı

Projenin amacı; PM2.5, NO2, SO2, CO, O3, sıcaklık, nem ve rüzgar hızı gibi hava kalitesi verilerinden kişiler için solunum risk seviyesini tahmin etmektir. Risk seviyesi üç kategori olarak gösterilir:

- Düşük risk
- Orta risk
- Yüksek risk

Ayrıca uygulama, girilen şehre göre veri setindeki ortalama bölgesel risk seviyesini de gösterir.

## Kullanılan Teknolojiler

- Python
- Tkinter
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- SQLite
- Joblib

## Dosya Yapısı

```text
.
|-- proje.py
|-- train_model.py
|-- global_air_quality_data_10000.csv
|-- air_quality.db
|-- risk_model.pkl
|-- scaler.pkl
|-- data.pkl
`-- README.md
```

## Dosyaların Görevleri

`proje.py`: Tkinter ile hazırlanan ana masaüstü uygulamasıdır. Kullanıcı değerleri girer, model tahmin yapar ve risk sonucu ekranda gösterilir.

`train_model.py`: Veri setini okuyup makine öğrenmesi modelini eğitir. Eğitim sonunda `risk_model.pkl`, `scaler.pkl` ve `data.pkl` dosyalarını oluşturur.

`global_air_quality_data_10000.csv`: Hava kalitesi veri setidir. Şehir, ülke, tarih, hava kirleticileri ve meteorolojik değerleri içerir.

`air_quality.db`: CSV verilerinden oluşturulan SQLite veritabanıdır. Şehir bazlı ortalama risk hesaplamaları için kullanılır.

`risk_model.pkl`: Eğitilmiş makine öğrenmesi modelidir.

`scaler.pkl`: Model eğitiminde kullanılan ölçeklendiricidir. Girilen değerleri modelin beklediği formata dönüştürür.

`data.pkl`: İşlenmiş veri setinin kaydedilmiş halidir.

## Kurulum

Gerekli Python kütüphanelerini yüklemek için:

```bash
pip install pandas numpy scikit-learn matplotlib joblib
```

## Modeli Eğitme

Model dosyaları yoksa veya modeli yeniden eğitmek isterseniz:

```bash
python train_model.py
```

Bu komut şu dosyaları oluşturur:

- `risk_model.pkl`
- `scaler.pkl`
- `data.pkl`

## Uygulamayı Çalıştırma

```bash
python proje.py
```

Uygulama açıldıktan sonra kullanıcı aşağıdaki değerleri girer:

- PM2.5
- NO2
- SO2
- CO
- O3
- Sıcaklık
- Nem
- Rüzgar
- Şehir

Ardından `Tahmin Et` butonuna basılarak risk seviyesi hesaplanır.

## Arayüz Özellikleri

- Kullanıcı girdilerine göre kişisel risk tahmini yapar.
- Şehir bazlı ortalama risk seviyesini gösterir.
- Son 7 tahmini grafik üzerinde gösterir.
- `Örnek Doldur` butonu ile test verileri otomatik doldurulabilir.
- `Temizle` butonu ile giriş alanları temizlenebilir.

## Risk Sınıflandırması

Model eğitiminde PM2.5 değeri temel alınarak risk sınıfları oluşturulmuştur:

```text
PM2.5 <= 12          -> Düşük risk
12 < PM2.5 <= 35.4  -> Orta risk
PM2.5 > 35.4        -> Yüksek risk
```

Uygulamada ek olarak basit bir kural motoru bulunur. Bu kural motoru, PM2.5 ve nem değerlerine göre tahmin sonucunu gerektiğinde yükseltebilir.

## Notlar

- `__pycache__` ve `.pyc` dosyaları projeye dahil edilmemiştir.
- `air_quality.db` dosyası yoksa uygulama, CSV dosyasından veritabanı oluşturmaya çalışır.
- Model dosyaları yoksa önce `train_model.py` çalıştırılmalıdır.
