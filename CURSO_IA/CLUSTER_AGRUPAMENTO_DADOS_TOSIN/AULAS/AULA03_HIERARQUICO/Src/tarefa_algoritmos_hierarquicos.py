"""
============================================================
LAB03 - Tarefa - Algoritmos Hierarquicos
Comparacao dos metodos: single, complete e ward
Determinacao do numero de clusters pelo metodo de Mojena
============================================================

Este script segue o estilo dos exemplos em Notebooks/.

Ele foi escrito de forma bem comentada para facilitar o estudo:
1. leitura da base DadosWH.csv;
2. filtro dos dados do ano de 2019;
3. selecao das variaveis usadas no agrupamento;
4. normalizacao min-max;
5. calculo da matriz de dissimilaridade;
6. aplicacao dos metodos single, complete e ward;
7. escolha do numero de clusters pelo metodo de Mojena;
8. comparacao dos resultados.
"""


# ------------------------------------------------------------
# 1. Importacao das bibliotecas
# ------------------------------------------------------------

# Path ajuda a montar caminhos de arquivos de forma mais segura.
from pathlib import Path

# Matplotlib e usado para gerar os graficos.
import matplotlib

# Numpy e usado para calculos numericos, como media e desvio padrao.
import numpy as np

# Pandas e usado para ler CSV e trabalhar com tabelas.
import pandas as pd

# linkage cria a estrutura do agrupamento hierarquico.
# dendrogram desenha o dendrograma.
# fcluster transforma o dendrograma em grupos numerados.
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage

# pdist calcula distancias entre observacoes.
# squareform transforma as distancias em matriz quadrada.
from scipy.spatial.distance import pdist, squareform


# Usa um modo de grafico que salva imagens sem abrir janela na tela.
matplotlib.use("Agg")

# pyplot e importado depois de escolher o backend do matplotlib.
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 2. Definicao dos caminhos e parametros da tarefa para Python. (Notebook é diferente)
# # ------------------------------------------------------------

# __file__ representa este arquivo .py.
# parents[1] sobe duas pastas: Src -> AULA03.
PASTA_AULA03 = Path(__file__).resolve().parents[1]

# Caminho da base de dados usada na tarefa.
CAMINHO_DADOS = PASTA_AULA03 / "Dados" / "DadosWH.csv"

# Pasta onde serao salvos os resultados gerados pelo script.
PASTA_RESULTADOS = PASTA_AULA03 / "Resultados"

# Cria a pasta de resultados caso ela ainda nao exista.
PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

# Ano usado na analise, seguindo o exemplo do Lab03Tarefa04.
ANO_ANALISE = 2019

# Variaveis escolhidas para formar os agrupamentos.
DIMENSOES = ["Life_Ladder", "Perceptions_of_corruption"]

# Metodos hierarquicos pedidos no roteiro.
# single = vizinho mais proximo.
# complete = vizinho mais distante.
# ward = metodo usado na tarefa IV para comparacao.
METODOS = ["single", "complete", "ward"]

# Constante usada na regra de Mojena.
# Valores comuns ficam entre 1.25 e 1.50.
C_MOJENA = 1.25


# ------------------------------------------------------------
# 3. Leitura da base de dados
# ------------------------------------------------------------

# Le o arquivo CSV e armazena o conteudo em um DataFrame chamado dados.
dados = pd.read_csv(CAMINHO_DADOS)

# Mostra as primeiras linhas para conferir se a leitura funcionou.
print("Primeiras linhas da base:")
print(dados.head())

# Mostra os nomes das colunas disponiveis.
print("\nColunas da base:")
print(dados.columns.tolist())

# Mostra a quantidade de linhas e colunas da base original.
print("\nDimensao da base original:")
print(dados.shape)


# ------------------------------------------------------------
# 4. Preparacao dos dados
# ------------------------------------------------------------

# Filtra somente as linhas referentes ao ano de 2019.
dados2019 = dados[dados["year"] == ANO_ANALISE].copy()

# Mostra a dimensao da base depois do filtro.
print(f"\nDimensao da base filtrada para {ANO_ANALISE}:")
print(dados2019.shape)

# Lista as colunas que serao usadas ou verificadas.
colunas_usadas = ["Name", "year"] + DIMENSOES

# Verifica se existem valores faltantes nas colunas importantes.
print("\nValores faltantes nas colunas usadas:")
print(dados2019[colunas_usadas].isna().sum())

