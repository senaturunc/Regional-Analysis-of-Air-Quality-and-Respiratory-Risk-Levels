import tkinter as tk
from tkinter import messagebox
import joblib
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import os
import pandas as pd
import numpy as np

CSV_FILE = "global_air_quality_data_10000.csv"
DB_FILE = "air_quality.db"
MODEL_FILE = "risk_model.pkl"
SCALER_FILE = "scaler.pkl"

# -------------------------
# MODEL + SCALER YÜKLE
# -------------------------
try:
    model = joblib.load(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)
except Exception as e:
    messagebox.showerror(
        "Hata",
        "Model veya scaler bulunamadı.\n\n"
        "Önce train_model.py dosyasını çalıştırın.\n"
        f"Detay: {e}"
    )
    exit()

# -------------------------
# VERİYİ SQLITE'A AKTAR (Sadece bir kez çalıştır) 
# -------------------------
def csv_to_sqlite():
    try:
        df = pd.read_csv(CSV_FILE)
        df.columns = df.columns.str.lower().str.replace('.', '', regex=False).str.replace(' ', '_')
        if 'city' not in df.columns:
            cities = ['İstanbul','Ankara','İzmir','Bursa','Adana']
            df['city'] = np.random.choice(cities, size=len(df))
        df['risk'] = df['pm10'].apply(lambda x: 0 if x<=20 else (1 if x<=50 else 2))
        conn = sqlite3.connect(DB_FILE)
        df.to_sql("air_quality", conn, if_exists="replace", index=False)
        conn.close()
        print("Veri başarıyla SQLite'a aktarıldı.")
    except Exception as e:
        print("Veri aktarma hatası:", e)

if not os.path.exists(DB_FILE):
    csv_to_sqlite()

# -------------------------
# ŞEHİR ORTALAMA RİSKİ
# -------------------------
def get_city_avg_risk():
    conn = sqlite3.connect(DB_FILE)
    df_city = pd.read_sql_query("SELECT city, AVG(risk) as avg_risk FROM air_quality GROUP BY city", conn)
    conn.close()
    df_city['city_key'] = df_city['city'].str.strip().str.lower()
    return dict(zip(df_city['city_key'], df_city['avg_risk']))

city_avg_risk = get_city_avg_risk()

# -------------------------
# KURAL MOTORU
# -------------------------
def final_risk_python(risk, pm25, nem):
    if risk == 1 and pm25 > 75:
        return 2
    elif risk == 0 and nem > 80:
        return 1
    else:
        return risk

# -------------------------
# GLOBAL
# -------------------------
son_7_risk = []

ornek_degerler = ["50", "40", "10", "2", "80", "22", "60", "5"]

# -------------------------
# GUI
# -------------------------
root = tk.Tk()
root.title("Hava Kalitesi Risk Tahmin Sistemi (SQLite Entegre)")
root.geometry("600x750")
root.resizable(False, False)

tk.Label(root, text="🌍 Hava Kalitesi Risk Tahmin Sistemi",
         font=("Arial", 16, "bold")).pack(pady=10)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

labels = ["PM2.5", "NO2", "SO2", "CO", "O3", "Sıcaklık", "Nem", "Rüzgar"]
entries = []

for i, label in enumerate(labels):
    tk.Label(frame_inputs, text=label).grid(row=i, column=0, sticky="w", pady=3)
    e = tk.Entry(frame_inputs, width=20)
    e.grid(row=i, column=1, pady=3)
    entries.append(e)

tk.Label(frame_inputs, text="Şehir").grid(row=len(labels), column=0, sticky="w", pady=5)
entry_city = tk.Entry(frame_inputs, width=20)
entry_city.grid(row=len(labels), column=1, pady=5)

frame_button = tk.Frame(root)
frame_button.pack(pady=(5, 8))

lbl_personal = tk.Label(root, text="Kişisel Risk Seviyesi", font=("Arial", 12, "bold"))
lbl_personal.pack(pady=5)

lbl_city = tk.Label(root, text="Şehir Ortalama Riski", font=("Arial", 11))
lbl_city.pack(pady=5)

frame_graph = tk.Frame(root)
frame_graph.pack(pady=10)

fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack()

# -------------------------
# Tahmin fonksiyonu
# -------------------------
def tahmin_et():
    global son_7_risk, fig, ax

    try:
        values = [float(e.get()) for e in entries]
    except:
        messagebox.showerror("Hata", "Lütfen tüm değerleri sayısal giriniz")
        return

    city = entry_city.get().strip()
    if city == "":
        messagebox.showerror("Hata", "Lütfen şehir adı giriniz")
        return
    city_key = city.lower()

    # ML tahmini
    X_scaled = scaler.transform([values])
    risk = int(model.predict(X_scaled)[0])

    # Kural motoru
    pm25 = values[0]
    nem = values[6]
    risk = final_risk_python(risk, pm25, nem)

    # Renk ve etiket
    risk_map = {0: "DÜŞÜK", 1: "ORTA", 2: "YÜKSEK"}
    color_map = {0: "green", 1: "orange", 2: "red"}

    lbl_personal.config(text=f"Kişisel Risk Seviyesi: {risk_map[risk]}", fg=color_map[risk])

    # Şehir ortalaması (SQLite)
    if city_key in city_avg_risk:
        city_risk_val = city_avg_risk[city_key]
        if city_risk_val < 0.5:
            city_risk = 0
        elif city_risk_val < 1.5:
            city_risk = 1
        else:
            city_risk = 2
    else:
        city_risk = 0

    lbl_city.config(text=f"{city} için Ortalama Risk: {risk_map[city_risk]}", fg=color_map[city_risk])

    # Son 7 tahmin
    son_7_risk.append(risk)
    if len(son_7_risk) > 7:
        son_7_risk.pop(0)

    # Grafik güncelle
    ax.clear()
    ax.plot(range(1, len(son_7_risk)+1), son_7_risk, marker="o", color="blue")
    ax.set_title("Son 7 Tahmin Risk Grafiği")
    ax.set_xlabel("Tahmin Sırası")
    ax.set_ylabel("Risk Seviyesi")
    ax.set_ylim(-0.1,2.1)
    ax.set_yticks([0,1,2])
    ax.set_yticklabels(["Düşük","Orta","Yüksek"])
    ax.grid(True)
    canvas.draw()

def ornek_doldur():
    for entry, value in zip(entries, ornek_degerler):
        entry.delete(0, tk.END)
        entry.insert(0, value)
    entry_city.delete(0, tk.END)
    entry_city.insert(0, "Istanbul")

def temizle():
    for entry in entries:
        entry.delete(0, tk.END)
    entry_city.delete(0, tk.END)
    lbl_personal.config(text="Kişisel Risk Seviyesi", fg="black")
    lbl_city.config(text="Şehir Ortalama Riski", fg="black")

# -------------------------
# Buton
# -------------------------
tk.Button(frame_button, text="Örnek Doldur", command=ornek_doldur,
          bg="#607D8B", fg="white", font=("Arial", 10, "bold"),
          padx=12, pady=5).grid(row=0, column=0, padx=5)

tk.Button(frame_button, text="Tahmin Et", command=tahmin_et,
          bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
          padx=15, pady=5).grid(row=0, column=1, padx=5)

tk.Button(frame_button, text="Temizle", command=temizle,
          bg="#795548", fg="white", font=("Arial", 10, "bold"),
          padx=12, pady=5).grid(row=0, column=2, padx=5)

root.mainloop()
