# ================================================================
# LAB02BIA - Tarefa 02
# Regressao linear: visualizacao, SQE (OLS) e SAE
# Codigo comentado para estudo no VSCode / Jupyter Notebook
# ================================================================

# Caso alguma biblioteca nao esteja instalada, execute no terminal da .venv:
# python -m pip install numpy matplotlib seaborn scipy

# ----------------------------------------------------------------
# 1. IMPORTACAO E CONFIGURACAO DAS BIBLIOTECAS
# ----------------------------------------------------------------
import numpy as np                      # Calculos numericos e vetores/matrizes.
import matplotlib.pyplot as plt         # Criacao dos graficos.
import seaborn as sns                   # Estilo visual para os graficos.
from pathlib import Path                # Manipulacao segura de pastas e arquivos.
from scipy.optimize import fmin         # Busca numerica pelos parametros que minimizam um erro.

# Define um estilo visual com grade branca.
sns.set_style("whitegrid")

# Define contexto e tamanho padrao dos elementos do grafico.
sns.set_context("notebook", font_scale=1, rc={"lines.linewidth": 2})

# Configuracoes gerais do Matplotlib.
plt.rc("font", family="serif")        # Usa fonte com serifas, quando disponivel.
plt.rc("xtick", labelsize=10)          # Tamanho dos numeros no eixo x.
plt.rc("ytick", labelsize=10)          # Tamanho dos numeros no eixo y.
plt.rc("font", size=12)                # Tamanho de fonte padrao.
plt.rc("figure", figsize=(12, 5))      # Largura e altura padrao da figura, em polegadas.

# OBSERVACAO SOBRE LATEX:
# O codigo original usa: plt.rc("text", usetex=True)
# Esta linha permite escrever textos matematicos usando LaTeX nos graficos,
# mas exige que o LaTeX esteja instalado e reconhecido pelo sistema.
# Descomente somente depois de instalar e testar o LaTeX:
# plt.rc("text", usetex=True)

# Cria a pasta "resultados" dentro da pasta atual do projeto.
# Assim, os graficos nao dependem de um caminho fixo como C:/Users/.../Desktop.
PASTA_RESULTADOS = Path("resultados")
PASTA_RESULTADOS.mkdir(exist_ok=True)


# ----------------------------------------------------------------
# 2. EXEMPLO INICIAL: RELACAO ENTRE EXPERIENCIA E PRECO DO SEGURO
# ----------------------------------------------------------------
# Lista x: experiencia de cada motorista, em anos.
x = [5, 2, 12, 9, 15, 6, 25, 16, 23]

# Lista y: valor mensal do seguro associado a cada motorista.
y = [650, 890, 500, 730, 450, 550, 380, 610, 350]

# Cria um grafico de dispersao: cada ponto representa uma observacao (x, y).
plt.figure()
plt.scatter(x, y, color="red")
plt.xlabel("Experiencia na direcao (anos)")
plt.ylabel("Seguro do carro (valor mensal)")
plt.title("Experiencia na direcao x valor do seguro")
plt.show()

# Interpretacao: a tendencia visual e de reducao do valor do seguro
# quando a experiencia de direcao aumenta. A regressao linear tenta
# representar esta tendencia por uma reta.


# ----------------------------------------------------------------
# 3. GERACAO DE DADOS ARTIFICIAIS EM DUAS DIMENSOES
# ----------------------------------------------------------------
# Define uma semente para que os mesmos numeros aleatorios sejam gerados
# a cada execucao. Isso torna o exemplo reprodutivel.
np.random.seed(42)

# Gera 300 observacoes com duas variaveis aleatorias normalmente distribuidas.
# A matriz X1 tem dimensao 300 x 2: 300 linhas (amostras) e 2 colunas (variaveis).
X1 = np.random.randn(300, 2)

# Matriz de transformacao que introduz correlacao entre as duas variaveis.
A = np.array([[0.6, 0.4],
              [0.4, 0.6]])

# Produto matricial: cada linha de X1 e transformada pela matriz A.
# O resultado X2 passa a ter uma nuvem de pontos inclinada/correlacionada.
X2 = np.dot(X1, A)

# X2[:, 0] seleciona todas as linhas da coluna 0 (eixo x).
# X2[:, 1] seleciona todas as linhas da coluna 1 (eixo y).
plt.figure()
plt.plot(X2[:, 0], X2[:, 1], "o", alpha=0.3)
plt.xlabel("Variavel 1")
plt.ylabel("Variavel 2")
plt.title("Dados artificiais com correlacao")
plt.show()


# ----------------------------------------------------------------
# 4. PRIMEIRA RETA CANDIDATA
# ----------------------------------------------------------------
# np.arange(-2, 3) produz os valores: -2, -1, 0, 1 e 2.
valores_x = np.arange(-2, 3)

# A expressao 0 + 1*x representa a reta y = 0 + 1*x, isto e, y = x.
# A compreensao de lista calcula o valor da reta para cada valor de x.
modelo1 = [0 + 1 * valor for valor in valores_x]

plt.figure()
plt.plot(X2[:, 0], X2[:, 1], "o", alpha=0.3, label="Dados")
plt.plot(valores_x, modelo1, "r", label="Modelo 1: y = x")
plt.xlabel("Variavel 1")
plt.ylabel("Variavel 2")
plt.title("Primeira reta candidata")
plt.legend()
plt.show()


# ----------------------------------------------------------------
# 5. COMPARACAO VISUAL ENTRE TRES RETAS CANDIDATAS
# ----------------------------------------------------------------
# Modelo 2: y = 0 + 1*x.
modelo2 = [0 + 1 * valor for valor in valores_x]

# Modelo 3: y = 0.3 + 0.9*x.
modelo3 = [0.3 + 0.9 * valor for valor in valores_x]

