from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup


# ------------------------------------------------------------
# 1. Definição do caminho do arquivo HTML que será convertido
# ------------------------------------------------------------

# Informe aqui o caminho completo do arquivo .html exportado do Jupyter.
# Use r antes das aspas para evitar problema com barras invertidas no Windows.
CAMINHO_HTML = Path(
    r"C:\Users\GSA\Workspace\ALGORITMOS_IA\CURSO_IA\ADEC_ANALISE_DADOS_BALBINOT\AULA01_ESTATISTICA\EXEMPLOS\Lab01B_IAENG.html"
)

# O arquivo de saída terá o mesmo nome, mas com extensão .ipynb.
# Exemplo: Lab01A_IAENG.html -> Lab01A_IAENG.ipynb
CAMINHO_IPYNB = CAMINHO_HTML.with_suffix(".ipynb")


def _normalizar_texto(text: str) -> str:
    """
    Organiza o texto extraído do HTML.

    Esta função:
    - remove espaços desnecessários no fim das linhas;
    - reduz muitas linhas em branco consecutivas;
    - preserva a indentação do código Python.
    """

    if not text:
        return ""

    # Converte entidades HTML, como &lt;, &gt;, &amp;.
    text = html.unescape(text)

    # Padroniza quebras de linha.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove espaços no final das linhas, preservando indentação no início.
    linhas = [linha.rstrip() for linha in text.split("\n")]

    text = "\n".join(linhas)

    # Reduz três ou mais linhas em branco para apenas duas.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _lines(text: str) -> list[str]:
    """
    Converte texto para o formato de linhas usado pelo notebook Jupyter.

    Importante:
    cada linha precisa terminar com \\n para o notebook abrir corretamente.
    """

    text = _normalizar_texto(text)

    if not text:
        return []

    return [line + "\n" for line in text.splitlines()]


def _extract_markdown(cell: Any) -> dict[str, Any] | None:
    """
    Extrai uma célula Markdown do HTML exportado pelo Jupyter/JupyterLab.
    """

    rendered = (
        cell.find("div", class_="jp-RenderedMarkdown")
        or cell.find("div", class_="text_cell_render")
        or cell.find("div", class_="rendered_html")
    )

    if not rendered:
        return None

    # Em Markdown pode ser útil manter separação entre blocos.
    text = rendered.get_text("\n", strip=False)
    text = _normalizar_texto(text)

    if not text:
        return None

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": _lines(text),
    }


def _extract_output(area: Any) -> dict[str, Any] | None:
    """
    Extrai uma saída de célula de código.

    Pode recuperar:
    - texto impresso no output;
    - imagem PNG em base64.
    """

    # ------------------------------------------------------------
    # 1. Tenta extrair imagem PNG, se existir
    # ------------------------------------------------------------

    img = area.find("img")

    if img and img.get("src", "").startswith("data:image/png;base64,"):
        data = img["src"].split("base64,", 1)[1]

        return {
            "output_type": "display_data",
            "metadata": {},
            "data": {
                "image/png": data
            },
        }

    # ------------------------------------------------------------
    # 2. Tenta extrair saída em texto
    # ------------------------------------------------------------

    text_value = area.get_text("\n", strip=False)
    text_value = _normalizar_texto(text_value)

    if text_value:
        return {
            "output_type": "stream",
            "name": "stdout",
            "text": _lines(text_value),
        }

    return None


def _extract_code(cell: Any) -> dict[str, Any] | None:
    """
    Extrai uma célula de código Python do HTML exportado pelo Jupyter/JupyterLab.

    Ponto importante:
    aqui usamos get_text("", strip=False), e não get_text("\\n").
    Isso evita que o BeautifulSoup insira quebras de linha artificiais
    entre spans, palavras, números e símbolos do código.
    """

    code_block = (
        cell.find("div", class_="highlight")
        or cell.find("div", class_="input_area")
        or cell.find("div", class_="jp-InputArea-editor")
        or cell.find("pre")
    )

    if not code_block:
        return None

    # ------------------------------------------------------------
    # Atenção:
    # usar separador "" evita quebrar o código em linhas artificiais.
    # ------------------------------------------------------------

    code = code_block.get_text("", strip=False)
    code = _normalizar_texto(code)

    if not code:
        return None

    outputs: list[dict[str, Any]] = []

    output_areas = cell.find_all("div", class_="jp-OutputArea-output")

    if not output_areas:
        output_areas = cell.find_all("div", class_="output_area")

    for out_area in output_areas:
        out = _extract_output(out_area)

        if out:
            outputs.append(out)

    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": outputs,
        "source": _lines(code),
    }


