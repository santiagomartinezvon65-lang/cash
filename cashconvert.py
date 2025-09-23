import streamlit as st
import requests
from datetime import datetime

# Page setup
st.set_page_config(page_title="Currency Converter", layout="centered")

# Title
st.markdown(
    """
    <h1 style='text-align: center; color: #1F618D;'>Currency Converter</h1>
    <p style='text-align: center; color: #566573; font-size:16px;'>Real-time currency conversion</p>
    <br>
    """,
    unsafe_allow_html=True
)

# Currencies
currencies = {
    "USD": {"name": "US Dollar", "flag": "🇺🇸", "symbol": "$"},
    "EUR": {"name": "Euro", "flag": "🇪🇺", "symbol": "€"},
    "GBP": {"name": "British Pound", "flag": "🇬🇧", "symbol": "£"},
    "ARS": {"name": "Argentine Peso", "flag": "🇦🇷", "symbol": "$"},
    "JPY": {"name": "Japanese Yen", "flag": "🇯🇵", "symbol": "¥"},
    "BRL": {"name": "Brazilian Real", "flag": "🇧🇷", "symbol": "R$"}
}

# API
url = "https://open.er-api.com/v6/latest/USD"

try:
    data = requests.get(url).json()
    rates = data["rates"]
    last_update = datetime.fromtimestamp(data["time_last_update_unix"]).strftime('%Y-%m-%d %H:%M:%S')

    st.markdown(f"<p style='text-align:center; color:#566573; font-size:12px;'>Last update: {last_update}</p>", unsafe_allow_html=True)

    st.markdown("### Enter amount and select currencies")

    # Input columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h4 style='color:#1F618D;'>From</h4>", unsafe_allow_html=True)
        from_currency = st.selectbox(
            "From currency",
            [f"{currencies[c]['flag']} {c} - {currencies[c]['name']}" for c in currencies.keys()],
            index=3,
            label_visibility="collapsed"
        )
        from_currency_code = from_currency.split()[1]
        amount = st.number_input(
            f"Amount in {from_currency_code}",
            min_value=0.0,
            step=10.0,
            format="%.2f",
            key="from_amount",
            help="Enter the amount to convert"
        )

    with col2:
        st.markdown("<h4 style='color:#1F618D;'>To</h4>", unsafe_allow_html=True)
        to_currency = st.selectbox(
            "To currency",
            [f"{currencies[c]['flag']} {c} - {currencies[c]['name']}" for c in currencies.keys()],
            index=0,
            label_visibility="collapsed"
        )
        to_currency_code = to_currency.split()[1]

    # Decimals control
    decimals = st.slider("Decimals", min_value=0, max_value=4, value=2, step=1)

    st.markdown("<br>", unsafe_allow_html=True)  # spacing

    if amount > 0:
        usd_amount = amount / rates[from_currency_code]
        result = usd_amount * rates[to_currency_code]

        # Resultado final con color verde fuerte
        st.markdown(
            f"""
            <div style='background-color:#EAF2F8; padding:25px; border-radius:12px; text-align:center; 
                        border:1px solid #D5D8DC; box-shadow:0 2px 5px rgba(0,0,0,0.05); max-width:350px; margin:auto;'>
                <h2 style='margin:0; color:#117A65; font-weight:600;'>= {currencies[to_currency_code]['symbol']}{result:,.{decimals}f} {to_currency_code}</h2>
            </div>
            <p style='text-align:center; color:#566573; margin-top:8px;'>Converted amount</p>
            """,
            unsafe_allow_html=True
        )

        # Tabla de referencia
        steps = [1, 5, 10, 25, 50, 100, 500, 1000]
        table_html = "<div style='display:flex; justify-content:center; gap:30px; margin-top:20px; flex-wrap:wrap;'>"

        # From -> To
        left_table = "<div style='background:#D6EAF8; border-radius:12px; padding:15px; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>"
        left_table += f"<h4 style='text-align:center; margin-bottom:10px; color:#1F618D;'>{from_currency_code} → {to_currency_code}</h4>"
        left_table += "<table style='width:100%; border-collapse: collapse;'>"
        for s in steps:
            left_table += f"<tr style='border-bottom:1px solid #AED6F1;'><td style='padding:4px; color:#000;'>{s} {from_currency_code}</td><td style='padding:4px; color:#000;'>{(s / rates[from_currency_code] * rates[to_currency_code]):,.{decimals}f} {to_currency_code}</td></tr>"
        left_table += "</table></div>"

        # To -> From
        right_table = "<div style='background:#D6EAF8; border-radius:12px; padding:15px; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>"
        right_table += f"<h4 style='text-align:center; margin-bottom:10px; color:#1F618D;'>{to_currency_code} → {from_currency_code}</h4>"
        right_table += "<table style='width:100%; border-collapse: collapse;'>"
        for s in steps:
            right_table += f"<tr style='border-bottom:1px solid #AED6F1;'><td style='padding:4px; color:#000;'>{s} {to_currency_code}</td><td style='padding:4px; color:#000;'>{(s / rates[to_currency_code] * rates[from_currency_code]):,.{decimals}f} {from_currency_code}</td></tr>"
        right_table += "</table></div>"

        table_html += left_table + right_table + "</div>"
        st.markdown(table_html, unsafe_allow_html=True)

    st.caption("Rates provided by open.er-api.com")

except Exception as e:
    st.error(f"Error: Could not fetch exchange rates. Try again later. ({e})")

