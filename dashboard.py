
import streamlit as st
import requests

# === CONFIG ===
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/pairs/ethereum/0x3ebec0a1b4055c8d1180fce64db2a8c068170880"
EXCHANGE_RATE_API = "https://api.exchangerate.host/latest?base=USD&symbols=EUR,GBP"
TOKEN_HOLDINGS = 25775845

st.set_page_config(page_title="PEPU Price Dashboard", layout="centered")
st.title("📊 Our Retirement Fund")

# === Fetch live token price in USD ===
def fetch_price():
    try:
        res = requests.get(DEXSCREENER_URL).json()
        return float(res['pair']['priceUsd'])
    except:
        return None

# === Fetch USD to EUR/GBP exchange rates ===
def fetch_exchange_rates():
    try:
        res = requests.get(EXCHANGE_RATE_API).json()
        return res["rates"]["EUR"], res["rates"]["GBP"]
    except:
        return None, None

price = fetch_price()
eur_rate, gbp_rate = fetch_exchange_rates()

if price:
    total_usd = price * TOKEN_HOLDINGS
    st.metric("PEPU Token Price", f"${price:,.6f}")
    st.metric("Your Holdings", f"{TOKEN_HOLDINGS:,} tokens")
    st.metric("Total Value (USD)", f"${total_usd:,.2f}")

    if eur_rate and gbp_rate:
        total_eur = total_usd * eur_rate
        total_gbp = total_usd * gbp_rate
        st.metric("Total Value (EUR)", f"€{total_eur:,.2f}")
        st.metric("Total Value (GBP)", f"£{total_gbp:,.2f}")
    else:
        st.warning("⚠️ Couldn't fetch exchange rates for EUR/GBP.")
else:
    st.error("❌ Could not fetch live price. Try again later.")
