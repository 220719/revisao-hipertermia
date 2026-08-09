import duckdb
import json
from pathlib import Path

DB_PATH = "data/artigos.duckdb"

def criar_banco():
    con = duckdb.connect(DB_PATH)
    con.execute("DROP TABLE IF EXISTS artigos")
    con.execute("""
        CREATE TABLE artigos (
            id VARCHAR PRIMARY KEY,
            autores VARCHAR,
            ano INTEGER,
            periodico VARCHAR,
            titulo VARCHAR,
            doi VARCHAR,
            tipo_estudo VARCHAR,
            q1_conceito VARCHAR,
            q1_janela_min FLOAT,
            q1_janela_max FLOAT,
            q1_vias_morte VARCHAR,
            q2_neel BOOLEAN,
            q2_browniana BOOLEAN,
            q2_histerese BOOLEAN,
            q2_coletivas BOOLEAN,
            q2_nanoscale BOOLEAN,
            q2_forma_onda VARCHAR,
            q2_mecanismo_dominante VARCHAR,
            q2_descricao VARCHAR,
            q3_material VARCHAR,
            q3_dopagem VARCHAR,
            q3_tamanho_nm FLOAT,
            q3_tamanho_min FLOAT,
            q3_tamanho_max FLOAT,
            q3_forma VARCHAR,
            q3_multicore BOOLEAN,
            q3_anisotropia VARCHAR,
            q3_revestimento VARCHAR,
            q3_autorregulavel BOOLEAN,
            q3_SAR FLOAT,
            q3_ILP FLOAT,
            q3_Ms FLOAT,
            q4_amplitude FLOAT,
            q4_frequencia FLOAT,
            q4_limite_seguranca BOOLEAN,
            q4_tempo_min FLOAT,
            q4_forma_onda VARCHAR,
            q4_dosimetria VARCHAR,
            q5_tipo_estudo VARCHAR,
            q5_linhagem VARCHAR,
            q5_modelo_animal VARCHAR,
            q5_tipo_cancer VARCHAR,
            q5_concentracao FLOAT,
            q5_agregacao BOOLEAN,
            q5_protein_corona BOOLEAN,
            q5_toxicidade BOOLEAN,
            q5_apoptose BOOLEAN,
            q5_necrose BOOLEAN,
            q5_ferroptose BOOLEAN,
            q5_imunomodulacao BOOLEAN,
            q6_limitacoes VARCHAR,
            q6_problemas_SAR BOOLEAN,
            q6_padronizacao BOOLEAN,
            q6_recomendacoes VARCHAR,
            q7_fisica VARCHAR,
            q7_engenharia VARCHAR,
            q7_biologia VARCHAR,
            q7_materiais VARCHAR,
            q7_mensagem VARCHAR,
            json_completo VARCHAR
        )
    """)
    con.close()
    print("Banco criado em", DB_PATH)

def ingerir_artigo(con, dados: dict):
    q1 = dados.get("q1") or {}
    q2 = dados.get("q2") or {}
    q3 = dados.get("q3") or {}
    q4 = dados.get("q4") or {}
    q5 = dados.get("q5") or {}
    q6 = dados.get("q6") or {}
    q7 = dados.get("q7") or {}

    artigo_id = dados.get("custom_id") or dados.get("id") or dados.get("arquivo", "")

    valores = [
        artigo_id,
        dados.get("autores"),
        dados.get("ano"),
        dados.get("periodico"),
        dados.get("titulo"),
        dados.get("doi"),
        dados.get("tipo_estudo"),
        q1.get("conceito_tecnica"),
        q1.get("janela_termica_min_C"),
        q1.get("janela_termica_max_C"),
        json.dumps(q1.get("vias_morte_celular"), ensure_ascii=False),
        q2.get("relaxacao_neel"),
        q2.get("relaxacao_browniana"),
        q2.get("perdas_histerese"),
        q2.get("interacoes_coletivas"),
        q2.get("nanoscale_heating"),
        q2.get("forma_onda_campo"),
        q2.get("mecanismo_dominante"),
        q2.get("descricao_mecanismo"),
        q3.get("material"),
        q3.get("dopagem"),
        q3.get("tamanho_nm"),
        q3.get("faixa_tamanho_min_nm"),
        q3.get("faixa_tamanho_max_nm"),
        q3.get("forma"),
        q3.get("arquitetura_multicore"),
        q3.get("anisotropia"),
        q3.get("revestimento"),
        q3.get("material_autorregulavel"),
        q3.get("SAR_W_g"),
        q3.get("ILP_nHm2_kg"),
        q3.get("magnetizacao_saturacao_emu_g"),
        q4.get("amplitude_kA_m"),
        q4.get("frequencia_kHz"),
        q4.get("dentro_limite_seguranca"),
        q4.get("tempo_tratamento_min"),
        q4.get("forma_onda"),
        q4.get("dosimetria_termica"),
        q5.get("tipo_estudo"),
        q5.get("linhagem_celular"),
        q5.get("modelo_animal"),
        q5.get("tipo_cancer"),
        q5.get("concentracao_mg_mL"),
        q5.get("agregacao_discutida"),
        q5.get("protein_corona"),
        q5.get("toxicidade_avaliada"),
        q5.get("apoptose"),
        q5.get("necrose"),
        q5.get("ferroptose"),
        q5.get("imunomodulacao"),
        json.dumps(q6.get("limitacoes_reportadas"), ensure_ascii=False),
        q6.get("problemas_SAR_ILP"),
        q6.get("falta_padronizacao"),
        json.dumps(q6.get("recomendacoes_futuras"), ensure_ascii=False),
        q7.get("integracao_fisica"),
        q7.get("integracao_engenharia"),
        q7.get("integracao_biologia"),
        q7.get("integracao_materiais"),
        q7.get("mensagem_principal"),
        json.dumps(dados, ensure_ascii=False)
    ]

    placeholders = ", ".join(["?"] * len(valores))
    con.execute(f"INSERT OR REPLACE INTO artigos VALUES ({placeholders})", valores)

def ingerir_pasta(pasta: Path):
    criar_banco()
    con = duckdb.connect(DB_PATH)

    jsons = list(pasta.glob("*.json"))
    print(f"Ingerindo {len(jsons)} artigos no DuckDB...")

    for arquivo in jsons:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        ingerir_artigo(con, dados)
        print(f"  ✓ {arquivo.name[:50]}")

    total = con.execute("SELECT COUNT(*) FROM artigos").fetchone()[0]
    print(f"\nBanco atualizado: {total} artigos no total")
    con.close()

if __name__ == "__main__":
    ingerir_pasta(Path("data/extraidos"))
