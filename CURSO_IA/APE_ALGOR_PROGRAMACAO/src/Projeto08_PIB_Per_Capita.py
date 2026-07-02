# %% [markdown]
# # Projeto 08 - Calculo do PIB per capita
#
# Objetivo:
#
# - Ler o arquivo `DADOS/pib.csv`.
# - Ler o arquivo `DADOS/pop.csv`.
# - Cruzar os paises dos dois arquivos.
# - Calcular o PIB per capita.
# - Criar uma estrutura em memoria indexada pelo nome do pais.
# - Gerar um CSV com pais e PIB per capita.
# - Gerar um CSV com paises que nao aparecem em uma das listas.
# - Gerar um JSON com todos os dados estruturados.
# - Exibir metricas simples estudadas em aula:
#   - total de paises processados;
#   - media;
#   - mediana;
#   - menor valor;
#   - maior valor;
#   - amplitude;
#   - Top 10 maiores PIB per capita.
#
# Formula:
#
#     PIB per capita = PIB / populacao
#
# No arquivo `pib.csv`, os valores de PIB estao em milhoes de dolares.
# Por isso, antes de dividir pela populacao, multiplicamos o PIB por 1.000.000.

# %%
import csv
import json
from pathlib import Path
from statistics import mean, median


# %%
PASTA_ATUAL = Path(__file__).resolve().parent
CAMINHO_PIB = PASTA_ATUAL / "DADOS" / "pib.csv"
CAMINHO_POP = PASTA_ATUAL / "DADOS" / "pop.csv"
CAMINHO_SAIDA = PASTA_ATUAL / "DADOS" / "pib_per_capita.csv"
CAMINHO_FALTANTES = PASTA_ATUAL / "DADOS" / "paises_dados_faltantes.csv"
CAMINHO_JSON = PASTA_ATUAL / "DADOS" / "pib_per_capita_estrutura.json"

FONTE_PIB_ESCOLHIDA = "IMF (2026)"
FONTE_POP_ESCOLHIDA = "Population"


# Alguns paises/territorios aparecem com nomes diferentes nos dois arquivos.
# Este dicionario padroniza os nomes do arquivo pop.csv para o nome usado no pib.csv.
# Crie esse dicionario pois a minha dificuldade esta sendo a sintaxe, lembrar dos comandos.
#  essa pratica somnete com uso e treino.
ALIASES_POPULACAO = {
    "American Samoa (US)": "American Samoa",
    "Anguilla (UK)": "Anguilla",
    "Aruba (Netherlands)": "Aruba",
    "Bermuda (UK)": "Bermuda",
    "British Virgin Islands (UK)": "British Virgin Islands",
    "Cayman Islands (UK)": "Cayman Islands",
    "Cook Islands (New Zealand)": "Cook Islands",
    "Curaçao (Netherlands)": "Curaçao",
    "Czechia": "Czech Republic",
    "Democratic Republic of the Congo": "DR Congo",
    "Faroe Islands (Denmark)": "Faroe Islands",
    "French Polynesia (France)": "French Polynesia",
    "Greenland (Denmark)": "Greenland",
    "Guam (US)": "Guam",
    "Hong Kong (China)": "Hong Kong",
    "Isle of Man (UK)": "Isle of Man",
    "Macau (China)": "Macau",
    "Micronesia": "Federated States of Micronesia",
    "Montserrat (UK)": "Montserrat",
    "New Caledonia (France)": "New Caledonia",
    "Northern Mariana Islands (US)": "Northern Mariana Islands",
    "Puerto Rico (US)": "Puerto Rico",
    "Saint Martin (France)": "Saint Martin",
    "Sint Maarten (Netherlands)": "Sint Maarten",
    "Turks and Caicos Islands (UK)": "Turks and Caicos Islands",
    "United States Virgin Islands (US)": "U.S. Virgin Islands",
}


