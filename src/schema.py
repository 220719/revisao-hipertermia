from pydantic import BaseModel, Field
from typing import Optional

# ─────────────────────────────────────────
# Q1 — O que é hipertermia magnética?
# ─────────────────────────────────────────
class Q1_Conceito(BaseModel):
    conceito_tecnica: Optional[str] = Field(None,
        description="Definição da técnica conforme o artigo")
    etapas_processo: Optional[list[str]] = Field(None,
        description="Etapas do processo terapêutico")
    internalizacao_nps: Optional[str] = Field(None,
        description="Como as NPs são internalizadas")
    aplicacao_campo: Optional[str] = Field(None,
        description="Como o campo magnético alternado é aplicado")
    janela_termica_min_C: Optional[float] = Field(None,
        description="Temperatura mínima da janela terapêutica em °C")
    janela_termica_max_C: Optional[float] = Field(None,
        description="Temperatura máxima da janela terapêutica em °C")
    vias_morte_celular: Optional[list[str]] = Field(None,
        description="Vias de morte celular: apoptose, necrose, ferroptose, imunomodulação")

# ─────────────────────────────────────────
# Q2 — Mecanismos de geração de calor
# ─────────────────────────────────────────
class Q2_Mecanismos(BaseModel):
    relaxacao_neel: Optional[bool] = Field(None,
        description="Artigo discute relaxação de Néel?")
    relaxacao_browniana: Optional[bool] = Field(None,
        description="Artigo discute relaxação Browniana?")
    perdas_histerese: Optional[bool] = Field(None,
        description="Artigo discute perdas por histerese?")
    interacoes_coletivas: Optional[bool] = Field(None,
        description="Artigo discute interações coletivas entre NPs?")
    nanoscale_heating: Optional[bool] = Field(None,
        description="Artigo discute aquecimento localizado (nanoscale heating)?")
    forma_onda_campo: Optional[str] = Field(None,
        description="Forma de onda do campo: senoidal, quadrada, trapezoidal")
    mecanismo_dominante: Optional[str] = Field(None,
        description="Mecanismo de aquecimento predominante no artigo")
    descricao_mecanismo: Optional[str] = Field(None,
        description="Descrição do mecanismo físico principal")

# ─────────────────────────────────────────
# Q3 — Propriedades das nanopartículas
# ─────────────────────────────────────────
class Q3_Nanoparticulas(BaseModel):
    material: Optional[str] = Field(None,
        description="Material principal: Fe3O4, γ-Fe2O3, ferrita, etc.")
    composicao_quimica: Optional[str] = Field(None,
        description="Composição química detalhada")
    dopagem: Optional[str] = Field(None,
        description="Elemento dopante se houver: Ce, Mn, Zn, Co, etc.")
    tamanho_nm: Optional[float] = Field(None,
        description="Tamanho médio das NPs em nm")
    faixa_tamanho_min_nm: Optional[float] = Field(None,
        description="Tamanho mínimo reportado em nm")
    faixa_tamanho_max_nm: Optional[float] = Field(None,
        description="Tamanho máximo reportado em nm")
    forma: Optional[str] = Field(None,
        description="Forma das NPs: esférica, cubo, flor, haste, etc.")
    arquitetura_multicore: Optional[bool] = Field(None,
        description="NPs multicore (nanoflowers, Rubik-like)?")
    anisotropia: Optional[str] = Field(None,
        description="Tipo de anisotropia: magnetocristalina, forma, superfície")
    revestimento: Optional[str] = Field(None,
        description="Revestimento superficial: PEG, quitosana, sílica, etc.")
    material_autorregulavel: Optional[bool] = Field(None,
        description="Material com temperatura de Curie na faixa terapêutica?")
    SAR_W_g: Optional[float] = Field(None,
        description="Specific Absorption Rate em W/g")
    ILP_nHm2_kg: Optional[float] = Field(None,
        description="Intrinsic Loss Power em nH·m²/kg")
    magnetizacao_saturacao_emu_g: Optional[float] = Field(None,
        description="Magnetização de saturação em emu/g")
    relacao_estrutura_propriedade: Optional[str] = Field(None,
        description="Como estrutura afeta propriedades magnéticas")

# ─────────────────────────────────────────
# Q4 — Parâmetros de aplicação
# ─────────────────────────────────────────
class Q4_Parametros(BaseModel):
    amplitude_kA_m: Optional[float] = Field(None,
        description="Amplitude do campo magnético em kA/m")
    frequencia_kHz: Optional[float] = Field(None,
        description="Frequência do campo em kHz")
    produto_Hf: Optional[float] = Field(None,
        description="Produto H×f em A/m·s (limite de segurança)")
    dentro_limite_seguranca: Optional[bool] = Field(None,
        description="H×f ≤ 5×10⁹ A/m·s (limite Hergt-Dutz)?")
    tempo_tratamento_min: Optional[float] = Field(None,
        description="Tempo de tratamento em minutos")
    forma_onda: Optional[str] = Field(None,
        description="Forma de onda: senoidal, quadrada, trapezoidal, pulsada")
    dosimetria_termica: Optional[str] = Field(None,
        description="Método de dosimetria térmica usado")
    distribuicao_espacial_calor: Optional[str] = Field(None,
        description="Como o calor se distribui espacialmente")
    padronizacao_reportada: Optional[bool] = Field(None,
        description="Artigo segue recomendações de padronização?")