# Modelo 4: y = 0 - 0.1*x.
modelo4 = [0 - 0.1 * valor for valor in valores_x]

plt.figure()
plt.plot(X2[:, 0], X2[:, 1], "o", alpha=0.3, label="Dados")
plt.plot(valores_x, modelo2, "r", label="Modelo 2: y = x")
plt.plot(valores_x, modelo3, "g", label="Modelo 3: y = 0.3 + 0.9x")
plt.plot(valores_x, modelo4, "y", label="Modelo 4: y = -0.1x")
plt.xlabel("Variavel 1")
plt.ylabel("Variavel 2")
plt.title("Comparacao de retas candidatas")
plt.legend()

# Salva a figura usando um caminho relativo ao projeto.
plt.savefig(PASTA_RESULTADOS / "ExemplosRLin.png", dpi=300, bbox_inches="tight")
plt.show()

# A avaliacao visual ajuda a criar intuicao, mas a escolha final de um modelo
# deve ser baseada em uma metrica de erro calculada para todas as observacoes.


# ----------------------------------------------------------------
# 6. AJUSTE POR MINIMIZACAO DA SOMA DOS QUADRADOS DOS ERROS (SQE)
# ----------------------------------------------------------------
# Dados de exemplo para ajustar uma reta y = a0 + a1*x.
x = np.array([2.2, 4.3, 5.1, 5.8, 6.4, 8.0])
y = np.array([0.4, 10.1, 14.0, 10.9, 15.4, 18.5])

# Funcao objetivo da SQE (Soma dos Quadrados dos Erros).
# a[0] corresponde ao intercepto a0 da reta.
# a[1] corresponde ao coeficiente angular a1 da reta.
#
# Para cada ponto, a[0] + a[1]*x e o valor previsto pela reta.
# A diferenca entre previsao e y real e o residuo/erro.
# O operador ** 2 eleva cada erro ao quadrado.
# np.sum soma todos os erros ao quadrado.
#
# Minimizar SQE equivale ao metodo OLS (Ordinary Least Squares),
# ou Minimos Quadrados Ordinarios.
SQE = lambda a, x, y: np.sum((a[0] + a[1] * x - y) ** 2)

# fmin procura os valores de a0 e a1 que minimizam a SQE.
# [0, 1] e apenas um palpite inicial para os parametros.
# args=(x, y) envia os dados para a funcao SQE.
a0, a1 = fmin(SQE, [0, 1], args=(x, y), disp=False)

# Mostra os parametros encontrados.
print(f"Modelo OLS: y = {a0:.3f} + {a1:.3f}x")
print(f"SQE minima: {SQE([a0, a1], x, y):.3f}")

# Gera a figura que mostra os pontos, a reta e os residuos.
plt.figure()
plt.plot(x, y, "ro", label="Dados observados")
plt.plot([0, 10], [a0, a0 + a1 * 10], alpha=0.8, label="Reta OLS")

# zip(x, y) percorre simultaneamente cada par (xi, yi).
for xi, yi in zip(x, y):
    # A linha pontilhada vertical mostra a distancia entre o valor observado
    # e o valor previsto pela reta: este e o residuo do ponto.
    plt.plot([xi] * 2, [yi, a0 + a1 * xi], "k:")

plt.xlim(2, 9)
plt.ylim(0, 20)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Ajuste por SQE / OLS e residuos")
plt.legend()
plt.savefig(PASTA_RESULTADOS / "ExemplosErros.png", dpi=300, bbox_inches="tight")
plt.show()


# ----------------------------------------------------------------
# 7. AJUSTE POR SOMA DOS ERROS ABSOLUTOS (SAE)
# ----------------------------------------------------------------
# A SAE usa o valor absoluto dos residuos, sem elevar o erro ao quadrado.
# Em geral, ela e menos sensivel a valores muito afastados (outliers) do que a SQE.
# b[0] e o intercepto; b[1] e o coeficiente angular da reta ajustada por SAE.
SAE = lambda b, x, y: np.sum(np.abs(b[0] + b[1] * x - y))

# Procura os parametros b0 e b1 que minimizam a SAE.
b0, b1 = fmin(SAE, [0, 1], args=(x, y), disp=False)

print(f"Modelo SAE: y = {b0:.3f} + {b1:.3f}x")
print(f"SAE minima: {SAE([b0, b1], x, y):.3f}")

# Compara visualmente a reta ajustada por OLS/SQE e a reta ajustada por SAE.
plt.figure()
plt.plot(x, y, "ro", label="Dados observados")
plt.plot([0, 10], [a0, a0 + a1 * 10], alpha=0.8, label="OLS / SQE")
plt.plot([0, 10], [b0, b0 + b1 * 10], alpha=0.8, label="SAE")

# Mantem os residuos da reta OLS para visualizacao.
for xi, yi in zip(x, y):
    plt.plot([xi] * 2, [yi, a0 + a1 * xi], "k:")

plt.xlim(2, 9)
plt.ylim(0, 20)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Comparacao entre ajuste por SQE e SAE")
plt.legend()
plt.savefig(PASTA_RESULTADOS / "ExemplosErros_SAE_e_SQE.png", dpi=300, bbox_inches="tight")
plt.show()

# ----------------------------------------------------------------
# CONCLUSAO
# ----------------------------------------------------------------
# - Regressao linear procura uma reta para aproximar a relacao entre x e y.
# - A SQE/OLS penaliza fortemente erros grandes, pois os erros sao elevados ao quadrado.
# - A SAE soma os valores absolutos dos erros e tende a ser menos influenciada por outliers.
# - Em ambos os casos, fmin e usado para encontrar os parametros que minimizam a metrica.
