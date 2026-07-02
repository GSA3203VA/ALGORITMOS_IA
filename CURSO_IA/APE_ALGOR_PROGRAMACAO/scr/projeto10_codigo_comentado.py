# Projeto 10 (v2) - Obtendo Dados com APIs HTTP
# Versao comentada extraida do notebook projeto10_comentado.ipynb


# ----------------------------------------------------------------------
# Projeto 10 (v2) — Obtendo Dados com APIs HTTP
# 
# **Disciplina:** Algoritmos e Programação (APE)
# **Curso:** Especialização em Inteligência Artificial para Engenheiros — UFRGS
# **Professor:** Raphael Martins Brum — 2026
# 
# ---
# 
# Objetivo
# 
# Desenvolver um sistema que permita entender o **impacto do clima nas operações de uma empresa hipotética de logística** em diferentes cidades do Brasil, integrando quatro APIs públicas:
# 
# | API | Finalidade | Autenticação |
# |-----|-----------|-------------|
# | **ViaCEP** | Cidade, UF e código IBGE a partir do CEP | Nenhuma |
# | **Open-Meteo Geocoding** | Latitude/longitude da cidade | Nenhuma |
# | **Open-Meteo Archive** | Temperatura máx./mín. e precipitação diária de 2024 | Nenhuma |
# | **IBGE** | População do município (Censo 2022) | Nenhuma |

# ----------------------------------------------------------------------
# ---
# 0. Importações e configuração inicial

# ----------------------------------------------------------------------
# Como o c?digo est? organizado
# 
# O projeto segue o mesmo padr?o das aulas sobre APIs HTTP:
# 
# 1. **Montar a URL e os par?metros** da API.
# 2. **Fazer a requisi??o GET** com `requests`.
# 3. **Converter a resposta JSON** para dicion?rios/listas do Python.
# 4. **Validar e tratar os dados** antes da an?lise.
# 5. **Organizar tudo em DataFrames** para tabelas, gr?ficos e exporta??o.
# 
# A fun??o `_get_json` concentra a parte repetitiva das chamadas HTTP. As demais fun??es ficam pequenas e com uma responsabilidade clara.

# ============================================================
# 0. Importa??es e configura??o inicial
# ============================================================

import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec

# Mostra tabelas com mais conforto dentro do Jupyter/Colab.
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

# ------------------------------------------------------------
# CEPs representativos de diferentes regi?es do Brasil.
# A chave ? apenas um r?tulo amig?vel para aparecer no relat?rio.
# O valor ? o CEP consultado na API ViaCEP.
# ------------------------------------------------------------
CEPS = {
    "Porto Alegre - RS": "90010150",
    "S?o Paulo - SP":    "01310100",
    "Manaus - AM":       "69010080",
    "Recife - PE":       "50010080",
    "Cuiab? - MT":       "78005100",
    "Fortaleza - CE":    "60160180",
}

# ------------------------------------------------------------
# Endpoints usados no projeto.
# Deixar as URLs em constantes facilita manuten??o e leitura.
# ------------------------------------------------------------
URL_VIACEP = "https://viacep.com.br/ws/{cep}/json/"
URL_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
URL_ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"
URL_IBGE_POPULACAO = (
    "https://servicodados.ibge.gov.br/api/v3"
    "/agregados/4709/periodos/2022/variaveis/93"
)

# ------------------------------------------------------------
# Sess?o HTTP ?nica reaproveitada por todas as chamadas.
# Isso ? mais eficiente do que criar uma conex?o nova a cada request.
# O User-Agent identifica nosso script de forma educada para os servidores.
# ------------------------------------------------------------
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "projeto10-ape-ufrgs/2.0"})


