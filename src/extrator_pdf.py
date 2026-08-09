import pymupdf
import json
from pathlib import Path

def extrair_texto(caminho_pdf: Path) -> dict:
    """Extrai texto de um PDF e retorna metadados + texto."""
    doc = pymupdf.open(str(caminho_pdf))
    
    texto_completo = ""
    num_paginas = doc.page_count
    
    for page in doc:
        texto_completo += page.get_text("text")
    
    doc.close()
    
    return {
        "arquivo": caminho_pdf.name,
        "pasta": caminho_pdf.parent.name,
        "paginas": num_paginas,
        "caracteres": len(texto_completo),
        "texto": texto_completo
    }

def processar_pasta(pasta_pdfs: Path, pasta_saida: Path):
    """Processa todos os PDFs de uma pasta."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    
    pdfs = list(pasta_pdfs.glob("*.pdf"))
    print(f"Encontrados {len(pdfs)} PDFs em {pasta_pdfs}")
    
    for pdf in pdfs:
        print(f"  Processando: {pdf.name}...")
        
        resultado = extrair_texto(pdf)
        
        # Salva como JSON
        saida = pasta_saida / (pdf.stem + ".json")
        with open(saida, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ {resultado['paginas']} páginas, {resultado['caracteres']} caracteres")
    
    print(f"\nConcluído. {len(pdfs)} arquivos salvos em {pasta_saida}")

if __name__ == "__main__":
    pasta_pdfs = Path("data/pdfs")
    pasta_saida = Path("data/textos")
    processar_pasta(pasta_pdfs, pasta_saida)
