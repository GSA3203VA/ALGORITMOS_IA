"""Gera um PDF de resumo (para apresentacao) do pipeline DOUTORADO.

Nao le nenhum dado bruto/amostra: apenas monta um diagrama fixo com a
estrutura e o proposito de cada etapa do pipeline, com base na
documentacao existente em docs/.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT_DIR = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT_DIR / "docs" / "Resumo_Pipeline_Doutorado.pdf"

NAVY = "#1f2a44"
BLUE = "#2f6fed"
GRAY = "#5a6472"
LIGHT = "#eef2fb"
WHITE = "#ffffff"
ACCENT = "#e8734a"


def box(ax, xy, w, h, title, subtitle, face=LIGHT, edge=BLUE, text_color=NAVY):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.6, edgecolor=edge, facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h * 0.62, title, ha="center", va="center",
            fontsize=11, fontweight="bold", color=text_color, wrap=True)
    ax.text(x + w / 2, y + h * 0.28, subtitle, ha="center", va="center",
            fontsize=8.3, color=GRAY, wrap=True)
    return (x + w / 2, y), (x + w / 2, y + h), (x, y + h / 2), (x + w, y + h / 2)


def arrow(ax, p1, p2, color=GRAY):
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=16,
                         linewidth=1.6, color=color, shrinkA=2, shrinkB=2)
    ax.add_patch(a)


def pagina_diagrama(pdf: PdfPages) -> None:
    fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 paisagem
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    fig.text(0.5, 0.955, "Pipeline DOUTORADO — Knock em Motor a Hidrogênio",
              ha="center", fontsize=16, fontweight="bold", color=NAVY)
    fig.text(0.5, 0.925, "Estrutura de dados, documentação e análise (CURSO_IA/DOUTORADO)",
              ha="center", fontsize=10, color=GRAY)

    # Linha 1 - dados
    b1_bottom, b1_top, b1_left, b1_right = box(
        ax, (0.3, 5.3), 2.6, 1.3,
        "dados_bruto(s)/", "Dados originais e pesados\n(não versionados, não lidos)",
        face="#fdeee8", edge=ACCENT)
    b2_bottom, b2_top, b2_left, b2_right = box(
        ax, (3.4, 5.3), 2.6, 1.3,
        "dados_amostra/", "Amostra p/ desenvolvimento\nresults_hydrogen_v2.csv")
    b3_bottom, b3_top, b3_left, b3_right = box(
        ax, (6.5, 5.3), 3.2, 1.3,
        "docs/", "Legenda de features, resumos\nteóricos e enunciados das tarefas")

    arrow(ax, b1_right, b2_left)
    arrow(ax, b2_right, b3_left)

    # Linha 2 - processamento
    b4_bottom, b4_top, b4_left, b4_right = box(
        ax, (0.3, 3.2), 3.2, 1.3,
        "src/leitura_dados.py", "Lê CSV (cabeçalho duplo),\ncruza com legenda de features")
    b5_bottom, b5_top, b5_left, b5_right = box(
        ax, (3.9, 3.2), 3.2, 1.3,
        "src/inspecionar_...py", "Inspeciona colunas (duplicadas,\nvazias, sem unidade) → gera docs")
    b6_bottom, b6_top, b6_left, b6_right = box(
        ax, (7.5, 3.2), 2.2, 1.3,
        "docs/ricardo.md", "Relatório gerado\nautomaticamente")

    arrow(ax, (b2_bottom[0], b2_bottom[1]), (b4_top[0], b4_top[1]))
    arrow(ax, (b3_bottom[0], b3_bottom[1]), (b5_top[0], b5_top[1]))
    arrow(ax, b5_right, b6_left)

    # Linha 3 - analise
    b7_bottom, b7_top, b7_left, b7_right = box(
        ax, (0.3, 1.1), 3.2, 1.3,
        "notebooks/\nEDA_Knock_Hidrogenio", "Estatísticas, boxplots,\ncorrelações (Tarefa_ADEC)",
        face="#e9f3ec", edge="#2e8b57")
    b8_bottom, b8_top, b8_left, b8_right = box(
        ax, (3.9, 1.1), 3.2, 1.3,
        "Modelagem\n(AMCLASS / Cluster)", "Classificação de knock +\nclusterização (próxima etapa)",
        face="#e9f3ec", edge="#2e8b57")
    b9_bottom, b9_top, b9_left, b9_right = box(
        ax, (7.5, 1.1), 2.2, 1.3,
        "notebooks/\nwaterfall", "Visualização de pressão\npor ciclo de combustão")

    arrow(ax, (b4_bottom[0], b4_bottom[1]), (b7_top[0], b7_top[1]))
    arrow(ax, b7_right, b8_left)
    arrow(ax, (b6_bottom[0], b6_bottom[1]), (b9_top[0], b9_top[1]))

    fig.text(0.5, 0.03,
              "Regra do projeto: scripts/notebooks só leem dados_amostra/ e docs/ — dados_bruto(s)/ nunca é lido diretamente.",
              ha="center", fontsize=8, color=GRAY, style="italic")

    pdf.savefig(fig)
    plt.close(fig)


def pagina_resumo(pdf: PdfPages) -> None:
    fig = plt.figure(figsize=(11.69, 8.27))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.axis("off")

    fig.text(0.5, 0.955, "Resumo por pasta", ha="center", fontsize=16,
              fontweight="bold", color=NAVY)

    itens = [
        ("dados_bruto/ e dados_brutos/",
         "Dados originais e pesados do projeto. Ficam fora do Git (.gitignore) e nunca são lidos "
         "diretamente pelos scripts — apenas documentados (README.md, imagem Waterfall_Pressão)."),
        ("dados_amostra/",
         "Subconjunto dos dados (results_hydrogen_v2.csv, 260 colunas / 83 linhas) usado para "
         "desenvolver e validar os scripts com segurança, sem tocar nos dados brutos."),
        ("docs/",
         "Documentação viva do projeto: roteiro geral, resumos teóricos das disciplinas (ADEC, "
         "AMCLASS, Clusterização), enunciados das tarefas, dicionário de features "
         "(Legenda_Features.md) e o relatório automático ricardo.md."),
        ("src/leitura_dados.py",
         "Módulo de leitura padronizada do CSV Resultados_H2: trata o cabeçalho duplo "
         "(nomes + unidades), cruza com a legenda de features e separa 'features resumidas' "
         "da tabela completa de medições."),
        ("src/inspecionar_results_hydrogen_v2.py",
         "Script somente leitura que varre a amostra, identifica colunas duplicadas/vazias/sem "
         "unidade e gera automaticamente o relatório docs/ricardo.md."),
        ("notebooks/",
         "Análise exploratória de dados (EDA) do knock com hidrogênio — estatísticas, boxplots, "
         "histogramas, correlações — e geração do gráfico 'waterfall' de pressão por ciclo."),
        ("Objetivo do pipeline",
         "Preparar e documentar os dados experimentais de combustão com hidrogênio para, em "
         "seguida, aplicar métodos de classificação (AMCLASS) e clusterização na detecção de knock."),
    ]

    y = 0.88
    for titulo, texto in itens:
        fig.text(0.07, y, f"• {titulo}", fontsize=11.5, fontweight="bold", color=BLUE)
        fig.text(0.10, y - 0.032, texto, fontsize=9.3, color=NAVY, wrap=True,
                  va="top", ha="left")
        y -= 0.115

    pdf.savefig(fig)
    plt.close(fig)


def main() -> Path:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUT_PATH) as pdf:
        pagina_diagrama(pdf)
        pagina_resumo(pdf)
    return OUT_PATH


if __name__ == "__main__":
    caminho = main()
    print(f"PDF gerado em: {caminho}")