def _get_json(url: str, params: dict | None = None, timeout: int = 15, tentativas: int = 3) -> dict | list:
    """
    Faz uma requisi??o HTTP GET e devolve a resposta convertida de JSON para Python.

    Par?metros:
    - url: endere?o do endpoint.
    - params: dicion?rio com os par?metros da query string.
    - timeout: tempo m?ximo de espera por tentativa.
    - tentativas: quantidade de tentativas antes de desistir.

    Por que criar esta fun??o?
    As quatro APIs do projeto usam o mesmo padr?o: GET -> status OK -> JSON.
    Centralizar esse padr?o evita repeti??o e deixa os erros mais f?ceis de tratar.
    """
    ultimo_erro: Exception | None = None

    for tentativa in range(1, tentativas + 1):
        try:
            resposta = SESSION.get(url, params=params, timeout=timeout)

            # Se o servidor retornar 404, 500 etc., esta linha gera uma exce??o.
            resposta.raise_for_status()

            # Converte o corpo JSON para tipos nativos do Python: dict/list/str/int/float.
            return resposta.json()

        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as exc:
            ultimo_erro = exc

            # Pausa progressiva: 0.5s, 1.0s, 2.0s...
            # Ajuda em instabilidades tempor?rias de rede/API.
            if tentativa < tentativas:
                espera = 0.5 * (2 ** (tentativa - 1))
                time.sleep(espera)

    raise RuntimeError(f"Falha ap?s {tentativas} tentativas em {url}: {ultimo_erro}")


print(f"Cidades configuradas: {list(CEPS.keys())}")

# ----------------------------------------------------------------------
# ---
# 1. Obtenção dos Dados
# 
# 1.1 API ViaCEP — Cidade, UF e código IBGE
# 
# Endpoint: `https://viacep.com.br/ws/{cep}/json/`
# Retorna JSON com `localidade`, `uf`, `ibge`, entre outros campos.

def fetch_viacep(cep: str) -> dict:
    """
    Consulta a API ViaCEP e retorna informa??es b?sicas do munic?pio.

    Entrada:
    - cep: string com 8 d?gitos, por exemplo "90010150".

    Sa?da:
    - dicion?rio com cidade, UF, c?digo IBGE e logradouro.
    """
    dados = _get_json(URL_VIACEP.format(cep=cep))

    # A API ViaCEP retorna {"erro": true} quando o CEP n?o existe.
    if "erro" in dados:
        raise ValueError(f"CEP n?o encontrado: {cep}")

    return {
        "cidade":     dados["localidade"],
        "uf":         dados["uf"],
        "ibge":       dados["ibge"],
        "logradouro": dados.get("logradouro", ""),
    }


# Teste r?pido com o CEP de Porto Alegre.
# Testes pequenos ajudam a encontrar erro antes de rodar o pipeline inteiro.
exemplo = fetch_viacep("90010150")
print("Resposta ViaCEP:", exemplo)

# ----------------------------------------------------------------------
# 1.2 API Open-Meteo Geocoding — Latitude e Longitude
# 
# Endpoint: `https://geocoding-api.open-meteo.com/v1/search`
# Parâmetros: `name` (apenas a cidade), `countryCode=BR`, e `count=10` para depois filtrar pela UF correta usando o campo `admin1` (nome do estado retornado pela API).

# A API de geocoding retorna o nome do estado por extenso no campo "admin1".
# Por isso precisamos converter a UF do ViaCEP para o nome completo do estado.
UF_PARA_ESTADO = {
    "AC": "Acre",             "AL": "Alagoas",             "AP": "Amap?",
    "AM": "Amazonas",         "BA": "Bahia",               "CE": "Cear?",
    "DF": "Distrito Federal", "ES": "Esp?rito Santo",      "GO": "Goi?s",
    "MA": "Maranh?o",         "MT": "Mato Grosso",         "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",     "PA": "Par?",                "PB": "Para?ba",
    "PR": "Paran?",           "PE": "Pernambuco",          "PI": "Piau?",
    "RJ": "Rio de Janeiro",   "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rond?nia",         "RR": "Roraima",             "SC": "Santa Catarina",
    "SP": "S?o Paulo",        "SE": "Sergipe",             "TO": "Tocantins",
}


