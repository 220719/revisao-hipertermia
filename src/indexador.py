import chromadb
import json
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_PATH = "data/chroma"

def criar_chunks(texto: str, arquivo: str) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = splitter.split_text(texto)
    return [
        {"texto": chunk, "arquivo": arquivo, "chunk_id": i}
        for i, chunk in enumerate(chunks)
    ]

def indexar_artigos(pasta_textos: Path):
    print("Iniciando indexação no ChromaDB...")
    print("(Primeira vez pode demorar — baixando modelo de embeddings)\n")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection("artigos")
    except:
        pass

    collection = client.create_collection(
        name="artigos",
        metadata={"hnsw:space": "cosine"}
    )

    jsons = list(pasta_textos.glob("*.json"))
    print(f"Indexando {len(jsons)} artigos...\n")

    total_chunks = 0

    for arquivo in jsons:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        nome = dados["arquivo"]
        texto = dados["texto"]

        chunks = criar_chunks(texto, nome)

        textos = [c["texto"] for c in chunks]
        ids = [f"{arquivo.stem}__chunk_{c['chunk_id']}" for c in chunks]
        metadados = [{"arquivo": nome, "chunk_id": c["chunk_id"]} for c in chunks]

        vetores = embeddings.embed_documents(textos)

        collection.add(
            ids=ids,
            embeddings=vetores,
            documents=textos,
            metadatas=metadados
        )

        total_chunks += len(chunks)
        print(f"  ✓ {nome[:50]} — {len(chunks)} chunks")

    print(f"\nIndexação concluída: {total_chunks} chunks de {len(jsons)} artigos")
    print(f"Índice salvo em {CHROMA_PATH}")

if __name__ == "__main__":
    indexar_artigos(Path("data/textos"))
