import streamlit as st
import requests
from datetime import datetime

# Page setup
st.set_page_config(page_title="Currency Converter", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #F8F9F9;
        }
        .main-title {
            text-align: center;
            color: #1F618D;
            margin-bottom: 0;
        }
        .subtitle {
            text-align: center;
            color: #566573;
            font-size: 16px;
            margin-top: 5px;
            margin-bottom: 20px;
        }
        .update-time {
            text-align: center;
            color: #7B7D7D;
            font-size: 12px;
            margin-bottom: 25px;
        }
        .result-box {
            background-color: #EAF2F8;
            padding: 25px;
            border-radius: 14px;
            text-align: center;
            border: 1px solid #D5D8DC;
            box-shadow: 0 3px 8px rgba(0,0,0,0.06);
            max-width: 400px;
            margin: auto;
        }
        .result-value {
            color: #1F618D;
            font-weight: 600;
            margin: 0;
            font-size: 28px;
        }
        .result-label {
            text-align: center;
            color: #566573;
            margin-top: 8px;
            font-size: 14px;
        }
        .ref-tables {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 25px;
            flex-wrap: wrap;
        }
        .ref-card {
            background: #D6EAF8;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            min-width: 220px;
        }
        .ref-card h4 {
            text-align: center;
            margin-bottom: 10px;
            color: #1F618D;
        }
        .ref-card table {
            width: 100%;
            border-collapse: collapse;
        }
        .ref-card td {
            padding: 6px;
            font-size: 13px;
        }
        .ref-card tr {
            border-bottom: 1px solid #AED6F1;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>Currency Converter</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Real-time currency conversion</p>", unsafe_allow_html=True)

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

    st.markdown(f"<p class='update-time'>Last update: {last_update}</p>", unsafe_allow_html=True)

    # Inputs
    st.markdown("### Enter amount and select currencies")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**From**")
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
            key="from_amount"
        )

    with col2:
        st.markdown("**To**")
        to_currency = st.selectbox(
            "To currency",
            [f"{currencies[c]['flag']} {c} - {currencies[c]['name']}" for c in currencies.keys()],
            index=0,
            label_visibility="collapsed"
        )
        to_currency_code = to_currency.split()[1]

    # Decimals control
    decimals = st.slider("Decimals", min_value=0, max_value=4, value=2, step=1)

    st.markdown("<br>", unsafe_allow_html=True)

    # Conversion
    if amount > 0:
        usd_amount = amount / rates[from_currency_code]
        result = usd_amount * rates[to_currency_code]

        st.markdown(
            f"""
            <div class='result-box'>
                <h2 class='result-value'>= {currencies[to_currency_code]['symbol']}{result:,.{decimals}f} {to_currency_code}</h2>
                <p class='result-label'>Converted amount</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Reference tables
        steps = [1, 5, 10, 25, 50, 100, 500, 1000]
        table_html = "<div class='ref-tables'>"

        left_table = "<div class='ref-card'>"
        left_table += f"<h4>{from_currency_code} → {to_currency_code}</h4><table>"
        for s in steps:
            left_table += f"<tr><td>{s} {from_currency_code}</td><td>{(s / rates[from_currency_code] * rates[to_currency_code]):,.{decimals}f} {to_currency_code}</td></tr>"
        left_table += "</table></div>"

        right_table = "<div class='ref-card'>"
        right_table += f"<h4>{to_currency_code} → {from_currency_code}</h4><table>"
        for s in steps:
            right_table += f"<tr><td>{s} {to_currency_code}</td><td>{(s / rates[to_currency_code] * rates[from_currency_code]):,.{decimals}f} {from_currency_code}</td></tr>"
        right_table += "</table></div>"

        table_html += left_table + right_table + "</div>"
        st.markdown(table_html, unsafe_allow_html=True)

    st.caption("Rates provided by open.er-api.com")

except Exception as e:
    st.error(f"Error: Could not fetch exchange rates. Try again later. ({e})")

