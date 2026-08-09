import anthropic
import chromadb
import json
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "data/chroma"

def carregar_indice():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection("artigos")
    return embeddings, collection

def buscar_chunks(pergunta: str, embeddings, collection, n_resultados: int = 8) -> list[dict]:
    vetor = embeddings.embed_query(pergunta)
    resultados = collection.query(
        query_embeddings=[vetor],
        n_results=n_resultados,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for i in range(len(resultados["documents"][0])):
        chunks.append({
            "texto": resultados["documents"][0][i],
            "arquivo": resultados["metadatas"][0][i]["arquivo"],
            "distancia": resultados["distances"][0][i]
        })
    return chunks

def montar_contexto(chunks: list[dict]) -> str:
    contexto = ""
    arquivos_vistos = set()
    for chunk in chunks:
        arquivo = chunk["arquivo"]
        if arquivo not in arquivos_vistos:
            contexto += f"\n\n--- Artigo: {arquivo[:60]} ---\n"
            arquivos_vistos.add(arquivo)
        contexto += chunk["texto"] + "\n"
    return contexto

def responder(pergunta: str, embeddings, collection) -> str:
    # 1. Busca chunks relevantes
    chunks = buscar_chunks(pergunta, embeddings, collection)
    contexto = montar_contexto(chunks)

    # 2. Monta prompt
    prompt = f"""Você é um especialista em hipertermia magnética para tratamento de câncer.
Responda a pergunta abaixo baseando-se APENAS nos trechos dos artigos fornecidos.
Cite os artigos quando usar informações deles.
Responda em português, de forma clara e científica.

TRECHOS DOS ARTIGOS:
{contexto}

PERGUNTA: {pergunta}

RESPOSTA:"""

    # 3. Chama Claude
    client = anthropic.Anthropic()
    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return resposta.content[0].text

def main():
    print("Carregando índice...")
    embeddings, collection = carregar_indice()
    print(f"Índice carregado: {collection.count()} chunks\n")

    perguntas_teste = [
        "Quais mecanismos de geração de calor são discutidos nos artigos?",
        "Qual é a janela terapêutica de temperatura para hipertermia magnética?"
    ]

    for pergunta in perguntas_teste:
        print(f"PERGUNTA: {pergunta}")
        print("-" * 60)
        resposta = responder(pergunta, embeddings, collection)
        print(resposta)
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
