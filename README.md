# 🧲 Revisão Sistemática — Hipertermia Magnética

Plataforma colaborativa para revisão sistemática de artigos científicos sobre hipertermia magnética para tratamento de câncer.

## Sobre o projeto

Este repositório contém o pipeline completo de extração, análise e consulta de artigos científicos sobre Magnetic Fluid Hyperthermia (MFH), desenvolvido para subsidiar a escrita de um artigo de revisão submetido a revista científica convidada.

### Grupo
- Luiz Fernando Cotica
- Gabriel Tolardo
- Anuar Mincache

## Perguntas da revisão

| # | Pergunta |
|---|----------|
| Q1 | O que é hipertermia magnética? |
| Q2 | Quais mecanismos geram calor nas nanopartículas? |
| Q3 | Quais propriedades das nanopartículas controlam o aquecimento? |
| Q4 | Quais parâmetros estão envolvidos na aplicação? |
| Q5 | Quais fatores biológicos impactam o processo? |
| Q6 | Quais problemas a técnica enfrenta? |
| Q7 | Qual a contribuição integradora do artigo? |

## Stack tecnológica

| Componente | Tecnologia |
|-----------|------------|
| Extração de PDF | PyMuPDF |
| Extração estruturada | Claude Batch API |
| Banco de dados | DuckDB |
| Busca semântica | ChromaDB |
| Chat RAG | Claude API |
| Interface | Streamlit |
| Controle de acesso | Google OAuth |

## Como rodar localmente

git clone https://github.com/220719/revisao-hipertermia.git
cd revisao-hipertermia
uv sync
cp .env.example .env
uv run streamlit run app/app.py

## Como atualizar com novos artigos

uv run python src/extrator_pdf.py
uv run python src/extrator_llm.py
uv run python src/database.py
uv run python src/indexador.py
git add data/artigos.duckdb data/extraidos/ data/chroma/
git commit -m "data: novos artigos"
git push

## Contato

Anuar Mincache — fisicanuar@gmail.com — Maringá, Paraná, Brasil
