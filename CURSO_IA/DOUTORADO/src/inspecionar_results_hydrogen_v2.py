"""Inspecao (somente leitura) da base results_hydrogen_v2.csv.

O arquivo possui tres blocos de cabecalho/dados:
    linha 1        -> nomes das features;
    linha 2        -> unidades das features;
    linha 3 em diante -> dados experimentais.

Este script NAO altera, filtra nem limpa o CSV original. Ele apenas
extrai metadados de cada coluna (posicao, nome, unidade, tipo inferido)
e imprime um relatorio de validacao no terminal, alem de gerar a tabela
markdown usada em Docs/ricardo.md.

Nao inventa unidades: quando a linha 2 esta vazia para uma coluna, a
unidade e reportada como ausente, mesmo que fisicamente exista uma
unidade obvia para a grandeza.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "dados_amostra"
CSV_PATH = DATA_DIR / "results_hydrogen_v2.csv"
XLSX_PATH = DATA_DIR / "results_hydrogen_v2.xlsx"
DOCS_DIR = ROOT_DIR / "Docs"

CSV_ENCODING = "utf-8-sig"
CSV_SEPARATOR = ";"

# Tokens que representam ausencia de valor nos dados experimentais.
# Nao inclui "-" sozinho quando usado como unidade (isso e tratado a
# parte, na leitura da linha de unidades).
NULL_TOKENS = {"", "-", "--", "n/a", "na", "none", "nan", "null", "?", "#n/a"}


@dataclass
class FeatureInfo:
    """Metadados de uma unica coluna do CSV."""

    posicao: int  # 1-indexado, para exibicao amigavel
    indice: int  # 0-indexado, posicao real no arquivo
    nome_bruto: str
    unidade_bruta: str
    tipo: str
    nome_duplicado: bool = False
    sem_nome: bool = False
    unidade_ausente: bool = False
    coluna_vazia: bool = False


@dataclass
class RelatorioInspecao:
    features: list[FeatureInfo] = field(default_factory=list)
    total_colunas: int = 0
    n_linhas_dados: int = 0
    xlsx_existe: bool = False


def _limpar(valor: object) -> str:
    """Remove espacos extras nas bordas; preserva string vazia."""

    if valor is None:
        return ""
    texto = str(valor).strip()
    return texto


def _ler_cabecalhos(csv_path: Path) -> tuple[list[str], list[str]]:
    cabecalho = pd.read_csv(
        csv_path,
        sep=CSV_SEPARATOR,
        encoding=CSV_ENCODING,
        header=None,
        nrows=2,
        dtype=str,
        keep_default_na=False,
    )
    nomes = [_limpar(v) for v in cabecalho.iloc[0]]
    unidades = [_limpar(v) for v in cabecalho.iloc[1]]
    return nomes, unidades


def _ler_dados_brutos(csv_path: Path) -> pd.DataFrame:
    """Le os dados (linha 3 em diante) mantendo tudo como texto (sem parsing)."""

    return pd.read_csv(
        csv_path,
        sep=CSV_SEPARATOR,
        encoding=CSV_ENCODING,
        header=None,
        skiprows=2,
        dtype=str,
        keep_default_na=False,
    )


def _valor_e_nulo(valor: str) -> bool:
    return valor.strip().lower() in NULL_TOKENS


def _inferir_tipo(valores_coluna: list[str]) -> tuple[str, bool]:
    """Infere o tipo (text/int/float) a partir dos valores nao nulos.

    Retorna (tipo, coluna_100pct_vazia).
    """

    nao_nulos = [v.strip() for v in valores_coluna if not _valor_e_nulo(v)]

    if not nao_nulos:
        return "vazio (sem dados)", True

    def para_float(texto: str) -> float | None:
        # Dados usam virgula decimal (padrao BR). Ex: "7,485686919"
        candidato = texto.replace(".", "").replace(",", ".") if "," in texto else texto
        try:
            return float(candidato)
        except ValueError:
            return None

    convertidos = [para_float(v) for v in nao_nulos]
    if all(c is not None for c in convertidos):
        todos_inteiros = all(float(c).is_integer() for c in convertidos)  # type: ignore[arg-type]
        return ("int", False) if todos_inteiros else ("float", False)

    return "text", False


def inspecionar(csv_path: Path = CSV_PATH, xlsx_path: Path = XLSX_PATH) -> RelatorioInspecao:
    nomes, unidades = _ler_cabecalhos(csv_path)
    dados = _ler_dados_brutos(csv_path)

    total_colunas = len(nomes)
    contagem_nomes: dict[str, int] = {}
    for nome in nomes:
        if nome:
            contagem_nomes[nome] = contagem_nomes.get(nome, 0) + 1

    features: list[FeatureInfo] = []
    for indice in range(total_colunas):
        nome = nomes[indice]
        unidade = unidades[indice]
        coluna_valores = (
            dados[indice].tolist() if indice in dados.columns else []
        )
        tipo, vazia = _inferir_tipo(coluna_valores)

        features.append(
            FeatureInfo(
                posicao=indice + 1,
                indice=indice,
                nome_bruto=nome,
                unidade_bruta=unidade,
                tipo=tipo,
                nome_duplicado=bool(nome) and contagem_nomes.get(nome, 0) > 1,
                sem_nome=not nome,
                unidade_ausente=not unidade,
                coluna_vazia=vazia,
            )
        )

    return RelatorioInspecao(
        features=features,
        total_colunas=total_colunas,
        n_linhas_dados=len(dados),
        xlsx_existe=xlsx_path.exists(),
    )


def imprimir_relatorio(relatorio: RelatorioInspecao, dados_preview: pd.DataFrame) -> None:
    print("=" * 78)
    print("VERIFICACAO DE ARQUIVOS")
    print("=" * 78)
    print(f"CSV utilizado : {CSV_PATH}")
    print(f"XLSX esperado : {XLSX_PATH}")
    print(f"XLSX existe?  : {'sim' if relatorio.xlsx_existe else 'nao'}")
    if not relatorio.xlsx_existe:
        print("  -> Nenhuma acao tomada sobre o xlsx (arquivo nao encontrado).")

    print()
    print("=" * 78)
    print("PRIMEIRAS 5 LINHAS DE DADOS (sem cabecalho, valores brutos como texto)")
    print("=" * 78)
    with pd.option_context("display.max_columns", 8, "display.width", 160):
        print(dados_preview.head(5).iloc[:, :8].to_string(index=False, header=False))
    print(f"(exibindo apenas as 8 primeiras das {relatorio.total_colunas} colunas; "
          f"veja Docs/ricardo.md para a lista completa)")

    print()
    print("=" * 78)
    print("LISTA DE FEATURES (posicao | nome | unidade | tipo)")
    print("=" * 78)
    for f in relatorio.features:
        nome_exibicao = f.nome_bruto if f.nome_bruto else "<SEM NOME>"
        unidade_exibicao = f.unidade_bruta if f.unidade_bruta else "<AUSENTE>"
        flags = []
        if f.nome_duplicado:
            flags.append("DUPLICADO")
        if f.coluna_vazia:
            flags.append("100% VAZIA")
        flags_txt = f" [{', '.join(flags)}]" if flags else ""
        print(f"{f.posicao:3d}. {nome_exibicao:<25s} | unidade: {unidade_exibicao:<10s} | tipo: {f.tipo}{flags_txt}")

    duplicados = sorted({f.nome_bruto for f in relatorio.features if f.nome_duplicado})
    sem_nome = [f.posicao for f in relatorio.features if f.sem_nome]
    unidade_ausente = [f.posicao for f in relatorio.features if f.unidade_ausente]
    colunas_vazias = [f.posicao for f in relatorio.features if f.coluna_vazia]

    print()
    print("=" * 78)
    print("VALIDACOES")
    print("=" * 78)
    print(f"Total de colunas            : {relatorio.total_colunas}")
    print(f"Total de linhas de dados    : {relatorio.n_linhas_dados}")
    print(f"Nomes duplicados ({len(duplicados)}): {duplicados}")
    print(f"Colunas sem nome ({len(sem_nome)}): posicoes {sem_nome}")
    print(f"Unidades ausentes ({len(unidade_ausente)}): posicoes {unidade_ausente}")
    print(f"Colunas 100% vazias ({len(colunas_vazias)}): posicoes {colunas_vazias}")
    print()
    print("Obs.: CSV nao possui conceito de 'celulas mescladas' (isso e proprio")
    print("de planilhas .xlsx). Como results_hydrogen_v2.xlsx nao foi encontrado,")
    print("essa verificacao nao se aplica nesta etapa.")


def gerar_tabela_markdown(relatorio: RelatorioInspecao) -> str:
    linhas = ["| Posicao | Nome | Unidade | Tipo | Observacoes |",
              "|---|---|---|---|---|"]
    for f in relatorio.features:
        nome = f.nome_bruto if f.nome_bruto else "_(sem nome)_"
        unidade = f.unidade_bruta if f.unidade_bruta else "_(ausente)_"
        obs = []
        if f.nome_duplicado:
            obs.append("nome duplicado")
        if f.sem_nome:
            obs.append("sem nome")
        if f.unidade_ausente:
            obs.append("sem unidade")
        if f.coluna_vazia:
            obs.append("100% vazia")
        obs_txt = ", ".join(obs) if obs else "-"
        linhas.append(f"| {f.posicao} | {nome} | {unidade} | {f.tipo} | {obs_txt} |")
    return "\n".join(linhas)


def gerar_ricardo_md(relatorio: RelatorioInspecao, destino: Path = DOCS_DIR / "ricardo.md") -> Path:
    duplicados = sorted({f.nome_bruto for f in relatorio.features if f.nome_duplicado})
    sem_nome = [f.posicao for f in relatorio.features if f.sem_nome]
    unidade_ausente = [f.posicao for f in relatorio.features if f.unidade_ausente]
    colunas_vazias = [f.posicao for f in relatorio.features if f.coluna_vazia]

    conteudo = f"""# Inspecao de Features - results_hydrogen_v2.csv

