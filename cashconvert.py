import streamlit as st
import requests

st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")

st.title("💱 Currency Converter")

# Available currencies (you can extend this list)
currencies = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "ARS": "Argentine Peso",
    "JPY": "Japanese Yen",
    "BRL": "Brazilian Real"
}

# API to get exchange rates (base = USD)
url = "https://open.er-api.com/v6/latest/USD"

try:
    data = requests.get(url).json()
    rates = data["rates"]

    st.markdown("### Enter amount to convert")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**From**")
        from_currency = st.selectbox("From currency", list(currencies.keys()), index=3, label_visibility="collapsed")
        amount = st.number_input(f"Amount in {from_currency}", min_value=0.0, step=10.0)

    with col2:
        st.markdown("**To**")
        to_currency = st.selectbox("To currency", list(currencies.keys()), index=0, label_visibility="collapsed")

        if amount > 0:
            # Convert to USD first, then to target
            usd_amount = amount / rates[from_currency]
            result = usd_amount * rates[to_currency]
            st.success(f"{result:,.2f} {to_currency}")

    st.caption("💡 Rates provided by open.er-api.com")

except Exception:
    st.error("⚠️ Could not fetch exchange rates. Try again later.")

