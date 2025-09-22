import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="Currency Converter", layout="centered")

st.markdown("<h1 style='text-align: center;'>Currency Converter</h1>", unsafe_allow_html=True)

# Monedas disponibles
currencies = ["USD", "ARS", "EUR", "BRL"]

col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox("From", currencies)
    from_amount = st.number_input("Amount", min_value=0.0, value=1.0, step=1.0)

with col2:
    to_currency = st.selectbox("To", currencies)

# Llamada a la API para obtener la tasa
def get_rate(from_curr, to_curr):
    url = f"https://api.exchangerate.host/latest?base={from_curr}&symbols={to_curr}"
    res = requests.get(url)
    data = res.json()
    return data["rates"][to_curr]

rate = get_rate(from_currency, to_currency)
converted_amount = round(from_amount * rate, 2)

st.markdown(f"<h2 style='text-align: center;'>{from_amount} {from_currency} = {converted_amount} {to_currency}</h2>", unsafe_allow_html=True)

# Tabla de referencia
steps = [1, 5, 10, 25, 50, 100, 500, 1000, 5000, 10000]
table_html = "<div style='display:flex;justify-content:center;gap:30px;margin-top:20px;'>"

# From -> To
table_html += "<table border='1' style='border-collapse:collapse;padding:5px;'>"
table_html += f"<tr><th colspan='2'>{from_currency} → {to_currency}</th></tr>"
for s in steps:
    table_html += f"<tr><td style='padding:5px;'>{s}</td><td style='padding:5px;'>{round(s*rate,2)}</td></tr>"
table_html += "</table>"

# To -> From
table_html += "<table border='1' style='border-collapse:collapse;padding:5px;'>"
table_html += f"<tr><th colspan='2'>{to_currency} → {from_currency}</th></tr>"
for s in steps:
    table_html += f"<tr><td style='padding:5px;'>{s}</td><td style='padding:5px;'>{round(s/rate,2)}</td></tr>"
table_html += "</table>"

table_html += "</div>"

components.html(table_html, height=400)