def fetch_geocoding(cidade: str, uf: str) -> tuple[float, float]:
    """
    Busca latitude e longitude de uma cidade brasileira na API Open-Meteo Geocoding.

    A API pode retornar mais de uma cidade com o mesmo nome. Para reduzir erro,
    filtramos pelo pa?s BR e pelo estado correspondente ? UF.
    """
    dados = _get_json(
        URL_GEOCODING,
        params={
            "name":        cidade,
            "count":       10,
            "language":    "pt",
            "countryCode": "BR",
        },
    )

    resultados = dados.get("results", [])
    if not resultados:
        raise ValueError(f"Geocoding n?o encontrou: {cidade} - {uf}")

    estado = UF_PARA_ESTADO.get(uf)

    # Primeiro tentamos o resultado mais confi?vel: mesmo pa?s e mesmo estado.
    for local in resultados:
        if local.get("country_code") == "BR" and local.get("admin1") == estado:
            return local["latitude"], local["longitude"]

    # Fallback: se o nome do estado vier diferente, usamos o primeiro resultado do Brasil.
    for local in resultados:
        if local.get("country_code") == "BR":
            return local["latitude"], local["longitude"]

    raise ValueError(f"Geocoding n?o encontrou no Brasil: {cidade} - {uf}")


# Teste da fun??o de geocodifica??o.
lat, lon = fetch_geocoding("Porto Alegre", "RS")
print(f"Porto Alegre -> lat={lat}, lon={lon}")

# ----------------------------------------------------------------------
# 1.3 API Open-Meteo Archive — Dados Climáticos Históricos de 2024
# 
# Endpoint: `https://archive-api.open-meteo.com/v1/archive`
# Coleta temperatura máxima, mínima e precipitação diária para o ano todo.

def fetch_clima(lat: float, lon: float, ano: int = 2024) -> pd.DataFrame:
    """
    Coleta dados clim?ticos di?rios no Open-Meteo Archive.

    Retorna um DataFrame com:
    - time: data da medi??o;
    - temperature_2m_max: temperatura m?xima di?ria;
    - temperature_2m_min: temperatura m?nima di?ria;
    - precipitation_sum: precipita??o total di?ria.
    """
    dados = _get_json(
        URL_ARCHIVE,
        params={
            "latitude":   lat,
            "longitude":  lon,
            "start_date": f"{ano}-01-01",
            "end_date":   f"{ano}-12-31",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "America/Sao_Paulo",
        },
        timeout=20,
    )

    # A chave "daily" cont?m listas paralelas: uma lista de datas, uma de m?ximas etc.
    # O pandas transforma isso facilmente em uma tabela.
    return pd.DataFrame(dados["daily"])


# Teste: 2024 ? ano bissexto, ent?o esperamos 366 registros.
df_teste = fetch_clima(-30.03, -51.23)
print(f"Registros retornados: {len(df_teste)}")
df_teste.head(3)

# ----------------------------------------------------------------------
# 1.4 API IBGE — População do Município (Censo 2022)
# 
# Usa o código IBGE retornado pelo ViaCEP para buscar a população na API de Agregados do IBGE.
# Agregado `4709` (Sinopse do Censo 2022), Variável `93` = população residente, período `2022`.

def fetch_populacao(ibge_code: str) -> int | None:
    """
    Busca a popula??o residente do munic?pio no Censo 2022 pela API do IBGE.

    O c?digo IBGE vem da API ViaCEP. A consulta usa:
    - agregado 4709: Sinopse do Censo Demogr?fico 2022;
    - vari?vel 93: popula??o residente;
    - localidade N6: munic?pio.
    """
    params = {"localidades": f"N6[{ibge_code}]"}

    try:
        dados = _get_json(URL_IBGE_POPULACAO, params=params, timeout=15)
        serie = dados[0]["resultados"][0]["series"][0]["serie"]
        return int(serie["2022"])

    except (KeyError, IndexError, ValueError, RuntimeError) as exc:
        # A an?lise clim?tica continua mesmo que a popula??o esteja indispon?vel.
        print(f"  [aviso] fetch_populacao({ibge_code}) falhou: {type(exc).__name__}: {exc}")
        return None


