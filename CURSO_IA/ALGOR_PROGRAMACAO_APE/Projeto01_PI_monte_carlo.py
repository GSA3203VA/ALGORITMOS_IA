# %% [markdown]
# # Projeto 01 - Algoritmo do Pi por Monte Carlo
#
# Neste projeto vamos estimar o valor de pi usando uma simulacao de Monte Carlo.
#
# A ideia e sortear pontos `(x, y)` dentro de um quadrado de lado 1. O quarto de circulo de raio 1 ocupa uma parte desse quadrado. Um ponto esta dentro do quarto de circulo quando:
#
# `x**2 + y**2 <= 1`
#
# Como a area do quarto de circulo e `pi / 4`, podemos estimar:
#
# `pi ~= 4 * pontos_dentro / pontos_sorteados`

# %%
# math tem o valor real de pi, que vou usar para comparar com a estimativa.
import math

# random sorteia os pontos do metodo de Monte Carlo.
import random

# mean calcula a media quando eu repetir a simulacao varias vezes.
from statistics import mean

# %% [markdown]
# ## Funcao principal

# %%
def estimar_pi_monte_carlo(quantidade_pontos, semente=None):
    """Estima pi sorteando pontos aleatorios no quadrado unitario."""
    # Primeiro verifico se o usuario pediu uma quantidade valida de pontos.
    if quantidade_pontos <= 0:
        raise ValueError("quantidade_pontos deve ser maior que zero")

    # Uso uma semente para conseguir repetir o mesmo resultado durante os estudos.
    gerador = random.Random(semente)

    # Este contador guarda quantos pontos cairam dentro do quarto de circulo.
    pontos_dentro = 0

    # Guardo os primeiros pontos apenas para mostrar como o algoritmo esta funcionando.
    primeiros_pontos = []

    for indice in range(quantidade_pontos):
        # Sorteio x e y entre 0 e 1, ou seja, dentro do quadrado unitario.
        x = gerador.random()
        y = gerador.random()

        # Pelo teorema de Pitagoras, o ponto esta dentro do circulo se x^2 + y^2 <= raio^2.
        # Como o raio e 1, raio^2 tambem e 1.
        dentro = x**2 + y**2 <= 1

        if dentro:
            pontos_dentro += 1

        # Para nao imprimir milhares de linhas, separo so os 5 primeiros pontos.
        if indice < 5:
            primeiros_pontos.append((x, y, dentro))

    # A proporcao pontos_dentro / quantidade_pontos aproxima a area pi/4.
    # Por isso multiplico por 4 para estimar pi.
    pi_estimado = 4 * pontos_dentro / quantidade_pontos

    # Retorno um dicionario para deixar os resultados organizados.
    return {
        "pontos_sorteados": quantidade_pontos,
        "pontos_dentro": pontos_dentro,
        "pi_estimado": pi_estimado,
        "erro_absoluto": abs(math.pi - pi_estimado),
        "primeiros_pontos": primeiros_pontos,
    }

# %% [markdown]
# ## Execucao com 10.000 pontos

# %%
# Aqui faco uma simulacao principal com 10.000 pontos.
resultado = estimar_pi_monte_carlo(10_000, semente=42)

# Mostro alguns pontos para visualizar a regra dentro/fora.
for numero, (x, y, dentro) in enumerate(resultado["primeiros_pontos"], start=1):
    posicao = "dentro" if dentro else "fora"
    print(f"Ponto {numero}: ({x:.4f}, {y:.4f}) -> {posicao}")

# Agora imprimo o resumo da simulacao.
print("\nPontos sorteados:", resultado["pontos_sorteados"])
print("Pontos dentro do quarto de circulo:", resultado["pontos_dentro"])
print(f"Pi estimado: {resultado['pi_estimado']:.6f}")
print(f"Pi real:      {math.pi:.6f}")
print(f"Erro:         {resultado['erro_absoluto']:.6f}")

# %% [markdown]
# ## Comparacao usando quantidades diferentes de pontos
#
# Quanto maior o numero de pontos, maior tende a ser a precisao da estimativa. Como o metodo e aleatorio, o resultado pode variar a cada execucao.

# %%
# Vou testar quantidades diferentes para observar a melhora da aproximacao.
quantidades = [100, 1_000, 10_000, 100_000]

print(f"{'Pontos':>10} | {'Pi estimado':>12} | {'Erro':>10}")
print("-" * 39)

for quantidade in quantidades:
    # Uso a propria quantidade como semente para a tabela sempre sair igual.
    resultado = estimar_pi_monte_carlo(quantidade, semente=quantidade)
    print(f"{quantidade:>10} | {resultado['pi_estimado']:>12.6f} | {resultado['erro_absoluto']:>10.6f}")

# %% [markdown]
# ## Repetindo a simulacao
#
# Uma unica simulacao pode ficar um pouco acima ou abaixo de pi. Repetir o experimento ajuda a observar a variacao dos resultados.

# %%
# Nesta parte repito o experimento 10 vezes com a mesma quantidade de pontos.
estimativas = []

for rodada in range(10):
    # Cada rodada recebe uma semente diferente para simular sorteios diferentes.
    resultado = estimar_pi_monte_carlo(10_000, semente=rodada)
    estimativas.append(resultado["pi_estimado"])

print("Estimativas:", [round(valor, 6) for valor in estimativas])
print(f"Media das estimativas: {mean(estimativas):.6f}")
print(f"Erro da media:         {abs(math.pi - mean(estimativas)):.6f}")

# %% [markdown]
# ## Teste simples

# %%
# Estes testes simples ajudam a conferir se a funcao esta devolvendo valores possiveis.
teste = estimar_pi_monte_carlo(1_000, semente=123)

assert 0 <= teste["pontos_dentro"] <= teste["pontos_sorteados"]
assert 0 <= teste["pi_estimado"] <= 4

print("Testes concluidos com sucesso.")

