# %% [markdown]
# # Projeto 05 - Calculadora RPN com entrada CSV e saida JSON
#
# Incremento sobre o Projeto 05 original.
#
# Nesta versao, a Arvore RPN passa a:
#
# 1. Ler expressoes a partir de um arquivo CSV.
# 2. Construir uma arvore binaria de expressao para cada linha.
# 3. Dumpar, ou salvar, a arvore em um arquivo JSON.
# 4. Reconstruir a arvore a partir do arquivo JSON.
# 5. Calcular novamente o resultado usando a arvore reconstruida.
#
# Arquivos usados:
#
# - Entrada CSV: `DADOS/expressoes_rpn.csv`
# - Saida JSON: `DADOS/arvores_rpn_projeto05.json`

# %%
import csv
import json
from collections import deque
from pathlib import Path


# %%
class NodoExpressao:
    """Representa um nodo da arvore de expressao matematica."""

    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


# %%
class CalculadoraRPNArquivos:
    """Calculadora RPN com leitura de CSV, dump JSON e reconstrucao da arvore."""

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
    # Bloco 1 - Tratamento da string RPN
    # -------------------------------------------------------------------------
    def separar_tokens(self, expressao):
        """Separa a string RPN em operandos e operadores."""
        return expressao.strip().split()

    def converter_token(self, token):
        """Converte cada token para numero ou operador padronizado."""
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

    # -------------------------------------------------------------------------
    # Bloco 2 - Construcao da arvore RPN
    # -------------------------------------------------------------------------
    def construir_arvore(self, expressao):
        """
        Constroi uma arvore a partir de uma expressao RPN.

        Numero vira nodo folha.
        Operador vira nodo pai, ligando dois nodos retirados da pilha.
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

        if len(pilha_arvore) != 1:
            raise ValueError("Expressao RPN invalida: sobraram operandos sem operador.")

        self.raiz = pilha_arvore.pop()
        return self.raiz

    # -------------------------------------------------------------------------
    # Bloco 3 - Caminhamento da arvore
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

    # -------------------------------------------------------------------------
    # Bloco 4 - Calculo usando pilha
    # -------------------------------------------------------------------------
    def calcular_fila(self):
        """Consome a fila RPN e calcula o resultado usando uma pilha."""
        self.pilha_execucao = []

        while len(self.fila_execucao) > 0:
            valor = self.fila_execucao.popleft()

            if isinstance(valor, (int, float)):
                self.pilha_execucao.append(valor)
            else:
                operando_direito = self.pilha_execucao.pop()
                operando_esquerdo = self.pilha_execucao.pop()
                resultado = self.aplicar_operacao(
                    valor,
                    operando_esquerdo,
                    operando_direito,
                )
                self.pilha_execucao.append(resultado)

        if len(self.pilha_execucao) != 1:
            raise ValueError("A pilha terminou com uma quantidade invalida de valores.")

        return self.pilha_execucao[0]

    def aplicar_operacao(self, operador, operando_esquerdo, operando_direito):
        """Executa a operacao matematica."""
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
    # Bloco 5 - Dump da arvore para JSON
    # -------------------------------------------------------------------------
    def nodo_para_dicionario(self, nodo_atual):
        """Converte um nodo da arvore para dicionario."""
        if nodo_atual is None:
            return None

        if isinstance(nodo_atual.valor, (int, float)):
            tipo = "operando"
        else:
            tipo = "operador"

        return {
            "valor": nodo_atual.valor,
            "tipo": tipo,
            "esquerda": self.nodo_para_dicionario(nodo_atual.esquerda),
            "direita": self.nodo_para_dicionario(nodo_atual.direita),
        }

    def dumpar_arvore_json(self, caminho_json, metadados=None):
        """Salva a arvore atual em um arquivo JSON."""
        if self.raiz is None:
            raise ValueError("Nao existe arvore para dumpar.")

        dados = {
            "metadados": metadados or {},
            "arvore": self.nodo_para_dicionario(self.raiz),
        }

        caminho_json = Path(caminho_json)
        caminho_json.parent.mkdir(parents=True, exist_ok=True)

        with caminho_json.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    # -------------------------------------------------------------------------
    # Bloco 6 - Reconstrucao da arvore a partir do JSON
    # -------------------------------------------------------------------------
    def dicionario_para_nodo(self, dados_nodo):
        """Reconstrui um nodo da arvore a partir de um dicionario."""
        if dados_nodo is None:
            return None

        nodo = NodoExpressao(dados_nodo["valor"])
        nodo.esquerda = self.dicionario_para_nodo(dados_nodo["esquerda"])
        nodo.direita = self.dicionario_para_nodo(dados_nodo["direita"])
        return nodo

    def reconstruir_arvore_json(self, caminho_json):
        """Le um arquivo JSON e reconstrui a arvore dentro do objeto."""
        caminho_json = Path(caminho_json)

        with caminho_json.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.raiz = self.dicionario_para_nodo(dados["arvore"])
        return self.raiz

    # -------------------------------------------------------------------------
    # Bloco 7 - Resolucao completa
    # -------------------------------------------------------------------------
    def calcular_arvore_atual(self):
        """Calcula o resultado usando a arvore que ja esta em self.raiz."""
        self.enfileirar_pos_ordem()
        return self.calcular_fila()

    def resolver(self, expressao):
        """Constroi a arvore e calcula a expressao RPN."""
        self.construir_arvore(expressao)
        return self.calcular_arvore_atual()


# %%
class ProcessadorCSVArvoreJSON:
    """Processa varias expressoes RPN de um CSV e gera um JSON consolidado."""

    def __init__(self, caminho_csv, caminho_json):
        self.caminho_csv = Path(caminho_csv)
        self.caminho_json = Path(caminho_json)

    def ler_expressoes_csv(self):
        """Le o arquivo CSV com as expressoes RPN."""
        expressoes = []

        with self.caminho_csv.open("r", encoding="utf-8-sig", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                expressoes.append(
                    {
                        "id": linha.get("id", "").strip(),
                        "descricao": linha.get("descricao", "").strip(),
                        "expressao_rpn": linha.get("expressao_rpn", "").strip(),
                    }
                )

        return expressoes

    def processar_csv(self):
        """Constroi uma arvore para cada expressao do CSV."""
        registros = []

        for linha in self.ler_expressoes_csv():
            calculadora = CalculadoraRPNArquivos()
            expressao = linha["expressao_rpn"]

            try:
                resultado = calculadora.resolver(expressao)

                registros.append(
                    {
                        "id": linha["id"],
                        "descricao": linha["descricao"],
                        "expressao_rpn": expressao,
                        "status": "ok",
                        "resultado": resultado,
                        "arvore": calculadora.nodo_para_dicionario(calculadora.raiz),
                    }
                )
            except Exception as erro:
                registros.append(
                    {
                        "id": linha["id"],
                        "descricao": linha["descricao"],
                        "expressao_rpn": expressao,
                        "status": "erro",
                        "erro": str(erro),
                    }
                )

        return registros

    def dumpar_registros_json(self, registros):
        """Salva todas as arvores processadas em um unico arquivo JSON."""
        dados = {
            "origem_csv": str(self.caminho_csv),
            "total_registros": len(registros),
            "registros": registros,
        }

        self.caminho_json.parent.mkdir(parents=True, exist_ok=True)

        with self.caminho_json.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def reconstruir_registros_json(self):
        """Le o JSON consolidado e reconstrui cada arvore salva nele."""
        with self.caminho_json.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        reconstruidos = []

        for registro in dados["registros"]:
            if registro["status"] != "ok":
                reconstruidos.append(registro)
                continue

            calculadora = CalculadoraRPNArquivos()
            calculadora.raiz = calculadora.dicionario_para_nodo(registro["arvore"])
            resultado_reconstruido = calculadora.calcular_arvore_atual()

            reconstruidos.append(
                {
                    "id": registro["id"],
                    "descricao": registro["descricao"],
                    "expressao_rpn": registro["expressao_rpn"],
                    "resultado_original": registro["resultado"],
                    "resultado_reconstruido": resultado_reconstruido,
                }
            )

        return reconstruidos

    def executar(self):
        """Executa o fluxo completo: CSV -> arvores -> JSON -> reconstrucao."""
        registros = self.processar_csv()
        self.dumpar_registros_json(registros)
        reconstruidos = self.reconstruir_registros_json()
        return registros, reconstruidos


# %%
if __name__ == "__main__":
    pasta_atual = Path(__file__).resolve().parent
    caminho_csv = pasta_atual / "DADOS" / "expressoes_rpn.csv"
    caminho_json = pasta_atual / "DADOS" / "arvores_rpn_projeto05.json"

    processador = ProcessadorCSVArvoreJSON(caminho_csv, caminho_json)
    registros, reconstruidos = processador.executar()

    print("Projeto 05 incrementado executado com sucesso.")
    print(f"CSV lido: {caminho_csv}")
    print(f"JSON gerado: {caminho_json}")
    print(f"Expressoes processadas: {len(registros)}")

    print("\nResultados reconstruidos a partir do JSON:")
    for item in reconstruidos:
        if "resultado_reconstruido" in item:
            print(
                f"{item['id']} - {item['descricao']}: "
                f"{item['resultado_reconstruido']}"
            )
        else:
            print(f"{item['id']} - erro: {item.get('erro')}")
