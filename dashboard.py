import streamlit as st
import requests

# === CONFIG ===
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/pairs/ethereum/0x3ebec0a1b4055c8d1180fce64db2a8c068170880"
TOKEN_HOLDINGS = 25590860

st.set_page_config(page_title="PEPU Price Dashboard", layout="centered")
st.title("📊 PEPU Live Dashboard")

# === Fetch live price ===
def fetch_price():
    try:
        res = requests.get(DEXSCREENER_URL).json()
        return float(res['pair']['priceUsd'])
    except:
        return None

price = fetch_price()

if price:
    total_value = price * TOKEN_HOLDINGS
    st.metric("PEPU Token Price", f"${price:,.6f}")
    st.metric("Your Holdings", f"{TOKEN_HOLDINGS:,} tokens")
    st.metric("Total Value (USD)", f"${total_value:,.2f}")
else:
    st.error("❌ Could not fetch live price. Try again later.")
