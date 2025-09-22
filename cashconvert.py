import streamlit as st
import requests
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Currency Converter", layout="centered")

# Título
st.markdown("<h1 style='text-align: center;'>Currency Converter</h1>", unsafe_allow_html=True)

# Monedas disponibles
currencies = ["USD", "ARS", "EUR", "BRL"]

# Columnas para elegir monedas
col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox("From", currencies)
    from_amount = st.number_input("Amount", min_value=0.0, value=1.0, step=1.0)

with col2:
    to_currency = st.selectbox("To", currencies)

# Función segura para obtener la tasa de cambio
def get_rate(from_curr, to_curr):
    url = f"https://api.exchangerate.host/latest?base={from_curr}&symbols={to_curr}"
    try:
        res = requests.get(url)
        res.raise_for_status()  # Lanza error si la respuesta no es 200
        data = res.json()
        if "rates" in data and to_curr in data["rates"]:
            return data["rates"][to_curr]
        else:
            st.error("No se pudo obtener la tasa de cambio.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectarse a la API: {e}")
        return None

# Obtener la tasa
rate = get_rate(from_currency, to_currency)

if rate is not None:
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

else:
    st.warning("No se puede mostrar la conversión.")

