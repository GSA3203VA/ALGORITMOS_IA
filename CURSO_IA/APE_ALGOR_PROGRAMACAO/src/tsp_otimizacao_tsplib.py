# %%
"""
Projeto 09 - TSP com algoritmos de otimizacao

Baseado nas aulas:
- Aula 8: algoritmo guloso, Hill Climbing / busca local e Simulated Annealing.
- Aula 9: algoritmos geneticos, selecao, crossover, mutacao, populacao e fitness.

Como usar no VS Code:
1. Abra este arquivo como Python Interactive/Notebook.
2. Rode as celulas # %% em ordem.
3. Ajuste BENCHMARKS se quiser testar outras instancias da TSPLIB.
"""

# %%
# Se necessario, descomente e rode:
# %pip install tsplib95 pandas matplotlib

from __future__ import annotations

import csv
import math
import random
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import tsplib95

try:
    import pandas as pd
except ImportError:
    pd = None


# %%
# Configuracao geral

BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "tsplib_benchmarks"
RESULTS_CSV = BASE_DIR / "resultados_tsp_tsplib.csv"

TSPLIB_REPO_API = "https://api.github.com/repos/mastqe/tsplib/contents"
TSPLIB_RAW_BASE = "https://raw.githubusercontent.com/mastqe/tsplib/master"

# Instancias pequenas/medias para rodar em tempo razoavel em notebook.
# Para mais testes, adicione nomes como "att48", "eil51", "ch130", "kroB100".
BENCHMARKS = ["burma14", "berlin52", "kroA100"]

# Otimos conhecidos de algumas instancias TSPLIB. O gap so sera calculado
# quando o benchmark estiver neste dicionario.
OPTIMOS_CONHECIDOS = {
    "burma14": 3323,
    "berlin52": 7542,
    "kroA100": 21282,
    "att48": 10628,
    "eil51": 426,
    "eil76": 538,
    "eil101": 629,
    "ch130": 6110,
    "ch150": 6528,
    "kroB100": 22141,
    "kroC100": 20749,
    "kroD100": 21294,
    "kroE100": 22068,
    "lin105": 14379,
    "pr76": 108159,
}

SEMENTE = 42


# %%
# Download dos benchmarks

def listar_benchmarks_tsplib() -> list[str]:
    """Lista arquivos .tsp disponiveis no repositorio mastqe/tsplib."""
    with urllib.request.urlopen(TSPLIB_REPO_API) as response:
        import json

        itens = json.loads(response.read().decode("utf-8"))
    return sorted(item["name"] for item in itens if item["name"].endswith(".tsp"))


def baixar_benchmark(nome: str, destino: Path = DATA_DIR) -> Path:
    """Baixa uma instancia .tsp se ela ainda nao existir localmente."""
    destino.mkdir(parents=True, exist_ok=True)
    arquivo = nome if nome.endswith(".tsp") else f"{nome}.tsp"
    caminho = destino / arquivo
    if caminho.exists():
        return caminho

    url = f"{TSPLIB_RAW_BASE}/{arquivo}"
    print(f"Baixando {arquivo}...")
    urllib.request.urlretrieve(url, caminho)
    return caminho


def preparar_benchmarks(nomes: Iterable[str]) -> list[Path]:
    return [baixar_benchmark(nome) for nome in nomes]


# %%
# Parser TSPLIB95 e funcoes auxiliares

@dataclass
class ProblemaTSP:
    nome: str
    prob: object
    nos: list
    n: int
    dist: list[list[float]]


def carregar_problema_tsp(arquivo: Path) -> ProblemaTSP:
    # Parser pedido no enunciado:
    prob = tsplib95.load(str(arquivo))
    nos = list(prob.get_nodes())

    n = len(nos)
    dist = [[0.0] * n for _ in range(n)]
    for i, a in enumerate(nos):
        for j, b in enumerate(nos):
            if i != j:
                dist[i][j] = float(prob.get_weight(a, b))

    return ProblemaTSP(
        nome=arquivo.stem,
        prob=prob,
        nos=nos,
        n=n,
        dist=dist,
    )


def distancia_tour(tour: list[int], dist: list[list[float]]) -> float:
    return sum(dist[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))


def gap_percentual(distancia: float, otimo: float | None) -> float | None:
    if otimo is None:
        return None
    return 100.0 * (distancia - otimo) / otimo


def normalizar_tour_para_nodes(tour: list[int], nos: list) -> list:
    return [nos[i] for i in tour]


# %%
# Algoritmo 1: Guloso - Nearest Neighbor

