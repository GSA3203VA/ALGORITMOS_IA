#!/usr/bin/env python
# coding: utf-8

# ## Projeto 05 - Calculadora RPN com Arvore Binaria
# Nome: Giovanni Andrade
# OBS: Apos horas de estudo, entendi os conceitos:
# - de arvoré basica;
# - uma arvore com expressão, tem uma expressão logica ou matematica ou simbolos;
# - uma arvore BST (Binary Search Tree), permite uma procura, inserção, remocão de nós usado para armazenar e gerenciar dados;
# - Com base em exemplos, e as IAs como Chat, Codex, foi entendo linha a linha o codigo. 
# 
# 
# RPN significa Notacao Polonesa Reversa. Em RPN, os operadores aparecem depois dos operandos.
# 
# Exemplo:
# 
# ```text
# 10 17 +
# ```
# 
# significa:
# 
# ```text
# 10 + 17
# ```
# 
# A partir do exercicio da Aula 4 temos quatro etapas:
# 
# 1. Ler uma string que representa um conjunto de operacoes em notacao RPN.
# 2. Construir uma arvore binaria que representa as operacoes a serem feitas.
# 3. Caminhar na arvore para enfileirar operandos e operadores adequadamente.
# 4. Utilizar uma pilha para implementar o algoritmo de calculo baseado na notacao RPN.
# 5. Lembrando que:
# Se o valor novo for menor que o nó atual:
#     vou para a esquerda
# 
# Se o valor novo for maior que o nó atual:
#     vou para a direita
# 
# Se não existir nó naquela direção:
#     insiro ali

# In[ ]:


# Importa a estrutura deque da biblioteca collections.
# O deque será usado como fila, permitindo retirar elementos do início com popleft().
from collections import deque


# Celula 01 - Classe do nodo
# 
# Cada nodo guarda um valor e duas referencias: filho da esquerda e filho da direita.

# In[2]:


class NodoExpressao:
    """Representa um nodo da arvore de expressao matematica
    cada no (nodo) precisa de 
    valor raiz
    valor da esquerda
    valor da direita
    """

    def __init__(self, valor): #construir os valores
        self.valor = valor     #guarda o valor do NodoExpressão
        self.esquerda = None    #cria um valor do filho a esquerda
        self.direita = None     # cria um valor do filho a direita (inicial vazio)


# Celula 02 - Calculadora RPN
# 
# A calculadora usa tres estruturas principais:
# 
# - arvore binaria de expressao;
# - fila para guardar o caminhamento em pos-ordem;
# - pilha para calcular a expressao RPN.

# In[ ]:


# Define a classe principal da calculadora.
# Ela usa árvore, fila e pilha para resolver uma expressão em RPN.

