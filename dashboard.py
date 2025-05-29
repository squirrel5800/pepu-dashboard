import streamlit as st
import requests

# === CONFIG ===
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/pairs/ethereum/0xb1b10b05aa043dd8d471d4da999782bc694993e3ecbe8e7319892b261b412ed5"

TOKEN_HOLDINGS = 30500000

EUR_RATE = 0.889
GBP_RATE = 0.751
QAR_RATE = 3.64

st.set_page_config(page_title="PEPU Price Dashboard", layout="centered")
st.title("📊 Our Retirement Fund")

# === Fetch token data safely ===
def fetch_token_data():
    try:
        res = requests.get(DEXSCREENER_URL).json()
        if 'pair' not in res:
            st.error("❌ 'pair' not found in Dexscreener response.")
            return None

        pair = res['pair']
        price = float(pair.get('priceUsd', 0))
        price_change = float(pair.get('priceChange', {}).get('h24', 0))
        high_price = float(pair.get('priceUsd', 0)) * (1 + price_change / 100)
        low_price = float(pair.get('priceUsd', 0)) * (1 - abs(price_change) / 100)

        return {
            "price": price,
            "priceChangePct": price_change,
            "high24h": high_price,
            "low24h": low_price
        }
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return None

data = fetch_token_data()

if data and data["price"] > 0:
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

    st.metric("PEPU Token Price", f"${price:,.6f}", f"{pct_change:.2f}% / 24h")
    st.metric("Your Holdings", f"{TOKEN_HOLDINGS:,} tokens")

    col1, col2 = st.columns(2)
    col1.metric("Total Value (USD)", f"${total_usd:,.2f}")
    col2.metric("Total Value (EUR)", f"€{total_eur:,.2f}")

    col3, col4 = st.columns(2)
    col3.metric("Total Value (GBP)", f"£{total_gbp:,.2f}")
    col4.metric("Total Value (QAR)", f"﷼{total_qar:,.2f}")

    st.markdown("---")
    st.subheader("📈 24h Performance Summary")

    col5, col6, col7 = st.columns(3)
    col5.metric("💸 Change (24h)", f"{pct_change:.2f}%", delta_color="normal")
    col6.metric("🔺 24h High Value", f"${total_usd_high:,.2f}")
    col7.metric("🔻 24h Low Value", f"${total_usd_low:,.2f}")
else:
    st.error("❌ Could not fetch or parse live data.")