def nearest_neighbor(n: int, dist: list[list[float]], inicio: int = 0) -> list[int]:
    visitado = [False] * n
    tour = [inicio]
    visitado[inicio] = True
    atual = inicio

    for _ in range(n - 1):
        proximo = min(
            (j for j in range(n) if not visitado[j]),
            key=lambda j: dist[atual][j],
        )
        tour.append(proximo)
        visitado[proximo] = True
        atual = proximo

    return tour


def guloso_multistart(n: int, dist: list[list[float]], max_inicios: int | None = None) -> list[int]:
    inicios = range(n) if max_inicios is None else range(min(n, max_inicios))
    return min(
        (nearest_neighbor(n, dist, inicio=i) for i in inicios),
        key=lambda tour: distancia_tour(tour, dist),
    )


# %%
# Algoritmo 2: Hill Climbing / busca local com 2-opt

def two_opt_hill_climbing(
    tour_inicial: list[int],
    dist: list[list[float]],
    max_passes: int = 200,
) -> list[int]:
    melhor = tour_inicial[:]
    n = len(melhor)

    for _ in range(max_passes):
        melhorou = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                a, b = melhor[i - 1], melhor[i]
                c, d = melhor[j], melhor[(j + 1) % n]
                delta = (dist[a][c] + dist[b][d]) - (dist[a][b] + dist[c][d])
                if delta < -1e-9:
                    melhor[i : j + 1] = reversed(melhor[i : j + 1])
                    melhorou = True
        if not melhorou:
            break

    return melhor


# %%
# Algoritmo 3: Simulated Annealing

def vizinho_2opt_aleatorio(tour: list[int]) -> list[int]:
    novo = tour[:]
    i, j = sorted(random.sample(range(1, len(tour)), 2))
    novo[i : j + 1] = reversed(novo[i : j + 1])
    return novo


def simulated_annealing(
    tour_inicial: list[int],
    dist: list[list[float]],
    temperatura: float = 1000.0,
    alpha: float = 0.995,
    temperatura_min: float = 1e-3,
    max_iter: int = 50_000,
) -> list[int]:
    atual = tour_inicial[:]
    custo_atual = distancia_tour(atual, dist)
    melhor = atual[:]
    melhor_custo = custo_atual

    for _ in range(max_iter):
        if temperatura <= temperatura_min:
            break

        candidato = vizinho_2opt_aleatorio(atual)
        custo_candidato = distancia_tour(candidato, dist)
        delta = custo_candidato - custo_atual

        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            atual = candidato
            custo_atual = custo_candidato
            if custo_atual < melhor_custo:
                melhor = atual[:]
                melhor_custo = custo_atual

        temperatura *= alpha

    return melhor


# %%
# Algoritmo 4: Algoritmo Genetico

def torneio(populacao: list[list[int]], fitness: list[float], k: int = 3) -> list[int]:
    candidatos = random.sample(range(len(populacao)), k)
    melhor_idx = min(candidatos, key=lambda idx: fitness[idx])
    return populacao[melhor_idx][:]


def order_crossover(pai1: list[int], pai2: list[int]) -> list[int]:
    n = len(pai1)
    a, b = sorted(random.sample(range(n), 2))
    filho = [-1] * n
    filho[a : b + 1] = pai1[a : b + 1]

    pos = (b + 1) % n
    for gene in pai2:
        if gene in filho:
            continue
        filho[pos] = gene
        pos = (pos + 1) % n

    return filho


def mutacao_swap(individuo: list[int], taxa: float = 0.02) -> list[int]:
    filho = individuo[:]
    for i in range(len(filho)):
        if random.random() < taxa:
            j = random.randrange(len(filho))
            filho[i], filho[j] = filho[j], filho[i]
    return filho


