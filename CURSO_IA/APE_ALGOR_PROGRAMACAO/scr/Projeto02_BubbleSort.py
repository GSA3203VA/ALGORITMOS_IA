# %% [markdown]
# # Projeto 02 - Bubble Sort
#
# O Bubble Sort e um algoritmo de ordenacao simples. Ele percorre a lista varias vezes, compara elementos vizinhos e troca os dois de lugar quando estao fora de ordem.
#
# Depois de cada passada completa, o maior elemento restante fica na posicao correta no fim da lista.

# %% [markdown]
# ## Implementacao

# %%
def bubble_sort(valores, mostrar_passos=False):
    """Ordena uma lista usando Bubble Sort e retorna uma nova lista."""
    # Faco uma copia para nao modificar a lista original que foi passada para a funcao.
    ordenada = valores.copy()
    tamanho = len(ordenada)

    # Estes contadores nao sao obrigatorios para ordenar, mas ajudam a estudar o algoritmo.
    comparacoes = 0
    trocas = 0

    # Cada passada empurra o maior valor ainda nao ordenado para o final da lista.
    for passada in range(tamanho - 1):
        # Se uma passada inteira nao fizer troca, a lista ja esta ordenada.
        houve_troca = False

        # No fim de cada passada ja existe um elemento na posicao correta,
        # por isso o limite diminui com "passada".
        for indice in range(tamanho - passada - 1):
            comparacoes += 1

            # Comparo sempre elementos vizinhos.
            if ordenada[indice] > ordenada[indice + 1]:
                # Se estiverem fora de ordem, troco as duas posicoes.
                ordenada[indice], ordenada[indice + 1] = ordenada[indice + 1], ordenada[indice]
                trocas += 1
                houve_troca = True

        # Esta impressao e util para acompanhar a evolucao da lista em aula.
        if mostrar_passos:
            print(f"Passada {passada + 1}: {ordenada}")

        # Otimizacao simples: se nao houve troca, nao preciso continuar.
        if not houve_troca:
            break

    # Retorno tambem as estatisticas para comparar com outros algoritmos.
    return {
        "lista_ordenada": ordenada,
        "comparacoes": comparacoes,
        "trocas": trocas,
    }

# %% [markdown]
# ## Exemplo com passo a passo

# %%
# Lista usada como exemplo. Ela tem numeros fora de ordem para mostrar as trocas.
numeros = [42, 7, 91, 13, 58, 24, 76, 3, 65, 30]

resultado = bubble_sort(numeros, mostrar_passos=True)

print("\nLista original: ", numeros)
print("Lista ordenada:", resultado["lista_ordenada"])
print("Comparacoes:   ", resultado["comparacoes"])
print("Trocas:        ", resultado["trocas"])

# %% [markdown]
# ## Funcao auxiliar para imprimir listas

# %%
def mostrar_resultado(nome, lista):
    # Esta funcao evita repetir os mesmos prints para cada lista de teste.
    resultado = bubble_sort(lista)
    print(f"{nome}")
    print("  original:", lista)
    print("  ordenada:", resultado["lista_ordenada"])
    print("  comparacoes:", resultado["comparacoes"])
    print("  trocas:", resultado["trocas"])
    print()

# %% [markdown]
# ## Testando diferentes entradas

# %%
# Testo casos diferentes para verificar se o algoritmo funciona em situacoes comuns.
listas_de_teste = {
    "lista vazia": [],
    "um elemento": [5],
    "ja ordenada": [1, 2, 3, 4, 5],
    "invertida": [5, 4, 3, 2, 1],
    "com repetidos": [4, 2, 4, 1, 3, 2],
    "com negativos": [3, -1, 0, -5, 8, 2],
}

for nome, lista in listas_de_teste.items():
    mostrar_resultado(nome, lista)

# %% [markdown]
# ## Conferindo com testes automatizados

# %%
# Comparo meu Bubble Sort com o sorted do Python, que ja e confiavel.
for lista in listas_de_teste.values():
    assert bubble_sort(lista)["lista_ordenada"] == sorted(lista)

# Confere que a lista original nao foi alterada.
original = [3, 1, 2]
ordenada = bubble_sort(original)["lista_ordenada"]
assert original == [3, 1, 2]
assert ordenada == [1, 2, 3]

print("Testes concluidos com sucesso.")

# %% [markdown]
# ## Observacao sobre desempenho
#
# No pior caso, o Bubble Sort faz muitas comparacoes. Para listas grandes, algoritmos mais eficientes costumam ser preferidos. Ainda assim, ele e excelente para estudar lacos, comparacoes e trocas.

