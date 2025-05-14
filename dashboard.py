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

# === Fetch token data ===
def fetch_token_data():
    try:
        res = requests.get(DEXSCREENER_URL).json()
        pair = res['pair']
        return {
            "price": float(pair['priceUsd']),
            "priceChangePct": float(pair['priceChange']['h24']),
            "high24h": float(pair['priceNative']['h24High']),
            "low24h": float(pair['priceNative']['h24Low'])
        }
    except:
        return None

data = fetch_token_data()

if data:
    price = data["price"]
    pct_change = data["priceChangePct"]
    high_price = data["high24h"]
    low_price = data["low24h"]

    total_usd = price * TOKEN_HOLDINGS
    total_eur = total_usd * EUR_RATE
    total_gbp = total_usd * GBP_RATE
    total_qar = total_usd * QAR_RATE

    total_usd_high = high_price * TOKEN_HOLDINGS
    total_usd_low = low_price * TOKEN_HOLDINGS

    # === Display core metrics ===
    st.metric("PEPU Token Price", f"${price:,.6f}", f"{pct_change:.2f}% / 24h")
    st.metric("Your Holdings", f"{TOKEN_HOLDINGS:,} tokens")

    # === Value rows ===
    col1, col2 = st.columns(2)
    col1.metric("Total Value (USD)", f"${total_usd:,.2f}")
    col2.metric("Total Value (EUR)", f"€{total_eur:,.2f}")

    col3, col4 = st.columns(2)
    col3.metric("Total Value (GBP)", f"£{total_gbp:,.2f}")
    col4.metric("Total Value (QAR)", f"﷼{total_qar:,.2f}")

    # === 24h Change Box ===
    st.markdown("---")
    st.subheader("📈 24h Performance Summary")

    col5, col6, col7 = st.columns(3)
    col5.metric("💸 Change (24h)", f"{pct_change:.2f}%", delta_color="normal")
    col6.metric("🔺 24h High Value", f"${total_usd_high:,.2f}")
    col7.metric("🔻 24h Low Value", f"${total_usd_low:,.2f}")
else:
    st.error("❌ Could not fetch live data. Try again later.")
