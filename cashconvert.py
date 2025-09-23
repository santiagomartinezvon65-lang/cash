import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Currency Converter", layout="centered")

# Custom CSS for look & feel
st.markdown(
    """
    <style>
    .stApp {
        background-color: #EAF2F8;
        font-family: 'Roboto', sans-serif;
    }
    .currency-selectbox .stSelectbox>div>div {
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stSlider>div>div>div>div>div {
        color: #117A65;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Title
# -----------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #1F618D;'> Currency Converter</h1>
    <p style='text-align: center; color: #566573; font-size:16px;'>Real-time currency conversion</p>
    <br>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Currencies
# -----------------------------
currencies = {
    "USD": {"name": "US Dollar", "flag": "🇺🇸", "symbol": "$"},
    "EUR": {"name": "Euro", "flag": "🇪🇺", "symbol": "€"},
    "GBP": {"name": "British Pound", "flag": "🇬🇧", "symbol": "£"},
    "ARS": {"name": "Argentine Peso", "flag": "🇦🇷", "symbol": "$"},
    "JPY": {"name": "Japanese Yen", "flag": "🇯🇵", "symbol": "¥"},
    "BRL": {"name": "Brazilian Real", "flag": "🇧🇷", "symbol": "R$"}
}

# -----------------------------
# API fetch
# -----------------------------
url = "https://open.er-api.com/v6/latest/USD"

try:
    data = requests.get(url).json()
    rates = data["rates"]
    last_update = datetime.fromtimestamp(
        data["time_last_update_unix"]).strftime('%Y-%m-%d %H:%M:%S')

    st.markdown(
        f"<p style='text-align:center; color:#566573; font-size:12px;'>Last update: {last_update}</p>",
        unsafe_allow_html=True
    )

    # -----------------------------
    # Inputs
    # -----------------------------
    col1, col2, col3 = st.columns([1,0.3,1])  # middle for swap button

    with col1:
        st.markdown("<h4 style='color:#1F618D;'>From</h4>", unsafe_allow_html=True)
        from_currency = st.selectbox(
            "From currency",
            [f"{currencies[c]['flag']} {c} - {currencies[c]['name']}" for c in currencies.keys()],
            index=3,
            label_visibility="collapsed",
            key="from_currency"
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

    with col3:
        st.markdown("<h4 style='color:#1F618D;'>To</h4>", unsafe_allow_html=True)
        to_currency = st.selectbox(
            "To currency",
            [f"{currencies[c]['flag']} {c} - {currencies[c]['name']}" for c in currencies.keys()],
            index=0,
            label_visibility="collapsed",
            key="to_currency"
        )
        to_currency_code = to_currency.split()[1]

    with col2:
        if st.button("↔ Swap"):
            from_currency_code, to_currency_code = to_currency_code, from_currency_code
            amount = amount  # keep same amount

    decimals = st.slider("Decimals", min_value=0, max_value=4, value=2, step=1)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Conversion
    # -----------------------------
    if amount > 0:
        usd_amount = amount / rates[from_currency_code]
        result = usd_amount * rates[to_currency_code]

        # Percent change indicator
        last_rate = rates[to_currency_code] / rates[from_currency_code]
        percent_change = ((last_rate - last_rate) / last_rate) * 100  # placeholder 0%

        # Result box
        st.markdown(
            f"""
            <div style='background-color:#FFFFFF; padding:25px; border-radius:12px; 
                        text-align:center; border:1px solid #D5D8DC; 
                        box-shadow:0 2px 5px rgba(0,0,0,0.05); 
                        max-width:350px; margin:auto;'>
                <h2 style='margin:0; color:#117A65; font-weight:700;'>
                    = {currencies[to_currency_code]['symbol']}{result:,.{decimals}f} {to_currency_code}
                </h2>
                <p style='color:#566573; font-size:12px; margin:5px 0;'>Converted amount</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------
        # Reference Table
        # -----------------------------
        steps = [1, 5, 10, 25, 50, 100, 500, 1000]
        table_html = "<div style='display:flex; justify-content:center; gap:30px; margin-top:20px; flex-wrap:wrap;'>"

        def build_table(base, target):
            html = f"<div style='background:#FFFFFF; border-radius:12px; padding:15px; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>"
            html += f"<h4 style='text-align:center; margin-bottom:10px; color:#1F618D;'>{base} → {target}</h4>"
            html += "<table style='width:100%; border-collapse: collapse;'>"
            for i, s in enumerate(steps):
                color = "#F2F4F4" if i % 2 else "#FFFFFF"
                val = s / rates[base] * rates[target] if base == from_currency_code else s / rates[base] * rates[target]
                html += f"<tr style='background:{color};'><td style='padding:4px; color:#117A65; font-weight:600;'>{s} {base}</td>"
                html += f"<td style='padding:4px; color:#117A65; font-weight:600;'>{val:,.{decimals}f} {target}</td></tr>"
            html += "</table></div>"
            return html

        table_html += build_table(from_currency_code, to_currency_code)
        table_html += build_table(to_currency_code, from_currency_code)
        table_html += "</div>"

        st.markdown(table_html, unsafe_allow_html=True)

        # -----------------------------
        # Conversion history
        # -----------------------------
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append(f"{amount} {from_currency_code} → {result:,.{decimals}f} {to_currency_code}")
        history_html = "<ul>"
        for h in st.session_state.history[-5:]:
            history_html += f"<li style='margin-bottom:4px;'>{h}</li>"
        history_html += "</ul>"
        st.markdown("<h4 style='color:#1F618D;'>Recent conversions:</h4>" + history_html, unsafe_allow_html=True)

    st.caption("Rates provided by open.er-api.com")

except Exception as e:
    st.error(f"Error: Could not fetch exchange rates. Try again later. ({e})")


