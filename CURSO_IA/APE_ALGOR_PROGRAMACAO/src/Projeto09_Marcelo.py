"""
Projeto 09 - TSP com diferentes algoritmos de otimizacao
Aula 9 - Algoritmos e Programacao (IA para Engenheiros - UFRGS)

Resolve benchmarks da TSPLIB95 usando:
    - Nearest Neighbor (guloso)
    - 2-opt (busca local)
    - Algoritmo Genetico (Order Crossover + swap mutation + torneio + elitismo)
"""

import os
import random
import time
import math

import tsplib95
import matplotlib
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Carregamento do benchmark
# ---------------------------------------------------------------------------
def carregar_problema(arquivo):
    prob = tsplib95.load(arquivo)
    nos = list(prob.get_nodes())
    n = len(nos)
    # Matriz de distancias pre-calculada (acelera bastante o GA)
    dist = [[0.0] * n for _ in range(n)]
    for i, a in enumerate(nos):
        for j, b in enumerate(nos):
            if i != j:
                dist[i][j] = prob.get_weight(a, b)
    coords = {i: prob.node_coords[nos[i]] for i in range(n)}
    return prob, nos, n, dist, coords


def tour_distancia(tour, dist):
    n = len(tour)
    return sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n))


# ---------------------------------------------------------------------------
# Algoritmo 1: Nearest Neighbor (guloso)
# ---------------------------------------------------------------------------
def nearest_neighbor(n, dist, inicio=0):
    visitados = [False] * n
    tour = [inicio]
    visitados[inicio] = True
    atual = inicio
    for _ in range(n - 1):
        proximo, menor = -1, float("inf")
        for j in range(n):
            if not visitados[j] and dist[atual][j] < menor:
                menor, proximo = dist[atual][j], j
        tour.append(proximo)
        visitados[proximo] = True
        atual = proximo
    return tour


# ---------------------------------------------------------------------------
# Algoritmo 2: 2-opt (busca local, melhoria iterativa)
# ---------------------------------------------------------------------------
def dois_opt(tour, dist, max_iter=10_000):
    n = len(tour)
    melhor = tour[:]
    melhorou = True
    it = 0
    while melhorou and it < max_iter:
        melhorou = False
        it += 1
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                a, b = melhor[i - 1], melhor[i]
                c, d = melhor[j], melhor[(j + 1) % n]
                delta = (dist[a][c] + dist[b][d]) - (dist[a][b] + dist[c][d])
                if delta < -1e-9:
                    melhor[i:j + 1] = melhor[i:j + 1][::-1]
                    melhorou = True
        # repete enquanto encontrar melhorias (first improvement)
    return melhor


# ---------------------------------------------------------------------------
# Algoritmo 3: Algoritmo Genetico para TSP
# ---------------------------------------------------------------------------
def torneio(pop, fits, k=3):
    candidatos = random.sample(list(zip(pop, fits)), k)
    return min(candidatos, key=lambda x: x[1])[0]  # menor distancia = melhor


def ox_crossover(p1, p2):
    """Order Crossover (OX) - preserva permutacao valida."""
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    filho = [-1] * n
    filho[a:b + 1] = p1[a:b + 1]
    resto = [g for g in p2 if g not in filho]
    k = 0
    for i in range(n):
        if filho[i] == -1:
            filho[i] = resto[k]
            k += 1
    return filho


def mut_swap(ind, taxa=0.02):
    ind = ind[:]
    for i in range(len(ind)):
        if random.random() < taxa:
            j = random.randrange(len(ind))
            ind[i], ind[j] = ind[j], ind[i]
    return ind