class CalculadoraRPN:
     # Dicionário com os operadores aceitos pela calculadora.
    OPERADORES = {
        "+": "SOMA",
        "-": "SUBTRACAO",
        "*": "MULTIPLICACAO",
        "/": "DIVISAO",
        "SOMA": "SOMA",
        "SUBTRACAO": "SUBTRACAO",
        "SUBTRAÇÃO": "SUBTRACAO",
        "MULTIPLICACAO": "MULTIPLICACAO",
        "MULTIPLICAÇÃO": "MULTIPLICACAO",
        "DIVISAO": "DIVISAO",
        "DIVISÃO": "DIVISAO",
    }

    def __init__(self):
        self.raiz = None
        self.fila_execucao = deque()
        self.pilha_execucao = []

    # -------------------------------------------------------------------------
    # Bloco 1 - Leitura e tratamento da string RPN
    # -------------------------------------------------------------------------

    # Método responsável por separar a expressão em partes menores.
    def separar_tokens(self, expressao):
        """Separa a string em operandos e operadores."""
        return expressao.strip().split()

     # Método responsável por converter cada token.
     # Token é cada pedaço da expressão.
    def converter_token(self, token):
        """Converte numeros para float e operadores para nomes padronizados."""
        token_maiusculo = token.upper()

        # Verifica se o token está no dicionário de operadores.
        if token_maiusculo in self.OPERADORES:

            # Se for operador, retorna o nome padronizado.
            return self.OPERADORES[token_maiusculo]

         # Se não for operador, o programa tenta converter para número.
        try:

            # Substitui vírgula por ponto para aceitar números como "3,5".
            # Depois converte para float.
            numero = float(token.replace(",", "."))

            # Verifica se o número convertido é inteiro.
            # Exemplo: 3.0 pode ser convertido para 3.
            if numero.is_integer():

                # Retorna o número como inteiro.
                return int(numero)

            # Se não for inteiro, retorna como float.  
            return numero

         # Se não conseguir converter para número, gera erro.
        except ValueError:

            # Informa qual token é inválido.
            raise ValueError(f"Token invalido na expressao RPN: {token}")

    # -------------------------------------------------------------------------
    # Bloco 2 - Construcao da arvore binaria de expressao
    # -------------------------------------------------------------------------

     # Método que constrói a árvore a partir da expressão RPN.
    def construir_arvore(self, expressao):
        """
        Constroi a arvore a partir da expressao RPN.
        Para cada numero, empilho um nodo folha.
        Para cada operador, desempilho dois nodos e crio um novo nodo pai.
        """
        # Cria uma pilha vazia para montar a árvore.
        # Essa pilha armazena nodos, não números diretamente.
        pilha_arvore = []
        # Separa a expressão em tokens.
        tokens = self.separar_tokens(expressao)

        # Verifica se a expressão está vazia.
        if len(tokens) == 0:
             # Se estiver vazia, gera erro.
            raise ValueError("A expressao RPN nao pode ficar vazia.")

        # Percorre cada token da expressão.
        for token in tokens:

            # Converte o token para número ou operador padronizado.
            valor = self.converter_token(token)

             # Cria um novo nodo para armazenar esse valor.
            nodo = NodoExpressao(valor)

             # Verifica se o valor é número.
            if isinstance(valor, (int, float)):

                # Se for número, ele é uma folha da árvore.
                # Por isso, apenas empilha o nodo.
                pilha_arvore.append(nodo)

                # Mostra na tela o que aconteceu.
                print(f"ARVORE PUSH: {valor} | Pilha de nodos: {len(pilha_arvore)}")

            # Se não for número, então é operador.    
            else:

                # Para aplicar um operador binário, são necessários dois operandos.
                # Por isso, a pilha precisa ter pelo menos dois nodos.
                if len(pilha_arvore) < 2:

                    # Se não tiver dois operandos, a expressão RPN está incorreta.
                    raise ValueError(
                        f"Operador {token} nao possui dois operandos disponiveis."
                    )
                #remove os filhos
                filho_direito = pilha_arvore.pop()
                filho_esquerdo = pilha_arvore.pop()

                #Liga os filhos
                nodo.esquerda = filho_esquerdo
                nodo.direita = filho_direito

                # Empilha o nodo operador.
                # Agora esse operador representa uma subárvore.
                pilha_arvore.append(nodo)
                # Mostra na tela como o operador foi ligado aos filhos.
                print(
                    f"ARVORE OP: {valor} | "
                    f"esquerda={filho_esquerdo.valor}, direita={filho_direito.valor}"
                )
        # No final, a pilha deve conter apenas um nodo.
        # Esse nodo será a raiz da árvore inteira.
        if len(pilha_arvore) != 1:

            # Se sobrar mais de um nodo, faltaram operadores na expressão.
            raise ValueError("Expressao RPN invalida: sobraram operandos sem operador.")

        # Remove o último nodo da pilha e define como raiz da árvore. 
        self.raiz = pilha_arvore.pop()
        # Retorna a raiz da árvore construída.
        return self.raiz

    # -------------------------------------------------------------------------
    # Bloco 3 - Caminhamento da arvore para enfileirar a RPN
    # -------------------------------------------------------------------------
    def enfileirar_pos_ordem(self):
        """Percorre a arvore em pos-ordem e guarda os valores em uma fila."""
        self.fila_execucao = deque()
        self._enfileirar_pos_ordem_recursivo(self.raiz)
        return self.fila_execucao

    def _enfileirar_pos_ordem_recursivo(self, nodo_atual):
        """Percorre esquerda, direita e raiz."""
        if nodo_atual is not None:
            self._enfileirar_pos_ordem_recursivo(nodo_atual.esquerda)
            self._enfileirar_pos_ordem_recursivo(nodo_atual.direita)

            self.fila_execucao.append(nodo_atual.valor)
            print(f"ENFILEIRA: {nodo_atual.valor} | Fila: {list(self.fila_execucao)}")

    # -------------------------------------------------------------------------
    # Bloco 4 - Calculo usando pilha
    # -------------------------------------------------------------------------
    def calcular_fila(self):
        """Consome a fila RPN e calcula o resultado usando pilha."""
        self.pilha_execucao = []

        while len(self.fila_execucao) > 0:
            valor = self.fila_execucao.popleft()

            if isinstance(valor, (int, float)):
                self.pilha_execucao.append(valor)
                print(f"PUSH: {valor} | Pilha: {self.pilha_execucao}")
            else:
                operando_direito = self.pilha_execucao.pop()
                operando_esquerdo = self.pilha_execucao.pop()
                resultado = self.aplicar_operacao(
                    valor,
                    operando_esquerdo,
                    operando_direito,
                )

                self.pilha_execucao.append(resultado)
                print(
                    f"OP {valor}: {operando_esquerdo} e {operando_direito} "
                    f"| Resultado: {resultado} | Pilha: {self.pilha_execucao}"
                )

        if len(self.pilha_execucao) != 1:
            raise ValueError("A pilha terminou com uma quantidade invalida de valores.")

        return self.pilha_execucao[0]

    def aplicar_operacao(self, operador, operando_esquerdo, operando_direito):
        """Executa a operacao matematica indicada pelo operador."""
        if operador == "SOMA":
            return operando_esquerdo + operando_direito

        if operador == "SUBTRACAO":
            return operando_esquerdo - operando_direito

        if operador == "MULTIPLICACAO":
            return operando_esquerdo * operando_direito

        if operador == "DIVISAO":
            if operando_direito == 0:
                raise ZeroDivisionError("Nao e possivel dividir por zero.")

            return operando_esquerdo / operando_direito

        raise ValueError(f"Operador desconhecido: {operador}")

    # -------------------------------------------------------------------------
    # Bloco 5 - Funcoes auxiliares de exibicao
    # -------------------------------------------------------------------------
    def imprimir_arvore(self):
        """Mostra a estrutura da arvore de expressao."""
        if self.raiz is None:
            print("(arvore vazia)")
            return

        print(f"raiz: {self.raiz.valor}")
        self._imprimir_arvore_recursivo(self.raiz.esquerda, "e")
        self._imprimir_arvore_recursivo(self.raiz.direita, "d")

    def _imprimir_arvore_recursivo(self, nodo_atual, lado, nivel=1):
        """Imprime os filhos indicando esquerda e direita."""
        if nodo_atual is None:
            return

        espacos = "  " * nivel
        print(f"{espacos}{lado}: {nodo_atual.valor}")

        self._imprimir_arvore_recursivo(nodo_atual.esquerda, "e", nivel + 1)
        self._imprimir_arvore_recursivo(nodo_atual.direita, "d", nivel + 1)

    def resolver(self, expressao):
        """Executa todas as etapas do exercicio."""
        print("\n1) Lendo a string RPN:")
        print(expressao)

        print("\n2) Construindo a arvore:")
        self.construir_arvore(expressao)
        self.imprimir_arvore()

        print("\n3) Caminhando na arvore e enfileirando em pos-ordem:")
        self.enfileirar_pos_ordem()

        print("\n4) Calculando com pilha:")
        return self.calcular_fila()


# Celula 03 - Teste com uma expressao RPN
# 
# A expressao abaixo representa:
# 
# ```text
# (10 + 17) + (120 / 5)
# ```

# In[4]:


calculadora = CalculadoraRPN()
expressao = "10 17 + 120 5 / +"

resultado_final = calculadora.resolver(expressao)
print(f"\nResultado final: {resultado_final}")


# Celula 04 - Testes simples

# In[5]:


assert CalculadoraRPN().resolver("10 17 +") == 27
assert CalculadoraRPN().resolver("120 5 /") == 24
assert CalculadoraRPN().resolver("15 15 *") == 225
assert CalculadoraRPN().resolver("517 17 -") == 500

print("Testes concluidos com sucesso.")

