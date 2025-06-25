import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime

st.title("📊 Suivi du Bitcoin - 30 derniers jours")

if not os.path.exists("data/bitcoin_data.json"):
    st.warning("Lance d'abord le script fetch_data.py pour récupérer les données.")
    st.stop()

with open("data/bitcoin_data.json", "r") as f:
    data = json.load(f)

prices = data.get("prices", [])
df = pd.DataFrame(prices, columns=["timestamp", "prix_eur"])
df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
df = df[["date", "prix_eur"]]

df = df.set_index("date").resample("D").mean().interpolate("linear").reset_index()

st.line_chart(df.set_index("date"))

st.subheader("📌 Détail brut des données")
st.dataframe(df)
