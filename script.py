import requests
import pandas as pd
import sqlite3

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

query_parameters = {
    "vs_currency": "usd",
    "days": "365"
}

print("Fetching data from CoinGecko...")

response = requests.get(url, params=query_parameters)

if response.status_code == 200:
    data = response.json()
    print("Successfully fetched data!")

    df = pd.DataFrame(data["prices"], columns=["raw_datetime", "price"])

    df["date"] = pd.to_datetime(df["raw_datetime"], unit="ms")
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    df["price"] = df["price"].round(2)
    
    clean_table = df[["date", "price"]]

    print("\nPreview of the clean structured table:")
    print(clean_table.head())

    print("Saving to the database...")
    conn = sqlite3.connect("crypto_analysis.db")
    clean_table.to_sql("bitcoin_prices", conn, if_exists="replace", index=False)
    conn.close()

    print("Load successful! Database 'crypto_analysis.db' is ready.")
else:
    print(f"Failed to fetch data. Status Code: {response.status_code}")