def html_to_notebook(input_html: Path, output_ipynb: Path) -> int:
    """
    Converte um arquivo HTML exportado do Jupyter/JupyterLab em um arquivo .ipynb.

    Esta versão:
    - não depende obrigatoriamente da tag <main>;
    - procura células no HTML inteiro se necessário;
    - evita quebras de linha artificiais no código;
    - mantém o nome do arquivo, trocando apenas .html por .ipynb.
    """

    # ------------------------------------------------------------
    # 1. Verifica se o arquivo HTML existe
    # ------------------------------------------------------------

    if not input_html.exists():
        raise FileNotFoundError(f"Arquivo HTML não encontrado: {input_html}")

    if input_html.suffix.lower() not in [".html", ".htm"]:
        raise ValueError(
            f"O arquivo informado não possui extensão .html ou .htm: {input_html}"
        )

    # ------------------------------------------------------------
    # 2. Lê o arquivo HTML
    # ------------------------------------------------------------

    with input_html.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # ------------------------------------------------------------
    # 3. Define a área de busca
    # ------------------------------------------------------------

    main = soup.find("main")

    if main is not None:
        area_busca = main
        print("Tag <main> encontrada. Procurando células dentro dela.")
    else:
        area_busca = soup
        print("Tag <main> não encontrada. Procurando células no HTML inteiro.")

    # ------------------------------------------------------------
    # 4. Procura células no padrão JupyterLab
    # ------------------------------------------------------------

    elements = area_busca.find_all("div", class_="jp-Cell")

    # ------------------------------------------------------------
    # 5. Caso não encontre jp-Cell, tenta outros padrões comuns
    # ------------------------------------------------------------

    if not elements:
        print("Não encontrei células com classe jp-Cell.")
        print("Tentando encontrar células com outros padrões comuns...")

        possible_cells = []

        possible_cells.extend(area_busca.find_all("div", class_="cell"))
        possible_cells.extend(area_busca.find_all("div", class_="code_cell"))
        possible_cells.extend(area_busca.find_all("div", class_="text_cell"))
        possible_cells.extend(area_busca.find_all("div", class_="jp-CodeCell"))
        possible_cells.extend(area_busca.find_all("div", class_="jp-MarkdownCell"))

        elements = possible_cells

    # ------------------------------------------------------------
    # 6. Se ainda não encontrou células, interrompe com mensagem clara
    # ------------------------------------------------------------

    if not elements:
        raise ValueError(
            "Não encontrei células do notebook no HTML. "
            "O arquivo pode não ter sido exportado diretamente do Jupyter/JupyterLab, "
            "ou pode estar em um formato diferente."
        )

    cells: list[dict[str, Any]] = []

    # ------------------------------------------------------------
    # 7. Percorre cada célula encontrada
    # ------------------------------------------------------------

    for elem in elements:
        classes = elem.get("class", [])
        classes_texto = " ".join(classes)
        classes_texto_minusculo = classes_texto.lower()

        # --------------------------------------------------------
        # Células Markdown
        # --------------------------------------------------------

        if (
            "jp-MarkdownCell" in classes
            or "text_cell" in classes_texto
            or "markdown" in classes_texto_minusculo
        ):
            cell = _extract_markdown(elem)

            if cell:
                cells.append(cell)
                continue

        # --------------------------------------------------------
        # Células de código
        # --------------------------------------------------------

        if (
            "jp-CodeCell" in classes
            or "code_cell" in classes_texto
            or "input_area" in classes_texto
            or "code" in classes_texto_minusculo
        ):
            cell = _extract_code(elem)

            if cell:
                cells.append(cell)
                continue

        # --------------------------------------------------------
        # Tentativa genérica:
        # primeiro tenta como código, depois como markdown
        # --------------------------------------------------------

        cell = _extract_code(elem)

        if cell:
            cells.append(cell)
            continue

        cell = _extract_markdown(elem)

        if cell:
            cells.append(cell)
            continue

    # ------------------------------------------------------------
    # 8. Monta a estrutura final do notebook
    # ------------------------------------------------------------

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.x",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    # ------------------------------------------------------------
    # 9. Salva o arquivo .ipynb
    # ------------------------------------------------------------

    with output_ipynb.open("w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)

    return len(cells)


def main() -> None:
    """
    Função principal do programa.
    """

    total = html_to_notebook(CAMINHO_HTML, CAMINHO_IPYNB)

    print("-" * 60)
    print(f"Arquivo HTML de entrada: {CAMINHO_HTML}")
    print(f"Notebook salvo como: {CAMINHO_IPYNB}")
    print(f"Total de células reconstruídas: {total}")
    print("-" * 60)


if __name__ == "__main__":
    main()