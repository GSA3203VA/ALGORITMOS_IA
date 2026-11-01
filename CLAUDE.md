# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Diretrizes obrigatórias

1. **Restrição de Escopo:** Este é um repositório multi-projeto (Cursos e Tese). Nunca tente ler arquivos fora da pasta do subprojeto em que fomos inicializados.
2. **Proibição de Leitura de Dados:** Nunca leia arquivos dentro de pastas `dados_bruto/` ou `dados_brutos/`, nem arquivos com extensão `.csv` ou `.dat`.
3. **Uso de Amostras:** Para entender a estrutura dos dados ao corrigir ou criar scripts em `src/`, leia única e exclusivamente `dados_amostra/` ou os metadados em `docs/` (ex.: `DOUTORADO/docs/Legenda_Features.md` e `ricardo.md` descrevem as features/unidades da base de hidrogênio).
4. **Estilo de Código:** Prefira scripts Python estruturados e limpos, com boas práticas de Machine Learning e Pandas.

Regras de `AGENTS.md` (valem também aqui):
- Usar o ambiente virtual existente em `.venv/` (na raiz do repositório).
- Não alterar arquivos fora da pasta solicitada; não apagar arquivos sem confirmação.
- Não executar `git commit`, `git push` ou `git reset` sem autorização.
- Antes de criar ou alterar código, explicar o plano resumidamente.
- Em notebooks Jupyter, comentar o código em português.
- Ao instalar bibliotecas, atualizar `requirements.txt`.
- Salvar gráficos e resultados em `resultados/` da disciplina, quando existir (a pasta é ignorada pelo Git).

## Ambiente e comandos

Windows + PowerShell. Não há build, lint nem suíte de testes. O trabalho é feito em notebooks e scripts avulsos.

```powershell
.\.venv\Scripts\Activate.ps1                 # ativar o venv (a partir da raiz)
pip install -r requirements.txt               # dependências (pandas 3, numpy 2, scikit-learn, seaborn, jupyterlab, bs4)
jupyter lab                                   # notebooks
python CURSO_IA\DOUTORADO\src\leitura_dados.py   # scripts rodam isolados; caminhos resolvidos via Path(__file__)
python CURSO_IA\GERAL\src\html_to_ipynb.py <arquivo.html> [-o saida.ipynb]  # reconstrói .ipynb a partir do HTML exportado do Jupyter
```

`requirements.txt` está em **UTF-8 sem BOM**. No Windows PowerShell 5.1, `pip freeze > requirements.txt` grava em UTF-16, e `Out-File -Encoding utf8` acrescenta um BOM. Para atualizar o arquivo sem mudar a codificação, use o Git Bash (`pip freeze > requirements.txt`) ou `[IO.File]::WriteAllLines("$PWD\requirements.txt", (pip freeze))` no PowerShell.

## Arquitetura

- `CURSO_IA/<DISCIPLINA>/` é um subprojeto independente por disciplina da especialização "IA para Engenheiros". Todos seguem o layout `dados_amostra/`, `dados_bruto/` (local, fora do Git), `docs/`, `notebooks/`, `src/` e `resultados/`. Não há código compartilhado entre disciplinas, nem pacote instalável.
- `docs/` costuma ter os enunciados dos labs exportados em HTML (`Lab*.html`). `GERAL/` e alguns `notebooks/` têm utilitários para converter HTML para `.ipynb`/`.py` e para baixar materiais do Moodle. `src/` normalmente guarda versões `.py` (comentadas) de notebooks.
- `DOUTORADO/` é a tese (dados de motor a hidrogênio/knock). É o único subprojeto com pipeline em `src/`:
  - **`src/caminhos.py` é a única fonte de caminhos** (`DADOS_AMOSTRA_DIR`, `DADOS_BRUTO_DIR`, `DOCS_DIR`, `NOTEBOOKS_DIR`, `RESULTADOS_DIR`). Scripts e notebooks importam dele; não monte caminhos à mão. Os notebooks começam com uma célula que sobe até a pasta `DOUTORADO`, adiciona `src/` ao `sys.path` e faz `from caminhos import ...`.
  - `leitura_dados.py` lê `dados_bruto/Resultados_H2.csv` (CSV `;`, codificação `cp850`, **duas linhas de cabeçalho: nomes + unidades**) e cruza com `docs/Legenda_Features.md`.
  - `inspecionar_results_hydrogen_v2.py` faz inspeção somente leitura de `dados_amostra/results_hydrogen_v2.csv` (`utf-8-sig`, `;`) e gera `docs/ricardo.md`. Não inventa unidades ausentes.
  - `gerar_*_pdf.py` geram PDFs de apresentação em `resultados/` a partir dos `.md` em `docs/`, sem ler dados.
  - `docs/Roteiro.md` define o objetivo: análise de features → EDA (`Resumo_ADEC.md`/`Tarefa_ADEC.md`) → clusterização (`Resumo_AMCLASS.md`/`Tarefa_Cluster.md`), usando ADEC, AMCLASS e CLUSTER como material de referência.
  - Todas as pastas estão em minúsculas. No Windows o Git está com `core.ignorecase=true`, então para mudar só a caixa de um nome é preciso passar por um nome temporário (`git mv Pasta tmp; git mv tmp pasta`).
- `PAD/` é uma área confidencial, ignorada pelo Git. Não leia nem cite o conteúdo dela.
- `.gitattributes` força LF em `.py`, `.ipynb`, `.md`, `.json` e `.yaml`. `.gitignore` exclui `*.dat`, `*.pdf`, `dados_bruto/`, `dados_brutos/` e `resultados/` em qualquer nível. CSV só são ignorados dentro de `CURSO_IA/DOUTORADO/`, exceto os de `dados_amostra/`. Nas outras disciplinas os CSV dos exercícios são rastreados, então um CSV novo fora do DOUTORADO entra no Git se não estiver em `dados_bruto/`.
