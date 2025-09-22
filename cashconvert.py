import streamlit as st
import requests
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Currency Converter", layout="centered")

# Título
st.markdown("<h1 style='text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem;'>Currency Converter</h1>", unsafe_allow_html=True)

# Monedas disponibles
currencies = ["USD", "ARS", "EUR", "BRL"]

# Columnas para elegir monedas
col1, col2 = st.columns([1,1])

with col1:
    from_currency = st.selectbox("From", currencies)
    from_amount = st.number_input("Amount", min_value=0.0, value=1.0, step=1.0, format="%.2f")

with col2:
    to_currency = st.selectbox("To", currencies)

# Fallback de tasas en caso de error de API
fallback_rates = {
    "USD": {"ARS": 380.0, "EUR": 0.92, "BRL": 5.1, "USD": 1.0},
    "ARS": {"USD": 0.0026, "EUR": 0.0024, "BRL": 0.013, "ARS": 1.0},
    "EUR": {"USD": 1.09, "ARS": 414.0, "BRL": 5.55, "EUR": 1.0},
    "BRL": {"USD": 0.20, "ARS": 75.0, "EUR": 0.18, "BRL": 1.0},
}

# Función para obtener tasa de cambio
def get_rate(from_curr, to_curr):
    url = f"https://api.exchangerate.host/latest?base={from_curr}&symbols={to_curr}"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()
        if "rates" in data and to_curr in data["rates"]:
            return data["rates"][to_curr]
        else:
            st.warning("API no devolvió la tasa correcta, usando valores de respaldo.")
            return fallback_rates[from_curr][to_curr]
    except requests.exceptions.RequestException:
        st.warning("No se pudo conectar a la API, usando valores de respaldo.")
        return fallback_rates[from_curr][to_curr]

rate = get_rate(from_currency, to_currency)
converted_amount = round(from_amount * rate, 2)

# Resultado principal
st.markdown(f"""
<div style='
    background-color: #f0f4f8; 
    padding: 1rem 2rem; 
    border-radius: 1rem; 
    text-align: center; 
    font-size: 1.8rem; 
    font-weight: 600;
    margin-top: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
'>
    {from_amount} {from_currency} = {converted_amount} {to_currency}
</div>
""", unsafe_allow_html=True)

# Tabla de referencia
steps = [1, 5, 10, 25, 50, 100, 500, 1000, 5000, 10000]
table_html = "<div style='display:flex; justify-content:center; gap:30px; margin-top:2rem; flex-wrap:wrap;'>"

# From -> To
table_html += "<div style='background:white; border-radius:1rem; padding:1rem; box-shadow:0 4px 8px rgba(0,0,0,0.1);'>"
table_html += f"<h3 style='text-align:center; font-weight:bold; margin-bottom:0.5rem;'>{from_currency} → {to_currency}</h3>"
table_html += "<table style='width:100%; text-align:center; border-collapse: collapse;'>"
for s in steps:
    table_html += f"<tr style='border-bottom:1px solid #ddd;'><td style='padding:0.5rem;'>{s}</td><td style='padding:0.5rem;'>{round(s*rate,2)}</td></tr>"
table_html += "</table></div>"

# To -> From
table_html += "<div style='background:white; border-radius:1rem; padding:1rem; box-shadow:0 4px 8px rgba(0,0,0,0.1);'>"
table_html += f"<h3 style='text-align:center; font-weight:bold; margin-bottom:0.5rem;'>{to_currency} → {from_currency}</h3>"
table_html += "<table style='width:100%; text-align:center; border-collapse: collapse;'>"
for s in steps:
    table_html += f"<tr style='border-bottom:1px solid #ddd;'><td style='padding:0.5rem;'>{s}</td><td style='padding:0.5rem;'>{round(s/rate,2)}</td></tr>"
table_html += "</table></div>"

table_html += "</div>"

components.html(table_html, height=450)

