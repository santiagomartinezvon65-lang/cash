import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- Configuración de página ---
st.set_page_config(page_title="Currency Converter + Chart", layout="centered")

# --- Monedas con emoji y símbolo ---
currencies = {
    "USD": {"name": "US Dollar", "flag": "🇺🇸", "symbol": "$"},
    "EUR": {"name": "Euro", "flag": "🇪🇺", "symbol": "€"},
    "GBP": {"name": "British Pound", "flag": "🇬🇧", "symbol": "£"},
    "ARS": {"name": "Argentine Peso", "flag": "🇦🇷", "symbol": "$"},
    "JPY": {"name": "Japanese Yen", "flag": "🇯🇵", "symbol": "¥"},
    "BRL": {"name": "Brazilian Real", "flag": "🇧🇷", "symbol": "R$"}
}

# --- Título ---
st.markdown(
    "<h1 style='text-align:center; color:#1F618D;'>Currency Converter</h1>"
    "<p style='text-align:center; color:#566573;'>Real-time currency conversion</p><br>",
    unsafe_allow_html=True
)

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox(
        "From",
        [f"{currencies[c]['flag']} {c} - {currencies[c]['name']}" for c in currencies.keys()],
        index=3
    )
    from_currency_code = from_currency.split()[1]

    amount = st.number_input(
        f"Amount in {from_currency_code}", min_value=0.0, step=10.0, format="%.2f"
    )

with col2:
    to_currency = st.selectbox(
        "To",
        [f"{currencies[c]['flag']} {c} - {currencies[c]['name']}" for c in currencies.keys()],
        index=0
    )
    to_currency_code = to_currency.split()[1]

decimals = st.slider("Decimals", 0, 4, 2)

# --- Obtener tasa actual ---
try:
    url = f"https://api.exchangerate.host/latest?base={from_currency_code}&symbols={to_currency_code}"
    res = requests.get(url).json()
    rate = res["rates"][to_currency_code]
    result = amount * rate

    # --- Caja resultado final ---
    st.markdown(
        f"""
        <div style='background-color:#EAF2F8; padding:25px; border-radius:12px; text-align:center; border:1px solid #D5D8DC; box-shadow:0 2px 5px rgba(0,0,0,0.05); max-width:350px; margin:auto;'>
            <h2 style='margin:0; color:#1F618D; font-weight:500;'>= {currencies[to_currency_code]['symbol']}{result:,.{decimals}f} {to_currency_code}</h2>
        </div>
        <p style='text-align:center; color:#566573; margin-top:8px;'>Converted amount</p>
        """,
        unsafe_allow_html=True
    )

    # --- Tabla de referencia ---
    steps = [1, 5, 10, 25, 50, 100, 500, 1000]
    table_html = "<div style='display:flex; justify-content:center; gap:30px; margin-top:20px; flex-wrap:wrap;'>"

    # From -> To
    left_table = "<div style='background:#D6EAF8; border-radius:12px; padding:15px; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>"
    left_table += f"<h4 style='text-align:center; margin-bottom:10px; color:#1F618D;'>{from_currency_code} → {to_currency_code}</h4>"
    left_table += "<table style='width:100%; border-collapse: collapse;'>"
    for s in steps:
        left_table += f"<tr style='border-bottom:1px solid #AED6F1;'><td style='padding:4px;'>{s} {from_currency_code}</td><td style='padding:4px;'>{(s * rate):,.{decimals}f} {to_currency_code}</td></tr>"
    left_table += "</table></div>"

    # To -> From
    right_table = "<div style='background:#D6EAF8; border-radius:12px; padding:15px; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>"
    right_table += f"<h4 style='text-align:center; margin-bottom:10px; color:#1F618D;'>{to_currency_code} → {from_currency_code}</h4>"
    right_table += "<table style='width:100%; border-collapse: collapse;'>"
    for s in steps:
        right_table += f"<tr style='border-bottom:1px solid #AED6F1;'><td style='padding:4px;'>{s} {to_currency_code}</td><td style='padding:4px;'>{(s / rate):,.{decimals}f} {from_currency_code}</td></tr>"
    right_table += "</table></div>"

    table_html += left_table + right_table + "</div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # --- Gráfico histórico 30 días usando st.line_chart ---
    st.markdown("### Historical rate (last 30 days)")

    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)
    hist_url = f"https://api.exchangerate.host/timeseries?start_date={start_date.date()}&end_date={end_date.date()}&base={from_currency_code}&symbols={to_currency_code}"
    hist_data = requests.get(hist_url).json()

    dates = []
    values = []
    for date, rates_dict in hist_data["rates"].items():
        dates.append(datetime.strptime(date, "%Y-%m-%d"))
        values.append(rates_dict[to_currency_code])

    df = pd.DataFrame({"Date": dates, "Rate": values})
    df.set_index("Date", inplace=True)

    st.line_chart(df["Rate"])

except Exception as e:
    st.error(f"Error: Could not fetch exchange rates. Try again later. ({e})")

