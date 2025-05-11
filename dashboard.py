
import streamlit as st
import requests

# === CONFIG ===
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/pairs/ethereum/0x3ebec0a1b4055c8d1180fce64db2a8c068170880"
TOKEN_HOLDINGS = 25775845

# Manually set exchange rates (1 USD = X)
EUR_RATE = 0.889
GBP_RATE = 0.751
QAR_RATE = 3.64

st.set_page_config(page_title="PEPU Price Dashboard", layout="centered")
st.title("📊 Our Retirement Fund")

# === Fetch live token price in USD ===
def fetch_price():
    try:
        res = requests.get(DEXSCREENER_URL).json()
        return float(res['pair']['priceUsd'])
    except:
        return None

price = fetch_price()

if price:
    total_usd = price * TOKEN_HOLDINGS
    total_eur = total_usd * EUR_RATE
    total_gbp = total_usd * GBP_RATE
    total_qar = total_usd * QAR_RATE

    st.metric("PEPU Token Price", f"${price:,.6f}")
    st.metric("Your Holdings", f"{TOKEN_HOLDINGS:,} tokens")
    st.metric("Total Value (USD)", f"${total_usd:,.2f}")
    st.metric("Total Value (EUR)", f"€{total_eur:,.2f}")
    st.metric("Total Value (GBP)", f"£{total_gbp:,.2f}")
    st.metric("Total Value (QAR)", f"﷼{total_qar:,.2f}")
else:
    st.error("❌ Could not fetch live price. Try again later.")
