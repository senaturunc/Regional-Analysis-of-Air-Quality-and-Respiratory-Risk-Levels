import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# -------------------------
# VERİ YÜKLE
# -------------------------
df = pd.read_csv("global_air_quality_data_10000.csv")

# Kolon isimlerini normalize et
df.columns = (
    df.columns.str.lower()
    .str.replace('.', '', regex=False)
    .str.replace(' ', '_')
)

# Eksik sayısal verileri doldur
df.fillna(df.mean(numeric_only=True), inplace=True)

# City kolonu yoksa rastgele ekle
if 'city' not in df.columns:
    cities = df['country'].unique().tolist()
    df['city'] = np.random.choice(cities, size=len(df))

# -------------------------
# RISK SINIFLANDIRMA (PM2.5’e göre)
# -------------------------
def solunum_riski(pm25):
    if pm25 <= 12:
        return 0  # Düşük
    elif pm25 <= 35.4:
        return 1  # Orta
    else:
        return 2  # Yüksek

df['risk'] = df['pm25'].apply(solunum_riski)

# -------------------------
# ÖZELLİKLER VE HEDEF
# -------------------------
X = df[['pm25','no2','so2','co','o3','temperature','humidity','wind_speed']]
y = df['risk']

# -------------------------
# ÖLÇEKLENDİRME
# -------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------
# EĞİTİM
# -------------------------
X_train, _, y_train, _ = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=2000, C=0.1, class_weight="balanced")
model.fit(X_train, y_train)

# -------------------------
# MODEL VE SCALER KAYDET
# -------------------------
joblib.dump(model, "risk_model.pkl")
joblib.dump(scaler, "scaler.pkl")
df.to_pickle("data.pkl")

print("Model ve veri kaydedildi.")
