# %% [markdown]
# ## Projeto 04 - Insertion Sort
#
# O Insertion Sort ordena a lista como se estivessemos organizando cartas na mao.
#
# A cada passo, ele escolhe um elemento chamado `chave`, compara com os elementos anteriores e insere essa chave na posicao correta da parte ja ordenada.

# %% [markdown]
# Celula 01 - Implementacao

# %%
def insertion_sort(valores, mostrar_passos=False):
    """Ordena uma lista usando Insertion Sort e retorna uma nova lista."""
    # Faco uma copia para preservar a lista original.
    ordenada = valores.copy()

    # Estes contadores ajudam a entender quanto trabalho o algoritmo fez.
    comparacoes = 0
    deslocamentos = 0

    # Comeco no indice 1 porque uma lista com apenas o primeiro item ja esta ordenada.
    for indice in range(1, len(ordenada)):
        # A chave e o valor que vou encaixar na parte esquerda da lista.
        chave = ordenada[indice]
        posicao = indice - 1

        # Enquanto houver valores maiores que a chave, empurro esses valores para a direita.
        while posicao >= 0:
            comparacoes += 1

            # Quando encontro um valor menor ou igual, achei o lugar da chave.
            if ordenada[posicao] <= chave:
                break

            # Desloca o valor maior uma casa para a direita.
            ordenada[posicao + 1] = ordenada[posicao]
            deslocamentos += 1
            posicao -= 1

        # Coloco a chave na posicao correta, depois dos valores menores que ela.
        ordenada[posicao + 1] = chave

        # Esta opcao mostra a lista depois de cada insercao.
        if mostrar_passos:
            print(f"Inserindo {chave}: {ordenada}")

    # Retorno a lista ordenada e tambem os contadores para analise.
    return {
        "lista_ordenada": ordenada,
        "comparacoes": comparacoes,
        "deslocamentos": deslocamentos,
    }

# %% [markdown]
# Celula 02 - Exemplo com passo a passo

# %%
# Lista usada como exemplo. Ela permite ver bem os deslocamentos.
numeros = [42, 7, 91, 13, 58, 24, 76, 3, 65, 30]

resultado = insertion_sort(numeros, mostrar_passos=True)

print("\nLista original: ", numeros)
print("Lista ordenada:", resultado["lista_ordenada"])
print("Comparacoes:   ", resultado["comparacoes"])
print("Deslocamentos: ", resultado["deslocamentos"])

# %% [markdown]
# Celula 04 -  Funcao auxiliar para imprimir listas

# %%
def mostrar_resultado(nome, lista):
    # Esta funcao deixa os testes mais organizados e evita repetir codigo.
    resultado = insertion_sort(lista)
    print(f"{nome}")
    print("  original:", lista)
    print("  ordenada:", resultado["lista_ordenada"])
    print("  comparacoes:", resultado["comparacoes"])
    print("  deslocamentos:", resultado["deslocamentos"])
    print()

# %% [markdown]
# Celulas 05 - Testando diferentes entradas

# %%
# Testo casos diferentes para ter mais confianca na implementacao.
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
# Celulas 06 - Conferindo com testes automatizados

# %%
# Comparo meu resultado com o sorted do Python.
for lista in listas_de_teste.values():
    assert insertion_sort(lista)["lista_ordenada"] == sorted(lista)

# Confere que a lista original nao foi alterada.
original = [3, 1, 2]
ordenada = insertion_sort(original)["lista_ordenada"]
assert original == [3, 1, 2]
assert ordenada == [1, 2, 3]

print("Testes concluidos com sucesso.")

# %% [markdown]
# ### Observacao sobre desempenho
#
# O Insertion Sort costuma ser bom para listas pequenas ou quase ordenadas. No pior caso, como em uma lista totalmente invertida, ele precisa fazer muitos deslocamentos.

