import requests
import json
import os

os.makedirs("data", exist_ok=True)

# Appel API historique
r = requests.get(
    'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart',
    params={'vs_currency': 'eur', 'days': '30', 'interval': 'daily'}
)

if r.status_code == 200:
    with open('data/bitcoin_data.json', 'w') as f:
        json.dump(r.json(), f, indent=4)
else:
    print(f"Erreur récupération market data : {r.status_code}")

# Appel API détails
details = requests.get(
    'https://api.coingecko.com/api/v3/coins/bitcoin',
    params={'localization': 'false', 'tickers': 'false', 'market_data': 'true'}
)

if details.status_code == 200:
    with open('data/bitcoin_details.json', 'w') as f:
        json.dump(details.json(), f, indent=4)
else:
    print(f"Erreur récupération détails : {details.status_code}")

print("✅ Données mises à jour.")