# ─────────────────────────────────────────
# Q5 — Fatores biológicos
# ─────────────────────────────────────────
class Q5_Biologico(BaseModel):
    tipo_estudo: Optional[str] = Field(None,
        description="in vitro, in vivo, in silico, ex vivo, clínico")
    linhagem_celular: Optional[str] = Field(None,
        description="Linhagem celular usada: HeLa, MCF-7, etc.")
    modelo_animal: Optional[str] = Field(None,
        description="Modelo animal: camundongo, rato, etc.")
    tipo_cancer: Optional[str] = Field(None,
        description="Tipo de câncer estudado")
    concentracao_mg_mL: Optional[float] = Field(None,
        description="Concentração de NPs em mg/mL")
    agregacao_discutida: Optional[bool] = Field(None,
        description="Artigo discute agregação das NPs?")
    viscosidade_discutida: Optional[bool] = Field(None,
        description="Artigo discute viscosidade do meio?")
    imobilizacao_celular: Optional[bool] = Field(None,
        description="Artigo discute imobilização intracelular?")
    perfusao_discutida: Optional[bool] = Field(None,
        description="Artigo discute perfusão sanguínea?")
    protein_corona: Optional[bool] = Field(None,
        description="Artigo discute protein corona?")
    biodistribuicao: Optional[bool] = Field(None,
        description="Artigo avalia biodistribuição?")
    toxicidade_avaliada: Optional[bool] = Field(None,
        description="Artigo avalia toxicidade?")
    localizacao_intracelular: Optional[bool] = Field(None,
        description="Artigo discute localização intracelular das NPs?")
    apoptose: Optional[bool] = Field(None,
        description="Via de morte: apoptose?")
    necrose: Optional[bool] = Field(None,
        description="Via de morte: necrose?")
    ferroptose: Optional[bool] = Field(None,
        description="Via de morte: ferroptose?")
    imunomodulacao: Optional[bool] = Field(None,
        description="Via de morte: imunomodulação?")

# ─────────────────────────────────────────
# Q6 — Problemas e limitações
# ─────────────────────────────────────────
class Q6_Limitacoes(BaseModel):
    limitacoes_reportadas: Optional[list[str]] = Field(None,
        description="Limitações explicitamente reportadas pelos autores")
    problemas_SAR_ILP: Optional[bool] = Field(None,
        description="Artigo discute problemas na comparação de SAR/ILP?")
    falta_padronizacao: Optional[bool] = Field(None,
        description="Artigo menciona falta de padronização?")
    recomendacoes_futuras: Optional[list[str]] = Field(None,
        description="Recomendações para estudos futuros")
    gaps_identificados: Optional[list[str]] = Field(None,
        description="Lacunas identificadas na literatura")

# ─────────────────────────────────────────
# Q7 — Conclusão integradora
# ─────────────────────────────────────────
class Q7_Conclusao(BaseModel):
    integracao_fisica: Optional[str] = Field(None,
        description="Contribuição do artigo para física das NPs")
    integracao_engenharia: Optional[str] = Field(None,
        description="Contribuição do artigo para engenharia do campo")
    integracao_biologia: Optional[str] = Field(None,
        description="Contribuição do artigo para contexto biológico")
    integracao_materiais: Optional[str] = Field(None,
        description="Contribuição do artigo para ciência dos materiais")
    mensagem_principal: Optional[str] = Field(None,
        description="Principal mensagem ou contribuição do artigo")

# ─────────────────────────────────────────
# Schema completo do artigo
# ─────────────────────────────────────────
class Artigo(BaseModel):
    # Metadados
    id: str = Field(description="Identificador único: número do arquivo")
    arquivo: str = Field(description="Nome do arquivo PDF")
    pasta: str = Field(description="Pasta de origem: 10_0, 10_1, etc.")
    autores: Optional[str] = Field(None, description="Autores do artigo")
    ano: Optional[int] = Field(None, description="Ano de publicação")
    periodico: Optional[str] = Field(None, description="Nome do periódico")
    titulo: Optional[str] = Field(None, description="Título completo")
    doi: Optional[str] = Field(None, description="DOI do artigo")
    tipo_estudo: Optional[str] = Field(None,
        description="in vitro, in vivo, in silico, revisão, etc.")

    # As 7 perguntas
    q1: Optional[Q1_Conceito] = None
    q2: Optional[Q2_Mecanismos] = None
    q3: Optional[Q3_Nanoparticulas] = None
    q4: Optional[Q4_Parametros] = None
    q5: Optional[Q5_Biologico] = None
    q6: Optional[Q6_Limitacoes] = None
    q7: Optional[Q7_Conclusao] = None
