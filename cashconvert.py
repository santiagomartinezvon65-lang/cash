import streamlit as st
import requests

st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")

st.title("💱 Currency Converter")

# Get exchange rate
url = "https://api.bluelytics.com.ar/v2/latest"

try:
    data = requests.get(url).json()
    usd_blue = data["blue"]["value_sell"]

    st.markdown("### Enter amount to convert")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**From (ARS)**")
        pesos = st.number_input("Pesos (ARS)", min_value=0.0, step=100.0, label_visibility="collapsed")

    with col2:
        st.markdown("**To (USD - Blue)**")
        if pesos > 0:
            usd = pesos / usd_blue
            st.success(f"{usd:.2f} USD")

    st.caption(f"💡 Current Blue Dollar rate: 1 USD = {usd_blue} ARS")

except Exception:
    st.error("⚠️ Could not fetch exchange rate. Try again later.")