# Remove linhas com valores faltantes nas dimensoes numericas.
# Assim evitamos erro no calculo das distancias.
dados2019 = dados2019.dropna(subset=DIMENSOES).copy()

# Seleciona somente as duas dimensoes numericas usadas no agrupamento.
Xs = dados2019[DIMENSOES].copy()

# Normaliza os dados pela regra min-max.
# O menor valor vira 0 e o maior valor vira 1.
Xs = (Xs - Xs.min()) / (Xs.max() - Xs.min())

# Usa o nome do pais como indice da matriz Xs.
Xs.index = dados2019["Name"]

# Mostra as primeiras linhas da matriz normalizada.
print("\nPrimeiras linhas da matriz Xs normalizada:")
print(Xs.head())


# ------------------------------------------------------------
# 5. Matriz de dissimilaridade
# ------------------------------------------------------------

# Calcula a distancia euclidiana entre todos os pares de paises.
distancias = pdist(Xs, metric="euclidean")

# Transforma o vetor de distancias em uma matriz quadrada.
matriz_distancias = squareform(distancias)

# Cria uma tabela com nomes dos paises nas linhas e nas colunas.
matriz_dissimilaridade = pd.DataFrame(
    matriz_distancias,
    index=Xs.index,
    columns=Xs.index,
)

# Define o caminho onde a matriz de dissimilaridade sera salva.
caminho_matriz = PASTA_RESULTADOS / "matriz_dissimilaridade.csv"

# Salva a matriz em CSV para consulta posterior.
matriz_dissimilaridade.to_csv(caminho_matriz, encoding="utf-8")

# Mostra uma pequena parte da matriz para conferencia.
print("\nPrimeiras linhas da matriz de dissimilaridade:")
print(matriz_dissimilaridade.head())


# ------------------------------------------------------------
# 6. Funcao para aplicar o metodo de Mojena
# ------------------------------------------------------------

def mojena_num_clusters(Z, c=C_MOJENA):
    """
    Estima o numero ideal de clusters pelo metodo de Mojena.

    Parametros:
    Z -> matriz linkage gerada pelo scipy
    c -> constante da regra de Mojena

    Retorna:
    k_otimo -> numero estimado de clusters
    corte -> distancia de corte calculada pelo metodo
    indice_salto -> posicao da primeira fusao considerada grande
    """

    # A terceira coluna de Z guarda as distancias de fusao dos clusters.
    distancias_fusao = Z[:, 2]

    # Calcula a media das distancias de fusao.
    media = np.mean(distancias_fusao)

    # Calcula o desvio padrao das distancias de fusao.
    desvio = np.std(distancias_fusao)

    # Regra de Mojena: media + c vezes o desvio padrao.
    corte = media + c * desvio

    # O numero inicial de grupos e igual ao numero de observacoes.
    numero_observacoes = Z.shape[0] + 1

    # Percorre as distancias procurando a primeira que passa do corte.
    for indice_salto, distancia in enumerate(distancias_fusao):
        # Quando a distancia passa do corte, encontramos uma quebra importante.
        if distancia > corte:
            # Antes dessa fusao acontecer, havia numero_observacoes - indice_salto grupos.
            k_otimo = numero_observacoes - indice_salto

            # Retorna o numero de clusters e informacoes auxiliares.
            return k_otimo, corte, indice_salto

    # Caso nenhuma distancia passe do corte, retorna 1 cluster.
    return 1, corte, len(distancias_fusao) - 1


# ------------------------------------------------------------
# 7. Funcao para gerar o dendrograma
# ------------------------------------------------------------

def plotar_dendrograma(Z, labels, metodo):
    """Gera e salva o dendrograma de um metodo."""

    # Define o caminho do arquivo de saida.
    caminho_grafico = PASTA_RESULTADOS / f"dendrograma_{metodo}.png"

    # Cria uma figura grande para caberem os nomes dos paises.
    plt.figure(figsize=(22, 10))

    # Cria o dendrograma com os nomes dos paises.
    dendrogram(
        Z,
        labels=labels,
        leaf_rotation=90,
        leaf_font_size=7,
    )

    # Define o titulo do grafico.
    plt.title(f"Dendrograma - Metodo {metodo}", fontsize=16)

    # Define o nome do eixo x.
    plt.xlabel("Paises", fontsize=12)

    # Define o nome do eixo y.
    plt.ylabel("Distancia", fontsize=12)

    # Ajusta os espacamentos do grafico.
    plt.tight_layout()

    # Salva o grafico em arquivo PNG.
    plt.savefig(caminho_grafico, dpi=150)

    # Fecha o grafico para liberar memoria.
    plt.close()

    # Retorna o caminho do grafico salvo.
    return caminho_grafico