# Teste: c?digo IBGE de Porto Alegre = 4314902.
pop = fetch_populacao("4314902")
if pop is not None:
    print(f"Popula??o de Porto Alegre (Censo 2022): {pop:,}")
else:
    print("Popula??o de Porto Alegre: dado indispon?vel")

# ----------------------------------------------------------------------
# ---
# 2. Pipeline Completo + Tratamento dos Dados
# 
# A função `processar_cep` orquestra as 4 chamadas de API e aplica o tratamento:
# - Conversão de datas
# - Remoção de nulos
# - Cálculo da amplitude térmica (max − min)
# - Extração da coluna mês

def processar_cep(label: str, cep: str) -> dict:
    """
    Executa o pipeline completo para um CEP.

    Esta fun??o ? o cora??o do projeto. Ela combina as quatro APIs:
    1. ViaCEP -> cidade, UF e c?digo IBGE;
    2. Open-Meteo Geocoding -> latitude e longitude;
    3. Open-Meteo Archive -> clima di?rio de 2024;
    4. IBGE -> popula??o do munic?pio.

    Retorna um dicion?rio com:
    - info: dados resumidos da cidade;
    - df_diario: dados clim?ticos tratados por dia;
    - df_mensal: resumo mensal para an?lise e gr?ficos.
    """
    print(f"\n{'=' * 55}\n  {label} | CEP: {cep}\n{'=' * 55}")

    print("  [1/4] Consultando ViaCEP...", end=" ")
    info = fetch_viacep(cep)
    print(f"OK -> {info['cidade']} / {info['uf']}")

    print("  [2/4] Geocodificando...", end=" ")
    info["lat"], info["lon"] = fetch_geocoding(info["cidade"], info["uf"])
    print(f"OK -> lat={info['lat']:.4f}, lon={info['lon']:.4f}")

    print("  [3/4] Coletando clima 2024...", end=" ")
    df = fetch_clima(info["lat"], info["lon"])
    print(f"OK -> {len(df)} dias coletados")

    print("  [4/4] Buscando popula??o (IBGE)...", end=" ")
    info["populacao"] = fetch_populacao(info["ibge"])
    print(f"OK -> {info['populacao']:,}" if info["populacao"] else "OK -> dado indispon?vel")

    # -----------------------------
    # Tratamento dos dados di?rios
    # -----------------------------
    df["time"] = pd.to_datetime(df["time"])

    # Remove linhas sem temperatura, pois elas prejudicam m?dias e extremos.
    df = df.dropna(subset=["temperature_2m_max", "temperature_2m_min"]).copy()

    # Se a precipita??o vier vazia, consideramos 0 mm para manter a soma anual.
    df["precipitation_sum"] = df["precipitation_sum"].fillna(0)

    # Amplitude t?rmica: diferen?a entre m?xima e m?nima do mesmo dia.
    df["amplitude_termica"] = df["temperature_2m_max"] - df["temperature_2m_min"]

    # Periodo mensal facilita agrupamentos por m?s.
    df["mes"] = df["time"].dt.to_period("M")
    df["cidade"] = info["cidade"]

    # -----------------------------
    # Resumo mensal
    # -----------------------------
    df_mensal = (
        df.groupby("mes")
        .agg(
            temp_max_media=("temperature_2m_max", "mean"),
            temp_min_media=("temperature_2m_min", "mean"),
            amplitude_media=("amplitude_termica", "mean"),
            precipitacao_total=("precipitation_sum", "sum"),
        )
        .round(1)
        .reset_index()
    )

    # R?tulos curtos para o eixo dos gr?ficos.
    df_mensal["mes_str"] = df_mensal["mes"].dt.strftime("%b")

    # -----------------------------
    # Indicadores anuais para relat?rio
    # -----------------------------
    info["mes_quente"] = df_mensal.loc[df_mensal["temp_max_media"].idxmax(), "mes_str"]
    info["mes_chuvoso"] = df_mensal.loc[df_mensal["precipitacao_total"].idxmax(), "mes_str"]
    info["temp_max_anual"] = df["temperature_2m_max"].max()
    info["temp_min_anual"] = df["temperature_2m_min"].min()
    info["precip_anual"] = df["precipitation_sum"].sum()
    info["label"] = label

    print(f"  -> M?s mais quente: {info['mes_quente']} | M?s mais chuvoso: {info['mes_chuvoso']}")
    return {"info": info, "df_diario": df, "df_mensal": df_mensal}

