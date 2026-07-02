from collections import deque


# ==============================================================================
# Projeto 05 - Calculadora RPN com Arvore Binaria
#
# RPN significa Notacao Polonesa Reversa.
# Em RPN, os operadores aparecem depois dos operandos.
#
# Exemplo:
#     10 17 +
# significa:
#     10 + 17
#
# O exercicio pede quatro etapas:
# 1) ler uma string RPN;
# 2) construir uma arvore binaria que representa a expressao;
# 3) caminhar na arvore para enfileirar operandos e operadores;
# 4) usar uma pilha para calcular o resultado.
# ==============================================================================


class NodoExpressao:
    """Representa um nodo da arvore de expressao."""

    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


class CalculadoraRPN:
    """Calculadora baseada em arvore, fila e pilha."""

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
    def separar_tokens(self, expressao):
        """Separa a string em operandos e operadores."""
        return expressao.strip().split()

    def converter_token(self, token):
        """Converte numeros para float e operadores para nomes padronizados."""
        token_maiusculo = token.upper()

        if token_maiusculo in self.OPERADORES:
            return self.OPERADORES[token_maiusculo]

        try:
            numero = float(token.replace(",", "."))

            if numero.is_integer():
                return int(numero)

            return numero
        except ValueError:
            raise ValueError(f"Token invalido na expressao RPN: {token}")

    def eh_operador(self, valor):
        """Verifica se o valor representa uma operacao matematica."""
        return valor in {
            "SOMA",
            "SUBTRACAO",
            "MULTIPLICACAO",
            "DIVISAO",
        }

    # -------------------------------------------------------------------------
    # Bloco 2 - Construcao da arvore binaria de expressao
    # -------------------------------------------------------------------------
    def construir_arvore(self, expressao):
        """
        Constroi a arvore a partir da expressao RPN.

        Para cada numero, empilho um nodo folha.
        Para cada operador, desempilho dois nodos e crio um novo nodo pai.
        """
        pilha_arvore = []
        tokens = self.separar_tokens(expressao)

        if len(tokens) == 0:
            raise ValueError("A expressao RPN nao pode ficar vazia.")

        for token in tokens:
            valor = self.converter_token(token)
            nodo = NodoExpressao(valor)

            if isinstance(valor, (int, float)):
                pilha_arvore.append(nodo)
                print(f"ARVORE PUSH: {valor} | Pilha de nodos: {len(pilha_arvore)}")
            else:
                if len(pilha_arvore) < 2:
                    raise ValueError(
                        f"Operador {token} nao possui dois operandos disponiveis."
                    )

                filho_direito = pilha_arvore.pop()
                filho_esquerdo = pilha_arvore.pop()

                nodo.esquerda = filho_esquerdo
                nodo.direita = filho_direito

                pilha_arvore.append(nodo)
                print(
                    f"ARVORE OP: {valor} | "
                    f"esquerda={filho_esquerdo.valor}, direita={filho_direito.valor}"
                )

        if len(pilha_arvore) != 1:
            raise ValueError("Expressao RPN invalida: sobraram operandos sem operador.")

        self.raiz = pilha_arvore.pop()
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


if __name__ == "__main__":
    calculadora = CalculadoraRPN()

    try:
        expressao_digitada = input(
            "Digite uma expressao RPN. Exemplo: 10 17 + 120 5 / +\n> "
        )
    except EOFError:
        expressao_digitada = ""

    if expressao_digitada.strip() == "":
        expressao_digitada = "10 17 + 120 5 / +"
        print(f"Usando exemplo padrao: {expressao_digitada}")

    resultado_final = calculadora.resolver(expressao_digitada)
    print(f"\nResultado final: {resultado_final}")