# ------------------------------------------------------------
# 8. Funcao para gerar grafico dos clusters
# ------------------------------------------------------------

def plotar_clusters(X, rotulos, metodo):
    """Gera e salva um grafico de dispersao com os clusters."""

    # Define o caminho do arquivo de saida.
    caminho_grafico = PASTA_RESULTADOS / f"clusters_{metodo}.png"

    # Cria a figura do grafico.
    plt.figure(figsize=(14, 9))

    # Plota os paises como pontos coloridos pelo cluster.
    plt.scatter(
        X["Life_Ladder"],
        X["Perceptions_of_corruption"],
        c=rotulos,
        cmap="viridis",
        marker="o",
        edgecolor="black",
        linewidth=0.3,
    )

    # Percorre cada pais para escrever o nome dele no grafico.
    for nome_pais, linha in X.iterrows():
        # Escreve o nome do pais ao lado do ponto.
        plt.annotate(
            nome_pais,
            (linha["Life_Ladder"], linha["Perceptions_of_corruption"]),
            fontsize=6,
            alpha=0.75,
        )

    # Define o titulo do grafico.
    plt.title(f"Agrupamento Hierarquico - Metodo {metodo}", fontsize=15)

    # Define o nome do eixo x.
    plt.xlabel("Qualidade de vida normalizada")

    # Define o nome do eixo y.
    plt.ylabel("Percepcao de corrupcao normalizada")

    # Adiciona uma grade leve para facilitar a leitura.
    plt.grid(True, linestyle="--", alpha=0.3)

    # Ajusta os espacamentos do grafico.
    plt.tight_layout()

    # Salva o grafico em arquivo PNG.
    plt.savefig(caminho_grafico, dpi=150)

    # Fecha o grafico para liberar memoria.
    plt.close()

    # Retorna o caminho do grafico salvo.
    return caminho_grafico


# ------------------------------------------------------------
# 9. Funcao para analisar um metodo hierarquico
# ------------------------------------------------------------

def analisar_metodo(X, metodo):
    """Aplica um metodo hierarquico e devolve um resumo dos resultados."""

    # Mostra uma separacao visual no terminal.
    print("\n" + "=" * 60)

    # Mostra o nome do metodo atual.
    print(f"METODO: {metodo.upper()}")

    # Mostra outra linha de separacao.
    print("=" * 60)

    # Cria a matriz linkage pelo metodo escolhido.
    # single: une grupos pela menor distancia entre pontos.
    # complete: une grupos pela maior distancia entre pontos.
    # ward: une grupos tentando reduzir a variacao interna dos grupos.
    Z = linkage(X, method=metodo, metric="euclidean")

    # Aplica o metodo de Mojena para escolher o numero de clusters.
    k_otimo, corte, indice_salto = mojena_num_clusters(Z, c=C_MOJENA)

    # Mostra o numero de clusters encontrado.
    print(f"Numero ideal de clusters pelo metodo de Mojena: {k_otimo}")

    # Mostra a distancia de corte calculada.
    print(f"Distancia de corte de Mojena: {corte:.6f}")

    # Gera os rotulos dos clusters para cada pais.
    rotulos = fcluster(Z, t=k_otimo, criterion="maxclust")

    # Conta quantos paises ficaram em cada cluster.
    tamanho_clusters = pd.Series(rotulos).value_counts().sort_index()

    # Mostra o tamanho de cada cluster.
    print("\nQuantidade de paises por cluster:")
    print(tamanho_clusters)

    # Gera e salva o dendrograma.
    caminho_dendrograma = plotar_dendrograma(Z, X.index.tolist(), metodo)

    # Gera e salva o grafico dos clusters.
    caminho_clusters = plotar_clusters(X, rotulos, metodo)

    # Monta uma tabela relacionando pais e cluster.
    tabela_clusters = pd.DataFrame(
        {
            "Name": X.index,
            f"cluster_{metodo}": rotulos,
        }
    )

    # Retorna um dicionario com os principais resultados.
    return {
        "metodo": metodo,
        "Z": Z,
        "k_otimo": k_otimo,
        "corte": corte,
        "indice_salto": indice_salto,
        "rotulos": rotulos,
        "tamanho_clusters": tamanho_clusters.to_dict(),
        "tabela_clusters": tabela_clusters,
        "dendrograma": caminho_dendrograma,
        "grafico_clusters": caminho_clusters,
    }