> Documento gerado por `src/inspecionar_results_hydrogen_v2.py`. Etapa somente de
> leitura/documentacao: nenhuma limpeza definitiva ou selecao de features foi
> feita aqui. Serve de base para a proxima etapa de EDA.

## Arquivos verificados

- CSV: `dados_amostra/results_hydrogen_v2.csv` (usado nesta inspecao)
- XLSX: `dados_amostra/results_hydrogen_v2.xlsx` -> **{"encontrado" if relatorio.xlsx_existe else "NAO encontrado"}**
  (nenhuma alteracao foi feita nele; verificacao de celulas mescladas nao se
  aplica pois o arquivo nao existe na pasta)

## Estrutura do arquivo

- Linha 1: nomes das features
- Linha 2: unidades
- Linha 3 em diante: dados experimentais ({relatorio.n_linhas_dados} linhas)
- Separador: `;` | Decimal: `,` | Encoding: UTF-8 com BOM

## Validacoes

| Verificacao | Resultado |
|---|---|
| Total de colunas | {relatorio.total_colunas} |
| Total de linhas de dados | {relatorio.n_linhas_dados} |
| Nomes duplicados | {len(duplicados)} -> {duplicados} |
| Colunas sem nome | {len(sem_nome)} -> posicoes {sem_nome} |
| Unidades ausentes | {len(unidade_ausente)} -> posicoes {unidade_ausente} |
| Colunas 100% vazias | {len(colunas_vazias)} -> posicoes {colunas_vazias} |

Observacao: nomes duplicados ocorrem porque o arquivo repete um bloco de
features "resumo" no inicio e depois apresenta a tabela completa de medicoes
(ideia ja documentada em `src/leitura_dados.py`). Unidades ausentes/marcadas
como `-` ou `[?]` foram mantidas exatamente como estao na fonte; nenhuma
unidade foi inferida ou inventada.

## Lista de features e unidades

{gerar_tabela_markdown(relatorio)}

## Features selecionadas para o projeto

_(a preencher em etapa futura - nenhuma feature foi selecionada automaticamente)_
"""

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")
    return destino


if __name__ == "__main__":
    relatorio = inspecionar()
    preview = _ler_dados_brutos(CSV_PATH)
    imprimir_relatorio(relatorio, preview)
    caminho_md = gerar_ricardo_md(relatorio)
    print()
    print(f"Documentacao gerada em: {caminho_md}")
