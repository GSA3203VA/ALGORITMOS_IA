"""Leitura padronizada da base Resultados_H2.

O arquivo CSV possui duas linhas de cabecalho: nomes das features e unidades.
A primeira parte do arquivo repete as features descritas na legenda; depois de
uma coluna vazia vem a tabela completa de medicoes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "Dados" / "Resultados_H2.csv"
LEGEND_PATH = ROOT_DIR / "Docs" / "Legenda_Features.md"

CSV_ENCODING = "cp850"
LEGEND_ENCODING = "utf-8"
CSV_SEPARATOR = ";"


@dataclass(frozen=True)
class ResultadosH2:
    """Pacote com dados, metadados e recorte das features documentadas."""

    completo: pd.DataFrame
    features_legenda: pd.DataFrame
    metadados: pd.DataFrame
    legenda: pd.DataFrame


def ler_legenda_features(path: Path = LEGEND_PATH) -> pd.DataFrame:
    """Le a legenda em Markdown e retorna feature/descricao."""

    linhas = path.read_text(encoding=LEGEND_ENCODING).splitlines()
    registros: list[dict[str, str]] = []

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith("#") or ":" not in linha:
            continue

        feature, descricao = linha.split(":", 1)
        feature = feature.strip()
        descricao = re.sub(r"\s+", " ", descricao.strip())
        if feature:
            registros.append({"feature": feature, "descricao": descricao})

    return pd.DataFrame(registros)


def _normalizar_texto(valor: object) -> str:
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def _nomes_unicos(nomes: list[str]) -> list[str]:
    vistos: dict[str, int] = {}
    unicos: list[str] = []

    for indice, nome in enumerate(nomes):
        base = nome or f"coluna_{indice:03d}"
        vistos[base] = vistos.get(base, 0) + 1
        unicos.append(base if vistos[base] == 1 else f"{base}__{vistos[base]}")

    return unicos


def _converter_colunas_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas numericas sem forcar colunas textuais/categoricas."""

    convertido = df.copy()
    for coluna in convertido.columns:
        serie = convertido[coluna]
        numerica = pd.to_numeric(serie, errors="coerce")
        preenchidos = serie.notna().sum()

        if preenchidos and numerica.notna().sum() == preenchidos:
            convertido[coluna] = numerica

    return convertido


def ler_resultados_h2(
    data_path: Path = DATA_PATH,
    legend_path: Path = LEGEND_PATH,
) -> ResultadosH2:
    """Carrega o CSV respeitando nomes, unidades e legenda das features."""

    legenda = ler_legenda_features(legend_path)
    descricoes = dict(zip(legenda["feature"], legenda["descricao"]))

    cabecalho = pd.read_csv(
        data_path,
        sep=CSV_SEPARATOR,
        encoding=CSV_ENCODING,
        header=None,
        nrows=2,
        dtype=str,
    )

    nomes_originais = [_normalizar_texto(valor) for valor in cabecalho.iloc[0]]
    unidades = [_normalizar_texto(valor) for valor in cabecalho.iloc[1]]
    colunas_vazias = [
        indice
        for indice, (nome, unidade) in enumerate(zip(nomes_originais, unidades))
        if not nome and not unidade
    ]

    separador = colunas_vazias[0] if colunas_vazias else None
    indices_validos = [
        indice for indice in range(len(nomes_originais)) if indice not in colunas_vazias
    ]

    nomes_filtrados = [nomes_originais[indice] for indice in indices_validos]
    unidades_filtradas = [unidades[indice] for indice in indices_validos]
    nomes_colunas = _nomes_unicos(nomes_filtrados)

    completo = pd.read_csv(
        data_path,
        sep=CSV_SEPARATOR,
        encoding=CSV_ENCODING,
        header=None,
        skiprows=2,
        usecols=indices_validos,
        names=nomes_colunas,
    )
    completo = _converter_colunas_numericas(completo)

    registros_metadados: list[dict[str, object]] = []
    for coluna, indice_original, feature, unidade in zip(
        nomes_colunas, indices_validos, nomes_filtrados, unidades_filtradas
    ):
        secao = (
            "features_resumidas"
            if separador is not None and indice_original < separador
            else "medicoes_completas"
        )
        registros_metadados.append(
            {
                "coluna": coluna,
                "feature_original": feature,
                "unidade": unidade,
                "secao_csv": secao,
                "indice_csv": indice_original,
                "descricao_legenda": descricoes.get(feature, ""),
            }
        )

    metadados = pd.DataFrame(registros_metadados)

    colunas_legenda = metadados.loc[
        (metadados["secao_csv"] == "features_resumidas")
        & (metadados["feature_original"].isin(descricoes)),
        "coluna",
    ].tolist()
    features_legenda = completo[colunas_legenda].copy()

    return ResultadosH2(
        completo=completo,
        features_legenda=features_legenda,
        metadados=metadados,
        legenda=legenda,
    )


if __name__ == "__main__":
    dados = ler_resultados_h2()
    print(f"Base completa: {dados.completo.shape[0]} linhas x {dados.completo.shape[1]} colunas")
    print(
        "Features da legenda: "
        f"{dados.features_legenda.shape[0]} linhas x {dados.features_legenda.shape[1]} colunas"
    )
    print(dados.metadados.query("secao_csv == 'features_resumidas'").to_string(index=False))
