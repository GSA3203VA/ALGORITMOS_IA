# %% [markdown]
# Com base no material das suas aulas, o algoritmo para calcular o valor de Pi pelo método de Monte Carlo consiste em "sortear" pontos com coordenadas x e y aleatórias e verificar se eles caem dentro de um círculo de raio 1
# . Para fazer essa verificação, utiliza-se a condição geométrica x**2 + y**2 < 1

# %%
import random as r

# %%
# 1. Inicialização das variáveis (isso evita o NameError)
pt_sorteados = 0 
pt_dentro = 0 
pt_a_sortear = 10000 

# %%
# 2. Execução do laço
while pt_sorteados < pt_a_sortear:  # repete até sortear 10000 pontos  
    pt = r.random(), r.random()     # nesta sintaxe pt é uma tuple 'dupla'(x,y), x e y são numeros aleatórios entre 0 e 1.
    # x = r.random()
    # y = r.random()
    if (pt[0]**2 + pt[1]**2 < 1):  #verifica se o ponto está dentro do quarto de círculo  
        # if x**2 + y**2 < 1:     
        pt_dentro += 1   
        posicao ="dentro"
    else:
        posicao = "fora"     # sintaxe de incremento com += igual a pt_dentro = pt_dentro + 1, se estiver dentro, soma 1

    if pt_sorteados < 5:
         print(f"Ponto {pt_sorteados + 1}: pt = {pt} -> {posicao}")

    pt_sorteados += 1              # se estiver dentro, soma 1

# %%
pi_mc = 4 * pt_dentro / pt_sorteados
print("\nEstimativa de pi =", pi_mc)

# %% [markdown]
# 

