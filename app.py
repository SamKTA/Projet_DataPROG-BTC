import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Suivi Bitcoin", layout="centered")
st.title("📊 Suivi du Bitcoin")

periode = st.selectbox(
    "Sélectionne la période à analyser :",
    ["24h", "7 jours", "15 jours", "30 jours"]
)

jours = {
    "24h": 1,
    "7 jours": 7,
    "15 jours": 15,
    "30 jours": 30
}[periode]

@st.cache_data(ttl=86400)  # cache les données 24h (86400 secondes)
def get_bitcoin_data(days):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        'vs_currency': 'eur',
        'days': str(days),
        'interval': 'daily' if days > 1 else 'hourly'
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        if r.status_code == 429:
            st.error("⏳ Trop de requêtes. Réessaye dans quelques minutes. Les données sont limitées par CoinGecko.")
        else:
            st.error(f"Erreur API : {e}")
        return None

data = get_bitcoin_data(jours)

if data and "prices" in data:
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "prix_eur"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["date", "prix_eur"]]

    df = df.set_index("date").resample("D" if jours > 1 else "H").mean().interpolate("linear").reset_index()

    prix_debut = df["prix_eur"].iloc[0]
    prix_fin = df["prix_eur"].iloc[-1]
    variation = ((prix_fin - prix_debut) / prix_debut) * 100

    st.metric(
        label=f"Variation sur {periode}",
        value=f"{variation:.2f}%",
        delta=f"{prix_fin - prix_debut:.2f} €"
    )

    st.line_chart(df.set_index("date"))

    with st.expander("📌 Voir les données brutes"):
        st.dataframe(df)

else:
    st.warning("Impossible de récupérer les données.")
