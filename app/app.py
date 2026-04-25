import streamlit as st
import pandas as pd
import subprocess
from auth import login

auth = login()

if not auth:
    st.warning("Acceso restringido")
    st.stop()

subprocess.run(["python", "src/ingesta.py"])
subprocess.run(["python", "src/transform.py"])

# configuración
st.set_page_config(layout="wide")

# cargar datos
df = pd.read_parquet("data/crypto.parquet")

# =========================
# 1. TÍTULO
# =========================
st.title("Dashboard del Mercado Cripto")
st.caption("Datos en tiempo real desde API - Análisis de capitalización y variación")

st.divider()

# =========================
# 2. KPIs
# =========================
top = df.sort_values(by='capitalizacion', ascending=False).iloc[0]
top_gain = df.sort_values(by='cambio_24h', ascending=False).iloc[0]
top_loss = df.sort_values(by='cambio_24h').iloc[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Market Cap Total", f"${df['capitalizacion'].sum():,.0f}")
col2.metric("Cambio Promedio 24h", f"{df['cambio_24h'].mean():.2f}%")
col3.metric("Top Cripto", top['crypto'])
col4.metric("Precio Top", f"${top['precio']:,.2f}")

st.divider()

# =========================
# 3. GRÁFICOS
# =========================

col1, col2 = st.columns(2)

top10 = df.sort_values(by='capitalizacion', ascending=False).head(10)

with col1:
    st.subheader("Top 10 por Capitalización")
    st.bar_chart(top10.set_index('crypto')['capitalizacion'])

with col2:
    st.subheader("Variación 24h (%)")
    st.bar_chart(top10.set_index('crypto')['cambio_24h'])

st.divider()

# =========================
# 4. FILTRO
# =========================
st.subheader("🔍 Análisis por criptomoneda")

crypto = st.selectbox("Selecciona criptomoneda", df['crypto'])

row = df[df['crypto'] == crypto].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric("Precio", f"${row['precio']:,.2f}")
col2.metric("Market Cap", f"${row['capitalizacion']:,.0f}")
col3.metric("Cambio 24h", f"{row['cambio_24h']:.2f}%")

st.divider()

# =========================
# 5. TABLA DETALLADA
# =========================
def color_cambio(val):
    if val > 0:
        return 'color: green'
    elif val < 0:
        return 'color: red'
    return 'color: gray'

styled_df = df.style.format({
    "precio": "${:,.2f}",
    "capitalizacion": "${:,.0f}"
})

styled_df = styled_df.map(color_cambio, subset=["cambio_24h"])

st.dataframe(styled_df)

