import streamlit as st
import duckdb
import pandas as pd
import io

st.set_page_config(page_title="Exportar", page_icon="📥", layout="wide")
st.title("📥 Exportar Dados")

DB_PATH = "data/artigos.duckdb"

@st.cache_data
def carregar_dados():
    con = duckdb.connect(DB_PATH, read_only=True)
    df = con.execute("SELECT * FROM artigos").df()
    con.close()
    return df

df = carregar_dados()

st.subheader("Exportar tabela completa")

# CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Baixar CSV completo",
    data=csv,
    file_name="artigos_hipertermia.csv",
    mime="text/csv"
)

st.divider()

st.subheader("Exportar por pergunta")

opcoes = {
    "Q1 — Conceito e etapas": ["autores", "ano", "q1_conceito", "q1_janela_min", "q1_janela_max", "q1_vias_morte"],
    "Q2 — Mecanismos": ["autores", "ano", "q2_neel", "q2_browniana", "q2_histerese", "q2_mecanismo_dominante", "q2_descricao"],
    "Q3 — Nanopartículas": ["autores", "ano", "q3_material", "q3_dopagem", "q3_tamanho_nm", "q3_SAR", "q3_ILP", "q3_Ms", "q3_revestimento"],
    "Q4 — Parâmetros": ["autores", "ano", "q4_amplitude", "q4_frequencia", "q4_limite_seguranca", "q4_forma_onda"],
    "Q5 — Biológico": ["autores", "ano", "q5_tipo_estudo", "q5_linhagem", "q5_tipo_cancer", "q5_apoptose", "q5_necrose", "q5_ferroptose"],
    "Q6 — Limitações": ["autores", "ano", "q6_limitacoes", "q6_problemas_SAR", "q6_padronizacao"],
}

pergunta_sel = st.selectbox("Selecione a pergunta", list(opcoes.keys()))
colunas = [c for c in opcoes[pergunta_sel] if c in df.columns]
df_sel = df[colunas].dropna(how="all")

st.dataframe(df_sel, use_container_width=True)

csv_sel = df_sel.to_csv(index=False).encode("utf-8")
st.download_button(
    label=f"⬇️ Baixar {pergunta_sel}",
    data=csv_sel,
    file_name=f"tabela_{pergunta_sel[:2].lower()}.csv",
    mime="text/csv"
)