# ----------------------------------------------------------------------
# ---
# 3. Execução — Coletando dados para todas as cidades
# 
# > ⏳ Esta célula faz chamadas reais às APIs. Aguarde alguns segundos por cidade.

# Lista que vai armazenar o resultado de cada cidade processada.
resultados = []

for label, cep in CEPS.items():
    try:
        resultado = processar_cep(label, cep)
        resultados.append(resultado)

    except Exception as exc:
        # O erro de uma cidade n?o interrompe o projeto inteiro.
        # Isso ? ?til quando trabalhamos com v?rias APIs externas.
        print(f"  ERRO ao processar {label}: {exc}")

print(f"\nCidades processadas com sucesso: {len(resultados)}")

# ----------------------------------------------------------------------
# ---
# 4. Relatório Comparativo

# Monta uma tabela resumida, uma linha por cidade/base log?stica.
linhas = []

for r in resultados:
    i = r["info"]
    linhas.append({
        "Cidade / Base":      i["label"],
        "UF":                 i["uf"],
        "Popula??o":          f"{i['populacao']:,}" if i["populacao"] else "N/D",
        "Temp. M?x. (?C)":    f"{i['temp_max_anual']:.1f}",
        "Temp. M?n. (?C)":    f"{i['temp_min_anual']:.1f}",
        "Precip. Anual (mm)": f"{i['precip_anual']:.0f}",
        "M?s Mais Quente":    i["mes_quente"],
        "M?s Mais Chuvoso":   i["mes_chuvoso"],
    })

df_relatorio = pd.DataFrame(linhas)
df_relatorio

print("INSIGHTS OPERACIONAIS - EMPRESA LOG?STICA HIPOT?TICA\n" + "=" * 55)

for r in resultados:
    i = r["info"]
    print(f"\n{i['label']}:")

    alertou = False

    # Regra 1: chuva anual muito alta tende a aumentar risco de atraso.
    if i["precip_anual"] > 1800:
        print(f"  Alta pluviosidade ({i['precip_anual']:.0f} mm): risco elevado de atrasos em rotas externas.")
        alertou = True

    # Regra 2: temperatura extrema pode exigir cuidados com carga e equipes.
    if i["temp_max_anual"] > 38:
        print(f"  Temperatura m?xima extrema ({i['temp_max_anual']:.1f}?C): aten??o a cargas sens?veis e cadeia fria.")
        alertou = True

    # Regra 3: pouca chuva favorece opera??es a c?u aberto, embora possa trazer outros riscos.
    if i["precip_anual"] < 800:
        print(f"  Baixa precipita??o ({i['precip_anual']:.0f} mm): condi??es favor?veis para opera??es externas.")
        alertou = True

    if not alertou:
        print("  Condi??es clim?ticas moderadas: opera??es sem restri??es especiais.")

# ----------------------------------------------------------------------
# Painel de Gráficos — Temperatura e Precipitação Mensal

n = len(resultados)

