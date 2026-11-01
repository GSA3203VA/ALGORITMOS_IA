"""Caminhos padronizados do subprojeto DOUTORADO.

Ponto unico de definicao das pastas usadas pelos scripts de ``src/`` e pelos
notebooks de ``notebooks/``. Todos os nomes de pasta estao em minusculas para
funcionar igual no Windows e em sistemas sensiveis a maiusculas (Linux/CI).
"""

from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DADOS_AMOSTRA_DIR = ROOT_DIR / "dados_amostra"  # amostras leves, versionadas
DADOS_BRUTO_DIR = ROOT_DIR / "dados_bruto"  # dados originais, fora do Git
DOCS_DIR = ROOT_DIR / "docs"
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
RESULTADOS_DIR = ROOT_DIR / "resultados"  # saidas geradas, fora do Git
