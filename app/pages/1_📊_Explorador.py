import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Explorador", page_icon="📊", layout="wide")
st.title("📊 Explorador de Artigos")

DB_PATH = "data/artigos.duckdb"

@st.cache_data
def carregar_dados():
    con = duckdb.connect(DB_PATH, read_only=True)
    df = con.execute("SELECT * FROM artigos").df()
    con.close()
    return df

df = carregar_dados()

# Filtros na sidebar
st.sidebar.header("Filtros")

anos = sorted(df["ano"].dropna().unique().astype(int).tolist())
if anos:
    ano_range = st.sidebar.slider("Ano", min_value=min(anos), max_value=max(anos),
                                   value=(min(anos), max(anos)))
    df = df[df["ano"].between(ano_range[0], ano_range[1])]

materiais = ["Todos"] + sorted(df["q3_material"].dropna().unique().tolist())
material = st.sidebar.selectbox("Material", materiais)
if material != "Todos":
    df = df[df["q3_material"].str.contains(material, na=False, case=False)]

tipos = ["Todos"] + sorted(df["q5_tipo_estudo"].dropna().unique().tolist())
tipo = st.sidebar.selectbox("Tipo de estudo", tipos)
if tipo != "Todos":
    df = df[df["q5_tipo_estudo"] == tipo]

neel = st.sidebar.checkbox("Relaxação de Néel")
if neel:
    df = df[df["q2_neel"] == True]

browniana = st.sidebar.checkbox("Relaxação Browniana")
if browniana:
    df = df[df["q2_browniana"] == True]

st.write(f"**{len(df)} artigos** encontrados")
st.divider()

# Tabela principal
colunas = ["autores", "ano", "periodico", "q3_material",
           "q3_SAR", "q4_frequencia", "q5_tipo_estudo"]
colunas_existentes = [c for c in colunas if c in df.columns]
st.dataframe(df[colunas_existentes], use_container_width=True, height=400)

st.divider()

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mecanismos de aquecimento")
    mecanismos = {
        "Néel": df["q2_neel"].sum(),
        "Browniana": df["q2_browniana"].sum(),
        "Histerese": df["q2_histerese"].sum(),
        "Coletivas": df["q2_coletivas"].sum(),
        "Nanoscale": df["q2_nanoscale"].sum()
    }
    fig = px.bar(x=list(mecanismos.keys()), y=list(mecanismos.values()),
                 labels={"x": "Mecanismo", "y": "Nº de artigos"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Tipo de estudo")
    tipo_counts = df["q5_tipo_estudo"].value_counts()
    if not tipo_counts.empty:
        fig2 = px.pie(values=tipo_counts.values, names=tipo_counts.index)
        st.plotly_chart(fig2, use_container_width=True)
