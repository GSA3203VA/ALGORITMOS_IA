"""Gera um PDF com a tabela de features de results_hydrogen_v2.csv.

Nao le o CSV: reaproveita a tabela ja documentada em docs/ricardo.md
(gerada por inspecionar_results_hydrogen_v2.py) e a renderiza paginada
em um PDF, pronta para anexar a uma apresentacao.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT_DIR = Path(__file__).resolve().parents[1]
RICARDO_MD = ROOT_DIR / "docs" / "ricardo.md"
OUT_PATH = ROOT_DIR / "docs" / "Tabela_Features_Hydrogen_v2.pdf"

NAVY = "#1f2a44"
BLUE = "#2f6fed"
GRAY = "#5a6472"
HEADER_BG = "#2f6fed"
ROW_ALT_BG = "#eef2fb"

LINHAS_POR_PAGINA = 45


def ler_tabela_markdown(path: Path = RICARDO_MD) -> list[list[str]]:
    """Extrai a secao 'Lista de features e unidades' do ricardo.md."""

    texto = path.read_text(encoding="utf-8")
    inicio = texto.index("## Lista de features e unidades")
    resto = texto[inicio:]
    fim = resto.find("\n## ", 1)
    bloco = resto if fim == -1 else resto[:fim]

    linhas_tabela = [
        linha.strip() for linha in bloco.splitlines()
        if linha.strip().startswith("|")
    ]
    # remove cabecalho markdown ("| Posicao | ... |") e separador ("|---|...")
    linhas_tabela = linhas_tabela[2:]

    registros = []
    for linha in linhas_tabela:
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        registros.append(celulas)
    return registros


def paginar(registros: list[list[str]], tamanho: int) -> list[list[list[str]]]:
    return [registros[i:i + tamanho] for i in range(0, len(registros), tamanho)]


def desenhar_pagina(pdf: PdfPages, pagina_dados: list[list[str]], indice: int, total_paginas: int,
                     total_features: int) -> None:
    fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 retrato
    ax.axis("off")

    fig.text(0.5, 0.975, "Tabela de Features — results_hydrogen_v2.csv",
              ha="center", fontsize=13, fontweight="bold", color=NAVY)
    fig.text(0.5, 0.955, f"{total_features} colunas no total  |  página {indice} de {total_paginas}",
              ha="center", fontsize=9, color=GRAY)

    colunas = ["Pos.", "Nome", "Unidade", "Tipo", "Observações"]
    linhas_com_espaco = [
        [celulas[0], f" {celulas[1]}", f" {celulas[2]}", f" {celulas[3]}", f" {celulas[4]}"]
        for celulas in pagina_dados
    ]
    tabela = ax.table(
        cellText=linhas_com_espaco,
        colLabels=colunas,
        colWidths=[0.07, 0.25, 0.16, 0.17, 0.35],
        loc="upper center",
        bbox=(0.0, 0.0, 1.0, 0.93),
        cellLoc="left",
    )
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(7.2)

    for (row, col), cell in tabela.get_celld().items():
        cell.set_edgecolor("#d7dce6")
        if row == 0:
            cell.set_facecolor(HEADER_BG)
            cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor(ROW_ALT_BG if row % 2 == 0 else "white")
            cell.set_text_props(color=NAVY)

    pdf.savefig(fig)
    plt.close(fig)


def main() -> Path:
    registros = ler_tabela_markdown()
    paginas = paginar(registros, LINHAS_POR_PAGINA)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUT_PATH) as pdf:
        for i, pagina_dados in enumerate(paginas, start=1):
            desenhar_pagina(pdf, pagina_dados, i, len(paginas), len(registros))

    return OUT_PATH


if __name__ == "__main__":
    caminho = main()
    print(f"PDF gerado em: {caminho}")
