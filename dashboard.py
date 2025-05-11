
import streamlit as st
import requests

# === CONFIG ===
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/pairs/ethereum/0x3ebec0a1b4055c8d1180fce64db2a8c068170880"
TOKEN_HOLDINGS = 25795775

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

    # Display token info
    st.metric("PEPU Token Price", f"${price:,.6f}")
    st.metric("Your Holdings", f"{TOKEN_HOLDINGS:,} tokens")

    # First row
    col1, col2 = st.columns(2)
    col1.metric("Total Value (USD)", f"${total_usd:,.2f}")
    col2.metric("Total Value (EUR)", f"€{total_eur:,.2f}")

    # Second row
    col3, col4 = st.columns(2)
    col3.metric("Total Value (GBP)", f"£{total_gbp:,.2f}")
    col4.metric("Total Value (QAR)", f"﷼{total_qar:,.2f}")
else:
    st.error("❌ Could not fetch live price. Try again later.")