# %%
def limpar_numero(valor):
    """
    Converte textos numericos do CSV para float.

    Exemplos:
    - "31,821,293" vira 31821293.0
    - "62 (2023)" vira 62.0
    - "—N/a" vira None
    """
    if valor is None:
        return None

    texto = str(valor).strip()

    if texto == "" or "N/a" in texto or texto == "—":
        return None

    # Remove observacoes entre parenteses, como "62 (2023)".
    texto = texto.split(" ")[0]

    # Remove separador de milhar.
    texto = texto.replace(",", "")

    try:
        return float(texto)
    except ValueError:
        return None


def formatar_dinheiro(valor):
    """Formata um numero como dinheiro, usando duas casas decimais."""
    return f"US$ {valor:,.2f}"


# %%
def ler_pib(caminho_arquivo):
    """
    Le o CSV de PIB.

    Conforme o roteiro, adotamos apenas a primeira fonte do dado:
    IMF (2026).
    """
    dados_pib = {}

    with caminho_arquivo.open("r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            pais = linha["Country/Territory"].strip()
            pib_milhoes = limpar_numero(linha.get(FONTE_PIB_ESCOLHIDA))

            dados_pib[pais] = {
                "pais": pais,
                "pib_milhoes_usd": pib_milhoes,
                "fonte_pib": FONTE_PIB_ESCOLHIDA,
                "linha_original": linha,
            }

    return dados_pib


def ler_populacao(caminho_arquivo):
    """Le o CSV de populacao usando a primeira fonte de populacao."""
    dados_populacao = {}

    with caminho_arquivo.open("r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            local = linha["Location"].strip()
            pais_padronizado = ALIASES_POPULACAO.get(local, local)
            populacao = limpar_numero(linha.get("Population"))

            if populacao is not None:
                populacao = int(populacao)

            dados_populacao[pais_padronizado] = {
                "pais": pais_padronizado,
                "nome_original": local,
                "populacao": populacao,
                "fonte_populacao": FONTE_POP_ESCOLHIDA,
                "data_populacao": linha.get("Date", "").strip(),
                "linha_original": linha,
            }

    return dados_populacao


# %%
def criar_estrutura_indexada(dados_pib, dados_populacao):
    """
    Cria uma estrutura em memoria indexada pelo nome do pais.

    Cada chave do dicionario principal e o nome do pais.
    Cada valor guarda os dados de PIB, populacao, calculo e pendencias.
    """
    estrutura = {}
    todos_os_paises = set(dados_pib) | set(dados_populacao)

    for pais in sorted(todos_os_paises):
        item_pib = dados_pib.get(pais)
        item_populacao = dados_populacao.get(pais)
        pendencias = []

        if item_pib is None:
            pendencias.append("PIB")
        elif item_pib["pib_milhoes_usd"] is None:
            pendencias.append(f"PIB da fonte {FONTE_PIB_ESCOLHIDA}")

        if item_populacao is None:
            pendencias.append("populacao")
        elif item_populacao["populacao"] is None:
            pendencias.append("populacao numerica")

        estrutura[pais] = {
            "pais": pais,
            "pib": item_pib,
            "populacao": item_populacao,
            "pib_per_capita_usd": None,
            "pendencias": pendencias,
        }

    return estrutura


def calcular_pib_per_capita(estrutura):
    """Calcula o PIB per capita dentro da estrutura indexada."""
    resultado = []

    for pais, item in estrutura.items():
        if len(item["pendencias"]) > 0:
            continue

        item_pib = item["pib"]
        item_populacao = item["populacao"]
        pib_usd = item_pib["pib_milhoes_usd"] * 1_000_000
        populacao = item_populacao["populacao"]
        pib_per_capita = pib_usd / populacao
        item["pib_per_capita_usd"] = pib_per_capita

        resultado.append(
            {
                "pais": pais,
                "pib_per_capita_usd": pib_per_capita,
            }
        )

    resultado.sort(key=lambda linha: linha["pib_per_capita_usd"], reverse=True)
    return resultado


def calcular_metricas(resultado):
    """Calcula metricas simples para analisar o PIB per capita."""
    valores = [linha["pib_per_capita_usd"] for linha in resultado]

    return {
        "total_paises": len(resultado),
        "media": mean(valores),
        "mediana": median(valores),
        "menor": min(valores),
        "maior": max(valores),
        "amplitude": max(valores) - min(valores),
    }


# %%
def salvar_csv(resultado, caminho_saida):
    """Salva o resultado do calculo com pais e PIB per capita."""
    campos = [
        "pais",
        "pib_per_capita_usd",
    ]

    with caminho_saida.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()

        for linha in resultado:
            linha_saida = linha.copy()
            linha_saida["pib_per_capita_usd"] = round(
                linha_saida["pib_per_capita_usd"],
                2,
            )
            escritor.writerow(linha_saida)


def gerar_dados_faltantes(estrutura):
    """Gera uma lista com paises que nao possuem algum dado necessario."""
    faltantes = []

    for pais, item in estrutura.items():
        for pendencia in item["pendencias"]:
            faltantes.append(
                {
                    "pais": pais,
                    "informacao_faltante": pendencia,
                }
            )

    return faltantes


def salvar_csv_faltantes(faltantes, caminho_saida):
    """Salva um CSV com paises que nao constam em uma das listas."""
    campos = ["pais", "informacao_faltante"]

    with caminho_saida.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(faltantes)


def salvar_json(estrutura, resultado, faltantes, metricas, caminho_saida):
    """Salva todos os dados em formato estruturado JSON."""
    dados_json = {
        "fontes_adotadas": {
            "pib": FONTE_PIB_ESCOLHIDA,
            "populacao": FONTE_POP_ESCOLHIDA,
        },
        "metricas": metricas,
        "pib_per_capita": resultado,
        "dados_faltantes": faltantes,
        "estrutura_indexada_por_pais": estrutura,
    }

    with caminho_saida.open("w", encoding="utf-8") as arquivo:
        json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)


def exibir_resumo(resultado, metricas):
    """Mostra as principais metricas na tela."""
    print("Calculo do PIB per capita concluido.")
    print(f"Total de paises processados: {metricas['total_paises']}")
    print(f"Media: {formatar_dinheiro(metricas['media'])}")
    print(f"Mediana: {formatar_dinheiro(metricas['mediana'])}")
    print(f"Menor valor: {formatar_dinheiro(metricas['menor'])}")
    print(f"Maior valor: {formatar_dinheiro(metricas['maior'])}")
    print(f"Amplitude: {formatar_dinheiro(metricas['amplitude'])}")

    print("\nTop 10 maiores PIB per capita:")

    for posicao, linha in enumerate(resultado[:10], start=1):
        print(
            f"{posicao:02d}. {linha['pais']}: "
            f"{formatar_dinheiro(linha['pib_per_capita_usd'])}"
        )


# %%
def executar():
    """Executa o fluxo completo do projeto."""
    dados_pib = ler_pib(CAMINHO_PIB)
    dados_populacao = ler_populacao(CAMINHO_POP)
    estrutura = criar_estrutura_indexada(dados_pib, dados_populacao)
    resultado = calcular_pib_per_capita(estrutura)
    faltantes = gerar_dados_faltantes(estrutura)
    metricas = calcular_metricas(resultado)

    salvar_csv(resultado, CAMINHO_SAIDA)
    salvar_csv_faltantes(faltantes, CAMINHO_FALTANTES)
    salvar_json(estrutura, resultado, faltantes, metricas, CAMINHO_JSON)
    exibir_resumo(resultado, metricas)

    print(f"\nCSV de PIB per capita gerado: {CAMINHO_SAIDA}")
    print(f"CSV de dados faltantes gerado: {CAMINHO_FALTANTES}")
    print(f"JSON estruturado gerado: {CAMINHO_JSON}")


# %%
if __name__ == "__main__":
    executar()
