"""
Tarefa para Casa - Lab02Tarefa03

Objetivo:
- gerar uma base artificial do tipo blobs;
- treinar k-means com diferentes valores de k;
- observar a Soma dos Quadrados Dentro dos Clusters (WCSS);
- escolher o k otimo pela Curva do Cotovelo;
- treinar o modelo final e avaliar o agrupamento encontrado.

Este script foi organizado e comentado com base no enunciado do Lab02.pdf e no
codigo do arquivo Lab02Tarefa03.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score, silhouette_score


BASE_DIR = Path(__file__).resolve().parent
GRAFICO_BLOBS = BASE_DIR / "Lab02Tarefa03_01_blobs_originais.png"
GRAFICO_COTOVELO = BASE_DIR / "Lab02Tarefa03_02_curva_cotovelo.png"
GRAFICO_COMPARACAO = BASE_DIR / "Lab02Tarefa03_03_kmeans_vs_original.png"
ARQUIVO_WCSS = BASE_DIR / "Lab02Tarefa03_wcss.csv"

RANDOM_STATE = 150
N_AMOSTRAS = 200
N_VARIAVEIS = 2
CENTROS_ORIGINAIS = 5
DESVIO_CLUSTER = 1
K_MIN = 1
K_MAX = 10
K_OTIMO = 5


def gerar_dados_blobs() -> tuple:
    """Cria a base artificial usada na tarefa."""
    dados, rotulos_originais = make_blobs(
        n_samples=N_AMOSTRAS,
        n_features=N_VARIAVEIS,
        centers=CENTROS_ORIGINAIS,
        cluster_std=DESVIO_CLUSTER,
        random_state=RANDOM_STATE,
    )
    return dados, rotulos_originais


def salvar_grafico_blobs(dados, rotulos_originais) -> None:
    """Mostra os blobs originais, coloridos pelos rotulos gerados pela base."""
    plt.figure(figsize=(8, 6))
    plt.scatter(dados[:, 0], dados[:, 1], c=rotulos_originais, cmap="rainbow")
    plt.title("Blobs Originais")
    plt.xlabel("Variavel 1")
    plt.ylabel("Variavel 2")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(GRAFICO_BLOBS, dpi=150)
    plt.show()


def calcular_wcss(dados) -> list[float]:
    """
    Treina k-means com varios valores de k e guarda o WCSS.

    No scikit-learn, o WCSS fica disponivel em `inertia_`.
    Quanto maior o k, menor tende a ser o WCSS. O ponto de interesse e onde a
    reducao deixa de ser tao acentuada, formando o "cotovelo".
    """
    valores_wcss = []

    for k in range(K_MIN, K_MAX + 1):
        modelo = KMeans(
            n_clusters=k,
            init="k-means++",
            random_state=RANDOM_STATE,
            n_init=10,
        )
        modelo.fit(dados)
        valores_wcss.append(modelo.inertia_)

    return valores_wcss


def salvar_curva_cotovelo(valores_wcss: list[float]) -> None:
    """Salva a Curva do Cotovelo e a tabela de WCSS."""
    valores_k = list(range(K_MIN, K_MAX + 1))
    tabela_wcss = pd.DataFrame({"k": valores_k, "WCSS": valores_wcss})
    tabela_wcss.to_csv(ARQUIVO_WCSS, index=False)

    plt.figure(figsize=(8, 6))
    plt.plot(valores_k, valores_wcss, marker="o", color="black")
    plt.axvline(K_OTIMO, color="red", linestyle="--", label=f"k otimo = {K_OTIMO}")
    plt.title("Curva do Cotovelo do Algoritmo k-means")
    plt.xlabel("Numero de Clusters (k)")
    plt.ylabel("Soma dos Quadrados Dentro dos Clusters (WCSS)")
    plt.xticks(valores_k)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAFICO_COTOVELO, dpi=150)
    plt.show()

    print("\nValores de WCSS:")
    print(tabela_wcss.to_string(index=False))


def treinar_modelo_final(dados) -> KMeans:
    """Treina o k-means final usando o k escolhido pela Curva do Cotovelo."""
    modelo = KMeans(
        n_clusters=K_OTIMO,
        init="k-means++",
        random_state=RANDOM_STATE,
        n_init=10,
    )
    modelo.fit(dados)
    return modelo


def avaliar_modelo(dados, rotulos_originais, modelo: KMeans) -> None:
    """
    Avalia o agrupamento final.

    Silhouette Score mede separacao/coesao dos clusters. Quanto mais proximo de
    1, melhor. Adjusted Rand Index compara os clusters encontrados com os
    rotulos originais dos blobs. Quanto mais proximo de 1, maior a concordancia.
    """
    silhouette = silhouette_score(dados, modelo.labels_)
    ari = adjusted_rand_score(rotulos_originais, modelo.labels_)

    print("\nAvaliacao do modelo final:")
    print(f"k escolhido: {K_OTIMO}")
    print(f"WCSS final: {modelo.inertia_:.2f}")
    print(f"Silhouette Score: {silhouette:.4f}")
    print(f"Adjusted Rand Index: {ari:.4f}")
    print("\nCentroides encontrados:")
    print(pd.DataFrame(modelo.cluster_centers_, columns=["Variavel 1", "Variavel 2"]))


def salvar_comparacao_clusters(dados, rotulos_originais, modelo: KMeans) -> None:
    """Compara visualmente os clusters encontrados com os blobs originais."""
    figura, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12, 6))

    ax1.set_title("K-means")
    ax1.scatter(dados[:, 0], dados[:, 1], c=modelo.labels_, cmap="rainbow")
    ax1.scatter(
        modelo.cluster_centers_[:, 0],
        modelo.cluster_centers_[:, 1],
        marker="X",
        s=250,
        color="black",
        label="Centroides",
    )
    ax1.set_xlabel("Variavel 1")
    ax1.set_ylabel("Variavel 2")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.4)

    ax2.set_title("Original")
    ax2.scatter(dados[:, 0], dados[:, 1], c=rotulos_originais, cmap="rainbow")
    ax2.set_xlabel("Variavel 1")
    ax2.grid(True, linestyle="--", alpha=0.4)

    figura.suptitle("Comparacao entre agrupamento k-means e blobs originais")
    figura.tight_layout()
    figura.savefig(GRAFICO_COMPARACAO, dpi=150)
    plt.show()


def main() -> None:
    dados, rotulos_originais = gerar_dados_blobs()

    salvar_grafico_blobs(dados, rotulos_originais)

    valores_wcss = calcular_wcss(dados)
    salvar_curva_cotovelo(valores_wcss)

    modelo_final = treinar_modelo_final(dados)
    avaliar_modelo(dados, rotulos_originais, modelo_final)
    salvar_comparacao_clusters(dados, rotulos_originais, modelo_final)

    print("\nArquivos gerados:")
    print(f"- {GRAFICO_BLOBS}")
    print(f"- {GRAFICO_COTOVELO}")
    print(f"- {GRAFICO_COMPARACAO}")
    print(f"- {ARQUIVO_WCSS}")


if __name__ == "__main__":
    main()
