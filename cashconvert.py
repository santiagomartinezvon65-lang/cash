import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Currency Converter", layout="centered")

# Title
st.markdown(
    """
    <h1 style='text-align: center; color: #2E4053;'>Currency Converter</h1>
    <p style='text-align: center; color: #566573; font-size:16px;'>Real-time currency conversion</p>
    <br>
    """,
    unsafe_allow_html=True
)

# Available currencies
currencies = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "ARS": "Argentine Peso",
    "JPY": "Japanese Yen",
    "BRL": "Brazilian Real"
}

# API to get exchange rates
url = "https://open.er-api.com/v6/latest/USD"

try:
    data = requests.get(url).json()
    rates = data["rates"]

    st.markdown("### Enter amount and select currencies")

    col1, col2 = st.columns(2)

    # Input: From
    with col1:
        st.markdown("<h4 style='color:#1C2833;'>From</h4>", unsafe_allow_html=True)
        from_currency = st.selectbox("From currency", list(currencies.keys()), index=3, label_visibility="collapsed")
        amount = st.number_input(
            f"Amount in {from_currency}", min_value=0.0, step=10.0,
            format="%.2f",
            key="from_amount",
            help="Enter the amount to convert"
        )
        # Styled box for amount input (mismo estilo que resultado)
        st.markdown(
            f"""
            <div style='background-color:#F8F9F9; padding:20px; border-radius:12px; text-align:center; border:1px solid #D5D8DC; box-shadow:0 2px 5px rgba(0,0,0,0.05); margin-top:10px;'>
                <h3 style='margin:0; color:#2E4053; font-weight:500;'>{amount:,.2f} {from_currency}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Input: To
    with col2:
        st.markdown("<h4 style='color:#1C2833;'>To</h4>", unsafe_allow_html=True)
        to_currency = st.selectbox("To currency", list(currencies.keys()), index=0, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)  # spacing

        if amount > 0:
            # Convert to USD first, then to target
            usd_amount = amount / rates[from_currency]
            result = usd_amount * rates[to_currency]

            # Styled box for result (igual al de amount)
            st.markdown(
                f"""
                <div style='background-color:#F8F9F9; padding:20px; border-radius:12px; text-align:center; border:1px solid #D5D8DC; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>
                    <h2 style='color:#2E4053; margin:0;'>{result:,.2f} {to_currency}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.caption("Rates provided by open.er-api.com")

except Exception:
    st.error("Error: Could not fetch exchange rates. Try again later.")
