

# Tarefa 04 - Arvore Binaria de Busca

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None  # Filho 1 (Menor)
        self.direita = None   # Filho 2 (Maior)

class BST:
    def __init__(self):
        self.raiz = None

    # Bloco 2 - Método para inserir valores-----------------------------------------------------

    def inserir(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._inserir_recursivo(self.raiz, valor)

    def _inserir_recursivo(self, nodo_atual, valor):
        if valor < nodo_atual.valor:
            if nodo_atual.esquerda is None:
                nodo_atual.esquerda = Nodo(valor)
            else:
                self._inserir_recursivo(nodo_atual.esquerda, valor)
        elif valor > nodo_atual.valor:
            if nodo_atual.direita is None:
                nodo_atual.direita = Nodo(valor)
            else:
                self._inserir_recursivo(nodo_atual.direita, valor)

    # Bloco 3 - Função que percorre a árvore "In-order" (em ordem)------------------------------------
   
    def exibir_em_ordem(self):
        print("Caminhamento em Ordem:", end=" ")
        self._percorrer_em_ordem(self.raiz)
        print()

    def _percorrer_em_ordem(self, nodo):
        if nodo:
            self._percorrer_em_ordem(nodo.esquerda)
            print(nodo.valor, end=" ")
            self._percorrer_em_ordem(nodo.direita)

    # Bloco 4 - Função para remover um valor
   
    def remover(self, valor):
        self.raiz = self._remover_recursivo(self.raiz, valor)

    def _remover_recursivo(self, nodo, valor):
        if nodo is None:
            return nodo

        # Busca o nó a ser removido
        #======================================================
        if valor < nodo.valor:
            nodo.esquerda = self._remover_recursivo(nodo.esquerda, valor)
        elif valor > nodo.valor:
            nodo.direita = self._remover_recursivo(nodo.direita, valor)
        else:
            # Caso 1 e 2: Nó com apenas um filho ou nenhum
            #======================================================
            if nodo.esquerda is None:
                return nodo.direita
            elif nodo.direita is None:
                return nodo.esquerda

            # Caso 3: Nó com dois filhos
            # Precisamos encontrar o sucessor (menor valor da subárvore direita)
            #======================================================
            sucessor = self._min_valor_nodo(nodo.direita)
            nodo.valor = sucessor.valor
            # Remove o sucessor que foi movido para o lugar do nó atual
            #======================================================
            nodo.direita = self._remover_recursivo(nodo.direita, sucessor.valor)

        return nodo

    def _min_valor_nodo(self, nodo):
        atual = nodo
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

#Bloco 5 - Testando a implementação -------------------------

minha_arvore = BST()
valores = [50, 30, 70, 20, 40, 60, 80]

for v in valores:
    minha_arvore.inserir(v)

minha_arvore.exibir_em_ordem() # Esperado: 20 30 40 50 60 70 80

print("Removendo o 30 (nó com dois filhos)...")
minha_arvore.remover(30)
minha_arvore.exibir_em_ordem() # Esperado: 20 40 50 60 70 80