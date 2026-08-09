import streamlit as st
import sys
sys.path.append(".")
from src.rag import carregar_indice, responder

st.set_page_config(page_title="Perguntas", page_icon="💬", layout="wide")
st.title("💬 Perguntas sobre os Artigos")
st.caption("Faça qualquer pergunta sobre os 100 artigos da revisão")

# Carrega índice uma vez
@st.cache_resource
def get_indice():
    return carregar_indice()

with st.spinner("Carregando índice de artigos..."):
    embeddings, collection = get_indice()

st.success(f"✓ {collection.count()} chunks indexados de {len(set([m['arquivo'] for m in collection.get()['metadatas']]))} artigos")
st.divider()

# Histórico de perguntas
if "historico" not in st.session_state:
    st.session_state.historico = []

# Input
pergunta = st.chat_input("Digite sua pergunta sobre hipertermia magnética...")

if pergunta:
    st.session_state.historico.append({"role": "user", "content": pergunta})

    with st.spinner("Consultando artigos..."):
        resposta = responder(pergunta, embeddings, collection)

    st.session_state.historico.append({"role": "assistant", "content": resposta})

# Mostra histórico
for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
