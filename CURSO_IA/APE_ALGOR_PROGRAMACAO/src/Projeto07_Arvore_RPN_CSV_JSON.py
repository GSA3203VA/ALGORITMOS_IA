# %% [markdown]
# # Projeto 07 - Arvore RPN com CSV e JSON
#
# Neste projeto vou implementar uma arvore de expressao RPN que:
#
# 1. Le expressoes RPN a partir de um arquivo CSV.
# 2. Constroi uma arvore binaria para cada expressao.
# 3. Calcula o resultado usando a mesma logica de pilha do Projeto 05.
# 4. Dumpa, ou salva, a arvore em um arquivo JSON.
#
# Arquivos usados:
#
# - entrada: `DADOS/expressoes_rpn.csv`
# - saida: `DADOS/arvores_rpn.json`

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
class ArvoreRPN:
    """Arvore de expressao baseada em Notacao Polonesa Reversa."""

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
    # Bloco 1 - Tratamento da expressao RPN
    # -------------------------------------------------------------------------
    def separar_tokens(self, expressao):
        """Separa a expressao RPN em tokens."""
        return expressao.strip().split()

    def converter_token(self, token):
        """Converte o token para numero ou operador padronizado."""
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
    # Bloco 2 - Construcao da arvore
    # -------------------------------------------------------------------------
    def construir_arvore(self, expressao):
        """
        Constroi a arvore de expressao.

        Numeros viram folhas.
        Operadores viram nodos internos com filho esquerdo e filho direito.
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
    # Bloco 3 - Caminhamento em pos-ordem
    # -------------------------------------------------------------------------
    def enfileirar_pos_ordem(self):
        """Percorre a arvore em pos-ordem e salva os valores em uma fila."""
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
        """Calcula a expressao consumindo a fila RPN com uma pilha."""
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
    # Bloco 5 - Conversao da arvore para dicionario
    # -------------------------------------------------------------------------
    def nodo_para_dicionario(self, nodo_atual):
        """Converte um nodo da arvore para um dicionario compativel com JSON."""
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

    def resolver(self, expressao):
        """Constroi a arvore, percorre em pos-ordem e calcula o resultado."""
        self.construir_arvore(expressao)
        fila = self.enfileirar_pos_ordem()
        percurso_pos_ordem = list(fila)
        resultado = self.calcular_fila()

        return {
            "tokens": self.separar_tokens(expressao),
            "percurso_pos_ordem": percurso_pos_ordem,
            "resultado": resultado,
            "arvore": self.nodo_para_dicionario(self.raiz),
        }


# %%
class Projeto07CSVJSON:
    """Coordena a leitura do CSV e a gravacao do JSON."""

    def __init__(self, caminho_csv, caminho_json):
        self.caminho_csv = Path(caminho_csv)
        self.caminho_json = Path(caminho_json)

    def ler_expressoes_csv(self):
        """Le as expressoes RPN de um arquivo CSV."""
        expressoes = []

        with self.caminho_csv.open("r", encoding="utf-8-sig", newline="") as arquivo:
            amostra = arquivo.read(1024)
            arquivo.seek(0)

            dialecto = csv.Sniffer().sniff(amostra, delimiters=",;")
            leitor = csv.DictReader(arquivo, dialect=dialecto)

            for linha in leitor:
                expressoes.append(
                    {
                        "id": linha.get("id", "").strip(),
                        "descricao": linha.get("descricao", "").strip(),
                        "expressao_rpn": linha.get("expressao_rpn", "").strip(),
                    }
                )

        return expressoes

    def processar(self):
        """Processa todas as linhas do CSV e monta a lista de saida."""
        saida = []

        for linha in self.ler_expressoes_csv():
            arvore = ArvoreRPN()
            expressao = linha["expressao_rpn"]

            try:
                dados_arvore = arvore.resolver(expressao)

                saida.append(
                    {
                        "id": linha["id"],
                        "descricao": linha["descricao"],
                        "expressao_rpn": expressao,
                        "status": "ok",
                        **dados_arvore,
                    }
                )
            except Exception as erro:
                saida.append(
                    {
                        "id": linha["id"],
                        "descricao": linha["descricao"],
                        "expressao_rpn": expressao,
                        "status": "erro",
                        "erro": str(erro),
                    }
                )

        return saida

    def salvar_json(self, dados):
        """Salva os dados processados em JSON."""
        self.caminho_json.parent.mkdir(parents=True, exist_ok=True)

        with self.caminho_json.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def executar(self):
        """Executa o fluxo completo: CSV -> Arvore RPN -> JSON."""
        dados = self.processar()
        self.salvar_json(dados)
        return dados


# %%
if __name__ == "__main__":
    pasta_atual = Path(__file__).resolve().parent
    caminho_csv = pasta_atual / "DADOS" / "expressoes_rpn.csv"
    caminho_json = pasta_atual / "DADOS" / "arvores_rpn.json"

    projeto = Projeto07CSVJSON(caminho_csv, caminho_json)
    resultado = projeto.executar()

    print("Projeto 07 executado com sucesso.")
    print(f"Arquivo CSV lido: {caminho_csv}")
    print(f"Arquivo JSON gerado: {caminho_json}")
    print(f"Total de expressoes processadas: {len(resultado)}")
