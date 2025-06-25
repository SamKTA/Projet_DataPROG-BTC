import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Suivi Bitcoin", layout="centered")
st.title("📊 Suivi du Bitcoin - 30 derniers jours")

# ⚙️ Appel API CoinGecko
@st.cache_data(ttl=3600)  # cache 1h
def get_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        'vs_currency': 'eur',
        'days': '30',
        'interval': 'daily'
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Erreur API : {e}")
        return None

# 📥 Chargement des données
data = get_bitcoin_data()

if data is None or "prices" not in data:
    st.stop()

# 🔁 Mise en forme
prices = data["prices"]
df = pd.DataFrame(prices, columns=["timestamp", "prix_eur"])
df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
df = df[["date", "prix_eur"]]
df = df.set_index("date").resample("D").mean().interpolate("linear").reset_index()

# 📈 Affichage
st.line_chart(df.set_index("date"))

# 📋 Détail
st.subheader("📌 Données brutes")
st.dataframe(df)