def algoritmo_genetico(n, dist,
                       pop_size=100, geracoes=500,
                       taxa_cx=0.9, taxa_mut=0.02, elitismo=2,
                       semeado_nn=True, refinar_2opt_a_cada=0):
    """AG para TSP. Se refinar_2opt_a_cada > 0, aplica 2-opt no melhor
    individuo a cada N geracoes (memetico) - muito mais eficaz em
    instancias maiores."""
    base = list(range(n))
    pop = [random.sample(base, n) for _ in range(pop_size)]
    # Semeia com NN comecando em varias cidades distintas
    if semeado_nn:
        for k in range(min(n, max(1, pop_size // 10))):
            pop[k] = nearest_neighbor(n, dist, inicio=k)

    hist_melhor, hist_medio = [], []

    for g in range(geracoes):
        fits = [tour_distancia(ind, dist) for ind in pop]
        hist_melhor.append(min(fits))
        hist_medio.append(sum(fits) / pop_size)

        ordem = sorted(range(pop_size), key=lambda i: fits[i])
        nova_pop = [pop[i] for i in ordem[:elitismo]]

        # Refino 2-opt periodico no melhor (memetico)
        if refinar_2opt_a_cada and g % refinar_2opt_a_cada == 0 and g > 0:
            nova_pop[0] = dois_opt(nova_pop[0], dist, max_iter=2)

        while len(nova_pop) < pop_size:
            p1 = torneio(pop, fits)
            p2 = torneio(pop, fits)
            filho = ox_crossover(p1, p2) if random.random() < taxa_cx else p1[:]
            nova_pop.append(mut_swap(filho, taxa_mut))

        pop = nova_pop

    fits = [tour_distancia(ind, dist) for ind in pop]
    melhor = pop[min(range(pop_size), key=lambda i: fits[i])]
    return melhor, hist_melhor, hist_medio


# ---------------------------------------------------------------------------
# Plot do tour - estilo do slide 27 (burma14)
# ---------------------------------------------------------------------------
def plotar_tour(tour, coords, dist, titulo, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 6))

    xs = [coords[i][1] for i in tour] + [coords[tour[0]][1]]
    ys = [coords[i][0] for i in tour] + [coords[tour[0]][0]]
    ax.plot(xs, ys, color="#534AB7", linewidth=1.5, label="Tour", zorder=2)

    for i, (lat, lon) in coords.items():
        ax.scatter(lon, lat, s=80, color="#5DCAA5",
                   edgecolors="#1F4D3D", zorder=3)
        ax.annotate(str(i + 1), (lon, lat),
                    textcoords="offset points", xytext=(6, 6), fontsize=8)

    d = tour_distancia(tour, dist)
    ax.set_title(f"{titulo}  -  distancia = {d:.2f}")
    ax.set_xlabel("Longitude / x")
    ax.set_ylabel("Latitude / y")
    ax.grid(True, linewidth=0.4, alpha=0.5)
    ax.legend()


def plotar_convergencia(hist_melhor, hist_medio, otimo=None, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 4))

    geracoes = range(1, len(hist_melhor) + 1)
    ax.plot(geracoes, hist_melhor, color="#534AB7", linewidth=2,
            label="Melhor fitness")
    ax.plot(geracoes, hist_medio, color="#5DCAA5", linewidth=1.5,
            linestyle="--", label="Fitness medio")
    if otimo is not None:
        ax.axhline(otimo, color="#D85A30", linewidth=1, linestyle=":",
                   label=f"Otimo ({otimo})")
    ax.set_xlabel("Geracao")
    ax.set_ylabel("Distancia do tour")
    ax.set_title("Convergencia do AG")
    ax.grid(True, linewidth=0.4, alpha=0.5)
    ax.legend()


# ---------------------------------------------------------------------------
# Execucao de um benchmark
# ---------------------------------------------------------------------------
def resolver(arquivo, otimo=None, semente=42):
    random.seed(semente)
    nome = os.path.splitext(os.path.basename(arquivo))[0]
    print(f"\n{'='*60}\nBenchmark: {nome}\n{'='*60}")

    prob, nos, n, dist, coords = carregar_problema(arquivo)
    print(f"Dimensao: {n} cidades  |  tipo: {prob.edge_weight_type}")

    resultados = []

    # 1) Nearest Neighbor
    t0 = time.perf_counter()
    tour_nn = nearest_neighbor(n, dist)
    t_nn = time.perf_counter() - t0
    resultados.append(("Nearest Neighbor", tour_distancia(tour_nn, dist), t_nn, tour_nn))

    # 2) 2-opt (sementeado pelo NN)
    t0 = time.perf_counter()
    tour_2opt = dois_opt(tour_nn, dist)
    t_2opt = time.perf_counter() - t0
    resultados.append(("2-opt (NN + busca local)", tour_distancia(tour_2opt, dist), t_2opt, tour_2opt))

    # 3) AG
    t0 = time.perf_counter()
    tour_ag, hist_m, hist_a = algoritmo_genetico(
        n, dist,
        pop_size=120,
        geracoes=400 if n <= 30 else 800,
        taxa_cx=0.9, taxa_mut=0.02, elitismo=2,
        refinar_2opt_a_cada=(0 if n <= 30 else 25),
    )
    t_ag = time.perf_counter() - t0
    resultados.append(("Algoritmo Genetico", tour_distancia(tour_ag, dist), t_ag, tour_ag))

    # Tabela
    print(f"\n{'Algoritmo':<28}{'Distancia':>12}{'Tempo (s)':>12}{'Gap (%)':>10}")
    print("-" * 62)
    for nm, d, t, _ in resultados:
        gap = f"{(d - otimo) / otimo * 100:>9.2f}" if otimo else "    -    "
        print(f"{nm:<28}{d:>12.2f}{t:>12.3f}{gap:>10}")
    print("-" * 62)
    if otimo:
        print(f"{'Otimo conhecido':<28}{otimo:>12.2f}")

    # Melhor tour entre os algoritmos
    melhor_nm, melhor_d, _, melhor_tour = min(resultados, key=lambda r: r[1])
    print(f"\nMelhor solucao: {melhor_nm} (distancia {melhor_d:.2f})")
    print("Tour: " + " -> ".join(str(c + 1) for c in melhor_tour + [melhor_tour[0]]))

    # Plot - estilo slide 27
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    plotar_tour(melhor_tour, coords, dist,
                f"{nome.upper()}  -  {melhor_nm}", ax=ax1)
    plotar_convergencia(hist_m, hist_a, otimo=otimo, ax=ax2)
    fig.suptitle(f"Projeto 09 - TSP: {nome}", fontsize=13, fontweight="bold")
    fig.tight_layout()
    pasta_saida = os.path.dirname(os.path.abspath(__file__))
    fig.savefig(os.path.join(pasta_saida, f"resultado_{nome}.png"), dpi=120)
    if matplotlib.get_backend().lower() not in ("agg",):
        plt.show()
    else:
        plt.close(fig)

    return resultados


# ---------------------------------------------------------------------------
# Main - rodar nos dois benchmarks
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    pasta = os.path.dirname(os.path.abspath(__file__))

    benchmarks = [
        ("burma14.tsp", 3323),    # otimo conhecido (slide 27)
        ("berlin52.tsp", 7542),   # otimo conhecido TSPLIB
    ]

    tabela_geral = []
    for arq, otimo in benchmarks:
        caminho = os.path.join(pasta, arq)
        if not os.path.exists(caminho):
            print(f"[skip] {arq} nao encontrado")
            continue
        res = resolver(caminho, otimo=otimo)
        tabela_geral.append((arq, otimo, res))

    # Resumo final
    print(f"\n\n{'='*78}\nRESUMO GERAL\n{'='*78}")
    print(f"{'Benchmark':<14}{'Otimo':>10}  {'Algoritmo':<28}{'Distancia':>12}{'Gap (%)':>10}")
    print("-" * 78)
    for arq, otimo, res in tabela_geral:
        for nm, d, _, _ in res:
            gap = (d - otimo) / otimo * 100
            print(f"{arq:<14}{otimo:>10}  {nm:<28}{d:>12.2f}{gap:>10.2f}")
        print("-" * 78)
