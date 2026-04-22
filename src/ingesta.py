# ingest.py
import requests 
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {"vs_currency": "usd"}

data = requests.get(url, params=params).json()
df = pd.DataFrame(data)
df.to_csv("data/raw_crypto.csv", index=False)

print(df.head())