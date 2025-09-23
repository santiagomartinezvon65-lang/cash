import streamlit as st
import requests

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

    # Input columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h4 style='color:#1F618D;'>From</h4>", unsafe_allow_html=True)
        from_currency = st.selectbox("From currency", list(currencies.keys()), index=3, label_visibility="collapsed")
        amount = st.number_input(
            f"Amount in {from_currency}", min_value=0.0, step=10.0,
            format="%.2f",
            key="from_amount",
            help="Enter the amount to convert"
        )

    with col2:
        st.markdown("<h4 style='color:#1F618D;'>To</h4>", unsafe_allow_html=True)
        to_currency = st.selectbox("To currency", list(currencies.keys()), index=0, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)  # spacing

    if amount > 0:
        # Convert to USD first, then to target
        usd_amount = amount / rates[from_currency]
        result = usd_amount * rates[to_currency]

        # Mostrar ambas cajas al lado
        col_amount, col_result = st.columns(2)

        box_style = """
        background-color:#EAF2F8; 
        padding:20px; 
        border-radius:12px; 
        text-align:center; 
        border:1px solid #D5D8DC; 
        box-shadow:0 2px 5px rgba(0,0,0,0.05);
        """

        with col_amount:
            st.markdown(
                f"""
                <div style='{box_style}'>
                    <h3 style='margin:0; color:#1F618D; font-weight:500;'>{amount:,.2f} {from_currency}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_result:
            st.markdown(
                f"""
                <div style='{box_style}'>
                    <h3 style='margin:0; color:#1F618D; font-weight:500;'>= {result:,.2f} {to_currency}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Tabla de referencia
        steps = [1, 5, 10, 25, 50, 100, 500, 1000]
        table_html = "<div style='display:flex; justify-content:center; gap:30px; margin-top:20px; flex-wrap:wrap;'>"

        # From -> To
        left_table = "<div style='background:#D6EAF8; border-radius:12px; padding:15px; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>"
        left_table += f"<h4 style='text-align:center; margin-bottom:10px; color:#1F618D;'>{from_currency} → {to_currency}</h4>"
        left_table += "<table style='width:100%; border-collapse: collapse;'>"
        for s in steps:
            left_table += f"<tr style='border-bottom:1px solid #AED6F1;'><td style='padding:4px;'>{s} {from_currency}</td><td style='padding:4px;'>{(s / rates[from_currency] * rates[to_currency]):,.2f} {to_currency}</td></tr>"
        left_table += "</table></div>"

        # To -> From
        right_table = "<div style='background:#D6EAF8; border-radius:12px; padding:15px; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>"
        right_table += f"<h4 style='text-align:center; margin-bottom:10px; color:#1F618D;'>{to_currency} → {from_currency}</h4>"
        right_table += "<table style='width:100%; border-collapse: collapse;'>"
        for s in steps:
            right_table += f"<tr style='border-bottom:1px solid #AED6F1;'><td style='padding:4px;'>{s} {to_currency}</td><td style='padding:4px;'>{(s / rates[to_currency] * rates[from_currency]):,.2f} {from_currency}</td></tr>"
        right_table += "</table></div>"

        table_html += left_table + right_table + "</div>"

        st.markdown(table_html, unsafe_allow_html=True)

    st.caption("Rates provided by open.er-api.com")

except Exception:
    st.error("Error: Could not fetch exchange rates. Try again later.")
