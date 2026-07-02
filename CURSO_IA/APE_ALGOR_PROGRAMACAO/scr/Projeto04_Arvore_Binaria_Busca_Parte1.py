# %% [markdown]
# # Projeto 04 - Arvore Binaria de Busca (Parte 1)
#
# Neste projeto vou implementar uma Arvore Binaria de Busca, tambem chamada de
# BST, do ingles Binary Search Tree.
#
# A regra principal da arvore e:
#
# - valores menores que o nodo atual ficam do lado esquerdo;
# - valores maiores que o nodo atual ficam do lado direito;
# - valores repetidos serao ignorados nesta primeira versao.
#
# A parte 1 contem:
#
# - criacao da classe Nodo;
# - criacao da classe BST;
# - insercao de valores;
# - busca de valores;
# - caminhamento em ordem;
# - impressao simples da arvore;
# - remocao de valores.

# %%
class Nodo:
    """Representa um nodo da arvore."""

    def __init__(self, valor):
        # Cada nodo guarda um valor.
        self.valor = valor

        # O filho da esquerda recebe valores menores.
        self.esquerda = None

        # O filho da direita recebe valores maiores.
        self.direita = None


# %%
class BST:
    """Arvore Binaria de Busca."""

    def __init__(self):
        # Quando a arvore nasce, ela ainda nao tem raiz.
        self.raiz = None

    # -------------------------------------------------------------------------
    # Bloco 1 - Insercao
    # -------------------------------------------------------------------------
    def inserir(self, valor):
        """Insere um valor na arvore."""
        # Se a arvore esta vazia, o primeiro valor vira a raiz.
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            # Se ja existe raiz, procuro recursivamente o lugar certo.
            self._inserir_recursivo(self.raiz, valor)

    def _inserir_recursivo(self, nodo_atual, valor):
        """Procura recursivamente a posicao correta do novo valor."""
        if valor < nodo_atual.valor:
            # Se o valor e menor, devo ir para a esquerda.
            if nodo_atual.esquerda is None:
                nodo_atual.esquerda = Nodo(valor)
            else:
                self._inserir_recursivo(nodo_atual.esquerda, valor)

        elif valor > nodo_atual.valor:
            # Se o valor e maior, devo ir para a direita.
            if nodo_atual.direita is None:
                nodo_atual.direita = Nodo(valor)
            else:
                self._inserir_recursivo(nodo_atual.direita, valor)

        else:
            # Nesta versao, valores repetidos nao sao inseridos.
            print(f"Valor repetido ignorado: {valor}")

    # -------------------------------------------------------------------------
    # Bloco 2 - Busca
    # -------------------------------------------------------------------------
    def buscar(self, valor):
        """Retorna True se o valor existir na arvore, ou False caso contrario."""
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_atual, valor):
        """Busca um valor seguindo a regra da BST."""
        # Se cheguei em None, o valor nao foi encontrado.
        if nodo_atual is None:
            return False

        # Se o valor e igual ao valor do nodo atual, encontrei.
        if valor == nodo_atual.valor:
            return True

        # Se for menor, continuo procurando na subarvore esquerda.
        if valor < nodo_atual.valor:
            return self._buscar_recursivo(nodo_atual.esquerda, valor)

        # Se for maior, continuo procurando na subarvore direita.
        return self._buscar_recursivo(nodo_atual.direita, valor)

    # -------------------------------------------------------------------------
    # Bloco 3 - Caminhamento em ordem
    # -------------------------------------------------------------------------
    def listar_em_ordem(self):
        """Retorna uma lista com os valores em ordem crescente."""
        valores = []
        self._listar_em_ordem_recursivo(self.raiz, valores)
        return valores

    def _listar_em_ordem_recursivo(self, nodo_atual, valores):
        """Percorre esquerda, raiz e direita."""
        if nodo_atual is not None:
            # Primeiro visito todos os valores menores.
            self._listar_em_ordem_recursivo(nodo_atual.esquerda, valores)

            # Depois visito o proprio nodo.
            valores.append(nodo_atual.valor)

            # Por ultimo visito os valores maiores.
            self._listar_em_ordem_recursivo(nodo_atual.direita, valores)

    def exibir_em_ordem(self):
        """Imprime os valores da arvore em ordem crescente."""
        valores = self.listar_em_ordem()
        print("Caminhamento em ordem:", valores)

    # -------------------------------------------------------------------------
    # Bloco 4 - Impressao da estrutura da arvore
    # -------------------------------------------------------------------------
    def imprimir(self):
        """Mostra a estrutura da arvore de forma simples."""
        if self.raiz is None:
            print("(arvore vazia)")
            return

        print(f"raiz: {self.raiz.valor}")
        self._imprimir_recursivo(self.raiz.esquerda, "e")
        self._imprimir_recursivo(self.raiz.direita, "d")

    def _imprimir_recursivo(self, nodo_atual, lado, nivel=1):
        """Imprime os filhos indicando esquerda e direita."""
        if nodo_atual is None:
            return

        espacos = "  " * nivel
        print(f"{espacos}{lado}: {nodo_atual.valor}")

        self._imprimir_recursivo(nodo_atual.esquerda, "e", nivel + 1)
        self._imprimir_recursivo(nodo_atual.direita, "d", nivel + 1)

    # -------------------------------------------------------------------------
    # Bloco 5 - Remocao
    # -------------------------------------------------------------------------
    def remover(self, valor):
        """Remove um valor da arvore, se ele existir."""
        self.raiz = self._remover_recursivo(self.raiz, valor)

    def _remover_recursivo(self, nodo_atual, valor):
        """Remove um nodo mantendo a regra da Arvore Binaria de Busca."""
        # Se o nodo atual e None, o valor nao existe na arvore.
        if nodo_atual is None:
            return None

        # Primeiro procuro o nodo que deve ser removido.
        if valor < nodo_atual.valor:
            nodo_atual.esquerda = self._remover_recursivo(
                nodo_atual.esquerda,
                valor,
            )

        elif valor > nodo_atual.valor:
            nodo_atual.direita = self._remover_recursivo(
                nodo_atual.direita,
                valor,
            )

        else:
            # Agora encontrei o valor que precisa ser removido.
            # Caso 1: nodo sem filho esquerdo.
            if nodo_atual.esquerda is None:
                return nodo_atual.direita

            # Caso 2: nodo sem filho direito.
            if nodo_atual.direita is None:
                return nodo_atual.esquerda

            # Caso 3: nodo com dois filhos.
            # Uso o sucessor, que e o menor valor da subarvore direita.
            sucessor = self._menor_nodo(nodo_atual.direita)
            nodo_atual.valor = sucessor.valor

            # Depois de copiar o valor do sucessor, removo o sucessor antigo.
            nodo_atual.direita = self._remover_recursivo(
                nodo_atual.direita,
                sucessor.valor,
            )

        return nodo_atual

    def _menor_nodo(self, nodo_atual):
        """Encontra o menor nodo de uma subarvore."""
        while nodo_atual.esquerda is not None:
            nodo_atual = nodo_atual.esquerda

        return nodo_atual


# %% [markdown]
# ## Testando a implementacao

# %%
# Crio a arvore e insiro os mesmos valores usados no exemplo de aula.
minha_arvore = BST()
valores = [50, 30, 70, 20, 40, 60, 80]

for valor in valores:
    minha_arvore.inserir(valor)

# %%
# A impressao mostra a raiz e os filhos da esquerda/direita.
minha_arvore.imprimir()

# %%
# O caminhamento em ordem deve mostrar os valores em ordem crescente.
minha_arvore.exibir_em_ordem()

# %%
# Agora testo a busca de valores que existem e que nao existem na arvore.
print("Buscar 40:", minha_arvore.buscar(40))
print("Buscar 90:", minha_arvore.buscar(90))

# %%
# Removo o valor 30. Neste exemplo, 30 tem dois filhos: 20 e 40.
print("Removendo o 30...")
minha_arvore.remover(30)
minha_arvore.exibir_em_ordem()
minha_arvore.imprimir()

# %%
# Testes simples para conferir se a arvore esta funcionando.
assert minha_arvore.listar_em_ordem() == [20, 40, 50, 60, 70, 80]
assert minha_arvore.buscar(40) is True
assert minha_arvore.buscar(30) is False

print("Testes concluidos com sucesso.")
