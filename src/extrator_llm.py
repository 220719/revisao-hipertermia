import anthropic
import json
import re
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def limpar_id(texto: str) -> str:
    """Remove caracteres inválidos do custom_id."""
    limpo = re.sub(r'[^a-zA-Z0-9_-]', '_', texto)
    return limpo[:64]

def carregar_prompt() -> str:
    with open("prompts/extracao_artigo.txt", "r", encoding="utf-8") as f:
        return f.read()

def carregar_textos(pasta: Path) -> list[dict]:
    textos = []
    for arquivo in sorted(pasta.glob("*.json")):
        with open(arquivo, "r", encoding="utf-8") as f:
            textos.append(json.load(f))
    return textos

def criar_requests(textos: list[dict], prompt_template: str) -> list[dict]:
    requests = []
    for t in textos:
        texto_truncado = t["texto"][:90000]
        prompt = prompt_template.replace("{texto}", texto_truncado)
        custom_id = limpar_id(Path(t["arquivo"]).stem)

        requests.append({
            "custom_id": custom_id,
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 4000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        })
    return requests

def enviar_batch(requests: list[dict]) -> str:
    client = anthropic.Anthropic()

    print(f"Enviando batch com {len(requests)} artigos...")

    batch = client.messages.batches.create(requests=requests)

    print(f"Batch criado: {batch.id}")
    print(f"Status: {batch.processing_status}")

    with open("data/batch_id.txt", "w") as f:
        f.write(batch.id)

    return batch.id

def aguardar_batch(batch_id: str) -> bool:
    client = anthropic.Anthropic()

    print(f"\nAguardando processamento do batch {batch_id}...")
    print("Isso pode levar alguns minutos.\n")

    while True:
        batch = client.messages.batches.retrieve(batch_id)
        status = batch.processing_status
        counts = batch.request_counts

        print(f"Status: {status} | "
              f"Processando: {counts.processing} | "
              f"Concluídos: {counts.succeeded} | "
              f"Erros: {counts.errored}")

        if status == "ended":
            return True

        time.sleep(30)

def salvar_resultados(batch_id: str, pasta_saida: Path):
    client = anthropic.Anthropic()
    pasta_saida.mkdir(parents=True, exist_ok=True)

    print(f"\nSalvando resultados em {pasta_saida}...")

    salvos = 0
    erros = 0

    for result in client.messages.batches.results(batch_id):
        custom_id = result.custom_id

        if result.result.type == "succeeded":
            texto_resposta = result.result.message.content[0].text

            try:
                texto_limpo = texto_resposta.strip()
                if texto_limpo.startswith("```"):
                    texto_limpo = texto_limpo.split("```")[1]
                    if texto_limpo.startswith("json"):
                        texto_limpo = texto_limpo[4:]

                dados = json.loads(texto_limpo)
                dados["custom_id"] = custom_id

                saida = pasta_saida / f"{custom_id}.json"
                with open(saida, "w", encoding="utf-8") as f:
                    json.dump(dados, f, ensure_ascii=False, indent=2)

                print(f"  ✓ {custom_id[:50]}")
                salvos += 1

            except json.JSONDecodeError as e:
                print(f"  ✗ Erro JSON em {custom_id}: {e}")
                saida = pasta_saida / f"{custom_id}_raw.txt"
                with open(saida, "w", encoding="utf-8") as f:
                    f.write(texto_resposta)
                erros += 1
        else:
            print(f"  ✗ Falhou: {custom_id} — {result.result.type}")
            erros += 1

    print(f"\nConcluído: {salvos} salvos, {erros} erros")

def main():
    pasta_textos = Path("data/textos")
    pasta_extraidos = Path("data/extraidos")

    prompt = carregar_prompt()
    textos = carregar_textos(pasta_textos)
    print(f"Textos carregados: {len(textos)} artigos")

    requests = criar_requests(textos, prompt)
    batch_id = enviar_batch(requests)

    aguardar_batch(batch_id)

    salvar_resultados(batch_id, pasta_extraidos)

if __name__ == "__main__":
    main()