def algoritmo_genetico(
    n: int,
    dist: list[list[float]],
    pop_size: int = 120,
    geracoes: int = 500,
    taxa_crossover: float = 0.90,
    taxa_mutacao: float = 0.02,
    elitismo: int = 2,
) -> list[int]:
    base = list(range(n))
    populacao = [random.sample(base, n) for _ in range(pop_size)]

    # Semeia parte da populacao com solucoes gulosas, uma pratica simples
    # para acelerar a convergencia em TSP.
    for inicio in range(min(n, max(1, pop_size // 10))):
        populacao[inicio] = nearest_neighbor(n, dist, inicio=inicio)

    for _ in range(geracoes):
        fitness = [distancia_tour(ind, dist) for ind in populacao]
        ordem = sorted(range(pop_size), key=lambda idx: fitness[idx])
        nova_pop = [populacao[idx][:] for idx in ordem[:elitismo]]

        while len(nova_pop) < pop_size:
            pai1 = torneio(populacao, fitness)
            pai2 = torneio(populacao, fitness)
            if random.random() < taxa_crossover:
                filho = order_crossover(pai1, pai2)
            else:
                filho = pai1
            nova_pop.append(mutacao_swap(filho, taxa_mutacao))

        populacao = nova_pop

    fitness = [distancia_tour(ind, dist) for ind in populacao]
    melhor = populacao[min(range(pop_size), key=lambda idx: fitness[idx])]
    return two_opt_hill_climbing(melhor, dist, max_passes=20)


# %%
# Execucao dos experimentos e tabela de resultados

def parametros_por_tamanho(n: int) -> dict:
    """Ajusta esforco computacional para instancias maiores."""
    if n <= 30:
        return {"sa_iter": 20_000, "ga_pop": 80, "ga_ger": 300}
    if n <= 100:
        return {"sa_iter": 50_000, "ga_pop": 120, "ga_ger": 600}
    return {"sa_iter": 80_000, "ga_pop": 160, "ga_ger": 800}


def medir_algoritmo(nome: str, func, problema: ProblemaTSP, otimo: float | None) -> dict:
    t0 = time.perf_counter()
    tour = func()
    tempo = time.perf_counter() - t0
    distancia = distancia_tour(tour, problema.dist)

    return {
        "benchmark": problema.nome,
        "dimensao": problema.n,
        "edge_weight_type": getattr(problema.prob, "edge_weight_type", None),
        "algoritmo": nome,
        "distancia": round(distancia, 3),
        "otimo_conhecido": otimo,
        "gap_percentual": None if otimo is None else round(gap_percentual(distancia, otimo), 3),
        "tempo_s": round(tempo, 4),
        "tour": " -> ".join(map(str, normalizar_tour_para_nodes(tour + [tour[0]], problema.nos))),
    }


def resolver_benchmark(arquivo: Path, semente: int = SEMENTE) -> list[dict]:
    random.seed(semente)
    problema = carregar_problema_tsp(arquivo)
    otimo = OPTIMOS_CONHECIDOS.get(problema.nome)
    pars = parametros_por_tamanho(problema.n)

    print(f"\nBenchmark: {problema.nome} ({problema.n} cidades)")

    tour_guloso = guloso_multistart(problema.n, problema.dist)

    resultados = [
        medir_algoritmo(
            "Guloso - Nearest Neighbor",
            lambda: tour_guloso,
            problema,
            otimo,
        ),
        medir_algoritmo(
            "Hill Climbing - 2-opt",
            lambda: two_opt_hill_climbing(tour_guloso, problema.dist),
            problema,
            otimo,
        ),
        medir_algoritmo(
            "Simulated Annealing",
            lambda: simulated_annealing(
                tour_guloso,
                problema.dist,
                temperatura=1000.0,
                alpha=0.995,
                temperatura_min=1e-3,
                max_iter=pars["sa_iter"],
            ),
            problema,
            otimo,
        ),
        medir_algoritmo(
            "Algoritmo Genetico",
            lambda: algoritmo_genetico(
                problema.n,
                problema.dist,
                pop_size=pars["ga_pop"],
                geracoes=pars["ga_ger"],
                taxa_crossover=0.9,
                taxa_mutacao=0.02,
                elitismo=2,
            ),
            problema,
            otimo,
        ),
    ]

    melhor = min(resultados, key=lambda row: row["distancia"])
    print(f"Melhor: {melhor['algoritmo']} | distancia = {melhor['distancia']}")
    return resultados


def salvar_resultados_csv(resultados: list[dict], caminho: Path = RESULTS_CSV) -> None:
    if not resultados:
        return
    with caminho.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(resultados[0].keys()))
        writer.writeheader()
        writer.writerows(resultados)


def executar_experimentos(benchmarks: Iterable[str] = BENCHMARKS) -> list[dict]:
    arquivos = preparar_benchmarks(benchmarks)
    resultados: list[dict] = []
    for arquivo in arquivos:
        resultados.extend(resolver_benchmark(arquivo))

    salvar_resultados_csv(resultados)
    print(f"\nTabela salva em: {RESULTS_CSV}")
    return resultados


# %%
# Rodar os experimentos

resultados = executar_experimentos(BENCHMARKS)

colunas_resumo = [
    "benchmark",
    "dimensao",
    "algoritmo",
    "distancia",
    "otimo_conhecido",
    "gap_percentual",
    "tempo_s",
]

if pd is not None:
    tabela = pd.DataFrame(resultados)
    try:
        from IPython.display import display

        display(tabela[colunas_resumo])
    except ImportError:
        print(tabela[colunas_resumo].to_string(index=False))
else:
    for linha in resultados:
        print({k: linha[k] for k in colunas_resumo})


# %%
# Opcional: listar todos os .tsp disponiveis no repositorio

# todos = listar_benchmarks_tsplib()
# print(f"{len(todos)} benchmarks encontrados")
# print(todos[:30])
