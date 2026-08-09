import streamlit as st

st.set_page_config(
    page_title="Revisão — Hipertermia Magnética",
    page_icon="🧲",
    layout="wide"
)

st.title("🧲 Revisão Sistemática")
st.subheader("Hipertermia Magnética para Tratamento de Câncer")

st.markdown("""
Esta plataforma permite explorar e consultar os **100 artigos** 
da revisão sistemática sobre hipertermia magnética.

### Páginas disponíveis

| Página | Descrição |
|--------|-----------|
| 📊 **Explorador** | Filtre e visualize os artigos por material, mecanismo, SAR, ano |
| 💬 **Perguntas** | Faça perguntas em português sobre os artigos |
| 📝 **Revisão** | Gere rascunhos das seções do artigo |
| 📥 **Exportar** | Baixe tabelas em DOCX ou CSV |

### Como usar
Use o menu lateral esquerdo para navegar entre as páginas.
""")

st.divider()

# Estatísticas rápidas do banco
try:
    import duckdb
    con = duckdb.connect("data/artigos.duckdb", read_only=True)
    total = con.execute("SELECT COUNT(*) FROM artigos").fetchone()[0]
    anos = con.execute("SELECT MIN(ano), MAX(ano) FROM artigos WHERE ano IS NOT NULL").fetchone()
    materiais = con.execute("SELECT COUNT(DISTINCT q3_material) FROM artigos WHERE q3_material IS NOT NULL").fetchone()[0]
    con.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de artigos", total)
    col2.metric("Período", f"{anos[0]}–{anos[1]}" if anos[0] else "—")
    col3.metric("Materiais distintos", materiais)
except:
    st.info("Banco de dados sendo carregado...")
