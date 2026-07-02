from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup


def _lines(text: str) -> list[str]:
    """Convert plain text into Notebook source/output line format."""
    if not text:
        return []
    return [line + "\n" for line in text.splitlines()]


def _extract_markdown(cell: Any) -> dict[str, Any] | None:
    rendered = cell.find("div", class_="jp-RenderedMarkdown")
    if not rendered:
        return None

    text = html.unescape(rendered.get_text("\n", strip=False)).strip()
    if not text:
        return None

    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": _lines(text),
    }


def _extract_output(area: Any) -> dict[str, Any] | None:
    """Extract one Jupyter-like output from a HTML output area."""
    # 1) text/plain rendered output
    text_value = html.unescape(area.get_text("\n", strip=False)).strip()
    if text_value:
        return {
            "output_type": "stream",
            "name": "stdout",
            "text": _lines(text_value),
        }

    # 2) image/png if present as base64 src
    img = area.find("img")
    if img and img.get("src", "").startswith("data:image/png;base64,"):
        data = img["src"].split("base64,", 1)[1]
        return {
            "output_type": "display_data",
            "metadata": {},
            "data": {"image/png": data},
        }

    return None


def _extract_code(cell: Any) -> dict[str, Any] | None:
    # JupyterLab HTML can use <div class="highlight"> or plain <pre>
    code_block = cell.find("div", class_="highlight") or cell.find("pre")
    if not code_block:
        return None

    code = html.unescape(code_block.get_text("\n", strip=False)).strip()
    if not code:
        return None

    outputs: list[dict[str, Any]] = []
    for out_area in cell.find_all("div", class_="jp-OutputArea-output"):
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
    with input_html.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    main = soup.find("main")
    if main is None:
        raise ValueError("Não encontrei a tag <main> no HTML.")

    cells: list[dict[str, Any]] = []
    elements = main.find_all("div", class_="jp-Cell", recursive=False)

    for elem in elements:
        classes = elem.get("class", [])

        if "jp-MarkdownCell" in classes:
            cell = _extract_markdown(elem)
            if cell:
                cells.append(cell)

        elif "jp-CodeCell" in classes:
            cell = _extract_code(elem)
            if cell:
                cells.append(cell)

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

    with output_ipynb.open("w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)

    return len(cells)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Converte HTML exportado do JupyterLab em notebook .ipynb"
    )
    parser.add_argument("input_html", type=Path, help="Arquivo HTML de entrada")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("saida.ipynb"),
        help="Arquivo .ipynb de saída (padrão: saida.ipynb)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    total = html_to_notebook(args.input_html, args.output)
    print(f"Notebook salvo como: {args.output}")
    print(f"Total de células reconstruídas: {total}")


if __name__ == "__main__":
    main()