# ------------------------------------------------------------
# 10. Execucao dos metodos single, complete e ward
# ------------------------------------------------------------

# Cria uma lista vazia para guardar os resultados dos tres metodos.
resultados = []

# Percorre cada metodo definido na lista METODOS.
for metodo in METODOS:
    # Executa a analise para o metodo atual.
    resultado = analisar_metodo(Xs, metodo)

    # Guarda o resultado na lista geral.
    resultados.append(resultado)


# ------------------------------------------------------------
# 11. Tabela com os clusters de cada pais
# ------------------------------------------------------------

# Comeca a tabela com uma coluna contendo o nome dos paises.
clusters_por_pais = pd.DataFrame({"Name": Xs.index})

# Adiciona na tabela uma coluna para cada metodo.
for resultado in resultados:
    # Recupera o nome do metodo atual.
    metodo = resultado["metodo"]

    # Cria uma coluna com os rotulos encontrados pelo metodo.
    clusters_por_pais[f"cluster_{metodo}"] = resultado["rotulos"]

# Define o caminho do arquivo CSV.
caminho_clusters_por_pais = PASTA_RESULTADOS / "clusters_por_pais.csv"

# Salva a tabela em CSV.
clusters_por_pais.to_csv(caminho_clusters_por_pais, index=False, encoding="utf-8")

# Mostra as primeiras linhas da tabela.
print("\nPrimeiras linhas da tabela de clusters por pais:")
print(clusters_por_pais.head())


# ------------------------------------------------------------
# 12. Tabela-resumo da comparacao dos metodos
# ------------------------------------------------------------

# Cria uma tabela comparando os tres metodos.
comparacao = pd.DataFrame(
    {
        "Metodo": [resultado["metodo"] for resultado in resultados],
        "Numero otimo de clusters (Mojena)": [resultado["k_otimo"] for resultado in resultados],
        "Distancia de corte": [round(resultado["corte"], 6) for resultado in resultados],
        "Indice do salto": [resultado["indice_salto"] for resultado in resultados],
        "Tamanho dos clusters": [resultado["tamanho_clusters"] for resultado in resultados],
        "Dendrograma": [str(resultado["dendrograma"]) for resultado in resultados],
        "Grafico dos clusters": [str(resultado["grafico_clusters"]) for resultado in resultados],
    }
)

# Define o caminho do arquivo CSV.
caminho_comparacao = PASTA_RESULTADOS / "comparacao_metodos_hierarquicos.csv"

# Salva a tabela de comparacao em CSV.
comparacao.to_csv(caminho_comparacao, index=False, encoding="utf-8")

# Mostra a tabela de comparacao no terminal.
print("\nTabela-resumo da comparacao:")
print(comparacao)


# ------------------------------------------------------------
# 13. Interpretacao simples dos resultados
# ------------------------------------------------------------

# Recupera o numero de clusters do metodo single.
k_single = comparacao.loc[comparacao["Metodo"] == "single", "Numero otimo de clusters (Mojena)"].iloc[0]

# Recupera o numero de clusters do metodo complete.
k_complete = comparacao.loc[comparacao["Metodo"] == "complete", "Numero otimo de clusters (Mojena)"].iloc[0]

# Recupera o numero de clusters do metodo ward.
k_ward = comparacao.loc[comparacao["Metodo"] == "ward", "Numero otimo de clusters (Mojena)"].iloc[0]

# Mostra uma interpretacao curta comparando os metodos.
print("\nInterpretacao geral:")
print(f"- O metodo single encontrou {k_single} clusters.")
print(f"- O metodo complete encontrou {k_complete} clusters.")
print(f"- O metodo ward encontrou {k_ward} clusters.")
print("- O single costuma formar cadeias e pode deixar muitos pontos em um grupo grande.")
print("- O complete costuma formar grupos mais compactos, pois considera a maior distancia entre grupos.")
print("- O ward busca grupos com menor variacao interna e serve como comparacao com a tarefa IV.")


# ------------------------------------------------------------
# 14. Arquivos gerados
# ------------------------------------------------------------

# Mostra os principais arquivos gerados pelo script.
print("\nArquivos salvos:")
print(f"Matriz de dissimilaridade: {caminho_matriz}")
print(f"Clusters por pais: {caminho_clusters_por_pais}")
print(f"Comparacao dos metodos: {caminho_comparacao}")