# Uma linha de gr?ficos por cidade e duas colunas: temperatura e precipita??o.
fig = plt.figure(figsize=(18, 5 * n))
gs = GridSpec(n, 2, figure=fig, hspace=0.55, wspace=0.35)

fig.suptitle(
    "An?lise Clim?tica 2024 - Bases de Log?stica no Brasil\n"
    "(Projeto 10 v2 | APE - IA para Engenheiros / UFRGS)",
    fontsize=14,
    fontweight="bold",
    y=1.01,
)

cores = plt.cm.tab10.colors

# Escalas globais deixam a compara??o entre cidades mais honesta.
temp_min_global = min(r["df_mensal"]["temp_min_media"].min() for r in resultados)
temp_max_global = max(r["df_mensal"]["temp_max_media"].max() for r in resultados)
precip_max_global = max(r["df_mensal"]["precipitacao_total"].max() for r in resultados)

for idx, r in enumerate(resultados):
    dm = r["df_mensal"]
    inf = r["info"]
    cor = cores[idx % len(cores)]

    # -----------------------------
    # Gr?fico de temperatura
    # -----------------------------
    ax1 = fig.add_subplot(gs[idx, 0])
    ax1.fill_between(
        dm["mes_str"],
        dm["temp_min_media"],
        dm["temp_max_media"],
        alpha=0.25,
        color=cor,
        label="Faixa min-m?x",
    )
    ax1.plot(dm["mes_str"], dm["temp_max_media"], "o-", color=cor, linewidth=2, label="M?x. m?dia")
    ax1.plot(dm["mes_str"], dm["temp_min_media"], "s--", color=cor, linewidth=1.5, alpha=0.7, label="M?n. m?dia")
    ax1.set_ylim(temp_min_global - 2, temp_max_global + 2)
    ax1.set_title(f"{inf['label']}\nTemperatura Mensal (?C)", fontsize=11)
    ax1.set_ylabel("?C")
    ax1.tick_params(axis="x", rotation=45)
    ax1.legend(fontsize=8)
    ax1.grid(axis="y", alpha=0.3)

    # -----------------------------
    # Gr?fico de precipita??o
    # -----------------------------
    ax2 = fig.add_subplot(gs[idx, 1])
    barras = ax2.bar(dm["mes_str"], dm["precipitacao_total"], color=cor, alpha=0.75, edgecolor="white")
    ax2.set_ylim(0, precip_max_global * 1.1)
    ax2.set_title(f"{inf['label']}\nPrecipita??o Total Mensal (mm)", fontsize=11)
    ax2.set_ylabel("mm")
    ax2.tick_params(axis="x", rotation=45)
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f"))
    ax2.grid(axis="y", alpha=0.3)

    # R?tulos acima das barras facilitam leitura no relat?rio.
    for barra in barras:
        altura = barra.get_height()
        if altura > 0:
            ax2.text(
                barra.get_x() + barra.get_width() / 2,
                altura + 1,
                f"{altura:.0f}",
                ha="center",
                va="bottom",
                fontsize=7,
            )

plt.savefig("clima_logistica_2024_v2.png", dpi=150, bbox_inches="tight")
plt.show()
print("Gr?fico salvo como clima_logistica_2024_v2.png")

# ----------------------------------------------------------------------
# Exportar CSV consolidado com dados diários

# Junta os dados di?rios de todas as cidades em uma ?nica tabela.
df_total = pd.concat(
    [
        r["df_diario"][[
            "time",
            "cidade",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "amplitude_termica",
            "mes",
        ]]
        for r in resultados
    ],
    ignore_index=True,
)

# utf-8-sig ajuda o Excel em portugu?s a abrir acentos corretamente.
df_total.to_csv("dados_climaticos_2024_v2.csv", index=False, encoding="utf-8-sig")

print(f"CSV salvo: {len(df_total)} linhas | {df_total['cidade'].nunique()} cidades")
df_total.head()
