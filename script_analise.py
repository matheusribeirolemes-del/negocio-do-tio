import pandas as pd
import numpy as np
import plotly.express as px
import json

# 1. LEVANTAMENTO E COLETA DE DADOS (SIMULAÇÃO)
np.random.seed(42)
n_jovens = 300

dados = {
    "id": range(1, n_jovens + 1),
    "renda_familiar_sm": np.random.choice(
        ["Até 1 SM", "1 a 2 SM", "2 a 4 SM", "Mais de 4 SM"],
        n_jovens,
        p=[0.40, 0.35, 0.15, 0.10]
    ),
    "acesso_internet": np.random.choice(
        ["Banda Larga", "Apenas 4G/5G", "Sem Acesso Regular"],
        n_jovens,
        p=[0.50, 0.40, 0.10]
    ),
    "frequencia_escolar_pct": np.random.normal(85, 10, n_jovens).clip(50, 100).round(1),
    "horas_estudo_diario": np.random.choice([1, 2, 3, 4, 5], n_jovens, p=[0.30, 0.35, 0.20, 0.10, 0.05]),
    "tempo_deslocamento_min": np.random.randint(15, 120, n_jovens),
    "nivel_satisfacao_saude_mental": np.random.randint(1, 6, n_jovens)
}

df = pd.DataFrame(dados)

# 2. TRATAMENTO E ANÁLISE EXPLORATÓRIA (EDA)
df["risco_evasao"] = np.where(
    (df["frequencia_escolar_pct"] < 75) | (df["acesso_internet"] == "Sem Acesso Regular"),
    "Alto",
    "Baixo"
)

media_frequencia = round(float(df["frequencia_escolar_pct"].mean()), 2)
pct_internet_limitada = round(float((df["acesso_internet"] != "Banda Larga").mean() * 100), 2)
taxa_risco_evasao = round(float((df["risco_evasao"] == "Alto").mean() * 100), 2)

# Exportação de gráficos para HTML
fig_renda_internet = px.histogram(
    df, x="renda_familiar_sm", color="acesso_internet",
    title="Acesso à Internet por Faixa de Renda Familiar",
    barmode="group",
    labels={"renda_familiar_sm": "Renda Familiar", "count": "Quantidade de Jovens"}
)
fig_renda_internet.write_html("grafico_renda_internet.html")

# Exportação do resumo executivo em JSON
resumo = {
    "media_frequencia": media_frequencia,
    "pct_internet_limitada": pct_internet_limitada,
    "taxa_risco_evasao": taxa_risco_evasao,
    "total_jovens_analisados": n_jovens
}

with open("dados_resumo.json", "w", encoding="utf-8") as f:
    json.dump(resumo, f, ensure_ascii=False, indent=4)