import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime
import subprocess

# 📁 Vérifie si les données existent
if not os.path.exists("data/bitcoin_data.json"):
    st.warning("Les données n'existent pas. On les télécharge...")
    # Lance fetch_data.py automatiquement
    subprocess.run(["python", "fetch_data.py"])

# 🔁 Re-vérifie après tentative de création
if not os.path.exists("data/bitcoin_data.json"):
    st.error("Échec de récupération des données. Vérifie fetch_data.py.")
    st.stop()

# 💾 Chargement des données
with open("data/bitcoin_data.json", "r") as f:
    data = json.load(f)

prices = data.get("prices", [])
df = pd.DataFrame(prices, columns=["timestamp", "prix_eur"])
df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
df = df[["date", "prix_eur"]]

# Complétion des jours manquants
df = df.set_index("date").resample("D").mean().interpolate("linear").reset_index()

st.title("📊 Suivi du Bitcoin - 30 derniers jours")
st.line_chart(df.set_index("date"))
st.subheader("📌 Détail brut des données")
st.dataframe(df)
